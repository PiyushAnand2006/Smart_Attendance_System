'use client';
import { useAuth } from '@/hooks/useAuth';
import { Settings, Shield, Bell, Database, Save } from 'lucide-react';

export default function SettingsPage() {
  const { loading: al } = useAuth(['admin']);
  if (al) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-white">Settings</h1><p className="text-slate-400">System configuration</p></div>
      <div className="glass-card p-6 space-y-6">
        <h3 className="font-semibold text-white flex items-center gap-2"><Shield size={18} className="text-accent" /> Attendance Settings</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div><label className="text-xs text-slate-400 mb-1 block">Minimum Attendance Threshold (%)</label><input className="input-field" defaultValue="75" type="number" /></div>
          <div><label className="text-xs text-slate-400 mb-1 block">Late Threshold (minutes)</label><input className="input-field" defaultValue="15" type="number" /></div>
          <div><label className="text-xs text-slate-400 mb-1 block">QR Token Expiry (seconds)</label><input className="input-field" defaultValue="300" type="number" /></div>
          <div><label className="text-xs text-slate-400 mb-1 block">Face Recognition Tolerance</label><input className="input-field" defaultValue="0.6" step="0.1" type="number" /></div>
        </div>
        <div className="border-t border-slate-700 pt-4"><h3 className="font-semibold text-white flex items-center gap-2 mb-4"><Bell size={18} className="text-accent" /> Notification Settings</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="text-xs text-slate-400 mb-1 block">WhatsApp Mode</label><select className="input-field text-white"><option value="mock">Mock (No real messages)</option><option value="cloud_api">Cloud API</option></select></div>
            <div><label className="text-xs text-slate-400 mb-1 block">Retry Attempts</label><input className="input-field" defaultValue="3" type="number" /></div>
          </div>
        </div>
        <button className="btn-primary flex items-center gap-2"><Save size={16} /> Save Settings</button>
      </div>
    </div>
  );
}