import { MessageSquare, History, Settings, Plus } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto h-18 px-6 flex items-center justify-between">
        
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
            <span className="text-white font-bold">AI</span>
          </div>

          <h1 className="text-xl font-bold text-slate-900">
            AIChat
          </h1>
        </div>

        <div className="hidden md:flex items-center gap-8">
          <button className="flex items-center gap-2 text-slate-600 hover:text-blue-600 transition">
            <Plus size={18} />
            New Chat
          </button>

          <button className="flex items-center gap-2 text-slate-600 hover:text-blue-600 transition">
            <History size={18} />
            History
          </button>

          <button className="flex items-center gap-2 text-slate-600 hover:text-blue-600 transition">
            <MessageSquare size={18} />
            Chats
          </button>

          <button className="flex items-center gap-2 text-slate-600 hover:text-blue-600 transition">
            <Settings size={18} />
            Settings
          </button>
        </div>

        <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-semibold">
          Y
        </div>
      </div>
    </nav>
  );
}