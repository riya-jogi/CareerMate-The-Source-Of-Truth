import React, { useState, useEffect, useRef } from 'react';
import { Link, NavLink, Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  ShieldCheck,
  LayoutDashboard,
  UserCheck,
  FileText,
  Briefcase,
  GitCompare,
  Wand2,
  Settings,
  LogOut,
  Menu,
  X,
  CheckCircle2,
  ChevronDown,
  Loader2,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const AppLayout: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close user dropdown and mobile drawer on route change
  useEffect(() => {
    setUserDropdownOpen(false);
    setMobileMenuOpen(false);
  }, [location.pathname]);

  // Click outside to close user dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setUserDropdownOpen(false);
      }
    };

    if (userDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [userDropdownOpen]);

  const handleLogout = async (allDevices: boolean = false) => {
    try {
      setIsLoggingOut(true);
      await logout(allDevices);
      navigate('/signin', { replace: true });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setIsLoggingOut(false);
    }
  };

  const navItems = [
    { label: 'Dashboard', path: '/app/dashboard', icon: LayoutDashboard, tag: 'Module 1' },
    { label: 'Career Profile', path: '/app/profile', icon: UserCheck, tag: 'Module 2' },
    { label: 'Resumes', path: '/app/resumes', icon: FileText, tag: 'Module 3' },
    { label: 'Jobs', path: '/app/jobs', icon: Briefcase, tag: 'Module 4' },
    { label: 'Matching', path: '/app/matching', icon: GitCompare, tag: 'Module 5' },
    { label: 'Optimization', path: '/app/optimization', icon: Wand2, tag: 'Module 6' },
    { label: 'Settings', path: '/app/settings', icon: Settings, tag: 'Security' },
  ];

  const getInitials = (name?: string) => {
    if (!name) return 'CM';
    return name
      .split(' ')
      .filter(Boolean)
      .map((n) => n[0])
      .slice(0, 2)
      .join('')
      .toUpperCase();
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex flex-col">
      {/* Top Navbar */}
      <header className="sticky top-0 z-40 glass-panel border-b border-white/5 px-4 sm:px-8 py-3.5 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Toggle navigation menu"
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <Link to="/app/dashboard" className="flex items-center space-x-3 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 flex items-center justify-center shadow-glow-brand transition-transform group-hover:scale-105">
              <ShieldCheck className="w-5 h-5 text-white" aria-hidden="true" />
            </div>
            <div>
              <span className="font-extrabold tracking-tight text-white text-lg block leading-none">
                CareerMate
              </span>
              <span className="text-[10px] uppercase font-bold tracking-widest text-indigo-400 block mt-0.5">
                The Source Of Truth
              </span>
            </div>
          </Link>
        </div>

        {/* Source of Truth Principle Badge & User Status */}
        <div className="flex items-center space-x-3 sm:space-x-6">
          <div className="hidden lg:flex items-center space-x-2 py-1 px-3 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
            <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Source of Truth: Active Anchor</span>
          </div>

          {/* User Menu Dropdown */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setUserDropdownOpen(!userDropdownOpen)}
              className="flex items-center space-x-2.5 p-1.5 rounded-xl hover:bg-white/5 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500"
              aria-label="Open candidate menu"
              aria-haspopup="true"
              aria-expanded={userDropdownOpen}
            >
              <div className="w-8 h-8 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-xs font-bold text-indigo-300">
                {getInitials(user?.full_name)}
              </div>
              <div className="hidden sm:block text-left">
                <div className="text-xs font-semibold text-white leading-tight">
                  {user?.full_name || 'Candidate'}
                </div>
                <div className="text-[11px] text-slate-400 leading-tight truncate max-w-[130px]">
                  {user?.email}
                </div>
              </div>
              <ChevronDown
                className={`w-3.5 h-3.5 text-slate-400 transition-transform ${
                  userDropdownOpen ? 'rotate-180 text-white' : ''
                }`}
                aria-hidden="true"
              />
            </button>

            {/* Dropdown Menu */}
            {userDropdownOpen && (
              <div
                role="menu"
                className="absolute right-0 mt-2 w-64 glass-panel rounded-2xl border border-white/10 shadow-2xl py-2 z-50 animate-in fade-in slide-in-from-top-2 duration-150"
              >
                <div className="px-4 py-2.5 border-b border-white/5">
                  <div className="text-xs font-bold text-white truncate">
                    {user?.full_name || 'Candidate Profile'}
                  </div>
                  <div className="text-[11px] text-slate-400 truncate">{user?.email}</div>
                  <div className="mt-1.5 inline-flex items-center space-x-1 py-0.5 px-2 rounded-md bg-emerald-500/10 text-emerald-400 text-[10px] font-semibold">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Verified Career Anchor</span>
                  </div>
                </div>

                <div className="py-1">
                  <Link
                    to="/app/profile"
                    role="menuitem"
                    className="flex items-center space-x-2.5 px-4 py-2 text-xs text-slate-300 hover:text-white hover:bg-white/5 transition-colors"
                  >
                    <UserCheck className="w-4 h-4 text-indigo-400" />
                    <span>Career Profile & Evidence</span>
                  </Link>

                  <Link
                    to="/app/settings"
                    role="menuitem"
                    className="flex items-center space-x-2.5 px-4 py-2 text-xs text-slate-300 hover:text-white hover:bg-white/5 transition-colors"
                  >
                    <Settings className="w-4 h-4 text-slate-400" />
                    <span>Account & Security</span>
                  </Link>
                </div>

                <div className="pt-1 border-t border-white/5">
                  <button
                    onClick={() => handleLogout(false)}
                    disabled={isLoggingOut}
                    role="menuitem"
                    className="w-full flex items-center space-x-2.5 px-4 py-2 text-xs text-rose-400 hover:bg-rose-500/10 transition-colors disabled:opacity-50 text-left"
                  >
                    {isLoggingOut ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <LogOut className="w-4 h-4" />
                    )}
                    <span>{isLoggingOut ? 'Signing out...' : 'Sign Out of Session'}</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main App Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar for Desktop */}
        <aside className="hidden md:flex flex-col w-64 glass-panel border-r border-white/5 p-4 justify-between shrink-0">
          <div className="space-y-1">
            <div className="text-[11px] font-semibold tracking-wider text-slate-500 uppercase px-3 py-2">
              ATS Optimization Pipeline
            </div>
            <nav className="space-y-1" aria-label="Sidebar Navigation">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all ${
                        isActive
                          ? 'bg-indigo-600 text-white shadow-glow-brand font-semibold'
                          : 'text-slate-400 hover:text-white hover:bg-white/5'
                      }`
                    }
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className="w-4 h-4" aria-hidden="true" />
                      <span>{item.label}</span>
                    </div>
                    <span className="text-[10px] text-slate-500 group-hover:text-slate-400 font-mono">
                      {item.tag}
                    </span>
                  </NavLink>
                );
              })}
            </nav>
          </div>

          <div className="pt-4 border-t border-white/5">
            <div className="p-3 rounded-xl bg-slate-900/60 border border-white/5 text-[11px] text-slate-400 space-y-1">
              <span className="font-semibold text-slate-300 block">Single Source of Truth</span>
              <p className="text-[10px] text-slate-500 leading-normal">
                AI outputs are derived artifacts. Your career evidence is never altered by AI.
              </p>
            </div>
          </div>
        </aside>

        {/* Mobile Sidebar Overlay */}
        {mobileMenuOpen && (
          <div className="fixed inset-0 z-50 md:hidden flex">
            {/* Backdrop */}
            <div
              className="fixed inset-0 bg-black/70 backdrop-blur-sm transition-opacity"
              onClick={() => setMobileMenuOpen(false)}
              aria-hidden="true"
            />

            {/* Drawer */}
            <div className="relative w-4/5 max-w-xs bg-[#0F172A] border-r border-white/10 p-6 flex flex-col justify-between z-10">
              <div>
                <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center text-white">
                      <ShieldCheck className="w-5 h-5" />
                    </div>
                    <span className="font-bold text-white text-base">CareerMate</span>
                  </div>
                  <button
                    onClick={() => setMobileMenuOpen(false)}
                    className="p-1 rounded-lg text-slate-400 hover:text-white"
                    aria-label="Close menu"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <nav className="space-y-1" aria-label="Mobile Navigation">
                  {navItems.map((item) => {
                    const Icon = item.icon;
                    return (
                      <NavLink
                        key={item.path}
                        to={item.path}
                        onClick={() => setMobileMenuOpen(false)}
                        className={({ isActive }) =>
                          `flex items-center justify-between px-3.5 py-3 rounded-xl text-sm font-medium transition-colors ${
                            isActive
                              ? 'bg-indigo-600 text-white font-semibold shadow-glow-brand'
                              : 'text-slate-300 hover:bg-white/5'
                          }`
                        }
                      >
                        <div className="flex items-center space-x-3">
                          <Icon className="w-4 h-4" />
                          <span>{item.label}</span>
                        </div>
                        <span className="text-[10px] text-slate-500 font-mono">{item.tag}</span>
                      </NavLink>
                    );
                  })}
                </nav>
              </div>

              <div className="pt-4 border-t border-white/10 space-y-3">
                <div className="px-2">
                  <div className="text-xs font-semibold text-white truncate">{user?.full_name}</div>
                  <div className="text-[11px] text-slate-400 truncate">{user?.email}</div>
                </div>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    handleLogout(false);
                  }}
                  disabled={isLoggingOut}
                  className="w-full flex items-center space-x-3 text-xs text-rose-400 hover:bg-rose-500/10 p-2.5 rounded-xl transition-colors disabled:opacity-50"
                >
                  <LogOut className="w-4 h-4" />
                  <span>{isLoggingOut ? 'Signing Out...' : 'Sign Out of Session'}</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Nested Route Viewport */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-8 bg-[#0B0F19] relative">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
