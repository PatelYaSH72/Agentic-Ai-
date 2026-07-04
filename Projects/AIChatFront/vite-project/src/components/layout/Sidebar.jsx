import { NavLink } from "react-router-dom";

function Sidebar({ menuItems }) {
  return (
    <aside className="w-[260px] h-screen bg-[var(--bg-secondary)] border-r border-white/10 flex flex-col">

      {/* Logo */}
      <div className="h-20 flex items-center px-6 border-b border-white/10">
        <h1 className="text-2xl font-bold text-white">
          Enterprise RAG
        </h1>
      </div>

      {/* Menu */}
      <nav className="flex-1 px-4 py-6">

        {menuItems.map((item) => {

          const Icon = item.icon;

          return (
            <NavLink
              key={item.title}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl mb-2 transition-all duration-300
                ${
                  isActive
                    ? "bg-blue-500/20 text-blue-400"
                    : "text-gray-300 hover:bg-white/5 hover:text-white"
                }`
              }
            >
              <Icon size={20} />

              <span>{item.title}</span>

            </NavLink>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="p-5 border-t border-white/10">

        <p className="font-medium text-white">
          Demo User
        </p>

        <p className="text-sm text-gray-400">
          Admin
        </p>

      </div>

    </aside>
  );
}

export default Sidebar;