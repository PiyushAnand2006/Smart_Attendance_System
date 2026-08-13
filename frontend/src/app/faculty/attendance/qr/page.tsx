'use client';

import { useState, useEffect } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { QrCode, Square, CheckCircle } from 'lucide-react';

export default function QRAttendancePage() {
  const [qrToken, setQrToken] = useState('');
  const [stats, setStats] = useState({ total: 60, present: 0 });
  const [timeLeft, setTimeLeft] = useState(60);

  useEffect(() => {
    generateQR();
    const interval = setInterval(generateQR, 60000); // Regenerate every minute
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(t => t > 0 ? t - 1 : 60);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const generateQR = () => {
    const token = `TKN${Math.random().toString(36).substring(2, 12).toUpperCase()}`;
    setQrToken(token);
    setTimeLeft(60);
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="glass-card p-6">
        <h2 className="text-xl font-bold text-white">Database Management Systems - CSE-A</h2>
        <p className="text-sm text-slate-400">QR Code Mode • <span className="text-accent">High-Speed Scanning</span></p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <QrCode className="text-accent" size={20} /> Session QR Code
            </h3>
            <div className="text-sm">
              <span className="text-slate-400">Refreshes in:</span>
              <span className="text-accent font-bold">{timeLeft}s</span>
            </div>
          </div>

          <div className="bg-white p-8 rounded-xl flex items-center justify-center aspect-square">
            {qrToken && (
              <QRCodeSVG value={`https://smartattend.app/scan/${qrToken}`} size={256} level="H" />
            )}
          </div>

          <p className="text-center text-xs text-slate-400 mt-4">Students scan this QR with their app</p>

          <button className="w-full mt-4 px-4 py-3 bg-danger hover:bg-danger/80 text-white font-semibold rounded-lg flex items-center justify-center gap-2">
            <Square size={16} /> End Session
          </button>
        </div>

        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Session Status</h3>
          <div className="space-y-4">
            <div className="bg-slate-800/50 p-4 rounded-lg">
              <p className="text-sm text-slate-400">Total Scans</p>
              <p className="text-3xl font-bold text-white">{stats.present}</p>
            </div>
            <div className="bg-success/10 border border-success/30 p-4 rounded-lg">
              <p className="text-sm text-slate-400">Attendance Rate</p>
              <p className="text-3xl font-bold text-success">
                {Math.round(stats.present / stats.total * 100)}%
              </p>
            </div>
            <div className="bg-info/10 border border-info/30 p-4 rounded-lg">
              <p className="text-sm text-slate-400 flex items-center gap-2">
                <CheckCircle size={14} /> Notifications Sent
              </p>
              <p className="text-3xl font-bold text-info">{stats.present}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
