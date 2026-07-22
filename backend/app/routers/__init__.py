"""Routers package."""
from .auth import router as auth_router
from .policy_events import router as policy_events_router
from .scenarios import router as scenarios_router
from .agreements import router as agreements_router
from .recommendations import router as recommendations_router
from .alerts import router as alerts_router
from .dashboard import router as dashboard_router
from .compliance import router as compliance_router

__all__ = [
    'auth_router',
    'policy_events_router',
    'scenarios_router',
    'agreements_router',
    'recommendations_router',
    'alerts_router',
    'dashboard_router',
    'compliance_router',
]
