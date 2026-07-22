"""Recommendation schemas."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class RecommendationFactorResponse(BaseModel):
    """Recommendation factor response."""
    id: int
    factor_type: str
    score: Decimal
    weight: Decimal
    rationale: str
    
    model_config = {'from_attributes': True}


class RecommendationResponse(BaseModel):
    """Recommendation response."""
    id: int
    recommendation_type: str
    priority_score: Decimal
    compliance_state: str
    expected_impact: Decimal
    currency: str
    rationale: dict
    factors: List[RecommendationFactorResponse] = []
    disposition: Optional[str] = None
    disposition_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {'from_attributes': True}


class GenerateRecommendationsRequest(BaseModel):
    """Generate recommendations request."""
    scenario_id: int = Field(..., gt=0)
    requested_by: int = Field(..., gt=0)


class DispositionRecommendationRequest(BaseModel):
    """Disposition recommendation request."""
    disposition: str = Field(..., pattern="^(accepted|rejected|deferred|contingent|escalated)$")
    reason_code: str = Field(..., min_length=1)
    actor_id: int = Field(..., gt=0)
