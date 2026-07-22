"""Compliance schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskFlagResponse(BaseModel):
    """Risk flag response."""
    id: int
    risk_category: str
    severity: str
    flagged_at: datetime
    resolution_status: str
    description: str
    
    model_config = {'from_attributes': True}


class ComplianceReviewResponse(BaseModel):
    """Compliance review response."""
    id: int
    subject_type: str
    subject_id: int
    review_state: str
    reviewer_role: str
    review_notes: Optional[str] = None
    reason_code: Optional[str] = None
    risk_flags: List[RiskFlagResponse] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = {'from_attributes': True}


class CreateComplianceReviewRequest(BaseModel):
    """Create compliance review request."""
    subject_type: str = Field(..., min_length=1)
    subject_id: int = Field(..., gt=0)
    reviewer_role: str = Field(..., min_length=1)


class TransitionReviewStateRequest(BaseModel):
    """Transition review state request."""
    new_state: str = Field(..., pattern="^(APPROVED|CONTINGENT|BLOCKED|UNDER_REVIEW)$")
    reason_code: str = Field(..., min_length=1)
    actor_id: int = Field(..., gt=0)
