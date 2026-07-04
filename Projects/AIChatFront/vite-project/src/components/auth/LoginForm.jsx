import { motion } from "framer-motion";
import { ShieldCheck } from "lucide-react";

function LoginCard() {
  return (
    <motion.div
      initial={{
        opacity: 0,
        scale: 0.95,
        y: 30,
      }}
      animate={{
        opacity: 1,
        scale: 1,
        y: 0,
      }}
      transition={{
        duration: 0.6,
        ease: "easeOut",
      }}
      whileHover={{
        y: -4,
        transition: {
          duration: 0.25,
        },
      }}
      className="
      relative
      z-20
      w-[480px]
      overflow-hidden
      rounded-[30px]
      border
      border-white/10
      bg-white/[0.04]
      backdrop-blur-3xl
      px-10
      py-12
      shadow-[0_20px_80px_rgba(0,0,0,.45)]
      "
    >
      {/* Top Glow */}

      <div
        className="
        absolute
        top-0
        left-0
        h-[2px]
        w-full
        bg-gradient-to-r
        from-transparent
        via-blue-400
        to-transparent
        opacity-60
        "
      />

      {/* Logo */}

      <div className="flex justify-center">

        <motion.div
          animate={{
            boxShadow: [
              "0 0 25px rgba(79,140,255,.35)",
              "0 0 55px rgba(139,92,246,.45)",
              "0 0 25px rgba(79,140,255,.35)",
            ],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
          }}
          className="
          flex
          h-24
          w-24
          items-center
          justify-center
          rounded-[28px]
          bg-gradient-to-br
          from-blue-500
          via-indigo-500
          to-purple-600
          "
        >
          <ShieldCheck
            size={44}
            className="text-white"
            strokeWidth={2.2}
          />
        </motion.div>

      </div>

      {/* Brand */}

      <div className="mt-8 text-center">

        <h1
          className="
          text-4xl
          font-bold
          tracking-tight
          text-white
          "
        >
          Enterprise RAG Studio
        </h1>

        <p
          className="
          mt-3
          text-base
          text-blue-300
          "
        >
          Enterprise AI Knowledge Platform
        </p>

      </div>

      {/* Divider */}

      <div className="my-8 flex items-center">

        <div className="h-px flex-1 bg-white/10" />

        <span
          className="
          px-4
          text-xs
          uppercase
          tracking-[0.3em]
          text-gray-500
          "
        >
          Secure Login
        </span>

        <div className="h-px flex-1 bg-white/10" />

      </div>

      {/* Welcome */}

      <div className="text-center">

        <h2
          className="
          text-3xl
          font-semibold
          text-white
          "
        >
          Welcome Back
        </h2>

        <p
          className="
          mt-4
          leading-8
          text-gray-400
          "
        >
          Sign in to securely access your organization's
          AI-powered knowledge workspace.
        </p>

      </div>

      {/* Bottom Glow */}

      <div
        className="
        pointer-events-none
        absolute
        -bottom-40
        left-1/2
        h-60
        w-60
        -translate-x-1/2
        rounded-full
        bg-blue-500/20
        blur-[120px]
        "
      />
    </motion.div>
  );
}

export default LoginCard;