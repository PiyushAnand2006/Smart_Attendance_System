import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar role="admin" />
      <div className="flex-1 ml-64">
        <Header title="Admin Dashboard" />
        <main className="p-6">{children}</main>
      </div>
    </div>
  );
}
