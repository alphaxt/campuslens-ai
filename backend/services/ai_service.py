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


def generate_campus_pulse(reports: list) -> dict:

    if not reports:
        return {
            "headline": "No campus reports available",
            "summary": "There is not enough report data to generate a Campus Pulse summary.",
            "major_concern": "No major concern detected.",
            "emerging_trend": "No emerging trend detected.",
            "critical_issue": "No critical issue detected.",
            "improvement": "No improvement data available.",
            "recommended_actions": []
        }


    compact_reports = []

    for report in reports:
        compact_reports.append({
            "summary": report.get("ai_summary"),
            "category": report.get("category"),
            "severity": report.get("severity"),
            "location": report.get("extracted_location"),
            "department": report.get("recommended_department"),
            "priority_score": report.get("priority_score"),
            "status": report.get("status")
        })


    prompt = f"""
You are the Campus Pulse intelligence engine for CampusLens AI.

Analyze the following university campus issue reports:

{json.dumps(compact_reports, indent=2)}

Return ONLY valid JSON using exactly this structure:

{{
    "headline": "short headline about the overall campus situation",
    "summary": "2-3 sentence executive summary",
    "major_concern": "most important current campus concern",
    "emerging_trend": "important pattern visible in the reports",
    "critical_issue": "highest-risk or most urgent issue",
    "improvement": "positive improvement or resolved trend if visible",
    "recommended_actions": [
        "action 1",
        "action 2",
        "action 3"
    ]
}}

Rules:

- Base the response only on the provided reports.
- Prioritize safety and accessibility issues even if their report count is low.
- Consider severity, priority scores, unresolved statuses and repeated categories.
- Do not invent information that is not supported by the reports.
- If there is not enough evidence for an improvement, say "No clear improvement detected."
- Return no markdown.
- Return JSON only.
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