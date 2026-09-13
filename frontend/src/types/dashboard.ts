export interface DashboardSummary {
  candidate_name: string;
  candidate_email: string;
  candidate_headline?: string | null;
  profile_completeness_percentage: number;
  career_claims_count: number;
  evidence_sources_count: number;
  analyzed_jobs_count: number;
  optimized_resumes_count: number;
  target_matches_count: number;
  active_anchor: boolean;
  account_created_at: string;
  last_login_at?: string | null;
}

export interface GettingStartedStep {
  id: string;
  stepNumber: number;
  title: string;
  description: string;
  actionText: string;
  link: string;
  completed: boolean;
  badge: string;
}
