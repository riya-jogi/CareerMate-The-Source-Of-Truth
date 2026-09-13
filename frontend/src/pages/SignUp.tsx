import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ShieldCheck,
  Mail,
  Lock,
  User,
  Briefcase,
  AlertCircle,
  Check,
  X,
  ArrowRight,
  Loader2,
  Eye,
  EyeOff,
  LogIn,
} from 'lucide-react';
import { useSignUpForm } from '../hooks/useSignUpForm';

export const SignUp: React.FC = () => {
  const navigate = useNavigate();

  const {
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
  } = useSignUpForm({
    onSuccess: () => {
      navigate('/app/dashboard', { replace: true });
    },
  });

  return (
    <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Ambient background glows */}
      <div
        className="ambient-glow bg-indigo-600/15 w-[500px] h-[500px] -top-32 -left-32 pointer-events-none"
        aria-hidden="true"
      />
      <div
        className="ambient-glow bg-emerald-600/10 w-[500px] h-[500px] -bottom-32 -right-32 pointer-events-none"
        aria-hidden="true"
      />

      <main className="w-full max-w-xl relative z-10 my-8">
        {/* Brand Header */}
        <header className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-600 to-indigo-400 text-white shadow-glow-brand mb-4">
            <ShieldCheck className="w-8 h-8" aria-hidden="true" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Create Candidate Account
          </h1>
          <p className="text-xs uppercase tracking-widest text-indigo-400 font-bold mt-1">
            Establish Your Source Of Truth
          </p>
          <p className="text-sm text-slate-400 mt-2 max-w-md mx-auto">
            Anchor your verified career claims and optimize resumes without fabrication.
          </p>
        </header>

        {/* Form Card */}
        <div className="glass-panel p-6 sm:p-8 rounded-2xl shadow-2xl border border-white/10">
          {/* Backend Error / Duplicate Email Banner */}
          {serverError && (
            <section
              role="alert"
              aria-live="polite"
              className={`mb-6 p-4 rounded-xl border flex items-start space-x-3 transition-all ${
                serverError.isDuplicateEmail
                  ? 'bg-amber-500/10 border-amber-500/30 text-amber-200'
                  : 'bg-rose-500/10 border-rose-500/20 text-rose-300'
              }`}
            >
              <AlertCircle
                className={`w-5 h-5 shrink-0 mt-0.5 ${
                  serverError.isDuplicateEmail ? 'text-amber-400' : 'text-rose-400'
                }`}
                aria-hidden="true"
              />
              <div className="flex-1 text-sm space-y-2">
                <p className="font-medium leading-relaxed">{serverError.message}</p>
                {serverError.isDuplicateEmail && (
                  <div>
                    <Link
                      to="/signin"
                      state={{ email: values.email }}
                      className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 font-medium text-xs border border-amber-500/30 transition-colors"
                    >
                      <LogIn className="w-3.5 h-3.5" aria-hidden="true" />
                      <span>Sign in to your account with this email &rarr;</span>
                    </Link>
                  </div>
                )}
              </div>
            </section>
          )}

          <form onSubmit={handleSubmit} noValidate className="space-y-4">
            {/* Full Name */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label
                  htmlFor="fullName"
                  className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
                >
                  Full Name <span className="text-rose-400">*</span>
                </label>
                {touched.fullName && errors.fullName && (
                  <span
                    id="fullName-error"
                    role="alert"
                    className="text-xs text-rose-400 font-medium"
                  >
                    {errors.fullName}
                  </span>
                )}
              </div>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400"
                  aria-hidden="true"
                >
                  <User className="w-4 h-4" />
                </div>
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  required
                  autoComplete="name"
                  disabled={isSubmitting}
                  value={values.fullName}
                  onChange={(e) => handleChange('fullName', e.target.value)}
                  onBlur={() => handleBlur('fullName')}
                  aria-required="true"
                  aria-invalid={Boolean(touched.fullName && errors.fullName)}
                  aria-describedby={touched.fullName && errors.fullName ? 'fullName-error' : undefined}
                  placeholder="Alex Rivera"
                  className={`w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/80 border text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                    touched.fullName && errors.fullName
                      ? 'border-rose-500/60 focus:border-rose-500 focus:ring-rose-500/20'
                      : 'border-white/10 focus:border-indigo-500 focus:ring-indigo-500/20'
                  }`}
                />
              </div>
            </div>

            {/* Email Address */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label
                  htmlFor="email"
                  className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
                >
                  Email Address <span className="text-rose-400">*</span>
                </label>
                {touched.email && errors.email && (
                  <span
                    id="email-error"
                    role="alert"
                    className="text-xs text-rose-400 font-medium"
                  >
                    {errors.email}
                  </span>
                )}
              </div>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400"
                  aria-hidden="true"
                >
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  autoComplete="email"
                  disabled={isSubmitting}
                  value={values.email}
                  onChange={(e) => handleChange('email', e.target.value)}
                  onBlur={() => handleBlur('email')}
                  aria-required="true"
                  aria-invalid={Boolean(touched.email && errors.email)}
                  aria-describedby={touched.email && errors.email ? 'email-error' : undefined}
                  placeholder="alex.rivera@example.com"
                  className={`w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/80 border text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                    touched.email && errors.email
                      ? 'border-rose-500/60 focus:border-rose-500 focus:ring-rose-500/20'
                      : 'border-white/10 focus:border-indigo-500 focus:ring-indigo-500/20'
                  }`}
                />
              </div>
            </div>

            {/* Professional Headline (Optional) */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label
                  htmlFor="headline"
                  className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
                >
                  Professional Headline{' '}
                  <span className="text-slate-500 font-normal normal-case">(Optional)</span>
                </label>
                {touched.headline && errors.headline && (
                  <span
                    id="headline-error"
                    role="alert"
                    className="text-xs text-rose-400 font-medium"
                  >
                    {errors.headline}
                  </span>
                )}
              </div>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400"
                  aria-hidden="true"
                >
                  <Briefcase className="w-4 h-4" />
                </div>
                <input
                  id="headline"
                  name="headline"
                  type="text"
                  disabled={isSubmitting}
                  value={values.headline}
                  onChange={(e) => handleChange('headline', e.target.value)}
                  onBlur={() => handleBlur('headline')}
                  aria-describedby="headline-desc"
                  placeholder="Lead AI Platform Engineer | Python & React"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/80 border border-white/10 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                />
              </div>
              <p id="headline-desc" className="text-[11px] text-slate-500 mt-1">
                Serves as the headline on your initial verified career anchor profile.
              </p>
            </div>

            {/* Password */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label
                  htmlFor="password"
                  className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
                >
                  Password <span className="text-rose-400">*</span>
                </label>
                {touched.password && errors.password && (
                  <span
                    id="password-error"
                    role="alert"
                    className="text-xs text-rose-400 font-medium"
                  >
                    {errors.password}
                  </span>
                )}
              </div>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400"
                  aria-hidden="true"
                >
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  autoComplete="new-password"
                  disabled={isSubmitting}
                  value={values.password}
                  onChange={(e) => handleChange('password', e.target.value)}
                  onBlur={() => handleBlur('password')}
                  aria-required="true"
                  aria-invalid={Boolean(touched.password && errors.password)}
                  aria-describedby="password-rules password-strength"
                  placeholder="Create a strong password"
                  className={`w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-900/80 border text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                    touched.password && errors.password
                      ? 'border-rose-500/60 focus:border-rose-500 focus:ring-rose-500/20'
                      : 'border-white/10 focus:border-indigo-500 focus:ring-indigo-500/20'
                  }`}
                />
                <button
                  type="button"
                  onClick={toggleShowPassword}
                  disabled={isSubmitting}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-200 transition-colors focus:outline-none"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" aria-hidden="true" />
                  ) : (
                    <Eye className="w-4 h-4" aria-hidden="true" />
                  )}
                </button>
              </div>

              {/* Password Strength Meter */}
              {values.password.length > 0 && (
                <div id="password-strength" className="mt-2 space-y-1">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-400">Security Strength:</span>
                    <span className={`font-semibold ${passwordStrength.textColor}`}>
                      {passwordStrength.label}
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full transition-all duration-300 ${passwordStrength.barColor}`}
                      style={{ width: `${passwordStrength.percentage}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Password Requirements Checklist */}
              <div
                id="password-rules"
                className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-white/5 space-y-1.5"
              >
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Password Strength Requirements
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs">
                  {passwordStrength.criteria.map((criterion) => (
                    <div
                      key={criterion.id}
                      className={`flex items-center space-x-2 ${
                        criterion.met ? 'text-emerald-400 font-medium' : 'text-slate-500'
                      }`}
                    >
                      <div
                        className={`w-3.5 h-3.5 rounded-full flex items-center justify-center text-[10px] shrink-0 transition-colors ${
                          criterion.met
                            ? 'bg-emerald-500/20 text-emerald-400'
                            : 'bg-slate-800 text-slate-600'
                        }`}
                      >
                        {criterion.met ? (
                          <Check className="w-2.5 h-2.5" aria-hidden="true" />
                        ) : (
                          <span aria-hidden="true">•</span>
                        )}
                      </div>
                      <span>{criterion.label}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label
                  htmlFor="confirmPassword"
                  className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
                >
                  Confirm Password <span className="text-rose-400">*</span>
                </label>
                {touched.confirmPassword && errors.confirmPassword && (
                  <span
                    id="confirmPassword-error"
                    role="alert"
                    className="text-xs text-rose-400 font-medium"
                  >
                    {errors.confirmPassword}
                  </span>
                )}
              </div>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400"
                  aria-hidden="true"
                >
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  autoComplete="new-password"
                  disabled={isSubmitting}
                  value={values.confirmPassword}
                  onChange={(e) => handleChange('confirmPassword', e.target.value)}
                  onBlur={() => handleBlur('confirmPassword')}
                  aria-required="true"
                  aria-invalid={Boolean(touched.confirmPassword && errors.confirmPassword)}
                  aria-describedby="confirm-password-status"
                  placeholder="Repeat your password"
                  className={`w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-900/80 border text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                    passwordsMismatch
                      ? 'border-rose-500/60 focus:border-rose-500 focus:ring-rose-500/20'
                      : passwordsMatch
                      ? 'border-emerald-500/60 focus:border-emerald-500 focus:ring-emerald-500/20'
                      : 'border-white/10 focus:border-indigo-500 focus:ring-indigo-500/20'
                  }`}
                />
                <button
                  type="button"
                  onClick={toggleShowConfirmPassword}
                  disabled={isSubmitting}
                  aria-label={showConfirmPassword ? 'Hide confirm password' : 'Show confirm password'}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-200 transition-colors focus:outline-none"
                >
                  {showConfirmPassword ? (
                    <EyeOff className="w-4 h-4" aria-hidden="true" />
                  ) : (
                    <Eye className="w-4 h-4" aria-hidden="true" />
                  )}
                </button>
              </div>

              {/* Real-time Confirm Password Feedback */}
              <div id="confirm-password-status" className="mt-1.5">
                {passwordsMatch && (
                  <div className="flex items-center space-x-1.5 text-xs text-emerald-400">
                    <Check className="w-3.5 h-3.5" aria-hidden="true" />
                    <span>Passwords match perfectly.</span>
                  </div>
                )}
                {passwordsMismatch && (
                  <div className="flex items-center space-x-1.5 text-xs text-rose-400">
                    <X className="w-3.5 h-3.5" aria-hidden="true" />
                    <span>Passwords do not match.</span>
                  </div>
                )}
              </div>
            </div>

            {/* Submit Button with Duplicate Request Protection */}
            <button
              type="submit"
              disabled={isSubmitting || !passwordStrength.allMet || passwordsMismatch}
              className="w-full mt-4 py-3 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-600 text-white font-semibold text-sm shadow-glow-brand transition-all flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#0B0F19]"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                  <span>Provisioning Career Anchor...</span>
                </>
              ) : (
                <>
                  <span>Create Candidate Profile</span>
                  <ArrowRight className="w-4 h-4" aria-hidden="true" />
                </>
              )}
            </button>
          </form>

          {/* Footer Navigation */}
          <footer className="mt-6 pt-6 border-t border-white/10 text-center text-xs text-slate-400">
            Already have an account?{' '}
            <Link
              to="/signin"
              className="text-indigo-400 hover:text-indigo-300 font-semibold focus:outline-none focus:underline"
            >
              Sign in to your account
            </Link>
          </footer>
        </div>
      </main>
    </div>
  );
};
