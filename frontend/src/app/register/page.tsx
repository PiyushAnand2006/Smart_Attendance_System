'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { UserPlus, Eye, EyeOff, Sparkles, ArrowLeft } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: '', password: '', confirmPassword: '', first_name: '', last_name: '', role: 'student' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPwd, setShowPwd] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setError('');
    if (form.password !== form.confirmPassword) { setError('Passwords do not match'); return; }
    if (form.password.length < 6) { setError('Password must be at least 6 characters'); return; }
    setLoading(true);
    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: form.email, password: form.password, first_name: form.first_name, last_name: form.last_name, role: form.role }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.message || 'Registration failed');
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
        <div className="absolute top-1/3 right-1/3 w-72 h-72 bg-accent/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 left-1/3 w-72 h-72 bg-highlight/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>
      <div className="w-full max-w-md relative animate-slide-up">
        <Link href="/login" className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-accent mb-6 transition-colors">
          <ArrowLeft size={16} /> Back to login
        </Link>
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-accent to-highlight mb-3 animate-pulse-glow">
            <Sparkles size={24} className="text-white" />
          </div>
          <h1 className="text-3xl font-bold gradient-text mb-1">Create Account</h1>
          <p className="text-slate-400">Join SmartAttend today</p>
        </div>
        <form onSubmit={handleSubmit} className="glass-card p-8 space-y-4">
          {error && <div className="p-3 rounded-lg bg-danger/20 border border-danger/50 text-danger text-sm animate-scale-in">{error}</div>}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">First Name</label>
              <input type="text" value={form.first_name} required onChange={(e) => setForm({...form, first_name: e.target.value})} className="input-field" placeholder="Rahul" />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Last Name</label>
              <input type="text" value={form.last_name} required onChange={(e) => setForm({...form, last_name: e.target.value})} className="input-field" placeholder="Sharma" />
            </div>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Email</label>
            <input type="email" value={form.email} required onChange={(e) => setForm({...form, email: e.target.value})} className="input-field" placeholder="you@college.edu" />
          </div>
          <div className="relative">
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Password</label>
            <input type={showPwd ? 'text' : 'password'} value={form.password} required onChange={(e) => setForm({...form, password: e.target.value})} className="input-field pr-12" placeholder="Min 6 characters" />
            <button type="button" onClick={() => setShowPwd(!showPwd)} className="absolute right-3 top-8 text-slate-400 hover:text-accent transition-colors">{showPwd ? <EyeOff size={16} /> : <Eye size={16} />}</button>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Confirm Password</label>
            <input type="password" value={form.confirmPassword} required onChange={(e) => setForm({...form, confirmPassword: e.target.value})} className="input-field" placeholder="Re-enter password" />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">I am a</label>
            <select value={form.role} onChange={(e) => setForm({...form, role: e.target.value})}
              className="input-field text-white">
              <option value="student">Student</option>
              <option value="faculty">Faculty</option>
            </select>
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full py-3.5 flex items-center justify-center gap-2 disabled:opacity-50">
            {loading ? <span className="animate-spin">&#9696;</span> : <UserPlus size={18} />}
            {loading ? 'Creating...' : 'Create Account'}
          </button>
          <p className="text-center text-xs text-slate-500">Already have an account? <Link href="/login" className="text-accent hover:underline">Sign in</Link></p>
        </form>
      </div>
    </div>
  );
}
