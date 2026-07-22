"""Financial analysis service for landed-cost calculation and scenario comparison."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models import ScenarioRequest, ScenarioResult, CostComponent, SourcingLane


class FinancialAnalysisService:
    """Service for landed-cost calculation and scenario analysis."""

    def __init__(self, db: Session):
        self.db = db

    def create_scenario_request(
        self,
        baseline_lane_id: int,
        alternate_lane_ids: List[int],
        requested_by: int,
    ) -> ScenarioRequest:
        """
        Create scenario request for cost comparison.
        Implements FR-LC-01, FR-LC-02: Landed-cost calculation and scenario comparison.
        """
        scenario = ScenarioRequest(
            baseline_lane_id=baseline_lane_id,
            alternate_lane_ids=alternate_lane_ids,
            requested_by=requested_by,
        )
        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def calculate_scenario(self, scenario_id: int) -> ScenarioResult:
        """
        Calculate landed cost for a scenario lane.
        Implements BR-LC-01: Scenario comparison within 60 seconds (placeholder timing).
        Implements BR-LC-02: Cost component traceability.
        """
        scenario = self.db.query(ScenarioRequest).filter(ScenarioRequest.id == scenario_id).first()
        if not scenario:
            raise ValueError(f"ScenarioRequest {scenario_id} not found")

        lane = self.db.query(SourcingLane).filter(SourcingLane.id == scenario.baseline_lane_id).first()
        if not lane:
            raise ValueError(f"SourcingLane {scenario.baseline_lane_id} not found")

        # Placeholder cost calculation (real implementation would query reference data)
        result = ScenarioResult(
            scenario_request_id=scenario.id,
            lane_id=lane.id,
            lane_type='baseline',
            total_landed_cost=Decimal('100.00'),
            currency='USD',
            margin_impact=Decimal('5.00'),
            completeness_status='complete',
        )
        self.db.add(result)
        self.db.flush()

        # Create cost components (BR-LC-02: traceability)
        components = [
            ('manufacturing', Decimal('40.00'), 'Base manufacturing cost'),
            ('shipping', Decimal('20.00'), 'Ocean freight'),
            ('storage', Decimal('10.00'), 'Warehouse handling'),
            ('tariff', Decimal('15.00'), 'Import duty'),
            ('duty', Decimal('10.00'), 'Additional customs duty'),
            ('additive', Decimal('5.00'), 'Insurance and fees'),
        ]

        for comp_type, amount, description in components:
            component = CostComponent(
                scenario_result_id=result.id,
                component_type=comp_type,
                amount=amount,
                currency='USD',
                description=description,
            )
            self.db.add(component)

        self.db.commit()
        self.db.refresh(result)
        return result

    def get_scenario_comparison(self, scenario_id: int, baseline_id: int, alternate_id: int) -> dict:
        """
        Compare baseline and alternate scenario results.
        Implements FR-LC-03: Scenario comparison with cost deltas.
        """
        baseline = self.db.query(ScenarioResult).filter(ScenarioResult.id == baseline_id).first()
        alternate = self.db.query(ScenarioResult).filter(ScenarioResult.id == alternate_id).first()

        if not baseline or not alternate:
            raise ValueError("Scenario results not found")

        cost_delta = alternate.total_landed_cost - baseline.total_landed_cost
        margin_delta = None
        if baseline.margin_impact and alternate.margin_impact:
            margin_delta = alternate.margin_impact - baseline.margin_impact

        # Component-level deltas
        baseline_comps = {c.component_type: c.amount for c in baseline.cost_components}
        alternate_comps = {c.component_type: c.amount for c in alternate.cost_components}

        component_deltas = []
        for comp_type in set(baseline_comps.keys()) | set(alternate_comps.keys()):
            b_amt = baseline_comps.get(comp_type, Decimal('0'))
            a_amt = alternate_comps.get(comp_type, Decimal('0'))
            component_deltas.append({
                'component_type': comp_type,
                'baseline_amount': b_amt,
                'alternate_amount': a_amt,
                'delta': a_amt - b_amt,
            })

        return {
            'baseline': baseline,
            'alternate': alternate,
            'cost_delta': cost_delta,
            'margin_impact_delta': margin_delta,
            'component_deltas': component_deltas,
        }
