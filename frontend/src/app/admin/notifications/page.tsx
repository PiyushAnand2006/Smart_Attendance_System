'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { Bell, Send, RefreshCw } from 'lucide-react';

export default function NotificationsPage() {
  const { loading: al } = useAuth(['admin']);
  const [queue, setQueue] = useState<any[]>([]);
  const [processing, setProcessing] = useState(false);
  const fetchQueue = () => api.get('/notifications/queue').then((r: any) => setQueue(r.data || []));
  useEffect(() => { if (!al) fetchQueue(); }, [al]);
  const processQueue = async () => { setProcessing(true); await api.post('/notifications/process'); fetchQueue(); setProcessing(false); };
  if (al) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold text-white">Notification Queue</h1><p className="text-slate-400">{queue.length} notifications</p></div>
      <div className="flex gap-2"><button onClick={fetchQueue} className="btn-secondary flex items-center gap-2"><RefreshCw size={16} /> Refresh</button><button onClick={processQueue} disabled={processing} className="btn-primary flex items-center gap-2"><Send size={16} /> {processing ? 'Processing...' : 'Process All'}</button></div></div>
      <div className="glass-card overflow-hidden">
        <table className="w-full"><thead><tr className="text-left text-xs text-slate-400 border-b border-slate-700"><th className="p-4">To</th><th className="p-4">Message</th><th className="p-4">Status</th><th className="p-4">Time</th></tr></thead>
        <tbody>{queue.map((n: any, i: number) => (<tr key={i} className="table-row-hover"><td className="p-4 text-slate-300 text-sm">{n.recipient_number}</td><td className="p-4 text-slate-200 text-sm">{n.message}</td><td className="p-4"><span className={n.status==='SENT' ? 'badge-success' : 'badge-warning'}>{n.status}</span></td><td className="p-4 text-slate-400 text-xs">{n.created_at?.split('T')[0]}</td></tr>))}</tbody></table>
      </div>
    </div>
  );
}