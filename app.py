import os
import re
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Code Reviewer", page_icon="🛠️", layout="wide")

LANGUAGES = ["Python", "JavaScript", "TypeScript", "Java", "C++", "SQL", "Go", "Rust", "C#", "Ruby", "PHP", "Swift", "Kotlin","R","HTML"]

SYSTEM_PROMPT = """You are a senior software engineer and code-review agent.
Analyze the user's code carefully. Do not invent errors that are not supported by the code.
Return a practical review with:
1. Executive summary
2. Bugs found (severity: Critical/High/Medium/Low)
3. Why each bug happens
4. A corrected version of the code
5. Security concerns
6. Performance/readability improvements
7. Tests that should be added
For every proposed fix, explain the reasoning briefly.
If the code is already correct, say so and focus on improvements.
Keep the answer concise enough to be useful to a developer."""

# put api key in GROQ_API_KEY or enter it in the sidebar.

def get_client():
    key = os.getenv("GROQ_API_KEY") or st.session_state.get("api_key")
    return Groq(api_key=key) if key else None

def heuristic_checks(code, language):
    findings = []
    if language == "Python":
        if re.search(r"except\s*:", code):
            findings.append(("Medium", "Bare except catches every exception and can hide real failures."))
        if re.search(r"eval\s*\(", code):
            findings.append(("Critical", "eval() can execute arbitrary input and is unsafe with untrusted data."))
        if re.search(r"exec\s*\(", code):
            findings.append(("Critical", "exec() can execute arbitrary code and should not be used with untrusted input."))
        if "SELECT " in code.upper() and re.search(r'["\'].*\+.*["\']', code):
            findings.append(("High", "String-built SQL may be vulnerable to SQL injection; use parameterized queries."))
        if "password" in code.lower() and re.search(r'=\s*["\']', code):
            findings.append(("High", "Possible hard-coded credential detected. Move secrets to environment variables."))
    elif language in ["JavaScript", "TypeScript"]:
        if re.search(r"\beval\s*\(", code):
            findings.append(("Critical", "eval() can execute arbitrary JavaScript and is unsafe with untrusted input."))
        if re.search(r"(password|api[_-]?key|secret)\s*=\s*['\"]", code, re.I):
            findings.append(("High", "Possible hard-coded secret detected. Use environment variables or a secret manager."))
    return findings

def review_code(code, language, focus, model):
    client = get_client()
    if not client:
        return None, "Add GROQ_API_KEY in the environment or enter it in the sidebar."

    prompt = f"""Review this {language} code.

Focus areas: {focus}

Code:
```{language.lower()}
{code}
```

Use this exact structure:
## Executive Summary
## Bugs Found
For each issue: **Severity — Title**, then explanation and fix.
## Corrected Code
Provide a complete corrected code block.
## Security
## Performance & Quality
## Recommended Tests
"""
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.1,
            max_tokens=5000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"LLM request failed: {e}"

st.title("🛠️ AI Code Reviewer & Bug Fixing Agent")
st.caption("Generative-AI powered code analysis, bug detection, fixes, security review and test suggestions.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Groq API key", type="password", help="Used only for this Streamlit session.")
    if api_key:
        st.session_state["api_key"] = api_key

    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "openai/gpt-oss-120b"],
        index=0
    )
    language = st.selectbox("Language", LANGUAGES)
    focus = st.multiselect(
        "Review focus",
        ["Correctness", "Security", "Performance", "Readability", "Edge cases", "Testing"],
        default=["Correctness", "Security", "Performance"]
    )

example = """def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

numbers = [10, 20, 30]
print(calculate_average(numbers))
"""

if "code" not in st.session_state:
    st.session_state.code = example

code = st.text_area("Paste your code", height=420, value=st.session_state.code)

c1, c2 = st.columns([1, 1])
with c1:
    review = st.button("🔍 Review & Fix", type="primary", use_container_width=True)
with c2:
    clear = st.button("🧹 Clear", use_container_width=True)

if clear:
    st.session_state.code = ""
    st.rerun()

if review:
    if not code.strip():
        st.warning("Please paste some code first.")
    else:
        st.session_state.code = code
        st.subheader("⚡ Pre-review checks")
        heuristic = heuristic_checks(code, language)
        if heuristic:
            for severity, message in heuristic:
                st.warning(f"**{severity}:** {message}")
        else:
            st.success("No obvious pattern-based issues detected.")

        with st.spinner("AI agent is reviewing the code..."):
            result, error = review_code(code, language, ", ".join(focus), model)

        if error:
            st.error(error)
        else:
            st.subheader("🤖 AI Review")
            st.markdown(result)
            st.download_button(
                "Download review as Markdown",
                data=result,
                file_name="code_review.md",
                mime="text/markdown"
            )

st.divider()
st.markdown("**MVP flow:** Put groq API key → heuristic safety checks → LLM reasoning → bug explanation → corrected code → tests.")
