"""Audit entry model for immutable history."""
from sqlalchemy import Column, Integer, String, DateTime, Index, JSON
from .base import Base, TimestampMixin


class AuditEntry(Base, TimestampMixin):
    """Immutable audit entry with hash chain."""
    __tablename__ = 'audit_entries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregate_type = Column(String(100), nullable=False, index=True)
    aggregate_id = Column(Integer, nullable=False, index=True)
    action_type = Column(String(100), nullable=False)
    actor_id = Column(Integer)
    occurred_at = Column(DateTime, nullable=False)
    payload_hash = Column(String(64), nullable=False)
    previous_hash = Column(String(64))
    correlation_id = Column(String(100), index=True)
    audit_metadata = Column(JSON, nullable=False)


# Composite index for audit queries
Index('idx_audit_entries_aggregate', AuditEntry.aggregate_type, AuditEntry.aggregate_id, AuditEntry.occurred_at.desc())
