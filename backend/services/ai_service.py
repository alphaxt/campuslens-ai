import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)


def analyze_issue(description: str) -> dict:

    prompt = f"""
You are the AI analysis engine for CampusLens AI.

Analyze the following university campus issue:

"{description}"

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "short concise summary",
    "category": "Network | Facilities | Security | Cleanliness | Transport | Accessibility | Academic Facilities | Uncategorized",
    "severity": "Low | Medium | High | Critical",
    "recommended_department": "department responsible for fixing the issue",
    "extracted_location": "location mentioned in the complaint or null",
    "safety_flag": true or false,
    "accessibility_flag": true or false,
    "confidence": number between 0 and 1
}}

Rules:

- Network means Wi-Fi, internet, network or connectivity problems.
- Facilities means electricity, AC, plumbing, furniture or building infrastructure.
- Security means theft, unsafe situations or security concerns.
- Cleanliness means trash, sanitation or cleaning problems.
- Transport means buses, parking or campus transportation.
- Accessibility means barriers affecting disabled or mobility-impaired people.
- Academic Facilities means projectors, computers, laboratories or classroom equipment.

Severity:
Low = inconvenience with little impact.
Medium = affects normal campus activity.
High = significantly affects classes or many users.
Critical = immediate safety risk or serious campus-wide disruption.

Do not include markdown.
Do not include ```json.
Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)