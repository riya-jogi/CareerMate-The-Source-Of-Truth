import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardApi } from '../api/dashboard';
import type { DashboardSummary } from '../types/dashboard';
import { WelcomeSection } from '../components/dashboard/WelcomeSection';
import { ProfileProgressCard } from '../components/dashboard/ProfileProgressCard';
import { ResumeStatusCard } from '../components/dashboard/ResumeStatusCard';
import { JobAnalysisCard } from '../components/dashboard/JobAnalysisCard';
import { MatchingCard } from '../components/dashboard/MatchingCard';
import { OptimizationCard } from '../components/dashboard/OptimizationCard';
import { GettingStartedSection } from '../components/dashboard/GettingStartedSection';
import { SecurityOverviewCard } from '../components/dashboard/SecurityOverviewCard';
import { Loader2, RefreshCw, AlertCircle } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { user, refreshProfile } = useAuth();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Ensure user profile is up-to-date
      await refreshProfile();
      const data = await dashboardApi.getSummary();
      setSummary(data);
    } catch (err: any) {
      console.error('Failed to load dashboard summary:', err);
      setError('Unable to load live dashboard statistics. Displaying cached session information.');
    } finally {
      setIsLoading(false);
    }
  }, [refreshProfile]);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  return (
    <div className="space-y-8 pb-12 max-w-7xl mx-auto">
      {/* Dynamic Error / Refresh Notification */}
      {error && (
        <div
          role="alert"
          className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-200 text-sm flex items-center justify-between gap-3"
        >
          <div className="flex items-center space-x-2.5">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" aria-hidden="true" />
            <span>{error}</span>
          </div>
          <button
            onClick={fetchDashboardData}
            className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-xs font-semibold transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* 1. Welcome Section with Live User Profile */}
      <WelcomeSection
        summary={summary}
        fallbackName={user?.full_name}
        fallbackHeadline={user?.career_profile?.headline}
      />

      {/* 2. Progressive Getting Started Guide */}
      <GettingStartedSection
        profileCompleted={Boolean(user?.career_profile)}
        resumesUploaded={Boolean(summary && summary.evidence_sources_count > 0)}
        jobsAnalyzed={Boolean(summary && summary.analyzed_jobs_count > 0)}
        resumesOptimized={Boolean(summary && summary.optimized_resumes_count > 0)}
      />

      {/* 3. Core Modules & Feature Placeholders Grid */}
      <section aria-labelledby="platform-modules-heading" className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 id="platform-modules-heading" className="text-lg font-bold text-white tracking-tight">
              Platform Modules & Pipeline Status
            </h2>
            <p className="text-xs text-slate-400">
              Modular components representing each stage of the truth-first ATS optimization pipeline.
            </p>
          </div>

          <button
            onClick={fetchDashboardData}
            disabled={isLoading}
            className="inline-flex items-center space-x-1.5 text-xs text-indigo-400 hover:text-indigo-300 font-medium self-start sm:self-auto disabled:opacity-50"
            title="Refresh dashboard metrics"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} aria-hidden="true" />
            <span>Refresh Metrics</span>
          </button>
        </div>

        {isLoading && !summary ? (
          <div className="glass-panel p-12 rounded-2xl flex flex-col items-center justify-center space-y-3 border border-white/10">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-400" aria-hidden="true" />
            <span className="text-sm text-slate-400">Querying candidate career anchors & metrics...</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Module 2: Career Profile & Evidence */}
            <ProfileProgressCard summary={summary} />

            {/* Module 3: Resume Ingestion */}
            <ResumeStatusCard summary={summary} />

            {/* Module 4: Job Description Analysis */}
            <JobAnalysisCard summary={summary} />

            {/* Module 5: Matching Engine */}
            <MatchingCard summary={summary} />

            {/* Module 6: Truth-Validated Optimizer */}
            <OptimizationCard summary={summary} />

            {/* Module 7: Future Integration Slot */}
            <div className="glass-panel p-6 rounded-2xl border border-dashed border-white/10 flex flex-col justify-between opacity-80 hover:opacity-100 transition-opacity">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1">
                  Upcoming Module
                </span>
                <h3 className="text-base font-bold text-white mb-2">Automated Application Tracker</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Track submitted applications, submission dates, interview rounds, and version-specific tailored resumes in a unified Kanban pipeline.
                </p>
              </div>
              <div className="mt-6 pt-4 border-t border-white/5 text-[11px] text-slate-500 flex items-center justify-between">
                <span>Status: In Architectural Roadmap</span>
                <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono text-[10px]">
                  v1.2
                </span>
              </div>
            </div>
          </div>
        )}
      </section>

      {/* 4. Account Security & Session Overview */}
      <SecurityOverviewCard
        summary={summary}
        email={user?.email}
        lastLoginAt={user?.last_login_at}
      />
    </div>
  );
};
