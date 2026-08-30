import json
import os
import logging

from dotenv import load_dotenv
from google import genai
from google.api_core import exceptions as api_exceptions

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_issue(description: str) -> dict:
    """
    Analyze an issue using Gemini API with fallback handling.
    
    Returns:
        dict: Analysis results with fallback values on API failure
    """
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
Low = cosmetic inconvenience, non-essential equipment, or issue does not significantly disrupt learning, safety, or accessibility (e.g., broken classroom clock, minor furniture issue).
Medium = noticeable disruption but alternatives exist (e.g., one classroom projector unavailable, slow Wi-Fi in one small area).
High = significant disruption affecting classes/services or many students (e.g., network outage in a lab, major cooling failure, important facility unavailable).
Critical = immediate safety risk, serious accessibility issue, emergency, or major campus-wide outage (e.g., exposed electrical wiring, fire hazard, blocked emergency exit).

IMPORTANT: Do not classify ordinary inconvenience as High or Critical.

Do not include markdown.
Do not include ```json.
Return JSON only.
"""

    try:
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

    except api_exceptions.ResourceExhausted as e:
        logger.error(f"Gemini API 429 Resource Exhausted: {e}")
        return get_fallback_analysis(description)
    except api_exceptions.DeadlineExceeded as e:
        logger.error(f"Gemini API Deadline Exceeded (timeout): {e}")
        return get_fallback_analysis(description)
    except api_exceptions.GoogleAPIError as e:
        logger.error(f"Gemini API error: {e}")
        return get_fallback_analysis(description)
    except Exception as e:
        logger.error(f"Unexpected error during AI analysis: {e}")
        return get_fallback_analysis(description)


def get_fallback_analysis(description: str) -> dict:
    """
    Return clean fallback analysis when Gemini API fails.
    
    Uses keyword matching to provide reasonable defaults without exposing
    raw error text to the frontend.
    """
    description_lower = description.lower()
    
    # Keyword-based fallback for category and department
    category = "Uncategorized"
    department = "General Maintenance"
    
    if any(word in description_lower for word in ["wifi", "internet", "network", "connection", "internet"]):
        category = "Network"
        department = "IT Support"
    elif any(word in description_lower for word in ["electric", "power", "light", "ac", "cooling", "heater"]):
        category = "Facilities"
        department = "Facilities Management"
    elif any(word in description_lower for word in ["security", "theft", "unsafe", "danger", "threat"]):
        category = "Security"
        department = "Campus Security"
    elif any(word in description_lower for word in ["trash", "sanitation", "clean", "dirty", "garbage"]):
        category = "Cleanliness"
        department = "Campus Cleaning"
    elif any(word in description_lower for word in ["bus", "parking", "transport", "shuttle"]):
        category = "Transport"
        department = "Transportation Services"
    elif any(word in description_lower for word in ["accessible", "wheelchair", "ramp", "disabled", "handicap"]):
        category = "Accessibility"
        department = "Accessibility Services"
    elif any(word in description_lower for word in ["projector", "computer", "lab", "classroom equipment", "whiteboard"]):
        category = "Academic Facilities"
        department = "Academic Facilities"
    
    # Keyword-based fallback for severity
    severity = "Medium"
    if any(word in description_lower for word in ["critical", "emergency", "dangerous", "life-threatening", "immediate"]):
        severity = "Critical"
    elif any(word in description_lower for word in ["high", "urgent", "major", "significant"]):
        severity = "High"
    elif any(word in description_lower for word in ["low", "minor", "cosmetic", "small"]):
        severity = "Low"
    
    # Safety and accessibility flags based on keywords
    safety_flag = any(word in description_lower for word in ["danger", "unsafe", "emergency", "hazard", "threat"])
    accessibility_flag = any(word in description_lower for word in ["accessible", "wheelchair", "ramp", "disabled", "handicap", "mobility"])
    
    # Extract location if mentioned
    extracted_location = None
    if "building" in description_lower or "room" in description_lower:
        # Simple extraction - look for "building X" or "room X"
        import re
        building_match = re.search(r'(building\s+\w+)', description_lower)
        room_match = re.search(r'(room\s+\w+)', description_lower)
        extracted_location = building_match.group(1) if building_match else room_match.group(1) if room_match else None
    
    return {
        "summary": f"Issue reported: {description[:100]}...",
        "category": category,
        "severity": severity,
        "recommended_department": department,
        "extracted_location": extracted_location,
        "safety_flag": safety_flag,
        "accessibility_flag": accessibility_flag,
        "confidence": 0.0
    }


def generate_campus_pulse(reports: list) -> dict:
    """
    Generate campus pulse summary using Gemini API with fallback handling.
    
    Returns:
        dict: Campus pulse summary with fallback values on API failure
    """
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

    try:
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

    except api_exceptions.ResourceExhausted as e:
        logger.error(f"Gemini API 429 Resource Exhausted: {e}")
        return get_fallback_campus_pulse(compact_reports)
    except api_exceptions.DeadlineExceeded as e:
        logger.error(f"Gemini API Deadline Exceeded (timeout): {e}")
        return get_fallback_campus_pulse(compact_reports)
    except api_exceptions.GoogleAPIError as e:
        logger.error(f"Gemini API error: {e}")
        return get_fallback_campus_pulse(compact_reports)
    except Exception as e:
        logger.error(f"Unexpected error during campus pulse generation: {e}")
        return get_fallback_campus_pulse(compact_reports)


def get_fallback_campus_pulse(reports: list) -> dict:
    """
    Return clean fallback campus pulse when Gemini API fails.
    
    Uses simple aggregation to provide basic stats without exposing
    raw error text to the frontend.
    """
    # Calculate basic stats
    total_reports = len(reports)
    categories = {}
    severities = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    open_issues = 0
    critical_issues = []
    
    for report in reports:
        # Count categories
        cat = report.get("category", "Uncategorized")
        categories[cat] = categories.get(cat, 0) + 1
        
        # Count severities
        sev = report.get("severity", "Medium")
        if sev in severities:
            severities[sev] += 1
        
        # Count open issues
        if report.get("status") == "Open":
            open_issues += 1
        
        # Track critical issues
        if report.get("severity") == "Critical":
            critical_issues.append(report.get("summary", "Unknown issue"))
    
    # Determine major concern based on critical issues
    major_concern = "No major concern detected."
    if critical_issues:
        major_concern = critical_issues[0] if len(critical_issues) == 1 else f"{len(critical_issues)} critical issues require attention."
    elif severities["High"] > 0:
        major_concern = f"{severities['High']} high-severity issues require attention."
    elif open_issues > 0:
        major_concern = f"{open_issues} open issues pending resolution."
    
    # Determine emerging trend
    emerging_trend = "No emerging trend detected."
    if categories:
        most_common = max(categories.items(), key=lambda x: x[1])
        if most_common[1] >= 2:
            emerging_trend = f"{most_common[1]} reports in the '{most_common[0]}' category suggest a recurring issue."
    
    # Determine improvement
    improvement = "No clear improvement detected."
    if severities["Critical"] == 0 and severities["High"] > 0:
        improvement = "No critical issues currently reported, which is a positive sign."
    
    # Build recommended actions
    recommended_actions = []
    if severities["Critical"] > 0:
        recommended_actions.append(f"Address {severities['Critical']} critical issue(s) immediately.")
    if severities["High"] > 0:
        recommended_actions.append(f"Review {severities['High']} high-severity issue(s).")
    if "Network" in categories:
        recommended_actions.append("Check network infrastructure for common issues.")
    if "Facilities" in categories:
        recommended_actions.append("Schedule facilities inspection for reported issues.")
    
    if not recommended_actions:
        recommended_actions.append("Continue monitoring campus issues.")
        recommended_actions.append("Address issues as they arise.")
        recommended_actions.append("Prioritize based on severity.")
    
    return {
        "headline": f"Campus Status: {open_issues} Open Issues",
        "summary": f"Total of {total_reports} campus reports. {open_issues} remain unresolved. {major_concern}",
        "major_concern": major_concern,
        "emerging_trend": emerging_trend,
        "critical_issue": "None detected" if not critical_issues else critical_issues[0],
        "improvement": improvement,
        "recommended_actions": recommended_actions[:3]  # Return at most 3 actions
    }
