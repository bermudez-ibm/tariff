"""Tests for compliance router."""


def test_create_compliance_review(client):
    """Test compliance review creation."""
    payload = {
        "subject_type": "recommendation",
        "subject_id": 1,
        "reviewer_role": "trade_compliance_manager",
    }

    response = client.post("/api/v1/compliance-reviews", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["subject_type"] == "recommendation"
    assert data["subject_id"] == 1
    assert data["review_state"] == "UNDER_REVIEW"


def test_transition_review_state(client):
    """Test compliance review state transition."""
    # Create review
    create_payload = {
        "subject_type": "agreement",
        "subject_id": 1,
        "reviewer_role": "trade_compliance_manager",
    }
    create_response = client.post("/api/v1/compliance-reviews", json=create_payload)
    review_id = create_response.json()["id"]

    # Transition to APPROVED
    transition_payload = {
        "new_state": "APPROVED",
        "reason_code": "All requirements met",
        "actor_id": 1,
    }
    response = client.patch(f"/api/v1/compliance-reviews/{review_id}", json=transition_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["review_state"] == "APPROVED"
    assert data["reason_code"] == "All requirements met"


def test_transition_review_invalid_state(client):
    """Test compliance review with invalid state."""
    # Create review
    create_payload = {
        "subject_type": "scenario",
        "subject_id": 1,
        "reviewer_role": "trade_compliance_manager",
    }
    create_response = client.post("/api/v1/compliance-reviews", json=create_payload)
    review_id = create_response.json()["id"]

    # Try invalid state
    transition_payload = {
        "new_state": "INVALID_STATE",
        "reason_code": "Test",
        "actor_id": 1,
    }
    response = client.patch(f"/api/v1/compliance-reviews/{review_id}", json=transition_payload)
    assert response.status_code == 400


def test_list_compliance_reviews(client):
    """Test list compliance reviews."""
    # Create multiple reviews
    for i in range(3):
        payload = {
            "subject_type": "recommendation",
            "subject_id": i + 1,
            "reviewer_role": "trade_compliance_manager",
        }
        client.post("/api/v1/compliance-reviews", json=payload)

    # List all
    response = client.get("/api/v1/compliance-reviews")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3

    # Filter by subject type
    response = client.get("/api/v1/compliance-reviews?subject_type=recommendation")
    assert response.status_code == 200
    assert response.json()["total"] == 3
