export type ResumeStatus = 'uploaded' | 'extracted';

export type ProposalType = 'skill' | 'experience' | 'education' | 'certification' | 'project' | 'summary';
export type ProposalDecision = 'pending' | 'accepted' | 'rejected';

export interface ResumeFile {
  id: string;
  career_profile_id: string;
  filename: string;
  content_type: string;
  file_size: number;
  status: ResumeStatus;
  extracted_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ResumeProposal {
  id: string;
  resume_file_id: string;
  proposal_type: ProposalType;
  field_name: string;
  proposed_value: string;
  source_excerpt?: string | null;
  confidence: number;
  decision: ProposalDecision;
  review_notes?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ResumeExtractionResponse {
  resume_id: string;
  proposals: ResumeProposal[];
}
