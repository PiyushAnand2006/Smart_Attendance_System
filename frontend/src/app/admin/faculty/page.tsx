'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { GraduationCap, Mail, Building } from 'lucide-react';

export default function FacultyPage() {
  const { loading: al } = useAuth(['admin']);
  const [faculty, setFaculty] = useState<any[]>([]);
  useEffect(() => { if (!al) api.get('/admin/stats').then((r: any) => {}).catch(() => {}); }, [al]);
  if (al) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-white">Faculty</h1><p className="text-slate-400">Manage faculty members</p></div>
      </div>
      <div className="glass-card p-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-info/20 text-info mb-4"><GraduationCap size={28} /></div>
        <h2 className="text-xl font-bold text-white mb-2">Faculty Management</h2>
        <p className="text-slate-400 mb-4">Faculty can be added via the registration page with role &quot;faculty&quot;</p>
      </div>
    </div>
  );
}