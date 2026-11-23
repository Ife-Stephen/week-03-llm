# Week 3 – Session 5: Prompt Engineering Lab

This project explores how prompt engineering improves AI-generated product descriptions through systematic prompt iteration using the Groq API.

## Prompt Versions Breakdown

1. **Version 1 (V1) - Naive Baseline:** Raw instruction only (*"Write a product description for a solar-powered backpack."*). Results in unstructured, generic text.
2. **Version 2 (V2) - Role + Audience:** Adds persona and geographic/demographic targeting (*"You are an expert E-Commerce Copywriter... targeting tech-savvy outdoor commuters in Lagos"*). Yields much more tailored, engaging copy.
3. **Version 3 (V3) - Tone + Constraints + Few-Shot + JSON Schema:** Enforces strict length limits, professional tone, few-shot examples, and a strict JSON format (`product_name`, `tagline`, `bullet_points`, `target_audience`). Enables programmatic downstream parsing.

---

## Results & Score Comparison Table

Each version was evaluated and scored from 1 to 10 across clarity, specificity, and output structure:

| Version | Clarity (1-10) | Specificity (1-10) | Structure (1-10) | Parseable Output |
|---|---:|---:|---:|---|
| **V1 (Naive Baseline)** | 5/10 | 3/10 | 4/10 | ❌ No (Unstructured Text) |
| **V2 (Role + Audience)** | 8/10 | 8/10 | 6/10 | ❌ No (Unstructured Text) |
| **V3 (JSON Schema + Constraints)** | 10/10 | 9/10 | 10/10 | ✅ Yes (Valid JSON Dictionary) |

---

## Features

- Runs all three prompt versions using the Groq API.
- Evaluates clarity, specificity, and structure.
- Prints a comparison table of prompt scores.
- Parses V3 structured JSON using Python's `json.loads()`.
- Prints individual JSON fields cleanly.
- Displays total token usage.
- Secure API key management using environment variables.
- Handles HTTP and network errors.

## Technologies Used

- Python
- Groq API
- Requests
- Python-dotenv
- JSON
- Pandas

---

## How to Run the Code

1. **Install Dependencies:**

   ```bash
   pip install requests python-dotenv pandas
   ```

2. **Create a `.env` file** in the project folder and add your Groq API key:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

---

## Project Structure

```text
week-03-llm/
├── main.py
├── prompt_lab.ipynb (optional)
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Security

The `.env` file is excluded from Git using `.gitignore` to protect API credentials. Never commit or share your API key.

---

Completed as part of **Week 3 – Session 5: Prompt Engineering Lab & Assignment**.
