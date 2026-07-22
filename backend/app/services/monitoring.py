"""Monitoring service for policy event ingestion and materiality evaluation."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import (
    PolicyEvent,
    EventDelta,
    ImpactAssociation,
    MaterialityEvaluation,
)


class MonitoringService:
    """Service for policy event monitoring and materiality evaluation."""

    def __init__(self, db: Session):
        self.db = db

    def ingest_policy_event(self, event_data: dict) -> PolicyEvent:
        """
        Ingest policy event from external source (idempotent).
        Implements BR-TM-01: Materiality evaluation and event publication timing.
        """
        # Check for existing event (idempotency)
        existing = self.db.query(PolicyEvent).filter(
            PolicyEvent.source_system == event_data['source_system'],
            PolicyEvent.event_external_id == event_data['event_external_id']
        ).first()

        if existing:
            return existing

        # Create event
        event = PolicyEvent(
            source_system=event_data['source_system'],
            event_external_id=event_data['event_external_id'],
            policy_type=event_data['policy_type'],
            severity=event_data['severity'],
            effective_date=event_data['effective_date'],
            impacted_geographies=event_data.get('impacted_geographies', []),
            relevance_type=event_data['relevance_type'],
            prior_state=event_data.get('prior_state'),
            current_state=event_data.get('current_state', {}),
            ingested_at=datetime.utcnow(),
        )
        self.db.add(event)
        self.db.flush()

        # Create deltas
        for delta_data in event_data.get('deltas', []):
            delta = EventDelta(
                event_id=event.id,
                changed_field=delta_data['field_name'],
                prior_value=delta_data.get('prior_value'),
                current_value=delta_data['current_value'],
                detected_at=datetime.utcnow(),
            )
            self.db.add(delta)

        self.db.commit()
        self.db.refresh(event)
        return event

    def evaluate_materiality(self, event_id: int) -> MaterialityEvaluation:
        """
        Evaluate materiality for a policy event.
        Implements BR-TM-02: Materiality thresholds and actionable flag.
        """
        event = self.db.query(PolicyEvent).filter(PolicyEvent.id == event_id).first()
        if not event:
            raise ValueError(f"PolicyEvent {event_id} not found")

        # Simple materiality logic (placeholder for real business rules)
        materiality_state = 'MATERIAL' if event.severity in ['critical', 'high'] else 'WATCHLIST'
        actionable = event.severity == 'critical'
        partial_impact = False  # Would check reference data completeness

        evaluation = MaterialityEvaluation(
            policy_event_id=event.id,
            materiality_state=materiality_state,
            actionable=actionable,
            partial_impact=partial_impact,
            evaluation_timestamp=datetime.utcnow(),
        )
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

    def get_event_by_id(self, event_id: int) -> Optional[PolicyEvent]:
        """Retrieve single policy event with associations."""
        return self.db.query(PolicyEvent).filter(PolicyEvent.id == event_id).first()

    def list_events(
        self,
        page: int = 1,
        page_size: int = 20,
        severity: Optional[str] = None,
        materiality: Optional[str] = None,
    ) -> tuple[List[PolicyEvent], int]:
        """List policy events with filters and pagination."""
        query = self.db.query(PolicyEvent)

        if severity:
            query = query.filter(PolicyEvent.severity == severity)

        # Materiality filter requires join
        if materiality:
            query = query.join(MaterialityEvaluation).filter(
                MaterialityEvaluation.materiality_state == materiality
            )

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(PolicyEvent.created_at.desc()).offset(offset).limit(page_size).all()

        return items, total

    def get_impact_associations(self, event_id: int) -> List[ImpactAssociation]:
        """Get impact associations for an event."""
        return self.db.query(ImpactAssociation).filter(
            ImpactAssociation.policy_event_id == event_id
        ).all()
