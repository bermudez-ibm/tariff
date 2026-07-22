"""Alerts router."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..services import AlertService
from ..schemas import (
    PaginatedResponse,
    AlertResponse,
    AcknowledgeAlertRequest,
    AssignAlertRequest,
    EscalateAlertRequest,
    ResolveAlertRequest,
)

router = APIRouter(prefix="/alerts", tags=["alerts"])


def get_alert_service(db: Session = Depends(get_db)) -> AlertService:
    """Dependency injection for AlertService."""
    return AlertService(db)


@router.get("", response_model=PaginatedResponse[AlertResponse])
async def list_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    owner_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    service: AlertService = Depends(get_alert_service),
):
    """
    List alerts with filters and pagination.
    Implements REQ-API-006: Alert list endpoint.
    """
    items, total = service.list_alerts(page, page_size, owner_id, severity, status, category)

    return PaginatedResponse(
        items=[AlertResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    service: AlertService = Depends(get_alert_service),
):
    """
    Get alert detail with transitions.
    Implements REQ-API-006: Alert detail endpoint.
    """
    from ..models import Alert

    alert = service.db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return alert


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: int,
    payload: AcknowledgeAlertRequest,
    service: AlertService = Depends(get_alert_service),
):
    """
    Acknowledge alert.
    Implements REQ-API-006: Alert acknowledgement endpoint.
    Implements FR-AL-03, BR-AL-02: Acknowledgement tracking.
    """
    try:
        alert = service.acknowledge_alert(alert_id, payload.actor_id)
        return alert
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{alert_id}/assign", response_model=AlertResponse)
async def assign_alert(
    alert_id: int,
    payload: AssignAlertRequest,
    service: AlertService = Depends(get_alert_service),
):
    """
    Assign or reassign alert to owner.
    Implements REQ-API-006: Alert assignment endpoint.
    """
    try:
        alert = service.assign_alert(alert_id, payload.owner_id, payload.actor_id)
        return alert
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{alert_id}/escalate", response_model=AlertResponse)
async def escalate_alert(
    alert_id: int,
    payload: EscalateAlertRequest,
    service: AlertService = Depends(get_alert_service),
):
    """
    Escalate alert to higher scope.
    Implements REQ-API-006: Alert escalation endpoint.
    Implements FR-AL-04, BR-AL-03: Escalation tracking.
    """
    try:
        alert = service.escalate_alert(alert_id, payload.escalation_scope, payload.actor_id)
        return alert
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: int,
    payload: ResolveAlertRequest,
    service: AlertService = Depends(get_alert_service),
):
    """
    Resolve alert with outcome summary.
    Implements REQ-API-006: Alert resolution endpoint.
    Implements FR-AL-07, BR-AL-02: Resolution tracking.
    """
    try:
        alert = service.resolve_alert(alert_id, payload.outcome_summary, payload.actor_id)
        return alert
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
