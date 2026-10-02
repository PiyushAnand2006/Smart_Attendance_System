'use client';
import { useState, useEffect, useRef, useCallback } from 'react';
import { QrCode, Scan, CheckCircle, Camera, CameraOff, Square } from 'lucide-react';
import { Html5Qrcode } from 'html5-qrcode';
import { api } from '@/services/api';
import { useAuth } from '@/hooks/useAuth';

export default function StudentScanPage() {
  const { loading: al } = useAuth(['student']);
  const [qrInput, setQrInput] = useState('');
  const [result, setResult] = useState<any>(null);
  const [scanning, setScanning] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState('');
  const scannerRef = useRef<Html5Qrcode | null>(null);
  const scannerIdRef = useRef('qr-reader');

  const stopCamera = useCallback(async () => {
    if (scannerRef.current) {
      try {
        const state = await scannerRef.current.getState();
        if (state === 2) {
          await scannerRef.current.stop();
        }
      } catch {}
      scannerRef.current = null;
    }
    setCameraActive(false);
  }, []);

  const startCamera = async () => {
    setCameraError('');
    setResult(null);
    try {
      if (!scannerRef.current) {
        scannerRef.current = new Html5Qrcode(scannerIdRef.current);
      }
      await scannerRef.current.start(
        { facingMode: 'environment' },
        { fps: 10, qrbox: { width: 250, height: 250 }, aspectRatio: 1.0 },
        async (decodedText) => {
          const token = decodedText.split('/').pop() || decodedText;
          await stopCamera();
          await submitToken(token);
        },
        () => {}
      );
      setCameraActive(true);
    } catch (err: any) {
      setCameraError(err?.message || 'Could not access camera. Check permissions.');
      setCameraActive(false);
    }
  };

  const submitToken = async (rawToken: string) => {
    const token = rawToken.includes('scan/') ? (rawToken.split('/').pop() || rawToken) : rawToken;
    setScanning(true);
    try {
      const r = await api.post('/qr/scan-my', { token });
      setResult(r.data);
    } catch (e: any) {
      setResult({ error: e.message });
    }
    setScanning(false);
  };

  const handleManualScan = async () => {
    if (!qrInput.trim()) return;
    await submitToken(qrInput.trim());
  };

  useEffect(() => {
    return () => { stopCamera(); };
  }, [stopCamera]);

  if (al) return <div className="flex items-center justify-center h-64"><div className="animate-spin text-4xl text-accent">&#9696;</div></div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-card p-5">
        <h2 className="text-xl font-bold text-white">QR Code Scanner</h2>
        <p className="text-sm text-slate-400">Scan the QR code shown by your faculty to mark attendance</p>
      </div>

      <div className="glass-card p-8 max-w-lg mx-auto">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
            <Camera size={16} className="text-accent" /> Camera Scanner
          </h3>
          {!cameraActive ? (
            <button onClick={startCamera} className="btn-primary flex items-center gap-2 px-4 py-2 text-sm">
              <Camera size={16} /> Open Camera
            </button>
          ) : (
            <button onClick={stopCamera} className="btn-secondary flex items-center gap-2 px-4 py-2 text-sm">
              <Square size={16} /> Stop Camera
            </button>
          )}
        </div>

        <div className="relative rounded-xl overflow-hidden bg-black/50 border border-white/10" style={{ minHeight: '300px' }}>
          <div id={scannerIdRef.current} className="w-full" />
          {!cameraActive && (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500">
              <CameraOff size={48} className="mb-3 opacity-50" />
              <p className="text-sm">Camera is off</p>
              <p className="text-xs mt-1">Click &quot;Open Camera&quot; to scan QR codes</p>
            </div>
          )}
        </div>

        {cameraError && (
          <div className="mt-3 p-3 rounded-lg bg-danger/20 border border-danger/50 text-danger text-sm">{cameraError}</div>
        )}

        <div className="flex items-center gap-3 my-5">
          <div className="flex-1 h-px bg-white/10" />
          <span className="text-xs text-slate-500">OR ENTER MANUALLY</span>
          <div className="flex-1 h-px bg-white/10" />
        </div>

        <div className="flex gap-3">
          <input type="text" value={qrInput} onChange={e => setQrInput(e.target.value)}
            placeholder="Paste QR code here..." className="input-field flex-1"
            onKeyDown={e => e.key === 'Enter' && handleManualScan()} />
          <button onClick={handleManualScan} disabled={scanning || !qrInput.trim()}
            className="btn-primary flex items-center gap-2 px-6">
            {scanning ? <span className="animate-spin">&#9696;</span> : <Scan size={16} />} Scan
          </button>
        </div>

        {result && (
          <div className={`mt-4 p-4 rounded-xl animate-scale-in ${result.error ? 'bg-danger/20 border border-danger/30' : 'bg-success/20 border border-success/30'}`}>
            {result.error ? (
              <p className="text-danger font-medium">{result.error}</p>
            ) : (
              <div className="flex items-center gap-3">
                <CheckCircle size={24} className="text-success" />
                <div>
                  <p className="font-semibold text-white">Attendance Marked!</p>
                  <p className="text-sm text-slate-300">Subject: {result.subject_name}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="glass-card p-6 max-w-lg mx-auto">
        <h3 className="text-sm font-semibold text-slate-300 mb-3">How to mark attendance:</h3>
        <ol className="space-y-2 text-sm text-slate-400 list-decimal list-inside">
          <li>Your faculty starts an attendance session and shows a QR code</li>
          <li>Click &quot;Open Camera&quot; and scan the QR code</li>
          <li>Or paste the token manually and click Scan</li>
          <li>You&apos;re marked present automatically!</li>
        </ol>
      </div>
    </div>
  );
}
