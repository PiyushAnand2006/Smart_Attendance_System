'use client';

import { Construction } from 'lucide-react';
import { usePathname } from 'next/navigation';

export default function ComingSoon() {
  const pathname = usePathname() ?? '';
  const title = pathname
    .split('/')
    .filter(Boolean)
    .map((seg) => seg.charAt(0).toUpperCase() + seg.slice(1))
    .join(' / ');

  return (
    <div className="glass-card p-10 text-center animate-fade-in">
      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-accent/20 text-accent mb-4">
        <Construction size={28} />
      </div>
      <h2 className="text-2xl font-bold text-white mb-2">{title}</h2>
      <p className="text-slate-400">
        This section is under construction. Check back soon!
      </p>
    </div>
  );
}
