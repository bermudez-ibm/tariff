# Multi-stage Dockerfile for Tariff Resilience application
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install frontend dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# Stage 2: Backend runtime
FROM python:3.11-slim AS backend

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Create app user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/storage && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy backend files
COPY --chown=appuser:appuser backend/pyproject.toml backend/setup.py* ./
COPY --chown=appuser:appuser backend/app ./app/

# Install backend dependencies
RUN pip install --no-cache-dir .

# Copy frontend build from previous stage
COPY --from=frontend-build --chown=appuser:appuser /app/frontend/dist ./frontend/dist

# Copy shared configuration
COPY --chown=appuser:appuser shared_config.json ./

# Switch to non-root user
USER appuser

# Expose backend port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:9000/health || exit 1

# Start backend server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
