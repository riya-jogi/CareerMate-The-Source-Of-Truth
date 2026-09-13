import React from 'react';
import { Link } from 'react-router-dom';
import { GitCompare, ArrowRight } from 'lucide-react';
import type { DashboardSummary } from '../../types/dashboard';

interface MatchingCardProps {
  summary: DashboardSummary | null;
}

export const MatchingCard: React.FC<MatchingCardProps> = ({ summary }) => {
  const matchCount = summary?.target_matches_count ?? 0;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col justify-between glass-panel-hover transition-all">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-violet-500/10 text-violet-400 flex items-center justify-center">
              <GitCompare className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-violet-400 block">
                Module 5 &bull; Match Engine
              </span>
              <h3 className="text-base font-bold text-white">Candidate-Job Compatibility</h3>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-violet-500/20 text-violet-300 text-xs font-semibold border border-violet-500/30">
            {matchCount} Evaluated
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed mb-4">
          Multi-layer compatibility evaluation combining deterministic exact matches, normalized terminology, and vector semantic similarity.
        </p>

        {/* 3-Tier Match Preview */}
        <div className="grid grid-cols-3 gap-2 mb-6 text-center text-xs">
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-white/5">
            <div className="text-white font-bold">Exact</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Strict Keyword</div>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-white/5">
            <div className="text-white font-bold">Normalized</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Synonym Map</div>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-white/5">
            <div className="text-white font-bold">Semantic</div>
            <div className="text-[10px] text-slate-500 mt-0.5">pgvector Match</div>
          </div>
        </div>
      </div>

      <Link
        to="/app/matching"
        className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-violet-600 text-slate-200 hover:text-white font-semibold text-xs border border-white/10 hover:border-violet-500/30 transition-all flex items-center justify-center space-x-2 group"
      >
        <span>Evaluate Match Compatibility</span>
        <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" aria-hidden="true" />
      </Link>
    </div>
  );
};
