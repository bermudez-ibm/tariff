"""Tests for scenarios router."""
from app.models import SourcingLane, Country, Supplier


def test_analyze_scenario(client, db_session):
    """Test scenario analysis request."""
    # Create prerequisite data
    country = Country(name="China", iso_code="CN")
    db_session.add(country)
    db_session.flush()

    supplier = Supplier(name="Test Supplier", country_id=country.id)
    db_session.add(supplier)
    db_session.flush()

    lane = SourcingLane(
        supplier_id=supplier.id,
        origin_country_id=country.id,
        destination_country_id=country.id,
        lane_name="Test Lane",
    )
    db_session.add(lane)
    db_session.commit()

    payload = {
        "baseline_lane_id": lane.id,
        "alternate_lane_ids": [],
        "requested_by": 1,
    }

    response = client.post("/api/v1/scenarios:analyze", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "baseline_result" in data
    assert "alternate_results" in data


def test_get_scenario_not_found(client):
    """Test get non-existent scenario."""
    response = client.get("/api/v1/scenarios/99999")
    assert response.status_code == 404
