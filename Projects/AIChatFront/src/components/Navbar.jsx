import { MessageSquare, History, Settings, Plus } from "lucide-react";

export default function Navbar() {
  return (
    <nav
      style={{ backgroundColor: "#1A1A1A", borderBottom: "1px solid #2C2C2C" }}
      className="sticky top-0 z-40"
    >
      <div className="max-w-7xl mx-auto h-16 px-6 flex items-center justify-between">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <div
            style={{ backgroundColor: "#E85D00" }}
            className="w-10 h-10 rounded-xl flex items-center justify-center"
          >
            <span style={{ color: "#FFFFFF" }} className="font-bold text-sm">
              AI
            </span>
          </div>

          <h1 style={{ color: "#FFFFFF" }} className="text-xl font-bold">
            AIChat
          </h1>
        </div>

        {/* Nav Links */}
        <div className="hidden md:flex items-center gap-2">
          <NavButton icon={<Plus size={16} />} label="New Chat" primary />
          <NavButton icon={<History size={16} />} label="History" />
          <NavButton icon={<MessageSquare size={16} />} label="Chats" />
          <NavButton icon={<Settings size={16} />} label="Settings" />
        </div>

        {/* Avatar */}
        <div
          style={{
            backgroundColor: "#E85D00",
            color: "#FFFFFF",
          }}
          className="w-9 h-9 rounded-full flex items-center justify-center font-semibold text-sm"
        >
          Y
        </div>
      </div>
    </nav>
  );
}

function NavButton({ icon, label, primary = false }) {
  return (
    <button
      style={
        primary
          ? {
              backgroundColor: "#E85D00",
              color: "#FFFFFF",
              border: "none",
            }
          : {
              backgroundColor: "transparent",
              color: "#888580",
              border: "1px solid #2C2C2C",
            }
      }
      onMouseEnter={(e) => {
        if (primary) {
          e.currentTarget.style.backgroundColor = "#FF7A20";
        } else {
          e.currentTarget.style.color = "#E85D00";
          e.currentTarget.style.borderColor = "#E85D00";
        }
      }}
      onMouseLeave={(e) => {
        if (primary) {
          e.currentTarget.style.backgroundColor = "#E85D00";
        } else {
          e.currentTarget.style.color = "#888580";
          e.currentTarget.style.borderColor = "#2C2C2C";
        }
      }}
      className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-150"
    >
      {icon}
      {label}
    </button>
  );
}