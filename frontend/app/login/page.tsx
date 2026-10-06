"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function Login() {
  const r = useRouter();
  const [m, setM] = useState<"login" | "register" | "forgot" | "reset">("login");
  const [f, setF] = useState<any>({});
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPw, setShowPw] = useState(false);
  const [remember, setRemember] = useState(true);

  const set = (k: string) => (e: any) => setF({ ...f, [k]: e.target.value });

  async function go(e: any) {
    e.preventDefault();
    setMsg("");
    setLoading(true);
    try {
      if (m === "forgot") {
        const x = await api("/auth/forgot", { method: "POST", body: { email: f.email } });
        setMsg(x.note || "If the account exists, check the server console for the reset token.");
        setM("reset");
        return;
      }
      if (m === "reset") {
        await api("/auth/reset", { method: "POST", body: { token: f.token, password: f.password } });
        setMsg("Password updated successfully. Please sign in.");
        setM("login");
        return;
      }
      const x = await api(m === "login" ? "/auth/login" : "/auth/register", {
        method: "POST",
        body: m === "login" ? { email: f.email, password: f.password } : { email: f.email, password: f.password, name: f.name }
      });
      localStorage.setItem("token", x.token);
      const me = await api("/me");
      r.push(me.board ? "/home" : "/setup");
    } catch (e: any) {
      setMsg(e.message || "An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-2 bg-[#F9F6F0]">
      {/* Left Column: Cozy Study Hero Image */}
      <div className="relative min-h-[340px] md:min-h-screen overflow-hidden flex flex-col justify-between p-8 md:p-14 text-white">
        {/* Background photo */}
        <img
          src="/study_hero_bg.jpg"
          alt="Aesthetic study workspace"
          className="absolute inset-0 w-full h-full object-cover object-center transform scale-105 transition-transform duration-1000 ease-out"
        />

        {/* Cinematic atmospheric overlays */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#29221C]/90 via-[#3D3027]/40 to-[#2A231D]/45" />
        <div className="absolute inset-0 bg-[#4A382A]/20 mix-blend-multiply" />

        {/* Top Branding / Logo */}
        <div className="relative z-10 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/30 shadow-sm">
            <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
              <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12" />
            </svg>
          </div>
          <span className="font-serif text-3xl md:text-4xl tracking-tight font-medium text-white drop-shadow-sm">
            Marginalia
          </span>
        </div>

        {/* Hero Tagline & Description */}
        <div className="relative z-10 max-w-lg mt-12 md:mt-auto space-y-4">
          <h1 className="font-serif text-3xl sm:text-4xl md:text-5xl leading-tight text-white font-normal drop-shadow-md">
            Learn more.<br />
            Think deeper.<br />
            Build your tomorrow.
          </h1>
          <p className="text-white/85 text-sm md:text-base font-light leading-relaxed max-w-sm drop-shadow">
            Your personal AI study companion, for a smarter, brighter future.
          </p>
          <div className="pt-2 flex items-center gap-2 text-xs text-white/70">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-400"></span>
            Curriculum aligned for CBSE & ICSE
          </div>
        </div>
      </div>

      {/* Right Column: Authentication Card */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12 md:p-16">
        <div className="w-full max-w-md bg-white/80 md:bg-transparent backdrop-blur-sm md:backdrop-blur-none p-6 sm:p-8 md:p-0 rounded-2xl md:rounded-none shadow-sm md:shadow-none border border-[#E9E2D8] md:border-none">
          <div className="mb-8">
            <h2 className="font-serif text-3xl md:text-4xl text-[#3A2E2B] font-medium tracking-tight">
              {m === "login" && "Welcome back"}
              {m === "register" && "Create your account"}
              {m === "forgot" && "Reset password"}
              {m === "reset" && "Choose new password"}
            </h2>
            <p className="text-[#6D635B] text-sm mt-1.5">
              {m === "login" && "Sign in to continue your learning journey"}
              {m === "register" && "Join Marginalia and start mastering your syllabus"}
              {m === "forgot" && "Enter your email to receive a password reset token"}
              {m === "reset" && "Provide the token from backend console and your new password"}
            </p>
          </div>

          <form onSubmit={go} className="space-y-4">
            {m === "register" && (
              <div>
                <label className="block text-xs font-medium text-[#5A504A] mb-1.5">Your Name</label>
                <div className="relative">
                  <input
                    className="w-full px-4 py-3 rounded-xl border border-[#DCD3C7] bg-[#FAF8F5] text-[#2D2622] text-sm placeholder-[#9C9288] focus:outline-none focus:ring-2 focus:ring-[#684D43]/30 focus:border-[#684D43] transition-all"
                    placeholder="e.g. Ishita Sharma"
                    onChange={set("name")}
                    required
                  />
                </div>
              </div>
            )}

            {m !== "reset" && (
              <div>
                <label className="block text-xs font-medium text-[#5A504A] mb-1.5">Email address</label>
                <input
                  className="w-full px-4 py-3 rounded-xl border border-[#DCD3C7] bg-[#FAF8F5] text-[#2D2622] text-sm placeholder-[#9C9288] focus:outline-none focus:ring-2 focus:ring-[#684D43]/30 focus:border-[#684D43] transition-all"
                  type="email"
                  placeholder="student@example.com"
                  onChange={set("email")}
                  required
                />
              </div>
            )}

            {m === "reset" && (
              <div>
                <label className="block text-xs font-medium text-[#5A504A] mb-1.5">Reset Token</label>
                <input
                  className="w-full px-4 py-3 rounded-xl border border-[#DCD3C7] bg-[#FAF8F5] text-[#2D2622] text-sm placeholder-[#9C9288] focus:outline-none focus:ring-2 focus:ring-[#684D43]/30 focus:border-[#684D43] transition-all"
                  placeholder="Paste token from server logs"
                  onChange={set("token")}
                  required
                />
              </div>
            )}

            {m !== "forgot" && (
              <div>
                <label className="block text-xs font-medium text-[#5A504A] mb-1.5">Password</label>
                <div className="relative">
                  <input
                    className="w-full pl-4 pr-11 py-3 rounded-xl border border-[#DCD3C7] bg-[#FAF8F5] text-[#2D2622] text-sm placeholder-[#9C9288] focus:outline-none focus:ring-2 focus:ring-[#684D43]/30 focus:border-[#684D43] transition-all"
                    type={showPw ? "text" : "password"}
                    placeholder="8+ characters"
                    onChange={set("password")}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPw(!showPw)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#8C8075] hover:text-[#52463D] transition-colors p-1"
                    title={showPw ? "Hide password" : "Show password"}
                  >
                    {showPw ? (
                      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
                        <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68" />
                        <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61" />
                        <line x1="2" x2="22" y1="2" y2="22" />
                      </svg>
                    ) : (
                      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
                        <circle cx="12" cy="12" r="3" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* Remember me & Forgot Password */}
            {m === "login" && (
              <div className="flex items-center justify-between text-xs pt-1">
                <label className="flex items-center gap-2 cursor-pointer text-[#6D635B]">
                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                    className="rounded border-[#C8BEB2] text-[#684D43] focus:ring-[#684D43]"
                  />
                  <span>Remember me</span>
                </label>
                <button
                  type="button"
                  onClick={() => { setM("forgot"); setMsg(""); }}
                  className="text-[#9B6256] hover:text-[#7A453A] font-medium"
                >
                  Forgot password?
                </button>
              </div>
            )}

            {msg && (
              <div className="p-3 rounded-lg text-xs bg-[#FBF1EE] border border-[#F0D1C7] text-[#9B6256] flex items-center gap-2">
                <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                <span>{msg}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 py-3 px-4 rounded-xl bg-[#5C463D] hover:bg-[#483730] text-[#F9F6F0] font-medium text-sm transition-all duration-150 shadow-sm flex items-center justify-center gap-2 disabled:opacity-60 cursor-pointer"
            >
              {loading && (
                <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
              )}
              <span>
                {m === "login" && (loading ? "Signing in..." : "Sign in")}
                {m === "register" && (loading ? "Creating account..." : "Create account")}
                {m === "forgot" && (loading ? "Sending..." : "Request reset")}
                {m === "reset" && (loading ? "Updating..." : "Set new password")}
              </span>
            </button>
          </form>

          {/* Bottom Switcher */}
          <div className="mt-8 pt-6 border-t border-[#E8DFD3] text-center text-xs text-[#6D635B]">
            {m === "login" ? (
              <p>
                Don't have an account?{" "}
                <button
                  type="button"
                  onClick={() => { setM("register"); setMsg(""); }}
                  className="text-[#9B6256] font-semibold hover:underline"
                >
                  Create one
                </button>
              </p>
            ) : (
              <p>
                Already have an account?{" "}
                <button
                  type="button"
                  onClick={() => { setM("login"); setMsg(""); }}
                  className="text-[#9B6256] font-semibold hover:underline"
                >
                  Sign in
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
