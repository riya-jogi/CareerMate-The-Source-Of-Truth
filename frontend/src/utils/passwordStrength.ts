/**
 * Utility functions for password strength calculation, rule evaluation,
 * and email format validation.
 */

export interface PasswordCriterion {
  id: string;
  label: string;
  met: boolean;
}

export interface PasswordStrengthResult {
  score: number; // 0 to 5
  label: 'Very Weak' | 'Weak' | 'Fair' | 'Good' | 'Strong';
  barColor: string;
  textColor: string;
  percentage: number;
  criteria: PasswordCriterion[];
  allMet: boolean;
}

export const evaluatePasswordStrength = (password: string): PasswordStrengthResult => {
  const criteria: PasswordCriterion[] = [
    {
      id: 'length',
      label: 'At least 8 characters',
      met: password.length >= 8,
    },
    {
      id: 'uppercase',
      label: 'At least one uppercase letter (A-Z)',
      met: /[A-Z]/.test(password),
    },
    {
      id: 'lowercase',
      label: 'At least one lowercase letter (a-z)',
      met: /[a-z]/.test(password),
    },
    {
      id: 'number',
      label: 'At least one number (0-9)',
      met: /[0-9]/.test(password),
    },
    {
      id: 'special',
      label: 'At least one special character (!@#$%^&*)',
      met: /[!@#$%^&*()_+\-=[\]{}|;:,.<>?~`]/.test(password),
    },
  ];

  const metCount = criteria.filter((c) => c.met).length;
  const allMet = metCount === criteria.length;

  if (password.length === 0) {
    return {
      score: 0,
      label: 'Very Weak',
      barColor: 'bg-slate-700',
      textColor: 'text-slate-500',
      percentage: 0,
      criteria,
      allMet: false,
    };
  }

  if (metCount <= 1) {
    return {
      score: 1,
      label: 'Very Weak',
      barColor: 'bg-rose-500',
      textColor: 'text-rose-400',
      percentage: 20,
      criteria,
      allMet,
    };
  }

  if (metCount <= 2) {
    return {
      score: 2,
      label: 'Weak',
      barColor: 'bg-rose-400',
      textColor: 'text-rose-400',
      percentage: 40,
      criteria,
      allMet,
    };
  }

  if (metCount <= 3) {
    return {
      score: 3,
      label: 'Fair',
      barColor: 'bg-amber-400',
      textColor: 'text-amber-400',
      percentage: 60,
      criteria,
      allMet,
    };
  }

  if (metCount === 4) {
    return {
      score: 4,
      label: 'Good',
      barColor: 'bg-indigo-400',
      textColor: 'text-indigo-400',
      percentage: 80,
      criteria,
      allMet,
    };
  }

  return {
    score: 5,
    label: 'Strong',
    barColor: 'bg-emerald-400',
    textColor: 'text-emerald-400',
    percentage: 100,
    criteria,
    allMet: true,
  };
};

/**
 * Validates whether an email string adheres to basic RFC-compliant format.
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.trim());
};
