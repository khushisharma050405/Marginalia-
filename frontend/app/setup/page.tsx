"use client";
import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

const BOARDS = [
  { id: "CBSE", name: "CBSE", desc: "Central Board of Secondary Education" },
  { id: "ICSE", name: "ICSE", desc: "Council for the Indian School Certificate" }
];

const FOUNDATION_CLASSES = ["Nursery", "LKG", "UKG"];
const PRIMARY_CLASSES = ["1", "2", "3", "4", "5"];
const SECONDARY_CLASSES = ["6", "7", "8", "9", "10"];
const SENIOR_CLASSES = ["11", "12"];

const STREAMS = [
  { id: "Science", name: "Science", desc: "Physics, Chemistry, Maths / Biology" },
  { id: "Commerce", name: "Commerce", desc: "Accountancy, Business Studies, Economics" },
  { id: "Humanities", name: "Humanities", desc: "History, Political Science, Geography" }
];

// Official CBSE & ICSE Subjects matching current NCERT / CISCE curriculum
function getSubjectsForClass(classLevel: string, stream?: string) {
  if (!classLevel) return [];
  if (FOUNDATION_CLASSES.includes(classLevel)) {
    return [
      { name: "Mathematics", icon: "🔢", desc: "Counting, number patterns, shapes & early arithmetic" },
      { name: "Environmental Awareness", icon: "🌿", desc: "Nature awareness, senses, plants & animals" },
      { name: "English", icon: "🔤", desc: "Phonics, alphabet, vocabulary & storytelling" },
      { name: "Hindi", icon: "🇮🇳", desc: "वर्णमाला, स्वर, व्यंजन व बालगीत" }
    ];
  }
  const n = parseInt(classLevel);
  if (n <= 5) {
    // Primary School (Classes 1 - 5, e.g. Class 3)
    return [
      { name: "Mathematics", icon: "📐", desc: "Numbers, addition, subtraction, multiplication, measurement & shapes" },
      { name: "Science", icon: "🔬", desc: "Plants, animals, water cycle, food, habitats & environmental care" },
      { name: "Social Science (SST)", icon: "🏛️", desc: "Our country India, maps, continents, transport, helpers & heritage" },
      { name: "English", icon: "📖", desc: "Prose, poetry, nouns, pronouns, verbs, tenses & creative writing" },
      { name: "Hindi", icon: "🇮🇳", desc: "हिन्दी: पाठ, कहानियाँ, संज्ञा, सर्वनाम, विलोम, पर्यायवाची व मुहावरे" }
    ];
  }
  if (n >= 6 && n <= 8) {
    // Middle School (Classes 6 - 8) - includes Sanskrit & French as 3rd Languages
    return [
      { name: "Mathematics", icon: "📐", desc: "Integers, fractions, decimals, simple equations, geometry & mensuration" },
      { name: "Science", icon: "🔬", desc: "Physics (motion, light, electricity), Chemistry (matter, acids), Biology (food, plants, cells)" },
      { name: "Social Science (SST)", icon: "🏛️", desc: "History (Our Pasts), Geography (Earth & Resources), Civics (Social & Political Life)" },
      { name: "English", icon: "📖", desc: "Honeysuckle / Honeycomb / Honeydew, grammar, voice, speech & composition" },
      { name: "Hindi", icon: "🇮🇳", desc: "वसंत: पाठ, कविताएँ, वर्ण-विचार, संधि, समास, मुहावरे व लोकोक्तियाँ" },
      { name: "Sanskrit", icon: "🕉️", desc: "संस्कृतम् (रुचिरा): शब्दपरिचयः, सुभाषितानि, धातु रूप, शब्द रूप व अव्यय (3rd Language)" },
      { name: "French", icon: "🇫🇷", desc: "Français: Salutations, les articles, les verbes en -ER, être, avoir, la météo (3rd Language)" }
    ];
  }
  if (n >= 9 && n <= 10) {
    // Secondary School (Classes 9 - 10)
    return [
      { name: "Mathematics", icon: "📐", desc: "Real numbers, polynomials, linear equations, quadratics, trigonometry, circles, stats" },
      { name: "Science", icon: "🔬", desc: "Physics (optics, electricity, magnetic), Chemistry (reactions, carbon), Biology (life processes)" },
      { name: "Social Science (SST)", icon: "🏛️", desc: "History (Nationalism), Geography (Resources & Agriculture), Civics (Power Sharing), Economics" },
      { name: "English", icon: "📖", desc: "First Flight & Footprints / Beehive & Moments, formal letters, grammar & analytical writing" },
      { name: "Hindi", icon: "🇮🇳", desc: "क्षितिज, कृतिका, स्पर्श, संचयन: वाक्य रूपांतर, पदबंध, समास, मुहावरे" },
      { name: "Sanskrit", icon: "🕉️", desc: "शेमुषी: पर्यावरणम्, सुभाषितानि, सन्धि, प्रत्यय, वाच्यपरिवर्तनम्" },
      { name: "French", icon: "🇫🇷", desc: "Entre Jeunes: Le passé composé, l'imparfait, les pronoms relatifs, le subjonctif" },
      { name: "Information Technology", icon: "💻", desc: "Digital documentation, electronic spreadsheets, RDBMS (SQL) & web security" }
    ];
  }
  if (stream === "Science") {
    return [
      { name: "Physics", icon: "⚛️", desc: "Mechanics, thermodynamics, electrostatics, optics, magnetism & modern physics" },
      { name: "Chemistry", icon: "🧪", desc: "Atomic structure, bonding, thermodynamics, solutions, organic reaction mechanisms" },
      { name: "Mathematics", icon: "📐", desc: "Calculus (differentiation & integration), vectors, 3D geometry, matrices & probability" },
      { name: "Biology", icon: "🧬", desc: "Genetics, molecular biology, biotechnology, human physiology & ecology" },
      { name: "English Core", icon: "📖", desc: "Hornbill, Flamingo, Vistas, note making, discursive essays & formal letters" },
      { name: "Computer Science", icon: "💻", desc: "Python computational thinking, data structures (stacks/queues), computer networks & SQL" }
    ];
  }
  if (stream === "Commerce") {
    return [
      { name: "Accountancy", icon: "📊", desc: "Partnership accounting, company share capital, debentures & cash flow statements" },
      { name: "Business Studies", icon: "💼", desc: "Fayol's principles, planning, staffing, directing, marketing mix & financial management" },
      { name: "Economics", icon: "📈", desc: "Microeconomics (demand/cost), Macroeconomics (national income, money) & Indian economy" },
      { name: "Mathematics", icon: "📐", desc: "Applied mathematics, financial mathematics, linear programming & calculus" },
      { name: "English Core", icon: "📖", desc: "Business communication, official letters, article writing & literary analysis" }
    ];
  }
  if (stream === "Humanities") {
    return [
      { name: "History", icon: "📜", desc: "Themes in Indian History (Ancient, Medieval, Modern) & World Civilisations" },
      { name: "Political Science", icon: "⚖️", desc: "Indian Constitution at Work, democratic institutions & Contemporary Global Politics" },
      { name: "Geography", icon: "🗺️", desc: "Fundamentals of Physical Geography, India: Physical Environment, Human settlements" },
      { name: "Economics", icon: "📈", desc: "Development economics, macroeconomic policies & current challenges of Indian economy" },
      { name: "English Core", icon: "📖", desc: "Critical literary analysis, speeches, rhetorical essays & editorial writing" }
    ];
  }
  return [];
}

export default function Setup() {
  const r = useRouter();
  const [b, setB] = useState("CBSE");
  const [c, setC] = useState("");
  const [s, setS] = useState("");
  const [e, setE] = useState("");
  const [saving, setSaving] = useState(false);

  const hi = c === "11" || c === "12";
  const subjects = useMemo(() => getSubjectsForClass(c, hi ? s : undefined), [c, s, hi]);

  async function save() {
    if (!b || !c) return;
    if (hi && !s) return;
    setSaving(true);
    setE("");
    try {
      await api("/me/profile", {
        method: "PUT",
        body: { board: b, class_level: c, stream: hi ? s : null }
      });
      // Direct navigation to the main dashboard
      r.push("/home");
    } catch (x: any) {
      setE(x.message || "Failed to update profile");
      setSaving(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#F9F6F0] py-12 px-4 sm:px-6 lg:px-8 flex flex-col justify-center items-center">
      <div className="w-full max-w-3xl bg-white rounded-2xl border border-[#E8DFD3] shadow-sm p-6 sm:p-10 space-y-8">
        
        {/* Header */}
        <div className="flex items-start justify-between border-b border-[#EFEAE2] pb-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 rounded-full bg-[#684D43]/10 flex items-center justify-center text-[#684D43]">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
                  <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12" />
                </svg>
              </div>
              <span className="font-serif text-xl text-[#3A2E2B] font-medium">Marginalia</span>
            </div>
            <h1 className="font-serif text-3xl text-[#3A2E2B]">Set up your learning space</h1>
            <p className="text-sm text-[#6D635B] mt-1">
              Select your academic curriculum to personalize your chapters, question bank, and study tools.
            </p>
          </div>
        </div>

        {/* 1. Board Selection */}
        <div className="space-y-3">
          <label className="block text-xs font-semibold uppercase tracking-wider text-[#73675F]">
            1. Education Board
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {BOARDS.map((board) => {
              const active = b === board.id;
              return (
                <button
                  key={board.id}
                  type="button"
                  onClick={() => setB(board.id)}
                  className={`text-left p-4 rounded-xl border transition-all cursor-pointer ${
                    active
                      ? "bg-[#FAF5EF] border-[#684D43] ring-1 ring-[#684D43]"
                      : "bg-[#FAF8F5] border-[#E2D8CC] hover:border-[#C4B7A7]"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-serif text-lg font-medium text-[#2E2420]">{board.name}</span>
                    {active && (
                      <span className="w-5 h-5 rounded-full bg-[#684D43] text-white flex items-center justify-center text-xs">
                        ✓
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-[#7A6E65] mt-1">{board.desc}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* 2. Class Selection */}
        <div className="space-y-3">
          <label className="block text-xs font-semibold uppercase tracking-wider text-[#73675F]">
            2. Select Class / Grade
          </label>

          <div className="space-y-2.5">
            <div className="text-xs text-[#8A7E75]">Foundation & Primary</div>
            <div className="flex flex-wrap gap-2">
              {[...FOUNDATION_CLASSES, ...PRIMARY_CLASSES].map((lvl) => {
                const active = c === lvl;
                return (
                  <button
                    key={lvl}
                    type="button"
                    onClick={() => { setC(lvl); setS(""); }}
                    className={`px-4 py-2 rounded-lg text-sm border font-medium transition-all cursor-pointer ${
                      active
                        ? "bg-[#684D43] text-white border-[#684D43] shadow-sm"
                        : "bg-[#FAF8F5] text-[#3D332D] border-[#E2D8CC] hover:bg-[#F3EFE9]"
                    }`}
                  >
                    {FOUNDATION_CLASSES.includes(lvl) ? lvl : `Class ${lvl}`}
                  </button>
                );
              })}
            </div>

            <div className="text-xs text-[#8A7E75] pt-1">Middle & Secondary</div>
            <div className="flex flex-wrap gap-2">
              {SECONDARY_CLASSES.map((lvl) => {
                const active = c === lvl;
                return (
                  <button
                    key={lvl}
                    type="button"
                    onClick={() => { setC(lvl); setS(""); }}
                    className={`px-4 py-2 rounded-lg text-sm border font-medium transition-all cursor-pointer ${
                      active
                        ? "bg-[#684D43] text-white border-[#684D43] shadow-sm"
                        : "bg-[#FAF8F5] text-[#3D332D] border-[#E2D8CC] hover:bg-[#F3EFE9]"
                    }`}
                  >
                    Class {lvl}
                  </button>
                );
              })}
            </div>

            <div className="text-xs text-[#8A7E75] pt-1">Senior Secondary</div>
            <div className="flex flex-wrap gap-2">
              {SENIOR_CLASSES.map((lvl) => {
                const active = c === lvl;
                return (
                  <button
                    key={lvl}
                    type="button"
                    onClick={() => { setC(lvl); if (!s) setS("Science"); }}
                    className={`px-4 py-2 rounded-lg text-sm border font-medium transition-all cursor-pointer ${
                      active
                        ? "bg-[#684D43] text-white border-[#684D43] shadow-sm"
                        : "bg-[#FAF8F5] text-[#3D332D] border-[#E2D8CC] hover:bg-[#F3EFE9]"
                    }`}
                  >
                    Class {lvl}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* 3. Stream Selection (Only for 11 & 12) */}
        {hi && (
          <div className="space-y-3 animate-fadeIn">
            <label className="block text-xs font-semibold uppercase tracking-wider text-[#73675F]">
              3. Select Academic Stream
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {STREAMS.map((st) => {
                const active = s === st.id;
                return (
                  <button
                    key={st.id}
                    type="button"
                    onClick={() => setS(st.id)}
                    className={`text-left p-3.5 rounded-xl border transition-all cursor-pointer ${
                      active
                        ? "bg-[#FAF5EF] border-[#684D43] ring-1 ring-[#684D43]"
                        : "bg-[#FAF8F5] border-[#E2D8CC] hover:border-[#C4B7A7]"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-serif font-medium text-[#2E2420]">{st.name}</span>
                      {active && (
                        <span className="w-4 h-4 rounded-full bg-[#684D43] text-white flex items-center justify-center text-xs">
                          ✓
                        </span>
                      )}
                    </div>
                    <p className="text-[11px] text-[#7A6E65] mt-1">{st.desc}</p>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* 4. Subject Options dynamically displayed according to selected class */}
        {c && (
          <div className="space-y-3 pt-2 border-t border-[#EFEAE2]">
            <div className="flex items-center justify-between">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-[#73675F]">
                  {hi ? "4. Curriculum Subjects" : "3. Curriculum Subjects"}
                </label>
                <p className="text-xs text-[#8A7E75] mt-0.5">
                  Tailored for <span className="font-medium text-[#483730]">{b}</span> •{" "}
                  <span className="font-medium text-[#483730]">{FOUNDATION_CLASSES.includes(c) ? c : `Class ${c}`}</span>
                  {hi && s ? ` • ${s}` : ""}
                </p>
              </div>
              <span className="text-xs bg-[#E8EFE8] text-[#346638] px-2.5 py-1 rounded-full font-medium">
                {subjects.length} Subjects Ready
              </span>
            </div>

            {/* Subject Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              {subjects.map((sub) => (
                <div
                  key={sub.name}
                  className="p-3.5 rounded-xl border border-[#E4DCD0] bg-[#FAF8F5] flex items-start gap-3 shadow-xs"
                >
                  <div className="w-10 h-10 rounded-lg bg-white border border-[#E2D8CC] flex items-center justify-center text-xl shrink-0 shadow-xs">
                    {sub.icon}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium text-sm text-[#2E2420] truncate">{sub.name}</h4>
                      <span className="text-[10px] text-[#4A724E] bg-[#EAF2EA] px-2 py-0.5 rounded font-medium">
                        Active
                      </span>
                    </div>
                    <p className="text-xs text-[#7A6E65] mt-1 line-clamp-1 leading-snug">{sub.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Error message */}
        {e && (
          <div className="p-3 rounded-lg text-xs bg-[#FBF1EE] border border-[#F0D1C7] text-[#9B6256] flex items-center gap-2">
            <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <span>{e}</span>
          </div>
        )}

        {/* Submit button: Takes user to the main page */}
        <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-[#8A7E75]">
            {!c
              ? "Please pick your Class above to proceed."
              : hi && !s
              ? "Please select your Stream to proceed."
              : "Ready to explore your personalised study dashboard."}
          </div>

          <button
            type="button"
            disabled={!b || !c || (hi && !s) || saving}
            onClick={save}
            className="w-full sm:w-auto px-7 py-3 rounded-xl bg-[#5C463D] hover:bg-[#483730] text-[#F9F6F0] font-medium text-sm transition-all duration-150 shadow-sm flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            {saving ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                <span>Setting up workspace...</span>
              </>
            ) : (
              <>
                <span>Take Me to the Main Page</span>
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14" />
                  <path d="m12 5 7 7-7 7" />
                </svg>
              </>
            )}
          </button>
        </div>

      </div>
    </div>
  );
}
