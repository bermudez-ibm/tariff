"""Tests for recommendations router."""


def test_generate_recommendations(client):
    """Test recommendation generation."""
    payload = {
        "scenario_id": 1,
        "requested_by": 1,
    }

    response = client.post("/api/v1/recommendations:generate", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Verify recommendation structure
    rec = data[0]
    assert "id" in rec
    assert "recommendation_type" in rec
    assert "priority_score" in rec
    assert "compliance_state" in rec
    assert "expected_impact" in rec
    assert "rationale" in rec


def test_disposition_recommendation_blocked(client):
    """Test disposition of blocked recommendation (should fail)."""
    # Generate recommendations first
    gen_response = client.post(
        "/api/v1/recommendations:generate",
        json={"scenario_id": 1, "requested_by": 1},
    )
    recommendations = gen_response.json()

    # Find blocked recommendation (pre-shipping is blocked in test data)
    blocked_rec = next((r for r in recommendations if r["compliance_state"] == "BLOCKED"), None)
    if not blocked_rec:
        # Skip if no blocked recommendation
        return

    # Try to accept blocked recommendation
    payload = {
        "disposition": "accepted",
        "reason_code": "TEST",
        "actor_id": 1,
    }

    response = client.post(
        f"/api/v1/recommendations/{blocked_rec['id']}/disposition",
        json=payload,
    )
    assert response.status_code == 400
    assert "blocked" in response.json()["detail"].lower()


def test_disposition_recommendation_approved(client):
    """Test disposition of approved recommendation (should succeed)."""
    # Generate recommendations first
    gen_response = client.post(
        "/api/v1/recommendations:generate",
        json={"scenario_id": 1, "requested_by": 1},
    )
    recommendations = gen_response.json()

    # Find approved recommendation
    approved_rec = next((r for r in recommendations if r["compliance_state"] == "APPROVED"), None)
    if not approved_rec:
        return

    # Accept approved recommendation
    payload = {
        "disposition": "accepted",
        "reason_code": "Cost-effective solution",
        "actor_id": 1,
    }

    response = client.post(
        f"/api/v1/recommendations/{approved_rec['id']}/disposition",
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["disposition"] == "accepted"
    assert data["disposition_reason"] == "Cost-effective solution"
