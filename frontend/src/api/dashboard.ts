import { apiClient } from './client';
import type { DashboardSummary } from '../types/dashboard';

export const dashboardApi = {
  getSummary: async (): Promise<DashboardSummary> => {
    return apiClient<DashboardSummary>('/dashboard/summary');
  },
};
