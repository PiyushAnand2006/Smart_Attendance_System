'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { History } from 'lucide-react';

export default function HistoryPage() {
  const { loading: al } = useAuth(['faculty', 'admin']);
  const [sessions, setSessions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { if (!al) { api.get('/attendance/sessions').then((r: any) => { setSessions(r.data || []); setLoading(false); }); } }, [al]);
  if (al || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Attendance History</h1><p className="text-slate-400">{sessions.length} sessions</p></div>
      <div className="space-y-3">
        {sessions.map((s: any, i: number) => (
          <div key={s.id} className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay: i*30+'ms',animationFillMode:'both'}}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3"><History size={18} className="text-accent" /><div><h3 className="font-semibold text-white">{s.subject_name || 'Unknown'}</h3><p className="text-xs text-slate-400">{s.class_name} | {s.scheduled_date} | {s.attendance_mode}</p></div></div>
              <div className="flex items-center gap-3"><span className="text-sm text-slate-300">{s.marked}/{s.total_students}</span><span className={s.status==='completed' ? 'badge-success' : 'badge-info'}>{s.status}</span></div>
            </div>
          </div>
        ))}
        {sessions.length === 0 && <div className="glass-card p-8 text-center text-slate-400">No sessions yet</div>}
      </div>
    </div>
  );
}