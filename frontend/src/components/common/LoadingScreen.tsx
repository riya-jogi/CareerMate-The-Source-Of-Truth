import React from 'react';
import { ShieldCheck, Loader2 } from 'lucide-react';

interface LoadingScreenProps {
  message?: string;
}

export const LoadingScreen: React.FC<LoadingScreenProps> = ({
  message = 'Verifying candidate credentials...',
}) => {
  return (
    <div className="min-h-screen bg-[#0B0F19] flex flex-col items-center justify-center relative overflow-hidden px-4">
      {/* Background Ambient Glows */}
      <div className="ambient-glow bg-indigo-600/15 w-96 h-96 -top-20 -left-20" />
      <div className="ambient-glow bg-violet-600/10 w-96 h-96 -bottom-20 -right-20" />

      <div className="z-10 flex flex-col items-center max-w-sm text-center">
        {/* Brand Icon Badge */}
        <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-6 shadow-glow-brand animate-pulse">
          <ShieldCheck className="w-8 h-8 text-indigo-400" />
        </div>

        <h2 className="text-xl font-bold tracking-tight text-white mb-2">CareerMate</h2>
        <p className="text-xs uppercase tracking-widest text-indigo-400 font-semibold mb-6">
          The Source Of Truth
        </p>

        <div className="flex items-center space-x-3 text-slate-400 text-sm glass-panel py-2 px-4 rounded-full">
          <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
          <span>{message}</span>
        </div>
      </div>
    </div>
  );
};
