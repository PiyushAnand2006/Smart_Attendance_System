'use client';
import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';

export function useAuth(allowedRoles?: string[]) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    if (!token || !role) {
      router.push('/login');
      return;
    }
    if (allowedRoles && !allowedRoles.includes(role)) {
      router.push(`/${role}/dashboard`);
      return;
    }
    const userData = localStorage.getItem('user');
    setUser(userData ? JSON.parse(userData) : null);
    setLoading(false);
  }, [pathname, allowedRoles, router]);

  return { user, loading, role: typeof window !== 'undefined' ? localStorage.getItem('role') : null };
}
