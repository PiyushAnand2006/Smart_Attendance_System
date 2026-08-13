'use client';
import { useState, useEffect } from 'react';
import { Bell, Search, LogOut, Settings, User } from 'lucide-react';
import { logout } from '@/services/api';

interface HeaderProps { title: string; }

export default function Header({ title }: HeaderProps) {
  const [user, setUser] = useState<any>(null);
  const [showProfile, setShowProfile] = useState(false);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) setUser(JSON.parse(userData));
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-primary-dark/80 backdrop-blur-xl border-b border-slate-700/50 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">{title}</h1>
          <p className="text-sm text-slate-400 mt-0.5">Welcome back, {user?.first_name || user?.email || 'User'}</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <input type="search" placeholder="Search..."
              className="pl-10 pr-4 py-2 bg-slate-700/30 border border-slate-600/50 rounded-lg text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-accent/50 w-64 transition-all" />
          </div>
          <button className="relative p-2.5 hover:bg-slate-700/30 rounded-xl transition-all duration-300 group">
            <Bell size={20} className="text-slate-300 group-hover:text-accent transition-colors" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-accent rounded-full animate-pulse" />
          </button>
          <div className="relative">
            <button onClick={() => setShowProfile(!showProfile)}
              className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-highlight flex items-center justify-center text-white font-semibold hover:shadow-glow transition-all duration-300 hover:scale-105">
              {user?.first_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || 'U'}
            </button>
            {showProfile && (
              <div className="absolute right-0 top-12 w-56 glass-card p-2 animate-scale-in z-50">
                <div className="px-3 py-2 border-b border-slate-700/50 mb-1">
                  <p className="text-sm font-medium text-white">{user?.first_name} {user?.last_name}</p>
                  <p className="text-xs text-slate-400">{user?.email}</p>
                </div>
                <button onClick={() => { logout(); setShowProfile(false); }}
                  className="w-full flex items-center gap-2 px-3 py-2 text-sm text-slate-300 hover:text-danger hover:bg-danger/10 rounded-lg transition-all">
                  <LogOut size={16} /> Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
