"""Correlation ID middleware for request tracing."""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract or generate X-Correlation-Id for request tracing.
    Implements API design requirement for correlation ID propagation.
    """

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get('X-Correlation-Id', str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        response = await call_next(request)
        response.headers['X-Correlation-Id'] = correlation_id
        return response
