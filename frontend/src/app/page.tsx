export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-dark via-primary to-primary-light relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-highlight/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>
      <div className="relative text-center px-6 animate-bounce-in">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-accent to-highlight mb-6 animate-pulse-glow">
          <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </div>
        <h1 className="text-6xl font-black mb-4 gradient-text">SmartAttend</h1>
        <p className="text-xl text-slate-300 mb-10 max-w-md mx-auto">Intelligent Multi-Modal Attendance System with QR Codes</p>
        <div className="flex gap-4 justify-center">
          <a href="/login" className="btn-primary text-lg px-8 py-3.5 shadow-glow">Get Started</a>
          <a href="/register" className="btn-secondary text-lg px-8 py-3.5">Create Account</a>
        </div>
      </div>
    </main>
  );
}
