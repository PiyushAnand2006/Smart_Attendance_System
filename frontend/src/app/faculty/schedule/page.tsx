'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { Calendar as CalIcon, Plus, X, Play, CheckCircle } from 'lucide-react';

export default function SchedulePage() {
  const { loading: al, user } = useAuth(['faculty', 'admin']);
  const router = useRouter();
  const [schedule, setSchedule] = useState<any[]>([]);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [classes, setClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ subject_id: '', class_id: '', mode: 'QR', scheduled_date: '' });

  const fetchSchedule = () => api.get('/faculty/schedule').then((r: any) => setSchedule(r.data || [])).catch(() => {});
  const fetchLookups = () => {
    api.get('/subjects').then((r: any) => setSubjects(r.data || [])).catch(() => {});
    api.get('/classes').then((r: any) => setClasses(r.data || [])).catch(() => {});
  };
  useEffect(() => { if (!al) { fetchSchedule(); fetchLookups(); setLoading(false); } }, [al]);
  if (al || loading) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;

  const handleSchedule = async () => {
    if (!form.subject_id || !form.class_id) { alert('Subject and Class are required'); return; }
    await api.post('/faculty/schedule', { ...form, faculty_id: user?.user_id });
    setModal(false);
    setForm({ subject_id: '', class_id: '', mode: 'QR', scheduled_date: '' });
    fetchSchedule();
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-white">Schedule</h1><p className="text-slate-400">{schedule.length} classes scheduled</p></div>
        <button onClick={() => setModal(true)} className="btn-primary flex items-center gap-2"><Plus size={16} /> Schedule Class</button>
      </div>
      <div className="space-y-3">
        {schedule.map((s: any, i: number) => (
          <div key={s.id} className="glass-card glass-card-hover p-5 animate-slide-up" style={{animationDelay: i*50+'ms',animationFillMode:'both'}}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3"><CalIcon size={20} className="text-accent" /><div><h3 className="font-semibold text-white">{s.subject?.name || 'Subject'}</h3><p className="text-xs text-slate-400">{s.attendance_mode} mode &middot; {s.scheduled_date || 'Today'}</p></div></div>
              <div className="flex items-center gap-3">
                <span className={s.status==='completed' ? 'badge-success' : s.status==='active' ? 'badge-info' : 'badge-warning'}>{s.status}</span>
                {s.status !== 'completed' && (
                  <button onClick={() => router.push(`/faculty/attendance/qr?session=${s.id}`)}
                    className="btn-primary text-xs py-1.5 px-3 flex items-center gap-1.5">
                    <Play size={12} /> {s.status === 'active' ? 'Open QR' : 'Start'}
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
        {schedule.length === 0 && <div className="glass-card p-8 text-center text-slate-400">No classes scheduled today</div>}
      </div>
      {modal && (<div className="modal-overlay" onClick={() => setModal(false)}><div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4"><h2 className="text-lg font-bold text-white">Schedule Class</h2><button onClick={() => setModal(false)} className="text-slate-400 hover:text-white"><X size={20} /></button></div>
        <div className="space-y-3">
          <div><label className="text-xs text-slate-400 mb-1 block">Subject</label><select className="input-field" value={form.subject_id} onChange={e => setForm({...form, subject_id: e.target.value})}><option value="">Select subject</option>{subjects.map((s: any) => <option key={s.id} value={s.id}>{s.name} ({s.code})</option>)}</select></div>
          <div><label className="text-xs text-slate-400 mb-1 block">Class</label><select className="input-field" value={form.class_id} onChange={e => setForm({...form, class_id: e.target.value})}><option value="">Select class</option>{classes.map((c: any) => <option key={c.id} value={c.id}>{c.name} ({c.code})</option>)}</select></div>
          <div className="grid grid-cols-2 gap-3"><div><label className="text-xs text-slate-400 mb-1 block">Mode</label><select className="input-field" value={form.mode} onChange={e => setForm({...form, mode: e.target.value})}><option value="QR">QR</option><option value="MANUAL">Manual</option></select></div><div><label className="text-xs text-slate-400 mb-1 block">Date</label><input type="date" className="input-field" value={form.scheduled_date} onChange={e => setForm({...form, scheduled_date: e.target.value})} /></div></div>
          <button onClick={handleSchedule} className="btn-primary w-full py-3 flex items-center justify-center gap-2"><CheckCircle size={16} /> Schedule Class</button>
        </div></div></div>)}
    </div>
  );
}