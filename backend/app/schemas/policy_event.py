"""Policy event schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class EventDeltaResponse(BaseModel):
    """Event delta response."""
    id: int
    field_name: str
    prior_value: Optional[str] = None
    current_value: str
    
    model_config = {'from_attributes': True}


class ImpactAssociationResponse(BaseModel):
    """Impact association response."""
    id: int
    entity_type: str
    entity_id: int
    impact_description: str
    
    model_config = {'from_attributes': True}


class MaterialityEvaluationResponse(BaseModel):
    """Materiality evaluation response."""
    id: int
    materiality_state: str
    actionable: bool
    partial_impact: bool
    evaluation_timestamp: datetime
    
    model_config = {'from_attributes': True}


class PolicyEventListResponse(BaseModel):
    """Policy event list item."""
    id: int
    source_system: str
    event_external_id: str
    policy_type: str
    severity: str
    effective_date: datetime
    impacted_geographies: List[str]
    relevance_type: str
    materiality_state: Optional[str] = None
    actionable: bool = False
    created_at: datetime
    
    model_config = {'from_attributes': True}


class PolicyEventDetailResponse(BaseModel):
    """Policy event detail response."""
    id: int
    source_system: str
    event_external_id: str
    policy_type: str
    severity: str
    effective_date: datetime
    impacted_geographies: List[str]
    relevance_type: str
    description: Optional[str] = None
    deltas: List[EventDeltaResponse] = []
    associations: List[ImpactAssociationResponse] = []
    materiality: Optional[MaterialityEvaluationResponse] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {'from_attributes': True}


class IngestPolicyEventRequest(BaseModel):
    """Ingest policy event request."""
    source_system: str = Field(..., min_length=1)
    event_external_id: str = Field(..., min_length=1)
    policy_type: str = Field(..., min_length=1)
    severity: str = Field(..., pattern="^(critical|high|medium|low)$")
    effective_date: datetime
    impacted_geographies: List[str] = Field(default_factory=list)
    relevance_type: str = Field(..., pattern="^(primary|secondary|informational)$")
    description: Optional[str] = None
    deltas: List[dict] = Field(default_factory=list)
