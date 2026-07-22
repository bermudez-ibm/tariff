"""Policy event models: events, deltas, impact associations, materiality evaluations."""
from sqlalchemy import Column, Integer, String, Boolean, Text, Date, DateTime, ForeignKey, DECIMAL, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class PolicyEvent(BaseModel):
    """Policy event normalized from external sources."""
    __tablename__ = 'policy_events'
    __table_args__ = (
        UniqueConstraint('source_system', 'event_external_id', name='uq_policy_events_source'),
    )
    
    source_system = Column(String(100), nullable=False, index=True)
    event_external_id = Column(String(255), nullable=False, index=True)
    policy_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), nullable=False, index=True)
    relevance_type = Column(String(100), index=True)
    effective_date = Column(Date, nullable=False, index=True)
    impacted_geographies = Column(JSON, nullable=False)
    prior_state = Column(JSON)
    current_state = Column(JSON, nullable=False)
    actionable_flag = Column(Boolean, nullable=False, default=False)
    materiality_state = Column(String(50), index=True)
    source_occurred_at = Column(DateTime)
    ingested_at = Column(DateTime, nullable=False)
    raw_payload_ref = Column(Text)
    association_quality = Column(String(50))
    
    # Relationships
    deltas = relationship('EventDelta', back_populates='event', cascade='all, delete-orphan')
    associations = relationship('ImpactAssociation', back_populates='event', cascade='all, delete-orphan')
    materiality_evaluations = relationship('MaterialityEvaluation', back_populates='event', cascade='all, delete-orphan')


class EventDelta(BaseModel):
    """Delta changes detected in policy events."""
    __tablename__ = 'event_deltas'
    
    event_id = Column(Integer, ForeignKey('policy_events.id'), nullable=False, index=True)
    changed_field = Column(String(255), nullable=False)
    prior_value = Column(Text)
    current_value = Column(Text)
    detected_at = Column(DateTime, nullable=False)
    
    # Relationships
    event = relationship('PolicyEvent', back_populates='deltas')


class ImpactAssociation(BaseModel):
    """Impact associations linking events to affected entities."""
    __tablename__ = 'impact_associations'
    
    event_id = Column(Integer, ForeignKey('policy_events.id'), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    association_quality = Column(String(50), nullable=False)
    actionable_flag = Column(Boolean, nullable=False, default=False)
    missing_reference_reason = Column(Text)
    
    # Relationships
    event = relationship('PolicyEvent', back_populates='associations')


class MaterialityEvaluation(BaseModel):
    """Materiality classification for policy events."""
    __tablename__ = 'materiality_evaluations'
    
    event_id = Column(Integer, ForeignKey('policy_events.id'), nullable=False, index=True)
    threshold_profile = Column(String(100), nullable=False)
    exposure_value = Column(DECIMAL(18, 2))
    classification = Column(String(50), nullable=False, index=True)
    rationale = Column(JSON, nullable=False)
    evaluated_at = Column(DateTime, nullable=False)
    
    # Relationships
    event = relationship('PolicyEvent', back_populates='materiality_evaluations')
