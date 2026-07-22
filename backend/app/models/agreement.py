"""Trade agreement evaluation models."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL, DateTime, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class AgreementEvaluation(BaseModel):
    """Trade agreement qualification and savings evaluation."""
    __tablename__ = 'agreement_evaluations'
    __table_args__ = (
        UniqueConstraint('scenario_result_id', 'agreement_code', name='uq_agreement_eval_code'),
    )
    
    scenario_result_id = Column(Integer, ForeignKey('scenario_results.id'), nullable=False, index=True)
    agreement_code = Column(String(50), nullable=False, index=True)
    qualification_status = Column(String(50), nullable=False, index=True)
    estimated_savings = Column(DECIMAL(18, 2))
    evidence_state = Column(String(50), nullable=False)
    contingent_flag = Column(Boolean, nullable=False, default=False)
    evaluated_at = Column(DateTime, nullable=False)
    
    # Relationships
    scenario_result = relationship('ScenarioResult', back_populates='agreement_evaluations')
    evidence_gaps = relationship('EvidenceGap', back_populates='agreement_evaluation', cascade='all, delete-orphan')


class EvidenceGap(BaseModel):
    """Evidence gaps preventing agreement qualification."""
    __tablename__ = 'evidence_gaps'
    
    agreement_evaluation_id = Column(Integer, ForeignKey('agreement_evaluations.id'), nullable=False, index=True)
    gap_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), nullable=False)
    blocking_flag = Column(Boolean, nullable=False, default=False)
    details = Column(JSON)
    
    # Relationships
    agreement_evaluation = relationship('AgreementEvaluation', back_populates='evidence_gaps')
