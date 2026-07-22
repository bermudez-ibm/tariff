"""Idempotent seed data script for Tariff Resilience application.

REQ-OPS-001: Seed default users, policy events, suppliers, products, scenarios,
agreement evaluations, recommendations, alerts, and compliance reviews.

Run via: python3 app/seed.py
Or import: from app.seed import seed_database
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.models.base import Base
from app.models.user import User, Role
from app.models.policy_event import PolicyEvent, EventDelta
from app.models.reference import Country, Supplier, Product, Port, Route, SourcingLane
from app.models.scenario import ScenarioRequest, ScenarioResult, CostComponent
from app.models.agreement import AgreementEvaluation, EvidenceGap
from app.models.recommendation import Recommendation
from app.models.alert import Alert
from app.models.compliance import ComplianceReview


def hash_password(plain_password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')


def seed_database():
    """Seed the database with default data idempotently."""
    # Create engine and session
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Seed Roles
        roles_data = [
            {"name": "Trade Compliance Manager", "description": "Monitors policy changes, reviews compliance-sensitive decisions"},
            {"name": "Strategic Sourcing Manager", "description": "Evaluates supplier alternatives, assesses country-of-origin implications"},
            {"name": "Finance Analyst", "description": "Quantifies margin impact, validates cost assumptions"},
            {"name": "Supply Chain Planner", "description": "Evaluates logistics alternatives, timing feasibility"},
            {"name": "Executive", "description": "Oversight of exposure concentration, unresolved risks, mitigation effectiveness"},
        ]
        
        roles = {}
        for role_data in roles_data:
            role = session.query(Role).filter(Role.name == role_data["name"]).first()
            if not role:
                role = Role(**role_data)
                session.add(role)
                session.flush()
            roles[role_data["name"]] = role
        
        # Seed Users (admin + one per role)
        users_data = [
            {"email": "admin@example.com", "password": "admin123", "full_name": "Admin User", "roles": list(roles.values())},
            {"email": "compliance@example.com", "password": "compliance123", "full_name": "Compliance Manager", "roles": [roles["Trade Compliance Manager"]]},
            {"email": "sourcing@example.com", "password": "sourcing123", "full_name": "Sourcing Manager", "roles": [roles["Strategic Sourcing Manager"]]},
            {"email": "finance@example.com", "password": "finance123", "full_name": "Finance Analyst", "roles": [roles["Finance Analyst"]]},
            {"email": "planner@example.com", "password": "planner123", "full_name": "Supply Chain Planner", "roles": [roles["Supply Chain Planner"]]},
            {"email": "exec@example.com", "password": "exec123", "full_name": "Executive Leader", "roles": [roles["Executive"]]},
        ]
        
        users = {}
        for user_data in users_data:
            user = session.query(User).filter(User.email == user_data["email"]).first()
            if not user:
                user = User(
                    email=user_data["email"],
                    password_hash=hash_password(user_data["password"]),
                    full_name=user_data["full_name"],
                    is_active=True
                )
                user.roles = user_data["roles"]
                session.add(user)
                session.flush()
            users[user_data["email"]] = user
        
        # Seed Countries
        countries_data = [
            {"country_code": "CN", "country_name": "China"},
            {"country_code": "VN", "country_name": "Vietnam"},
            {"country_code": "BD", "country_name": "Bangladesh"},
            {"country_code": "MX", "country_name": "Mexico"},
            {"country_code": "ET", "country_name": "Ethiopia"},
            {"country_code": "US", "country_name": "United States"},
        ]
        
        countries = {}
        for country_data in countries_data:
            country = session.query(Country).filter(Country.country_code == country_data["country_code"]).first()
            if not country:
                country = Country(**country_data)
                session.add(country)
                session.flush()
            countries[country_data["country_code"]] = country
        
        # Seed Suppliers
        suppliers_data = [
            {"supplier_external_id": "SUP-001", "supplier_name": "Pacific Footwear Co.", "country_code": "CN"},
            {"supplier_external_id": "SUP-002", "supplier_name": "Southeast Textiles", "country_code": "VN"},
            {"supplier_external_id": "SUP-003", "supplier_name": "Global Apparel Ltd.", "country_code": "BD"},
            {"supplier_external_id": "SUP-004", "supplier_name": "American Sourcing Partners", "country_code": "MX"},
        ]
        
        suppliers = {}
        for supplier_data in suppliers_data:
            supplier = session.query(Supplier).filter(Supplier.supplier_external_id == supplier_data["supplier_external_id"]).first()
            if not supplier:
                supplier = Supplier(**supplier_data)
                session.add(supplier)
                session.flush()
            suppliers[supplier_data["supplier_external_id"]] = supplier
        
        # Seed Products
        products_data = [
            {"product_external_id": "SHOE-001", "product_name": "Running Shoe Model A", "hts_code": "6403.99", "product_segment": "Footwear", "material_type": "Leather"},
            {"product_external_id": "SHIRT-001", "product_name": "Cotton T-Shirt Basic", "hts_code": "6109.10", "product_segment": "Apparel", "material_type": "Cotton"},
            {"product_external_id": "JACKET-001", "product_name": "Winter Jacket Premium", "hts_code": "6201.93", "product_segment": "Apparel", "material_type": "Synthetic"},
        ]
        
        products = {}
        for product_data in products_data:
            product = session.query(Product).filter(Product.product_external_id == product_data["product_external_id"]).first()
            if not product:
                product = Product(**product_data)
                session.add(product)
                session.flush()
            products[product_data["product_external_id"]] = product
        
        # Seed Ports
        ports_data = [
            {"port_code": "CNGUA", "port_name": "Guangzhou", "country_code": "CN"},
            {"port_code": "VNHCM", "port_name": "Ho Chi Minh", "country_code": "VN"},
            {"port_code": "BDCGP", "port_name": "Chittagong", "country_code": "BD"},
            {"port_code": "MXVER", "port_name": "Veracruz", "country_code": "MX"},
            {"port_code": "USLAX", "port_name": "Los Angeles", "country_code": "US"},
            {"port_code": "USNYC", "port_name": "New York", "country_code": "US"},
            {"port_code": "USHOU", "port_name": "Houston", "country_code": "US"},
        ]
        
        ports = {}
        for port_data in ports_data:
            port = session.query(Port).filter(Port.port_code == port_data["port_code"]).first()
            if not port:
                port = Port(**port_data)
                session.add(port)
                session.flush()
            ports[port_data["port_code"]] = port
        
        # Seed Routes
        routes_data = [
            {"route_external_id": "RT-001", "origin_port_code": "CNGUA", "destination_port_code": "USLAX", "shipping_mode": "Ocean"},
            {"route_external_id": "RT-002", "origin_port_code": "VNHCM", "destination_port_code": "USLAX", "shipping_mode": "Ocean"},
            {"route_external_id": "RT-003", "origin_port_code": "BDCGP", "destination_port_code": "USNYC", "shipping_mode": "Ocean"},
            {"route_external_id": "RT-004", "origin_port_code": "MXVER", "destination_port_code": "USHOU", "shipping_mode": "Ocean"},
        ]
        
        routes = {}
        for route_data in routes_data:
            route = session.query(Route).filter(Route.route_external_id == route_data["route_external_id"]).first()
            if not route:
                route = Route(**route_data)
                session.add(route)
                session.flush()
            routes[route_data["route_external_id"]] = route
        
        # Seed Sourcing Lanes
        lanes_data = [
            {"lane_external_id": "LANE-001", "supplier_id": suppliers["SUP-001"].id, "product_id": products["SHOE-001"].id, "route_id": routes["RT-001"].id, "origin_country_code": "CN", "destination_country_code": "US"},
            {"lane_external_id": "LANE-002", "supplier_id": suppliers["SUP-002"].id, "product_id": products["SHOE-001"].id, "route_id": routes["RT-002"].id, "origin_country_code": "VN", "destination_country_code": "US"},
            {"lane_external_id": "LANE-003", "supplier_id": suppliers["SUP-003"].id, "product_id": products["SHIRT-001"].id, "route_id": routes["RT-003"].id, "origin_country_code": "BD", "destination_country_code": "US"},
            {"lane_external_id": "LANE-004", "supplier_id": suppliers["SUP-004"].id, "product_id": products["JACKET-001"].id, "route_id": routes["RT-004"].id, "origin_country_code": "MX", "destination_country_code": "US"},
        ]
        
        lanes = {}
        for lane_data in lanes_data:
            lane = session.query(SourcingLane).filter(SourcingLane.lane_external_id == lane_data["lane_external_id"]).first()
            if not lane:
                lane = SourcingLane(**lane_data)
                session.add(lane)
                session.flush()
            lanes[lane_data["lane_external_id"]] = lane
        
        # Seed Policy Events
        base_date = datetime.now() - timedelta(days=30)
        events_data = [
            {
                "source_system": "TradeWatch",
                "event_external_id": "TW-2024-001",
                "policy_type": "TARIFF_CHANGE",
                "severity": "CRITICAL",
                "effective_date": (base_date + timedelta(days=5)).date(),
                "impacted_geographies": ["CN", "US"],
                "current_state": {"tariff_rate": "25%", "description": "Section 301 tariff increase on Chinese footwear from 15% to 25%"},
                "prior_state": {"tariff_rate": "15%"},
                "materiality_state": "MATERIAL",
                "actionable_flag": True,
                "ingested_at": datetime.now(),
            },
            {
                "source_system": "ComplianceHub",
                "event_external_id": "CH-2024-002",
                "policy_type": "FORCED_LABOR_RESTRICTION",
                "severity": "CRITICAL",
                "effective_date": (base_date + timedelta(days=10)).date(),
                "impacted_geographies": ["CN"],
                "current_state": {"description": "Xinjiang cotton import restrictions expanded to additional suppliers"},
                "materiality_state": "MATERIAL",
                "actionable_flag": True,
                "ingested_at": datetime.now(),
            },
            {
                "source_system": "TradeWatch",
                "event_external_id": "TW-2024-003",
                "policy_type": "TRADE_AGREEMENT_REVISION",
                "severity": "STANDARD",
                "effective_date": (base_date + timedelta(days=15)).date(),
                "impacted_geographies": ["VN", "US"],
                "current_state": {"description": "Vietnam environmental compliance audit requirements under EVFTA"},
                "materiality_state": "WATCHLIST",
                "actionable_flag": False,
                "ingested_at": datetime.now(),
            },
            {
                "source_system": "TradeWatch",
                "event_external_id": "TW-2024-004",
                "policy_type": "AGOA_STATUS_CHANGE",
                "severity": "STANDARD",
                "effective_date": (base_date + timedelta(days=20)).date(),
                "impacted_geographies": ["ET"],
                "current_state": {"description": "Ethiopia AGOA eligibility under review"},
                "materiality_state": "WATCHLIST",
                "actionable_flag": True,
                "ingested_at": datetime.now(),
            },
            {
                "source_system": "LogisticsNet",
                "event_external_id": "LN-2024-005",
                "policy_type": "PORT_DISRUPTION",
                "severity": "INFORMATIONAL",
                "effective_date": (base_date + timedelta(days=25)).date(),
                "impacted_geographies": ["US"],
                "current_state": {"description": "Los Angeles port labor negotiations ongoing, minor delays expected"},
                "materiality_state": "NON_MATERIAL",
                "actionable_flag": False,
                "ingested_at": datetime.now(),
            },
        ]
        
        events = {}
        for event_data in events_data:
            event = session.query(PolicyEvent).filter(
                PolicyEvent.source_system == event_data["source_system"],
                PolicyEvent.event_external_id == event_data["event_external_id"]
            ).first()
            if not event:
                event = PolicyEvent(**event_data)
                session.add(event)
                session.flush()
            events[event_data["event_external_id"]] = event
        
        # Seed Scenario Requests and Results
        admin_user = users["admin@example.com"]
        china_lane = lanes["LANE-001"]
        vietnam_lane = lanes["LANE-002"]
        
        scenario_request = session.query(ScenarioRequest).filter(
            ScenarioRequest.requested_by == admin_user.id
        ).first()
        
        if not scenario_request:
            scenario_request = ScenarioRequest(
                requested_by=admin_user.id,
                baseline_lane_id=china_lane.id,
                alternate_lane_ids=[vietnam_lane.id],
                request_source="Manual",
            )
            session.add(scenario_request)
            session.flush()
            
            # Baseline scenario result
            baseline_result = ScenarioResult(
                scenario_id=scenario_request.id,
                lane_id=china_lane.id,
                is_baseline=True,
                total_landed_cost=52.30,
                margin_impact=-0.15,
                completeness_status="COMPLETE",
                calculation_timestamp=datetime.now(),
                input_snapshot={"tariff_rate": "25%", "manufacturing_cost": 25.00}
            )
            session.add(baseline_result)
            session.flush()
            
            # Cost components for baseline
            baseline_components = [
                {"scenario_result_id": baseline_result.id, "component_type": "MANUFACTURING", "amount": 25.00, "currency": "USD"},
                {"scenario_result_id": baseline_result.id, "component_type": "SHIPPING", "amount": 8.50, "currency": "USD"},
                {"scenario_result_id": baseline_result.id, "component_type": "STORAGE", "amount": 3.80, "currency": "USD"},
                {"scenario_result_id": baseline_result.id, "component_type": "TARIFF", "amount": 12.50, "currency": "USD"},  # 25% tariff
                {"scenario_result_id": baseline_result.id, "component_type": "DUTY", "amount": 2.50, "currency": "USD"},
            ]
            for comp_data in baseline_components:
                comp = CostComponent(**comp_data)
                session.add(comp)
            
            # Alternate scenario result
            alternate_result = ScenarioResult(
                scenario_id=scenario_request.id,
                lane_id=vietnam_lane.id,
                is_baseline=False,
                total_landed_cost=48.20,
                margin_impact=0.05,
                completeness_status="COMPLETE",
                calculation_timestamp=datetime.now(),
                input_snapshot={"tariff_rate": "15%", "manufacturing_cost": 26.00}
            )
            session.add(alternate_result)
            session.flush()
            
            # Cost components for alternate
            alternate_components = [
                {"scenario_result_id": alternate_result.id, "component_type": "MANUFACTURING", "amount": 26.00, "currency": "USD"},
                {"scenario_result_id": alternate_result.id, "component_type": "SHIPPING", "amount": 9.00, "currency": "USD"},
                {"scenario_result_id": alternate_result.id, "component_type": "STORAGE", "amount": 4.00, "currency": "USD"},
                {"scenario_result_id": alternate_result.id, "component_type": "TARIFF", "amount": 7.50, "currency": "USD"},  # Lower tariff
                {"scenario_result_id": alternate_result.id, "component_type": "DUTY", "amount": 1.70, "currency": "USD"},
            ]
            for comp_data in alternate_components:
                comp = CostComponent(**comp_data)
                session.add(comp)
        
        # Seed Agreement Evaluations
        scenario_results = session.query(ScenarioResult).all()
        if scenario_results:
            for result in scenario_results[:2]:  # First two results
                # USMCA evaluation
                usmca_eval = session.query(AgreementEvaluation).filter(
                    AgreementEvaluation.scenario_result_id == result.id,
                    AgreementEvaluation.agreement_code == "USMCA"
                ).first()
                if not usmca_eval:
                    usmca_eval = AgreementEvaluation(
                        scenario_result_id=result.id,
                        agreement_code="USMCA",
                        qualification_status="CONTINGENT",
                        estimated_savings=2.30,
                        evidence_state="INCOMPLETE",
                        evaluated_at=datetime.now()
                    )
                    session.add(usmca_eval)
                    session.flush()
                    
                    # Evidence gap for USMCA
                    gap = EvidenceGap(
                        agreement_evaluation_id=usmca_eval.id,
                        gap_type="ORIGIN_DOCUMENTATION",
                        severity="BLOCKING",
                        blocking_flag=True,
                        details={"description": "Supplier certificate of origin pending"}
                    )
                    session.add(gap)
                
                # CPTPP evaluation
                cptpp_eval = session.query(AgreementEvaluation).filter(
                    AgreementEvaluation.scenario_result_id == result.id,
                    AgreementEvaluation.agreement_code == "CPTPP"
                ).first()
                if not cptpp_eval:
                    cptpp_eval = AgreementEvaluation(
                        scenario_result_id=result.id,
                        agreement_code="CPTPP",
                        qualification_status="QUALIFIED",
                        estimated_savings=1.80,
                        evidence_state="COMPLETE",
                        evaluated_at=datetime.now()
                    )
                    session.add(cptpp_eval)
                
                # EVFTA evaluation
                evfta_eval = session.query(AgreementEvaluation).filter(
                    AgreementEvaluation.scenario_result_id == result.id,
                    AgreementEvaluation.agreement_code == "EVFTA"
                ).first()
                if not evfta_eval:
                    evfta_eval = AgreementEvaluation(
                        scenario_result_id=result.id,
                        agreement_code="EVFTA",
                        qualification_status="BLOCKED",
                        estimated_savings=0.00,
                        evidence_state="INCOMPLETE",
                        evaluated_at=datetime.now()
                    )
                    session.add(evfta_eval)
        
        # Seed Recommendations
        recommendations_data = [
            {
                "recommendation_type": "RE_SOURCING",
                "priority_score": 0.85,
                "compliance_state": "APPROVED",
                "disposition_state": "PENDING",
                "rationale_summary": "Reduce landed cost by $4.10/unit, avoid 25% Section 301 tariff. Cost savings feasible, timing reasonable, compliance approved.",
            },
            {
                "recommendation_type": "PRE_SHIPPING",
                "priority_score": 0.72,
                "compliance_state": "CONTINGENT",
                "disposition_state": "PENDING",
                "rationale_summary": "Lock in current tariff rate before increase effective date. Timing urgent, inventory available, pending compliance review.",
            },
            {
                "recommendation_type": "EXECUTIVE_ESCALATION",
                "priority_score": 0.90,
                "compliance_state": "BLOCKED",
                "disposition_state": "PENDING",
                "rationale_summary": "Critical compliance review required before any sourcing decision. High forced labor risk detected, supplier audit incomplete.",
            },
        ]
        
        for rec_data in recommendations_data:
            rec = session.query(Recommendation).filter(
                Recommendation.recommendation_type == rec_data["recommendation_type"],
                Recommendation.priority_score == rec_data["priority_score"]
            ).first()
            if not rec:
                rec = Recommendation(**rec_data)
                session.add(rec)
        
        # Seed Alerts
        alerts_data = [
            {
                "category": "COST_INCREASE",
                "severity": "CRITICAL",
                "owner_id": users["finance@example.com"].id,
                "status": "NEW",
                "source_ref_type": "policy_event",
                "source_ref_id": events["TW-2024-001"].id,
                "dedupe_key": "cost_increase_tw_2024_001",
                "alert_title": "Critical Cost Increase Alert",
                "alert_description": "Tariff policy change TW-2024-001 causing significant cost impact",
                "details": {},
            },
            {
                "category": "COMPLIANCE_BLOCK",
                "severity": "CRITICAL",
                "owner_id": users["compliance@example.com"].id,
                "status": "ACKNOWLEDGED",
                "source_ref_type": "policy_event",
                "source_ref_id": events["CH-2024-002"].id,
                "dedupe_key": "compliance_block_ch_2024_002",
                "alert_title": "Compliance Block Alert",
                "alert_description": "Policy event CH-2024-002 requires compliance review",
                "details": {},
            },
            {
                "category": "AGREEMENT_OPPORTUNITY",
                "severity": "STANDARD",
                "owner_id": users["sourcing@example.com"].id,
                "status": "IN_PROGRESS",
                "source_ref_type": "agreement_evaluation",
                "source_ref_id": 1,
                "dedupe_key": "agreement_opp_cptpp_vn",
                "alert_title": "Trade Agreement Opportunity",
                "alert_description": "CPTPP agreement evaluation shows potential benefits",
                "details": {},
            },
            {
                "category": "SUPPLIER_DISRUPTION",
                "severity": "STANDARD",
                "owner_id": users["planner@example.com"].id,
                "status": "RESOLVED",
                "source_ref_type": "policy_event",
                "source_ref_id": events["TW-2024-004"].id,
                "dedupe_key": "supplier_disruption_agoa_et",
                "alert_title": "Supplier Disruption Notice",
                "alert_description": "AGOA policy change affecting Ethiopian supplier",
                "details": {},
            },
            {
                "category": "ROUTE_DISRUPTION",
                "severity": "INFORMATIONAL",
                "owner_id": users["planner@example.com"].id,
                "status": "DISMISSED",
                "source_ref_type": "policy_event",
                "source_ref_id": events["LN-2024-005"].id,
                "dedupe_key": "route_disruption_la_port",
                "alert_title": "Route Disruption Information",
                "alert_description": "LA Port congestion may affect delivery schedules",
                "details": {},
            },
        ]
        
        for alert_data in alerts_data:
            alert = session.query(Alert).filter(Alert.dedupe_key == alert_data["dedupe_key"]).first()
            if not alert:
                alert = Alert(**alert_data)
                session.add(alert)
        
        # Seed Compliance Reviews
        compliance_reviews_data = [
            {
                "subject_type": "recommendation",
                "subject_id": 1,
                "review_state": "APPROVED",
                "approver_role": "Trade Compliance Manager",
                "reason_code": "COST_JUSTIFIED_NO_COMPLIANCE_ISSUES",
                "notes": "Re-sourcing to Vietnam approved, no forced labor concerns identified",
            },
            {
                "subject_type": "recommendation",
                "subject_id": 3,
                "review_state": "BLOCKED",
                "approver_role": "Trade Compliance Manager",
                "reason_code": "FORCED_LABOR_AUDIT_INCOMPLETE",
                "notes": "Supplier audit incomplete, cannot proceed until cleared",
            },
        ]
        
        for review_data in compliance_reviews_data:
            review = session.query(ComplianceReview).filter(
                ComplianceReview.subject_type == review_data["subject_type"],
                ComplianceReview.subject_id == review_data["subject_id"]
            ).first()
            if not review:
                review = ComplianceReview(**review_data)
                session.add(review)
        
        # Commit all changes
        session.commit()
        
        print("\n" + "="*60)
        print("Seeding complete. Default credentials:")
        print("  admin@example.com / admin123")
        print("="*60)
        print("\nAll users:")
        for user_data in users_data:
            print(f"  {user_data['email']} / {user_data['password']}")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()


if __name__ == "__main__":
    success = seed_database()
    sys.exit(0 if success else 1)
