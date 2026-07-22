# Tariff Resilience

A decision-support application for managing tariff and trade-policy exposure in global footwear and apparel supply chains.

## Overview

Tariff Resilience provides:
- Real-time tariff and trade-policy monitoring
- Landed-cost scenario analysis and comparison
- Trade-agreement opportunity identification (USMCA, CPTPP, EVFTA)
- Mitigation recommendation generation and review
- Executive exposure dashboards and alerting
- Compliance workflow management with audit trails

## Repository Structure

```
/repos/tariff/
├── backend/          # FastAPI + SQLAlchemy backend
│   ├── app/
│   │   ├── models/       # ORM models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── middleware/   # Auth, CORS, correlation-id, security headers
│   │   └── main.py       # FastAPI app entrypoint
│   ├── tests/        # Backend unit tests
│   └── pyproject.toml
├── frontend/         # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── lib/          # API client, auth, utilities
│   │   ├── components/   # Shared UI components
│   │   ├── pages/        # Application pages
│   │   └── types/        # TypeScript interfaces
│   └── package.json
├── storage/          # SQLite database (local development)
├── Dockerfile        # Multi-stage Docker build
├── docker-compose.yml    # Orchestration (backend + frontend + PostgreSQL)
├── nginx.conf        # Nginx reverse proxy configuration
├── shared_config.json    # Runtime configuration
└── README.md
```

## Technology Stack

**Backend:**
- Python 3.10+
- FastAPI
- SQLAlchemy (sync)
- PostgreSQL (production) / SQLite (development)
- bcrypt for password hashing
- PyJWT for token generation

**Frontend:**
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router DOM

**Infrastructure:**
- Docker & Docker Compose
- PostgreSQL 15
- Nginx (reverse proxy)

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- pip
- npm
- Docker & Docker Compose (for containerized deployment)

## Local Development Setup

The project includes cross-platform startup scripts that handle all prerequisites.

### Quick Start (macOS/Linux)
```bash
chmod +x start.sh stop.sh
./start.sh
```

### Quick Start (Windows)
```cmd
start.bat
```

The startup script will:
1. Check prerequisites (Python 3.10+, Node 18+)
2. Create and activate a Python virtual environment
3. Install backend dependencies
4. Install frontend dependencies
5. Detect available ports (starting from 9000 for backend, 5173 for frontend)
6. Update configuration with detected ports
7. Initialize the database
8. Load seed data with default users
9. Start the backend API server
10. Start the frontend development server
11. Print service URLs and default credentials

### Default Credentials

After running `start.sh`, use these credentials to log in:

- **Email:** `admin@example.com`
- **Password:** `admin123`

Additional test users (one per role):
- Trade Compliance: `compliance@example.com` / `compliance123`
- Strategic Sourcing: `sourcing@example.com` / `sourcing123`
- Finance Analyst: `finance@example.com` / `finance123`
- Supply Chain Planner: `planner@example.com` / `planner123`
- Executive: `exec@example.com` / `exec123`

### Service URLs (Local Development)

After startup:
- **Backend API:** http://localhost:9000
- **API Documentation:** http://localhost:9000/docs
- **Frontend App:** http://localhost:5173

## Manual Setup (Alternative)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install .
python app/seed.py
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev -- --port 5173
```

## Environment Configuration

### Environment Separation

The application supports three environment profiles:

| Environment | Database | Debug Mode | API Docs | Security Headers | CORS |
|-------------|----------|------------|----------|------------------|------|
| **Development** | SQLite | ✅ Enabled | ✅ Enabled | ✅ Enabled | `localhost:*` |
| **Staging** | PostgreSQL | ⚠️ Optional | ⚠️ Optional | ✅ Enabled | Staging domain |
| **Production** | PostgreSQL | ❌ Disabled | ❌ Disabled | ✅ Enabled | Production domain |

### Backend Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

**Development (SQLite):**
```env
DATABASE_URL=sqlite:///./storage/app.db
SECRET_KEY=dev-secret-change-in-production
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
DEBUG=true
API_PORT=9000
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=development
```

**Production (PostgreSQL):**
```env
DATABASE_URL=postgresql://tariff_user:SECURE_PASSWORD@postgres:5432/tariff_resilience
SECRET_KEY=<generate-with-secrets.token_urlsafe-32>
CORS_ORIGINS=https://tariff-resilience.example.com
DEBUG=false
API_PORT=9000
ACCESS_TOKEN_EXPIRE_MINUTES=480
ENVIRONMENT=production
```

### Frontend Environment Variables

Copy `frontend/.env.example` to `frontend/.env` and configure:

**Development:**
```env
VITE_API_URL=http://localhost:9000
```

**Production:**
```env
VITE_API_URL=https://api.tariff-resilience.example.com
```

### Security Considerations

1. **SECRET_KEY Rotation**: Generate a secure random key and rotate every 90 days
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Database Credentials**: Never commit credentials. Use environment variables or secrets management (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).

3. **CORS Configuration**: Whitelist only known frontend domains in production.

4. **Security Headers**: Automatically applied by `SecurityHeadersMiddleware`:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
   - `X-XSS-Protection: 1; mode=block`

## Running Tests

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Docker Deployment

### Quick Start (Docker Compose)

1. **Copy environment template:**
   ```bash
   cp .env.docker.example .env
   ```

2. **Generate secure credentials:**
   ```bash
   # Generate SECRET_KEY
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # Generate POSTGRES_PASSWORD (or use a password manager)
   python -c "import secrets; print(secrets.token_urlsafe(24))"
   ```

3. **Update .env file** with generated credentials

4. **Build and start services:**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

5. **Initialize database and seed data:**
   ```bash
   docker-compose exec backend python app/seed.py
   ```

6. **Access the application:**
   - Frontend: http://127.0.0.1:8080 (or http://localhost:8080)
   - Backend API: http://127.0.0.1:9000
   - API Docs: http://127.0.0.1:9000/docs (if DEBUG=true)

### Docker Service URLs

When using Docker Compose:
- **Frontend:** http://127.0.0.1:8080
- **Backend API:** http://127.0.0.1:9000
- **PostgreSQL:** localhost:5432

**Note:** On macOS, use `127.0.0.1` instead of `localhost` for IPv4 resolution.

### Container Networking

- **Backend-to-Database:** Uses service name `postgres:5432`
- **Frontend-to-Backend:** Nginx proxies `/api/*` to `backend:9000`
- **External Access:** Host ports 8080 (frontend), 9000 (backend), 5432 (postgres)

### Docker Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart backend
docker-compose restart frontend

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v

# Check service health
docker-compose ps
```

## Production Deployment

### Cloud Platform Deployment

**AWS Deployment:**
1. Use AWS ECS/Fargate or EKS for container orchestration
2. Use RDS PostgreSQL for managed database
3. Use ALB for load balancing with TLS/SSL termination
4. Use CloudFront CDN for frontend static assets
5. Store secrets in AWS Secrets Manager
6. Enable CloudWatch for monitoring and logging

**Azure Deployment:**
1. Use Azure Container Instances or AKS
2. Use Azure Database for PostgreSQL
3. Use Application Gateway for load balancing
4. Use Azure CDN for frontend
5. Store secrets in Azure Key Vault
6. Enable Azure Monitor and Application Insights

**GCP Deployment:**
1. Use Cloud Run or GKE
2. Use Cloud SQL for PostgreSQL
3. Use Cloud Load Balancing
4. Use Cloud CDN for frontend
5. Store secrets in Secret Manager
6. Enable Cloud Monitoring and Cloud Logging

### Production Checklist

- [ ] Set `DEBUG=false` to disable API documentation
- [ ] Generate and rotate `SECRET_KEY` regularly (every 90 days)
- [ ] Use PostgreSQL with connection pooling (min 5, max 20 connections)
- [ ] Configure CORS to allow only production frontend domain
- [ ] Enable HTTPS/TLS at load balancer or reverse proxy
- [ ] Implement rate limiting on auth endpoints (10 req/min recommended)
- [ ] Set up monitoring and alerting (CPU, memory, response times, error rates)
- [ ] Configure log aggregation (CloudWatch, Azure Monitor, Stackdriver)
- [ ] Enable automated backups (daily recommended)
- [ ] Document incident response and escalation procedures
- [ ] Set up health check monitoring with uptime alerts
- [ ] Configure auto-scaling based on CPU/memory thresholds
- [ ] Implement disaster recovery plan with defined RTO/RPO

### Backup and Restore

#### PostgreSQL Backup (Docker)

**Create Backup:**
```bash
# Backup to file
docker-compose exec postgres pg_dump -U tariff_user tariff_resilience > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup with compression
docker-compose exec postgres pg_dump -U tariff_user tariff_resilience | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

**Restore Backup:**
```bash
# Restore from file
docker-compose exec -T postgres psql -U tariff_user tariff_resilience < backup_20260722_120000.sql

# Restore from compressed file
gunzip -c backup_20260722_120000.sql.gz | docker-compose exec -T postgres psql -U tariff_user tariff_resilience
```

#### PostgreSQL Backup (Production)

**Automated Backup Strategy:**
- **Daily backups**: Full database backup at 2 AM UTC
- **Retention**: 30 days for daily backups, 12 months for monthly snapshots
- **Backup location**: Off-site encrypted storage (S3, Azure Blob, Cloud Storage)
- **Restore testing**: Monthly restore drills to verify backup integrity
- **RPO**: 15 minutes (continuous WAL archiving)
- **RTO**: 4 hours (documented in runbook)

**Cloud-Managed Backup:**
- **AWS RDS:** Enable automated backups with 30-day retention
- **Azure Database:** Configure automated backups with geo-redundancy
- **GCP Cloud SQL:** Enable automated backups with point-in-time recovery

#### Audit Data Retention

Per compliance requirements (REQ-NFR-002, FR-CR-07):
- **Audit trail retention:** 7 years minimum
- **Immutable records:** Append-only audit entries with tamper-evident hash chain
- **Archival strategy:** Move audit records older than 1 year to cold storage
- **Compliance verification:** Quarterly audit of retention policy adherence

### Monitoring and Observability

**Key Metrics to Monitor:**
- API response time (p50, p95, p99)
- Error rate (4xx, 5xx responses)
- Database connection pool utilization
- CPU and memory usage per service
- Request throughput (requests per second)
- Active user sessions
- Failed login attempts (security monitoring)

**Alert Thresholds:**
- API p95 latency > 2 seconds
- Error rate > 1%
- CPU usage > 80% for 5 minutes
- Memory usage > 85%
- Database connection pool > 90% utilized
- Failed logins > 10 per minute from single IP

**Recommended Tools:**
- Application: Prometheus + Grafana, Datadog, New Relic
- Logs: ELK Stack, CloudWatch Logs, Azure Monitor
- APM: Application Insights, Datadog APM, New Relic

## API Documentation

Interactive API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when `DEBUG=true`.

**Note:** API documentation is automatically disabled in production when `DEBUG=false` for security.

## Troubleshooting

### Port Conflicts
If ports 9000 or 5173 are already in use, the start script will automatically detect and use the next available port.

### Python Version
Ensure Python 3.10 or higher is installed:
```bash
python --version
```

### Node Version
Ensure Node.js 18 or higher is installed:
```bash
node --version
```

### Database Issues

**Development (SQLite):**
```bash
# Reset database
rm storage/app.db
./start.sh
```

**Production (PostgreSQL):**
```bash
# Check database connection
docker-compose exec backend python -c "from app.database import engine; print(engine.connect())"

# View database logs
docker-compose logs postgres
```

### Docker Issues

**Container fails to start:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild without cache
docker-compose build --no-cache
```

**Permission errors:**
```bash
# Ensure storage directory is writable
chmod 755 storage
```

**IPv4 vs IPv6 on macOS:**
- Use `127.0.0.1` instead of `localhost` to access services
- Frontend: http://127.0.0.1:8080
- Backend: http://127.0.0.1:9000

## Security

### Implemented Security Measures

1. **Authentication**: JWT bearer tokens with configurable expiration
2. **Password Hashing**: bcrypt with secure salt rounds
3. **Security Headers**: X-Content-Type-Options, X-Frame-Options, HSTS, XSS-Protection
4. **CORS**: Configurable origin whitelist
5. **Input Validation**: Pydantic schema validation on all endpoints
6. **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
7. **Non-Root Containers**: Docker containers run as non-root user (UID 1000)
8. **Secrets Management**: Environment variable-based configuration
9. **Audit Trail**: Immutable append-only audit logs with hash chain

### Security Best Practices

- Never commit `.env` files or secrets to version control
- Rotate `SECRET_KEY` and database passwords regularly
- Use HTTPS/TLS for all production traffic
- Implement rate limiting on authentication endpoints
- Monitor failed login attempts for brute force attacks
- Keep dependencies updated (run `pip audit` and `npm audit` regularly)
- Perform regular security audits and penetration testing
- Follow principle of least privilege for database users and IAM roles

## License

Internal use only.
