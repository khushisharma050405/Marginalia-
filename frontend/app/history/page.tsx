"use client";
import React, { useState } from "react";
import Link from "next/link";
import { Shell, useApi } from "@/lib/api";

export default function HistoryPage() {
  const { d: history, reload } = useApi("/history");
  const [searchTerm, setSearchTerm] = useState("");
  const [selSubject, setSelSubject] = useState("all");

  const solves = history || [];

  // Extract unique subjects
  const subjects = Array.from(
    new Set(solves.map((s: any) => s.subject).filter(Boolean))
  );

  const filteredSolves = solves.filter((item: any) => {
    const matchesSearch =
      !searchTerm.trim() ||
      item.question?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.topic?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSubject =
      selSubject === "all" || item.subject === selSubject;
    return matchesSearch && matchesSubject;
  });

  return (
    <Shell
      title="Solve History"
      sub="Review and re-solve past questions with detailed step-by-step explanations."
    >
      <div className="max-w-4xl space-y-6">
        {/* Search & Subject Filters */}
        <div className="bg-white/95 rounded-2xl md:rounded-3xl p-5 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] flex flex-col md:flex-row gap-4 items-stretch md:items-center justify-between">
          <div className="relative flex-1">
            <svg
              className="w-4 h-4 text-[#8C8377] absolute left-3.5 top-1/2 -translate-y-1/2"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="text"
              placeholder="Search previous questions or topics..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-[#FAF7F2] border border-[#E3DBD0] rounded-xl pl-10 pr-4 py-2 text-sm text-[#272320] placeholder-[#8A8177] focus:outline-none focus:border-[#4B6854]"
            />
          </div>

          {/* Subject Pills */}
          <div className="flex gap-2 overflow-x-auto pb-1 md:pb-0">
            <button
              onClick={() => setSelSubject("all")}
              className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-colors ${
                selSubject === "all"
                  ? "bg-[#292A28] text-white"
                  : "bg-[#FAF7F2] border border-[#EDE7DF] text-[#6B635B] hover:bg-[#F2ECE1]"
              }`}
            >
              All Subjects
            </button>
            {subjects.map((sub: any) => (
              <button
                key={sub}
                onClick={() => setSelSubject(sub)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-colors ${
                  selSubject === sub
                    ? "bg-[#292A28] text-white"
                    : "bg-[#FAF7F2] border border-[#EDE7DF] text-[#6B635B] hover:bg-[#F2ECE1]"
                }`}
              >
                {sub}
              </button>
            ))}
          </div>
        </div>

        {/* History Items Count */}
        <div className="flex items-center justify-between px-1">
          <span className="text-xs font-medium text-[#7A7369]">
            Showing {filteredSolves.length} solved{" "}
            {filteredSolves.length === 1 ? "question" : "questions"}
          </span>
          <button
            onClick={() => reload()}
            className="text-xs text-[#4B6854] hover:underline flex items-center gap-1 font-medium"
          >
            <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67" />
            </svg>
            Refresh
          </button>
        </div>

        {/* List of Solved Questions */}
        <div className="space-y-3.5">
          {filteredSolves.map((item: any) => (
            <div
              key={item.id}
              className="bg-white/95 rounded-2xl p-5 border border-[#EDE7DF] shadow-[0_2px_12px_-2px_rgba(80,60,40,0.03)] hover:shadow-md transition-shadow group flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-1.5 flex-1 min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-[#E5EDE3] text-[#3D6649]">
                    {item.subject || "General"}
                  </span>
                  {item.topic && (
                    <span className="text-[11px] font-medium px-2.5 py-0.5 rounded-full bg-[#FAF5ED] text-[#7A6F62] border border-[#EBE4D8] truncate max-w-[250px]">
                      {item.topic}
                    </span>
                  )}
                  {item.created_at && (
                    <span className="text-[11px] text-[#A3998E]">
                      {item.created_at}
                    </span>
                  )}
                </div>

                <p className="font-serif text-base text-[#272320] leading-snug pt-0.5 line-clamp-2">
                  {item.question}
                </p>
              </div>

              {/* Action Button */}
              <div className="flex items-center gap-2 shrink-0">
                <Link
                  href={`/solve?q=${encodeURIComponent(item.question)}`}
                  className="px-4 py-2 rounded-xl bg-[#FAF5ED] hover:bg-[#F2ECE1] border border-[#DCD5C9] text-xs font-semibold text-[#4A443D] transition-colors flex items-center gap-1.5 group-hover:border-[#4B6854]/40"
                >
                  <span>Re-solve Solution</span>
                  <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </Link>
              </div>
            </div>
          ))}

          {history && !filteredSolves.length && (
            <div className="p-12 text-center bg-white/70 rounded-3xl border border-dashed border-[#DCD5C9] space-y-3">
              <div className="w-12 h-12 rounded-full bg-[#FAF5ED] text-[#8C8377] flex items-center justify-center mx-auto">
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
              </div>
              <h3 className="font-serif text-base font-medium text-[#272320]">
                No solved questions found
              </h3>
              <p className="text-xs text-[#7A7369] max-w-sm mx-auto">
                Whenever you solve questions on Marginalia, they are automatically saved here for rapid review and exam practice.
              </p>
              <div className="pt-2">
                <Link
                  href="/solve"
                  className="inline-flex items-center gap-1.5 px-4 py-2 bg-[#4B6854] text-white rounded-xl text-xs font-medium hover:bg-[#3B5242] transition-colors"
                >
                  Solve your first question
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </Shell>
  );
}
