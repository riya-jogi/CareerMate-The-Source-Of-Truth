export type ClaimStatus = 'evidence_backed' | 'candidate_confirmed' | 'self_declared' | 'needs_clarification' | 'unsupported';

export interface CareerClaim {
  id: string;
  claim_type: string;
  claim_text: string;
  subject: string;
  context?: string | null;
  experience_type: string;
  status: ClaimStatus;
  confidence: number;
  skill_name?: string | null;
  candidate_confirmed_at?: string | null;
  created_at: string;
  updated_at: string;
}
