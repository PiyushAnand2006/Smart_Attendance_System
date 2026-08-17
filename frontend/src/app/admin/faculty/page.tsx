'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { GraduationCap, Building, Mail, User, Trash2, X, Plus } from 'lucide-react';

export default function FacultyPage() {
  const { loading: al } = useAuth(['admin']);
  const [faculty, setFaculty] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFaculty = () => api.get('/admin/faculty').then((r: any) => setFaculty(r.data || [])).catch(() => {});
  useEffect(() => { if (!al) { fetchFaculty(); setLoading(false); } }, [al]);
  if (al || loading) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this faculty member?')) return;
    await api.delete(`/admin/faculty/${id}`).then(() => fetchFaculty()).catch(() => {});
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-white">Faculty</h1><p className="text-slate-400">{faculty.length} faculty members</p></div>
      </div>
      <div className="glass-card overflow-hidden">
        <table className="w-full"><thead><tr className="text-left text-xs text-slate-400 border-b border-slate-700"><th className="p-4">Faculty</th><th className="p-4">ID</th><th className="p-4">Email</th><th className="p-4">Department</th><th className="p-4">Status</th><th className="p-4 text-right">Actions</th></tr></thead>
        <tbody>{faculty.map((f: any, i: number) => (
          <tr key={f.id} className="table-row-hover" style={{ animationDelay: i*40+'ms', animationFillMode: 'both' }}>
            <td className="p-4"><div className="flex items-center gap-3"><div className="w-8 h-8 rounded-lg bg-info/20 flex items-center justify-center text-info"><GraduationCap size={16} /></div><span className="text-white text-sm font-medium">{f.full_name || f.first_name} {f.last_name}</span></div></td>
            <td className="p-4 text-slate-300 text-sm">{f.faculty_id}</td>
            <td className="p-4 text-slate-300 text-sm"><Mail size={14} className="inline mr-1" />{f.email || '—'}</td>
            <td className="p-4 text-slate-300 text-sm"><Building size={14} className="inline mr-1" />{f.department || '—'}</td>
            <td className="p-4"><span className={f.is_active ? 'badge-success' : 'badge-danger'}>{f.is_active ? 'Active' : 'Inactive'}</span></td>
            <td className="p-4 text-right"><button onClick={() => handleDelete(f.id)} className="text-slate-400 hover:text-danger transition-colors"><Trash2 size={16} /></button></td>
          </tr>
        ))}</tbody></table>
        {faculty.length === 0 && <div className="p-8 text-center text-slate-400">No faculty members found. Register faculty via the registration page with role &quot;faculty&quot;.</div>}
      </div>
    </div>
  );
}