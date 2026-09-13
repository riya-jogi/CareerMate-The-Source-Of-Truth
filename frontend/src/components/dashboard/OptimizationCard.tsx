import React from 'react';
import { Link } from 'react-router-dom';
import { Wand2, ArrowRight, ShieldCheck } from 'lucide-react';
import type { DashboardSummary } from '../../types/dashboard';

interface OptimizationCardProps {
  summary: DashboardSummary | null;
}

export const OptimizationCard: React.FC<OptimizationCardProps> = ({ summary }) => {
  const optimizedCount = summary?.optimized_resumes_count ?? 0;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col justify-between glass-panel-hover transition-all">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center">
              <Wand2 className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-cyan-400 block">
                Module 6 &bull; Optimizer
              </span>
              <h3 className="text-base font-bold text-white">Truth-Validated Optimizer</h3>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-semibold border border-cyan-500/30">
            {optimizedCount} Generated
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed mb-4">
          Generate targeted, ATS-tailored resumes strictly anchored to your verified CareerProfile claims. Every bullet point is mathematically verifiable.
        </p>

        {/* Anti-Hallucination Guarantee */}
        <div className="p-3 rounded-xl bg-slate-900/60 border border-cyan-500/20 mb-6 flex items-start space-x-3">
          <ShieldCheck className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" aria-hidden="true" />
          <div className="text-xs">
            <span className="font-semibold text-cyan-300 block">Anti-Fabrication Guarantee</span>
            <span className="text-slate-400 text-[11px] leading-tight">
              AI-generated content is an exported artifact, never the source of truth. Zero fabricated claims are permitted.
            </span>
          </div>
        </div>
      </div>

      <Link
        to="/app/optimization"
        className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-cyan-600 text-slate-200 hover:text-white font-semibold text-xs border border-white/10 hover:border-cyan-500/30 transition-all flex items-center justify-center space-x-2 group"
      >
        <span>Generate Truth-Validated Resume</span>
        <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" aria-hidden="true" />
      </Link>
    </div>
  );
};
