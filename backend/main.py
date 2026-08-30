from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from services.auth import (
    get_authenticated_user,
    get_admin_user,
    get_student_user
)

from services.duplicate import (
    find_best_duplicate
)

from models.report import ReportRequest, StatusUpdateRequest


from services.database import (
    save_report,
    get_all_reports,
    get_report_by_id,
    update_report_status,
    add_status_history,
    get_status_history,
    get_active_reports,
    save_duplicate_relationship,
    get_duplicate_count,
    update_report_priority,
    get_reports_for_priority_update
)

from services.ai_service import (
    analyze_issue,
    generate_campus_pulse
)
from services.priority import calculate_priority_score, calculate_duration_days, should_recalculate_priority

app = FastAPI(
    title="CampusLens AI API",
    description="Backend API for CampusLens AI",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {
        "message": "CampusLens AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/reports")
def create_report(
    report: ReportRequest,
    current_user: dict = Depends(
        get_student_user
    )
):

    try:
        # Analyze the issue - this will return fallback analysis on API failure
        # and never raise an exception (handled inside analyze_issue)
        analysis = analyze_issue(
            report.description
        )

        active_reports = get_active_reports(
            current_user["token"]
        )

        duplicate_result = find_best_duplicate(
            description=report.description,
            category=analysis["category"],
            location=analysis.get(
                "extracted_location"
            ),
            reports=active_reports
        )

        # Calculate priority score with duration
        # For new reports, created_at is not yet available, so we use None initially
        priority_score = calculate_priority_score(
            severity=analysis["severity"],
            safety_flag=analysis.get(
                "safety_flag",
                False
            ),
            accessibility_flag=analysis.get(
                "accessibility_flag",
                False
            ),
            duplicate_count=0  # Will be updated after duplicate check
        )

        if duplicate_result["is_duplicate"]:
            priority_score += 10

        original_priority = (
             duplicate_result.get(
                "duplicate_priority"
             )
             or 0
        )

        priority_score = max(
            priority_score,
            original_priority
        )
        priority_score += 10     

        priority_score = min(
            priority_score,
            100
        )

        original_report_id = duplicate_result.get(
            "duplicate_report_id"
        )

        duplicate_count = 0
        if original_report_id:
            duplicate_count = get_duplicate_count(
                original_report_id,
                current_user["token"]
            )

        analysis["duplicate_count"] = duplicate_count

        report_data = {
            "student_id":
                current_user["id"],

            "original_description":
                report.description,

            "ai_summary":
                analysis["summary"],

            "category":
                analysis["category"],

            "severity":
                analysis["severity"],

            "extracted_location":
                analysis.get(
                    "extracted_location"
                ),

            "recommended_department":
                analysis[
                    "recommended_department"
                ],

            "priority_score":
                priority_score,

            "status":
                "Submitted",

            "is_safety_flag":
                analysis.get(
                    "safety_flag",
                    False
                ),

            "is_accessibility_flag":
                analysis.get(
                    "accessibility_flag",
                    False
                ),

            "confidence":
                analysis.get(
                    "confidence"
                )
        }

        saved_report = save_report(
            report_data,
            current_user["token"]
        )

        new_report = saved_report[0]

        if duplicate_result[
            "is_duplicate"
        ]:

            # Save the duplicate relationship first
            save_duplicate_relationship(
                report_id=new_report["id"],
                duplicate_of_report_id=
                    duplicate_result[
                        "duplicate_report_id"
                    ],
                similarity_score=
                    duplicate_result[
                        "similarity_score"
                    ],
                access_token=
                    current_user["token"]
            )

            # Now get the updated count (includes the new relationship)
            original_report_id = duplicate_result.get(
                "duplicate_report_id"
            )
            if original_report_id:
                # Get the updated count of duplicates pointing to this original report
                dup_count = get_duplicate_count(
                    original_report_id,
                    current_user["token"]
                )
                
                # Get current priority of original report
                original_reports = get_report_by_id(
                    original_report_id,
                    current_user["token"]
                )
                current_priority = (
                    original_reports[0].get("priority_score") or 0
                    if original_reports else 0
                )
                
                # Calculate what the new priority should be based on duplicate count
                if original_reports:
                    original_severity = original_reports[0].get("severity", "Medium")
                    original_safety = original_reports[0].get("is_safety_flag", False)
                    original_accessibility = original_reports[0].get("is_accessibility_flag", False)
                    
                    # Calculate new priority using priority calculation function
                    new_priority = calculate_priority_score(
                        severity=original_severity,
                        safety_flag=original_safety,
                        accessibility_flag=original_accessibility,
                        duplicate_count=dup_count,
                        created_at=original_reports[0].get("created_at"),
                        current_status=original_reports[0].get("status")
                    )
                    
                    # Only increase priority, don't decrease
                    final_priority = max(current_priority, new_priority)
                    
                    update_report_priority(
                        original_report_id,
                        final_priority,
                        current_user["token"]
                    )

        return {
            "success": True,
            "report": saved_report,
            "analysis": analysis,
            "duplicate":
                duplicate_result
        }

    except HTTPException:
        # Re-raise HTTP exceptions (like 404, 400, etc.)
        raise

    except Exception as error:
        # Log the error but don't expose raw error details to users
        print(f"CREATE REPORT ERROR: {repr(error)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the report. Please try again."
        )

@app.get("/reports")
def list_reports(
    current_user: dict = Depends(
        get_authenticated_user
    )
):

    try:
        reports = get_all_reports(
            current_user["token"]
        )

        return {
            "success": True,
            "count": len(reports),
            "reports": reports
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/reports/{report_id}/history")
def report_status_history(
    report_id: str,
    current_user: dict = Depends(
        get_authenticated_user
    )
):

    try:

        history = get_status_history(
            report_id,
            current_user["token"]
        )

        return {
            "success": True,
            "count": len(history),
            "history": history
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/reports/{report_id}")
def get_report(
    report_id: str,
    current_user: dict = Depends(
        get_authenticated_user
    )
):

    try:

        reports = get_report_by_id(
            report_id,
            current_user["token"]
        )

        if not reports:
            raise HTTPException(
                status_code=404,
                detail="Report not found"
            )

        return {
            "success": True,
            "report": reports[0]
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/priority/recalculate")
def recalculate_priorities(
    current_user: dict = Depends(
        get_admin_user
    )
):
    """
    Recalculate priority scores for all active reports based on duration.
    This endpoint should be called daily via a scheduled job.
    """
    try:
        reports = get_reports_for_priority_update(
            current_user["token"]
        )
        
        recalc_count = 0
        no_change_count = 0
        
        for report in reports:
            report_id = report.get("id")
            severity = report.get("severity", "Medium")
            safety_flag = report.get("is_safety_flag", False)
            accessibility_flag = report.get("is_accessibility_flag", False)
            duplicate_count = report.get("duplicate_count", 0)
            created_at = report.get("created_at")
            current_status = report.get("status", "Submitted")
            current_priority = report.get("priority_score", 0)
            
            # Check if recalculation is needed
            should_recalc, new_priority = should_recalculate_priority(
                severity=severity,
                safety_flag=safety_flag,
                accessibility_flag=accessibility_flag,
                duplicate_count=duplicate_count,
                created_at=created_at,
                current_status=current_status,
                current_priority=current_priority
            )
            
            if should_recalc:
                update_report_priority(
                    report_id,
                    new_priority,
                    current_user["token"]
                )
                recalc_count += 1
            else:
                no_change_count += 1
        
        return {
            "success": True,
            "recalculated": recalc_count,
            "unchanged": no_change_count,
            "total_active": len(reports)
        }
        
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.put("/reports/{report_id}/status")
def change_report_status(
    report_id: str,
    status_update: StatusUpdateRequest,
    current_user: dict = Depends(
        get_admin_user
    )
):

    allowed_statuses = [
        "Submitted",
        "Under Review",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if status_update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    try:

        # 1. Get current report
        existing_reports = get_report_by_id(
            report_id,
            current_user["token"]
        )

        if not existing_reports:
            raise HTTPException(
                status_code=404,
                detail="Report not found"
            )

        old_status = existing_reports[0]["status"]
        new_status = status_update.status

        # Don't create duplicate history
        if old_status == new_status:
            return {
                "success": True,
                "message": "Status already set",
                "report": existing_reports[0]
            }

        # 2. Update report
        updated_reports = update_report_status(
            report_id,
            new_status,
            current_user["token"]
        )

        if not updated_reports:
            raise HTTPException(
                status_code=500,
                detail="Report status was not updated"
            )

        # 3. Save history
        history = add_status_history(
            report_id=report_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=current_user["id"],
            access_token=current_user["token"]
        )

        return {
            "success": True,
            "report": updated_reports[0],
            "history": history
        }

    except HTTPException:
        raise

    except Exception as error:
        print(
            "STATUS UPDATE ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )