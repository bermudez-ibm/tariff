"""Common schemas shared across all API endpoints."""
from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Standard pagination query parameters."""
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper."""
    items: List[T]
    total: int = Field(..., description="Total number of items across all pages")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")

    model_config = {'from_attributes': True}


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    status_code: int = Field(..., alias='statusCode')
