'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { BookOpen, Plus, X, Edit, Trash2 } from 'lucide-react';

export default function SubjectsPage() {
  const { loading: al } = useAuth(['admin']);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ name: '', code: '', department: 'CSE', credits: 3 });
  const [loading, setLoading] = useState(true);
  const fetch = () => api.get('/subjects').then((r: any) => setSubjects(r.data || []));
  useEffect(() => { if (!al) { fetch(); setLoading(false); } }, [al]);
  const handleAdd = async () => { await api.post('/subjects', form); setModal(false); setForm({ name: '', code: '', department: 'CSE', credits: 3 }); fetch(); };
  if (al || loading) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold text-white">Subjects</h1><p className="text-slate-400">{subjects.length} subjects</p></div><button onClick={() => setModal(true)} className="btn-primary flex items-center gap-2"><Plus size={16} /> Add Subject</button></div>
      <div className="glass-card overflow-hidden">
        <table className="w-full"><thead><tr className="text-left text-xs text-slate-400 border-b border-slate-700"><th className="p-4">Subject</th><th className="p-4">Code</th><th className="p-4">Dept</th><th className="p-4">Credits</th></tr></thead>
        <tbody>{subjects.map((s: any) => (<tr key={s.id} className="table-row-hover"><td className="p-4"><div className="flex items-center gap-3"><div className="w-8 h-8 rounded-lg bg-info/20 flex items-center justify-center text-info"><BookOpen size={14} /></div><span className="text-white text-sm font-medium">{s.name}</span></div></td><td className="p-4 text-slate-300 text-sm">{s.code}</td><td className="p-4 text-slate-300 text-sm">{s.department}</td><td className="p-4 text-slate-300 text-sm">{s.credits}</td></tr>))}</tbody></table>
      </div>
      {modal && (<div className="modal-overlay" onClick={() => setModal(false)}><div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4"><h2 className="text-lg font-bold text-white">Add Subject</h2><button onClick={() => setModal(false)} className="text-slate-400 hover:text-white"><X size={20} /></button></div>
        <div className="space-y-3">
          <div><label className="text-xs text-slate-400 mb-1 block">Name</label><input className="input-field" value={form.name} onChange={e => setForm({...form, name: e.target.value})} /></div>
          <div className="grid grid-cols-3 gap-3"><div><label className="text-xs text-slate-400 mb-1 block">Code</label><input className="input-field" value={form.code} onChange={e => setForm({...form, code: e.target.value})} /></div><div><label className="text-xs text-slate-400 mb-1 block">Credits</label><input type="number" className="input-field" value={form.credits} onChange={e => setForm({...form, credits: +e.target.value})} /></div><div><label className="text-xs text-slate-400 mb-1 block">Dept</label><input className="input-field" value={form.department} onChange={e => setForm({...form, department: e.target.value})} /></div></div>
          <button onClick={handleAdd} className="btn-primary w-full py-3">Add Subject</button>
        </div></div></div>)}
    </div>
  );
}