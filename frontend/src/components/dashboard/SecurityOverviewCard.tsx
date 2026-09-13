import React from 'react';
import { Link } from 'react-router-dom';
import { Lock, Clock, ShieldCheck, ArrowRight } from 'lucide-react';
import type { DashboardSummary } from '../../types/dashboard';

interface SecurityOverviewCardProps {
  summary: DashboardSummary | null;
  email?: string;
  lastLoginAt?: string | null;
}

export const SecurityOverviewCard: React.FC<SecurityOverviewCardProps> = ({
  summary,
  email,
  lastLoginAt,
}) => {
  const accountEmail = summary?.candidate_email || email;
  const loginTimestamp = summary?.last_login_at || lastLoginAt;

  const formattedDate = loginTimestamp
    ? new Date(loginTimestamp).toLocaleString(undefined, {
        dateStyle: 'medium',
        timeStyle: 'short',
      })
    : 'Current Active Session';

  return (
    <section aria-labelledby="security-overview-heading">
      <div className="glass-panel p-6 rounded-2xl border border-white/10">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
              <Lock className="w-4 h-4" aria-hidden="true" />
            </div>
            <div>
              <h2 id="security-overview-heading" className="text-sm font-bold text-white">
                Account Security & Session Guard
              </h2>
              <p className="text-[11px] text-slate-400">
                Stateless JWT authorization paired with secure, rotated HttpOnly refresh cookies.
              </p>
            </div>
          </div>

          <Link
            to="/app/settings"
            className="inline-flex items-center space-x-1 text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
          >
            <span>Manage Security Settings</span>
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
            <span className="text-slate-500 uppercase tracking-wider font-semibold block mb-1">
              Candidate Account Email
            </span>
            <span className="text-white font-medium truncate block">{accountEmail}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
            <span className="text-slate-500 uppercase tracking-wider font-semibold block mb-1">
              Last Login Verification
            </span>
            <div className="flex items-center space-x-1.5 text-slate-300">
              <Clock className="w-3.5 h-3.5 text-indigo-400 shrink-0" aria-hidden="true" />
              <span>{formattedDate}</span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5">
            <span className="text-slate-500 uppercase tracking-wider font-semibold block mb-1">
              Token Protection Policy
            </span>
            <div className="flex items-center space-x-1.5 text-emerald-400 font-medium">
              <ShieldCheck className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
              <span>HttpOnly &bull; SHA-256 Revocable</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
