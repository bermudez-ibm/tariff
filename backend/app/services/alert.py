"""Alert service for alert orchestration and routing."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models import Alert, AlertTransition


class AlertService:
    """Service for alert generation, routing, and lifecycle management."""

    def __init__(self, db: Session):
        self.db = db

    def create_alert(
        self,
        category: str,
        severity: str,
        source_ref_type: str,
        source_ref_id: int,
        owner_scope: dict,
        alert_title: str,
        alert_description: str,
        details: dict,
    ) -> Alert:
        """
        Create alert with routing based on severity and ownership.
        Implements FR-AL-01, FR-AL-02: Alert generation and routing.
        Implements BR-AL-01: Alert categorization and routing by severity.
        """
        dedupe_key = f"{source_ref_type}:{source_ref_id}:{category}"

        # Check for existing alert (idempotency)
        existing = self.db.query(Alert).filter(
            Alert.dedupe_key == dedupe_key,
            Alert.status.in_(['NEW', 'ACKNOWLEDGED', 'IN_PROGRESS']),
        ).first()

        if existing:
            return existing

        alert = Alert(
            category=category,
            severity=severity,
            status='NEW',
            source_ref_type=source_ref_type,
            source_ref_id=source_ref_id,
            owner_id=owner_scope.get('owner_id'),
            dedupe_key=dedupe_key,
            alert_title=alert_title,
            alert_description=alert_description,
            details=details,
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def acknowledge_alert(self, alert_id: int, actor_id: int) -> Alert:
        """
        Acknowledge alert.
        Implements FR-AL-03: Acknowledgement tracking.
        """
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        if alert.status != 'NEW':
            raise ValueError(f"Alert {alert_id} is not in NEW status")

        alert.status = 'ACKNOWLEDGED'

        transition = AlertTransition(
            alert_id=alert.id,
            from_status='NEW',
            to_status='ACKNOWLEDGED',
            actor_id=actor_id,
            transition_timestamp=datetime.utcnow(),
        )
        self.db.add(transition)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def assign_alert(self, alert_id: int, owner_id: int, actor_id: int) -> Alert:
        """Assign or reassign alert to an owner."""
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        old_status = alert.status
        alert.owner_id = owner_id
        alert.status = 'IN_PROGRESS' if alert.status == 'ACKNOWLEDGED' else alert.status

        if old_status != alert.status:
            transition = AlertTransition(
                alert_id=alert.id,
                from_status=old_status,
                to_status=alert.status,
                actor_id=actor_id,
                transition_timestamp=datetime.utcnow(),
                transition_reason='Assigned to owner',
            )
            self.db.add(transition)

        self.db.commit()
        self.db.refresh(alert)
        return alert

    def escalate_alert(self, alert_id: int, escalation_scope: dict, actor_id: int) -> Alert:
        """
        Escalate alert to higher scope.
        Implements FR-AL-04: Escalation paths.
        """
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        old_status = alert.status
        alert.status = 'ESCALATED'
        alert.details['escalation_scope'] = escalation_scope

        transition = AlertTransition(
            alert_id=alert.id,
            from_status=old_status,
            to_status='ESCALATED',
            actor_id=actor_id,
            transition_timestamp=datetime.utcnow(),
            transition_reason='Escalated to higher scope',
        )
        self.db.add(transition)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def resolve_alert(self, alert_id: int, outcome_summary: str, actor_id: int) -> Alert:
        """
        Resolve alert with outcome summary.
        Implements FR-AL-07, BR-AL-02: Alert lifecycle and resolution.
        """
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise ValueError(f"Alert {alert_id} not found")

        old_status = alert.status
        alert.status = 'RESOLVED'
        alert.details['outcome_summary'] = outcome_summary

        transition = AlertTransition(
            alert_id=alert.id,
            from_status=old_status,
            to_status='RESOLVED',
            actor_id=actor_id,
            transition_timestamp=datetime.utcnow(),
            transition_reason=outcome_summary,
        )
        self.db.add(transition)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def list_alerts(
        self,
        page: int = 1,
        page_size: int = 20,
        owner_id: Optional[int] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
    ) -> tuple[List[Alert], int]:
        """List alerts with filters and pagination."""
        query = self.db.query(Alert)

        if owner_id:
            query = query.filter(Alert.owner_id == owner_id)
        if severity:
            query = query.filter(Alert.severity == severity)
        if status:
            query = query.filter(Alert.status == status)
        if category:
            query = query.filter(Alert.category == category)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Alert.created_at.desc()).offset(offset).limit(page_size).all()

        return items, total
