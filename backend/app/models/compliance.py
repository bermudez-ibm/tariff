"""Compliance review and risk flag models."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class ComplianceReview(BaseModel):
    """Compliance review workflow."""
    __tablename__ = 'compliance_reviews'
    
    subject_type = Column(String(100), nullable=False, index=True)
    subject_id = Column(Integer, nullable=False, index=True)
    review_state = Column(String(50), nullable=False, index=True)
    approver_role = Column(String(100))
    reason_code = Column(String(100), nullable=False)
    notes = Column(Text)
    required_evidence_refs = Column(JSON)
    
    # Relationships
    risk_flags = relationship('RiskFlag', back_populates='review', cascade='all, delete-orphan')


class RiskFlag(BaseModel):
    """Risk flag for compliance concerns."""
    __tablename__ = 'risk_flags'
    
    review_id = Column(Integer, ForeignKey('compliance_reviews.id'), index=True)
    subject_type = Column(String(100), nullable=False, index=True)
    subject_id = Column(Integer, nullable=False, index=True)
    risk_category = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, index=True)
    detected_at = Column(DateTime, nullable=False)
    
    # Relationships
    review = relationship('ComplianceReview', back_populates='risk_flags')
