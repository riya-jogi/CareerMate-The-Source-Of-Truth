import type { ApiResponseError } from '../types/auth';

let inMemoryAccessToken: string | null = null;
let refreshPromise: Promise<string | null> | null = null;

export const setAccessToken = (token: string | null) => {
  inMemoryAccessToken = token;
};

export const getAccessToken = (): string | null => {
  return inMemoryAccessToken;
};

export class ApiError extends Error {
  code: string;
  details?: Record<string, any>;
  status: number;

  constructor(message: string, status: number, code: string = 'API_ERROR', details?: Record<string, any>) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

interface RequestOptions extends RequestInit {
  skipAuth?: boolean;
  retryOn401?: boolean;
}

export async function apiClient<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { skipAuth = false, retryOn401 = true, headers = {}, ...restOptions } = options;

  const url = endpoint.startsWith('http') ? endpoint : endpoint.startsWith('/api') ? endpoint : `/api/v1${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

  const requestHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(headers as Record<string, string>),
  };

  if (!skipAuth && inMemoryAccessToken) {
    requestHeaders['Authorization'] = `Bearer ${inMemoryAccessToken}`;
  }

  let response: Response;
  try {
    response = await fetch(url, {
      ...restOptions,
      headers: requestHeaders,
      credentials: 'include', // Transmits HttpOnly refresh cookies
    });
  } catch (err: any) {
    throw new ApiError(
      'Unable to connect to the CareerMate server. Please check your internet connection.',
      0,
      'NETWORK_ERROR',
      { originalError: err?.message }
    );
  }

  // Handle 401 Unauthorized with automatic token refresh (except for login/refresh requests themselves)
  if (response.status === 401 && retryOn401 && !url.includes('/auth/login') && !url.includes('/auth/refresh')) {
    if (!refreshPromise) {
      refreshPromise = (async () => {
        try {
          const refreshRes = await fetch('/api/v1/auth/refresh', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
          });

          if (!refreshRes.ok) {
            setAccessToken(null);
            return null;
          }

          const data = await refreshRes.json();
          setAccessToken(data.access_token);
          return data.access_token as string;
        } catch {
          setAccessToken(null);
          return null;
        } finally {
          refreshPromise = null;
        }
      })();
    }

    const newToken = await refreshPromise;
    if (newToken) {
      requestHeaders['Authorization'] = `Bearer ${newToken}`;
      try {
        response = await fetch(url, {
          ...restOptions,
          headers: requestHeaders,
          credentials: 'include',
        });
      } catch (err: any) {
        throw new ApiError(
          'Unable to connect to the CareerMate server. Please check your internet connection.',
          0,
          'NETWORK_ERROR',
          { originalError: err?.message }
        );
      }
    }
  }

  if (!response.ok) {
    let errorData: ApiResponseError | null = null;
    try {
      errorData = await response.json();
    } catch {
      // response was not JSON
    }

    const message = errorData?.error?.message || response.statusText || 'An unexpected error occurred.';
    const code = errorData?.error?.code || `HTTP_${response.status}`;
    const details = errorData?.error?.details;

    throw new ApiError(message, response.status, code, details);
  }

  // If response has no content (204)
  if (response.status === 204) {
    return {} as T;
  }

  return response.json() as Promise<T>;
}
