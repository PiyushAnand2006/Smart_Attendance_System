'use client';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';
import { Mail, Plus, X, Edit } from 'lucide-react';

export default function TemplatesPage() {
  const { loading: al } = useAuth(['admin']);
  const [templates, setTemplates] = useState<any[]>([]);
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ name: '', display_name: '', content: '' });
  const fetch = () => api.get('/notifications/templates').then((r: any) => setTemplates(r.data || []));
  useEffect(() => { if (!al) fetch(); }, [al]);
  const handleAdd = async () => { await api.post('/notifications/templates', form); setModal(false); setForm({ name: '', display_name: '', content: '' }); fetch(); };
  if (al) return <><div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div></>;
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold text-white">WhatsApp Templates</h1><p className="text-slate-400">{templates.length} templates</p></div><button onClick={() => setModal(true)} className="btn-primary flex items-center gap-2"><Plus size={16} /> Add Template</button></div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {templates.map((t: any, i: number) => (<div key={t.id} className="glass-card glass-card-hover p-5" style={{animationDelay: i*50+'ms', animationFillMode:'both'}}>
          <div className="flex items-center gap-2 mb-2"><Mail size={16} className="text-accent" /><h3 className="font-semibold text-white">{t.display_name || t.name}</h3></div>
          <p className="text-sm text-slate-400">{t.content}</p>
        </div>))}
      </div>
      {modal && (<div className="modal-overlay" onClick={() => setModal(false)}><div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4"><h2 className="text-lg font-bold text-white">New Template</h2><button onClick={() => setModal(false)} className="text-slate-400 hover:text-white"><X size={20} /></button></div>
        <div className="space-y-3">
          <div><label className="text-xs text-slate-400 mb-1 block">Name</label><input className="input-field" value={form.name} onChange={e => setForm({...form, name: e.target.value})} /></div>
          <div><label className="text-xs text-slate-400 mb-1 block">Display Name</label><input className="input-field" value={form.display_name} onChange={e => setForm({...form, display_name: e.target.value})} /></div>
          <div><label className="text-xs text-slate-400 mb-1 block">Content</label><textarea className="input-field h-24" value={form.content} onChange={e => setForm({...form, content: e.target.value})} /></div>
          <button onClick={handleAdd} className="btn-primary w-full py-3">Create Template</button>
        </div></div></div>)}
    </div>
  );
}