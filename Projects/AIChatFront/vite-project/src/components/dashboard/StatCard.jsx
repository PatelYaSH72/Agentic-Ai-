import React from "react";

function StatCard({ title, value, icon }) {
  return (
    <div className="bg-[var(--surface)] rounded-2xl p-6 border border-white/10 hover:border-[var(--primary)] transition-all duration-300">

      <div className="flex items-center justify-between">

        <div>

          <p className="text-sm text-gray-400">
            {title}
          </p>

          <h2 className="text-3xl font-bold mt-3">
            {value}
          </h2>

        </div>

        <div className="w-14 h-14 rounded-xl bg-blue-500/15 flex items-center justify-center">

          {icon}

        </div>

      </div>

    </div>
  );
}

export default StatCard;