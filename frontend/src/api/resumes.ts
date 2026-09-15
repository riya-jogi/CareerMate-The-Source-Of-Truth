import { apiClient } from './client';
import type { ResumeExtractionResponse, ResumeFile, ResumeProposal } from '../types/resume';

export const resumeApi = {
  list: async (): Promise<ResumeFile[]> => apiClient<ResumeFile[]>('/resumes'),

  upload: async (payload: { filename: string; content_type: string; content: string }): Promise<ResumeFile> =>
    apiClient<ResumeFile>('/resumes/upload', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  uploadFile: async (file: File): Promise<ResumeFile> => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient<ResumeFile>('/resumes/upload/file', {
      method: 'POST',
      body: formData,
    });
  },

  extract: async (resumeId: string): Promise<ResumeExtractionResponse> =>
    apiClient<ResumeExtractionResponse>(`/resumes/${resumeId}/extract`, {
      method: 'POST',
    }),

  reviewProposal: async (
    proposalId: string,
    decision: 'pending' | 'accepted' | 'rejected',
    notes?: string
  ): Promise<ResumeProposal> =>
    apiClient<ResumeProposal>(`/resumes/proposals/${proposalId}/review`, {
      method: 'PATCH',
      body: JSON.stringify({ decision, notes }),
    }),
};
