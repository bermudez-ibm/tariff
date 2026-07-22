"""Compliance router."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..services import ComplianceWorkflowService
from ..schemas import (
    PaginatedResponse,
    ComplianceReviewResponse,
    CreateComplianceReviewRequest,
    TransitionReviewStateRequest,
)

router = APIRouter(prefix="/compliance-reviews", tags=["compliance"])


def get_compliance_service(db: Session = Depends(get_db)) -> ComplianceWorkflowService:
    """Dependency injection for ComplianceWorkflowService."""
    return ComplianceWorkflowService(db)


@router.get("", response_model=PaginatedResponse[ComplianceReviewResponse])
async def list_compliance_reviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    subject_type: Optional[str] = Query(None),
    review_state: Optional[str] = Query(None),
    service: ComplianceWorkflowService = Depends(get_compliance_service),
):
    """
    List compliance reviews with filters and pagination.
    Implements REQ-API-008: Compliance review list endpoint.
    """
    from ..models import ComplianceReview

    query = service.db.query(ComplianceReview)

    if subject_type:
        query = query.filter(ComplianceReview.subject_type == subject_type)
    if review_state:
        query = query.filter(ComplianceReview.review_state == review_state)

    total = query.count()
    offset = (page - 1) * page_size
    items = query.order_by(ComplianceReview.created_at.desc()).offset(offset).limit(page_size).all()

    return PaginatedResponse(
        items=[ComplianceReviewResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", status_code=201, response_model=ComplianceReviewResponse)
async def create_compliance_review(
    payload: CreateComplianceReviewRequest,
    service: ComplianceWorkflowService = Depends(get_compliance_service),
):
    """
    Create compliance review for a subject.
    Implements REQ-API-008: Compliance review creation endpoint.
    Implements FR-CR-01, BR-CR-01: Review states and compliance blocks.
    """
    review = service.create_review(
        subject_type=payload.subject_type,
        subject_id=payload.subject_id,
        reviewer_role=payload.reviewer_role,
    )
    return review


@router.patch("/{review_id}", response_model=ComplianceReviewResponse)
async def transition_review_state(
    review_id: int,
    payload: TransitionReviewStateRequest,
    service: ComplianceWorkflowService = Depends(get_compliance_service),
):
    """
    Transition compliance review state.
    Implements REQ-API-008: Review state transition endpoint.
    Implements BR-CR-01: Compliance blocks override cost-favorable recommendations.
    Implements FR-CR-02, BR-CR-03: Non-destructive history preservation.
    """
    try:
        review = service.transition_review_state(
            review_id=review_id,
            new_state=payload.new_state,
            reason_code=payload.reason_code,
            actor_id=payload.actor_id,
        )
        return review
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{review_id}", response_model=ComplianceReviewResponse)
async def get_compliance_review(
    review_id: int,
    service: ComplianceWorkflowService = Depends(get_compliance_service),
):
    """
    Get compliance review detail with risk flags.
    Implements REQ-API-008: Compliance review detail endpoint.
    """
    from ..models import ComplianceReview

    review = service.db.query(ComplianceReview).filter(ComplianceReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="ComplianceReview not found")

    return review
