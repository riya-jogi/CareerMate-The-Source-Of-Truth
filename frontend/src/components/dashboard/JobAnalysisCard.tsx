import React from 'react';
import { Link } from 'react-router-dom';
import { Briefcase, ArrowRight, Tag, CheckCircle } from 'lucide-react';
import type { DashboardSummary } from '../../types/dashboard';

interface JobAnalysisCardProps {
  summary: DashboardSummary | null;
}

export const JobAnalysisCard: React.FC<JobAnalysisCardProps> = ({ summary }) => {
  const jobsCount = summary?.analyzed_jobs_count ?? 0;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col justify-between glass-panel-hover transition-all">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center">
              <Briefcase className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-400 block">
                Module 4 &bull; JD Analyzer
              </span>
              <h3 className="text-base font-bold text-white">Target Job Analysis</h3>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/30">
            {jobsCount} Target Sets
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed mb-4">
          Parse job descriptions to extract deterministic requirements, preferred attributes, and normalized tech stack taxonomy.
        </p>

        {/* Feature Highlights */}
        <div className="space-y-2 mb-6 text-xs">
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-white/5 flex items-center justify-between text-slate-300">
            <span className="flex items-center space-x-2">
              <Tag className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
              <span>Skill Terminology Normalization</span>
            </span>
            <span className="text-[10px] text-slate-500">K8s &rarr; Kubernetes</span>
          </div>

          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-white/5 flex items-center justify-between text-slate-300">
            <span className="flex items-center space-x-2">
              <CheckCircle className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
              <span>Required vs. Preferred Filtering</span>
            </span>
            <span className="text-[10px] text-slate-500">Explicit ATS Weights</span>
          </div>
        </div>
      </div>

      <Link
        to="/app/jobs"
        className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-amber-600 text-slate-200 hover:text-white font-semibold text-xs border border-white/10 hover:border-amber-500/30 transition-all flex items-center justify-center space-x-2 group"
      >
        <span>Analyze New Job Description</span>
        <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" aria-hidden="true" />
      </Link>
    </div>
  );
};
