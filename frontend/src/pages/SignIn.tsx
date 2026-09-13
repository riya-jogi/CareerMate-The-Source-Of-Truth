import React from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  Mail,
  Lock,
  AlertCircle,
  ArrowRight,
  Loader2,
  Eye,
  EyeOff,
  WifiOff,
  UserX,
} from 'lucide-react';
import { useSignInForm } from '../hooks/useSignInForm';

export const SignIn: React.FC = () => {
  const {
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
  } = useSignInForm();

  return (
    <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Ambient background glows */}
      <div
        className="ambient-glow bg-indigo-600/15 w-[500px] h-[500px] -top-32 -left-32 pointer-events-none"
        aria-hidden="true"
      />
      <div
        className="ambient-glow bg-violet-600/10 w-[500px] h-[500px] -bottom-32 -right-32 pointer-events-none"
        aria-hidden="true"
      />

      <main className="w-full max-w-md relative z-10 my-8">
        {/* Brand Header */}
        <header className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-600 to-indigo-400 text-white shadow-glow-brand mb-4">
            <ShieldCheck className="w-8 h-8" aria-hidden="true" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Welcome to CareerMate
          </h1>
          <p className="text-xs uppercase tracking-widest text-indigo-400 font-bold mt-1">
            The Source Of Truth Platform
          </p>
          <p className="text-sm text-slate-400 mt-2">
            Sign in to access your verified career source of truth.
          </p>
        </header>

        {/* Form Card */}
        <div className="glass-panel p-6 sm:p-8 rounded-2xl shadow-2xl border border-white/10">
          {/* Error Alert Banner */}
          {formError && (
            <section
              role="alert"
              aria-live="polite"
              className={`mb-6 p-4 rounded-xl border flex items-start space-x-3 transition-all ${
                formError.type === 'NETWORK_ERROR'
                  ? 'bg-amber-500/10 border-amber-500/20 text-amber-200'
                  : 'bg-rose-500/10 border-rose-500/20 text-rose-300'
              }`}
            >
              {formError.type === 'NETWORK_ERROR' ? (
                <WifiOff className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" aria-hidden="true" />
              ) : formError.type === 'INACTIVE_USER' ? (
                <UserX className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" aria-hidden="true" />
              ) : (
                <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" aria-hidden="true" />
              )}
              <div className="flex-1 text-sm">
                <p className="font-medium leading-relaxed">{formError.message}</p>
                {formError.type === 'NETWORK_ERROR' && (
                  <p className="text-xs text-amber-300/80 mt-1">
                    Please ensure your backend server is running and your device has an active internet connection.
                  </p>
                )}
              </div>
            </section>
          )}

          <form onSubmit={handleSubmit} noValidate className="space-y-5">
            {/* Email Field */}
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
                  placeholder="candidate@example.com"
                  className={`w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/80 border text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                    touched.email && errors.email
                      ? 'border-rose-500/60 focus:border-rose-500 focus:ring-rose-500/20'
                      : 'border-white/10 focus:border-indigo-500 focus:ring-indigo-500/20'
                  }`}
                />
              </div>
            </div>

            {/* Password Field */}
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
                  autoComplete="current-password"
                  disabled={isSubmitting}
                  value={values.password}
                  onChange={(e) => handleChange('password', e.target.value)}
                  onBlur={() => handleBlur('password')}
                  aria-required="true"
                  aria-invalid={Boolean(touched.password && errors.password)}
                  aria-describedby={touched.password && errors.password ? 'password-error' : undefined}
                  placeholder="••••••••••••"
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
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-600 text-white font-semibold text-sm shadow-glow-brand transition-all flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#0B0F19]"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>Sign In to CareerMate</span>
                  <ArrowRight className="w-4 h-4" aria-hidden="true" />
                </>
              )}
            </button>
          </form>

          {/* Footer Navigation */}
          <footer className="mt-6 pt-6 border-t border-white/10 text-center text-xs text-slate-400">
            Don't have an account yet?{' '}
            <Link
              to="/signup"
              className="text-indigo-400 hover:text-indigo-300 font-semibold focus:outline-none focus:underline"
            >
              Create a candidate account
            </Link>
          </footer>
        </div>
      </main>
    </div>
  );
};
