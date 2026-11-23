import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"

if not API_KEY:
    print("Error: GROQ_API_KEY is missing from .env")
    raise SystemExit(1)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# PROMPT V1: NAIVE BASELINE

prompt_v1 = """
Write a product description for a solar-powered backpack.
"""

# PROMPT V2: ROLE + AUDIENCE

prompt_v2 = """
You are an expert E-Commerce Copywriter.
Write a product description for a solar-powered backpack
targeting tech-savvy outdoor commuters in Lagos.
"""


# PROMPT V3: ROLE + TONE + CONSTRAINTS + JSON

prompt_v3 = """
You are an expert Copywriter.

Write a product description for a solar-powered backpack
targeting commuters.

Tone: Professional and inspiring.
Length: Under 80 words.

Return valid JSON only using these exact keys:
- product_name
- tagline
- bullet_points (an array of strings)
- target_audience

Example JSON structure:
{
    "product_name": "SolarPack",
    "tagline": "Power your journey",
    "bullet_points": [
        "Solar charging capability",
        "Comfortable design"
    ],
    "target_audience": "Daily commuters"
}

Ensure the output is valid JSON and contains all four keys.
"""

# API FUNCTION

def call_groq(prompt, json_mode=False):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    response = requests.post(
        URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})

    return content, usage


# RUN ALL THREE PROMPT VERSIONS

results = {}
total_tokens = 0

try:
    print("\nGenerating V1...")
    results["V1"] , usage1 = call_groq(prompt_v1)
    total_tokens += usage1.get("total_tokens", 0)

    print("Generating V2...")
    results["V2"], usage2 = call_groq(prompt_v2)
    total_tokens += usage2.get("total_tokens", 0)

    print("Generating V3...")
    results["V3"], usage3 = call_groq(prompt_v3, json_mode=True)
    total_tokens += usage3.get("total_tokens", 0)

    # Display all generated responses
    print("\n" + "=" * 60)
    print("PROMPT ENGINEERING RESULTS")
    print("=" * 60)

    for version, output in results.items():
        print(f"\n--- {version} OUTPUT ---")
        print(output)


    # EVALUATE ALL THREE RESPONSES

    evaluation_prompt = f"""
You are an objective prompt quality evaluator.

Evaluate these three product description outputs:
{json.dumps(results, indent=2)}

Score EACH version from 1 to 10 on:
1. clarity
2. specificity
3. structure

Use integer scores from 1 to 10.

Return JSON only using this structure:
{{
    "V1": {{
        "clarity": 1,
        "specificity": 1,
        "structure": 1
    }},
    "V2": {{
        "clarity": 1,
        "specificity": 1,
        "structure": 1
    }},
    "V3": {{
        "clarity": 1,
        "specificity": 1,
        "structure": 1
    }}
}}
"""

    print("\nScoring responses...")

    evaluation_text, evaluation_usage = call_groq(
        evaluation_prompt,
        json_mode=True
    )

    total_tokens += evaluation_usage.get("total_tokens", 0)
    scores = json.loads(evaluation_text)


    # PRINT COMPARISON TABLE

    print("\n" + "=" * 60)
    print("PROMPT COMPARISON SCORE (1-10)")
    print("=" * 60)

    print(f"{'Version':<10}{'Clarity':<12}{'Specificity':<15}{'Structure':<12}{'Average':<10}")
    print("-" * 59)

    for version in ["V1", "V2", "V3"]:
        clarity = scores[version]["clarity"]
        specificity = scores[version]["specificity"]
        structure = scores[version]["structure"]

        average = (clarity + specificity + structure) / 3

        print(
            f"{version:<10}"
            f"{clarity:<12}"
            f"{specificity:<15}"
            f"{structure:<12}"
            f"{average:.2f}"
        )

    # PARSE V3 JSON

    print("\n" + "=" * 60)
    print("STRUCTURED V3 OUTPUT")
    print("=" * 60)

    v3_data = json.loads(results["V3"])

    print("Product Name:", v3_data["product_name"])
    print("Tagline:", v3_data["tagline"])
    print("Target Audience:", v3_data["target_audience"])

    print("Bullet Points:")
    for point in v3_data["bullet_points"]:
        print("-", point)


    # TOKEN USAGE

    print("\n" + "=" * 60)
    print("TOTAL TOKEN USAGE")
    print("=" * 60)
    print("All API calls combined:", total_tokens)


except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)
    print("Response:", e.response.text if e.response is not None else "No response")

except requests.exceptions.RequestException as e:
    print("Network Error:", e)

except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
    print("Response parsing error:", e)

except Exception as e:
    print("Unexpected error:", e)