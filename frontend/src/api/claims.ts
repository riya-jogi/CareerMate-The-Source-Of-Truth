import { apiClient } from './client';
import type { CareerClaim } from '../types/claims';

export const claimsApi = {
  list: () => apiClient<CareerClaim[]>('/claims'),
  update: (id: string, payload: { claim_text?: string; subject?: string; context?: string }) =>
    apiClient<CareerClaim>(`/claims/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  confirm: (id: string) => apiClient<CareerClaim>(`/claims/${id}/confirm`, { method: 'POST' }),
  reject: (id: string) => apiClient<CareerClaim>(`/claims/${id}/reject`, { method: 'POST' }),
};
