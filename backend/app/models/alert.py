"""Alert and notification models."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class Alert(BaseModel):
    """Material impact alert."""
    __tablename__ = 'alerts'
    __table_args__ = (
        UniqueConstraint('dedupe_key', 'status', name='uq_alert_dedupe'),
    )
    
    category = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), index=True)
    source_ref_type = Column(String(100), nullable=False, index=True)
    source_ref_id = Column(Integer, nullable=False, index=True)
    due_at = Column(DateTime)
    escalation_at = Column(DateTime)
    dedupe_key = Column(String(255), nullable=False, index=True)
    alert_title = Column(String(500), nullable=False)
    alert_description = Column(Text, nullable=False)
    details = Column(JSON, nullable=False, default=dict)
    
    # Relationships
    transitions = relationship('AlertTransition', back_populates='alert', cascade='all, delete-orphan')


class AlertTransition(BaseModel):
    """Alert state transition history."""
    __tablename__ = 'alert_transitions'
    
    alert_id = Column(Integer, ForeignKey('alerts.id'), nullable=False, index=True)
    from_status = Column(String(50), nullable=False)
    to_status = Column(String(50), nullable=False)
    actor_id = Column(Integer, ForeignKey('users.id'))
    notes = Column(Text)
    transition_timestamp = Column(DateTime, nullable=False)
    transition_reason = Column(Text)
    
    # Relationships
    alert = relationship('Alert', back_populates='transitions')
