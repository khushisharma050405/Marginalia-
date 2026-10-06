"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shell, useApi, api } from "@/lib/api";

export default function HomePage() {
  const { d } = useApi("/dashboard");
  const router = useRouter();

  // Quick question asking modal
  const [askModalOpen, setAskModalOpen] = useState(false);
  const [questionText, setQuestionText] = useState("");
  const [solving, setSolving] = useState(false);
  const [quickResult, setQuickResult] = useState<any>(null);
  const [quickError, setQuickError] = useState("");

  const sampleQuestions = [
    "Solve 3x + 15 = 42",
    "Calculate 144 / 12",
    "What is an ecosystem?",
    "Find the perimeter of rectangle: l=8, w=5",
  ];

  async function handleQuickSolve(e?: React.FormEvent) {
    if (e) e.preventDefault();
    if (!questionText.trim()) return;

    setSolving(true);
    setQuickError("");
    setQuickResult(null);

    try {
      const payload = {
        question: questionText.trim(),
        board: d?.user?.board || "CBSE",
        class_level: d?.user?.class_level || "10",
        stream: d?.user?.stream || null,
        subject: "General",
        chapter: "General",
      };
      const res = await api("/solve", { method: "POST", body: payload });
      setQuickResult(res);
    } catch (err: any) {
      setQuickError(err.message || "Failed to solve question");
    } finally {
      setSolving(false);
    }
  }

  const userName = d?.user?.name ? d.user.name.toUpperCase() : "KHUSHI";

  return (
    <Shell
      title={`Hello, ${userName}`}
      sub="Your personal study workspace."
    >
      <div className="w-full space-y-6">
        {/* 6 Clean Dashboard Cards (2 rows of 3 columns, perfectly aligned) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
          
          {/* CARD 1: Today's goal */}
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] relative overflow-hidden transition-all duration-200 hover:shadow-md group flex flex-col justify-between min-h-[195px] h-full">
            <div>
              <div className="flex items-center justify-between">
                {/* Icon badge */}
                <div className="w-10 h-10 rounded-full bg-[#E5EDE3] text-[#3D6649] flex items-center justify-center shadow-xs">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <circle cx="12" cy="12" r="6" />
                    <circle cx="12" cy="12" r="2" />
                  </svg>
                </div>

                {/* Arrow */}
                <Link href="/hub" className="text-[#C4B7A6] group-hover:text-[#4A443D] transition-colors p-1" title="Practice questions">
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </Link>
              </div>

              <div className="mt-4">
                <h3 className="text-xs font-semibold text-[#5C554E] tracking-wide">
                  Today&apos;s goal
                </h3>
                <div className="mt-1 flex items-baseline">
                  <span className="text-2xl font-bold text-[#272320]">
                    {d?.goal ? `${d.goal.done}/${d.goal.target}` : "0/10"}
                  </span>
                  <span className="text-xs text-[#524B44] font-medium ml-1.5">
                    practice questions
                  </span>
                </div>
              </div>

              {/* Progress bar */}
              <div className="h-2 w-full bg-[#E3EAE1] rounded-full overflow-hidden mt-3.5">
                <div
                  className="h-full bg-gradient-to-r from-[#6E9570] to-[#547E56] rounded-full transition-all duration-500"
                  style={{
                    width: `${Math.min(
                      100,
                      d?.goal ? (d.goal.done / d.goal.target) * 100 : 0
                    )}%`,
                  }}
                />
              </div>
            </div>

            <p className="text-xs text-[#526350] mt-4 font-medium flex items-center gap-1.5">
              You&apos;re doing great! Keep going! 🌱
            </p>
          </div>

          {/* CARD 2: Progress */}
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] relative overflow-hidden transition-all duration-200 hover:shadow-md group flex flex-col justify-between min-h-[195px] h-full">
            {/* Subtle lavender/periwinkle wave corner */}
            <div className="pointer-events-none absolute -bottom-8 -right-8 w-28 h-28 rounded-full bg-gradient-to-tl from-[#DDE5F5]/70 to-transparent blur-md" />

            <div>
              <div className="flex items-center justify-between">
                {/* Icon badge */}
                <div className="w-10 h-10 rounded-full bg-[#E6EBF5] text-[#476294] flex items-center justify-center shadow-xs">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
                    <polyline points="17 6 23 6 23 12" />
                  </svg>
                </div>

                {/* Arrow */}
                <Link href="/growth" className="text-[#C4B7A6] group-hover:text-[#4A443D] transition-colors p-1" title="View growth">
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </Link>
              </div>

              <div className="mt-4">
                <h3 className="text-xs font-semibold text-[#5C554E] tracking-wide">
                  Progress
                </h3>
                <div className="mt-1 flex items-baseline">
                  <span className="text-2xl font-bold text-[#272320]">
                    {d?.accuracy !== undefined ? `${d.accuracy}%` : "0%"}
                  </span>
                  <span className="text-xs text-[#524B44] ml-1.5">
                    accuracy · {d?.attempted || 0} attempted
                  </span>
                </div>
              </div>
            </div>

            <p className="text-xs text-[#7A7065] mt-4">
              Real-time accuracy based on curriculum questions.
            </p>
          </div>

          {/* CARD 3: Streak */}
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] relative overflow-hidden transition-all duration-200 hover:shadow-md group flex flex-col justify-between min-h-[195px] h-full">
            {/* Subtle peach wave corner */}
            <div className="pointer-events-none absolute -bottom-10 -right-10 w-32 h-32 rounded-full bg-gradient-to-tl from-[#FCE4D4]/80 to-transparent blur-md" />

            <div>
              <div className="flex items-center justify-between">
                {/* Icon badge */}
                <div className="w-10 h-10 rounded-full bg-[#FCEEE2] text-[#D4784B] flex items-center justify-center shadow-xs">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z" />
                  </svg>
                </div>

                {/* Arrow */}
                <div className="text-[#C4B7A6] group-hover:text-[#4A443D] transition-colors p-1">
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </div>
              </div>

              <div className="mt-4">
                <h3 className="text-xs font-semibold text-[#5C554E] tracking-wide">
                  Streak
                </h3>
                <div className="mt-1">
                  <span className="text-3xl font-bold text-[#272320]">
                    {d?.streak || 0} days
                  </span>
                </div>
              </div>
            </div>

            <p className="text-xs text-[#7A7065] mt-4">
              Consistency creates results.
            </p>
          </div>

          {/* CARD 4: Continue learning */}
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] relative overflow-hidden transition-all duration-200 hover:shadow-md group flex flex-col justify-between min-h-[195px] h-full">
            <div>
              <div className="flex items-center justify-between">
                {/* Icon badge */}
                <div className="w-10 h-10 rounded-full bg-[#F7EAE5] text-[#9E5D4B] flex items-center justify-center shadow-xs">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
                  </svg>
                </div>

                {/* Arrow */}
                <Link href="/solve" className="text-[#C4B7A6] group-hover:text-[#4A443D] transition-colors p-1" title="Go to Solve">
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </Link>
              </div>

              <div className="mt-4">
                <h3 className="text-xs font-semibold text-[#5C554E] tracking-wide mb-2">
                  Continue learning
                </h3>
                <div className="space-y-1.5 max-w-[210px]">
                  {d?.recommend?.length ? (
                    d.recommend.slice(0, 3).map((c: any) => (
                      <Link
                        key={c.id}
                        href={`/solve?chapter=${encodeURIComponent(c.name)}${c.subject_name ? `&subject=${encodeURIComponent(c.subject_name)}` : ""}`}
                        className="block text-xs font-serif text-[#9E5646] hover:text-[#7B3F31] hover:underline leading-snug truncate"
                        title={`Solve questions from ${c.name}`}
                      >
                        {c.name}
                      </Link>
                    ))
                  ) : (
                    <>
                      <Link href="/solve" className="block text-xs font-serif text-[#9E5646] hover:underline leading-snug">
                        Mathematics &amp; Problem Solving
                      </Link>
                      <Link href="/solve" className="block text-xs font-serif text-[#9E5646] hover:underline leading-snug">
                        Science &amp; Conceptual Theory
                      </Link>
                      <Link href="/solve" className="block text-xs font-serif text-[#9E5646] hover:underline leading-snug">
                        Language, Grammar &amp; Literature
                      </Link>
                    </>
                  )}
                </div>
              </div>
            </div>

            {/* Bottom right decorative illustration: stacked books + pen cup */}
            <div className="absolute right-3 bottom-2 pointer-events-none">
              <svg className="w-20 h-16" viewBox="0 0 90 70" fill="none">
                {/* Bottom book: terracotta */}
                <path d="M10 52 L60 52 L57 62 L7 62 Z" fill="#D48C75" />
                <rect x="7" y="58" width="53" height="4" rx="2" fill="#BD725B" />
                <path d="M12 55 L58 55" stroke="#F6ECE7" strokeWidth="1" />

                {/* Middle book: cream/sand */}
                <path d="M14 43 L62 43 L59 52 L11 52 Z" fill="#E8DEC8" />
                <rect x="11" y="48" width="51" height="4" rx="2" fill="#D1C3A5" />

                {/* Top book: dark sage green */}
                <path d="M18 35 L64 35 L62 43 L16 43 Z" fill="#4B6854" />
                <rect x="16" y="39" width="48" height="4" rx="2" fill="#3B5242" />

                {/* Pencil Cup */}
                <path d="M64 32 L78 32 L76 60 L66 60 Z" fill="#FAF5ED" stroke="#D3C9B8" strokeWidth="1.5" />
                {/* Pencils */}
                <line x1="68" y1="18" x2="70" y2="32" stroke="#D48C75" strokeWidth="3" strokeLinecap="round" />
                <line x1="73" y1="14" x2="73" y2="32" stroke="#4B6854" strokeWidth="3" strokeLinecap="round" />
                <line x1="77" y1="20" x2="75" y2="32" stroke="#5C548C" strokeWidth="3" strokeLinecap="round" />
              </svg>
            </div>
          </div>

          {/* CARD 5: Weak areas */}
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] relative overflow-hidden transition-all duration-200 hover:shadow-md group flex flex-col justify-between min-h-[195px] h-full">
            {/* Soft warm wave corner */}
            <div className="pointer-events-none absolute -bottom-10 -right-10 w-28 h-28 rounded-full bg-gradient-to-tl from-[#F9ECE7]/70 to-transparent blur-md" />

            <div>
              <div className="flex items-center justify-between">
                {/* Icon badge */}
                <div className="w-10 h-10 rounded-full bg-[#F9ECE7] text-[#B05844] flex items-center justify-center shadow-xs">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                </div>

                {/* Arrow */}
                <Link href="/growth" className="text-[#C4B7A6] group-hover:text-[#4A443D] transition-colors p-1" title="View weak areas">
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </Link>
              </div>

              <div className="mt-4">
                <h3 className="text-xs font-semibold text-[#5C554E] tracking-wide mb-2">
                  Weak areas
                </h3>
                <div className="text-xs text-[#6B635B]">
                  {d?.weak?.length ? (
                    d.weak.map((w: any) => (
                      <p key={w.name} className="truncate">
                        {w.name} — <span className="text-[#9E5646] font-medium">{w.acc}%</span>
                      </p>
                    ))
                  ) : (
                    <p>
                      None yet.{" "}
                      <Link href="/hub" className="text-[#9E5646] font-medium hover:underline">
                        Start practising
                      </Link>
                    </p>
                  )}
                </div>
              </div>
            </div>

            <p className="text-[11px] text-[#8C8377] mt-4">
              Targeted revision unlocks faster mastery.
            </p>
          </div>

          {/* CARD 6: Dedicated Solve History Option */}
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] relative overflow-hidden transition-all duration-200 hover:shadow-md group flex flex-col justify-between min-h-[195px] h-full">
            <div>
              <div className="flex items-center justify-between">
                {/* Icon badge */}
                <div className="w-10 h-10 rounded-full bg-[#F7EBE4] text-[#A6614E] flex items-center justify-center shadow-xs">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                  </svg>
                </div>

                {/* Arrow to dedicated /history page */}
                <Link
                  href="/history"
                  className="text-[#C4B7A6] group-hover:text-[#4A443D] transition-colors p-1"
                  title="View full solve history"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </Link>
              </div>

              <div className="mt-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xs font-semibold text-[#5C554E] tracking-wide">
                    Solve History
                  </h3>
                  <span className="text-[11px] font-medium text-[#7A7369] bg-[#FAF5ED] px-2 py-0.5 rounded-full border border-[#EDE7DF]">
                    {d?.solved ? `${d.solved} solved` : "History"}
                  </span>
                </div>

                <div className="text-xs">
                  {d?.recent?.length ? (
                    <div className="space-y-1.5">
                      {d.recent.slice(0, 2).map((q: any) => (
                        <Link
                          key={q.id}
                          href={`/solve?q=${encodeURIComponent(q.question)}`}
                          className="block text-xs text-[#9E5646] hover:underline truncate"
                        >
                          • {q.question}
                        </Link>
                      ))}
                      <Link
                        href="/history"
                        className="text-[11px] text-[#554D45] hover:text-[#9E5646] font-medium underline mt-1.5 inline-flex items-center gap-1"
                      >
                        <span>View complete history</span>
                        <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M5 12h14" />
                          <path d="m12 5 7 7-7 7" />
                        </svg>
                      </Link>
                    </div>
                  ) : (
                    <Link
                      href="/solve"
                      className="text-[#9E5646] font-medium hover:underline text-xs text-left cursor-pointer transition-colors block"
                    >
                      No history yet. Solve your first question →
                    </Link>
                  )}
                </div>
              </div>
            </div>

            <div className="mt-3 pt-2 border-t border-[#F2ECE4] flex items-center justify-between text-[11px] text-[#8C8377]">
              <span>Saved automatically</span>
              <Link href="/history" className="text-[#A6614E] font-medium hover:underline">
                Open History →
              </Link>
            </div>
          </div>
        </div>

        {/* Full-Width Section: "Your learning path" */}
        <div className="w-full bg-white/95 rounded-2xl md:rounded-3xl p-6 md:p-8 border border-[#EDE7DF] shadow-[0_4px_24px_-4px_rgba(80,60,40,0.04)] relative overflow-hidden mt-6">
          {/* Header of Learning Path */}
          <div className="flex items-center justify-between mb-8 relative z-10">
            <div className="flex items-center gap-3">
              {/* Botanical Sprout Icon */}
              <div className="text-[#3D6649]">
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M7 20h10" />
                  <path d="M10 20c5.5-2.5.8-6.4 3-10" />
                  <path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4.1 5.5.8z" />
                  <path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z" />
                </svg>
              </div>
              <div>
                <h2 className="font-serif text-lg md:text-xl font-medium text-[#223328] tracking-tight">
                  Your learning path
                </h2>
                <p className="text-xs text-[#7A7369] mt-0.5">
                  A simple journey to better understanding
                </p>
              </div>
            </div>

            <Link
              href="/hub"
              className="text-xs font-medium px-4 py-1.5 rounded-full border border-[#DCD5C9] bg-white text-[#4A443D] hover:bg-[#FAF7F2] transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <span>View all</span>
              <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14" />
                <path d="m12 5 7 7-7 7" />
              </svg>
            </Link>
          </div>

          {/* 4 Clean Milestone Steps with subtle dotted guide line */}
          <div className="relative z-10">
            {/* Subtle connecting dotted guide line behind step icons (desktop only) */}
            <div className="hidden md:block absolute top-6 left-12 right-12 h-0.5 border-t border-dashed border-[#DCD5C9] z-0 pointer-events-none" />

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 relative z-10">
              {/* STEP 1: Understand */}
              <div className="relative group">
                <div className="w-12 h-12 rounded-2xl bg-[#E5EDE3] text-[#3D6649] flex items-center justify-center shadow-xs transition-transform group-hover:scale-105 border border-white">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
                  </svg>
                </div>
                <h4 className="font-medium text-xs text-[#2A2622] mt-3">
                  1. Understand
                </h4>
                <p className="text-[11px] text-[#7A7369] mt-0.5 leading-snug">
                  Build your foundation
                </p>
              </div>

              {/* STEP 2: Practise */}
              <div className="relative group">
                <div className="w-12 h-12 rounded-2xl bg-[#EDEBF5] text-[#5C548C] flex items-center justify-center shadow-xs transition-transform group-hover:scale-105 border border-white">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="16" y1="13" x2="8" y2="13" />
                    <line x1="16" y1="17" x2="8" y2="17" />
                  </svg>
                </div>
                <h4 className="font-medium text-xs text-[#2A2622] mt-3">
                  2. Practise
                </h4>
                <p className="text-[11px] text-[#7A7369] mt-0.5 leading-snug">
                  Apply what you learn
                </p>
              </div>

              {/* STEP 3: Improve */}
              <div className="relative group">
                <div className="w-12 h-12 rounded-2xl bg-[#FBF0DE] text-[#B87A29] flex items-center justify-center shadow-xs transition-transform group-hover:scale-105 border border-white">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                  </svg>
                </div>
                <h4 className="font-medium text-xs text-[#2A2622] mt-3">
                  3. Improve
                </h4>
                <p className="text-[11px] text-[#7A7369] mt-0.5 leading-snug">
                  Track your progress
                </p>
              </div>

              {/* STEP 4: Master */}
              <div className="relative group">
                <div className="w-12 h-12 rounded-2xl bg-[#E5EDE5] text-[#3B6A47] flex items-center justify-center shadow-xs transition-transform group-hover:scale-105 border border-white">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
                    <path d="M2 21c0-3 1.85-5.36 5.08-6" />
                  </svg>
                </div>
                <h4 className="font-medium text-xs text-[#2A2622] mt-3">
                  4. Master
                </h4>
                <p className="text-[11px] text-[#7A7369] mt-0.5 leading-snug">
                  Achieve your goals
                </p>
              </div>
            </div>
          </div>

          {/* Scenic Landscape Illustration on Bottom Right */}
          <div className="absolute right-0 bottom-0 w-64 h-36 pointer-events-none overflow-hidden select-none z-0 opacity-90">
            <svg viewBox="0 0 260 145" fill="none" className="w-full h-full">
              {/* Sunrise sun */}
              <circle cx="188" cy="55" r="23" fill="#FCE0BE" />

              {/* Back rolling hill */}
              <path d="M70 145 Q 160 82 260 102 L 260 145 Z" fill="#DFE8DC" />

              {/* Middle rolling hill */}
              <path d="M115 145 Q 185 96 260 122 L 260 145 Z" fill="#CCDBC7" />

              {/* Front rolling hill */}
              <path d="M150 145 Q 210 112 260 136 L 260 145 Z" fill="#B4CBB0" />

              {/* Botanical reeds / meadow stalks */}
              <g stroke="#2C4837" strokeWidth="1.5" strokeLinecap="round" opacity="0.85">
                {/* Tall central stalk */}
                <path d="M230 145 C230 110 234 80 236 50" />
                <path d="M234 85 C242 80 248 83 248 83" />
                <path d="M233 98 C224 95 220 99 220 99" />
                <path d="M235 68 C242 63 246 66 246 66" />
                <path d="M235 55 C230 50 228 53 228 53" />

                {/* Second stalk */}
                <path d="M245 145 C247 120 250 95 252 70" />
                <path d="M249 105 C255 101 258 103 258 103" />
                <path d="M248 118 C242 115 239 118 239 118" />
                <path d="M251 85 C256 81 258 83 258 83" />

                {/* Third stalk */}
                <path d="M218 145 C220 130 222 110 224 95" />
                <path d="M222 115 C216 112 214 115 214 115" />
                <path d="M223 102 C228 98 231 100 231 100" />
              </g>
            </svg>
          </div>
        </div>
      </div>

      {/* Quick Interactive Question Modal */}
      {askModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
          <div className="bg-[#FAF7F2] border border-[#E5DFD5] w-full max-w-lg rounded-3xl p-6 shadow-2xl relative animate-in fade-in zoom-in-95 duration-200">
            {/* Close button */}
            <button
              onClick={() => {
                setAskModalOpen(false);
                setQuickResult(null);
                setQuickError("");
              }}
              className="absolute top-4 right-4 text-[#8C8377] hover:text-[#25221E] w-8 h-8 rounded-full flex items-center justify-center hover:bg-[#EFECE6] transition-colors"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>

            {/* Modal Header */}
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-[#F7EBE4] text-[#A6614E] flex items-center justify-center shadow-xs">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 20h9" />
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                </svg>
              </div>
              <div>
                <h3 className="font-serif text-xl font-medium text-[#29221C]">
                  Ask Marginalia
                </h3>
                <p className="text-xs text-[#7A7369]">
                  Get instant step-by-step verified solutions for CBSE &amp; ICSE
                </p>
              </div>
            </div>

            {/* Form */}
            <form onSubmit={handleQuickSolve} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-[#5A504A] mb-1.5">
                  Type your question:
                </label>
                <textarea
                  className="w-full h-24 px-4 py-3 rounded-xl border border-[#DCD3C7] bg-white text-[#2D2622] text-sm placeholder-[#9C9288] focus:outline-none focus:ring-2 focus:ring-[#684D43]/30 focus:border-[#684D43] transition-all resize-none"
                  placeholder="e.g. Solve 2x + 7 = 19 or Calculate 35 * 12"
                  value={questionText}
                  onChange={(e) => setQuestionText(e.target.value)}
                  autoFocus
                />
              </div>

              {/* Sample Quick Questions */}
              <div>
                <span className="text-[11px] font-medium text-[#7D766E] block mb-1.5">
                  Or pick a sample question:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {sampleQuestions.map((q) => (
                    <button
                      key={q}
                      type="button"
                      onClick={() => setQuestionText(q)}
                      className="text-xs bg-[#EFECE6] hover:bg-[#E2DDD3] text-[#4A433B] px-3 py-1 rounded-full transition-colors"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>

              {quickError && (
                <div className="p-3 rounded-xl text-xs bg-[#FBF1EE] border border-[#F0D1C7] text-[#9B6256]">
                  {quickError}
                </div>
              )}

              {/* Quick Result Preview */}
              {quickResult && (
                <div className="p-4 rounded-2xl bg-white border border-[#EDE7DF] space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-[#3D6649] flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                      Verified Solution
                    </span>
                    <span className="text-[11px] text-[#7A7369]">
                      Confidence: {quickResult.confidence}%
                    </span>
                  </div>
                  <div className="text-sm font-medium text-[#29221C]">
                    Answer: {quickResult.steps?.[quickResult.steps.length - 1]?.[1] || "Solved"}
                  </div>
                  <div className="pt-2 border-t border-[#F0EBE3] flex justify-end">
                    <button
                      type="button"
                      onClick={() => {
                        setAskModalOpen(false);
                        router.push(`/solve?q=${encodeURIComponent(questionText)}`);
                      }}
                      className="text-xs text-[#9E5646] font-medium hover:underline flex items-center gap-1"
                    >
                      View full step-by-step derivation →
                    </button>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-2">
                <button
                  type="button"
                  onClick={() => {
                    setAskModalOpen(false);
                    router.push(questionText ? `/solve?q=${encodeURIComponent(questionText)}` : "/solve");
                  }}
                  className="text-xs text-[#7A7369] hover:text-[#25221E] underline"
                >
                  Upload image or PDF instead
                </button>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setAskModalOpen(false)}
                    className="px-4 py-2 rounded-xl text-xs font-medium text-[#6B6359] hover:bg-[#EFECE6] transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={solving || !questionText.trim()}
                    className="px-5 py-2 rounded-xl bg-[#5C463D] hover:bg-[#483730] text-[#F9F6F0] text-xs font-medium transition-all shadow-xs disabled:opacity-50 flex items-center gap-2"
                  >
                    {solving && (
                      <svg className="animate-spin h-3.5 w-3.5 text-white" viewBox="0 0 24 24" fill="none">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                      </svg>
                    )}
                    <span>{solving ? "Solving..." : "Solve Question"}</span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </Shell>
  );
}
