"use client";
import React, { useState, useEffect, Suspense, useMemo } from "react";
import { useSearchParams } from "next/navigation";
import { Shell, useApi, api } from "@/lib/api";
import { DiagramRenderer } from "./DiagramRenderer";

// Subject icon helper matching Indian CBSE/ICSE curriculum
function getSubjectIcon(name: string) {
  const n = (name || "").toLowerCase();
  if (n.includes("math")) return "📐";
  if (n.includes("physics")) return "⚛️";
  if (n.includes("chem")) return "🧪";
  if (n.includes("bio")) return "🧬";
  if (n.includes("science")) return "🔬";
  if (n.includes("social") || n.includes("sst")) return "🏛️";
  if (n.includes("english")) return "📖";
  if (n.includes("hindi")) return "🇮🇳";
  if (n.includes("sanskrit")) return "🕉️";
  if (n.includes("french")) return "🇫🇷";
  if (n.includes("computer") || n.includes("it")) return "💻";
  if (n.includes("account")) return "📊";
  if (n.includes("business")) return "💼";
  if (n.includes("eco")) return "📈";
  if (n.includes("hist")) return "📜";
  if (n.includes("pol")) return "⚖️";
  if (n.includes("geo")) return "🗺️";
  return "📚";
}

// Sample question generator accurately matching selected subject and chapter
function getSampleQuestionsFor(subjectName: string, chapterName?: string, topics?: any[]) {
  const s = (subjectName || "").toLowerCase();
  const c = (chapterName || "").toLowerCase();

  // 1. Chapter-specific matching for Science
  if (s.includes("science") || s.includes("physics") || s.includes("chem") || s.includes("bio")) {
    if (c.includes("sound")) {
      return [
        "Why can we hear a ringing bell? (5 marks)",
        "Define sound (1 mark)",
        "Draw and label the human ear",
        "How is sound produced by a vibrating tuning fork?",
      ];
    }
    if (c.includes("electri") || c.includes("current")) {
      return [
        "State Ohm's Law and calculate resistance if V=12V and I=3A",
        "Draw a simple circuit diagram with cell, key, bulb, and ammeter",
        "Plot a V-I graph for an ohmic conductor",
        "Define electric current and state its SI unit",
      ];
    }
    if (c.includes("motion") || c.includes("force")) {
      return [
        "Plot a distance-time graph for a car moving at 20 m/s for 5 seconds",
        "State Newton's three laws of motion with everyday examples",
        "Calculate acceleration if a car speeds from 0 to 60 m/s in 5s",
      ];
    }
    if (c.includes("water") || c.includes("natural") || c.includes("environment")) {
      return [
        "Explain the water cycle",
        "Explain the food chain and 10% law of energy transfer",
        "What causes lightning and how can we protect ourselves?",
      ];
    }
    if (c.includes("light") || c.includes("optics")) {
      return [
        "State laws of reflection of light",
        "What is the difference between real and virtual images?",
        "Draw ray diagram for a concave mirror when object is at C",
      ];
    }
    if (c.includes("chemical") || c.includes("reaction") || c.includes("acid")) {
      return [
        "Balance the chemical equation: Fe + H2O -> Fe3O4 + H2",
        "Differentiate between exothermic and endothermic reactions",
        "What happens when zinc granules react with dilute sulphuric acid?",
      ];
    }
    if (c.includes("life") || c.includes("cell") || c.includes("living")) {
      return [
        "Differentiate between plant cell and animal cell",
        "What are the main functions of roots in plants?",
        "Explain the process of photosynthesis and its equation",
      ];
    }
  }

  // 2. Commerce, Accountancy & Economics
  if (s.includes("account") || s.includes("commerce")) {
    return [
      "What is Working Capital and how is it calculated?",
      "Explain the Dual Aspect Concept in accounting with an example",
      "Distinguish between Capital Expenditure and Revenue Expenditure",
      "What are the key objectives of preparing a Cash Flow Statement?",
    ];
  }

  if (s.includes("eco")) {
    return [
      "Explain the Law of Diminishing Marginal Utility with assumptions",
      "What are the determinants of Price Elasticity of Demand?",
      "Distinguish between Microeconomics and Macroeconomics",
      "Explain the primary and secondary functions of money",
    ];
  }

  if (s.includes("business")) {
    return [
      "Explain the 14 principles of management formulated by Henri Fayol",
      "What is the difference between formal and informal organisation?",
      "Explain the importance of planning in business management",
    ];
  }

  // 3. Mathematics
  if (s.includes("math")) {
    if (c.includes("proportion") || c.includes("variation") || c.includes("unitary")) {
      return [
        "12 workers can complete a job in 15 days. How many days will 20 workers take to complete the same job?",
        "If 8 oranges cost ₹40, find the cost of 15 oranges.",
        "A car travels 180 km in 3 hours at uniform speed. How far will it travel in 5 hours?",
      ];
    }
    if (c.includes("rational")) {
      return [
        "Find the additive inverse and multiplicative inverse of -7/12",
        "Write 3 rational numbers between 1/4 and 1/2",
        "Verify closure and commutative properties for addition of 3/5 and -2/7",
      ];
    }
    if (c.includes("linear") || c.includes("equation")) {
      return [
        "Solve: 2x + 7 = 21",
        "Solve: 5x - 3 = 3x + 9",
        "The perimeter of a rectangle is 40 cm. If length is 4 cm more than breadth, find dimensions.",
      ];
    }
    if (c.includes("quadrilateral") || c.includes("polygon")) {
      return [
        "Find the sum of all interior angles of a pentagon",
        "Two adjacent angles of a parallelogram are in the ratio 3:2. Find all angles.",
        "State four properties of a rhombus and compare with a rectangle",
      ];
    }
    if (c.includes("mensuration") || c.includes("trapezium") || c.includes("area")) {
      return [
        "Find the area of a trapezium whose parallel sides are 12 cm and 8 cm and height is 5 cm",
        "Find the total surface area and volume of a cylinder of radius 7 cm and height 10 cm",
      ];
    }
    if (c.includes("interest") || c.includes("commercial")) {
      return [
        "Calculate the compound interest on ₹10000 at 10% per annum for 2 years compounded annually",
        "Find the simple interest on ₹5000 at 8% per annum for 3 years",
      ];
    }
    return [
      "Solve: 2x + 7 = 21",
      "Calculate: (45 * 12) / 6",
      "Find the area and perimeter of rectangle: l=12cm, w=8cm",
    ];
  }

  // 4. Social Science / History / Geography / Civics
  if (s.includes("social") || s.includes("sst") || s.includes("hist") || s.includes("geo") || s.includes("pol")) {
    return [
      "What are the three main tiers of Panchayati Raj in India?",
      "Name the 7 continents and 5 oceans of the world",
      "Explain why the monsoon is crucial for Indian agriculture",
      "Explain the fundamental rights guaranteed by the Indian Constitution",
    ];
  }

  // 5. Languages
  if (s.includes("english")) {
    return [
      "Identify the noun, verb, and adjective in: 'The brave girl ran quickly'",
      "Write 3 synonyms and antonyms for 'courageous'",
      "Explain the central theme of the poem",
    ];
  }

  if (s.includes("hindi")) {
    return [
      "संज्ञा की परिभाषा और तीन उदाहरण लिखिए",
      "निम्नलिखित शब्दों के विलोम शब्द लिखिए: दिन, मित्र, अमृत",
      "मुहावरे का अर्थ और वाक्य प्रयोग कीजिए: 'आँखों का तारा'",
    ];
  }

  return [
    "Explain key concepts from this chapter",
    "List 3 important board examination questions",
  ];
}

function SolveInner() {
  const searchParams = useSearchParams();
  const queryQ = searchParams?.get("q") || "";
  const queryChapter = searchParams?.get("chapter") || "";
  const querySubject = searchParams?.get("subject") || "";

  // Current student profile
  const { d: me } = useApi("/me");

  // Class-wise subjects from API
  const { d: subjects, reload: reloadSubjects } = useApi("/subjects");
  const [curSubject, setCurSubject] = useState<any>(null);

  // Chapters & Topics for selected subject
  const [chaptersData, setChaptersData] = useState<any>(null);
  const [loadingChapters, setLoadingChapters] = useState(false);
  const [selectedChapterId, setSelectedChapterId] = useState<string>("all");
  const [selectedTopic, setSelectedTopic] = useState<any>(null);

  // Question solving state
  const [q, setQ] = useState(queryQ);
  const [marks, setMarks] = useState<number | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  const [extracting, setExtracting] = useState<boolean>(false);
  const [extractStatus, setExtractStatus] = useState<string>("");
  const [r, setR] = useState<any>(null);
  const [e, setE] = useState("");
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState<number>(0);
  const [extra, setExtra] = useState("");

  // Syllabus view toggle
  const [activeTab, setActiveTab] = useState<"solve" | "curriculum">("solve");

  // Select subject automatically, prioritizing querySubject if given
  useEffect(() => {
    if (subjects?.length) {
      if (querySubject) {
        const found = subjects.find(
          (s: any) => s.name.toLowerCase() === querySubject.toLowerCase()
        );
        if (found) {
          pickSubject(found);
          return;
        }
      }
      if (!curSubject) {
        pickSubject(subjects[0]);
      }
    }
  }, [subjects, querySubject]);

  // When chapter data arrives, auto-select matching queryChapter and pre-fill prompt
  useEffect(() => {
    if (chaptersData?.chapters && queryChapter) {
      const match = chaptersData.chapters.find((ch: any) =>
        ch.name.toLowerCase().includes(queryChapter.toLowerCase()) ||
        queryChapter.toLowerCase().includes(ch.name.toLowerCase())
      );
      if (match) {
        setSelectedChapterId(String(match.id));
        if (!q || q === queryQ) {
          setQ(`Explain key concepts and important questions from "${match.name}"`);
        }
      }
    }
  }, [chaptersData, queryChapter]);

  const pickSubject = (sub: any) => {
    setCurSubject(sub);
    setSelectedChapterId("all");
    setSelectedTopic(null);
    setLoadingChapters(true);
    api("/subjects/" + sub.id)
      .then((data) => {
        setChaptersData(data);
      })
      .catch(() => {
        setChaptersData(null);
      })
      .finally(() => {
        setLoadingChapters(false);
      });
  };

  // Find currently selected chapter object
  const activeChapter = useMemo(() => {
    if (!chaptersData?.chapters || selectedChapterId === "all") return null;
    return chaptersData.chapters.find((c: any) => String(c.id) === selectedChapterId);
  }, [chaptersData, selectedChapterId]);

  // Dynamic sample questions for current subject & chapter
  const sampleQuestions = useMemo(() => {
    return getSampleQuestionsFor(curSubject?.name || "Science", activeChapter?.name, activeChapter?.topics);
  }, [curSubject, activeChapter]);

  // Handle File Selection (Image or PDF)
  async function handleFileSelect(selectedFile: File | null) {
    if (!selectedFile) {
      if (filePreview) {
        URL.revokeObjectURL(filePreview);
      }
      setFile(null);
      setFilePreview(null);
      setExtractStatus("");
      setExtracting(false);
      return;
    }

    setFile(selectedFile);
    setE("");

    // Create local image preview
    if (selectedFile.type.startsWith("image/")) {
      const url = URL.createObjectURL(selectedFile);
      setFilePreview(url);
    } else {
      setFilePreview(null);
    }

    setExtracting(true);
    setExtractStatus(`Extracting text from ${selectedFile.name}...`);

    try {
      // 1. If PDF: Call /extract-file endpoint (high-speed pypdf)
      if (selectedFile.type === "application/pdf" || selectedFile.name.toLowerCase().endsWith(".pdf")) {
        const formData = new FormData();
        formData.append("file", selectedFile);
        const res = await api("/extract-file", {
          method: "POST",
          body: formData,
        });
        if (res.extracted && res.extracted.trim()) {
          const cleanText = res.extracted.trim();
          setQ((prev) => (prev.trim() ? `${prev}\n\n${cleanText}` : cleanText));
          setExtractStatus(`✓ Extracted question from PDF (${cleanText.split(/\s+/).length} words)`);
        } else {
          setExtractStatus("✓ PDF attached and ready for solving.");
        }
      } else {
        // 2. If Image: Try backend /extract-file first, then fallback to client Tesseract.js
        let extractedText = "";
        try {
          const formData = new FormData();
          formData.append("file", selectedFile);
          const res = await api("/extract-file", {
            method: "POST",
            body: formData,
          });
          if (res.extracted && res.extracted.trim()) {
            extractedText = res.extracted.trim();
          }
        } catch {
          // Backend fallback
        }

        if (!extractedText) {
          setExtractStatus("Reading question text from image...");
          const Tesseract = await import("tesseract.js");
          const { data } = await Tesseract.recognize(selectedFile, "eng", {
            logger: (m) => {
              if (m.status === "recognizing text" && typeof m.progress === "number") {
                setExtractStatus(`Reading image text... ${Math.round(m.progress * 100)}%`);
              }
            },
          });
          extractedText = (data?.text || "").trim();
        }

        if (extractedText) {
          setQ((prev) => (prev.trim() ? `${prev}\n\n${extractedText}` : extractedText));
          setExtractStatus("✓ Extracted question from image! You can review or edit before solving.");
        } else {
          setExtractStatus("✓ Image attached and ready for solving.");
        }
      }
    } catch (err: any) {
      console.error("File OCR error:", err);
      setExtractStatus("✓ File attached. You can review or type your question and click Solve.");
    } finally {
      setExtracting(false);
    }
  }

  // Solver execution sending full SolveRequest schema
  async function go(textToSolve?: string) {
    let questionVal = (textToSolve || q).trim();

    // Auto-extract from file if question text is not yet entered
    if (!questionVal && file) {
      setLoading(true);
      setE("");
      try {
        if (file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf")) {
          const formData = new FormData();
          formData.append("file", file);
          const res = await api("/extract-file", { method: "POST", body: formData });
          questionVal = (res.extracted || "").trim();
        } else {
          const Tesseract = await import("tesseract.js");
          const { data } = await Tesseract.recognize(file, "eng");
          questionVal = (data?.text || "").trim();
        }
        if (questionVal) {
          setQ(questionVal);
        }
      } catch (err: any) {
        console.error("Auto extraction error:", err);
      }
      if (!questionVal) {
        questionVal = `Please analyze and solve the question from attached file: ${file.name}`;
      }
    }

    if (!questionVal) {
      return;
    }

    setE("");
    setR(null);
    setLoading(true);

    // Resolve chapter name and topics
    let targetChapter = activeChapter?.name || "";
    let chapterTopics: string[] =
      activeChapter?.topics?.map((t: any) => (typeof t === "string" ? t : t.name)) || [];

    // If chapter not explicitly selected (e.g. "all"), intelligently match chapter from question keywords or default
    if (!targetChapter && chaptersData?.chapters?.length) {
      const qLower = questionVal.toLowerCase();
      const matched = chaptersData.chapters.find((c: any) =>
        qLower.includes(c.name.toLowerCase()) ||
        c.topics?.some((t: any) => qLower.includes((typeof t === "string" ? t : t.name).toLowerCase()))
      );
      const chosen = matched || chaptersData.chapters[0];
      targetChapter = chosen.name;
      chapterTopics = chosen.topics?.map((t: any) => (typeof t === "string" ? t : t.name)) || [];
    }

    const payload: any = {
      board: me?.board || "CBSE",
      class_level: me?.class_level || "8",
      stream: me?.stream || (["11", "12"].includes(me?.class_level) ? "Science" : null),
      subject: curSubject?.name || "Science",
      chapter: targetChapter || "General",
      topics: chapterTopics,
      question: questionVal,
    };
    if (marks) {
      payload.marks = Number(marks);
    }

    try {
      const res = await api("/solve", {
        method: "POST",
        body: payload,
      });
      setR(res);
      setOpen(0);
    } catch (x: any) {
      setE(x.message || "Failed to solve question");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (queryQ) {
      setQ(queryQ);
      go(queryQ);
    }
  }, [queryQ]);


  const save = () =>
    api("/notes", {
      method: "POST",
      body: {
        kind: "saved",
        title: (r?.extracted || "Solution").slice(0, 60),
        body: (r?.direct_answer ? `Direct Answer:\n${r.direct_answer}\n\n` : "") +
              (r?.steps || []).map((s: any) => s[0] + ": " + s[1]).join("\n\n"),
      },
    }).then(() => setExtra("Saved to Study Notes."));

  return (
    <Shell
      title="Solve"
      sub="Class-wise curriculum subjects, chapter syllabus & verified question solver."
    >
      <div className="w-full space-y-6">

        {/* 1. CLASS-WISE SUBJECTS SELECTOR */}
        <div className="bg-white/95 rounded-2xl md:rounded-3xl p-5 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)]">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span className="text-xs font-semibold uppercase tracking-wider text-[#6B6359]">
                Your Class Subjects
              </span>
            </div>
            <span className="text-xs text-[#8C8377]">
              {subjects?.length || 0} subjects enrolled
            </span>
          </div>

          {/* Horizontal scrollable subject pills */}
          <div className="flex items-center gap-2.5 overflow-x-auto pb-1 scrollbar-none">
            {subjects?.map((sub: any) => {
              const active = curSubject?.id === sub.id;
              const icon = getSubjectIcon(sub.name);
              return (
                <button
                  key={sub.id}
                  onClick={() => pickSubject(sub)}
                  className={`flex items-center gap-2.5 px-4 py-2.5 rounded-2xl text-xs font-medium transition-all shrink-0 cursor-pointer border ${
                    active
                      ? "bg-[#DFE7DD] border-[#3D6649] text-[#25382B] shadow-xs font-semibold ring-1 ring-[#3D6649]/20"
                      : "bg-[#FAF8F5] border-[#E5DFD5] text-[#554E46] hover:bg-white hover:border-[#C5BCB0]"
                  }`}
                >
                  <span className="text-base">{icon}</span>
                  <span>{sub.name}</span>
                  {active && (
                    <span className="w-1.5 h-1.5 rounded-full bg-[#3D6649] ml-0.5"></span>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* 2. CHAPTER SELECTION OPTION & SYLLABUS CONTROLS */}
        <div className="bg-white/95 rounded-2xl md:rounded-3xl p-5 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)]">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            
            {/* Chapter Selection Dropdown */}
            <div className="flex-1">
              <label className="block text-xs font-medium text-[#5A504A] mb-1.5 flex items-center gap-1.5">
                <span>Select Chapter for <strong>{curSubject?.name || "Subject"}</strong>:</span>
                {loadingChapters && (
                  <span className="text-[10px] text-[#9E5646] animate-pulse">Loading chapters...</span>
                )}
              </label>

              <div className="relative">
                <select
                  value={selectedChapterId}
                  onChange={(e) => {
                    setSelectedChapterId(e.target.value);
                    setSelectedTopic(null);
                  }}
                  className="w-full px-4 py-2.5 pr-10 rounded-xl border border-[#DCD5C9] bg-[#FAF8F5] text-xs font-medium text-[#2D2622] focus:outline-none focus:ring-2 focus:ring-[#5C463D]/20 focus:border-[#5C463D] transition-all cursor-pointer appearance-none"
                >
                  <option value="all">
                    📚 All Chapters ({chaptersData?.chapters?.length || 0} chapters available)
                  </option>
                  {chaptersData?.chapters?.map((chap: any, idx: number) => (
                    <option key={chap.id} value={String(chap.id)}>
                      Chapter {idx + 1}: {chap.name} ({chap.topics?.length || 0} topics)
                    </option>
                  ))}
                </select>

                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[#7A7268]">
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="m6 9 6 6 6-6" />
                  </svg>
                </div>
              </div>
            </div>

            {/* View Mode Toggle: Solver vs Full Curriculum Syllabus */}
            <div className="flex items-center gap-1 bg-[#F3EFE9] p-1 rounded-xl self-start sm:self-end">
              <button
                type="button"
                onClick={() => setActiveTab("solve")}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeTab === "solve"
                    ? "bg-white text-[#29221C] shadow-xs"
                    : "text-[#6B6359] hover:text-[#25221E]"
                }`}
              >
                ✏️ Solver Workspace
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("curriculum")}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeTab === "curriculum"
                    ? "bg-white text-[#29221C] shadow-xs"
                    : "text-[#6B6359] hover:text-[#25221E]"
                }`}
              >
                📖 Syllabus &amp; Chapters ({chaptersData?.chapters?.length || 0})
              </button>
            </div>
          </div>

          {/* Active Chapter Topics Bar */}
          {activeChapter && (
            <div className="mt-4 pt-4 border-t border-[#EFEAE2] flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-medium text-[#7A7268]">
                Chapter Topics:
              </span>
              {activeChapter.topics?.map((top: any) => {
                const isSelected = selectedTopic?.id === top.id;
                return (
                  <button
                    key={top.id}
                    onClick={() => {
                      setSelectedTopic(top);
                      const sample = `Explain key concepts of "${top.name}" in ${curSubject?.name}`;
                      setQ(sample);
                      setActiveTab("solve");
                    }}
                    className={`text-xs px-2.5 py-1 rounded-lg transition-colors flex items-center gap-1 ${
                      isSelected
                        ? "bg-[#DFE7DD] text-[#25382B] font-semibold border border-[#3D6649]/30"
                        : "bg-[#EFECE6] hover:bg-[#E2DDD3] text-[#3D352E]"
                    }`}
                    title="Click to solve question for this topic"
                  >
                    <span>• {top.name}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* 3. SOLVER WORKSPACE TAB */}
        {activeTab === "solve" && (
          <div className="space-y-6">
            {/* Question Input Card */}
            <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] space-y-4">
              
              {/* Header with Scope Badge */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-serif font-medium text-[#29221C]">
                    Your Question
                  </span>
                  <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#E5EDE3] text-[#3D6649] font-medium">
                    {curSubject?.name || "Mathematics"}
                    {activeChapter ? ` · ${activeChapter.name}` : ""}
                  </span>
                </div>
                <span className="text-xs text-[#8C8377]">
                  Supports equations, algebra, word problems &amp; formulas
                </span>
              </div>

              {/* Textarea */}
              <textarea
                className="w-full h-28 px-4 py-3 rounded-2xl border border-[#DCD3C7] bg-[#FFFDF9] text-[#2D2622] text-sm placeholder-[#9C9288] focus:outline-none focus:ring-2 focus:ring-[#684D43]/30 focus:border-[#684D43] transition-all resize-none"
                placeholder="e.g. How is sound produced? or Solve 3x + 15 = 42"
                value={q}
                onChange={(e) => setQ(e.target.value)}
              />

              {/* Marks / Depth Selection (Optional) */}
              <div className="flex flex-wrap items-center gap-2 pt-1 pb-1">
                <span className="text-[11px] font-medium text-[#7D766E] flex items-center gap-1">
                  <span>Marks (Answer Length):</span>
                </span>
                {[
                  { label: "Auto Depth", val: null },
                  { label: "1 Mark (1 line)", val: 1 },
                  { label: "2 Marks (2 pts)", val: 2 },
                  { label: "3 Marks (3 pts)", val: 3 },
                  { label: "5 Marks (Detailed)", val: 5 },
                ].map((opt) => (
                  <button
                    key={String(opt.val)}
                    type="button"
                    onClick={() => setMarks(opt.val)}
                    className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all cursor-pointer ${
                      marks === opt.val
                        ? "bg-[#5C463D] text-white shadow-xs font-semibold"
                        : "bg-[#FAF7F2] text-[#554E46] border border-[#E5DFD5] hover:bg-[#EFECE4]"
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
                <div className="flex items-center gap-1.5 ml-auto">
                  <span className="text-[11px] text-[#8C8377]">Custom marks:</span>
                  <input
                    type="number"
                    min={1}
                    max={10}
                    placeholder="1-10"
                    value={marks ?? ""}
                    onChange={(ev) => {
                      const v = ev.target.value ? parseInt(ev.target.value) : null;
                      setMarks(v && v >= 1 && v <= 10 ? v : null);
                    }}
                    className="w-14 px-2 py-1 rounded-lg border border-[#DCD3C7] bg-[#FFFDF9] text-xs text-center font-medium focus:outline-none focus:ring-1 focus:ring-[#5C463D]"
                  />
                </div>
              </div>

              {/* Quick Sample Questions from Current Subject / Chapter */}
              <div>
                <span className="text-[11px] font-medium text-[#7D766E] block mb-1.5">
                  Sample questions for {curSubject?.name} {activeChapter ? `(${activeChapter.name})` : ""}:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {sampleQuestions.map((sample) => (
                    <button
                      key={sample}
                      type="button"
                      onClick={() => {
                        setQ(sample);
                        go(sample);
                      }}
                      className="text-xs bg-[#FAF7F2] hover:bg-[#EFECE4] text-[#4A433B] border border-[#E5DFD5] px-3 py-1 rounded-xl transition-colors text-left truncate max-w-full"
                    >
                      ⚡ {sample}
                    </button>
                  ))}
                </div>
              </div>

              {/* Attachment Preview Card */}
              {file && (
                <div className="p-3.5 rounded-2xl bg-[#F6F3EC] border border-[#E3DACB] flex items-center justify-between gap-3 animate-in fade-in duration-150">
                  <div className="flex items-center gap-3 overflow-hidden">
                    {filePreview ? (
                      <img
                        src={filePreview}
                        alt="Preview"
                        className="w-12 h-12 object-cover rounded-xl border border-[#D5CCC0] shrink-0 shadow-2xs"
                      />
                    ) : (
                      <div className="w-12 h-12 rounded-xl bg-[#EBE3D5] border border-[#DDD3C4] text-[#5C463D] flex items-center justify-center text-xl shrink-0">
                        📄
                      </div>
                    )}
                    <div className="overflow-hidden space-y-0.5">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-semibold text-xs text-[#29221C] truncate max-w-xs sm:max-w-md">
                          {file.name}
                        </span>
                        <span className="text-[10px] text-[#7A7369] px-2 py-0.5 rounded-full bg-white border border-[#E0D8CC]">
                          {(file.size / 1024).toFixed(1)} KB
                        </span>
                      </div>
                      <div className="text-[11px] text-[#5A5046] flex items-center gap-1.5">
                        {extracting ? (
                          <>
                            <svg className="animate-spin h-3 w-3 text-[#5C463D] shrink-0" viewBox="0 0 24 24" fill="none">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                            </svg>
                            <span className="text-[#8B5E3C] font-medium">{extractStatus || "Reading text from attachment..."}</span>
                          </>
                        ) : (
                          <span className="text-[#3D6649] font-medium">{extractStatus || "✓ Attachment ready for solver"}</span>
                        )}
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => handleFileSelect(null)}
                    className="text-xs text-[#8C8377] hover:text-[#9E5646] p-2 hover:bg-[#EBE4D8] rounded-xl transition-colors shrink-0"
                    title="Remove attachment"
                  >
                    ✕
                  </button>
                </div>
              )}

              {/* Bottom Controls */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-2 border-t border-[#F2EDE5]">
                <div className="flex items-center gap-2">
                  <label className="cursor-pointer text-xs font-medium px-4 py-2 rounded-xl border border-[#DCD5C9] bg-[#F7F4EE] hover:bg-[#EFECE4] text-[#4A433B] transition-colors flex items-center gap-2">
                    <svg className="w-4 h-4 text-[#7A7268]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                      <circle cx="8.5" cy="8.5" r="1.5" />
                      <polyline points="21 15 16 10 5 21" />
                    </svg>
                    <span>{file ? "Change Attached File" : "Attach Image or PDF"}</span>
                    <input
                      type="file"
                      accept="image/*,.pdf"
                      className="hidden"
                      onChange={(e) => handleFileSelect(e.target.files?.[0] || null)}
                    />
                  </label>
                  {file && (
                    <button
                      type="button"
                      onClick={() => handleFileSelect(null)}
                      className="text-xs text-[#9E5646] hover:underline"
                    >
                      Clear
                    </button>
                  )}
                </div>

                <button
                  className="px-6 py-2.5 rounded-xl bg-[#5C463D] hover:bg-[#483730] text-[#F9F6F0] font-medium text-xs shadow-xs transition-all flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
                  onClick={() => go()}
                  disabled={(!q && !file) || loading}
                >
                  {loading && (
                    <svg className="animate-spin h-3.5 w-3.5 text-white" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                  )}
                  <span>{loading ? "Solving & Verifying..." : "Solve Question"}</span>
                </button>
              </div>

              {/* Prominent Backend Error Message Banner */}
              {e && (
                <div className="p-4 rounded-2xl text-xs bg-[#FDF2F0] border border-[#F5C6CB] text-[#9B3636] flex items-start gap-3 shadow-xs animate-in fade-in duration-150">
                  <span className="text-base shrink-0 mt-0.5">⚠️</span>
                  <div className="space-y-1 overflow-hidden">
                    <div className="font-semibold text-[#8B2626] flex items-center gap-2">
                      <span>Backend Message:</span>
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#FCE8E6] text-[#A82B2B]">Error Details</span>
                    </div>
                    <div className="font-mono text-[11px] whitespace-pre-wrap leading-relaxed break-words">{e}</div>
                  </div>
                </div>
              )}
            </div>

            {/* Unsolved Warning / OCR Result */}
            {r && !r.solved && (
              <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)]">
                <p className="text-xs text-[#7A7369]">Extracted: {r.extracted}</p>
                <p className="mt-2 text-sm text-[#9B6256]">{r.message}</p>
              </div>
            )}

            {/* Solved Result Card - Structured Solver Pipeline Output */}
            {r && (r.solved || r.final_answer) && (
              <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] space-y-4 animate-in fade-in duration-200">
                {/* Header with Heading & Badges */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-serif font-medium text-[#29221C]">
                      Solution:
                    </span>
                    <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#E5EDE3] text-[#3D6649] font-medium">
                      {r.subject || "Academic Solution"} {r.topic || r.topic_matched ? `· ${r.topic || r.topic_matched}` : ""}
                    </span>
                    {r.confidence && (
                      <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-md ${
                        r.confidence === "high" ? "bg-emerald-100 text-emerald-800" :
                        r.confidence === "medium" ? "bg-amber-100 text-amber-800" : "bg-red-100 text-red-800"
                      }`}>
                        {r.confidence} confidence
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-2 flex-wrap">
                    {/* Verification badge only when self-check is complete, in_scope, factually_correct and confidence is not low */}
                    {r.verification_badge && r.confidence !== "low" && (
                      <span className="text-xs text-[#2E6038] font-medium bg-[#E2EDE3] border border-[#C5DEC7] px-2.5 py-0.5 rounded-full flex items-center gap-1 shadow-2xs">
                        <span className="font-bold">✓</span>
                        <span>Concept checked</span>
                      </span>
                    )}
                    {r.used_context && (
                      <span className="text-xs text-[#405445] font-medium bg-[#EEF4ED] border border-[#D5E2D4] px-2.5 py-0.5 rounded-full">
                        Textbook verified
                      </span>
                    )}
                  </div>
                </div>

                {/* Definition (if provided by solver pipeline) */}
                {r.definition && (
                  <div className="p-3.5 rounded-xl bg-[#F6F3ED] border border-[#E4DDD0] text-sm text-[#2D2622]">
                    <span className="font-semibold text-[#5C463D] block mb-1">Definition & Core Concept:</span>
                    <p className="leading-relaxed">{r.definition}</p>
                  </div>
                )}

                {/* Formula Box (if provided) */}
                {r.formula && (
                  <div className="p-3.5 rounded-xl bg-[#201D1A] text-[#F3EFEA] font-mono text-xs md:text-sm">
                    <span className="text-[#A3B899] text-xs font-sans block mb-1">Mathematical Formula:</span>
                    <div className="leading-relaxed">{r.formula}</div>
                  </div>
                )}

                {/* Calculation / Working Steps (if provided) */}
                {r.working && r.working.length > 0 && (
                  <div className="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EBE4D8] space-y-1 font-mono text-xs">
                    <span className="font-sans font-semibold text-[#5C463D] block mb-1">Numerical Steps & Substitution:</span>
                    {r.working.map((w: string, idx: number) => (
                      <div key={idx} className="text-[#38312A]">{w}</div>
                    ))}
                  </div>
                )}

                {/* Structured Explanation Points with Meaningful Step Titles */}
                {r.steps && r.steps.length > 0 ? (
                  <div className="space-y-3">
                    <span className="font-semibold text-[#29221C] text-sm block">Key Points:</span>
                    <div className="space-y-2.5">
                      {r.steps
                        .filter(([title]: any) => !/^(answer|final answer)$/i.test((title || "").trim()))
                        .map(([title, content]: any, i: number) => (
                          <div key={i} className="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EDE7DF] space-y-1">
                            <div className="flex items-center gap-2">
                              <span className="w-5 h-5 rounded-full bg-[#E5EDE3] text-[#3D6649] flex items-center justify-center text-xs font-bold shrink-0">
                                {i + 1}
                              </span>
                              <h5 className="font-semibold text-[#29221C] text-sm">
                                {title}
                              </h5>
                            </div>
                            <div className="text-[#3E3831] text-sm whitespace-pre-wrap leading-relaxed pl-7">
                              {content}
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>
                ) : r.explanation && Array.isArray(r.explanation) && r.explanation.length > 0 ? (
                  <div className="space-y-2">
                    <span className="font-semibold text-[#29221C] text-sm block">Explanation:</span>
                    <ul className="space-y-2 list-none text-sm text-[#3E3831] leading-relaxed">
                      {r.explanation.map((pt: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2.5">
                          <span className="w-5 h-5 rounded-full bg-[#E5EDE3] text-[#3D6649] flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">
                            {idx + 1}
                          </span>
                          <span className="flex-1">{pt}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}

                {/* Diagram & Visual Representation Section */}
                {r.diagram && r.diagram.type !== "none" && (
                  <DiagramRenderer diagram={r.diagram} />
                )}

                {/* Clear Final Answer section - Shown Once */}
                {(() => {
                  const ansText = r.final_answer || r.direct_answer;
                  if (!ansText) return null;
                  return (
                    <div className="p-4 rounded-xl bg-[#F6F2EC] border border-[#DDD3C7] text-sm md:text-[15px] font-medium text-[#29221C] flex items-baseline gap-2.5 shadow-2xs">
                      <span className="font-semibold text-[#6E4839] shrink-0">Final Answer:</span>
                      <span className="whitespace-pre-wrap leading-relaxed text-[#231E1B]">{ansText.replace(/^Answer:\s*/i, "")}</span>
                    </div>
                  );
                })()}

                {/* Bottom Controls / Actions (Unchanged functionality) */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-3 border-t border-[#F2EDE5]">
                  <div className="flex gap-2 flex-wrap text-xs">
                    <button
                      className="px-3.5 py-1.5 rounded-lg border border-[#DCD5C9] bg-white text-[#4A433B] hover:bg-[#FAF7F2] font-medium transition-colors cursor-pointer"
                      onClick={() => {
                        const hintStep = r.steps?.find((s: any) => /rule|concept|given|meaning|approach/i.test(s[0])) || r.steps?.[0];
                        setExtra("💡 Hint: " + (hintStep ? `${hintStep[0]} — ${hintStep[1]}` : (r.direct_answer || "")));
                      }}
                    >
                      💡 Hint
                    </button>
                    <button
                      className="px-3.5 py-1.5 rounded-lg border border-[#DCD5C9] bg-white text-[#4A433B] hover:bg-[#FAF7F2] font-medium transition-colors cursor-pointer"
                      onClick={() => {
                        const ansStep = r.steps?.find((s: any) => /answer/i.test(s[0])) || r.steps?.[r.steps?.length - 1];
                        setExtra("✨ Simple Explanation: " + (ansStep ? ansStep[1] : (r.direct_answer || "")));
                      }}
                    >
                      ✨ Simple Explanation
                    </button>
                    <button
                      className="px-3.5 py-1.5 rounded-lg border border-[#DCD5C9] bg-white text-[#4A433B] hover:bg-[#FAF7F2] font-medium transition-colors cursor-pointer"
                      onClick={() =>
                        setExtra(
                          (r.direct_answer ? `Answer:\n${r.direct_answer}\n\n` : "") +
                          (r.steps || []).map((s: any) => `${s[0]}:\n${s[1]}`).join("\n\n")
                        )
                      }
                    >
                      📜 Detailed Explanation
                    </button>
                    <button
                      className="px-3.5 py-1.5 rounded-lg border border-[#DCD5C9] bg-white text-[#4A433B] hover:bg-[#FAF7F2] font-medium transition-colors cursor-pointer"
                      onClick={() => {
                        const isMath = /math|equation|algebra|profit|arithmetic/i.test(r.subject || "") || /math|algebra|calculation|word problem/i.test(r.qtype || "");
                        const isLang = /english|hindi|grammar|vocab/i.test(r.subject || "") || /synonym|antonym|grammar|literature/i.test(r.qtype || "");
                        if (isMath) {
                          setExtra("🔄 Alternative Method: Verify correctness by subtracting one part from the total, or cross-checking with a number line.");
                        } else if (isLang) {
                          setExtra("🔄 Alternative Method: Test each term in distinct sample sentences or substitute into the target sentence to test contextual tone.");
                        } else {
                          setExtra("🔄 Alternative Method: Reason backwards from empirical observations to first principles to cross-validate the conclusion.");
                        }
                      }}
                    >
                      🔄 Another Method
                    </button>
                  </div>

                  <button
                    className="px-4 py-1.5 rounded-lg bg-[#5C463D] text-[#FAF7F2] hover:bg-[#483730] font-medium text-xs transition-colors cursor-pointer sm:ml-auto"
                    onClick={save}
                  >
                    💾 Save to Notes
                  </button>
                </div>

                {extra && (
                  <div className="p-3.5 rounded-xl bg-[#FAF7F2] border border-[#EBE4D8] text-xs font-mono text-[#38312A] whitespace-pre-wrap animate-in fade-in duration-150">
                    {extra}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* 4. FULL CURRICULUM SYLLABUS & CHAPTERS VIEW (FROM "MY SUBJECTS") */}
        {activeTab === "curriculum" && (
          <div className="bg-white/95 rounded-2xl md:rounded-3xl p-6 border border-[#EDE7DF] shadow-[0_4px_20px_-4px_rgba(80,60,40,0.04)] space-y-6">
            <div className="flex items-center justify-between border-b border-[#F0EBE3] pb-4">
              <div>
                <h3 className="font-serif text-xl font-medium text-[#29221C] flex items-center gap-2">
                  <span>{getSubjectIcon(curSubject?.name)}</span>
                  <span>{curSubject?.name} — Complete Syllabus</span>
                </h3>
                <p className="text-xs text-[#7A7369] mt-0.5">
                  Browse chapters, examine topics, and click any topic to immediately solve related problems.
                </p>
              </div>

              <span className="text-xs bg-[#E8EFE8] text-[#346638] px-3 py-1 rounded-full font-medium">
                {chaptersData?.chapters?.length || 0} Chapters
              </span>
            </div>

            {loadingChapters ? (
              <div className="p-8 text-center text-xs text-[#7A7369] animate-pulse">
                Loading syllabus chapters...
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {chaptersData?.chapters?.map((chap: any, index: number) => {
                  const isSelected = selectedChapterId === String(chap.id);
                  return (
                    <div
                      key={chap.id}
                      className={`p-4 rounded-2xl border transition-all ${
                        isSelected
                          ? "bg-[#FAF5EF] border-[#5C463D] shadow-xs ring-1 ring-[#5C463D]/20"
                          : "bg-[#FAF8F5] border-[#E8DFD3] hover:bg-white hover:border-[#C4B7A7]"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <span className="text-[11px] font-semibold text-[#8C8377] uppercase tracking-wide">
                            Chapter {index + 1}
                          </span>
                          <h4 className="font-serif text-sm font-medium text-[#2E2420] mt-0.5">
                            {chap.name}
                          </h4>
                        </div>

                        <button
                          type="button"
                          onClick={() => {
                            setSelectedChapterId(String(chap.id));
                            setActiveTab("solve");
                          }}
                          className="px-2.5 py-1 rounded-lg bg-[#5C463D] text-white hover:bg-[#483730] text-[11px] font-medium transition-all shrink-0 cursor-pointer"
                        >
                          Solve ➔
                        </button>
                      </div>

                      {/* Topics */}
                      <div className="mt-3 pt-2.5 border-t border-[#EFEAE2]">
                        <span className="text-[10px] uppercase font-semibold text-[#8C8377] block mb-1">
                          Topics in this chapter:
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {chap.topics?.map((top: any) => (
                            <button
                              key={top.id}
                              type="button"
                              onClick={() => {
                                setSelectedChapterId(String(chap.id));
                                setQ(`Explain and solve practice questions for "${top.name}" in Chapter ${index + 1}`);
                                setActiveTab("solve");
                              }}
                              className="text-[11px] bg-white border border-[#E2D8CC] text-[#4A433B] hover:border-[#5C463D] px-2 py-0.5 rounded-md transition-colors text-left"
                              title="Click to formulate question for this topic"
                            >
                              {top.name}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

      </div>
    </Shell>
  );
}

export default function SolvePage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-xs text-[#7A7369]">Loading solver...</div>}>
      <SolveInner />
    </Suspense>
  );
}
