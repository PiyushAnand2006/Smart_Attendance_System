'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { QrCode } from 'lucide-react';

export default function FacultyStudentsPage() {
  const { loading: al } = useAuth(['faculty', 'admin']);
  const [students, setStudents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { if (!al) { api.get('/faculty/students').then((r: any) => { setStudents(r.data || []); setLoading(false); }); } }, [al]);
  if (al || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">My Students</h1><p className="text-slate-400">{students.length} students</p></div>
      <div className="glass-card overflow-hidden">
        <table className="w-full"><thead><tr className="text-left text-xs text-slate-400 border-b border-slate-700"><th className="p-4">Student</th><th className="p-4">ID</th><th className="p-4">QR</th></tr></thead>
        <tbody>{students.map((s: any) => (
          <tr key={s.id} className="table-row-hover">
            <td className="p-4"><div className="flex items-center gap-3"><div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-highlight flex items-center justify-center text-white text-xs font-bold">{s.first_name?.[0]}</div><span className="text-white text-sm">{s.full_name || s.first_name}</span></div></td>
            <td className="p-4 text-slate-300 text-sm">{s.student_id}</td>
            <td className="p-4">{s.qr ? <QrCode size={16} className="text-success" /> : <QrCode size={16} className="text-slate-500" />}</td>
          </tr>
        ))}</tbody></table>
      </div>
    </div>
  );
}