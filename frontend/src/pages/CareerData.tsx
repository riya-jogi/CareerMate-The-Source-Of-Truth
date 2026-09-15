import React, { useEffect, useState } from 'react';
import { Award, BookOpen, FolderGit2, Plus, Trash2 } from 'lucide-react';
import { profileApi } from '../api/profile';
import type { CareerProfile } from '../types/profile';

export const CareerData: React.FC = () => {
  const [profile, setProfile] = useState<CareerProfile | null>(null);
  const [project, setProject] = useState({ name: '', description: '', project_type: 'personal' });
  const [education, setEducation] = useState({ institution: '', degree: '', field_of_study: '' });
  const [certification, setCertification] = useState({ name: '', issuing_organization: '' });
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try { setProfile(await profileApi.get()); } catch (err: any) { setError(err.message || 'Unable to load career data.'); }
  };
  useEffect(() => { void load(); }, []);

  const run = async (action: () => Promise<unknown>, success: string) => {
    try { setError(null); await action(); setMessage(success); await load(); }
    catch (err: any) { setError(err.message || 'Unable to update career data.'); }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <div><p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Module 2: Structured Career Data</p><h1 className="text-3xl font-bold text-white mt-2">Projects, education & certifications</h1><p className="text-slate-400 mt-2">Keep the structured facts that resume proposals can reference.</p></div>
      {(message || error) && <div role="alert" className={`p-3 rounded-xl border text-sm ${error ? 'border-rose-500/30 bg-rose-500/10 text-rose-200' : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'}`}>{error || message}</div>}
      <div className="grid lg:grid-cols-3 gap-6">
        <section className="glass-panel p-5 rounded-2xl border border-white/10"><div className="flex items-center gap-2 mb-4"><FolderGit2 className="text-indigo-400" /><h2 className="text-lg font-semibold text-white">Projects</h2></div><form onSubmit={(event) => { event.preventDefault(); void run(() => profileApi.addProject(project).then(() => setProject({ name: '', description: '', project_type: 'personal' })), 'Project added.'); }} className="space-y-3"><input required placeholder="Project name" value={project.name} onChange={(event) => setProject({ ...project, name: event.target.value })} className="input-field w-full" /><textarea required placeholder="What did you build?" value={project.description} onChange={(event) => setProject({ ...project, description: event.target.value })} className="input-field w-full" rows={3} /><button className="btn-secondary inline-flex items-center gap-2"><Plus className="w-4 h-4" />Add project</button></form><div className="mt-5 space-y-2">{profile?.projects.map((item) => <div key={item.id} className="p-3 rounded-xl bg-white/5 flex justify-between gap-2"><span className="text-sm text-white">{item.name}</span><button title="Delete project" onClick={() => void run(() => profileApi.deleteProject(item.id), 'Project deleted.')}><Trash2 className="w-4 h-4 text-rose-300" /></button></div>)}</div></section>
        <section className="glass-panel p-5 rounded-2xl border border-white/10"><div className="flex items-center gap-2 mb-4"><BookOpen className="text-indigo-400" /><h2 className="text-lg font-semibold text-white">Education</h2></div><form onSubmit={(event) => { event.preventDefault(); void run(() => profileApi.addEducation(education).then(() => setEducation({ institution: '', degree: '', field_of_study: '' })), 'Education added.'); }} className="space-y-3"><input required placeholder="Institution" value={education.institution} onChange={(event) => setEducation({ ...education, institution: event.target.value })} className="input-field w-full" /><input required placeholder="Degree" value={education.degree} onChange={(event) => setEducation({ ...education, degree: event.target.value })} className="input-field w-full" /><input placeholder="Field of study" value={education.field_of_study} onChange={(event) => setEducation({ ...education, field_of_study: event.target.value })} className="input-field w-full" /><button className="btn-secondary inline-flex items-center gap-2"><Plus className="w-4 h-4" />Add education</button></form><div className="mt-5 space-y-2">{profile?.education.map((item) => <div key={item.id} className="p-3 rounded-xl bg-white/5 flex justify-between gap-2"><span className="text-sm text-white">{item.degree} · {item.institution}</span><button title="Delete education" onClick={() => void run(() => profileApi.deleteEducation(item.id), 'Education deleted.')}><Trash2 className="w-4 h-4 text-rose-300" /></button></div>)}</div></section>
        <section className="glass-panel p-5 rounded-2xl border border-white/10"><div className="flex items-center gap-2 mb-4"><Award className="text-indigo-400" /><h2 className="text-lg font-semibold text-white">Certifications</h2></div><form onSubmit={(event) => { event.preventDefault(); void run(() => profileApi.addCertification(certification).then(() => setCertification({ name: '', issuing_organization: '' })), 'Certification added.'); }} className="space-y-3"><input required placeholder="Certification name" value={certification.name} onChange={(event) => setCertification({ ...certification, name: event.target.value })} className="input-field w-full" /><input required placeholder="Issuing organization" value={certification.issuing_organization} onChange={(event) => setCertification({ ...certification, issuing_organization: event.target.value })} className="input-field w-full" /><button className="btn-secondary inline-flex items-center gap-2"><Plus className="w-4 h-4" />Add certification</button></form><div className="mt-5 space-y-2">{profile?.certifications.map((item) => <div key={item.id} className="p-3 rounded-xl bg-white/5 flex justify-between gap-2"><span className="text-sm text-white">{item.name} · {item.issuing_organization}</span><button title="Delete certification" onClick={() => void run(() => profileApi.deleteCertification(item.id), 'Certification deleted.')}><Trash2 className="w-4 h-4 text-rose-300" /></button></div>)}</div></section>
      </div>
    </div>
  );
};