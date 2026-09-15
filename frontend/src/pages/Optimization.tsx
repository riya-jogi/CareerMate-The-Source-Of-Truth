import React, { useEffect, useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Download,
  Edit3,
  FileText,
  Loader2,
  RefreshCw,
  ShieldCheck,
  Wand2,
  XCircle,
} from 'lucide-react';
import { jobsApi } from '../api/jobs';
import { optimizationApi } from '../api/optimization';
import { getAccessToken } from '../api/client';
import type { Job } from '../types/job';
import type { ApprovalDecision, ResumeChange, ResumeVersion } from '../types/optimization';

// ─── Change card ───────────────────────────────────────────────────────────────

interface ChangeCardProps {
  change: ResumeChange;
  onDecide: (changeId: string, decision: ApprovalDecision, editedText?: string, comment?: string) => Promise<void>;
}

const ChangeCard: React.FC<ChangeCardProps> = ({ change, onDecide }) => {
  const [deciding, setDeciding] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [editedText, setEditedText] = useState(change.proposed_content);
  const [comment, setComment] = useState('');
  const [expanded, setExpanded] = useState(false);

  const decide = async (decision: ApprovalDecision, text?: string) => {
    try {
      setDeciding(true);
      await onDecide(change.id, decision, text, comment || undefined);
    } finally {
      setDeciding(false);
      setEditMode(false);
    }
  };

  const currentDecision = change.approval?.decision;

  const decisionStyle = (d: ApprovalDecision | undefined) => {
    if (d === 'approved') return 'border-emerald-500/40 bg-emerald-500/8';
    if (d === 'rejected') return 'border-rose-500/40 bg-rose-500/8';
    if (d === 'edited') return 'border-amber-500/40 bg-amber-500/8';
    return 'border-white/10 bg-white/5';
  };

  const riskBadge = (risk: string) => {
    if (risk === 'high') return 'bg-rose-500/15 text-rose-300 border border-rose-500/30';
    if (risk === 'medium') return 'bg-amber-500/15 text-amber-300 border border-amber-500/30';
    return 'bg-slate-500/15 text-slate-300 border border-slate-500/30';
  };

  return (
    <div className={`rounded-2xl border p-5 transition-all ${decisionStyle(currentDecision)}`}>
      {/* Header row */}
      <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-[10px] uppercase tracking-wider font-bold text-indigo-400">
            {change.change_type}
          </span>
          <span className="text-[10px] uppercase text-slate-500 px-1.5 py-0.5 rounded bg-slate-800">
            {change.section}
          </span>
          <span className={`text-[10px] uppercase px-1.5 py-0.5 rounded font-medium ${riskBadge(change.risk_level)}`}>
            {change.risk_level} risk
          </span>
        </div>
        {currentDecision && (
          <span
            className={`text-[10px] uppercase font-bold px-2 py-1 rounded-full ${
              currentDecision === 'approved'
                ? 'bg-emerald-500/20 text-emerald-300'
                : currentDecision === 'rejected'
                  ? 'bg-rose-500/20 text-rose-300'
                  : 'bg-amber-500/20 text-amber-300'
            }`}
          >
            {currentDecision}
          </span>
        )}
      </div>

      {/* Reason */}
      <p className="text-sm text-slate-300 mb-3">{change.reason}</p>

      {/* Original → Proposed diff */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 mb-3"
      >
        {expanded ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
        {expanded ? 'Hide diff' : 'Show diff'}
      </button>

      {expanded && (
        <div className="space-y-2 mb-4">
          {change.original_content && (
            <div className="p-3 rounded-xl bg-rose-500/8 border border-rose-500/20">
              <p className="text-[10px] uppercase text-rose-400 font-bold mb-1">Original</p>
              <p className="text-sm text-rose-100 whitespace-pre-wrap leading-relaxed">{change.original_content}</p>
            </div>
          )}
          <div className="p-3 rounded-xl bg-emerald-500/8 border border-emerald-500/20">
            <p className="text-[10px] uppercase text-emerald-400 font-bold mb-1">Proposed</p>
            {editMode ? (
              <textarea
                value={editedText}
                onChange={(e) => setEditedText(e.target.value)}
                rows={4}
                className="w-full input-field resize-y text-sm"
              />
            ) : (
              <p className="text-sm text-emerald-100 whitespace-pre-wrap leading-relaxed">{change.proposed_content}</p>
            )}
          </div>
        </div>
      )}

      {/* Edit comment */}
      {editMode && (
        <textarea
          placeholder="Optional note for your decision..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          rows={2}
          className="w-full input-field resize-none text-sm mb-3"
        />
      )}

      {/* Action buttons */}
      {!currentDecision && (
        <div className="flex flex-wrap gap-2 mt-1">
          <button
            disabled={deciding}
            onClick={() => decide('approved')}
            className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-200 text-sm hover:bg-emerald-500/25 disabled:opacity-50"
          >
            {deciding ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <CheckCircle2 className="w-3.5 h-3.5" />}
            Approve
          </button>

          <button
            disabled={deciding}
            onClick={() => {
              if (editMode) {
                void decide('edited', editedText);
              } else {
                setEditMode(true);
                setExpanded(true);
              }
            }}
            className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-500/15 border border-amber-500/30 text-amber-200 text-sm hover:bg-amber-500/25 disabled:opacity-50"
          >
            <Edit3 className="w-3.5 h-3.5" />
            {editMode ? 'Confirm edit' : 'Edit & approve'}
          </button>

          <button
            disabled={deciding}
            onClick={() => decide('rejected')}
            className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-200 text-sm hover:bg-rose-500/25 disabled:opacity-50"
          >
            <XCircle className="w-3.5 h-3.5" />
            Reject
          </button>

          {editMode && (
            <button
              onClick={() => { setEditMode(false); setEditedText(change.proposed_content); }}
              className="text-xs text-slate-400 hover:text-slate-200 px-2"
            >
              Cancel
            </button>
          )}
        </div>
      )}
    </div>
  );
};

// ─── Main Optimization page ────────────────────────────────────────────────────

/**
 * Downloads a generated resume file using an authenticated fetch so the
 * Bearer token is included. Plain <a href> would not send the token and
 * the backend would return a 401 JSON error saved as "download.json".
 */
async function downloadFile(versionId: string, format: 'pdf' | 'docx'): Promise<void> {
  const token = getAccessToken();
  const url = optimizationApi.downloadUrl(versionId, format);
  const response = await fetch(url, {
    credentials: 'include',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new Error(data?.error?.message || `Download failed (${response.status})`);
  }
  const blob = await response.blob();
  const objectUrl = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = objectUrl;
  anchor.download = `resume.${format}`;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(objectUrl);
}

export const Optimization: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState('');
  const [version, setVersion] = useState<ResumeVersion | null>(null);
  const [loadingJobs, setLoadingJobs] = useState(true);
  const [optimizing, setOptimizing] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [downloading, setDownloading] = useState<'pdf' | 'docx' | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  // Load analyzed jobs on mount
  useEffect(() => {
    void (async () => {
      try {
        setLoadingJobs(true);
        const data = await jobsApi.list();
        const analyzed = data.filter((j) => j.analysis_status === 'completed');
        setJobs(analyzed);
        if (analyzed.length) setSelectedJobId(analyzed[0].id);
      } catch (err: any) {
        setError(err.message || 'Unable to load analyzed jobs.');
      } finally {
        setLoadingJobs(false);
      }
    })();
  }, []);

  // When job changes, try to load existing optimization
  useEffect(() => {
    if (!selectedJobId) { setVersion(null); return; }
    void (async () => {
      try {
        const v = await optimizationApi.getOptimization(selectedJobId);
        setVersion(v);
      } catch {
        setVersion(null);
      }
    })();
  }, [selectedJobId]);

  const runOptimize = async () => {
    if (!selectedJobId) return;
    setOptimizing(true); setError(null); setMessage(null);
    try {
      const v = await optimizationApi.optimize(selectedJobId);
      setVersion(v);
      setMessage(`Optimization generated — ${v.changes.length} proposed change${v.changes.length !== 1 ? 's' : ''} ready for your review.`);
    } catch (err: any) {
      setError(err.message || 'Unable to generate optimization.');
    } finally {
      setOptimizing(false);
    }
  };

  const handleDecide = async (changeId: string, decision: ApprovalDecision, editedText?: string, comment?: string) => {
    setError(null);
    await optimizationApi.decideChange(changeId, decision, editedText, comment);
    // Refresh version to reflect updated approval state
    if (selectedJobId) {
      const v = await optimizationApi.getOptimization(selectedJobId);
      setVersion(v);
    }
  };

  const handleGenerate = async (format: 'pdf' | 'docx') => {
    if (!selectedJobId) return;
    setGenerating(true); setError(null); setMessage(null);
    try {
      const v = await optimizationApi.generate(selectedJobId, format);
      setVersion(v);
      // Immediately trigger the authenticated download so the user gets the file right away
      try {
        await downloadFile(v.id, format);
        setMessage(`Resume generated and downloaded as ${format.toUpperCase()}.`);
      } catch {
        setMessage(`Resume generated! Click "Download ${format.toUpperCase()}" below.`);
      }
    } catch (err: any) {
      setError(err.message || 'Unable to generate resume. Make sure all changes have been reviewed.');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async (format: 'pdf' | 'docx') => {
    if (!version) return;
    setDownloading(format); setError(null);
    try {
      await downloadFile(version.id, format);
    } catch (err: any) {
      setError(err.message || `Unable to download ${format.toUpperCase()}.`);
    } finally {
      setDownloading(null);
    }
  };

  const pendingChanges = version?.changes.filter((c) => !c.approval).length ?? 0;
  const allReviewed = version ? pendingChanges === 0 : false;
  const isReady = version?.status === 'ready';
  const hasApprovedChanges = version?.changes.some((c) => c.approval?.decision !== 'rejected') ?? false;
  const selectedJob = jobs.find((j) => j.id === selectedJobId);

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div>
        <p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Module 6 & 7: Optimizer & Generator</p>
        <h1 className="text-3xl font-bold text-white mt-2">Resume Optimization</h1>
        <p className="text-slate-400 mt-2">
          Generate a job-tailored resume exclusively from your verified career claims. Review every AI suggestion before it's final.
        </p>
      </div>

      {/* Alert banner */}
      {(error || message) && (
        <div
          role="alert"
          className={`p-4 rounded-xl border text-sm flex items-start gap-3 ${
            error
              ? 'border-rose-500/30 bg-rose-500/10 text-rose-200'
              : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'
          }`}
        >
          {error ? <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" /> : <CheckCircle2 className="w-4 h-4 mt-0.5 shrink-0" />}
          {error || message}
        </div>
      )}

      {/* Job selector + trigger */}
      <section className="glass-panel p-6 rounded-2xl border border-white/10">
        <div className="flex flex-col md:flex-row md:items-end gap-4">
          <label className="flex-1 space-y-2 text-sm text-slate-300">
            <span>Select an analyzed job</span>
            <select
              value={selectedJobId}
              onChange={(e) => setSelectedJobId(e.target.value)}
              className="input-field w-full"
              disabled={loadingJobs}
            >
              <option value="">Choose a job…</option>
              {jobs.map((job) => (
                <option key={job.id} value={job.id}>
                  {job.title || 'Untitled role'}{job.company_name ? ` · ${job.company_name}` : ''}
                </option>
              ))}
            </select>
          </label>

          <button
            disabled={!selectedJobId || optimizing || loadingJobs}
            onClick={() => void runOptimize()}
            className="btn-primary inline-flex items-center gap-2"
          >
            {optimizing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Wand2 className="w-4 h-4" />}
            {optimizing ? 'Optimizing…' : version ? 'Re-optimize' : 'Optimize resume'}
          </button>
        </div>

        {!loadingJobs && jobs.length === 0 && (
          <p className="text-sm text-slate-400 mt-4">
            Analyze a job description first, then return here to optimize your resume.
          </p>
        )}
      </section>

      {/* Truth firewall notice */}
      <div className="flex items-start gap-3 p-4 rounded-2xl bg-indigo-500/8 border border-indigo-500/20 text-sm text-slate-300">
        <ShieldCheck className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold text-white">Truth Firewall active</p>
          <p className="text-slate-400 text-xs mt-1">
            All proposed changes reference verified candidate claims only. No hallucination or fabricated experience can pass through.
          </p>
        </div>
      </div>

      {/* Optimization results */}
      {version && (
        <>
          {/* Version summary */}
          <section className="grid md:grid-cols-4 gap-4">
            <div className="glass-panel p-5 rounded-2xl border border-indigo-500/20">
              <p className="text-xs uppercase tracking-wider text-slate-400">Version</p>
              <p className="text-3xl font-bold text-white mt-2">v{version.version_number}</p>
              <p className="text-xs text-slate-500 mt-1">{version.template}</p>
            </div>
            <div className="glass-panel p-5 rounded-2xl border border-white/10">
              <p className="text-xs uppercase tracking-wider text-slate-400">Total changes</p>
              <p className="text-3xl font-bold text-white mt-2">{version.changes.length}</p>
            </div>
            <div className="glass-panel p-5 rounded-2xl border border-white/10">
              <p className="text-xs uppercase tracking-wider text-slate-400">Pending review</p>
              <p className={`text-3xl font-bold mt-2 ${pendingChanges > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
                {pendingChanges}
              </p>
            </div>
            <div className="glass-panel p-5 rounded-2xl border border-white/10">
              <p className="text-xs uppercase tracking-wider text-slate-400">Status</p>
              <p className="text-sm font-semibold text-white mt-3">{version.status.replace(/_/g, ' ')}</p>
              <p className="text-xs text-slate-500 mt-1">{version.validation_status}</p>
            </div>
          </section>

          {/* Changes review list */}
          {version.changes.length === 0 ? (
            <div className="glass-panel p-8 rounded-2xl border border-white/10 text-center">
              <FileText className="w-10 h-10 text-slate-600 mx-auto mb-3" />
              <p className="text-slate-400">No proposed changes were generated.</p>
              <p className="text-xs text-slate-500 mt-2">
                This may mean your profile already covers all job requirements. Try adding more experiences or skills.
              </p>
            </div>
          ) : (
            <section className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-white">Proposed changes</h2>
                {allReviewed && (
                  <span className="text-xs text-emerald-400 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" /> All reviewed
                  </span>
                )}
              </div>
              {version.changes.map((change) => (
                <ChangeCard key={change.id} change={change} onDecide={handleDecide} />
              ))}
            </section>
          )}

          {/* Generate / Download section */}
          <section className="glass-panel p-6 rounded-2xl border border-white/10">
            <h2 className="text-lg font-semibold text-white mb-4">Generate & Download</h2>

            {!allReviewed && (
              <div className="flex items-start gap-3 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-sm mb-5">
                <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
                Review all {pendingChanges} pending change{pendingChanges !== 1 ? 's' : ''} before generating the final resume.
              </div>
            )}

            <div className="flex flex-wrap gap-3">
              <button
                disabled={!allReviewed || !hasApprovedChanges || generating}
                onClick={() => void handleGenerate('pdf')}
                className="btn-primary inline-flex items-center gap-2 disabled:opacity-50"
              >
                {generating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                {generating ? 'Generating…' : 'Generate PDF'}
              </button>

              <button
                disabled={!allReviewed || !hasApprovedChanges || generating}
                onClick={() => void handleGenerate('docx')}
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/15 bg-white/5 text-slate-200 text-sm hover:bg-white/10 disabled:opacity-50"
              >
                <Download className="w-4 h-4" />
                Generate DOCX
              </button>

              {isReady && version.pdf_key && (
                <button
                  disabled={downloading === 'pdf'}
                  onClick={() => void handleDownload('pdf')}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-emerald-500/30 bg-emerald-500/15 text-emerald-200 text-sm hover:bg-emerald-500/25 disabled:opacity-50"
                >
                  {downloading === 'pdf' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                  {downloading === 'pdf' ? 'Downloading…' : 'Download PDF'}
                </button>
              )}

              {isReady && version.docx_key && (
                <button
                  disabled={downloading === 'docx'}
                  onClick={() => void handleDownload('docx')}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-emerald-500/30 bg-emerald-500/15 text-emerald-200 text-sm hover:bg-emerald-500/25 disabled:opacity-50"
                >
                  {downloading === 'docx' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                  {downloading === 'docx' ? 'Downloading…' : 'Download DOCX'}
                </button>
              )}

              {version && (
                <button
                  onClick={() => void runOptimize()}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/15 bg-white/5 text-slate-300 text-sm hover:bg-white/10"
                >
                  <RefreshCw className="w-4 h-4" />
                  Re-generate optimization
                </button>
              )}
            </div>

            {selectedJob && (
              <p className="text-xs text-slate-500 mt-4">
                Target: <span className="text-slate-300">{selectedJob.title || 'Untitled role'}</span>
                {selectedJob.company_name && <span className="text-slate-400"> · {selectedJob.company_name}</span>}
              </p>
            )}
          </section>
        </>
      )}
    </div>
  );
};
