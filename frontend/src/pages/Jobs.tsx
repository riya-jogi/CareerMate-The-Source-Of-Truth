import React, { useEffect, useState } from 'react';
import { AlertCircle, BriefcaseBusiness, CheckCircle2, Loader2, Search } from 'lucide-react';
import { jobsApi } from '../api/jobs';
import type { Job, JobRequirement } from '../types/job';

export const Jobs: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [requirements, setRequirements] = useState<JobRequirement[]>([]);
  const [form, setForm] = useState({ title: '', company_name: '', location: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const loadJobs = async () => {
    try { setLoading(true); const data = await jobsApi.list(); setJobs(data); if (data.length && !selectedJob) setSelectedJob(data[0]); }
    catch (err: any) { setError(err.message || 'Unable to load saved jobs.'); }
    finally { setLoading(false); }
  };
  useEffect(() => { void loadJobs(); }, []);

  useEffect(() => {
    if (!selectedJob) { setRequirements([]); return; }
    void jobsApi.requirements(selectedJob.id).then(setRequirements).catch((err: any) => setError(err.message || 'Unable to load requirements.'));
  }, [selectedJob]);

  const createAndAnalyze = async (event: React.FormEvent) => {
    event.preventDefault(); setSaving(true); setError(null); setMessage(null);
    try {
      const job = await jobsApi.create(form);
      const analysis = await jobsApi.analyze(job.id);
      setSelectedJob(analysis.job); setRequirements(analysis.requirements); setForm({ title: '', company_name: '', location: '', description: '' });
      await loadJobs(); setMessage('Job description analyzed successfully.');
    } catch (err: any) { setError(err.message || 'Unable to analyze this job description.'); }
    finally { setSaving(false); }
  };

  const importanceTone = (importance: JobRequirement['importance']) => importance === 'required' ? 'border-rose-500/30 bg-rose-500/10 text-rose-200' : importance === 'preferred' ? 'border-amber-500/30 bg-amber-500/10 text-amber-200' : 'border-slate-500/30 bg-slate-500/10 text-slate-300';

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <div><p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Module 4: JD Analyzer</p><h1 className="text-3xl font-bold text-white mt-2">Job description analysis</h1><p className="text-slate-400 mt-2">Paste a job description to separate important requirements before matching it against your source of truth.</p></div>
      {(message || error) && <div role="alert" className={`p-3 rounded-xl border text-sm ${error ? 'border-rose-500/30 bg-rose-500/10 text-rose-200' : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'}`}>{error || message}</div>}
      <div className="grid xl:grid-cols-[1fr_1.1fr] gap-6">
        <form onSubmit={createAndAnalyze} className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4"><div className="flex items-center gap-3 mb-2"><BriefcaseBusiness className="text-indigo-400" /><h2 className="text-lg font-semibold text-white">Analyze a job</h2></div><div className="grid sm:grid-cols-2 gap-3"><input placeholder="Job title" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} className="input-field" /><input placeholder="Company" value={form.company_name} onChange={(event) => setForm({ ...form, company_name: event.target.value })} className="input-field" /></div><input placeholder="Location" value={form.location} onChange={(event) => setForm({ ...form, location: event.target.value })} className="input-field w-full" /><textarea required minLength={20} rows={15} placeholder="Paste the complete job description here..." value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} className="input-field w-full resize-y" /><button disabled={saving} className="btn-primary inline-flex items-center gap-2">{saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}{saving ? 'Analyzing...' : 'Save & analyze'}</button></form>
        <section className="glass-panel p-6 rounded-2xl border border-white/10"><div className="flex items-center gap-3 mb-4"><CheckCircle2 className="text-indigo-400" /><h2 className="text-lg font-semibold text-white">Structured requirements</h2></div>{loading ? <p className="text-sm text-slate-400">Loading saved jobs...</p> : jobs.length === 0 ? <div className="text-sm text-slate-400 flex gap-2"><AlertCircle className="w-4 h-4 mt-0.5" />Analyze your first job description to see requirements.</div> : <><div className="flex flex-wrap gap-2 mb-5">{jobs.map((job) => <button key={job.id} onClick={() => setSelectedJob(job)} className={`px-3 py-2 rounded-lg border text-sm ${selectedJob?.id === job.id ? 'border-indigo-500/40 bg-indigo-500/10 text-white' : 'border-white/10 bg-white/5 text-slate-300'}`}>{job.title || 'Untitled role'}</button>)}</div>{selectedJob && <div className="mb-4"><h3 className="text-xl font-semibold text-white">{selectedJob.title || 'Untitled role'}</h3><p className="text-sm text-slate-400">{selectedJob.company_name || 'Company not specified'} · {selectedJob.analysis_status}</p></div>}{requirements.length === 0 ? <p className="text-sm text-slate-400">No structured requirements yet.</p> : <div className="space-y-3">{requirements.map((requirement) => <div key={requirement.id} className="p-4 rounded-xl border border-white/10 bg-white/5"><div className="flex flex-wrap justify-between gap-2"><span className="text-white font-medium">{requirement.skill_name || requirement.requirement_text}</span><span className={`px-2 py-1 rounded-full border text-[11px] uppercase ${importanceTone(requirement.importance)}`}>{requirement.importance}</span></div><p className="text-sm text-slate-400 mt-2">{requirement.requirement_text}{requirement.minimum_years ? ` · ${requirement.minimum_years}+ years` : ''}</p></div>)}</div>}</>}</section>
      </div>
    </div>
  );
};
