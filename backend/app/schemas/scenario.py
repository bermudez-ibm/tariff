"""Scenario analysis schemas."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class CostComponentResponse(BaseModel):
    """Cost component response."""
    id: int
    component_type: str
    amount: Decimal
    currency: str
    description: Optional[str] = None
    
    model_config = {'from_attributes': True}


class ScenarioResultResponse(BaseModel):
    """Scenario result response."""
    id: int
    scenario_request_id: int
    lane_id: int
    lane_type: str
    total_landed_cost: Decimal
    currency: str
    margin_impact: Optional[Decimal] = None
    completeness_status: str
    incomplete_reasons: Optional[List[str]] = None
    cost_components: List[CostComponentResponse] = []
    created_at: datetime
    
    model_config = {'from_attributes': True}


class ScenarioAnalysisRequest(BaseModel):
    """Request scenario analysis."""
    baseline_lane_id: int = Field(..., gt=0)
    alternate_lane_ids: List[int] = Field(..., min_length=1)
    requested_by: int = Field(..., gt=0)


class ScenarioAnalysisResponse(BaseModel):
    """Scenario analysis response."""
    id: int
    baseline_result: ScenarioResultResponse
    alternate_results: List[ScenarioResultResponse]
    created_at: datetime
    
    model_config = {'from_attributes': True}


class ScenarioComparisonResponse(BaseModel):
    """Scenario comparison response."""
    baseline: ScenarioResultResponse
    alternate: ScenarioResultResponse
    cost_delta: Decimal
    margin_impact_delta: Optional[Decimal] = None
    component_deltas: List[dict]
