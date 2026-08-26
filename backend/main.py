from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.report import ReportRequest, StatusUpdateRequest


from services.database import (
    save_report,
    get_all_reports,
    get_report_by_id,
    update_report_status
)

from services.ai_service import analyze_issue
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
def create_report(report: ReportRequest):

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

        saved_report = save_report(report_data)

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
def list_reports():

    try:
        reports = get_all_reports()

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


@app.get("/reports/{report_id}")
def get_report(report_id: str):

    try:
        reports = get_report_by_id(report_id)

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
    status_update: StatusUpdateRequest
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
            detail="Invalid report status"
        )

    try:
        updated_report = update_report_status(
            report_id,
            status_update.status
        )

        if not updated_report:
            raise HTTPException(
                status_code=404,
                detail="Report not found"
            )

        return {
            "success": True,
            "report": updated_report[0]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )