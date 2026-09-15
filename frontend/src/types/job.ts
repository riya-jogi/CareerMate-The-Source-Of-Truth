export type JobAnalysisStatus = 'pending' | 'completed' | 'failed';
export type RequirementImportance = 'required' | 'preferred' | 'contextual';

export interface Job {
  id: string;
  title?: string | null;
  company_name?: string | null;
  description: string;
  location?: string | null;
  source: string;
  analysis_status: JobAnalysisStatus;
  analysis_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface JobRequirement {
  id: string;
  job_id: string;
  requirement_text: string;
  requirement_type: string;
  importance: RequirementImportance;
  skill_name?: string | null;
  minimum_years?: number | null;
  experience_type?: string | null;
  created_at: string;
  updated_at: string;
}

export interface JobAnalysisResponse {
  job: Job;
  requirements: JobRequirement[];
}
