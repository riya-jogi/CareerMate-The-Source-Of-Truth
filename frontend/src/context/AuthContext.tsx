import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { authApi } from '../api/auth';
import { setAccessToken } from '../api/client';
import type { LoginCredentials, RegisterData, User } from '../types/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: (allDevices?: boolean) => Promise<void>;
  clearError: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Initialize session on application boot
  const initAuth = useCallback(async () => {
    try {
      setIsLoading(true);
      // Attempt silent refresh using HttpOnly cookie
      await authApi.refresh();
      // Fetch full candidate profile and verification state
      const currentUser = await authApi.getMe();
      setUser(currentUser);
    } catch {
      // Unauthenticated state is normal on cold boot when not logged in
      setUser(null);
      setAccessToken(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  const login = async (credentials: LoginCredentials) => {
    setError(null);
    setIsLoading(true);
    try {
      const response = await authApi.login(credentials);
      setUser(response.user);
    } catch (err: any) {
      const msg = err.message || 'Failed to sign in. Please verify your credentials.';
      setError(msg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    setError(null);
    setIsLoading(true);
    try {
      await authApi.register(data);
      // Auto-login after successful registration
      const loginRes = await authApi.login({ email: data.email, password: data.password });
      setUser(loginRes.user);
    } catch (err: any) {
      const msg = err.message || 'Registration failed. Please check your details.';
      setError(msg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (allDevices: boolean = false) => {
    setIsLoading(true);
    try {
      await authApi.logout(allDevices);
    } finally {
      setUser(null);
      setAccessToken(null);
      setIsLoading(false);
    }
  };

  const refreshProfile = async () => {
    try {
      const updated = await authApi.getMe();
      setUser(updated);
    } catch (err) {
      console.error('Failed to refresh user profile:', err);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        error,
        login,
        register,
        logout,
        clearError,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
