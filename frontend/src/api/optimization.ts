import { apiClient } from './client';
import type { ApprovalDecision, QualityCheck, ResumeVersion } from '../types/optimization';

const BASE = '/jobs';

export const optimizationApi = {
  /**
   * Trigger AI optimization for a specific job — generates a new ResumeVersion
   * with proposed changes derived strictly from candidate's verified claims.
   */
  optimize: (jobId: string, template = 'professional_ats'): Promise<ResumeVersion> =>
    apiClient<ResumeVersion>(`${BASE}/${jobId}/optimize`, {
      method: 'POST',
      body: JSON.stringify({ template }),
    }),

  /**
   * Get the latest optimization version for a job (if exists).
   */
  getOptimization: (jobId: string): Promise<ResumeVersion> =>
    apiClient<ResumeVersion>(`${BASE}/${jobId}/optimization`),

  /**
   * Approve, reject, or edit a specific proposed change.
   */
  decideChange: (
    changeId: string,
    decision: ApprovalDecision,
    editedText?: string,
    candidateComment?: string,
  ): Promise<import('../types/optimization').ResumeChange> =>
    apiClient(`/jobs/changes/${changeId}/decision`, {
      method: 'POST',
      body: JSON.stringify({ decision, edited_text: editedText ?? null, candidate_comment: candidateComment ?? null }),
    }),

  /**
   * Generate the final resume PDF/DOCX after all changes are approved.
   */
  generate: (jobId: string, format: 'pdf' | 'docx' = 'pdf'): Promise<ResumeVersion> =>
    apiClient<ResumeVersion>(`${BASE}/${jobId}/resume/generate`, {
      method: 'POST',
      body: JSON.stringify({ format }),
    }),

  /**
   * Get quality validation results for a version.
   */
  quality: (versionId: string): Promise<QualityCheck> =>
    apiClient<QualityCheck>(`/jobs/resume-versions/${versionId}/quality`),

  /**
   * Build the download URL for a generated resume version.
   */
  downloadUrl: (versionId: string, format: 'pdf' | 'docx' = 'pdf'): string =>
    `/api/v1/jobs/resume-versions/${versionId}/download?format=${format}`,
};
