export type MatchType = 'strong_match' | 'partial_match' | 'gap' | 'unknown';
export type MatchAnalysisStatus = 'complete' | 'complete_with_gaps' | 'incomplete';

export interface MatchDetail {
  id: string;
  job_requirement_id: string;
  career_claim_id?: string | null;
  match_type: MatchType;
  score: number;
  explanation: string;
  gap_category?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CandidateJobMatch {
  id: string;
  career_profile_id: string;
  job_id: string;
  algorithm_version: string;
  overall_score: number;
  profile_coverage: number;
  required_score?: number | null;
  preferred_score?: number | null;
  analysis_status: MatchAnalysisStatus;
  critical_gaps: string[];
  details: MatchDetail[];
  created_at: string;
  updated_at: string;
}