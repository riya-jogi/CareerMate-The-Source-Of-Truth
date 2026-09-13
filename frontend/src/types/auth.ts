export interface CareerProfileSummary {
  id: string;
  headline?: string | null;
  summary?: string | null;
  location?: string | null;
  created_at?: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  last_login_at?: string | null;
  created_at: string;
  career_profile?: CareerProfileSummary | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  headline?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface TokenRefreshResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface ApiErrorDetail {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export interface ApiResponseError {
  error: ApiErrorDetail;
}
