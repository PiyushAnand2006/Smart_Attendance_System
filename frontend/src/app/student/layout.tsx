import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';

export default function StudentLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar role="student" />
      <div className="flex-1 ml-64">
        <Header title="Student Dashboard" />
        <main className="p-6">{children}</main>
      </div>
    </div>
  );
}
