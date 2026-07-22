"""Trade agreement service for evaluation and qualification."""
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session

from ..models import AgreementEvaluation, EvidenceGap, ScenarioResult


class TradeAgreementService:
    """Service for trade agreement evaluation and savings calculation."""

    def __init__(self, db: Session):
        self.db = db

    def evaluate_agreements(self, scenario_result_id: int) -> List[AgreementEvaluation]:
        """
        Evaluate all applicable trade agreements for a scenario result.
        Implements FR-TA-01 through FR-TA-03: USMCA, CPTPP, EVFTA qualification.
        Implements BR-TA-01: Blocked/contingent qualification prevents auto-approval.
        """
        result = self.db.query(ScenarioResult).filter(ScenarioResult.id == scenario_result_id).first()
        if not result:
            raise ValueError(f"ScenarioResult {scenario_result_id} not found")

        # Evaluate each applicable agreement (placeholder logic)
        agreement_codes = ['USMCA', 'CPTPP', 'EVFTA']
        evaluations = []

        for agreement_code in agreement_codes:
            # Placeholder qualification logic
            qualification_status = 'QUALIFIED' if agreement_code == 'USMCA' else 'CONTINGENT'
            estimated_savings = Decimal('5000.00') if agreement_code == 'USMCA' else Decimal('2000.00')
            evidence_state = 'complete' if qualification_status == 'QUALIFIED' else 'incomplete'

            evaluation = AgreementEvaluation(
                scenario_result_id=scenario_result_id,
                agreement_code=agreement_code,
                qualification_status=qualification_status,
                estimated_savings=estimated_savings,
                currency='USD',
                evidence_state=evidence_state,
            )
            self.db.add(evaluation)
            self.db.flush()

            # Add evidence gaps for contingent/blocked states (BR-TA-02)
            if qualification_status in ['CONTINGENT', 'BLOCKED']:
                gap = EvidenceGap(
                    agreement_evaluation_id=evaluation.id,
                    gap_type='documentation',
                    severity='high',
                    blocking_flag=(qualification_status == 'BLOCKED'),
                    description=f"Missing origin certificate for {agreement_code}",
                )
                self.db.add(gap)

            evaluations.append(evaluation)

        self.db.commit()
        for eval in evaluations:
            self.db.refresh(eval)

        return evaluations

    def get_agreement_evaluation(self, evaluation_id: int) -> AgreementEvaluation:
        """Retrieve single agreement evaluation with evidence gaps."""
        evaluation = self.db.query(AgreementEvaluation).filter(
            AgreementEvaluation.id == evaluation_id
        ).first()
        if not evaluation:
            raise ValueError(f"AgreementEvaluation {evaluation_id} not found")
        return evaluation
