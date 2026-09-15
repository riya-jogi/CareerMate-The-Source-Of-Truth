import { apiClient } from './client';
import type { Job, JobAnalysisResponse, JobRequirement } from '../types/job';

export const jobsApi = {
  list: () => apiClient<Job[]>('/jobs'),
  create: (payload: { title?: string; company_name?: string; location?: string; description: string }) =>
    apiClient<Job>('/jobs', { method: 'POST', body: JSON.stringify(payload) }),
  analyze: (id: string) => apiClient<JobAnalysisResponse>(`/jobs/${id}/analyze`, { method: 'POST' }),
  requirements: (id: string) => apiClient<JobRequirement[]>(`/jobs/${id}/requirements`),
};
