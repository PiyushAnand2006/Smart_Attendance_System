'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { FileText, Calendar, Download, BarChart3 } from 'lucide-react';

export default function ReportsPage() {
  const { loading: al } = useAuth(['admin']);
  const [daily, setDaily] = useState<any>(null);
  const [monthly, setMonthly] = useState<any>(null);
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  useEffect(() => { if (!al) { api.get('/reports/daily?date=' + date).then((r: any) => setDaily(r.data)); api.get('/reports/monthly').then((r: any) => setMonthly(r.data)); } }, [al, date]);
  if (al) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Reports</h1><p className="text-slate-400">Attendance analytics & reports</p></div>
      <div className="glass-card p-4"><div className="flex items-center gap-3"><Calendar size={16} className="text-accent" /><input type="date" value={date} onChange={e => setDate(e.target.value)} className="input-field w-auto" /></div></div>
      {daily && (<div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card glass-card-hover p-5 animate-slide-up"><p className="text-xs text-slate-400">Date</p><p className="text-lg font-bold text-white mt-1">{daily.report_date}</p></div>
        <div className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay:'50ms',animationFillMode:'both'}}><p className="text-xs text-slate-400">Total</p><p className="text-lg font-bold text-white mt-1">{daily.total}</p></div>
        <div className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay:'100ms',animationFillMode:'both'}}><p className="text-xs text-slate-400">Present</p><p className="text-lg font-bold text-success mt-1">{daily.present}</p></div>
        <div className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay:'150ms',animationFillMode:'both'}}><p className="text-xs text-slate-400">Rate</p><p className="text-lg font-bold text-accent mt-1">{daily.rate}%</p></div>
      </div>)}
      {monthly && monthly.subjects && monthly.subjects.length > 0 && (<div className="glass-card p-6 animate-slide-up" style={{animationDelay:'200ms',animationFillMode:'both'}}>
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2"><BarChart3 size={18} className="text-accent" /> Subject-wise Attendance</h3>
        <div className="space-y-3">{monthly.subjects.map((s: any, i: number) => (
          <div key={i} className="flex items-center gap-4 p-3 bg-slate-800/40 rounded-xl">
            <div className="w-12 text-center"><p className="text-xs text-slate-400">{s.code}</p></div>
            <div className="flex-1"><div className="flex items-center justify-between mb-1"><span className="text-sm text-white">{s.name}</span><span className="text-sm font-medium text-accent">{s.percentage}%</span></div><div className="h-2 bg-slate-700 rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-accent to-highlight rounded-full transition-all duration-500" style={{width: s.percentage+'%'}}/></div></div>
          </div>
        ))}</div>
      </div>)}
    </div>
  );
}