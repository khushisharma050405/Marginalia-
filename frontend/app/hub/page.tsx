"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Shell, api, useApi } from "@/lib/api";

export default function LearningHubPage() {
  const { d: stats, reload: reloadStats } = useApi("/growth");
  const { d: subjectsList } = useApi("/subjects");

  // Mode: "topic" (recommended), "mixed", "revision", "weak"
  const [practiceMode, setPracticeMode] = useState<"topic" | "mixed" | "revision" | "weak">("topic");

  // Topic-wise selection state
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | null>(null);
  const [chaptersData, setChaptersData] = useState<any[]>([]);
  const [selectedChapterId, setSelectedChapterId] = useState<number | null>(null);
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);
  const [difficulty, setDifficulty] = useState<"Easy" | "Medium" | "Hard">("Medium");

  // Active quiz state
  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [feedback, setFeedback] = useState<any>(null);
  const [startTime, setStartTime] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [quizFinished, setQuizFinished] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  // Auto-select first subject when subjects load
  useEffect(() => {
    if (subjectsList && subjectsList.length > 0 && !selectedSubjectId) {
      setSelectedSubjectId(subjectsList[0].id);
    }
  }, [subjectsList]);

  // Load chapters when selected subject changes
  useEffect(() => {
    if (selectedSubjectId) {
      api(`/subjects/${selectedSubjectId}`)
        .then((res) => {
          const chs = res.chapters || [];
          setChaptersData(chs);
          if (chs.length > 0) {
            setSelectedChapterId(chs[0].id);
            if (chs[0].topics && chs[0].topics.length > 0) {
              setSelectedTopicId(chs[0].topics[0].id);
            } else {
              setSelectedTopicId(null);
            }
          } else {
            setSelectedChapterId(null);
            setSelectedTopicId(null);
          }
        })
        .catch(() => {
          setChaptersData([]);
        });
    }
  }, [selectedSubjectId]);

  // Update selected topic when chapter changes
  const activeChapter = chaptersData.find((c) => c.id === selectedChapterId);
  const availableTopics = activeChapter?.topics || [];

  const handleChapterChange = (chapterId: number) => {
    setSelectedChapterId(chapterId);
    const ch = chaptersData.find((c) => c.id === chapterId);
    if (ch && ch.topics && ch.topics.length > 0) {
      setSelectedTopicId(ch.topics[0].id);
    } else {
      setSelectedTopicId(null);
    }
  };

  // Start Topic-wise 10 Questions Practice
  async function startTopicPractice(overrideDiff?: "Easy" | "Medium" | "Hard") {
    const diffToUse = overrideDiff || difficulty;
    if (overrideDiff) setDifficulty(overrideDiff);

    if (!selectedTopicId) {
      setStatusMessage("Please select a topic first.");
      return;
    }

    setLoadingQuestions(true);
    setStatusMessage("");
    setQuizFinished(false);

    try {
      const url = `/practice?topic_id=${selectedTopicId}&difficulty=${diffToUse}`;
      const qs = await api(url);
      if (!qs || qs.length === 0) {
        setStatusMessage("No questions available for this combination. Generating new questions...");
      }
      setQuestions(qs);
      setCurrentIndex(0);
      setFeedback(null);
      setCorrectCount(0);
      setStartTime(Date.now());
    } catch (err: any) {
      setStatusMessage(err.message || "Failed to load questions.");
    } finally {
      setLoadingQuestions(false);
    }
  }

  // Start Generic / Mixed Practice
  async function startGenericPractice(m: "mixed" | "revision" | "weak", diff?: string) {
    setPracticeMode(m);
    setLoadingQuestions(true);
    setStatusMessage("");
    setQuizFinished(false);

    try {
      let url = `/practice?mode=${m}`;
      if (diff) url += `&difficulty=${diff}`;
      const qs = await api(url);
      setQuestions(qs);
      setCurrentIndex(0);
      setFeedback(null);
      setCorrectCount(0);
      setStartTime(Date.now());
      if (!qs.length) {
        setStatusMessage(
          m === "revision"
            ? "No mistakes to revise yet. Great job!"
            : m === "weak"
            ? "No weak topics identified yet. Try some topic practice!"
            : "No practice questions found."
        );
      }
    } catch (err: any) {
      setStatusMessage(err.message || "Failed to load practice questions.");
    } finally {
      setLoadingQuestions(false);
    }
  }

  // Answer a question
  async function handleAnswer(choiceIdx: number) {
    if (feedback || !questions[currentIndex]) return;
    const q = questions[currentIndex];
    const seconds = Math.max(1, Math.round((Date.now() - startTime) / 1000));

    try {
      const res = await api("/practice/attempt", {
        method: "POST",
        body: {
          question_id: q.id,
          choice: choiceIdx,
          seconds,
        },
      });

      setFeedback({
        ...res,
        chosenIdx: choiceIdx,
      });

      if (res.correct) {
        setCorrectCount((prev) => prev + 1);
      }
      reloadStats();
    } catch (err: any) {
      console.error(err);
    }
  }

  // Next question
  function handleNext() {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setFeedback(null);
      setStartTime(Date.now());
    } else {
      setQuizFinished(true);
    }
  }

  const currentQ = questions[currentIndex];
  const progressPercent = questions.length
    ? Math.round(((currentIndex + (feedback ? 1 : 0)) / questions.length) * 100)
    : 0;

  return (
    <Shell
      title="Learning Hub"
      sub="Topic-wise curriculum practice with MCQs, True/False & Fill-in-the-Blank questions."
    >
      <div className="w-full space-y-5">
        {/* Practice Mode Selector Tabs */}
        <div className="flex flex-wrap items-center justify-between gap-2.5 bg-white/95 rounded-2xl p-2 border border-[#EDE7DF] shadow-xs">
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => {
                setPracticeMode("topic");
                setQuestions([]);
                setQuizFinished(false);
              }}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                practiceMode === "topic"
                  ? "bg-[#292A28] text-white shadow-xs"
                  : "text-[#6B635B] hover:bg-[#FAF7F2] hover:text-[#272320]"
              }`}
            >
              ✦ Topic-wise Practice
            </button>
            <button
              onClick={() => {
                setPracticeMode("mixed");
                setQuestions([]);
                setQuizFinished(false);
              }}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                practiceMode === "mixed"
                  ? "bg-[#292A28] text-white shadow-xs"
                  : "text-[#6B635B] hover:bg-[#FAF7F2] hover:text-[#272320]"
              }`}
            >
              Mixed Practice
            </button>
            <button
              onClick={() => {
                setPracticeMode("revision");
                setQuestions([]);
                setQuizFinished(false);
              }}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                practiceMode === "revision"
                  ? "bg-[#292A28] text-white shadow-xs"
                  : "text-[#6B635B] hover:bg-[#FAF7F2] hover:text-[#272320]"
              }`}
            >
              Revision (Mistakes)
            </button>
            <button
              onClick={() => {
                setPracticeMode("weak");
                setQuestions([]);
                setQuizFinished(false);
              }}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                practiceMode === "weak"
                  ? "bg-[#292A28] text-white shadow-xs"
                  : "text-[#6B635B] hover:bg-[#FAF7F2] hover:text-[#272320]"
              }`}
            >
              Weak Topics
            </button>
          </div>

          {/* Quick link to Solve History */}
          <Link
            href="/history"
            className="text-xs text-[#A6614E] font-medium hover:underline px-2.5 py-1 flex items-center gap-1"
          >
            <span>Solve History</span>
            <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14" />
              <path d="m12 5 7 7-7 7" />
            </svg>
          </Link>
        </div>

        {/* ------------------------------------------------------------- */}
        {/* TOPIC-WISE CONFIGURATION PANEL */}
        {/* ------------------------------------------------------------- */}
        {practiceMode === "topic" && questions.length === 0 && !quizFinished && (
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-4 sm:p-5 md:p-6 border border-[#EDE7DF] shadow-xs space-y-4">
            <div>
              <div className="flex items-center justify-between">
                <h2 className="font-serif text-lg md:text-xl font-medium text-[#223328]">
                  Select Topic & Difficulty
                </h2>
                <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-[#E5EDE3] text-[#3D6649]">
                  10 Standard Questions (MCQ · True/False · Fill in Blank)
                </span>
              </div>
              <p className="text-xs text-[#7A7369] mt-0.5">
                Includes multiple-choice, true/false, and sentence completion questions strictly matching your class syllabus.
              </p>
            </div>

            {/* 1. Subject Pills */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-semibold text-[#5C554E] uppercase tracking-wider">
                1. Select Subject
              </label>
              <div className="flex flex-wrap gap-1.5">
                {(subjectsList || []).map((s: any) => (
                  <button
                    key={s.id}
                    onClick={() => setSelectedSubjectId(s.id)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                      selectedSubjectId === s.id
                        ? "bg-[#3D6649] text-white shadow-xs font-semibold scale-102"
                        : "bg-[#FAF7F2] border border-[#E3DBD0] text-[#554D45] hover:bg-[#F2ECE1]"
                    }`}
                  >
                    {s.name}
                  </button>
                ))}
              </div>
            </div>

            {/* 2. Chapter & Topic Selectors */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-0.5">
              <div className="space-y-1.5">
                <label className="text-[11px] font-semibold text-[#5C554E] uppercase tracking-wider">
                  2. Select Chapter
                </label>
                <select
                  value={selectedChapterId || ""}
                  onChange={(e) => handleChapterChange(Number(e.target.value))}
                  className="w-full bg-[#FAF7F2] border border-[#E3DBD0] rounded-xl px-3 py-2 text-xs text-[#272320] focus:outline-none focus:border-[#4B6854]"
                >
                  {chaptersData.map((c: any) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-semibold text-[#5C554E] uppercase tracking-wider">
                  3. Select Topic
                </label>
                <select
                  value={selectedTopicId || ""}
                  onChange={(e) => setSelectedTopicId(Number(e.target.value))}
                  disabled={availableTopics.length === 0}
                  className="w-full bg-[#FAF7F2] border border-[#E3DBD0] rounded-xl px-3 py-2 text-xs text-[#272320] focus:outline-none focus:border-[#4B6854] disabled:opacity-50"
                >
                  {availableTopics.map((t: any) => (
                    <option key={t.id} value={t.id}>
                      {t.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* 3. Difficulty Level Selector: Easy / Medium / Hard */}
            <div className="space-y-2 pt-0.5">
              <label className="text-[11px] font-semibold text-[#5C554E] uppercase tracking-wider">
                4. Select Difficulty (10 Questions Each)
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                {[
                  {
                    level: "Easy" as const,
                    badge: "Foundational",
                    desc: "Direct concept questions, definition checks & core formulas.",
                    color: "border-[#8BA888] bg-[#F2F7F1] text-[#2F5234]",
                  },
                  {
                    level: "Medium" as const,
                    badge: "Standard",
                    desc: "NCERT syllabus-level multi-step reasoning & application.",
                    color: "border-[#D9A066] bg-[#FDF7F0] text-[#8C541D]",
                  },
                  {
                    level: "Hard" as const,
                    badge: "Advanced",
                    desc: "Higher-order thinking, analytical problems & exam synthesis.",
                    color: "border-[#D67B66] bg-[#FDF3F0] text-[#9E3E28]",
                  },
                ].map((d) => (
                  <button
                    key={d.level}
                    type="button"
                    onClick={() => setDifficulty(d.level)}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      difficulty === d.level
                        ? `ring-2 ring-[#292A28] ${d.color} shadow-xs font-medium`
                        : "border-[#EDE7DF] bg-[#FAF7F2] text-[#6B635B] hover:bg-[#F4EFE7]"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-xs md:text-sm">{d.level}</span>
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-white/80 border border-current/20">
                        {d.badge}
                      </span>
                    </div>
                    <p className="text-[11px] leading-relaxed mt-1 opacity-85 line-clamp-2">
                      {d.desc}
                    </p>
                    <span className="inline-block mt-1.5 text-[10px] font-semibold text-[#4B6854]">
                      10 Questions →
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* Launch Practice Button */}
            <div className="pt-1 flex flex-col sm:flex-row items-center gap-3">
              <button
                disabled={!selectedTopicId || loadingQuestions}
                onClick={() => startTopicPractice()}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-[#292A28] hover:bg-[#3E403C] text-white text-xs font-semibold transition-all shadow-xs flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loadingQuestions ? (
                  <>
                    <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <circle cx="12" cy="12" r="10" strokeWidth="3" strokeDasharray="30 60" />
                    </svg>
                    <span>Loading 10 Questions...</span>
                  </>
                ) : (
                  <>
                    <span>Start Practice ({difficulty} · 10 Qs)</span>
                    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M5 12h14" />
                      <path d="m12 5 7 7-7 7" />
                    </svg>
                  </>
                )}
              </button>

              <span className="text-xs text-[#8A8177]">
                Selected: {availableTopics.find((t) => t.id === selectedTopicId)?.name || "Topic"} ({difficulty})
              </span>
            </div>

            {statusMessage && (
              <p className="text-xs text-[#B05844] mt-1">{statusMessage}</p>
            )}
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* GENERIC / MIXED / WEAK / REVISION LAUNCHER */}
        {/* ------------------------------------------------------------- */}
        {practiceMode !== "topic" && questions.length === 0 && !quizFinished && (
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-4 sm:p-5 md:p-6 border border-[#EDE7DF] shadow-xs space-y-4">
            <div>
              <h2 className="font-serif text-lg md:text-xl font-medium text-[#223328] capitalize">
                {practiceMode === "mixed"
                  ? "Mixed Curriculum Practice"
                  : practiceMode === "revision"
                  ? "Revision of Mistakes"
                  : "Targeted Weak Topics"}
              </h2>
              <p className="text-xs text-[#7A7369] mt-0.5">
                {practiceMode === "mixed"
                  ? "A balanced set of 10 questions across your active class subjects."
                  : practiceMode === "revision"
                  ? "Re-practice questions you previously answered incorrectly."
                  : "Target topics where your accuracy is below 70% to boost your growth score."}
              </p>
            </div>

            {/* Choose Difficulty for Mixed/Revision */}
            <div className="flex items-center gap-2">
              <span className="text-xs text-[#6B635B] font-medium">Difficulty:</span>
              {(["Easy", "Medium", "Hard"] as const).map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => setDifficulty(lvl)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    difficulty === lvl
                      ? "bg-[#292A28] text-white"
                      : "bg-[#FAF7F2] border border-[#EDE7DF] text-[#6B635B]"
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>

            <div>
              <button
                onClick={() => startGenericPractice(practiceMode, difficulty)}
                disabled={loadingQuestions}
                className="px-5 py-2.5 bg-[#292A28] hover:bg-[#3E403C] text-white rounded-xl text-xs font-semibold transition-colors flex items-center gap-2"
              >
                {loadingQuestions ? "Loading..." : `Start 10 ${difficulty} Questions →`}
              </button>
            </div>

            {statusMessage && (
              <p className="text-xs text-[#B05844] mt-1">{statusMessage}</p>
            )}
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* ACTIVE PRACTICE QUESTION CARD */}
        {/* ------------------------------------------------------------- */}
        {currentQ && !quizFinished && (
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-4 sm:p-5 md:p-6 border border-[#EDE7DF] shadow-xs space-y-4">
            {/* Header: Progress, Topic, Difficulty & Type Badge */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-[#272320]">
                  Question {currentIndex + 1} of {questions.length}
                </span>
                <div className="flex items-center gap-2">
                  {currentQ.options?.length === 2 && (
                    <span className="font-semibold px-2 py-0.5 rounded-md text-[10px] uppercase tracking-wider bg-[#E5EDE3] text-[#3D6649] border border-[#CDE0CC]">
                      True / False
                    </span>
                  )}
                  {currentQ.prompt?.includes("_____") && (
                    <span className="font-semibold px-2 py-0.5 rounded-md text-[10px] uppercase tracking-wider bg-[#FEF3E8] text-[#A6614E] border border-[#FADCC7]">
                      Fill in the Blank
                    </span>
                  )}
                  <span className="font-medium text-[#6B635B] bg-[#FAF5ED] px-2.5 py-0.5 rounded-full border border-[#EDE7DF] hidden sm:inline-block">
                    {currentQ.topic || "Practice Topic"}
                  </span>
                  <span
                    className={`font-semibold px-2 py-0.5 rounded-full text-[11px] ${
                      currentQ.difficulty === "Easy"
                        ? "bg-[#E5EDE3] text-[#3D6649]"
                        : currentQ.difficulty === "Hard"
                        ? "bg-[#FBECE8] text-[#B05844]"
                        : "bg-[#FEF3E8] text-[#A6614E]"
                    }`}
                  >
                    {currentQ.difficulty || difficulty}
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full h-1.5 bg-[#EDE7DF] rounded-full overflow-hidden">
                <div
                  className="h-full bg-[#3D6649] transition-all duration-300 rounded-full"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>

            {/* Question Prompt */}
            <div className="pt-1 pb-1">
              <p className="font-serif text-base md:text-lg text-[#272320] leading-relaxed">
                {currentQ.prompt}
              </p>
            </div>

            {/* Options List: 2-column grid for True/False, vertical for MCQ / Fill in the blank */}
            <div className={currentQ.options?.length === 2 ? "grid grid-cols-2 gap-3 pt-1" : "space-y-2 pt-1"}>
              {(currentQ.options || []).map((opt: string, k: number) => {
                const isSelected = feedback?.chosenIdx === k;
                const isCorrect = feedback && k === feedback.answer;
                const isWrong = feedback && isSelected && !feedback.correct;

                let optClass = "border-[#E3DBD0] bg-[#FAF7F2] text-[#272320] hover:bg-[#F4EFE7]";
                if (feedback) {
                  if (isCorrect) {
                    optClass = "border-[#3D6649] bg-[#E5EDE3] text-[#1E3A25] font-semibold";
                  } else if (isWrong) {
                    optClass = "border-[#B05844] bg-[#FBECE8] text-[#8C3A27]";
                  } else {
                    optClass = "border-[#E3DBD0] bg-white opacity-50 text-[#8C8377]";
                  }
                }

                return (
                  <button
                    key={k}
                    disabled={!!feedback}
                    onClick={() => handleAnswer(k)}
                    className={`w-full text-left p-3 sm:p-3.5 rounded-xl border text-xs md:text-sm transition-all flex items-center justify-between ${optClass}`}
                  >
                    <span className="pr-2">{opt}</span>
                    {feedback && (
                      <span className="shrink-0 font-bold text-xs">
                        {isCorrect && "✓ Correct"}
                        {isWrong && "✗ Incorrect"}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>

            {/* Explanation & Next Button */}
            {feedback && (
              <div className="p-3.5 sm:p-4 rounded-xl bg-[#FAF5ED] border border-[#E8DFC9] space-y-2.5">
                <div className="flex items-start gap-2">
                  <span
                    className={`font-semibold text-xs px-2 py-0.5 rounded-md ${
                      feedback.correct
                        ? "bg-[#E5EDE3] text-[#3D6649]"
                        : "bg-[#FBECE8] text-[#B05844]"
                    }`}
                  >
                    {feedback.correct ? "Well Done!" : "Explanation"}
                  </span>
                  <p className="text-xs text-[#4A443D] leading-relaxed flex-1">
                    {feedback.explanation}
                  </p>
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-[#E8DFC9]/60">
                  <span className="text-xs text-[#7A7369]">
                    Current Score: {correctCount}/{currentIndex + 1}
                  </span>
                  <button
                    onClick={handleNext}
                    className="px-4 py-1.5 rounded-xl bg-[#292A28] hover:bg-[#3E403C] text-white text-xs font-semibold transition-colors flex items-center gap-1.5 shadow-xs"
                  >
                    <span>{currentIndex < questions.length - 1 ? "Next Question" : "Finish Practice"}</span>
                    <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M5 12h14" />
                      <path d="m12 5 7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* QUIZ FINISHED / SUMMARY CARD */}
        {/* ------------------------------------------------------------- */}
        {quizFinished && (
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-5 sm:p-6 border border-[#EDE7DF] shadow-[0_4px_24px_-4px_rgba(80,60,40,0.04)] text-center space-y-4">
            <div className="w-12 h-12 rounded-full bg-[#E5EDE3] text-[#3D6649] flex items-center justify-center mx-auto shadow-xs">
              <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <path d="m9 12 2 2 4-4" />
              </svg>
            </div>

            <div>
              <h2 className="font-serif text-xl sm:text-2xl font-semibold text-[#272320]">
                Practice Completed!
              </h2>
              <p className="text-xs text-[#7A7369] mt-1">
                You just finished a 10-question practice set on{" "}
                <strong className="text-[#272320]">
                  {availableTopics.find((t) => t.id === selectedTopicId)?.name || "your selected topic"}
                </strong>
                .
              </p>
            </div>

            {/* Score circle / metric */}
            <div className="inline-flex items-baseline gap-2 bg-[#FAF7F2] border border-[#E3DBD0] rounded-xl px-5 py-3">
              <span className="text-3xl font-bold text-[#272320]">
                {correctCount} / {questions.length}
              </span>
              <span className="text-xs font-semibold text-[#4B6854]">
                ({questions.length ? Math.round((correctCount / questions.length) * 100) : 0}% Accuracy)
              </span>
            </div>

            {/* Quick Action Buttons */}
            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button
                onClick={() => startTopicPractice()}
                className="px-5 py-2.5 rounded-xl bg-[#292A28] text-white text-xs font-semibold hover:bg-[#3E403C] transition-colors shadow-xs"
              >
                ↻ Practice Again (Same Topic)
              </button>

              <button
                onClick={() => {
                  const nextDiff =
                    difficulty === "Easy" ? "Medium" : difficulty === "Medium" ? "Hard" : "Easy";
                  startTopicPractice(nextDiff);
                }}
                className="px-5 py-2.5 rounded-xl bg-[#FAF5ED] border border-[#DCD5C9] text-xs font-semibold text-[#4A443D] hover:bg-[#F2ECE1] transition-colors"
              >
                Try {difficulty === "Easy" ? "Medium" : difficulty === "Medium" ? "Hard" : "Easy"} (10 Qs) →
              </button>

              <button
                onClick={() => {
                  setQuestions([]);
                  setQuizFinished(false);
                }}
                className="px-5 py-2.5 rounded-xl bg-white border border-[#EDE7DF] text-xs font-semibold text-[#6B635B] hover:bg-[#FAF7F2] transition-colors"
              >
                Change Topic
              </button>
            </div>
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* OVERALL LEARNING STATS FOOTER */}
        {/* ------------------------------------------------------------- */}
        {stats && (
          <div className="bg-[#FAF7F2] rounded-2xl p-4 border border-[#EDE7DF] flex flex-wrap items-center justify-between gap-4 text-xs text-[#6B635B]">
            <div className="flex items-center gap-4">
              <span>
                Total Attempted: <strong>{stats.attempted}</strong>
              </span>
              <span>
                Overall Accuracy: <strong>{stats.accuracy}%</strong>
              </span>
              <span>
                Streak: <strong>{stats.streak} {stats.streak === 1 ? "day" : "days"}</strong>
              </span>
            </div>

            <Link
              href="/growth"
              className="text-[#3D6649] font-semibold hover:underline flex items-center gap-1"
            >
              <span>View full growth analytics</span>
              <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14" />
                <path d="m12 5 7 7-7 7" />
              </svg>
            </Link>
          </div>
        )}
      </div>
    </Shell>
  );
}
