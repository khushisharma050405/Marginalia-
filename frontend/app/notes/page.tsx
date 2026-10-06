"use client";
import React, { useState } from "react";
import { Shell, api, useApi } from "@/lib/api";

export default function StudyNotesPage() {
  const { d, reload } = useApi("/notes");
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [filter, setFilter] = useState("all");
  const [submitting, setSubmitting] = useState(false);

  const add = async (kind: string) => {
    if (!title.trim()) return;
    setSubmitting(true);
    try {
      await api("/notes", {
        method: "POST",
        body: { kind, title: title.trim(), body: body.trim() },
      });
      setTitle("");
      setBody("");
      reload();
    } finally {
      setSubmitting(false);
    }
  };

  const deleteNote = async (id: number) => {
    await api("/notes/" + id, { method: "DELETE" });
    reload();
  };

  const filteredNotes = (d || []).filter((n: any) => {
    if (filter === "all") return true;
    return n.kind === filter;
  });

  return (
    <Shell
      title="Study Notes"
      sub="Saved solutions, personal notes, and bookmarks."
    >
      <div className="max-w-5xl space-y-4">
        {/* Note creation card */}
        <div className="card space-y-2.5 bg-white/95 rounded-2xl p-4 sm:p-5 border border-[#EDE7DF] shadow-xs">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-semibold text-[#5C554E] tracking-wider uppercase">
              Create Note or Bookmark
            </h2>
            <span className="text-[11px] text-[#8A8177]">Personal Study Bank</span>
          </div>
          <input
            className="inp w-full bg-[#FAF7F2] border border-[#E3DBD0] rounded-xl px-3.5 py-2 text-xs md:text-sm text-[#272320] placeholder-[#8A8177] focus:outline-none focus:border-[#4B6854]"
            placeholder="Note title or formula header..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <textarea
            className="inp w-full bg-[#FAF7F2] border border-[#E3DBD0] rounded-xl px-3.5 py-2 text-xs md:text-sm text-[#272320] placeholder-[#8A8177] min-h-[72px] focus:outline-none focus:border-[#4B6854]"
            placeholder="Key summary, formulas, steps, or study reminders..."
            value={body}
            onChange={(e) => setBody(e.target.value)}
          />
          <div className="flex items-center justify-between pt-0.5">
            <div className="flex gap-2">
              <button
                className="btn px-3.5 py-1.5 bg-[#4B6854] text-white rounded-xl text-xs font-semibold hover:bg-[#3B5242] transition-colors disabled:opacity-50 shadow-xs"
                disabled={!title.trim() || submitting}
                onClick={() => add("note")}
              >
                + Add Note
              </button>
              <button
                className="btn px-3.5 py-1.5 bg-[#FAF5ED] border border-[#DCD5C9] text-[#4A443D] rounded-xl text-xs font-semibold hover:bg-[#F2ECE1] transition-colors disabled:opacity-50"
                disabled={!title.trim() || submitting}
                onClick={() => add("bookmark")}
              >
                🔖 Bookmark
              </button>
            </div>
            <span className="text-[11px] text-[#8A8177]">Autosaved to your account</span>
          </div>
        </div>

        {/* Filter pills */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex gap-1.5">
            {[
              ["all", "All Items"],
              ["note", "Notes"],
              ["bookmark", "Bookmarks"],
              ["saved", "Saved Solutions"]
            ].map(([k, label]) => (
              <button
                key={k}
                onClick={() => setFilter(k)}
                className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                  filter === k
                    ? "bg-[#292A28] text-white"
                    : "bg-white/80 border border-[#EDE7DF] text-[#6B635B] hover:bg-[#F6F1EA]"
                }`}
              >
                {label}
              </button>
            ))}
          </div>
          <span className="text-xs font-medium text-[#8A8177]">
            {filteredNotes.length} {filteredNotes.length === 1 ? "entry" : "entries"}
          </span>
        </div>

        {/* Notes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {filteredNotes.map((n: any) => (
            <div
              key={n.id}
              className="card bg-white/95 rounded-xl p-3.5 sm:p-4 border border-[#EDE7DF] shadow-xs flex flex-col justify-between hover:border-[#D5CDC2] transition-colors"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <h3 className="font-serif text-sm md:text-base font-semibold text-[#272320] line-clamp-2">
                    {n.title}
                  </h3>
                  <button
                    className="text-[11px] text-[#B05844] hover:underline shrink-0"
                    onClick={() => deleteNote(n.id)}
                  >
                    Delete
                  </button>
                </div>
                <div className="mt-1">
                  <span className="inline-block text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-md bg-[#FAF5ED] text-[#6B635B] border border-[#EBE4D8]">
                    {n.kind}
                  </span>
                </div>
                <p className="mt-2.5 whitespace-pre-wrap text-xs text-[#4A443D] leading-relaxed line-clamp-6">
                  {n.body || "No additional details."}
                </p>
              </div>
            </div>
          ))}

          {d && !filteredNotes.length && (
            <div className="col-span-full p-6 text-center bg-white/70 rounded-2xl border border-dashed border-[#DCD5C9]">
              <p className="text-xs text-[#7A7369]">
                No notes or bookmarks found in this view. Use the form above to add your first note!
              </p>
            </div>
          )}
        </div>
      </div>
    </Shell>
  );
}
