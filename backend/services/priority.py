from datetime import datetime


def calculate_priority_score(
    severity: str,
    safety_flag: bool = False,
    accessibility_flag: bool = False,
    duplicate_count: int = 0,
    created_at: datetime = None,
    current_status: str = None
) -> int:
    """
    Calculate priority score based on the Kiro requirements:
    - Base severity scores: Low=25, Medium=50, High=70, Critical=90
    - Safety flag = +20
    - Accessibility flag = +15
    - Duration > 7 days = +15
    - Duplicates: 1=+10, 2=+15, 3+=+20
    - Score capped at 100
    
    Duration is only calculated for non-resolved reports.
    """
    # Base severity scores
    severity_scores = {
        "Low": 25,
        "Medium": 50,
        "High": 70,
        "Critical": 90
    }
    
    score = severity_scores.get(severity, 25)
    
    # Safety flag bonus
    if safety_flag:
        score += 20
    
    # Accessibility flag bonus
    if accessibility_flag:
        score += 15
    
    # Duplicate bonus
    if duplicate_count >= 3:
        score += 20
    elif duplicate_count == 2:
        score += 15
    elif duplicate_count == 1:
        score += 10
    
    # Duration bonus (only for non-resolved reports)
    if created_at and current_status not in ["Resolved", "Closed"]:
        try:
            now = datetime.utcnow()
            duration = now - created_at
            days_open = duration.days
            if days_open > 7:
                score += 15
        except Exception:
            pass
    
    # Cap at 100
    return min(score, 100)


def calculate_duration_days(created_at: datetime, current_status: str) -> int:
    """
    Calculate how many days an issue has been open.
    Returns 0 for resolved/closed reports.
    """
    if current_status in ["Resolved", "Closed"]:
        return 0
    
    try:
        now = datetime.utcnow()
        duration = now - created_at
        return max(0, duration.days)
    except Exception:
        return 0


def should_recalculate_priority(
    severity: str,
    safety_flag: bool,
    accessibility_flag: bool,
    duplicate_count: int,
    created_at: datetime,
    current_status: str,
    current_priority: int
) -> tuple:
    """
    Determine if priority should be recalculated based on duration changes.
    Returns (should_recalculate, new_priority) tuple.
    """
    # Only recalculate for active reports
    if current_status in ["Resolved", "Closed"]:
        return False, current_priority
    
    # Calculate what the new priority would be
    new_priority = calculate_priority_score(
        severity=severity,
        safety_flag=safety_flag,
        accessibility_flag=accessibility_flag,
        duplicate_count=duplicate_count,
        created_at=created_at,
        current_status=current_status
    )
    
    # Recalculate if score would be higher
    should_recalculate = new_priority > current_priority
    return should_recalculate, new_priority