// TypeScript types for Resume Optimization, Change Review, and Generation (Module 6 & 7)

export type ResumeVersionStatus = 'draft' | 'pending_review' | 'approved' | 'ready' | 'needs_review' | 'failed';
export type ValidationStatus = 'pass' | 'warning' | 'block' | 'needs_clarification';
export type ChangeType = 'add' | 'remove' | 'rewrite' | 'reorder' | 'condense' | 'normalize';
export type ApprovalDecision = 'approved' | 'rejected' | 'edited';

export interface ResumeChange {
  id: string;
  resume_version_id: string;
  change_type: ChangeType;
  section: string;
  original_content: string | null;
  proposed_content: string;
  reason: string;
  risk_level: string;
  validation_status: ValidationStatus;
  primary_claim_id: string | null;
  approval: Approval | null;
  created_at: string;
  updated_at: string;
}

export interface Approval {
  id: string;
  resume_change_id: string;
  decision: ApprovalDecision;
  edited_text: string | null;
  candidate_comment: string | null;
  created_at: string;
  updated_at: string;
}

export interface ResumeVersion {
  id: string;
  resume_id: string;
  job_id: string | null;
  version_number: number;
  content_snapshot: Record<string, unknown>;
  template: string;
  status: ResumeVersionStatus;
  validation_status: ValidationStatus;
  pdf_key: string | null;
  docx_key: string | null;
  changes: ResumeChange[];
  created_at: string;
  updated_at: string;
}

export interface QualityCheck {
  status: 'ready' | 'needs_review';
  checks: Record<string, string>;
  issues: string[];
}
