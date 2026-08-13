'use client';
import { useState, useEffect } from 'react';
import { Users, GraduationCap, BookOpen, TrendingUp, AlertCircle, MessageSquare, Building2, ClipboardCheck, Activity } from 'lucide-react';
import StatCard from '@/components/StatCard';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';

export default function AdminDashboard() {
  const { user, loading: authLoading } = useAuth(['admin']);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authLoading) return;
    api.get('/admin/dashboard').then((r: any) => { setStats(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, [authLoading]);

  if (authLoading || loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;
  if (!stats) return <div className="glass-card p-8 text-center text-danger">Failed to load dashboard</div>;

  const activities = [
    { time: 'Just now', text: 'System online', type: 'success' },
    { time: '09:02 AM', text: 'Attendance session started for DBMS - CSE-A', type: 'success' },
    { time: '09:05 AM', text: `WhatsApp notifications sent to ${stats.today_present || 0} parents`, type: 'info' },
    { time: '09:15 AM', text: `Low attendance alert for ${stats.low_attendance_count || 0} students`, type: 'warning' },
  ];

  const actions = [
    { label: 'Add Student', href: '/admin/students', icon: Users, color: 'from-accent/20 to-accent/5 border-accent/30' },
    { label: 'Add Faculty', href: '/admin/faculty', icon: GraduationCap, color: 'from-info/20 to-info/5 border-info/30' },
    { label: 'View Reports', href: '/admin/reports', icon: BookOpen, color: 'from-success/20 to-success/5 border-success/30' },
    { label: 'Templates', href: '/admin/templates', icon: MessageSquare, color: 'from-warning/20 to-warning/5 border-warning/30' },
  ];

  const dotColor = (t: string) => t === 'success' ? 'bg-success' : t === 'warning' ? 'bg-warning' : 'bg-info';

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard label="Total Students" value={stats.total_students} icon={<Users size={24} />} color="accent" delay={0} />
        <StatCard label="Total Faculty" value={stats.total_faculty} icon={<GraduationCap size={24} />} color="info" delay={50} />
        <StatCard label="Classes" value={stats.total_classes} icon={<Building2 size={24} />} color="warning" delay={100} />
        <StatCard label="Attendance Rate" value={stats.avg_attendance + '%'} icon={<TrendingUp size={24} />} color="success" delay={150} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard label="Present Today" value={stats.today_present} icon={<ClipboardCheck size={24} />} color="success" delay={200} />
        <StatCard label="Low Attendance" value={stats.low_attendance_count} icon={<AlertCircle size={24} />} color="warning" delay={250} />
        <StatCard label="WhatsApp Sent" value={stats.whatsapp_sent} icon={<MessageSquare size={24} />} color="info" delay={300} />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '350ms', animationFillMode: 'both' }}>
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2"><Activity size={18} className="text-accent" /> Recent Activity</h3>
          <div className="space-y-3">
            {activities.map((item, idx) => (
              <div key={idx} className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-xl hover:bg-slate-800/70 transition-colors">
                <div className={`w-2 h-2 rounded-full ${dotColor(item.type)} shrink-0`} />
                <div className="flex-1 min-w-0"><p className="text-sm text-slate-200 truncate">{item.text}</p><p className="text-xs text-slate-500">{item.time}</p></div>
              </div>
            ))}
          </div>
        </div>
        <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '400ms', animationFillMode: 'both' }}>
          <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 gap-3">
            {actions.map((action, idx) => {
              const Icon = action.icon;
              return (
                <a key={idx} href={action.href} className={`flex flex-col items-center gap-3 p-5 rounded-xl bg-gradient-to-br ${action.color} border hover:scale-105 hover:shadow-lg transition-all duration-300 group`}>
                  <Icon size={24} className="text-accent group-hover:scale-110 transition-transform duration-300" />
                  <span className="text-sm text-slate-200 font-medium">{action.label}</span>
                </a>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
