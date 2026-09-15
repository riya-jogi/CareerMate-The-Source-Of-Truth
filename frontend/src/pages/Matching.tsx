import React, { useEffect, useState } from 'react';
import { AlertTriangle, CheckCircle2, GitCompare, Loader2, RefreshCw, HelpCircle } from 'lucide-react';
import { jobsApi } from '../api/jobs';
import { matchingApi } from '../api/matching';
import type { Job } from '../types/job';
import type { CandidateJobMatch, MatchDetail } from '../types/matching';

export const Matching: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState('');
  const [match, setMatch] = useState<CandidateJobMatch | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadJobs = async () => {
    try { setLoading(true); const data = await jobsApi.list(); const analyzed = data.filter((job) => job.analysis_status === 'completed'); setJobs(analyzed); if (!selectedJobId && analyzed.length) setSelectedJobId(analyzed[0].id); }
    catch (err: any) { setError(err.message || 'Unable to load analyzed jobs.'); }
    finally { setLoading(false); }
  };
  useEffect(() => { void loadJobs(); }, []);

  const runMatch = async () => {
    if (!selectedJobId) return;
    try { setRunning(true); setError(null); setMatch(await matchingApi.run(selectedJobId)); }
    catch (err: any) { setError(err.message || 'Unable to match your profile to this job.'); }
    finally { setRunning(false); }
  };

  const grouped = (type: MatchDetail['match_type']) => match?.details.filter((detail) => detail.match_type === type) || [];
  const tone = (type: MatchDetail['match_type']) => type === 'strong_match' ? 'border-emerald-500/30 bg-emerald-500/10' : type === 'partial_match' ? 'border-amber-500/30 bg-amber-500/10' : type === 'gap' ? 'border-rose-500/30 bg-rose-500/10' : 'border-slate-500/30 bg-slate-500/10';
  const label = (type: MatchDetail['match_type']) => type === 'strong_match' ? 'Strong matches' : type === 'partial_match' ? 'Partial matches' : type === 'gap' ? 'Gaps' : 'Unknowns';

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <div><p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Module 5: Matching & Gap Analysis</p><h1 className="text-3xl font-bold text-white mt-2">Candidate-job matching</h1><p className="text-slate-400 mt-2">Compare supported career claims with analyzed requirements. Similarity never overrides evidence or experience context.</p></div>
      {error && <div role="alert" className="p-3 rounded-xl border border-rose-500/30 bg-rose-500/10 text-sm text-rose-200">{error}</div>}
      <section className="glass-panel p-6 rounded-2xl border border-white/10"><div className="flex flex-col md:flex-row md:items-end gap-4"><label className="flex-1 space-y-2 text-sm text-slate-300"><span>Select an analyzed job</span><select value={selectedJobId} onChange={(event) => setSelectedJobId(event.target.value)} className="input-field w-full"><option value="">Choose a job</option>{jobs.map((job) => <option key={job.id} value={job.id}>{job.title || 'Untitled role'}{job.company_name ? ` · ${job.company_name}` : ''}</option>)}</select></label><button disabled={!selectedJobId || running || loading} onClick={() => void runMatch()} className="btn-primary inline-flex items-center gap-2">{running ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}{running ? 'Matching...' : 'Run match'}</button></div>{!loading && jobs.length === 0 && <p className="text-sm text-slate-400 mt-4">Analyze a job description first, then return here to compare it with your career profile.</p>}</section>
      {match && <><section className="grid md:grid-cols-4 gap-4"><div className="glass-panel p-5 rounded-2xl border border-indigo-500/20"><p className="text-xs uppercase tracking-wider text-slate-400">Job alignment</p><p className="text-3xl font-bold text-white mt-2">{match.overall_score.toFixed(1)}<span className="text-base text-slate-400">/100</span></p></div><div className="glass-panel p-5 rounded-2xl border border-white/10"><p className="text-xs uppercase tracking-wider text-slate-400">Profile coverage</p><p className="text-3xl font-bold text-white mt-2">{match.profile_coverage.toFixed(0)}<span className="text-base text-slate-400">%</span></p></div><div className="glass-panel p-5 rounded-2xl border border-white/10"><p className="text-xs uppercase tracking-wider text-slate-400">Required</p><p className="text-3xl font-bold text-white mt-2">{match.required_score == null ? '—' : match.required_score.toFixed(1)}</p></div><div className="glass-panel p-5 rounded-2xl border border-white/10"><p className="text-xs uppercase tracking-wider text-slate-400">Status</p><p className="text-sm font-semibold text-white mt-3">{match.analysis_status.replaceAll('_', ' ')}</p><p className="text-xs text-slate-500 mt-1">{match.algorithm_version}</p></div></section>{match.critical_gaps.length > 0 && <section className="p-5 rounded-2xl border border-rose-500/30 bg-rose-500/10"><div className="flex gap-3"><AlertTriangle className="w-5 h-5 text-rose-300 shrink-0" /><div><h2 className="font-semibold text-rose-100">Critical gaps</h2><ul className="mt-2 space-y-1 text-sm text-rose-200">{match.critical_gaps.map((gap) => <li key={gap}>{gap}</li>)}</ul></div></div></section>}<section className="space-y-4">{(['strong_match', 'partial_match', 'gap', 'unknown'] as const).map((type) => <div key={type} className={`rounded-2xl border p-5 ${tone(type)}`}><div className="flex items-center gap-2 mb-3">{type === 'strong_match' ? <CheckCircle2 className="w-5 h-5 text-emerald-300" /> : type === 'unknown' ? <HelpCircle className="w-5 h-5 text-slate-300" /> : <GitCompare className="w-5 h-5 text-amber-200" />}<h2 className="font-semibold text-white">{label(type)}</h2><span className="text-xs text-slate-400">{grouped(type).length}</span></div>{grouped(type).length === 0 ? <p className="text-sm text-slate-400">None</p> : <div className="space-y-3">{grouped(type).map((detail) => <div key={detail.id} className="p-4 rounded-xl bg-black/10 border border-white/10"><div className="flex justify-between gap-3"><span className="text-white font-medium">Requirement</span><span className="text-xs text-slate-400">{detail.score.toFixed(0)}/100</span></div><p className="text-sm text-slate-300 mt-2">{detail.explanation}</p>{detail.gap_category && <p className="text-xs uppercase tracking-wider text-slate-500 mt-2">{detail.gap_category.replaceAll('_', ' ')}</p>}</div>)}</div>}</div>)}</section></>}
    </div>
  );
};