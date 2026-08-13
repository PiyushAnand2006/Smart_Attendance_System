'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { BookOpen } from 'lucide-react';

export default function SubjectsPage() {
  const { loading: al } = useAuth(['student']);
  const [subjects, setSubjects] = useState<any[]>([]);
  useEffect(() => { if (!al) api.get('/students/my-dashboard').then((r: any) => setSubjects(r.data?.subjects || [])); }, [al]);
  if (al) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Subject Attendance</h1><p className="text-slate-400">{subjects.length} subjects</p></div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {subjects.map((s: any, i: number) => {
          const color = s.percentage >= 85 ? 'success' : s.percentage >= 75 ? 'warning' : 'danger';
          return (
            <div key={i} className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay: i*80+'ms',animationFillMode:'both'}}>
              <div className="flex items-center justify-between mb-3"><div className="flex items-center gap-2"><BookOpen size={16} className="text-accent" /><span className="text-xs text-accent font-bold">{s.code}</span></div><span className={"text-2xl font-bold "+(color==='success'?'text-success':color==='warning'?'text-warning':'text-danger')}>{s.percentage}%</span></div>
              <h3 className="font-semibold text-white mb-2">{s.name}</h3>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden"><div className={"h-full "+(color==='success'?'bg-success':color==='warning'?'bg-warning':'bg-danger')} style={{width: s.percentage+'%'}} /></div>
              <p className="text-xs text-slate-400 mt-2">{s.present}/{s.total} classes attended</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}