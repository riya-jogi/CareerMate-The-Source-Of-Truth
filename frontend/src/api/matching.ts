import { apiClient } from './client';
import type { CandidateJobMatch } from '../types/matching';

export const matchingApi = {
  run: (jobId: string) => apiClient<CandidateJobMatch>(`/jobs/${jobId}/match`, { method: 'POST' }),
  get: (jobId: string) => apiClient<CandidateJobMatch>(`/jobs/${jobId}/match`),
};