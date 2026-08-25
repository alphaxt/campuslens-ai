from fastapi import FastAPI, HTTPException
from services.database import save_report

from models.report import ReportRequest
from services.ai_service import analyze_issue
from services.priority import calculate_priority


app = FastAPI(
    title="CampusLens AI API",
    description="Backend API for CampusLens AI",
    version="0.1.0"
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