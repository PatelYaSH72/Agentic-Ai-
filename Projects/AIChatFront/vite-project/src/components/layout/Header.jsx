import { Menu, Search, Bell, ChevronDown } from "lucide-react";

function Header({ title }) {
  return (
    <header className="h-[72px] border-b border-white/10 bg-[var(--bg-primary)] flex items-center justify-between px-8">

      {/* Left Section */}
      <div className="flex items-center gap-4">

        <button className="p-2 rounded-lg hover:bg-white/5 transition">
          <Menu size={22} />
        </button>

        <h1 className="text-2xl font-semibold text-white">
          {title}
        </h1>

      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">

        {/* Search */}

        <div className="flex items-center gap-2 bg-[var(--surface)] px-4 py-2 rounded-xl">

          <Search size={18} />

          <input
            type="text"
            placeholder="Search..."
            className="bg-transparent outline-none text-sm w-48"
          />

        </div>

        {/* Notification */}

        <button className="p-2 rounded-lg hover:bg-white/5 transition">

          <Bell size={20} />

        </button>

        {/* User */}

        <button className="flex items-center gap-3 hover:bg-white/5 px-3 py-2 rounded-xl transition">

          <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center font-bold">
            Y
          </div>

          <div className="text-left">

            <p className="text-sm font-medium">
              Yash Patel
            </p>

            <p className="text-xs text-gray-400">
              Admin
            </p>

          </div>

          <ChevronDown size={18} />

        </button>

      </div>

    </header>
  );
}

export default Header;