def calculate_priority(
    severity: str,
    safety_flag: bool = False,
    accessibility_flag: bool = False
) -> int:

    severity_scores = {
        "Low": 25,
        "Medium": 50,
        "High": 75,
        "Critical": 90
    }

    score = severity_scores.get(severity, 25)

    if safety_flag:
        score += 10

    if accessibility_flag:
        score += 10

    return min(score, 100)