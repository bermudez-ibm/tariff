"""Alert schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class AlertTransitionResponse(BaseModel):
    """Alert transition response."""
    id: int
    from_status: str
    to_status: str
    actor_id: int
    transition_timestamp: datetime
    transition_reason: Optional[str] = None
    
    model_config = {'from_attributes': True}


class AlertResponse(BaseModel):
    """Alert response."""
    id: int
    category: str
    severity: str
    status: str
    source_ref_type: str
    source_ref_id: int
    owner_id: Optional[int] = None
    dedupe_key: str
    alert_title: str
    alert_description: str
    details: dict
    created_at: datetime
    updated_at: datetime
    transitions: List[AlertTransitionResponse] = []
    
    model_config = {'from_attributes': True}


class AcknowledgeAlertRequest(BaseModel):
    """Acknowledge alert request."""
    actor_id: int = Field(..., gt=0)


class AssignAlertRequest(BaseModel):
    """Assign alert request."""
    owner_id: int = Field(..., gt=0)
    actor_id: int = Field(..., gt=0)


class EscalateAlertRequest(BaseModel):
    """Escalate alert request."""
    escalation_scope: dict
    actor_id: int = Field(..., gt=0)


class ResolveAlertRequest(BaseModel):
    """Resolve alert request."""
    outcome_summary: str = Field(..., min_length=1)
    actor_id: int = Field(..., gt=0)
