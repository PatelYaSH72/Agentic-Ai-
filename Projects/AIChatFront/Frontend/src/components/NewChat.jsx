import { useState, useRef, useEffect } from "react";
import {
  Plus,
  MessageSquare,
  Trash2,
  Send,
  Settings,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

// ── Y Brix Color Tokens ──────────────────────────────────────────
const C = {
  bgMain:     "#FAF7F2",
  bgSection:  "#F2EDE4",
  bgDark:     "#E8E2D9",
  black:      "#1A1A1A",
  softBlack:  "#2C2C2C",
  cardBlack:  "#222222",
  orange:     "#E85D00",
  orangeHov:  "#FF7A20",
  orangeTint: "rgba(232,93,0,0.1)",
  white:      "#FFFFFF",
  bodyText:   "#555450",
  mutedText:  "#888580",
};

// ── Fake history data ────────────────────────────────────────────
const INITIAL_HISTORY = [
  {
    id: 1,
    title: "React hooks kya hote hain?",
    date: "Aaj",
    messages: [
      { role: "user", content: "React hooks kya hote hain?" },
      { role: "ai",   content: "React Hooks functions hain jo aapko class components ke bina state aur lifecycle features use karne dete hain. Sabse common hain useState, useEffect, aur useContext." },
    ],
  },
  {
    id: 2,
    title: "Python list vs tuple",
    date: "Aaj",
    messages: [
      { role: "user", content: "Python list aur tuple mein kya fark hai?" },
      { role: "ai",   content: "List mutable hoti hai — aap usse change kar sakte ho. Tuple immutable hoti hai — ek baar banane ke baad change nahi hoti. Tuple thodi fast bhi hoti hai." },
    ],
  },
  {
    id: 3,
    title: "JWT authentication flow",
    date: "Kal",
    messages: [
      { role: "user", content: "JWT kaise kaam karta hai?" },
      { role: "ai",   content: "JWT (JSON Web Token) teen parts ka hota hai: Header, Payload, aur Signature. Login pe server token banata hai, client usse store karta hai aur har request mein bhejta hai." },
    ],
  },
  {
    id: 4,
    title: "FastAPI setup guide",
    date: "Kal",
    messages: [
      { role: "user", content: "FastAPI kaise setup karein?" },
      { role: "ai",   content: "pip install fastapi uvicorn karein, phir main.py banao aur uvicorn main:app --reload se run karein. Docs automatically /docs pe milti hain." },
    ],
  },
  {
    id: 5,
    title: "CSS flexbox tutorial",
    date: "Is Hafte",
    messages: [
      { role: "user", content: "Flexbox samjhao" },
      { role: "ai",   content: "Flexbox ek layout model hai. display:flex lagao parent pe, phir justify-content se horizontal aur align-items se vertical alignment control karo." },
    ],
  },
];

// ── Helpers ──────────────────────────────────────────────────────
let nextId = 100;
function groupByDate(history) {
  const groups = {};
  history.forEach((chat) => {
    if (!groups[chat.date]) groups[chat.date] = [];
    groups[chat.date].push(chat);
  });
  return groups;
}

// ── Main Component ───────────────────────────────────────────────
export default function ChatPage() {
  const [history, setHistory]           = useState(INITIAL_HISTORY);
  const [activeChatId, setActiveChatId] = useState(null);
  const [messages, setMessages]         = useState([]);
  const [input, setInput]               = useState("");
  const [isTyping, setIsTyping]         = useState(false);
  const [sidebarOpen, setSidebarOpen]   = useState(true);
  const [hoveredChat, setHoveredChat]   = useState(null);
  const bottomRef                       = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // Load a chat from history
  function openChat(chat) {
    setActiveChatId(chat.id);
    setMessages(chat.messages);
  }

  // New chat
  function newChat() {
    setActiveChatId(null);
    setMessages([]);
    setInput("");
  }

 // ── API Config ─────────────────────────
const API_URL = "http://127.0.0.1:8000";

// handleSend function — ye replace karo pura
async function handleSend() {
  const text = input.trim();
  if (!text || isTyping) return;

  // 1. User message turant dikhao
  const userMsg = { role: "user", content: text };
  const newMsgs = [...messages, userMsg];
  setMessages(newMsgs);
  setInput("");
  setIsTyping(true);

  try {
    // 2. Backend API call
    const response = await fetch(`${API_URL}/llm/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,          // string
        history: messages.map((msg) => ({
          role: msg.role,       // "user" ya "ai"
          content: msg.content,
        })),
      }),
    });

    if (!response.ok) throw new Error("Server error: " + response.status);

    const data = await response.json();

    // 3. AI reply add karo
    const aiMsg = { role: "ai", content: data.reply };
    const finalMsgs = [...newMsgs, aiMsg];
    setMessages(finalMsgs);

    // 4. Sidebar history update
    if (activeChatId) {
      setHistory((prev) =>
        prev.map((c) =>
          c.id === activeChatId ? { ...c, messages: finalMsgs } : c
        )
      );
    } else {
      const newChatObj = {
        id: ++nextId,
        title: text.length > 40 ? text.slice(0, 40) + "…" : text,
        date: "Aaj",
        messages: finalMsgs,
      };
      setHistory((prev) => [newChatObj, ...prev]);
      setActiveChatId(newChatObj.id);
    }

  } catch (err) {
    // 5. Error — ek alert dikhao
    console.error("API Error:", err);
    alert("Error: " + err.message);
  } finally {
    setIsTyping(false);
  }
}
  function deleteChat(e, id) {
    e.stopPropagation();
    setHistory((prev) => prev.filter((c) => c.id !== id));
    if (activeChatId === id) newChat();
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  const grouped = groupByDate(history);
  const isEmpty = messages.length === 0;

  return (
    <div style={{ display: "flex", height: "100vh", backgroundColor: C.black, fontFamily: "system-ui, sans-serif" }}>

      {/* ── SIDEBAR ── */}
      <aside
        style={{
          width: sidebarOpen ? 260 : 0,
          minWidth: sidebarOpen ? 260 : 0,
          backgroundColor: C.cardBlack,
          borderRight: `1px solid ${C.softBlack}`,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          transition: "width 0.2s ease, min-width 0.2s ease",
        }}
      >
        {/* Sidebar Header */}
        <div style={{ padding: "16px 12px 12px", borderBottom: `1px solid ${C.softBlack}`, flexShrink: 0 }}>
          {/* Logo row */}
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
            <div style={{ width: 32, height: 32, borderRadius: 8, backgroundColor: C.orange, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <span style={{ color: C.white, fontWeight: 700, fontSize: 12 }}>AI</span>
            </div>
            <span style={{ color: C.white, fontWeight: 600, fontSize: 15 }}>AIChat</span>
          </div>

          {/* New Chat button */}
          <button
            onClick={newChat}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = C.orangeHov)}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = C.orange)}
            style={{
              width: "100%",
              padding: "9px 12px",
              backgroundColor: C.orange,
              color: C.white,
              border: "none",
              borderRadius: 8,
              fontSize: 13,
              fontWeight: 500,
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: 8,
              transition: "background 0.15s",
            }}
          >
            <Plus size={15} />
            New Chat
          </button>
        </div>

        {/* History List */}
        <div style={{ flex: 1, overflowY: "auto", padding: "8px 8px" }}>
          {Object.entries(grouped).map(([date, chats]) => (
            <div key={date} style={{ marginBottom: 16 }}>
              {/* Date label */}
              <p style={{ fontSize: 11, color: C.mutedText, fontWeight: 500, padding: "4px 8px 6px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                {date}
              </p>

              {chats.map((chat) => {
                const isActive  = chat.id === activeChatId;
                const isHovered = hoveredChat === chat.id;
                return (
                  <div
                    key={chat.id}
                    onClick={() => openChat(chat)}
                    onMouseEnter={() => setHoveredChat(chat.id)}
                    onMouseLeave={() => setHoveredChat(null)}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 8,
                      padding: "8px 10px",
                      borderRadius: 8,
                      cursor: "pointer",
                      marginBottom: 2,
                      backgroundColor: isActive
                        ? C.softBlack
                        : isHovered
                        ? "#252525"
                        : "transparent",
                      borderLeft: isActive ? `2px solid ${C.orange}` : "2px solid transparent",
                      transition: "background 0.1s",
                    }}
                  >
                    <MessageSquare size={13} color={isActive ? C.orange : C.mutedText} style={{ flexShrink: 0 }} />
                    <span
                      style={{
                        fontSize: 13,
                        color: isActive ? C.white : C.mutedText,
                        flex: 1,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {chat.title}
                    </span>
                    {(isActive || isHovered) && (
                      <button
                        onClick={(e) => deleteChat(e, chat.id)}
                        onMouseEnter={(e) => (e.currentTarget.style.color = "#ff4444")}
                        onMouseLeave={(e) => (e.currentTarget.style.color = C.mutedText)}
                        style={{ background: "none", border: "none", cursor: "pointer", color: C.mutedText, padding: 2, display: "flex" }}
                      >
                        <Trash2 size={13} />
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          ))}
        </div>

        {/* Sidebar Footer */}
        <div style={{ padding: "12px", borderTop: `1px solid ${C.softBlack}`, flexShrink: 0 }}>
          <button
            onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = C.softBlack; e.currentTarget.style.color = C.white; }}
            onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = "transparent"; e.currentTarget.style.color = C.mutedText; }}
            style={{
              width: "100%",
              padding: "8px 10px",
              backgroundColor: "transparent",
              color: C.mutedText,
              border: "none",
              borderRadius: 8,
              fontSize: 13,
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: 8,
              transition: "all 0.15s",
            }}
          >
            <Settings size={15} />
            Settings
          </button>
        </div>
      </aside>

      {/* ── MAIN AREA ── */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", backgroundColor: C.black }}>

        {/* Top bar */}
        <div style={{ height: 52, borderBottom: `1px solid ${C.softBlack}`, display: "flex", alignItems: "center", padding: "0 16px", gap: 12, flexShrink: 0 }}>
          {/* Toggle sidebar */}
          <button
            onClick={() => setSidebarOpen((v) => !v)}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = C.softBlack)}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
            style={{ background: "transparent", border: "none", cursor: "pointer", color: C.mutedText, borderRadius: 6, padding: 6, display: "flex", transition: "background 0.15s" }}
          >
            {sidebarOpen ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
          </button>

          <span style={{ color: C.mutedText, fontSize: 13 }}>
            {activeChatId
              ? history.find((c) => c.id === activeChatId)?.title
              : "New Chat"}
          </span>
        </div>

        {/* Messages area */}
        <div style={{ flex: 1, overflowY: "auto", padding: "24px 0" }}>
          <div style={{ maxWidth: 720, margin: "0 auto", padding: "0 20px", display: "flex", flexDirection: "column", gap: 20 }}>

            {/* Empty state */}
            {isEmpty && (
              <div style={{ textAlign: "center", marginTop: 80 }}>
                <div style={{ width: 56, height: 56, borderRadius: 16, backgroundColor: C.orange, display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 20px" }}>
                  <span style={{ color: C.white, fontWeight: 700, fontSize: 20 }}>AI</span>
                </div>
                <h2 style={{ color: C.white, fontSize: 22, fontWeight: 600, marginBottom: 8 }}>
                  Kya poochna chahte ho?
                </h2>
                <p style={{ color: C.mutedText, fontSize: 14 }}>
                  Neeche type karo aur conversation shuru karo
                </p>

                {/* Suggestion chips */}
                <div style={{ display: "flex", gap: 10, justifyContent: "center", flexWrap: "wrap", marginTop: 28 }}>
                  {["React hooks samjhao", "FastAPI kya hai?", "Python tips do", "CSS flexbox tricks"].map((s) => (
                    <button
                      key={s}
                      onClick={() => setInput(s)}
                      onMouseEnter={(e) => { e.currentTarget.style.borderColor = C.orange; e.currentTarget.style.color = C.orange; }}
                      onMouseLeave={(e) => { e.currentTarget.style.borderColor = C.softBlack; e.currentTarget.style.color = C.mutedText; }}
                      style={{
                        padding: "8px 14px",
                        backgroundColor: C.cardBlack,
                        border: `1px solid ${C.softBlack}`,
                        borderRadius: 20,
                        color: C.mutedText,
                        fontSize: 13,
                        cursor: "pointer",
                        transition: "all 0.15s",
                      }}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Messages */}
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  display: "flex",
                  flexDirection: msg.role === "user" ? "row-reverse" : "row",
                  alignItems: "flex-end",
                  gap: 10,
                }}
              >
                {/* Avatar */}
                <div
                  style={{
                    width: 30,
                    height: 30,
                    borderRadius: "50%",
                    backgroundColor: msg.role === "ai" ? C.orange : C.softBlack,
                    border: msg.role === "user" ? `1px solid ${C.softBlack}` : "none",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                    fontSize: 11,
                    fontWeight: 600,
                    color: C.white,
                  }}
                >
                  {msg.role === "ai" ? "AI" : "Y"}
                </div>

                {/* Bubble */}
                <div
                  style={{
                    maxWidth: "72%",
                    padding: "11px 15px",
                    borderRadius: msg.role === "ai" ? "18px 18px 18px 4px" : "18px 18px 4px 18px",
                    backgroundColor: msg.role === "ai" ? C.cardBlack : C.orange,
                    color: C.white,
                    fontSize: 14,
                    lineHeight: 1.65,
                    border: msg.role === "ai" ? `1px solid ${C.softBlack}` : "none",
                  }}
                >
                  {msg.content}
                </div>
              </div>
            ))}

            {/* Typing indicator */}
            {isTyping && (
              <div style={{ display: "flex", alignItems: "flex-end", gap: 10 }}>
                <div style={{ width: 30, height: 30, borderRadius: "50%", backgroundColor: C.orange, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 600, color: C.white }}>
                  AI
                </div>
                <div style={{ padding: "12px 16px", borderRadius: "18px 18px 18px 4px", backgroundColor: C.cardBlack, border: `1px solid ${C.softBlack}`, display: "flex", gap: 5, alignItems: "center" }}>
                  {[0, 1, 2].map((i) => (
                    <div
                      key={i}
                      style={{
                        width: 7,
                        height: 7,
                        borderRadius: "50%",
                        backgroundColor: C.orange,
                        animation: "blink 1.2s infinite",
                        animationDelay: `${i * 0.2}s`,
                      }}
                    />
                  ))}
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>
        </div>

        {/* ── INPUT BAR ── */}
        <div style={{ padding: "14px 20px 18px", flexShrink: 0, borderTop: `1px solid ${C.softBlack}` }}>
          <div style={{ maxWidth: 720, margin: "0 auto", display: "flex", gap: 10, alignItems: "flex-end" }}>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Message karo... (Enter = send, Shift+Enter = new line)"
              rows={1}
              style={{
                flex: 1,
                padding: "12px 16px",
                backgroundColor: C.cardBlack,
                border: `1px solid ${C.softBlack}`,
                borderRadius: 12,
                color: C.white,
                fontSize: 14,
                fontFamily: "inherit",
                resize: "none",
                outline: "none",
                lineHeight: 1.5,
                maxHeight: 120,
                overflowY: "auto",
              }}
              onFocus={(e) => (e.target.style.borderColor = C.orange)}
              onBlur={(e) => (e.target.style.borderColor = C.softBlack)}
              onInput={(e) => {
                e.target.style.height = "auto";
                e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
              }}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              onMouseEnter={(e) => { if (input.trim()) e.currentTarget.style.backgroundColor = C.orangeHov; }}
              onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = input.trim() ? C.orange : C.softBlack; }}
              style={{
                width: 44,
                height: 44,
                borderRadius: 12,
                backgroundColor: input.trim() ? C.orange : C.softBlack,
                border: "none",
                cursor: input.trim() ? "pointer" : "not-allowed",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
                transition: "background 0.15s",
              }}
            >
              <Send size={18} color={C.white} />
            </button>
          </div>
          <p style={{ textAlign: "center", fontSize: 11, color: C.mutedText, marginTop: 8 }}>
            Enter se send • Shift+Enter se new line
          </p>
        </div>
      </div>

      <style>{`
        @keyframes blink {
          0%, 80%, 100% { opacity: 0.3; }
          40% { opacity: 1; }
        }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #2C2C2C; border-radius: 4px; }
      `}</style>
    </div>
  );
}