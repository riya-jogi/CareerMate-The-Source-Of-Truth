import { apiClient } from './client';
import type { CareerProfile, Experience, CandidateSkill } from '../types/profile';
import type { Certification, Education, Project } from '../types/career';

export interface ProfileUpdate {
  headline?: string;
  summary?: string;
  phone?: string;
  location?: string;
  linkedin_url?: string;
  github_url?: string;
  portfolio_url?: string;
}

export interface ExperienceInput {
  company_name: string;
  job_title: string;
  start_date: string;
  end_date?: string;
  is_current: boolean;
  description?: string;
}

export const profileApi = {
  get: () => apiClient<CareerProfile>('/profile'),
  update: (payload: ProfileUpdate) =>
    apiClient<CareerProfile>('/profile', { method: 'PUT', body: JSON.stringify(payload) }),
  addExperience: (payload: ExperienceInput) =>
    apiClient<Experience>('/profile/experiences', { method: 'POST', body: JSON.stringify(payload) }),
  deleteExperience: (id: string) =>
    apiClient<void>(`/profile/experiences/${id}`, { method: 'DELETE' }),
  addSkill: (name: string) =>
    apiClient<CandidateSkill>('/profile/skills', {
      method: 'POST',
      body: JSON.stringify({ name, experience_type: 'professional' }),
    }),
  deleteSkill: (id: string) => apiClient<void>(`/profile/skills/${id}`, { method: 'DELETE' }),
  addProject: (payload: { name: string; description: string; project_type: string }) =>
    apiClient<Project>('/profile/projects', { method: 'POST', body: JSON.stringify(payload) }),
  deleteProject: (id: string) => apiClient<void>(`/profile/projects/${id}`, { method: 'DELETE' }),
  addEducation: (payload: { institution: string; degree: string; field_of_study?: string }) =>
    apiClient<Education>('/profile/education', { method: 'POST', body: JSON.stringify(payload) }),
  deleteEducation: (id: string) => apiClient<void>(`/profile/education/${id}`, { method: 'DELETE' }),
  addCertification: (payload: { name: string; issuing_organization: string }) =>
    apiClient<Certification>('/profile/certifications', { method: 'POST', body: JSON.stringify(payload) }),
  deleteCertification: (id: string) => apiClient<void>(`/profile/certifications/${id}`, { method: 'DELETE' }),
};