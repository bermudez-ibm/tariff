"""Dashboard schemas."""
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class ExposureMetric(BaseModel):
    """Exposure metric."""
    dimension: str
    dimension_value: str
    exposure_amount: Decimal
    materiality_level: str
    trend: Optional[str] = None


class ExposureSummaryResponse(BaseModel):
    """Exposure summary response."""
    total_exposure: Decimal
    material_exposure: Decimal
    watchlist_exposure: Decimal
    by_country: List[ExposureMetric]
    by_supplier: List[ExposureMetric]
    by_route: List[ExposureMetric]
    by_material: List[ExposureMetric]


class TrendDataPoint(BaseModel):
    """Trend data point."""
    timestamp: str
    value: Decimal
    label: str


class TrendDataResponse(BaseModel):
    """Trend data response."""
    dimension: str
    time_window: str
    data_points: List[TrendDataPoint]


class ConcentrationItem(BaseModel):
    """Concentration item."""
    rank: int
    dimension_value: str
    exposure_amount: Decimal
    percentage_of_total: Decimal
    materiality_level: str


class ConcentrationViewResponse(BaseModel):
    """Concentration view response."""
    dimension: str
    top_items: List[ConcentrationItem]
    total_exposure: Decimal
