"""Test fixtures and configuration."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from app.models import Base
from app.dependencies import get_db
from app.middleware import CorrelationIdMiddleware
from app.routers import (
    policy_events_router,
    scenarios_router,
    agreements_router,
    recommendations_router,
    alerts_router,
    dashboard_router,
    compliance_router,
)


# Use in-memory SQLite for testing with StaticPool to avoid threading issues
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_app():
    """Create a test FastAPI app without lifespan."""
    test_app = FastAPI(title="Test API")

    # Add middleware
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    test_app.add_middleware(CorrelationIdMiddleware)

    # Include routers
    API_V1_PREFIX = "/api/v1"
    test_app.include_router(policy_events_router, prefix=API_V1_PREFIX)
    test_app.include_router(scenarios_router, prefix=API_V1_PREFIX)
    test_app.include_router(agreements_router, prefix=API_V1_PREFIX)
    test_app.include_router(recommendations_router, prefix=API_V1_PREFIX)
    test_app.include_router(alerts_router, prefix=API_V1_PREFIX)
    test_app.include_router(dashboard_router, prefix=API_V1_PREFIX)
    test_app.include_router(compliance_router, prefix=API_V1_PREFIX)

    return test_app


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency."""
    test_app = create_test_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    test_app.dependency_overrides[get_db] = override_get_db

    with TestClient(test_app) as test_client:
        yield test_client
