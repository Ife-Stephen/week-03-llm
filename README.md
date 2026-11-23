# Week 3 – Session 5: Prompt Engineering Lab

This project explores how prompt engineering improves AI-generated product descriptions through systematic prompt iteration.

## Prompt Versions
- **V1:** Basic instruction (naive baseline).
- **V2:** Adds expert role and target audience.
- **V3:** Adds tone, word constraints, an example, and JSON schema.

## Features
- Runs all three prompts using the Groq API.
- Evaluates clarity, specificity, and structure on a 1–10 scale.
- Prints a prompt comparison table.
- Parses V3 structured JSON using Python's `json.loads()`.
- Displays individual JSON fields and token usage.
- Uses environment variables to protect the API key.

## Setup
1. Install Python.
2. Create and activate a virtual environment.
3. Install dependencies: `python -m pip install -r requirements.txt`
4. Create `.env` and add `GROQ_API_KEY=your_api_key_here`
5. Run: `python main.py`

## Security
The `.env` file is excluded from Git using `.gitignore`.

**Tools:** Python, Groq API, Requests, Python-dotenv, JSON.

Completed as part of Week 3 – Session 5.