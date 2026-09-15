import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  KeyRound,
  LogOut,
  MonitorOff,
  ShieldCheck,
  User,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Settings: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [loggingOut, setLoggingOut] = useState(false);
  const [loggingOutAll, setLoggingOutAll] = useState(false);

  const handleLogout = async (allDevices: boolean) => {
    if (allDevices) setLoggingOutAll(true);
    else setLoggingOut(true);
    try {
      await logout(allDevices);
      navigate('/signin', { replace: true });
    } finally {
      setLoggingOut(false);
      setLoggingOutAll(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto pb-12">
      <div>
        <p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Security</p>
        <h1 className="text-3xl font-bold text-white mt-2">Account &amp; Security</h1>
        <p className="text-slate-400 mt-2">Manage your account identity, sessions, and security preferences.</p>
      </div>

      {/* Account info */}
      <section className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
        <div className="flex items-center gap-3">
          <User className="w-5 h-5 text-indigo-400" />
          <h2 className="text-lg font-semibold text-white">Account information</h2>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          <div className="space-y-1">
            <p className="text-xs text-slate-500 uppercase tracking-wide">Full name</p>
            <p className="text-white font-medium">{user?.full_name || '—'}</p>
          </div>
          <div className="space-y-1">
            <p className="text-xs text-slate-500 uppercase tracking-wide">Email address</p>
            <p className="text-white font-medium">{user?.email || '—'}</p>
          </div>
          <div className="space-y-1">
            <p className="text-xs text-slate-500 uppercase tracking-wide">Account status</p>
            <p className="text-emerald-400 font-medium">Active</p>
          </div>
          <div className="space-y-1">
            <p className="text-xs text-slate-500 uppercase tracking-wide">Member since</p>
            <p className="text-white font-medium">
              {user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}
            </p>
          </div>
        </div>
      </section>

      {/* Truth firewall notice */}
      <div className="flex items-start gap-3 p-4 rounded-2xl bg-indigo-500/8 border border-indigo-500/20 text-sm text-slate-300">
        <ShieldCheck className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold text-white">Career data protection</p>
          <p className="text-slate-400 text-xs mt-1">
            All your career claims, evidence, and verified profile data are locked behind authentication and can never be modified by AI directly. Only you can approve or reject any changes.
          </p>
        </div>
      </div>

      {/* Session management */}
      <section className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
        <div className="flex items-center gap-3">
          <KeyRound className="w-5 h-5 text-indigo-400" />
          <h2 className="text-lg font-semibold text-white">Session management</h2>
        </div>

        <p className="text-sm text-slate-400">
          CareerMate uses short-lived access tokens (15 min) with a rotating 7-day refresh session stored in an HttpOnly cookie. Your session is invalidated immediately upon logout.
        </p>

        <div className="flex flex-wrap gap-3 pt-2">
          <button
            disabled={loggingOut}
            onClick={() => void handleLogout(false)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-rose-500/30 bg-rose-500/15 text-rose-200 text-sm hover:bg-rose-500/25 disabled:opacity-50"
          >
            <LogOut className="w-4 h-4" />
            {loggingOut ? 'Signing out…' : 'Sign out this session'}
          </button>

          <button
            disabled={loggingOutAll}
            onClick={() => void handleLogout(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-rose-700/40 bg-rose-700/15 text-rose-300 text-sm hover:bg-rose-700/25 disabled:opacity-50"
          >
            <MonitorOff className="w-4 h-4" />
            {loggingOutAll ? 'Revoking all sessions…' : 'Revoke all devices'}
          </button>
        </div>
      </section>

      {/* Data & Privacy */}
      <section className="glass-panel p-6 rounded-2xl border border-white/10 space-y-3">
        <h2 className="text-lg font-semibold text-white">Data &amp; privacy</h2>
        <p className="text-sm text-slate-400">
          CareerMate stores your career profile, claims, evidence, uploaded resumes, and job descriptions locally in your PostgreSQL database. No data is shared with AI providers beyond the text required to perform analysis — and no AI output is persisted as trusted data without your explicit approval.
        </p>
        <div className="pt-2 space-y-2 text-sm text-slate-300">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            AI outputs are proposals, never trusted facts.
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            Resume generation uses only claims you explicitly approved.
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            Uploaded resumes are stored privately under your profile ID.
          </div>
        </div>
      </section>
    </div>
  );
};
