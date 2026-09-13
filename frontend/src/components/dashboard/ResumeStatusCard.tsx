import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, UploadCloud, ArrowRight } from 'lucide-react';
import type { DashboardSummary } from '../../types/dashboard';

interface ResumeStatusCardProps {
  summary: DashboardSummary | null;
}

export const ResumeStatusCard: React.FC<ResumeStatusCardProps> = ({ summary }) => {
  const resumeCount = summary?.evidence_sources_count ?? 0;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col justify-between glass-panel-hover transition-all">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <FileText className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-400 block">
                Module 3 &bull; Ingestion
              </span>
              <h3 className="text-base font-bold text-white">Resume Ingestion Status</h3>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/30">
            {resumeCount} Ingested
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed mb-4">
          Import your existing PDF and DOCX master resumes. The system proposes structured claims and evidence items for your verification.
        </p>

        {/* Source-of-Truth Architectural Callout */}
        <div className="p-3 rounded-xl bg-slate-900/60 border border-emerald-500/20 mb-6 space-y-1.5">
          <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-300">
            <UploadCloud className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Candidate Review Gate</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-normal">
            AI-extracted resume content is strictly a draft proposal until verified by you into your Career Profile anchor.
          </p>
        </div>
      </div>

      <Link
        to="/app/resumes"
        className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-emerald-600 text-slate-200 hover:text-white font-semibold text-xs border border-white/10 hover:border-emerald-500/30 transition-all flex items-center justify-center space-x-2 group"
      >
        <span>Ingest Master Resume (PDF/DOCX)</span>
        <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" aria-hidden="true" />
      </Link>
    </div>
  );
};
