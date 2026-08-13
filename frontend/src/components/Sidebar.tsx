'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Users, BookOpen, Calendar, ClipboardCheck, FileText, Bell, Settings, BarChart3, UserCheck, GraduationCap, Building2, Mail, QrCode, Calculator, History, Scan } from 'lucide-react';
import { useState } from 'react';

interface SidebarProps { role: 'admin' | 'faculty' | 'student'; }

const menuItems: Record<string, { href: string; label: string; icon: any }[]> = {
  admin: [
    { href: '/admin/dashboard', label: 'Dashboard', icon: Home },
    { href: '/admin/students', label: 'Students', icon: Users },
    { href: '/admin/faculty', label: 'Faculty', icon: GraduationCap },
    { href: '/admin/classes', label: 'Classes', icon: Building2 },
    { href: '/admin/subjects', label: 'Subjects', icon: BookOpen },
    { href: '/admin/reports', label: 'Reports', icon: FileText },
    { href: '/admin/notifications', label: 'Notifications', icon: Bell },
    { href: '/admin/templates', label: 'Templates', icon: Mail },
    { href: '/admin/settings', label: 'Settings', icon: Settings },
  ],
  faculty: [
    { href: '/faculty/dashboard', label: 'Dashboard', icon: Home },
    { href: '/faculty/schedule', label: 'Schedule', icon: Calendar },
    { href: '/faculty/attendance', label: 'Attendance', icon: ClipboardCheck },
    { href: '/faculty/students', label: 'Students', icon: GraduationCap },
    { href: '/faculty/history', label: 'History', icon: History },
    { href: '/faculty/reports', label: 'Reports', icon: FileText },
  ],
  student: [
    { href: '/student/dashboard', label: 'Dashboard', icon: Home },
    { href: '/student/attendance', label: 'Scan QR', icon: QrCode },
    { href: '/student/subjects', label: 'Subjects', icon: BookOpen },
    { href: '/student/history', label: 'History', icon: History },
    { href: '/student/calculator', label: 'Calculator', icon: Calculator },
    { href: '/student/reports', label: 'Reports', icon: FileText },
    { href: '/student/notifications', label: 'Alerts', icon: Bell },
    { href: '/student/profile', label: 'Profile', icon: UserCheck },
  ],
};

export default function Sidebar({ role }: SidebarProps) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const items = menuItems[role] || [];

  return (
    <aside className={`fixed left-0 top-0 h-screen bg-primary border-r border-slate-700/50 z-50 transition-all duration-300 flex flex-col ${collapsed ? 'w-16' : 'w-64'}`}>
      <div className="p-5 border-b border-slate-700/50 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-accent to-highlight flex items-center justify-center animate-pulse-glow shrink-0">
          <Scan size={18} className="text-white" />
        </div>
        {!collapsed && (
          <div className="animate-fade-in">
            <h1 className="text-xl font-bold gradient-text">SmartAttend</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-wider">{role} Portal</p>
          </div>
        )}
      </div>

      <button onClick={() => setCollapsed(!collapsed)} className="mx-3 mt-3 mb-1 px-3 py-1.5 text-xs text-slate-500 hover:text-accent hover:bg-accent/10 rounded-lg transition-all text-left">
        {collapsed ? '>>' : '<< Collapse'}
      </button>

      <nav className="flex-1 px-3 space-y-0.5 overflow-y-auto" style={{ height: 'calc(100vh - 160px)' }}>
        {items.map((item, i) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-300 group relative overflow-hidden
                ${isActive
                  ? 'bg-accent/15 text-accent border-l-2 border-accent'
                  : 'text-slate-400 hover:bg-slate-700/30 hover:text-white'}`}
              style={{ animationDelay: `${i * 30}ms`, animationFillMode: 'both' }}>
              {isActive && <div className="absolute inset-0 bg-gradient-to-r from-accent/10 to-transparent" />}
              <Icon size={18} className={`shrink-0 transition-transform duration-300 group-hover:scale-110 ${isActive ? 'text-accent' : ''}`} />
              {!collapsed && <span className="text-sm font-medium relative z-10">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="p-3 border-t border-slate-700/50">
        <button onClick={() => { localStorage.clear(); window.location.href = '/login'; }}
          className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-slate-400 hover:text-danger hover:bg-danger/10 rounded-xl transition-all duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          {!collapsed && <span>Sign Out</span>}
        </button>
      </div>
    </aside>
  );
}
