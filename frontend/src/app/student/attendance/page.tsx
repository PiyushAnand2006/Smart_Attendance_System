'use client';
import { useState } from 'react';
import { QrCode, Scan, CheckCircle } from 'lucide-react';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';

export default function StudentScanPage() {
  const { loading: al } = useAuth(['student']);
  const [qrInput, setQrInput] = useState('');
  const [result, setResult] = useState<any>(null);
  const [scanning, setScanning] = useState(false);

  const handleScan = async () => {
    if (!qrInput.trim()) return;
    setScanning(true);
    try {
      const r = await api.post('/qr/scan-my', { token: qrInput });
      setResult(r.data);
    } catch (e: any) {
      setResult({ error: e.message });
    }
    setScanning(false);
  };

  if (al) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-card p-5"><h2 className="text-xl font-bold text-white">QR Code Scanner</h2><p className="text-sm text-slate-400">Enter the QR token shown by your faculty to mark attendance</p></div>
      <div className="glass-card p-8 max-w-lg mx-auto">
        <div className="flex gap-3 mb-4">
          <input type="text" value={qrInput} onChange={e => setQrInput(e.target.value)} placeholder="Paste QR code here..." className="input-field flex-1" />
          <button onClick={handleScan} disabled={scanning || !qrInput.trim()} className="btn-primary flex items-center gap-2 px-6">{scanning ? <span className="animate-spin">&#9696;</span> : <Scan size={16} />} Scan</button>
        </div>
        {result && (
          <div className={result.error ? "p-4 rounded-xl bg-danger/20 border border-danger/30 animate-scale-in" : "p-4 rounded-xl bg-success/20 border border-success/30 animate-scale-in"}>
            {result.error ? (
              <p className="text-danger font-medium">{result.error}</p>
            ) : (
              <div className="flex items-center gap-3"><CheckCircle size={24} className="text-success" /><div><p className="font-semibold text-white">Attendance Marked!</p><p className="text-sm text-slate-300">Subject: {result.subject_name}</p></div></div>
            )}
          </div>
        )}
      </div>
      <div className="glass-card p-6 max-w-lg mx-auto">
        <h3 className="text-sm font-semibold text-slate-300 mb-3">How to mark attendance:</h3>
        <ol className="space-y-2 text-sm text-slate-400 list-decimal list-inside">
          <li>Your faculty starts an attendance session and shows a QR code</li>
          <li>They share the QR token (or you scan it with your camera)</li>
          <li>Paste or enter the token above and click Scan</li>
          <li>You&apos;re marked present automatically!</li>
        </ol>
      </div>
    </div>
  );
}