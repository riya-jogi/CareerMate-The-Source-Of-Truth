import type { LucideIcon } from 'lucide-react';
import { Sparkles } from 'lucide-react';

interface PlaceholderPageProps {
  title: string;
  moduleName: string;
  description: string;
  icon: LucideIcon;
}

export const PlaceholderPage: React.FC<PlaceholderPageProps> = ({
  title,
  moduleName,
  description,
  icon: Icon,
}) => {
  return (
    <div className="glass-panel p-8 sm:p-12 rounded-2xl border border-white/10 text-center max-w-2xl mx-auto my-8">
      <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mx-auto mb-6 shadow-glow-brand">
        <Icon className="w-8 h-8" />
      </div>

      <div className="inline-flex items-center space-x-2 text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3 py-1 px-3 rounded-full bg-indigo-500/10 border border-indigo-500/20">
        <Sparkles className="w-3.5 h-3.5" />
        <span>{moduleName}</span>
      </div>

      <h1 className="text-2xl sm:text-3xl font-bold text-white mb-3 tracking-tight">{title}</h1>
      <p className="text-slate-400 text-sm leading-relaxed max-w-lg mx-auto mb-6">
        {description}
      </p>

      <div className="p-4 rounded-xl bg-slate-900/60 border border-white/5 text-xs text-slate-500 max-w-md mx-auto">
        Authentication guard verified. Route shell active and ready for module integration.
      </div>
    </div>
  );
};
