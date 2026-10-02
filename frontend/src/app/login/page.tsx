'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, LogIn, UserPlus, Sparkles, Shield, GraduationCap, BookOpen } from 'lucide-react';
import Link from 'next/link';

const ROLES = [
  { key: 'student', label: 'Student', icon: GraduationCap, email: 'student@smartattend.com', password: 'student123' },
  { key: 'admin', label: 'Admin', icon: Shield, email: 'admin@smartattend.com', password: 'admin123' },
  { key: 'faculty', label: 'Teacher', icon: BookOpen, email: 'faculty@smartattend.com', password: 'faculty123' },
] as const;

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: '', password: '' });
  const [role, setRole] = useState<string>('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPwd, setShowPwd] = useState(false);

  const selectRole = (r: typeof ROLES[number]) => {
    setRole(r.key);
    setForm({ email: r.email, password: r.password });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, role }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.message || 'Login failed');
      localStorage.setItem('token', data.data.access_token);
      localStorage.setItem('user', JSON.stringify(data.data.user));
      localStorage.setItem('role', data.data.role);
      router.push(`/${data.data.role}/dashboard`);
    } catch (err: any) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-dark via-primary to-primary p-4 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/3 left-1/3 w-72 h-72 bg-accent/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 right-1/3 w-72 h-72 bg-highlight/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>
      <div className="w-full max-w-md relative animate-slide-up">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-accent to-highlight mb-4 animate-pulse-glow">
            <Sparkles size={28} className="text-white" />
          </div>
          <h1 className="text-4xl font-bold gradient-text mb-2">SmartAttend</h1>
          <p className="text-slate-400">Sign in to your account</p>
        </div>
        <form onSubmit={handleSubmit} className="glass-card p-8 space-y-5">
          {error && (
            <div className="p-3 rounded-lg bg-danger/20 border border-danger/50 text-danger text-sm animate-scale-in">{error}</div>
          )}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Sign in as</label>
            <div className="grid grid-cols-3 gap-2">
              {ROLES.map((r) => {
                const Icon = r.icon;
                const active = role === r.key;
                return (
                  <button key={r.key} type="button" onClick={() => selectRole(r)}
                    className={`flex flex-col items-center gap-1.5 py-3 px-2 rounded-xl border text-sm font-medium transition-all duration-200 ${
                      active
                        ? 'bg-accent/20 border-accent text-accent shadow-lg shadow-accent/20'
                        : 'bg-white/5 border-white/10 text-slate-400 hover:border-accent/50 hover:text-slate-200'
                    }`}>
                    <Icon size={20} />
                    {r.label}
                  </button>
                );
              })}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Email</label>
            <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="input-field" placeholder="admin@smartattend.com" required />
          </div>
          <div className="relative">
            <label className="block text-sm font-medium text-slate-300 mb-2">Password</label>
            <input type={showPwd ? 'text' : 'password'} value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="input-field pr-12" placeholder="Enter password" required />
            <button type="button" onClick={() => setShowPwd(!showPwd)}
              className="absolute right-3 top-9 text-slate-400 hover:text-accent transition-colors">
              {showPwd ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
          <button type="submit" disabled={loading}
            className="btn-primary w-full py-3.5 text-base flex items-center justify-center gap-2 disabled:opacity-50">
            {loading ? <span className="animate-spin">&#9696;</span> : <LogIn size={18} />}
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
          <div className="text-center space-y-2 pt-2">
            <p className="text-sm text-slate-400">
              Demo: <span className="text-accent">admin@smartattend.com</span> / <span className="text-slate-300">admin123</span>
            </p>
            <p className="text-sm text-slate-500">
              No account? <Link href="/register" className="text-accent hover:underline font-medium">Create one</Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
