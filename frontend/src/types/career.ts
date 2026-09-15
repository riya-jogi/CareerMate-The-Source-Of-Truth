export interface Project {
  id: string;
  name: string;
  description: string;
  role?: string | null;
  project_type: string;
  start_date?: string | null;
  end_date?: string | null;
  repository_url?: string | null;
  project_url?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Education {
  id: string;
  institution: string;
  degree: string;
  field_of_study?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  grade?: string | null;
  description?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Certification {
  id: string;
  name: string;
  issuing_organization: string;
  issue_date?: string | null;
  expiry_date?: string | null;
  credential_id?: string | null;
  credential_url?: string | null;
  created_at: string;
  updated_at: string;
}
