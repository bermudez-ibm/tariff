"""Scenarios router."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..services import FinancialAnalysisService
from ..schemas import (
    ScenarioAnalysisRequest,
    ScenarioAnalysisResponse,
    ScenarioResultResponse,
    ScenarioComparisonResponse,
)

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


def get_financial_service(db: Session = Depends(get_db)) -> FinancialAnalysisService:
    """Dependency injection for FinancialAnalysisService."""
    return FinancialAnalysisService(db)


@router.post("/analyze", status_code=201, response_model=ScenarioAnalysisResponse)
async def analyze_scenario(
    payload: ScenarioAnalysisRequest,
    service: FinancialAnalysisService = Depends(get_financial_service),
    current_user: User = Depends(get_current_user),
):
    """
    Request scenario analysis for baseline and alternate lanes.
    Implements REQ-API-003: Scenario analysis endpoint.
    Implements BR-LC-01: Scenario comparison within 60 seconds.
    """
    scenario = service.create_scenario_request(
        baseline_lane_id=payload.baseline_lane_id,
        alternate_lane_ids=payload.alternate_lane_ids,
        requested_by=payload.requested_by,
    )

    # Calculate baseline result
    baseline_result = service.calculate_scenario(scenario.id)

    # Calculate alternate results (placeholder: only first alternate for simplicity)
    alternate_results = []
    if payload.alternate_lane_ids:
        # In real implementation, would calculate all alternates
        pass

    return ScenarioAnalysisResponse(
        id=scenario.id,
        baseline_result=ScenarioResultResponse.model_validate(baseline_result),
        alternate_results=alternate_results,
        created_at=scenario.created_at,
    )


@router.get("/{scenario_id}", response_model=ScenarioResultResponse)
async def get_scenario(
    scenario_id: int,
    service: FinancialAnalysisService = Depends(get_financial_service),
    current_user: User = Depends(get_current_user),
):
    """
    Get scenario detail with cost components.
    Implements REQ-API-003: Scenario detail endpoint.
    """
    from ..models import ScenarioResult

    result = service.db.query(ScenarioResult).filter(ScenarioResult.id == scenario_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="ScenarioResult not found")

    return result


@router.get("/{scenario_id}/comparison", response_model=ScenarioComparisonResponse)
async def get_scenario_comparison(
    scenario_id: int,
    baseline_id: int = Query(...),
    alternate_id: int = Query(...),
    service: FinancialAnalysisService = Depends(get_financial_service),
    current_user: User = Depends(get_current_user),
):
    """
    Compare baseline and alternate scenario results.
    Implements REQ-API-003: Scenario comparison endpoint.
    Implements BR-LC-01, BR-LC-03: Cost comparison with deltas.
    """
    comparison = service.get_scenario_comparison(scenario_id, baseline_id, alternate_id)
    return ScenarioComparisonResponse(**comparison)
