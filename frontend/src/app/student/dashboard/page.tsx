'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { TrendingUp, CheckCircle, AlertCircle, BookOpen, Download } from 'lucide-react';
import StatCard from '@/components/StatCard';

export default function StudentDashboard() {
  const { loading: al, user } = useAuth(['student']);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { if (!al) { api.get('/students/my-dashboard').then((r: any) => { setData(r.data); setLoading(false); }).catch(() => setLoading(false)); } }, [al]);
  if (al || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  if (!data) return <div className="glass-card p-8 text-center text-danger">Could not load your data. Make sure your student profile exists.</div>;
  const pct = data.overall.percentage;
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard label="Overall Attendance" value={pct + '%'} icon={<TrendingUp size={24} />} color={pct >= 75 ? 'success' : 'danger'} delay={0} />
        <StatCard label="Classes Attended" value={data.overall.present} icon={<CheckCircle size={24} />} color="accent" delay={50} />
        <StatCard label="Classes Missed" value={data.overall.absent} icon={<AlertCircle size={24} />} color="warning" delay={100} />
      </div>
      {pct < 75 && (
        <div className="glass-card p-4 border-l-4 border-danger animate-slide-up" style={{animationDelay:'150ms',animationFillMode:'both'}}>
          <div className="flex items-start gap-3"><AlertCircle className="text-danger mt-1" size={20} /><div><h4 className="font-semibold text-white">Low Attendance Warning</h4><p className="text-sm text-slate-300 mt-1">Your attendance is {pct}%, below the 75% requirement. Attend consecutive classes to improve.</p></div></div>
        </div>
      )}
      <div className="glass-card p-6 animate-slide-up" style={{animationDelay:'200ms',animationFillMode:'both'}}>
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2"><BookOpen size={20} className="text-accent" /> Subject-wise Attendance</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {data.subjects.map((s: any, i: number) => {
            const color = s.percentage >= 85 ? 'success' : s.percentage >= 75 ? 'warning' : 'danger';
            const colorClass = color === 'success' ? 'from-success/10 to-success/5 border-success/30' : color === 'warning' ? 'from-warning/10 to-warning/5 border-warning/30' : 'from-danger/10 to-danger/5 border-danger/30';
            const textColor = color === 'success' ? 'text-success' : color === 'warning' ? 'text-warning' : 'text-danger';
            return (
              <div key={i} className={"p-4 rounded-xl border bg-gradient-to-br " + colorClass + " animate-slide-up"} style={{animationDelay: (i+3)*50+'ms',animationFillMode:'both'}}>
                <p className="text-xs text-slate-400 mb-1">{s.code}</p>
                <h4 className="font-semibold text-white mb-2">{s.name}</h4>
                <p className={"text-2xl font-bold " + textColor}>{s.percentage}%</p>
                <div className="mt-3 h-2 bg-slate-700 rounded-full overflow-hidden"><div className={"h-full " + (color === 'success' ? 'bg-success' : color === 'warning' ? 'bg-warning' : 'bg-danger')} style={{width: s.percentage+'%'}} /></div>
                <p className="text-xs text-slate-400 mt-2">{s.present}/{s.total} classes</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}