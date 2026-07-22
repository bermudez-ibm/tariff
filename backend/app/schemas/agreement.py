"""Trade agreement schemas."""
from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel


class EvidenceGapResponse(BaseModel):
    """Evidence gap response."""
    id: int
    gap_type: str
    severity: str
    blocking_flag: bool
    description: str
    
    model_config = {'from_attributes': True}


class AgreementEvaluationResponse(BaseModel):
    """Agreement evaluation response."""
    id: int
    scenario_result_id: int
    agreement_code: str
    qualification_status: str
    estimated_savings: Decimal
    currency: str
    evidence_state: str
    evidence_gaps: List[EvidenceGapResponse] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = {'from_attributes': True}
