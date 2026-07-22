"""Policy events router."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..services import MonitoringService
from ..schemas import (
    PaginatedResponse,
    PolicyEventListResponse,
    PolicyEventDetailResponse,
    IngestPolicyEventRequest,
)

router = APIRouter(prefix="/policy-events", tags=["policy-events"])


def get_monitoring_service(db: Session = Depends(get_db)) -> MonitoringService:
    """Dependency injection for MonitoringService."""
    return MonitoringService(db)


@router.post("/ingest", status_code=201, response_model=PolicyEventDetailResponse)
async def ingest_policy_event(
    payload: IngestPolicyEventRequest,
    service: MonitoringService = Depends(get_monitoring_service),
    current_user: User = Depends(get_current_user),
):
    """
    Ingest policy event from external source (idempotent).
    Implements REQ-API-002: Policy event ingestion.
    """
    event = service.ingest_policy_event(payload.model_dump())

    # Trigger materiality evaluation
    service.evaluate_materiality(event.id)

    return event


@router.get("", response_model=PaginatedResponse[PolicyEventListResponse])
async def list_policy_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: Optional[str] = Query(None),
    materiality: Optional[str] = Query(None),
    service: MonitoringService = Depends(get_monitoring_service),
    current_user: User = Depends(get_current_user),
):
    """
    List policy events with pagination and filters.
    Implements REQ-API-002: List policy events.
    """
    items, total = service.list_events(page, page_size, severity, materiality)

    return PaginatedResponse(
        items=[PolicyEventListResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{event_id}", response_model=PolicyEventDetailResponse)
async def get_policy_event(
    event_id: int,
    service: MonitoringService = Depends(get_monitoring_service),
    current_user: User = Depends(get_current_user),
):
    """
    Get policy event detail with deltas, associations, and materiality.
    Implements REQ-API-002: Policy event detail.
    """
    event = service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="PolicyEvent not found")

    return event
