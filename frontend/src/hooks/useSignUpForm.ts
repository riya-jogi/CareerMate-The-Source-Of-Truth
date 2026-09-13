import { useState, useRef, useMemo } from 'react';
import { useAuth } from '../context/AuthContext';
import { evaluatePasswordStrength, isValidEmail } from '../utils/passwordStrength';
import type { PasswordStrengthResult } from '../utils/passwordStrength';
import { ApiError } from '../api/client';

export interface SignUpFormValues {
  fullName: string;
  email: string;
  headline: string;
  password: string;
  confirmPassword: string;
}

export interface SignUpFormErrors {
  fullName?: string;
  email?: string;
  headline?: string;
  password?: string;
  confirmPassword?: string;
}

export interface ServerErrorState {
  message: string;
  isDuplicateEmail: boolean;
  code?: string;
}

export interface UseSignUpFormOptions {
  onSuccess?: () => void;
}

export function useSignUpForm(options: UseSignUpFormOptions = {}) {
  const { register } = useAuth();

  const [values, setValues] = useState<SignUpFormValues>({
    fullName: '',
    email: '',
    headline: '',
    password: '',
    confirmPassword: '',
  });

  const [touched, setTouched] = useState<Partial<Record<keyof SignUpFormValues, boolean>>>({});
  const [errors, setErrors] = useState<SignUpFormErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [serverError, setServerError] = useState<ServerErrorState | null>(null);

  // Synchronous submission lock to prevent race conditions or duplicate clicks
  const submittingLock = useRef(false);

  // Real-time password evaluation
  const passwordStrength: PasswordStrengthResult = useMemo(
    () => evaluatePasswordStrength(values.password),
    [values.password]
  );

  const passwordsMatch = useMemo(() => {
    return values.confirmPassword.length > 0 && values.password === values.confirmPassword;
  }, [values.password, values.confirmPassword]);

  const passwordsMismatch = useMemo(() => {
    return values.confirmPassword.length > 0 && values.password !== values.confirmPassword;
  }, [values.password, values.confirmPassword]);

  // Validate a single field
  const validateField = (field: keyof SignUpFormValues, currentValues: SignUpFormValues): string | undefined => {
    switch (field) {
      case 'fullName':
        if (!currentValues.fullName.trim()) {
          return 'Full name is required.';
        }
        if (currentValues.fullName.trim().length < 2) {
          return 'Full name must be at least 2 characters.';
        }
        if (currentValues.fullName.length > 100) {
          return 'Full name cannot exceed 100 characters.';
        }
        return undefined;

      case 'email':
        if (!currentValues.email.trim()) {
          return 'Email address is required.';
        }
        if (!isValidEmail(currentValues.email)) {
          return 'Please enter a valid email address.';
        }
        return undefined;

      case 'headline':
        if (currentValues.headline && currentValues.headline.length > 255) {
          return 'Headline cannot exceed 255 characters.';
        }
        return undefined;

      case 'password':
        if (!currentValues.password) {
          return 'Password is required.';
        }
        if (!passwordStrength.allMet) {
          return 'Password does not meet all required security criteria.';
        }
        return undefined;

      case 'confirmPassword':
        if (!currentValues.confirmPassword) {
          return 'Please confirm your password.';
        }
        if (currentValues.password !== currentValues.confirmPassword) {
          return 'Passwords do not match.';
        }
        return undefined;

      default:
        return undefined;
    }
  };

  // Validate all fields together
  const validateAll = (): boolean => {
    const newErrors: SignUpFormErrors = {};
    let isValid = true;

    const fields: (keyof SignUpFormValues)[] = ['fullName', 'email', 'password', 'confirmPassword', 'headline'];
    fields.forEach((field) => {
      const err = validateField(field, values);
      if (err) {
        newErrors[field] = err;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  const handleChange = (field: keyof SignUpFormValues, val: string) => {
    setValues((prev) => {
      const next = { ...prev, [field]: val };

      // Clear field-level error when user modifies the input
      if (errors[field]) {
        setErrors((errs) => ({ ...errs, [field]: undefined }));
      }

      // If user is editing email, clear previous duplicate email server error
      if (field === 'email' && serverError?.isDuplicateEmail) {
        setServerError(null);
      }

      return next;
    });
  };

  const handleBlur = (field: keyof SignUpFormValues) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    const err = validateField(field, values);
    setErrors((prev) => ({ ...prev, [field]: err }));
  };

  const toggleShowPassword = () => setShowPassword((prev) => !prev);
  const toggleShowConfirmPassword = () => setShowConfirmPassword((prev) => !prev);

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault();
    }

    // Submit protection against duplicate clicks / concurrent requests
    if (submittingLock.current || isSubmitting) {
      return;
    }

    setServerError(null);

    // Mark all as touched to display validation indicators
    setTouched({
      fullName: true,
      email: true,
      headline: true,
      password: true,
      confirmPassword: true,
    });

    const isValid = validateAll();
    if (!isValid) {
      return;
    }

    submittingLock.current = true;
    setIsSubmitting(true);

    try {
      await register({
        full_name: values.fullName.trim(),
        email: values.email.trim().toLowerCase(),
        password: values.password,
        headline: values.headline.trim() || undefined,
      });

      if (options.onSuccess) {
        options.onSuccess();
      }
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        const isDuplicate =
          err.status === 409 ||
          err.code === 'CONFLICT' ||
          err.message.toLowerCase().includes('already exists');

        setServerError({
          message: isDuplicate
            ? `An account with the email "${values.email}" already exists.`
            : err.message || 'Registration failed. Please check your information.',
          isDuplicateEmail: isDuplicate,
          code: err.code,
        });

        if (isDuplicate) {
          setErrors((prev) => ({
            ...prev,
            email: 'An account with this email already exists.',
          }));
        }
      } else {
        setServerError({
          message: (err as Error)?.message || 'An unexpected error occurred. Please try again.',
          isDuplicateEmail: false,
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
    serverError,
    showPassword,
    showConfirmPassword,
    passwordStrength,
    passwordsMatch,
    passwordsMismatch,
    handleChange,
    handleBlur,
    handleSubmit,
    toggleShowPassword,
    toggleShowConfirmPassword,
    clearServerError: () => setServerError(null),
  };
}
