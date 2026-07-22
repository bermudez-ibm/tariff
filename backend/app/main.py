"""Main FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.config import settings
from app.database import init_db
from app.middleware import CorrelationIdMiddleware
from app.routers import (
    auth_router,
    policy_events_router,
    scenarios_router,
    agreements_router,
    recommendations_router,
    alerts_router,
    dashboard_router,
    compliance_router,
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses (REQ-SEC-001)."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup: Initialize database
    init_db()
    print("Database initialized")
    yield
    # Shutdown: cleanup if needed
    print("Application shutting down")


# Create FastAPI application
app = FastAPI(
    title="Tariff Resilience API",
    description="Decision-support API for managing tariff and trade-policy exposure",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Configure CORS (REQ-API-001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware (REQ-SEC-001)
app.add_middleware(SecurityHeadersMiddleware)

# Add correlation ID middleware (REQ-API-001)
app.add_middleware(CorrelationIdMiddleware)

# Include routers under /api/v1 prefix (REQ-API-001)
API_V1_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(policy_events_router, prefix=API_V1_PREFIX)
app.include_router(scenarios_router, prefix=API_V1_PREFIX)
app.include_router(agreements_router, prefix=API_V1_PREFIX)
app.include_router(recommendations_router, prefix=API_V1_PREFIX)
app.include_router(alerts_router, prefix=API_V1_PREFIX)
app.include_router(dashboard_router, prefix=API_V1_PREFIX)
app.include_router(compliance_router, prefix=API_V1_PREFIX)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Tariff Resilience API",
        "version": "0.1.0",
        "docs": "/docs" if settings.debug else "disabled in production",
    }
