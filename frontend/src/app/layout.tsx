import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'SmartAttend - Intelligent Attendance System',
  description: 'Multi-modal attendance tracking with QR codes',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-primary-dark text-slate-50 antialiased">{children}</body>
    </html>
  );
}
