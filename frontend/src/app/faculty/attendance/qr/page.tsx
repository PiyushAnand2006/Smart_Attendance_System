'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { QrCode, Square, CheckCircle, ArrowLeft, Copy } from 'lucide-react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';

export default function QRAttendancePage() {
  const { loading: al } = useAuth(['faculty', 'admin']);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [session, setSession] = useState<any>(null);
  const [qrToken, setQrToken] = useState('');
  const [genError, setGenError] = useState('');
  const [ended, setEnded] = useState(false);
  const [timeLeft, setTimeLeft] = useState(120);
  const sessionRef = useRef<number | null>(null);

  useEffect(() => {
    if (al) return;
    const params = new URLSearchParams(window.location.search);
    const sid = params.get('session');
    if (!sid) {
      setGenError('No session selected. Start a class from the Schedule page.');
      return;
    }
    const id = parseInt(sid);
    setSessionId(id);
    sessionRef.current = id;
    initSession(id);
  }, [al]);

  const initSession = async (id: number) => {
    try {
      const r = await api.get(`/attendance/sessions/${id}`);
      setSession(r.data);
      if (r.data.status === 'completed') {
        setEnded(true);
        return;
      }
      if (r.data.status === 'scheduled') {
        await api.post(`/attendance/sessions/${id}/start`);
        const r2 = await api.get(`/attendance/sessions/${id}`);
        setSession(r2.data);
      }
      generateQR(id);
    } catch (e: any) {
      setGenError(e.message || 'Failed to load session');
    }
  };

  const generateQR = async (id: number) => {
    setGenError('');
    try {
      const qrRes = await api.post('/qr/generate', { session_id: id });
      const token = qrRes.data?.token || '';
      if (token) setQrToken(token);
      else setGenError('Failed to generate QR token');
    } catch (e: any) {
      setGenError(e.message || 'Failed to generate QR token');
    }
    setTimeLeft(120);
  };

  useEffect(() => {
    if (al || !sessionId || ended) return;
    const interval = setInterval(() => generateQR(sessionId), 120000);
    return () => clearInterval(interval);
  }, [al, sessionId, ended]);

  useEffect(() => {
    if (ended) return;
    const timer = setInterval(() => setTimeLeft(t => t > 0 ? t - 1 : 120), 1000);
    return () => clearInterval(timer);
  }, [ended]);

  useEffect(() => {
    if (al || !sessionId || ended) return;
    const poll = setInterval(async () => {
      try {
        const r = await api.get(`/attendance/sessions/${sessionId}`);
        setSession(r.data);
        if (r.data.status === 'completed') setEnded(true);
      } catch {}
    }, 5000);
    return () => clearInterval(poll);
  }, [al, sessionId, ended]);

  const endSession = async () => {
    if (!sessionId) return;
    try {
      await api.post(`/attendance/sessions/${sessionId}/end`);
      setQrToken('');
      setEnded(true);
      const r = await api.get(`/attendance/sessions/${sessionId}`);
      setSession(r.data);
    } catch (e: any) {
      setGenError(e.message || 'Failed to end session');
    }
  };

  if (al) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;

  const total = session?.total_students || 0;
  const present = session?.present || 0;
  const rate = total > 0 ? Math.round(present / total * 100) : 0;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-card p-6 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">{session?.subject_name || 'Attendance Session'}</h2>
          <p className="text-sm text-slate-400">{session?.class_name}{session?.class_code ? ` - ${session.class_code}` : ''} • QR Code Mode</p>
        </div>
        {ended && <span className="badge-success">completed</span>}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <QrCode className="text-accent" size={20} /> Session QR Code
            </h3>
            {!ended && (
              <div className="text-sm">
                <span className="text-slate-400">Refreshes in:</span>
                <span className="text-accent font-bold">{timeLeft}s</span>
              </div>
            )}
          </div>

          <div className="bg-white p-8 rounded-xl flex items-center justify-center aspect-square">
            {!ended && qrToken ? (
              <QRCodeSVG value={qrToken} size={256} level="H" />
            ) : (
              <p className="text-slate-500 text-sm text-center px-6">
                {ended ? 'Session ended' : (genError || 'Generating QR...')}
              </p>
            )}
          </div>

          {!ended && qrToken && (
            <div className="mt-4 p-3 rounded-lg bg-slate-800/50 border border-white/10">
              <p className="text-xs text-slate-400 mb-1">QR Token (for manual entry):</p>
              <div className="flex items-center gap-2">
                <code className="flex-1 text-sm text-accent font-mono break-all">{qrToken}</code>
                <button onClick={() => navigator.clipboard.writeText(qrToken)}
                  className="text-xs text-slate-400 hover:text-white px-2 py-1 rounded border border-white/10 hover:border-accent/50 transition-colors flex items-center gap-1">
                  <Copy size={12} /> Copy
                </button>
              </div>
            </div>
          )}

          {genError && !qrToken && (
            <div className="mt-4 p-3 rounded-lg bg-danger/20 border border-danger/50 text-danger text-sm">{genError}</div>
          )}

          {!ended ? (
            <button onClick={endSession}
              className="w-full mt-4 px-4 py-3 bg-danger hover:bg-danger/80 text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition-colors">
              <Square size={16} /> End Session
            </button>
          ) : (
            <button onClick={() => window.location.href = '/faculty/schedule'}
              className="w-full mt-4 px-4 py-3 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition-colors">
              <ArrowLeft size={16} /> Back to Schedule
            </button>
          )}
        </div>

        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Session Status</h3>
          <div className="space-y-4">
            <div className="bg-slate-800/50 p-4 rounded-lg">
              <p className="text-sm text-slate-400">Total Scans</p>
              <p className="text-3xl font-bold text-white">{present}</p>
              <p className="text-xs text-slate-500 mt-1">of {total} students</p>
            </div>
            <div className="bg-success/10 border border-success/30 p-4 rounded-lg">
              <p className="text-sm text-slate-400">Attendance Rate</p>
              <p className="text-3xl font-bold text-success">{rate}%</p>
            </div>
            <div className="bg-info/10 border border-info/30 p-4 rounded-lg">
              <p className="text-sm text-slate-400 flex items-center gap-2">
                <CheckCircle size={14} /> Session Status
              </p>
              <p className="text-3xl font-bold text-info capitalize">{session?.status || '-'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
