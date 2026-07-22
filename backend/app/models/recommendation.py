"""Mitigation recommendation models."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .base import BaseModel


class Recommendation(BaseModel):
    """Mitigation recommendation."""
    __tablename__ = 'recommendations'
    
    scenario_id = Column(Integer, ForeignKey('scenario_requests.id'), index=True)
    event_id = Column(Integer, ForeignKey('policy_events.id'), index=True)
    recommendation_type = Column(String(100), nullable=False, index=True)
    priority_score = Column(DECIMAL(10, 4), nullable=False)
    compliance_state = Column(String(50), nullable=False, index=True)
    disposition_state = Column(String(50), nullable=False, index=True)
    rationale_summary = Column(Text, nullable=False)
    
    # Relationships
    factors = relationship('RecommendationFactor', back_populates='recommendation', cascade='all, delete-orphan')


class RecommendationFactor(BaseModel):
    """Factor contributing to recommendation score and rationale."""
    __tablename__ = 'recommendation_factors'
    
    recommendation_id = Column(Integer, ForeignKey('recommendations.id'), nullable=False, index=True)
    factor_type = Column(String(100), nullable=False, index=True)
    factor_score = Column(DECIMAL(10, 4), nullable=False)
    explanation = Column(Text, nullable=False)
    
    # Relationships
    recommendation = relationship('Recommendation', back_populates='factors')
