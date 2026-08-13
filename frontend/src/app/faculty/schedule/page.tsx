'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { Calendar as CalIcon } from 'lucide-react';

export default function SchedulePage() {
  const { loading: al } = useAuth(['faculty', 'admin']);
  const [schedule, setSchedule] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { if (!al) { api.get('/faculty/schedule').then((r: any) => { setSchedule(r.data || []); setLoading(false); }); } }, [al]);
  if (al || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Today&apos;s Schedule</h1><p className="text-slate-400">{schedule.length} classes</p></div>
      <div className="space-y-3">
        {schedule.map((s: any, i: number) => (
          <div key={s.id} className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay: i*50+'ms',animationFillMode:'both'}}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3"><CalIcon size={20} className="text-accent" /><div><h3 className="font-semibold text-white">{s.subject?.name || 'Subject'}</h3><p className="text-xs text-slate-400">{s.attendance_mode} mode</p></div></div>
              <span className={s.status==='completed' ? 'badge-success' : s.status==='active' ? 'badge-info' : 'badge-warning'}>{s.status}</span>
            </div>
          </div>
        ))}
        {schedule.length === 0 && <div className="glass-card p-8 text-center text-slate-400">No classes scheduled today</div>}
      </div>
    </div>
  );
}