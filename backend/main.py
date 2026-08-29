from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from services.auth import (
    get_authenticated_user,
    get_admin_user,
    get_student_user
)

from models.report import ReportRequest, StatusUpdateRequest


from services.database import (
    save_report,
    get_all_reports,
    get_report_by_id,
    update_report_status,
    add_status_history,
    get_status_history
)

from services.ai_service import (
    analyze_issue,
    generate_campus_pulse
)
from services.priority import calculate_priority


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
        analysis = analyze_issue(report.description)

        priority_score = calculate_priority(
            severity=analysis["severity"],
            safety_flag=analysis.get(
                "safety_flag",
                False
            ),
            accessibility_flag=analysis.get(
                "accessibility_flag",
                False
            )
        )

        analysis["priority_score"] = priority_score

        report_data = {
            "student_id": current_user["id"],
            "original_description": report.description,
            "ai_summary": analysis["summary"],
            "category": analysis["category"],
            "severity": analysis["severity"],
            "extracted_location": analysis.get(
                "extracted_location"
            ),
            "recommended_department": analysis[
                "recommended_department"
            ],
            "priority_score": priority_score,
            "status": "Submitted",
            "is_safety_flag": analysis.get(
                "safety_flag",
                False
            ),
            "is_accessibility_flag": analysis.get(
                "accessibility_flag",
                False
            ),
            "confidence": analysis.get(
                "confidence"
            )
        }

        saved_report = save_report(
         report_data,
         current_user["token"]
        )

        return {
            "success": True,
            "report": saved_report,
            "analysis": analysis
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
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


@app.get("/analytics/campus-pulse")
def campus_pulse(
    current_user: dict = Depends(
        get_admin_user
    )
):

    try:
        reports = get_all_reports(
            current_user["token"]
        )

        pulse = generate_campus_pulse(
            reports
        )

        return {
            "success": True,
            "report_count": len(reports),
            "pulse": pulse
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )




