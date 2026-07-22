"""Tests for dashboard router."""


def test_get_exposure_summary(client):
    """Test exposure summary endpoint."""
    response = client.get("/api/v1/dashboard/exposure?role=executive")
    assert response.status_code == 200
    data = response.json()
    assert "total_exposure" in data
    assert "material_exposure" in data
    assert "watchlist_exposure" in data
    assert "by_country" in data
    assert "by_supplier" in data
    assert "by_route" in data
    assert "by_material" in data


def test_get_trend_data(client):
    """Test trend data endpoint."""
    response = client.get("/api/v1/dashboard/trends?dimension=country&time_window=30d")
    assert response.status_code == 200
    data = response.json()
    assert "dimension" in data
    assert "time_window" in data
    assert "data_points" in data
    assert data["dimension"] == "country"


def test_get_concentration_view(client):
    """Test concentration view endpoint."""
    response = client.get("/api/v1/dashboard/concentration?dimension=country&top_n=5")
    assert response.status_code == 200
    data = response.json()
    assert "dimension" in data
    assert "total_exposure" in data
    assert "top_items" in data
    assert len(data["top_items"]) <= 5
