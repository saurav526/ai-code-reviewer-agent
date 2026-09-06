# 🛠️ AI Code Reviewer & Bug Fixing Agent

A 1-week Build Sprint MVP for a Generative AI Developer Intern application.

## What it does

The application accepts source code and combines deterministic heuristic checks with a Generative AI reviewer to:

- detect likely bugs
- explain why bugs occur
- generate corrected code
- identify security risks
- suggest performance/readability improvements
- recommend tests
- export the review as Markdown

## Architecture

```text
User Code
   │
   ▼
Streamlit UI
   │
   ├──► Heuristic Safety Checks
   │       ├── eval/exec
   │       ├── hard-coded secrets
   │       └── basic SQL injection patterns
   │
   ▼
Prompt Construction
   │
   ▼
Groq LLM
   │
   ▼
Structured Code Review
   ├── Bugs
   ├── Explanation
   ├── Corrected Code
   ├── Security
   └── Tests
```

## Tech stack

- Python
- Streamlit
- Groq API
- Llama 3.3 70B / OpenAI GPT OSS model
- Docker

## Run locally

```bash
git clone <your-repository-url>
cd ai-code-reviewer-agent

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Then enter your Groq API key in the sidebar.

You can also configure it as an environment variable:

```bash
# Windows PowerShell
$env:GROQ_API_KEY="your_key"

# macOS/Linux
export GROQ_API_KEY="your_key"
```

## Docker

```bash
docker build -t ai-code-reviewer .
docker run -p 8501:8501 -e GROQ_API_KEY="your_key" ai-code-reviewer
```

Open `http://localhost:8501`.

## Deployment

### Streamlit Community Cloud
1. Push the project to GitHub.
2. Create a new Streamlit deployment.
3. Select `app.py`.
4. Add `GROQ_API_KEY` under Secrets.
5. Deploy.

### Render / Railway / Hugging Face Spaces
Use the included Dockerfile. Expose port `8501` and configure `GROQ_API_KEY` as a secret/environment variable.

## Example test case

Input:

```python
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(calculate_average([]))
```

The agent should identify the empty-list division problem and propose a safe fix.

## Important design decisions

### Why heuristic checks + LLM?
The LLM is strong at reasoning over code, but deterministic checks are useful for obvious security patterns. Combining both makes the MVP more robust and demonstrates that the application is not simply "send code to an LLM and print the answer."

### Why low temperature?
Code review benefits from consistent, less creative responses. The temperature is therefore set to `0.1`.

### Security
API keys are never written to the repository. The UI stores a key only in the current Streamlit session. For deployment, use platform secrets.

## Future improvements

- AST-based Python analysis
- JavaScript/TypeScript parser integration
- repository/ZIP upload
- GitHub pull-request integration
- unit-test generation and execution in a sandbox
- static analyzers such as Ruff, Bandit, ESLint and Semgrep
- agentic multi-step repair + test loop
- RAG over project-specific coding standards
- patch/diff generation
