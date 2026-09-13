import React from 'react';
import { Link } from 'react-router-dom';
import { UserCheck, ShieldCheck, FileCheck, ArrowRight } from 'lucide-react';
import type { DashboardSummary } from '../../types/dashboard';

interface ProfileProgressCardProps {
  summary: DashboardSummary | null;
}

export const ProfileProgressCard: React.FC<ProfileProgressCardProps> = ({ summary }) => {
  const completeness = summary?.profile_completeness_percentage ?? 25;
  const claimsCount = summary?.career_claims_count ?? 0;
  const evidenceCount = summary?.evidence_sources_count ?? 0;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col justify-between glass-panel-hover transition-all">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
              <UserCheck className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-400 block">
                Module 2 &bull; Core Anchor
              </span>
              <h3 className="text-base font-bold text-white">Career Profile Progress</h3>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-extrabold border border-indigo-500/30">
            {completeness}% Complete
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed mb-4">
          Your Career Profile is the single persistent source of truth. Factual claims anchored here drive all future resume proposals.
        </p>

        {/* Progress Bar */}
        <div className="space-y-1.5 mb-5">
          <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-white/5">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 to-emerald-400 transition-all duration-500"
              style={{ width: `${completeness}%` }}
              role="progressbar"
              aria-valuenow={completeness}
              aria-valuemin={0}
              aria-valuemax={100}
            />
          </div>
          <div className="flex justify-between text-[11px] text-slate-500">
            <span>Identity & Headline Established</span>
            <span>{completeness >= 80 ? 'Comprehensive' : 'Anchor Expanding'}</span>
          </div>
        </div>

        {/* Anchored Sub-Metrics */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          <div className="p-3 rounded-xl bg-slate-900/60 border border-white/5 flex items-center space-x-2.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" aria-hidden="true" />
            <div>
              <div className="text-base font-bold text-white">{claimsCount}</div>
              <div className="text-[11px] text-slate-400">Verified Claims</div>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/60 border border-white/5 flex items-center space-x-2.5">
            <FileCheck className="w-4 h-4 text-indigo-400 shrink-0" aria-hidden="true" />
            <div>
              <div className="text-base font-bold text-white">{evidenceCount}</div>
              <div className="text-[11px] text-slate-400">Evidence Proofs</div>
            </div>
          </div>
        </div>
      </div>

      <Link
        to="/app/profile"
        className="w-full py-2.5 px-4 rounded-xl bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white font-semibold text-xs border border-indigo-500/30 transition-all flex items-center justify-center space-x-2 group"
      >
        <span>Maintain Career Profile & Claims</span>
        <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" aria-hidden="true" />
      </Link>
    </div>
  );
};
