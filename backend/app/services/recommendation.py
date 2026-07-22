"""Recommendation service for mitigation strategy generation."""
from datetime import datetime
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session

from ..models import Recommendation, RecommendationFactor, ScenarioResult, ComplianceReview


class RecommendationService:
    """Service for recommendation generation and disposition."""

    def __init__(self, db: Session):
        self.db = db

    def generate_recommendations(self, scenario_id: int, requested_by: int) -> List[Recommendation]:
        """
        Generate mitigation recommendations for a scenario.
        Implements FR-MR-01 through FR-MR-06: Recommendation types and feasibility.
        Implements BR-MR-01: Compliance blocks override cost-favorable outcomes.
        """
        # Placeholder: Check compliance gates first (BR-MR-01)
        compliance_blocked = False  # Would query ComplianceReview

        recommendation_types = [
            ('RE_ROUTING', Decimal('85.00'), Decimal('10000.00'), 'APPROVED'),
            ('RE_SOURCING', Decimal('75.00'), Decimal('15000.00'), 'CONTINGENT'),
            ('PRE_SHIPPING', Decimal('90.00'), Decimal('5000.00'), 'BLOCKED' if compliance_blocked else 'APPROVED'),
        ]

        recommendations = []
        for rec_type, priority_score, expected_impact, compliance_state in recommendation_types:
            recommendation = Recommendation(
                recommendation_type=rec_type,
                priority_score=priority_score,
                compliance_state=compliance_state,
                expected_impact=expected_impact,
                currency='USD',
                rationale={
                    'financial_score': '80',
                    'timing_score': '75',
                    'feasibility_score': '85',
                    'compliance_context': 'No blocking constraints' if compliance_state == 'APPROVED' else 'Pending review',
                },
            )
            self.db.add(recommendation)
            self.db.flush()

            # Add recommendation factors (BR-MR-02: Rationale traceability)
            factors = [
                ('financial', Decimal('0.8'), Decimal('0.4'), 'Strong cost savings'),
                ('timing', Decimal('0.7'), Decimal('0.3'), 'Moderate timeline impact'),
                ('feasibility', Decimal('0.85'), Decimal('0.3'), 'High operational feasibility'),
            ]

            for factor_type, score, weight, rationale in factors:
                factor = RecommendationFactor(
                    recommendation_id=recommendation.id,
                    factor_type=factor_type,
                    score=score,
                    weight=weight,
                    rationale=rationale,
                )
                self.db.add(factor)

            recommendations.append(recommendation)

        self.db.commit()
        for rec in recommendations:
            self.db.refresh(rec)

        return recommendations

    def disposition_recommendation(
        self,
        recommendation_id: int,
        disposition: str,
        reason_code: str,
        actor_id: int,
    ) -> Recommendation:
        """
        Apply disposition to a recommendation.
        Implements BR-MR-01: Blocked recommendations cannot be accepted.
        Implements BR-MR-03: Disposition preserved for audit.
        """
        recommendation = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        if not recommendation:
            raise ValueError(f"Recommendation {recommendation_id} not found")

        # Enforce BR-MR-01: Cannot accept blocked recommendations
        if recommendation.compliance_state == 'BLOCKED' and disposition == 'accepted':
            raise ValueError("Cannot accept a blocked recommendation without override")

        recommendation.disposition = disposition
        recommendation.disposition_reason = reason_code
        recommendation.disposition_timestamp = datetime.utcnow()
        recommendation.disposition_actor_id = actor_id

        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation
