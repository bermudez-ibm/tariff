"""Recommendations router."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..services import RecommendationService
from ..schemas import (
    RecommendationResponse,
    GenerateRecommendationsRequest,
    DispositionRecommendationRequest,
)
from ..schemas.common import PaginatedResponse

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_service(db: Session = Depends(get_db)) -> RecommendationService:
    """Dependency injection for RecommendationService."""
    return RecommendationService(db)


@router.post("/generate", status_code=201, response_model=PaginatedResponse[RecommendationResponse])
async def generate_recommendations(
    payload: GenerateRecommendationsRequest,
    service: RecommendationService = Depends(get_recommendation_service),
    current_user: User = Depends(get_current_user),
):
    """
    Generate mitigation recommendations for a scenario.
    Implements REQ-API-005: Recommendation generation endpoint.
    Implements BR-MR-01: Compliance blocks override cost-favorable outcomes.
    """
    recommendations = service.generate_recommendations(
        scenario_id=payload.scenario_id,
        requested_by=payload.requested_by,
    )
    items = [RecommendationResponse.model_validate(r) for r in recommendations]
    return PaginatedResponse(
        items=items,
        total=len(items),
        page=1,
        page_size=len(items)
    )


@router.get("/{recommendation_id}", response_model=RecommendationResponse)
async def get_recommendation(
    recommendation_id: int,
    service: RecommendationService = Depends(get_recommendation_service),
    current_user: User = Depends(get_current_user),
):
    """
    Get recommendation detail with rationale and factors.
    Implements REQ-API-005: Recommendation detail endpoint.
    """
    from ..models import Recommendation

    rec = service.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return rec


@router.post("/{recommendation_id}/disposition", response_model=RecommendationResponse)
async def disposition_recommendation(
    recommendation_id: int,
    payload: DispositionRecommendationRequest,
    service: RecommendationService = Depends(get_recommendation_service),
    current_user: User = Depends(get_current_user),
):
    """
    Apply disposition to a recommendation.
    Implements REQ-API-005: Recommendation disposition endpoint.
    Implements BR-MR-01: Cannot accept blocked recommendations.
    Implements BR-MR-03: Disposition preserved for audit.
    """
    try:
        rec = service.disposition_recommendation(
            recommendation_id=recommendation_id,
            disposition=payload.disposition,
            reason_code=payload.reason_code,
            actor_id=payload.actor_id,
        )
        return rec
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
