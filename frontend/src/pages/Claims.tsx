import React, { useEffect, useState } from 'react';
import { CheckCircle2, Edit3, ShieldCheck, XCircle } from 'lucide-react';
import { claimsApi } from '../api/claims';
import type { CareerClaim } from '../types/claims';

export const Claims: React.FC = () => {
  const [claims, setClaims] = useState<CareerClaim[]>([]);
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadClaims = async () => {
    try {
      setLoading(true);
      const data = await claimsApi.list();
      setClaims(data);
      setDrafts(Object.fromEntries(data.map((claim) => [claim.id, claim.claim_text])));
    } catch (err: any) {
      setError(err.message || 'Unable to load career claims.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void loadClaims(); }, []);

  const review = async (claim: CareerClaim, decision: 'confirm' | 'reject') => {
    try {
      setError(null);
      if (decision === 'confirm') {
        await claimsApi.update(claim.id, { claim_text: drafts[claim.id] });
        await claimsApi.confirm(claim.id);
      } else {
        await claimsApi.reject(claim.id);
      }
      setMessage(decision === 'confirm' ? 'Claim confirmed for future resume use.' : 'Claim rejected and blocked from trusted use.');
      await loadClaims();
    } catch (err: any) {
      setError(err.message || 'Unable to review this claim.');
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      <div>
        <p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Module 2: Truth Layer</p>
        <h1 className="text-3xl font-bold text-white mt-2">Career claims review</h1>
        <p className="text-slate-400 mt-2">Confirm, correct, or reject candidate facts before they can guide future resumes.</p>
      </div>
      {(message || error) && <div role="alert" className={`p-3 rounded-xl border text-sm ${error ? 'border-rose-500/30 bg-rose-500/10 text-rose-200' : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'}`}>{error || message}</div>}
      {loading ? <div className="glass-panel p-6 text-slate-400">Loading claims...</div> : claims.length === 0 ? <div className="glass-panel p-6 text-slate-400">No claims yet. Accept an extracted resume proposal or add a claim from the API.</div> : (
        <div className="space-y-4">
          {claims.map((claim) => (
            <section key={claim.id} className="glass-panel p-5 rounded-2xl border border-white/10">
              <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                <div><p className="text-[10px] uppercase tracking-wider text-indigo-400 font-bold">{claim.claim_type} · {claim.experience_type}</p><p className="text-xs text-slate-400 mt-1">Subject: {claim.subject}</p></div>
                <span className="px-2.5 py-1 rounded-full border border-white/10 bg-white/5 text-xs text-slate-300">{claim.status.replace('_', ' ')}</span>
              </div>
              <div className="flex gap-2 items-start"><Edit3 className="w-4 h-4 text-slate-500 mt-3" /><textarea value={drafts[claim.id] || ''} onChange={(event) => setDrafts((current) => ({ ...current, [claim.id]: event.target.value }))} rows={3} className="w-full input-field resize-y" /></div>
              <div className="mt-4 flex flex-wrap gap-3">
                <button onClick={() => void review(claim, 'confirm')} className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-200 text-sm"><CheckCircle2 className="w-4 h-4" /> Confirm</button>
                <button onClick={() => void review(claim, 'reject')} className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-200 text-sm"><XCircle className="w-4 h-4" /> Reject</button>
              </div>
            </section>
          ))}
        </div>
      )}
      <div className="flex gap-3 items-start text-sm text-slate-400"><ShieldCheck className="w-5 h-5 text-indigo-400 shrink-0" />Resume extraction remains a proposal until you make an explicit decision here.</div>
    </div>
  );
};
