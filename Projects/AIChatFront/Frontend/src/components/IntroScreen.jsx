import { useEffect } from "react";

export default function IntroScreen({ onFinish }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 2500);

    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div className="fixed inset-0 bg-white flex flex-col items-center justify-center z-50">
      <div className="animate-logo">
        <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg">
          <span className="text-white text-3xl font-bold">AI</span>
        </div>
      </div>

      <h1 className="mt-6 text-4xl font-bold text-slate-900">
        AIChat
      </h1>

      <p className="mt-2 text-slate-500">
        Powered by Intelligent Conversations
      </p>
    </div>
  );
}