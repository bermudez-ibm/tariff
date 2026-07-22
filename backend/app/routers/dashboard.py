"""Dashboard router."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..services import AnalyticsService
from ..schemas import (
    ExposureSummaryResponse,
    TrendDataResponse,
    ConcentrationViewResponse,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    """Dependency injection for AnalyticsService."""
    return AnalyticsService(db)


@router.get("/exposure", response_model=ExposureSummaryResponse)
async def get_exposure_summary(
    role: str = Query(..., description="User role for visibility scoping"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get exposure summary for dashboard.
    Implements REQ-API-007: Dashboard exposure endpoint.
    Implements FR-DV-01, FR-DV-02: Role-specific dashboard views.
    Implements BR-DV-01, BR-DV-02: Dashboard freshness and performance.
    """
    data = service.get_exposure_summary(role=role, filters={})
    return ExposureSummaryResponse(**data)


@router.get("/trends", response_model=TrendDataResponse)
async def get_trend_data(
    dimension: str = Query(..., description="Trend dimension (country, supplier, route, etc.)"),
    time_window: str = Query("30d", description="Time window for trend data"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get trend data over time for a dimension.
    Implements REQ-API-007: Dashboard trends endpoint.
    Implements FR-DV-03: Trend analysis over time.
    """
    data = service.get_trend_data(dimension=dimension, time_window=time_window, filters={})
    return TrendDataResponse(**data)


@router.get("/concentration", response_model=ConcentrationViewResponse)
async def get_concentration_view(
    dimension: str = Query(..., description="Concentration dimension (country, supplier, route, etc.)"),
    top_n: int = Query(10, ge=1, le=50, description="Number of top items to return"),
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get concentration view showing top exposures.
    Implements REQ-API-007: Dashboard concentration endpoint.
    Implements FR-DV-02, FR-DV-07: Exposure concentration visibility.
    Implements BR-DV-03: Filter refresh within 2 seconds.
    """
    data = service.get_concentration_view(dimension=dimension, top_n=top_n, filters={})
    return ConcentrationViewResponse(**data)
