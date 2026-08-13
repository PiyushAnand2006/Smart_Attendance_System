'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { Bell } from 'lucide-react';

export default function NotificationsPage() {
  const { loading: al } = useAuth(['student']);
  const [queue, setQueue] = useState<any[]>([]);
  useEffect(() => { if (!al) api.get('/notifications/queue').then((r: any) => setQueue(r.data || [])); }, [al]);
  if (al) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  const mine = queue.filter((n: any) => n.status === 'SENT');
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Notifications</h1><p className="text-slate-400">{mine.length} notifications</p></div>
      <div className="space-y-3">
        {mine.map((n: any, i: number) => (
          <div key={i} className="glass-card glass-card-hover p-4 flex items-start gap-3 animate-slide-up" style={{animationDelay: i*30+'ms',animationFillMode:'both'}}>
            <Bell size={16} className="text-accent mt-0.5 shrink-0" /><div><p className="text-sm text-white">{n.message}</p><p className="text-xs text-slate-400 mt-1">{n.created_at?.split('T')[0]}</p></div>
          </div>
        ))}
        {mine.length === 0 && <div className="glass-card p-8 text-center text-slate-400">No notifications yet</div>}
      </div>
    </div>
  );
}