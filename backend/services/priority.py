def calculate_priority(
    severity: str,
    safety_flag: bool = False,
    accessibility_flag: bool = False,
    duplicate_count: int = 0
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

    # Duplicate impact on original report
    if duplicate_count == 1:
        score += 10
    elif duplicate_count == 2:
        score += 15
    elif duplicate_count >= 3:
        score += 20

    return min(score, 100)