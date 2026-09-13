import { apiClient, setAccessToken } from './client';
import type {
  AuthResponse,
  LoginCredentials,
  RegisterData,
  TokenRefreshResponse,
  User,
} from '../types/auth';

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const data = await apiClient<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
      skipAuth: true,
      retryOn401: false,
    });
    setAccessToken(data.access_token);
    return data;
  },

  register: async (registerData: RegisterData) => {
    return apiClient<{ id: string; email: string; full_name: string; career_profile?: any; message: string }>(
      '/auth/register',
      {
        method: 'POST',
        body: JSON.stringify(registerData),
        skipAuth: true,
      }
    );
  },

  refresh: async (): Promise<TokenRefreshResponse> => {
    const data = await apiClient<TokenRefreshResponse>('/auth/refresh', {
      method: 'POST',
      skipAuth: true,
      retryOn401: false,
    });
    setAccessToken(data.access_token);
    return data;
  },

  logout: async (allDevices: boolean = false) => {
    try {
      await apiClient<{ message: string }>('/auth/logout', {
        method: 'POST',
        body: JSON.stringify({ all_devices: allDevices }),
        retryOn401: false,
      });
    } finally {
      setAccessToken(null);
    }
  },

  getMe: async (): Promise<User> => {
    return apiClient<User>('/auth/me');
  },
};
