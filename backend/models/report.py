from pydantic import BaseModel, Field
from typing import Optional


class ReportRequest(BaseModel):
    description: str = Field(
        ...,
        min_length=5,
        max_length=2000
    )


class AIAnalysis(BaseModel):
    summary: str
    category: str
    severity: str
    recommended_department: str
    extracted_location: Optional[str] = None
    safety_flag: bool = False
    accessibility_flag: bool = False
    confidence: float
    priority_score: int = 0

class StatusUpdateRequest(BaseModel):
    status: str