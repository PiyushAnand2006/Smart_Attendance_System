'use client';

import { useState } from 'react';
import { Calculator, TrendingUp } from 'lucide-react';

export default function CalculatorPage() {
  const [attended, setAttended] = useState(41);
  const [total, setTotal] = useState(50);
  const [target, setTarget] = useState(75);

  const safeTotal = total > 0 ? total : 1;
  const currentPct = (attended / safeTotal) * 100;
  const canMiss = target >= 100
    ? 0
    : Math.max(0, Math.floor((attended - (target / 100) * safeTotal) / (1 - target / 100)));
  const needToAttend = Math.max(0, Math.ceil((target / 100) * (safeTotal + 10) - attended));

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-white">Attendance Calculator</h1>
        <p className="text-slate-400">Plan your attendance effectively</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Calculator className="text-accent" size={20} /> Enter Details
          </h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-300 mb-2">Classes Attended</label>
              <input type="number" value={attended} onChange={(e) => setAttended(Number(e.target.value))}
                className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white" />
            </div>

            <div>
              <label className="block text-sm text-slate-300 mb-2">Total Classes</label>
              <input type="number" value={total} onChange={(e) => setTotal(Number(e.target.value))}
                className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white" />
            </div>

            <div>
              <label className="block text-sm text-slate-300 mb-2">Target Attendance (%)</label>
              <input type="number" value={target} onChange={(e) => setTarget(Number(e.target.value))}
                className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white" />
            </div>
          </div>
        </div>

        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <TrendingUp className="text-success" size={20} /> Results
          </h3>

          <div className="space-y-4">
            <div className="p-4 bg-slate-800/50 rounded-lg">
              <p className="text-sm text-slate-400">Current Attendance</p>
              <p className={"text-3xl font-bold " + (currentPct >= target ? 'text-success' : 'text-danger')}>
                {currentPct.toFixed(1)}%
              </p>
            </div>

            <div className="p-4 bg-info/10 border border-info/30 rounded-lg">
              <p className="text-sm text-slate-400">Classes You Can Miss</p>
              <p className="text-3xl font-bold text-info">{canMiss > 0 ? canMiss : 0}</p>
              <p className="text-xs text-slate-400 mt-1">while staying above {target}%</p>
            </div>

            <div className="p-4 bg-warning/10 border border-warning/30 rounded-lg">
              <p className="text-sm text-slate-400">Classes to Attend for Target</p>
              <p className="text-3xl font-bold text-warning">{needToAttend}</p>
              <p className="text-xs text-slate-400 mt-1">consecutive classes to reach {target}%</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
