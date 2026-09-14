import React, { useEffect, useState } from 'react';
import { BriefcaseBusiness, Check, Plus, Save, Trash2, UserRound } from 'lucide-react';
import { profileApi } from '../api/profile';
import type { CareerProfile } from '../types/profile';

const emptyExperience = { company_name: '', job_title: '', start_date: '', end_date: '', is_current: false, description: '' };

export const Profile: React.FC = () => {
  const [profile, setProfile] = useState<CareerProfile | null>(null);
  const [form, setForm] = useState({ headline: '', summary: '', phone: '', location: '', linkedin_url: '', github_url: '', portfolio_url: '' });
  const [experience, setExperience] = useState(emptyExperience);
  const [skill, setSkill] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const data = await profileApi.get();
      setProfile(data);
      setForm({
        headline: data.headline || '', summary: data.summary || '', phone: data.phone || '', location: data.location || '',
        linkedin_url: data.linkedin_url || '', github_url: data.github_url || '', portfolio_url: data.portfolio_url || '',
      });
    } catch (err: any) {
      setError(err.message || 'Unable to load your career profile.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadProfile(); }, []);

  const updateField = (field: keyof typeof form, value: string) => setForm((current) => ({ ...current, [field]: value }));

  const saveProfile = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true); setMessage(null); setError(null);
    try {
      const data = await profileApi.update(form);
      setProfile(data); setMessage('Career profile saved.');
    } catch (err: any) { setError(err.message || 'Unable to save your profile.'); }
    finally { setSaving(false); }
  };

  const addExperience = async (event: React.FormEvent) => {
    event.preventDefault(); setError(null);
    try { await profileApi.addExperience(experience); setExperience(emptyExperience); await loadProfile(); setMessage('Experience added.'); }
    catch (err: any) { setError(err.message || 'Unable to add experience.'); }
  };

  const addSkill = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!skill.trim()) return;
    try { await profileApi.addSkill(skill.trim()); setSkill(''); await loadProfile(); setMessage('Skill added.'); }
    catch (err: any) { setError(err.message || 'Unable to add skill.'); }
  };

  if (loading) return <div className="glass-panel p-8 text-slate-300">Loading your career profile...</div>;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <div><p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Module 2: Source of Truth</p><h1 className="text-3xl font-bold text-white mt-2">Career Profile</h1><p className="text-slate-400 mt-2">Keep the candidate facts that future resumes are allowed to use.</p></div>
      {(message || error) && <div role="alert" className={`p-3 rounded-xl border text-sm ${error ? 'border-rose-500/30 bg-rose-500/10 text-rose-200' : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'}`}>{error || message}</div>}
      <form onSubmit={saveProfile} className="glass-panel p-6 rounded-2xl border border-white/10 space-y-5">
        <div className="flex items-center gap-3"><UserRound className="text-indigo-400" /><h2 className="text-lg font-semibold text-white">Professional identity</h2></div>
        <div className="grid md:grid-cols-2 gap-4">
          {([['headline', 'Headline'], ['location', 'Location'], ['phone', 'Phone'], ['linkedin_url', 'LinkedIn URL'], ['github_url', 'GitHub URL'], ['portfolio_url', 'Portfolio URL']] as const).map(([field, label]) => <label key={field} className="space-y-1 text-sm text-slate-300"><span>{label}</span><input value={form[field]} onChange={(e) => updateField(field, e.target.value)} className="w-full input-field" /></label>)}
        </div>
        <label className="block space-y-1 text-sm text-slate-300"><span>Summary</span><textarea value={form.summary} onChange={(e) => updateField('summary', e.target.value)} rows={5} className="w-full input-field resize-y" /></label>
        <button disabled={saving} className="inline-flex items-center gap-2 btn-primary"><Save className="w-4 h-4" />{saving ? 'Saving...' : 'Save profile'}</button>
      </form>
      <div className="grid lg:grid-cols-2 gap-6">
        <section className="glass-panel p-6 rounded-2xl border border-white/10"><div className="flex items-center gap-3 mb-5"><BriefcaseBusiness className="text-indigo-400" /><h2 className="text-lg font-semibold text-white">Experience</h2></div><form onSubmit={addExperience} className="space-y-3"><div className="grid sm:grid-cols-2 gap-3"><input required placeholder="Company" value={experience.company_name} onChange={(e) => setExperience({ ...experience, company_name: e.target.value })} className="input-field" /><input required placeholder="Job title" value={experience.job_title} onChange={(e) => setExperience({ ...experience, job_title: e.target.value })} className="input-field" /><input required type="date" value={experience.start_date} onChange={(e) => setExperience({ ...experience, start_date: e.target.value })} className="input-field" /><input type="date" value={experience.end_date} disabled={experience.is_current} onChange={(e) => setExperience({ ...experience, end_date: e.target.value })} className="input-field" /></div><label className="flex items-center gap-2 text-sm text-slate-300"><input type="checkbox" checked={experience.is_current} onChange={(e) => setExperience({ ...experience, is_current: e.target.checked, end_date: '' })} /> Current role</label><textarea placeholder="Responsibilities and achievements" value={experience.description} onChange={(e) => setExperience({ ...experience, description: e.target.value })} className="w-full input-field" rows={3} /><button className="inline-flex items-center gap-2 btn-secondary"><Plus className="w-4 h-4" />Add experience</button></form><div className="mt-6 space-y-3">{profile?.experiences.map((item) => <div key={item.id} className="p-3 rounded-xl bg-white/5 flex justify-between gap-3"><div><p className="text-white font-medium">{item.job_title}</p><p className="text-sm text-slate-400">{item.company_name} · {item.start_date} - {item.is_current ? 'Present' : item.end_date}</p></div><button title="Delete experience" onClick={async () => { await profileApi.deleteExperience(item.id); loadProfile(); }} className="text-rose-400"><Trash2 className="w-4 h-4" /></button></div>)}</div></section>
        <section className="glass-panel p-6 rounded-2xl border border-white/10"><h2 className="text-lg font-semibold text-white mb-5">Skills</h2><form onSubmit={addSkill} className="flex gap-2"><input required placeholder="e.g. Python" value={skill} onChange={(e) => setSkill(e.target.value)} className="input-field flex-1" /><button title="Add skill" className="btn-secondary"><Plus className="w-4 h-4" /></button></form><div className="flex flex-wrap gap-2 mt-5">{profile?.skills.map((item) => <span key={item.id} className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-200 text-sm">{item.name}<button title={`Remove ${item.name}`} onClick={async () => { await profileApi.deleteSkill(item.id); loadProfile(); }}><Trash2 className="w-3.5 h-3.5 text-rose-300" /></button></span>)}</div>{profile?.skills.length === 0 && <p className="text-sm text-slate-500 mt-5">Add the skills you can support with real experience.</p>}<div className="mt-8 p-4 rounded-xl border border-indigo-500/20 bg-indigo-500/5 text-sm text-slate-300 flex gap-3"><Check className="w-5 h-5 text-indigo-400 shrink-0" /><span>These details become structured candidate data. Evidence and claim review will be added in the next module.</span></div></section>
      </div>
    </div>
  );
};