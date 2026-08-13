'use client';
import { useState, useEffect } from 'react';
import { Plus, Search, Edit, Trash2, X, UserCheck, QrCode, Camera } from 'lucide-react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';

export default function StudentsPage() {
  const { loading: authLoading } = useAuth(['admin']);
  const [students, setStudents] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ first_name: '', last_name: '', roll_number: '', department: 'CSE' });
  const [loading, setLoading] = useState(true);

  const fetchStudents = () => api.get('/students').then((r: any) => setStudents(r.data || [])).catch(() => {});
  useEffect(() => { if (!authLoading) { fetchStudents(); setLoading(false); } }, [authLoading]);

  const statusBadge = (s: string) => {
    if (s === 'ready' || s === 'READY') return 'badge-success';
    if (s === 'face_enrolled') return 'badge-info';
    if (s === 'incomplete' || s === 'INCOMPLETE') return 'badge-danger';
    return 'badge-warning';
  };

  const handleAdd = async () => {
    await api.post('/students', form);
    setModal(false); setForm({ first_name: '', last_name: '', roll_number: '', department: 'CSE' });
    fetchStudents();
  };

  const filtered = students.filter((s: any) => `${s.first_name} ${s.last_name} ${s.student_id}`.toLowerCase().includes(search.toLowerCase()));

  if (authLoading || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-white">Students</h1><p className="text-slate-400">{filtered.length} students</p></div>
        <button onClick={() => setModal(true)} className="btn-primary flex items-center gap-2"><Plus size={16} /> Add Student</button>
      </div>
      <div className="glass-card p-4">
        <div className="relative mb-4">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input className="input-field pl-10" placeholder="Search students..." value={search} onChange={e => setSearch(e.target.value)} />
        </div>
      </div>
      <div className="glass-card overflow-hidden">
        <table className="w-full"><thead><tr className="text-left text-xs text-slate-400 border-b border-slate-700"><th className="p-4">Student</th><th className="p-4">Roll No</th><th className="p-4">Dept</th><th className="p-4">Face</th><th className="p-4">QR</th><th className="p-4">Status</th></tr></thead>
        <tbody>{filtered.map((s: any) => (
          <tr key={s.id} className="table-row-hover">
            <td className="p-4"><div className="flex items-center gap-3"><div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-highlight flex items-center justify-center text-white text-xs font-bold">{s.first_name?.[0]}</div><span className="text-white text-sm font-medium">{s.first_name} {s.last_name}</span></div></td>
            <td className="p-4 text-slate-300 text-sm">{s.student_id}</td>
            <td className="p-4 text-slate-300 text-sm">{s.department}</td>
            <td className="p-4">{s.face ? <UserCheck size={16} className="text-success" /> : <Camera size={16} className="text-slate-500" />}</td>
            <td className="p-4">{s.qr ? <QrCode size={16} className="text-success" /> : <span className="text-slate-500 text-xs">No</span>}</td>
            <td className="p-4"><span className={statusBadge(s.status)}>{s.status}</span></td>
          </tr>
        ))}</tbody></table>
      </div>
      {modal && (<div className="modal-overlay" onClick={() => setModal(false)}><div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4"><h2 className="text-lg font-bold text-white">Add Student</h2><button onClick={() => setModal(false)} className="text-slate-400 hover:text-white"><X size={20} /></button></div>
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-3"><div><label className="text-xs text-slate-400 mb-1 block">First Name</label><input className="input-field" value={form.first_name} onChange={e => setForm({...form, first_name: e.target.value})} /></div><div><label className="text-xs text-slate-400 mb-1 block">Last Name</label><input className="input-field" value={form.last_name} onChange={e => setForm({...form, last_name: e.target.value})} /></div></div>
          <div className="grid grid-cols-2 gap-3"><div><label className="text-xs text-slate-400 mb-1 block">Roll Number</label><input className="input-field" value={form.roll_number} onChange={e => setForm({...form, roll_number: e.target.value})} /></div><div><label className="text-xs text-slate-400 mb-1 block">Department</label><input className="input-field" value={form.department} onChange={e => setForm({...form, department: e.target.value})} /></div></div>
          <button onClick={handleAdd} className="btn-primary w-full py-3">Add Student</button>
        </div></div></div>)}
    </div>
  );
}
