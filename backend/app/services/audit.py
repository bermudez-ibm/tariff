"""Audit service for immutable audit trail management."""
import hashlib
import json
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models import AuditEntry


class AuditService:
    """Service for append-only audit trail with tamper-evident hash chain."""

    def __init__(self, db: Session):
        self.db = db

    def append_audit_entry(
        self,
        aggregate_type: str,
        aggregate_id: int,
        action_type: str,
        actor_id: int,
        before_state: dict,
        after_state: dict,
    ) -> AuditEntry:
        """
        Append audit entry with hash chain for tamper evidence.
        Implements FR-CR-04, BR-CR-03: Immutable audit trail with 7-year retention.
        """
        # Get previous entry hash for chain
        previous_entry = self.db.query(AuditEntry).filter(
            AuditEntry.aggregate_type == aggregate_type,
            AuditEntry.aggregate_id == aggregate_id,
        ).order_by(AuditEntry.created_at.desc()).first()

        previous_hash = previous_entry.entry_hash if previous_entry else ''

        # Compute current entry hash
        entry_data = {
            'aggregate_type': aggregate_type,
            'aggregate_id': aggregate_id,
            'action_type': action_type,
            'actor_id': actor_id,
            'before_state': before_state,
            'after_state': after_state,
            'previous_hash': previous_hash,
            'timestamp': datetime.utcnow().isoformat(),
        }
        entry_hash = hashlib.sha256(json.dumps(entry_data, sort_keys=True).encode()).hexdigest()

        entry = AuditEntry(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            action_type=action_type,
            actor_id=actor_id,
            before_state=before_state,
            after_state=after_state,
            entry_hash=entry_hash,
            audit_metadata={'previous_hash': previous_hash},
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_audit_history(
        self,
        aggregate_type: str,
        aggregate_id: int,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[List[AuditEntry], int]:
        """
        Retrieve audit history for an aggregate.
        Returns entries in reverse chronological order.
        """
        query = self.db.query(AuditEntry).filter(
            AuditEntry.aggregate_type == aggregate_type,
            AuditEntry.aggregate_id == aggregate_id,
        )

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(AuditEntry.created_at.desc()).offset(offset).limit(page_size).all()

        return items, total

    def verify_audit_chain(self, aggregate_type: str, aggregate_id: int) -> bool:
        """
        Verify integrity of audit chain for an aggregate.
        Returns True if chain is intact, False if tampered.
        """
        entries = self.db.query(AuditEntry).filter(
            AuditEntry.aggregate_type == aggregate_type,
            AuditEntry.aggregate_id == aggregate_id,
        ).order_by(AuditEntry.created_at.asc()).all()

        if not entries:
            return True

        previous_hash = ''
        for entry in entries:
            # Recompute hash
            entry_data = {
                'aggregate_type': entry.aggregate_type,
                'aggregate_id': entry.aggregate_id,
                'action_type': entry.action_type,
                'actor_id': entry.actor_id,
                'before_state': entry.before_state,
                'after_state': entry.after_state,
                'previous_hash': previous_hash,
                'timestamp': entry.created_at.isoformat(),
            }
            computed_hash = hashlib.sha256(json.dumps(entry_data, sort_keys=True).encode()).hexdigest()

            if computed_hash != entry.entry_hash:
                return False

            previous_hash = entry.entry_hash

        return True
