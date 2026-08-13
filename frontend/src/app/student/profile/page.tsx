'use client';
import { useAuth } from '@/hooks/useAuth';
import { User, Mail, Hash } from 'lucide-react';

export default function ProfilePage() {
  const { user, loading: al } = useAuth(['student']);
  if (al) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">My Profile</h1></div>
      <div className="glass-card p-8 max-w-lg">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-accent to-highlight flex items-center justify-center text-white text-3xl font-bold animate-pulse-glow">{user?.first_name?.[0]?.toUpperCase() || '?'}</div>
          <div><h2 className="text-xl font-bold text-white">{user?.first_name} {user?.last_name}</h2><p className="text-slate-400">{user?.email}</p><span className="badge-info mt-1 inline-block">{user?.role}</span></div>
        </div>
        <div className="space-y-3 border-t border-slate-700 pt-4">
          <div className="flex items-center gap-3 text-sm"><Mail size={16} className="text-slate-400" /><span className="text-slate-300">{user?.email}</span></div>
          <div className="flex items-center gap-3 text-sm"><Hash size={16} className="text-slate-400" /><span className="text-slate-300">{user?.user_id}</span></div>
          <div className="flex items-center gap-3 text-sm"><User size={16} className="text-slate-400" /><span className="text-slate-300">{user?.first_name} {user?.last_name}</span></div>
        </div>
      </div>
    </div>
  );
}