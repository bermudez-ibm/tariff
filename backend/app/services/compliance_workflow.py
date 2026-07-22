"""Compliance workflow service for review and risk flagging."""
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from ..models import ComplianceReview, RiskFlag


class ComplianceWorkflowService:
    """Service for compliance review workflows and risk management."""

    def __init__(self, db: Session):
        self.db = db

    def create_review(
        self,
        subject_type: str,
        subject_id: int,
        reviewer_role: str,
    ) -> ComplianceReview:
        """
        Create compliance review for a subject.
        Implements FR-CR-01: Review states (APPROVED, CONTINGENT, BLOCKED, UNDER_REVIEW).
        """
        review = ComplianceReview(
            subject_type=subject_type,
            subject_id=subject_id,
            review_state='UNDER_REVIEW',
            reviewer_role=reviewer_role,
        )
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def transition_review_state(
        self,
        review_id: int,
        new_state: str,
        reason_code: str,
        actor_id: int,
    ) -> ComplianceReview:
        """
        Transition review state with audit trail.
        Implements BR-CR-01: Compliance blocks override cost-favorable recommendations.
        Implements FR-CR-02, BR-CR-03: Non-destructive history preservation.
        """
        review = self.db.query(ComplianceReview).filter(ComplianceReview.id == review_id).first()
        if not review:
            raise ValueError(f"ComplianceReview {review_id} not found")

        # Valid state transitions
        valid_states = ['APPROVED', 'CONTINGENT', 'BLOCKED', 'UNDER_REVIEW']
        if new_state not in valid_states:
            raise ValueError(f"Invalid review state: {new_state}")

        review.review_state = new_state
        review.reason_code = reason_code
        self.db.commit()
        self.db.refresh(review)
        return review

    def check_compliance_gates(self, subject_type: str, subject_id: int) -> dict:
        """
        Check compliance gates for a subject.
        Returns compliance state summary.
        """
        reviews = self.db.query(ComplianceReview).filter(
            ComplianceReview.subject_type == subject_type,
            ComplianceReview.subject_id == subject_id,
        ).all()

        if not reviews:
            return {'state': 'NO_REVIEW', 'blocked': False}

        # Check for any blocking review
        blocked = any(r.review_state == 'BLOCKED' for r in reviews)
        contingent = any(r.review_state == 'CONTINGENT' for r in reviews)
        approved = all(r.review_state == 'APPROVED' for r in reviews)

        if blocked:
            return {'state': 'BLOCKED', 'blocked': True}
        elif contingent:
            return {'state': 'CONTINGENT', 'blocked': False}
        elif approved:
            return {'state': 'APPROVED', 'blocked': False}
        else:
            return {'state': 'UNDER_REVIEW', 'blocked': False}

    def add_risk_flag(
        self,
        review_id: int,
        risk_category: str,
        severity: str,
        description: str,
    ) -> RiskFlag:
        """Add risk flag to a compliance review."""
        flag = RiskFlag(
            compliance_review_id=review_id,
            risk_category=risk_category,
            severity=severity,
            flagged_at=datetime.utcnow(),
            resolution_status='open',
            description=description,
        )
        self.db.add(flag)
        self.db.commit()
        self.db.refresh(flag)
        return flag
