# Build Sprint Submission

## Assignment
AI Code Reviewer & Bug Fixing Agent

## GitHub Repository
PASTE_GITHUB_REPOSITORY_LINK_HERE

## Live Demo
PASTE_DEPLOYED_LINK_HERE

## Short Explanation

I built an AI-powered code review and bug-fixing MVP that combines deterministic heuristic security checks with a Generative AI code-review agent. Users can select a programming language, paste code, choose review priorities, and receive a structured analysis covering bugs, severity, explanations, corrected code, security concerns, performance/readability improvements, and recommended tests.

The main goal was to demonstrate practical GenAI application development rather than only a chatbot wrapper. The pipeline first performs lightweight deterministic checks for obvious risky patterns and then passes the code plus review requirements to a Groq-hosted LLM using a constrained engineering prompt. The final review can be exported as Markdown.

## Technologies
Python, Streamlit, Groq API, Llama 3.3 70B, Docker.

## Key Engineering Decisions
- Deterministic checks supplement LLM reasoning.
- Low temperature for consistent technical output.
- API keys are handled through environment variables/secrets.
- Dockerfile enables reproducible deployment.
- The code is structured to make future static-analysis and sandboxed test execution easy.

## Demo Flow
1. Open the deployed application.
2. Select Python.
3. Paste code containing a bug.
4. Click Review & Fix.
5. Inspect deterministic checks.
6. Inspect AI-generated bug analysis and corrected code.
7. Download the review as Markdown.

## Future Scope
Repository-level review, AST/static-analysis integration, sandboxed test execution, GitHub PR integration, code-diff generation, project-specific RAG, and multi-agent repair/test loops.
