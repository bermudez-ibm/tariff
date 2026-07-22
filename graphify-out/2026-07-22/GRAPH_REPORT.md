# Graph Report - tariff  (2026-07-22)

## Corpus Check
- 90 files · ~21,357 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 766 nodes · 1174 edges · 55 communities (49 shown, 6 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 95 edges (avg confidence: 0.69)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ff82c47c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- README.md
- compilerOptions
- main.py
- devDependencies
- package.json
- compilerOptions
- config.py
- dependencies
- Troubleshooting
- Local Development Setup
- App.tsx
- __init__.py
- tariff-resilience-backend
- __init__.py
- alerts.py
- MonitoringService
- recommendations.py
- TradeAgreementService
- AuditEntry
- Alert
- __init__.py
- test_alerts.py
- test_policy_events.py
- test_compliance.py
- Recommendation
- test_dashboard.py
- test_recommendations.py
- scenario.py
- test_scenarios.py
- agreements.py
- recommendation.py
- scenario.py
- scenario.py
- FastAPI
- CorrelationIdMiddleware
- agreements.py
- dependencies.py
- auth-context.tsx
- config.py
- seed_database
- compliance.py
- auth.py
- Loading.tsx
- AgreementEvaluationResponse
- common.py
- verify_auth.py
- .create_scenario_request
- auth.py
- Recommendation
- test_scenarios.py

## God Nodes (most connected - your core abstractions)
1. `BaseModel` - 80 edges
2. `seed_database()` - 21 edges
3. `Alert` - 19 edges
4. `AlertService` - 18 edges
5. `compilerOptions` - 17 edges
6. `User` - 16 edges
7. `Tariff Resilience` - 15 edges
8. `ComplianceWorkflowService` - 14 edges
9. `MonitoringService` - 14 edges
10. `ComplianceReview` - 13 edges

## Surprising Connections (you probably didn't know these)
- `create_test_app()` --indirect_call--> `CorrelationIdMiddleware`  [INFERRED]
  backend/tests/conftest.py → backend/app/middleware/correlation_id.py
- `AgreementEvaluation` --uses--> `BaseModel`  [INFERRED]
  backend/app/models/agreement.py → backend/app/models/base.py
- `seed_database()` --indirect_call--> `AgreementEvaluation`  [INFERRED]
  backend/app/seed.py → backend/app/models/agreement.py
- `EvidenceGap` --uses--> `BaseModel`  [INFERRED]
  backend/app/models/agreement.py → backend/app/models/base.py
- `seed_database()` --calls--> `EvidenceGap`  [INFERRED]
  backend/app/seed.py → backend/app/models/agreement.py

## Import Cycles
- None detected.

## Communities (55 total, 6 thin omitted)

### Community 0 - "README.md"
Cohesion: 0.04
Nodes (45): API Documentation, Audit Data Retention, Backend Environment Variables, Backend Setup, Backend Tests, Backup and Restore, Cloud Platform Deployment, Container Networking (+37 more)

### Community 1 - "compilerOptions"
Cohesion: 0.10
Nodes (20): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+12 more)

### Community 2 - "main.py"
Cohesion: 0.05
Nodes (46): Application configuration using pydantic-settings., Parse CORS origins from comma-separated string., Application settings loaded from environment variables., Settings, get_db(), Session, Database connection and session management., Dependency to get database session. (+38 more)

### Community 3 - "devDependencies"
Cohesion: 0.07
Nodes (28): dependencies, clsx, react, react-dom, react-router-dom, tailwind-merge, devDependencies, autoprefixer (+20 more)

### Community 4 - "package.json"
Cohesion: 0.13
Nodes (20): Country, DistributionCenter, Port, Product, Reference data models: suppliers, products, countries, lanes, routes, ports, DCs, Supplier reference data., Product reference data., Shipping route reference data. (+12 more)

### Community 5 - "compilerOptions"
Cohesion: 0.18
Nodes (10): compilerOptions, allowSyntheticDefaultImports, lib, module, moduleResolution, noEmit, skipLibCheck, strict (+2 more)

### Community 6 - "config.py"
Cohesion: 0.10
Nodes (20): EventDelta, ImpactAssociation, MaterialityEvaluation, PolicyEvent, Policy event models: events, deltas, impact associations, materiality evaluation, Delta changes detected in policy events., Impact associations linking events to affected entities., Materiality classification for policy events. (+12 more)

### Community 7 - "dependencies"
Cohesion: 0.18
Nodes (11): Trade agreement evaluation models., Audit entry model for immutable history., Base declarative model and common columns., Mixin for created_at and updated_at timestamps., TimestampMixin, Compliance review and risk flag models., Risk flag for compliance concerns., RiskFlag (+3 more)

### Community 8 - "Troubleshooting"
Cohesion: 0.13
Nodes (15): analyze_scenario(), get_financial_service(), get_scenario(), get_scenario_comparison(), Session, Dependency injection for FinancialAnalysisService., Request scenario analysis for baseline and alternate lanes.     Implements REQ-A, Get scenario detail with cost components.     Implements REQ-API-003: Scenario d (+7 more)

### Community 9 - "Local Development Setup"
Cohesion: 0.09
Nodes (23): ComplianceReview, Compliance review workflow., create_compliance_review(), get_compliance_review(), get_compliance_service(), list_compliance_reviews(), Session, Get compliance review detail with risk flags.     Implements REQ-API-008: Compli (+15 more)

### Community 10 - "App.tsx"
Cohesion: 0.20
Nodes (9): App(), LoginPage(), RequireAuth(), RequireAuthProps, Header(), Layout(), LayoutProps, AuthProvider() (+1 more)

### Community 14 - "__init__.py"
Cohesion: 0.12
Nodes (15): get_analytics_service(), get_concentration_view(), get_exposure_summary(), get_trend_data(), Session, Dependency injection for AnalyticsService., Get exposure summary for dashboard.     Implements REQ-API-007: Dashboard exposu, Get trend data over time for a dimension.     Implements REQ-API-007: Dashboard (+7 more)

### Community 15 - "alerts.py"
Cohesion: 0.05
Nodes (48): AcknowledgeAlertRequest, Alert, AssignAlertRequest, Alert, AlertTransition, Alert and notification models., Alert state transition history., Material impact alert. (+40 more)

### Community 16 - "MonitoringService"
Cohesion: 0.14
Nodes (13): EventDeltaResponse, ImpactAssociationResponse, IngestPolicyEventRequest, MaterialityEvaluationResponse, PolicyEventDetailResponse, PolicyEventListResponse, Policy event schemas., Impact association response. (+5 more)

### Community 17 - "recommendations.py"
Cohesion: 0.07
Nodes (24): create_test_user(), hash_password(), Unit tests for authentication endpoints., Test login with non-existent email., Test login with incorrect password., Test login with inactive user account., Test that login accepts field names from shared_config.json., Test login with missing email field. (+16 more)

### Community 18 - "TradeAgreementService"
Cohesion: 0.18
Nodes (10): AgreementEvaluation, EvidenceGap, Evidence gaps preventing agreement qualification., Trade agreement qualification and savings evaluation., Session, Trade agreement service for evaluation and qualification., Service for trade agreement evaluation and savings calculation., Evaluate all applicable trade agreements for a scenario result.         Implemen (+2 more)

### Community 19 - "AuditEntry"
Cohesion: 0.16
Nodes (10): AuditEntry, Immutable audit entry with hash chain., AuditService, Session, Audit service for immutable audit trail management., Service for append-only audit trail with tamper-evident hash chain., Append audit entry with hash chain for tamper evidence.         Implements FR-CR, Retrieve audit history for an aggregate.         Returns entries in reverse chro (+2 more)

### Community 20 - "Alert"
Cohesion: 0.06
Nodes (35): AcknowledgeAlertRequest, AgreementEvaluationResponse, AlertResponse, AlertTransitionResponse, AssignAlertRequest, ComplianceReviewResponse, ConcentrationItem, ConcentrationViewResponse (+27 more)

### Community 21 - "__init__.py"
Cohesion: 0.10
Nodes (17): Badge(), BadgeProps, colorClasses, sizeClasses, Button(), ButtonProps, sizeClasses, variantClasses (+9 more)

### Community 22 - "test_alerts.py"
Cohesion: 0.28
Nodes (4): request(), Alert, ExposureData, PolicyEvent

### Community 23 - "test_policy_events.py"
Cohesion: 0.17
Nodes (11): Tests for policy events router., Test get non-existent policy event., Test policy event ingestion is idempotent., Test policy events list with pagination., Test policy event ingestion., Test get single policy event., test_get_policy_event(), test_get_policy_event_not_found() (+3 more)

### Community 24 - "test_compliance.py"
Cohesion: 0.20
Nodes (9): Tests for compliance router., Test compliance review state transition., Test compliance review with invalid state., Test compliance review creation., Test list compliance reviews., test_create_compliance_review(), test_list_compliance_reviews(), test_transition_review_invalid_state() (+1 more)

### Community 25 - "Recommendation"
Cohesion: 0.20
Nodes (13): BaseModel, Abstract base model with id, created_at, updated_at., AcknowledgeAlertRequest, AlertResponse, AlertTransitionResponse, AssignAlertRequest, EscalateAlertRequest, Acknowledge alert request. (+5 more)

### Community 26 - "test_dashboard.py"
Cohesion: 0.25
Nodes (7): Tests for dashboard router., Test trend data endpoint., Test concentration view endpoint., Test exposure summary endpoint., test_get_concentration_view(), test_get_exposure_summary(), test_get_trend_data()

### Community 27 - "test_recommendations.py"
Cohesion: 0.25
Nodes (7): Tests for recommendations router., Test disposition of blocked recommendation (should fail)., Test recommendation generation., Test disposition of approved recommendation (should succeed)., test_disposition_recommendation_approved(), test_disposition_recommendation_blocked(), test_generate_recommendations()

### Community 28 - "scenario.py"
Cohesion: 0.23
Nodes (9): CostComponent, Scenario analysis models: requests, results, cost components., Scenario calculation result for one lane., Individual cost component within a scenario result., Scenario analysis request., ScenarioRequest, ScenarioResult, Financial analysis service for landed-cost calculation and scenario comparison. (+1 more)

### Community 29 - "test_scenarios.py"
Cohesion: 0.18
Nodes (10): disposition_recommendation(), generate_recommendations(), get_recommendation_service(), Session, Recommendations router., Dependency injection for RecommendationService., Generate mitigation recommendations for a scenario.     Implements REQ-API-005:, Apply disposition to a recommendation.     Implements REQ-API-005: Recommendatio (+2 more)

### Community 31 - "agreements.py"
Cohesion: 0.33
Nodes (4): CorrelationIdMiddleware, Request, Correlation ID middleware for request tracing., Middleware to extract or generate X-Correlation-Id for request tracing.     Impl

### Community 32 - "recommendation.py"
Cohesion: 0.17
Nodes (11): get_monitoring_service(), get_policy_event(), ingest_policy_event(), list_policy_events(), Session, Policy events router., Dependency injection for MonitoringService., Ingest policy event from external source (idempotent).     Implements REQ-API-00 (+3 more)

### Community 33 - "scenario.py"
Cohesion: 0.20
Nodes (9): DispositionRecommendationRequest, GenerateRecommendationsRequest, Recommendation schemas., Recommendation response., Generate recommendations request., Disposition recommendation request., Recommendation factor response., RecommendationFactorResponse (+1 more)

### Community 34 - "scenario.py"
Cohesion: 0.17
Nodes (11): CostComponentResponse, Scenario analysis schemas., Scenario result response., Request scenario analysis., Scenario analysis response., Scenario comparison response., Cost component response., ScenarioAnalysisRequest (+3 more)

### Community 35 - "FastAPI"
Cohesion: 0.22
Nodes (9): client(), create_test_app(), db_session(), Test fixtures and configuration., Create a test FastAPI app without lifespan., Create a fresh database session for each test., Create a test client with overridden database dependency., override_get_db() (+1 more)

### Community 36 - "CorrelationIdMiddleware"
Cohesion: 0.33
Nodes (4): check_prerequisites(), CORS_ORIGINS, DATABASE_URL, start.sh script

### Community 38 - "dependencies.py"
Cohesion: 0.20
Nodes (8): get_agreement_evaluation(), get_agreement_service(), get_scenario_agreement_evaluations(), Session, Trade agreements router., Dependency injection for TradeAgreementService., Get agreement evaluations for a scenario result.     Implements REQ-API-004: Tra, Get single agreement evaluation with evidence gaps.     Implements REQ-API-004:

### Community 39 - "auth-context.tsx"
Cohesion: 0.40
Nodes (5): AuthContext, AuthContextType, LoginRequest, LoginResponse, UserResponse

### Community 40 - "config.py"
Cohesion: 0.33
Nodes (8): ConcentrationItem, ConcentrationViewResponse, ExposureMetric, ExposureSummaryResponse, Exposure summary response., Concentration view response., TrendDataPoint, TrendDataResponse

### Community 41 - "seed_database"
Cohesion: 0.40
Nodes (4): Request, Add security headers to all responses (REQ-SEC-001)., SecurityHeadersMiddleware, BaseHTTPMiddleware

### Community 42 - "compliance.py"
Cohesion: 0.25
Nodes (7): ComplianceReviewResponse, CreateComplianceReviewRequest, Compliance review response., Create compliance review request., Transition review state request., RiskFlagResponse, TransitionReviewStateRequest

### Community 43 - "auth.py"
Cohesion: 0.29
Nodes (6): LoginRequest, LoginResponse, Authentication schemas., Login response payload., Login request payload., UserResponse

### Community 48 - "AgreementEvaluationResponse"
Cohesion: 0.33
Nodes (5): AgreementEvaluationResponse, EvidenceGapResponse, Trade agreement schemas., Agreement evaluation response., Evidence gap response.

### Community 49 - "common.py"
Cohesion: 0.33
Nodes (5): ErrorResponse, PaginationParams, Common schemas shared across all API endpoints., Standard error response., Standard pagination query parameters.

### Community 51 - ".create_scenario_request"
Cohesion: 0.22
Nodes (8): init_db(), Initialize database tables., health_check(), lifespan(), Main FastAPI application entrypoint., Application lifespan manager for startup and shutdown events., Health check endpoint., FastAPI

### Community 53 - "Recommendation"
Cohesion: 0.14
Nodes (13): Mitigation recommendation models., Factor contributing to recommendation score and rationale., Mitigation recommendation., Recommendation, RecommendationFactor, get_recommendation(), Get recommendation detail with rationale and factors.     Implements REQ-API-005, Session (+5 more)

### Community 57 - "test_scenarios.py"
Cohesion: 0.50
Nodes (3): Tests for scenarios router., Test get non-existent scenario., test_get_scenario_not_found()

## Knowledge Gaps
- **145 isolated node(s):** `tariff-resilience-backend`, `name`, `private`, `version`, `type` (+140 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `Recommendation` to `scenario.py`, `main.py`, `scenario.py`, `package.json`, `config.py`, `dependencies`, `config.py`, `Local Development Setup`, `compliance.py`, `auth.py`, `alerts.py`, `AgreementEvaluationResponse`, `common.py`, `TradeAgreementService`, `AuditEntry`, `MonitoringService`, `Recommendation`, `scenario.py`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `Alert` connect `alerts.py` to `Recommendation`, `main.py`, `package.json`, `dependencies`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `User` connect `main.py` to `Recommendation`, `package.json`, `recommendations.py`, `dependencies`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `BaseModel` (e.g. with `AgreementEvaluation` and `EvidenceGap`) actually correct?**
  _`BaseModel` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `seed_database()` (e.g. with `AgreementEvaluation` and `EvidenceGap`) actually correct?**
  _`seed_database()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Alert` (e.g. with `BaseModel` and `get_alert()`) actually correct?**
  _`Alert` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Tariff Resilience Backend Application.`, `Application configuration using pydantic-settings.`, `Application settings loaded from environment variables.` to the rest of the system?**
  _381 weakly-connected nodes found - possible documentation gaps or missing edges._