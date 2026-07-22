"""Scenario analysis models: requests, results, cost components."""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DECIMAL, DateTime, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class ScenarioRequest(BaseModel):
    """Scenario analysis request."""
    __tablename__ = 'scenario_requests'
    
    triggering_event_id = Column(Integer, ForeignKey('policy_events.id'), index=True)
    baseline_lane_id = Column(Integer, nullable=False, index=True)
    alternate_lane_ids = Column(JSON, nullable=False)
    shipment_timing_option = Column(String(100))
    requested_by = Column(Integer, ForeignKey('users.id'), index=True)
    request_source = Column(String(100), nullable=False)
    reference_snapshot_id = Column(Integer, ForeignKey('reference_snapshots.id'))
    
    # Relationships
    results = relationship('ScenarioResult', back_populates='scenario', cascade='all, delete-orphan')


class ScenarioResult(BaseModel):
    """Scenario calculation result for one lane."""
    __tablename__ = 'scenario_results'
    
    scenario_id = Column(Integer, ForeignKey('scenario_requests.id'), nullable=False, index=True)
    lane_id = Column(Integer, nullable=False, index=True)
    is_baseline = Column(Boolean, nullable=False, default=False)
    completeness_status = Column(String(50), nullable=False)
    total_landed_cost = Column(DECIMAL(18, 2))
    margin_impact = Column(DECIMAL(18, 2))
    calculation_timestamp = Column(DateTime, nullable=False)
    input_snapshot = Column(JSON, nullable=False)
    incomplete_reasons = Column(JSON)
    
    # Relationships
    scenario = relationship('ScenarioRequest', back_populates='results')
    cost_components = relationship('CostComponent', back_populates='result', cascade='all, delete-orphan')
    agreement_evaluations = relationship('AgreementEvaluation', back_populates='scenario_result', cascade='all, delete-orphan')


class CostComponent(BaseModel):
    """Individual cost component within a scenario result."""
    __tablename__ = 'cost_components'
    __table_args__ = (
        UniqueConstraint('scenario_result_id', 'component_type', name='uq_cost_component_type'),
    )
    
    scenario_result_id = Column(Integer, ForeignKey('scenario_results.id'), nullable=False, index=True)
    component_type = Column(String(100), nullable=False, index=True)
    amount = Column(DECIMAL(18, 2))
    currency = Column(String(3), nullable=False)
    source_snapshot_ref = Column(Text)
    
    # Relationships
    result = relationship('ScenarioResult', back_populates='cost_components')
