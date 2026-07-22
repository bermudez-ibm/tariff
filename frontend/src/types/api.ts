// Common types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface ErrorResponse {
  detail: string;
  status_code: number;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface UserResponse {
  id: number;
  email: string;
  name: string;
}

export interface LoginResponse {
  access_token: string;
  user: UserResponse;
}

// Policy Event types
export interface EventDeltaResponse {
  id: number;
  field_name: string;
  prior_value: string | null;
  current_value: string;
}

export interface ImpactAssociationResponse {
  id: number;
  entity_type: string;
  entity_id: number;
  impact_description: string;
}

export interface MaterialityEvaluationResponse {
  id: number;
  materiality_state: string;
  actionable: boolean;
  partial_impact: boolean;
  evaluation_timestamp: string;
}

export interface PolicyEventListResponse {
  id: number;
  source_system: string;
  event_external_id: string;
  policy_type: string;
  severity: string;
  effective_date: string;
  impacted_geographies: string[];
  relevance_type: string;
  materiality_state: string | null;
  actionable: boolean;
  created_at: string;
}

export interface PolicyEventDetailResponse {
  id: number;
  source_system: string;
  event_external_id: string;
  policy_type: string;
  severity: string;
  effective_date: string;
  impacted_geographies: string[];
  relevance_type: string;
  description: string | null;
  deltas: EventDeltaResponse[];
  associations: ImpactAssociationResponse[];
  materiality: MaterialityEvaluationResponse | null;
  created_at: string;
  updated_at: string;
}

export interface IngestPolicyEventRequest {
  source_system: string;
  event_external_id: string;
  policy_type: string;
  severity: string;
  effective_date: string;
  impacted_geographies: string[];
  relevance_type: string;
  description?: string;
  deltas?: Record<string, unknown>[];
}

// Scenario types
export interface CostComponentResponse {
  id: number;
  component_type: string;
  amount: number;
  currency: string;
  description: string | null;
}

export interface ScenarioResultResponse {
  id: number;
  scenario_request_id: number;
  lane_id: number;
  lane_type: string;
  total_landed_cost: number;
  currency: string;
  margin_impact: number | null;
  completeness_status: string;
  incomplete_reasons: string[] | null;
  cost_components: CostComponentResponse[];
  created_at: string;
}

export interface ScenarioAnalysisRequest {
  baseline_lane_id: number;
  alternate_lane_ids: number[];
  requested_by: number;
}

export interface ScenarioAnalysisResponse {
  id: number;
  baseline_result: ScenarioResultResponse;
  alternate_results: ScenarioResultResponse[];
  created_at: string;
}

export interface ScenarioComparisonResponse {
  baseline: ScenarioResultResponse;
  alternate: ScenarioResultResponse;
  cost_delta: number;
  margin_impact_delta: number | null;
  component_deltas: Record<string, unknown>[];
}

// Agreement types
export interface EvidenceGapResponse {
  id: number;
  gap_type: string;
  severity: string;
  blocking_flag: boolean;
  description: string;
}

export interface AgreementEvaluationResponse {
  id: number;
  scenario_result_id: number;
  agreement_code: string;
  qualification_status: string;
  estimated_savings: number;
  currency: string;
  evidence_state: string;
  evidence_gaps: EvidenceGapResponse[];
  created_at: string;
  updated_at: string;
}

// Recommendation types
export interface RecommendationFactorResponse {
  id: number;
  factor_type: string;
  score: number;
  weight: number;
  rationale: string;
}

export interface RecommendationResponse {
  id: number;
  recommendation_type: string;
  priority_score: number;
  compliance_state: string;
  expected_impact: number;
  currency: string;
  rationale: Record<string, unknown>;
  factors: RecommendationFactorResponse[];
  disposition: string | null;
  disposition_reason: string | null;
  created_at: string;
  updated_at: string;
}

export interface GenerateRecommendationsRequest {
  scenario_id: number;
  requested_by: number;
}

export interface DispositionRecommendationRequest {
  disposition: string;
  reason_code: string;
  actor_id: number;
}

// Alert types
export interface AlertTransitionResponse {
  id: number;
  from_status: string;
  to_status: string;
  actor_id: number;
  transition_timestamp: string;
  transition_reason: string | null;
}

export interface AlertResponse {
  id: number;
  category: string;
  severity: string;
  status: string;
  source_ref_type: string;
  source_ref_id: number;
  owner_id: number | null;
  dedupe_key: string;
  alert_title: string;
  alert_description: string;
  details: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  transitions: AlertTransitionResponse[];
}

export interface AcknowledgeAlertRequest {
  actor_id: number;
}

export interface AssignAlertRequest {
  owner_id: number;
  actor_id: number;
}

export interface EscalateAlertRequest {
  escalation_scope: Record<string, unknown>;
  actor_id: number;
}

export interface ResolveAlertRequest {
  outcome_summary: string;
  actor_id: number;
}

// Dashboard types
export interface ExposureMetric {
  dimension: string;
  dimension_value: string;
  exposure_amount: number;
  materiality_level: string;
  trend: string | null;
}

export interface ExposureSummaryResponse {
  total_exposure: number;
  material_exposure: number;
  watchlist_exposure: number;
  by_country: ExposureMetric[];
  by_supplier: ExposureMetric[];
  by_route: ExposureMetric[];
  by_material: ExposureMetric[];
}

export interface TrendDataPoint {
  timestamp: string;
  value: number;
  label: string;
}

export interface TrendDataResponse {
  dimension: string;
  time_window: string;
  data_points: TrendDataPoint[];
}

export interface ConcentrationItem {
  rank: number;
  dimension_value: string;
  exposure_amount: number;
  percentage_of_total: number;
  materiality_level: string;
}

export interface ConcentrationViewResponse {
  dimension: string;
  top_items: ConcentrationItem[];
  total_exposure: number;
}

// Compliance types
export interface RiskFlagResponse {
  id: number;
  risk_category: string;
  severity: string;
  flagged_at: string;
  resolution_status: string;
  description: string;
}

export interface ComplianceReviewResponse {
  id: number;
  subject_type: string;
  subject_id: number;
  review_state: string;
  reviewer_role: string;
  review_notes: string | null;
  reason_code: string | null;
  risk_flags: RiskFlagResponse[];
  created_at: string;
  updated_at: string;
}

export interface CreateComplianceReviewRequest {
  subject_type: string;
  subject_id: number;
  reviewer_role: string;
}

export interface TransitionReviewStateRequest {
  new_state: string;
  reason_code: string;
  actor_id: number;
}
