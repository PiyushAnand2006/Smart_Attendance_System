'use client';
import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';

export function useAuth(allowedRoles?: string[]) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  // Stable key so an array literal passed each render doesn't re-trigger the effect.
  const rolesKey = allowedRoles?.join(',') ?? '';

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
    if (userData) setUser(JSON.parse(userData));
    setLoading(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname, rolesKey, router]);

  return { user, loading, role: typeof window !== 'undefined' ? localStorage.getItem('role') : null };
}
