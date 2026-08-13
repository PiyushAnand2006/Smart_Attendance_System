'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function FacultyAttendance() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/faculty/attendance/qr');
  }, [router]);

  return (
    <div className="glass-card p-10 text-center animate-fade-in">
      <p className="text-slate-400">Loading attendance session...</p>
    </div>
  );
}
