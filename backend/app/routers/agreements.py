"""Trade agreements router."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..services import TradeAgreementService
from ..schemas import AgreementEvaluationResponse
from ..schemas.common import PaginatedResponse

router = APIRouter(prefix="/agreements", tags=["agreements"])


def get_agreement_service(db: Session = Depends(get_db)) -> TradeAgreementService:
    """Dependency injection for TradeAgreementService."""
    return TradeAgreementService(db)


@router.get(
    "/scenarios/{scenario_result_id}/agreement-evaluations",
    response_model=PaginatedResponse[AgreementEvaluationResponse],
)
async def get_scenario_agreement_evaluations(
    scenario_result_id: int,
    service: TradeAgreementService = Depends(get_agreement_service),
    current_user: User = Depends(get_current_user),
):
    """
    Get agreement evaluations for a scenario result.
    Implements REQ-API-004: Trade agreement evaluation endpoints.
    Implements BR-TA-01, BR-TA-02: Qualification status and evidence gaps.
    """
    evaluations = service.evaluate_agreements(scenario_result_id)
    items = [AgreementEvaluationResponse.model_validate(e) for e in evaluations]
    return PaginatedResponse(
        items=items,
        total=len(items),
        page=1,
        page_size=len(items)
    )


@router.get("/{evaluation_id}", response_model=AgreementEvaluationResponse)
async def get_agreement_evaluation(
    evaluation_id: int,
    service: TradeAgreementService = Depends(get_agreement_service),
    current_user: User = Depends(get_current_user),
):
    """
    Get single agreement evaluation with evidence gaps.
    Implements REQ-API-004: Agreement detail endpoint.
    """
    try:
        evaluation = service.get_agreement_evaluation(evaluation_id)
        return evaluation
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
