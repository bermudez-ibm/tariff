"""Tests for policy events router."""
from datetime import datetime


def test_ingest_policy_event(client):
    """Test policy event ingestion."""
    payload = {
        "source_system": "external_api",
        "event_external_id": "EVENT-001",
        "policy_type": "tariff_change",
        "severity": "critical",
        "effective_date": datetime.utcnow().isoformat(),
        "impacted_geographies": ["CN", "VN"],
        "relevance_type": "primary",
        "description": "Test event",
        "deltas": [
            {
                "field_name": "tariff_rate",
                "prior_value": "10%",
                "current_value": "25%",
            }
        ],
    }

    response = client.post("/api/v1/policy-events:ingest", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["source_system"] == "external_api"
    assert data["event_external_id"] == "EVENT-001"
    assert data["severity"] == "critical"


def test_ingest_policy_event_idempotent(client):
    """Test policy event ingestion is idempotent."""
    payload = {
        "source_system": "external_api",
        "event_external_id": "EVENT-002",
        "policy_type": "tariff_change",
        "severity": "high",
        "effective_date": datetime.utcnow().isoformat(),
        "impacted_geographies": ["CN"],
        "relevance_type": "primary",
    }

    # First ingestion
    response1 = client.post("/api/v1/policy-events:ingest", json=payload)
    assert response1.status_code == 201
    id1 = response1.json()["id"]

    # Second ingestion (should return same event)
    response2 = client.post("/api/v1/policy-events:ingest", json=payload)
    assert response2.status_code == 201
    id2 = response2.json()["id"]

    assert id1 == id2


def test_list_policy_events_pagination(client):
    """Test policy events list with pagination."""
    # Create test events
    for i in range(5):
        payload = {
            "source_system": "test_system",
            "event_external_id": f"EVENT-{i}",
            "policy_type": "tariff_change",
            "severity": "medium",
            "effective_date": datetime.utcnow().isoformat(),
            "impacted_geographies": ["US"],
            "relevance_type": "primary",
        }
        client.post("/api/v1/policy-events:ingest", json=payload)

    # List first page
    response = client.get("/api/v1/policy-events?page=1&page_size=3")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert data["total"] == 5
    assert len(data["items"]) == 3
    assert data["page"] == 1
    assert data["page_size"] == 3


def test_get_policy_event(client):
    """Test get single policy event."""
    # Create event
    payload = {
        "source_system": "test_system",
        "event_external_id": "EVENT-DETAIL",
        "policy_type": "trade_agreement_change",
        "severity": "high",
        "effective_date": datetime.utcnow().isoformat(),
        "impacted_geographies": ["MX"],
        "relevance_type": "primary",
    }
    create_response = client.post("/api/v1/policy-events:ingest", json=payload)
    event_id = create_response.json()["id"]

    # Get event
    response = client.get(f"/api/v1/policy-events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["event_external_id"] == "EVENT-DETAIL"


def test_get_policy_event_not_found(client):
    """Test get non-existent policy event."""
    response = client.get("/api/v1/policy-events/99999")
    assert response.status_code == 404
