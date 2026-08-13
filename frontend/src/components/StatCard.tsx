interface StatCardProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  trend?: string;
  color?: string;
  delay?: number;
}

export default function StatCard({ label, value, icon, trend, color = 'accent', delay = 0 }: StatCardProps) {
  const colors: Record<string, string> = {
    accent: 'from-accent/20 to-accent/5 border-accent/30 text-accent',
    success: 'from-success/20 to-success/5 border-success/30 text-success',
    warning: 'from-warning/20 to-warning/5 border-warning/30 text-warning',
    danger: 'from-danger/20 to-danger/5 border-danger/30 text-danger',
    info: 'from-info/20 to-info/5 border-info/30 text-info',
  };
  return (
    <div className={`relative p-6 rounded-xl bg-gradient-to-br ${colors[color]} border backdrop-blur-sm hover:scale-[1.02] transition-all duration-300 animate-slide-up`}
         style={{ animationDelay: `${delay}ms`, animationFillMode: 'both' }}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-300 mb-1">{label}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
          {trend && <p className="text-xs text-slate-400 mt-2">{trend}</p>}
        </div>
        {icon && <div className="opacity-80">{icon}</div>}
      </div>
    </div>
  );
}
