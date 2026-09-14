export interface Experience {
  id: string;
  company_name: string;
  job_title: string;
  location?: string | null;
  employment_type: string;
  start_date: string;
  end_date?: string | null;
  is_current: boolean;
  description?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CandidateSkill {
  id: string;
  name: string;
  normalized_name: string;
  category?: string | null;
  experience_type: string;
  proficiency?: string | null;
  years_used?: number | null;
  first_used?: string | null;
  last_used?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CareerProfile {
  id: string;
  user_id: string;
  headline?: string | null;
  summary?: string | null;
  phone?: string | null;
  location?: string | null;
  linkedin_url?: string | null;
  github_url?: string | null;
  portfolio_url?: string | null;
  experiences: Experience[];
  projects: unknown[];
  education: unknown[];
  certifications: unknown[];
  skills: CandidateSkill[];
  created_at: string;
  updated_at: string;
}