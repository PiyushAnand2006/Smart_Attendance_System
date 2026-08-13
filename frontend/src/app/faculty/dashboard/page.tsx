'use client';
import { useState, useEffect } from 'react';
import { Users, ClipboardCheck, TrendingUp, Calendar } from 'lucide-react';
import StatCard from '@/components/StatCard';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';

export default function FacultyDashboard() {
  const { loading: al, user } = useAuth(['faculty', 'admin']);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { if (!al) { api.get('/faculty/dashboard').then((r: any) => { setStats(r.data); setLoading(false); }); } }, [al]);
  if (al || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard label="Today Sessions" value={stats?.today_sessions?.length || 0} icon={<Calendar size={24} />} color="accent" delay={0} />
        <StatCard label="Total Marked" value={stats?.today_total || 0} icon={<Users size={24} />} color="info" delay={50} />
        <StatCard label="Present" value={stats?.today_present || 0} icon={<ClipboardCheck size={24} />} color="success" delay={100} />
        <StatCard label="Rate" value={(stats?.attendance_rate || 0) + '%'} icon={<TrendingUp size={24} />} color="warning" delay={150} />
      </div>
      <div className="glass-card p-6 animate-slide-up" style={{animationDelay:'200ms',animationFillMode:'both'}}>
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2"><Calendar size={20} className="text-accent" /> Today&apos;s Schedule</h3>
        <div className="space-y-3">
          {(stats?.today_sessions || []).map((s: any) => (
            <div key={s.id} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl hover:bg-slate-800/80 transition-all duration-300 group">
              <div><h4 className="font-semibold text-white group-hover:text-accent transition-colors">{s.subject_name}</h4><p className="text-sm text-slate-400">{s.class_name}</p></div>
              <span className={s.status==='completed' ? 'badge-success' : s.status==='active' ? 'badge-info' : 'badge-warning'}>{s.status}</span>
            </div>
          ))}
          {(stats?.today_sessions || []).length === 0 && <p className="text-slate-400 text-center py-8">No sessions today</p>}
        </div>
      </div>
    </div>
  );
}
