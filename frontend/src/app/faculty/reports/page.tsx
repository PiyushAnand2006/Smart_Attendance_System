'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { FileText } from 'lucide-react';

export default function FacultyReportsPage() {
  const { loading: al } = useAuth(['faculty', 'admin']);
  const [report, setReport] = useState<any>(null);
  useEffect(() => { if (!al) api.get('/reports/monthly').then((r: any) => setReport(r.data)); }, [al]);
  if (al) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Reports</h1><p className="text-slate-400">Attendance overview</p></div>
      {report && <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card glass-card-hover p-5 animate-slide-up"><p className="text-xs text-slate-400">Overall</p><p className="text-3xl font-bold text-accent mt-1">{report.summary?.percentage}%</p></div>
        <div className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay:'50ms',animationFillMode:'both'}}><p className="text-xs text-slate-400">Present</p><p className="text-3xl font-bold text-success mt-1">{report.summary?.present}</p></div>
        <div className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay:'100ms',animationFillMode:'both'}}><p className="text-xs text-slate-400">Absent</p><p className="text-3xl font-bold text-danger mt-1">{report.summary?.absent}</p></div>
      </div>}
      {report?.subjects?.map((s: any, i: number) => (
        <div key={i} className="glass-card p-4 flex items-center gap-4 animate-slide-up" style={{animationDelay: (i+3)*50+'ms',animationFillMode:'both'}}>
          <div className="w-16 text-center"><p className="text-xs text-accent font-bold">{s.code}</p></div>
          <div className="flex-1"><div className="h-2 bg-slate-700 rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-accent to-highlight rounded-full" style={{width: s.percentage+'%'}} /></div></div>
          <span className="text-sm font-bold text-white w-12 text-right">{s.percentage}%</span>
        </div>
      ))}
    </div>
  );
}