'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { Building2, Plus, X, Users, Trash2 } from 'lucide-react';

export default function ClassesPage() {
  const { loading: al } = useAuth(['admin']);
  const [classes, setClasses] = useState<any[]>([]);
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ name: '', code: '', department: 'Engineering' });
  const [loading, setLoading] = useState(true);
  const fetchClasses = () => api.get('/classes').then((r: any) => setClasses(r.data || [])).catch(() => {});
  useEffect(() => { if (!al) { fetchClasses(); setLoading(false); } }, [al]);
  const handleAdd = async () => { await api.post('/classes', form); setModal(false); setForm({ name: '', code: '', department: 'Engineering' }); fetchClasses(); };
  const handleDelete = async (id: number) => {
    if (!confirm('Delete this class?')) return;
    await api.delete(`/classes/${id}`).then(() => fetchClasses()).catch(() => {});
  };
  if (al || loading) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold text-white">Classes</h1><p className="text-slate-400">{classes.length} classes</p></div><button onClick={() => setModal(true)} className="btn-primary flex items-center gap-2"><Plus size={16} /> Add Class</button></div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {classes.map((c: any, i: number) => (
          <div key={c.id} className="glass-card glass-card-hover p-5" style={{ animationDelay: i*50+'ms', animationFillMode: 'both' }}>
            <div className="flex items-center justify-between mb-3"><div className="flex items-center gap-3"><div className="w-10 h-10 rounded-xl bg-warning/20 flex items-center justify-center text-warning"><Building2 size={20} /></div><div><h3 className="font-semibold text-white">{c.name}</h3><p className="text-xs text-slate-400">{c.code} &middot; {c.department}</p></div></div><button onClick={() => handleDelete(c.id)} className="text-slate-400 hover:text-danger transition-colors"><Trash2 size={16} /></button></div>
          </div>
        ))}
      </div>
      {modal && (<div className="modal-overlay" onClick={() => setModal(false)}><div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4"><h2 className="text-lg font-bold text-white">Add Class</h2><button onClick={() => setModal(false)} className="text-slate-400 hover:text-white"><X size={20} /></button></div>
        <div className="space-y-3">
          <div><label className="text-xs text-slate-400 mb-1 block">Class Name</label><input className="input-field" value={form.name} onChange={e => setForm({...form, name: e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-3"><div><label className="text-xs text-slate-400 mb-1 block">Code</label><input className="input-field" value={form.code} onChange={e => setForm({...form, code: e.target.value})} /></div><div><label className="text-xs text-slate-400 mb-1 block">Department</label><input className="input-field" value={form.department} onChange={e => setForm({...form, department: e.target.value})} /></div></div>
          <button onClick={handleAdd} className="btn-primary w-full py-3">Add Class</button>
        </div></div></div>)}
    </div>
  );
}