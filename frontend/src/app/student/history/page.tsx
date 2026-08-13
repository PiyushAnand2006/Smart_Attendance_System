'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { History, CheckCircle, XCircle } from 'lucide-react';

export default function StudentHistoryPage() {
  const { loading: al } = useAuth(['student']);
  const [records, setRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { if (!al) { api.get('/attendance/my-attendance').then((r: any) => { setRecords(r.data || []); setLoading(false); }).catch(() => setLoading(false)); } }, [al]);
  if (al || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Attendance History</h1><p className="text-slate-400">{records.length} records</p></div>
      <div className="glass-card overflow-hidden">
        <table className="w-full"><thead><tr className="text-left text-xs text-slate-400 border-b border-slate-700"><th className="p-4">Date</th><th className="p-4">Subject</th><th className="p-4">Method</th><th className="p-4">Status</th></tr></thead>
        <tbody>{records.map((r: any, i: number) => (
          <tr key={i} className="table-row-hover animate-fade-in" style={{animationDelay: i*20+'ms',animationFillMode:'both'}}>
            <td className="p-4 text-slate-300 text-sm">{r.attendance_date}</td>
            <td className="p-4 text-white text-sm">{r.subject_name || 'N/A'} <span className="text-slate-500">({r.subject_code})</span></td>
            <td className="p-4"><span className="badge-info">{r.attendance_method}</span></td>
            <td className="p-4">{r.status === 'PRESENT' ? <span className="badge-success flex items-center gap-1 w-fit"><CheckCircle size={12} /> Present</span> : <span className="badge-danger flex items-center gap-1 w-fit"><XCircle size={12} /> {r.status}</span>}</td>
          </tr>
        ))}</tbody></table>
      </div>
      {records.length === 0 && <div className="glass-card p-8 text-center text-slate-400">No attendance records yet</div>}
    </div>
  );
}