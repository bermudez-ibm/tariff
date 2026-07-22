"""Verify seed data counts match requirements."""
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.user import User, Role
from app.models.policy_event import PolicyEvent
from app.models.reference import Supplier, Product, SourcingLane
from app.models.scenario import ScenarioRequest, ScenarioResult
from app.models.agreement import AgreementEvaluation
from app.models.recommendation import Recommendation
from app.models.alert import Alert
from app.models.compliance import ComplianceReview


def verify_counts():
    """Verify all seed data requirements are met."""
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("="*60)
    print("Verifying Seed Data Counts")
    print("="*60 + "\n")
    
    try:
        # Users - at least 5 (admin + one per role)
        user_count = session.query(func.count(User.id)).scalar()
        print(f"✓ Users: {user_count} (requirement: >= 5)")
        assert user_count >= 5, f"Expected at least 5 users, got {user_count}"
        
        # Verify all users have roles
        users_without_roles = session.query(User).filter(~User.roles.any()).count()
        print(f"✓ All users have roles: {users_without_roles == 0}")
        assert users_without_roles == 0, f"Found {users_without_roles} users without role assignments"
        
        # Roles - at least 5 named roles
        role_count = session.query(func.count(Role.id)).scalar()
        print(f"✓ Roles: {role_count} (requirement: >= 5)")
        assert role_count >= 5, f"Expected at least 5 roles, got {role_count}"
        
        # Policy Events - at least 5
        event_count = session.query(func.count(PolicyEvent.id)).scalar()
        print(f"✓ Policy Events: {event_count} (requirement: >= 5)")
        assert event_count >= 5, f"Expected at least 5 policy events, got {event_count}"
        
        # Verify varying severity/geography
        events = session.query(PolicyEvent).all()
        severities = set(e.severity for e in events)
        print(f"  - Severities represented: {severities}")
        
        # Suppliers - at least 3
        supplier_count = session.query(func.count(Supplier.id)).scalar()
        print(f"✓ Suppliers: {supplier_count} (requirement: >= 3)")
        assert supplier_count >= 3, f"Expected at least 3 suppliers, got {supplier_count}"
        
        # Sourcing Lanes - at least 3
        lane_count = session.query(func.count(SourcingLane.id)).scalar()
        print(f"✓ Sourcing Lanes: {lane_count} (requirement: >= 3)")
        assert lane_count >= 3, f"Expected at least 3 sourcing lanes, got {lane_count}"
        
        # Products - at least 2
        product_count = session.query(func.count(Product.id)).scalar()
        print(f"✓ Products: {product_count} (requirement: >= 2)")
        assert product_count >= 2, f"Expected at least 2 products, got {product_count}"
        
        # Scenarios - at least 2 scenario results (baseline + alternate)
        scenario_result_count = session.query(func.count(ScenarioResult.id)).scalar()
        print(f"✓ Scenario Results: {scenario_result_count} (requirement: >= 2)")
        assert scenario_result_count >= 2, f"Expected at least 2 scenario results, got {scenario_result_count}"
        
        # Agreement Evaluations - at least 1 per USMCA/CPTPP/EVFTA
        usmca_count = session.query(func.count(AgreementEvaluation.id)).filter(
            AgreementEvaluation.agreement_code == "USMCA"
        ).scalar()
        cptpp_count = session.query(func.count(AgreementEvaluation.id)).filter(
            AgreementEvaluation.agreement_code == "CPTPP"
        ).scalar()
        evfta_count = session.query(func.count(AgreementEvaluation.id)).filter(
            AgreementEvaluation.agreement_code == "EVFTA"
        ).scalar()
        print(f"✓ Agreement Evaluations: USMCA={usmca_count}, CPTPP={cptpp_count}, EVFTA={evfta_count}")
        assert usmca_count >= 1 and cptpp_count >= 1 and evfta_count >= 1, \
            "Expected at least 1 evaluation per agreement type"
        
        # Recommendations - at least 3
        recommendation_count = session.query(func.count(Recommendation.id)).scalar()
        print(f"✓ Recommendations: {recommendation_count} (requirement: >= 3)")
        assert recommendation_count >= 3, f"Expected at least 3 recommendations, got {recommendation_count}"
        
        # Alerts - at least 5
        alert_count = session.query(func.count(Alert.id)).scalar()
        print(f"✓ Alerts: {alert_count} (requirement: >= 5)")
        assert alert_count >= 5, f"Expected at least 5 alerts, got {alert_count}"
        
        # Verify varying categories and severities
        alerts = session.query(Alert).all()
        alert_categories = set(a.alert_category for a in alerts)
        alert_severities = set(a.severity for a in alerts)
        print(f"  - Categories represented: {alert_categories}")
        print(f"  - Severities represented: {alert_severities}")
        
        # Compliance Reviews - at least 1
        review_count = session.query(func.count(ComplianceReview.id)).scalar()
        print(f"✓ Compliance Reviews: {review_count} (requirement: >= 1)")
        assert review_count >= 1, f"Expected at least 1 compliance review, got {review_count}"
        
        # Verify admin credentials
        admin = session.query(User).filter(User.email == "admin@example.com").first()
        print(f"\n✓ Admin user exists: {admin is not None}")
        assert admin is not None, "Admin user not found"
        assert admin.is_active, "Admin user is not active"
        assert len(admin.roles) > 0, "Admin has no roles"
        
        print("\n" + "="*60)
        print("All seed data requirements verified!")
        print("="*60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Verification failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(verify_counts())
