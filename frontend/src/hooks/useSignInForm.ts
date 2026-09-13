import { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { isValidEmail } from '../utils/passwordStrength';
import { ApiError } from '../api/client';

export interface SignInFormValues {
  email: string;
  password: string;
}

export interface SignInFormErrors {
  email?: string;
  password?: string;
}

export type SignInErrorType = 'INVALID_CREDENTIALS' | 'INACTIVE_USER' | 'NETWORK_ERROR' | 'GENERAL_ERROR';

export interface SignInErrorState {
  message: string;
  type: SignInErrorType;
  code?: string;
}

export interface UseSignInFormOptions {
  onSuccess?: () => void;
}

export function useSignInForm(options: UseSignInFormOptions = {}) {
  const { login, clearError: clearAuthError } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  // Extract any email passed via route state or URL query parameters
  const initialEmail =
    (location.state as any)?.email ||
    new URLSearchParams(location.search).get('email') ||
    '';

  const [values, setValues] = useState<SignInFormValues>({
    email: initialEmail,
    password: '',
  });

  const [touched, setTouched] = useState<Partial<Record<keyof SignInFormValues, boolean>>>({});
  const [errors, setErrors] = useState<SignInFormErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState<SignInErrorState | null>(null);

  // Synchronous lock against rapid multi-clicks
  const submittingLock = useRef(false);

  useEffect(() => {
    if (initialEmail) {
      setValues((prev) => ({ ...prev, email: initialEmail }));
    }
  }, [initialEmail]);

  const validateField = (field: keyof SignInFormValues, currentValues: SignInFormValues): string | undefined => {
    switch (field) {
      case 'email':
        if (!currentValues.email.trim()) {
          return 'Email address is required.';
        }
        if (!isValidEmail(currentValues.email)) {
          return 'Please enter a valid email address.';
        }
        return undefined;

      case 'password':
        if (!currentValues.password) {
          return 'Password is required.';
        }
        return undefined;

      default:
        return undefined;
    }
  };

  const validateAll = (): boolean => {
    const newErrors: SignInFormErrors = {};
    let isValid = true;

    const emailErr = validateField('email', values);
    if (emailErr) {
      newErrors.email = emailErr;
      isValid = false;
    }

    const passErr = validateField('password', values);
    if (passErr) {
      newErrors.password = passErr;
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleChange = (field: keyof SignInFormValues, val: string) => {
    setValues((prev) => {
      const next = { ...prev, [field]: val };

      // Clear field-level error on edit
      if (errors[field]) {
        setErrors((prevErrors) => ({ ...prevErrors, [field]: undefined }));
      }

      // Clear top banner error when candidate edits inputs
      if (formError) {
        setFormError(null);
        clearAuthError();
      }

      return next;
    });
  };

  const handleBlur = (field: keyof SignInFormValues) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    const err = validateField(field, values);
    setErrors((prev) => ({ ...prev, [field]: err }));
  };

  const toggleShowPassword = () => setShowPassword((prev) => !prev);

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault();
    }

    // Submit protection against duplicate clicks / concurrent requests
    if (submittingLock.current || isSubmitting) {
      return;
    }

    setFormError(null);
    clearAuthError();

    // Mark all as touched to trigger validation displays
    setTouched({ email: true, password: true });

    if (!validateAll()) {
      return;
    }

    submittingLock.current = true;
    setIsSubmitting(true);

    try {
      await login({
        email: values.email.trim().toLowerCase(),
        password: values.password,
      });

      if (options.onSuccess) {
        options.onSuccess();
      } else {
        // Default navigation to redirect target or dashboard
        const from = (location.state as any)?.from?.pathname || '/app/dashboard';
        navigate(from, { replace: true });
      }
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        if (err.code === 'NETWORK_ERROR' || err.status === 0) {
          setFormError({
            type: 'NETWORK_ERROR',
            message: 'Unable to connect to CareerMate server. Please check your internet connection.',
            code: err.code,
          });
        } else if (err.status === 401) {
          const isInactive = err.message.toLowerCase().includes('deactivated');
          setFormError({
            type: isInactive ? 'INACTIVE_USER' : 'INVALID_CREDENTIALS',
            message: isInactive
              ? 'This account has been deactivated. Please contact support.'
              : 'Invalid email or password. Please verify your credentials and try again.',
            code: err.code,
          });
        } else {
          setFormError({
            type: 'GENERAL_ERROR',
            message: err.message || 'An unexpected authentication error occurred.',
            code: err.code,
          });
        }
      } else {
        setFormError({
          type: 'GENERAL_ERROR',
          message: (err as Error)?.message || 'An unexpected error occurred. Please try again.',
        });
      }
    } finally {
      setIsSubmitting(false);
      submittingLock.current = false;
    }
  };

  return {
    values,
    errors,
    touched,
    isSubmitting,
    formError,
    showPassword,
    handleChange,
    handleBlur,
    handleSubmit,
    toggleShowPassword,
    clearError: () => {
      setFormError(null);
      clearAuthError();
    },
  };
}
