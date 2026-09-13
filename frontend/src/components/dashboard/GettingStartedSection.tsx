import React from 'react';
import { Link } from 'react-router-dom';
import {
  CheckCircle2,
  CircleDot,
  ArrowRight,
} from 'lucide-react';
import type { GettingStartedStep } from '../../types/dashboard';

interface GettingStartedSectionProps {
  profileCompleted: boolean;
  resumesUploaded: boolean;
  jobsAnalyzed: boolean;
  resumesOptimized: boolean;
}

export const GettingStartedSection: React.FC<GettingStartedSectionProps> = ({
  profileCompleted = true,
  resumesUploaded = false,
  jobsAnalyzed = false,
  resumesOptimized = false,
}) => {
  const steps: GettingStartedStep[] = [
    {
      id: 'step-1',
      stepNumber: 1,
      title: 'Anchor Your Verified Profile',
      description: 'Your CareerProfile and credentials serve as the single source of truth for all claims.',
      actionText: 'Review Profile Anchor',
      link: '/app/profile',
      completed: profileCompleted,
      badge: 'Anchor Active',
    },
    {
      id: 'step-2',
      stepNumber: 2,
      title: 'Ingest Existing Master Resumes',
      description: 'Import your PDF or DOCX resumes to extract structured proposals and supporting evidence items.',
      actionText: 'Upload Master Resume',
      link: '/app/resumes',
      completed: resumesUploaded,
      badge: resumesUploaded ? 'Completed' : 'Recommended Next',
    },
    {
      id: 'step-3',
      stepNumber: 3,
      title: 'Analyze Target Job Descriptions',
      description: 'Paste job postings to parse required vs. preferred criteria and normalize skill terminology.',
      actionText: 'Paste Job Posting',
      link: '/app/jobs',
      completed: jobsAnalyzed,
      badge: jobsAnalyzed ? 'Completed' : 'Pending',
    },
    {
      id: 'step-4',
      stepNumber: 4,
      title: 'Validate Match & Generate Resumes',
      description: 'Evaluate transparent compatibility scores and export tailored resumes with 100% verifiable claims.',
      actionText: 'Run Optimization',
      link: '/app/optimization',
      completed: resumesOptimized,
      badge: resumesOptimized ? 'Completed' : 'Final Step',
    },
  ];

  return (
    <section aria-labelledby="getting-started-heading" className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 id="getting-started-heading" className="text-lg font-bold text-white tracking-tight">
            Getting Started: The 4-Step Truth-First Workflow
          </h2>
          <p className="text-xs text-slate-400">
            Progress through the candidate-controlled pipeline to anchor evidence and optimize resumes safely.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {steps.map((step) => {
          return (
            <div
              key={step.id}
              className={`glass-panel p-5 rounded-2xl border transition-all flex flex-col justify-between ${
                step.completed
                  ? 'border-emerald-500/30 bg-emerald-950/10'
                  : 'border-white/10 hover:border-indigo-500/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="w-6 h-6 rounded-full bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center border border-white/10">
                      {step.stepNumber}
                    </span>
                    <span
                      className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                        step.completed
                          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                          : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      }`}
                    >
                      {step.badge}
                    </span>
                  </div>

                  {step.completed ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" aria-hidden="true" />
                  ) : (
                    <CircleDot className="w-4 h-4 text-slate-500" aria-hidden="true" />
                  )}
                </div>

                <h3 className="text-sm font-bold text-white mb-1.5">{step.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed mb-4">
                  {step.description}
                </p>
              </div>

              <Link
                to={step.link}
                className={`w-full py-2 px-3 rounded-xl text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors ${
                  step.completed
                    ? 'bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-glow-brand'
                }`}
              >
                <span>{step.actionText}</span>
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
            </div>
          );
        })}
      </div>
    </section>
  );
};
