"""Tests for alerts router."""
from app.models import Alert


def test_list_alerts_empty(client):
    """Test list alerts when none exist."""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_list_alerts_with_filters(client, db_session):
    """Test list alerts with filters."""
    # Create test alerts
    alert1 = Alert(
        category="COST_INCREASE",
        severity="CRITICAL",
        status="NEW",
        source_ref_type="policy_event",
        source_ref_id=1,
        dedupe_key="pe:1:COST_INCREASE",
        alert_title="Critical cost increase",
        alert_description="Tariff increased by 15%",
        details={},
    )
    alert2 = Alert(
        category="AGREEMENT_OPPORTUNITY",
        severity="STANDARD",
        status="ACKNOWLEDGED",
        source_ref_type="scenario",
        source_ref_id=2,
        dedupe_key="scenario:2:AGREEMENT_OPPORTUNITY",
        alert_title="New trade agreement opportunity",
        alert_description="USMCA qualification possible",
        details={},
    )
    db_session.add_all([alert1, alert2])
    db_session.commit()

    # List all alerts
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    assert response.json()["total"] == 2

    # Filter by severity
    response = client.get("/api/v1/alerts?severity=CRITICAL")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["severity"] == "CRITICAL"

    # Filter by status
    response = client.get("/api/v1/alerts?status=NEW")
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_acknowledge_alert(client, db_session):
    """Test alert acknowledgement."""
    # Create alert
    alert = Alert(
        category="COST_INCREASE",
        severity="CRITICAL",
        status="NEW",
        source_ref_type="policy_event",
        source_ref_id=1,
        dedupe_key="pe:1:COST",
        alert_title="Test alert",
        alert_description="Test description",
        details={},
    )
    db_session.add(alert)
    db_session.commit()

    # Acknowledge alert
    payload = {"actor_id": 1}
    response = client.post(f"/api/v1/alerts/{alert.id}/acknowledge", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ACKNOWLEDGED"


def test_escalate_alert(client, db_session):
    """Test alert escalation."""
    # Create alert
    alert = Alert(
        category="COMPLIANCE_BLOCK",
        severity="CRITICAL",
        status="IN_PROGRESS",
        source_ref_type="recommendation",
        source_ref_id=1,
        dedupe_key="rec:1:COMPLIANCE_BLOCK",
        alert_title="Compliance block",
        alert_description="Blocked by forced labor risk",
        details={},
    )
    db_session.add(alert)
    db_session.commit()

    # Escalate alert
    payload = {
        "escalation_scope": {"team": "executive"},
        "actor_id": 1,
    }
    response = client.post(f"/api/v1/alerts/{alert.id}/escalate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ESCALATED"


def test_resolve_alert(client, db_session):
    """Test alert resolution."""
    # Create alert
    alert = Alert(
        category="COST_INCREASE",
        severity="STANDARD",
        status="IN_PROGRESS",
        source_ref_type="policy_event",
        source_ref_id=1,
        dedupe_key="pe:1:COST2",
        alert_title="Cost increase",
        alert_description="Minor cost impact",
        details={},
    )
    db_session.add(alert)
    db_session.commit()

    # Resolve alert
    payload = {
        "outcome_summary": "Mitigation implemented successfully",
        "actor_id": 1,
    }
    response = client.post(f"/api/v1/alerts/{alert.id}/resolve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RESOLVED"
