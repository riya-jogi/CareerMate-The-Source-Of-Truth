import React from 'react';
import { Sparkles, CheckCircle2, ShieldCheck } from 'lucide-react';
import type { DashboardSummary } from '../../types/dashboard';

interface WelcomeSectionProps {
  summary: DashboardSummary | null;
  fallbackName?: string;
  fallbackHeadline?: string | null;
}

export const WelcomeSection: React.FC<WelcomeSectionProps> = ({
  summary,
  fallbackName = 'Candidate',
  fallbackHeadline,
}) => {
  const name = summary?.candidate_name || fallbackName;
  const headline =
    summary?.candidate_headline ||
    fallbackHeadline ||
    'Your verified career anchor is active. Build truth-validated resumes customized for every opportunity.';

  return (
    <section aria-labelledby="dashboard-welcome-heading">
      <div className="glass-panel p-6 sm:p-8 rounded-2xl relative overflow-hidden border border-white/10 shadow-2xl">
        {/* Ambient radial glow */}
        <div
          className="ambient-glow bg-indigo-600/20 w-96 h-96 -top-24 -right-24 pointer-events-none"
          aria-hidden="true"
        />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-xs uppercase tracking-wider">
              <Sparkles className="w-4 h-4" aria-hidden="true" />
              <span>AI Candidate ATS &bull; Truth-Validated Optimization</span>
            </div>

            <h1
              id="dashboard-welcome-heading"
              className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight"
            >
              Welcome back, {name}
            </h1>

            <p className="text-slate-300 text-sm max-w-2xl leading-relaxed">
              {headline}
            </p>

            <div className="pt-2 flex flex-wrap items-center gap-3 text-xs text-slate-400">
              <div className="inline-flex items-center space-x-1.5 py-1 px-2.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-300">
                <ShieldCheck className="w-3.5 h-3.5" aria-hidden="true" />
                <span>Candidate Data is the Source of Truth</span>
              </div>
              <span className="hidden sm:inline text-slate-600">&bull;</span>
              <span>Deterministic Rule Verification</span>
              <span className="hidden sm:inline text-slate-600">&bull;</span>
              <span>Zero Unanchored Hallucinations</span>
            </div>
          </div>

          <div className="shrink-0 flex items-center">
            <div className="p-4 rounded-xl bg-slate-900/90 border border-emerald-500/30 flex items-center space-x-3.5 shadow-lg">
              <div
                className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0"
                aria-hidden="true"
              >
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <div>
                <div className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                  Career Anchor Status
                </div>
                <div className="text-sm font-bold text-white flex items-center space-x-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span>Verified Anchor Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
