function SystemHealth() {
  return (
    <div className="bg-[var(--surface)] rounded-2xl border border-white/10 p-6 h-[300px]">

      <h2 className="text-xl font-semibold mb-4">
        System Health
      </h2>

      <p className="text-gray-400">
        API, Database and Vector Store Status
      </p>

    </div>
  );
}

export default SystemHealth;