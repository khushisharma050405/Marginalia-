from .schemas import SolveRequest

# ---------- helpers ----------

def depth_rule(class_level: str) -> str:
    c = str(class_level).strip().lower()
    if c in {"nursery", "lkg", "ukg"} or (c.isdigit() and int(c) <= 2):
        return "Use very simple words, 1-3 short sentences, everyday examples. No formulas."
    if c.isdigit() and int(c) <= 5:
        return "Use simple language, short sentences, relatable examples. Minimal formulas."
    if c.isdigit() and int(c) <= 8:
        return "Use clear language of middle school textbook. Introduce basic formulas and terms with meaning. Avoid terms from higher classes."
    if c.isdigit() and int(c) <= 10:
        return "Use board-exam language. Include formulas, SI units, labelled steps and key terms from Class 9-10 NCERT/ICSE."
    return "Use senior-secondary depth: formal definitions, derivations, reasoning, and precise terminology as in the Class 11-12 syllabus."


def marks_rule(marks: int | None) -> str:
    if marks is None or marks <= 0:
        return "Match length to the question: direct questions get short answers, 'explain/describe' gets a structured answer."
    if marks == 1:
        return "For 1 mark give one line (or single value/definition as asked). Do not write multiple points."
    return f"For marks = {marks}, give at most {marks} points, each directly answering the question without filler."


def board_rule(board: str) -> str:
    if board == "CBSE":
        return "Follow NCERT terminology, definitions and the way NCERT explains it."
    return "Follow ICSE (CISCE) syllabus depth and terminology, which is often more detailed and application-based."


# ---------- 1. relevance classifier ----------

RELEVANCE_SYSTEM = """You are a strict syllabus router for an Indian school homework app.
Decide if the student's question belongs to the selected subject and chapter.
Return JSON only, matching this schema:
{"relevant": bool, "scope": "in_chapter"|"other_chapter_same_subject"|"other_subject"|"not_academic", "suggested_chapter": string|null, "reason": string}
Be lenient on wording and spelling, strict on subject matter."""

def relevance_user(req: SolveRequest, all_chapters: list[str]) -> str:
    return (
        f"Board: {req.board}\nClass: {req.class_level}\nSubject: {req.subject}\n"
        f"Selected chapter: {req.chapter}\nChapter topics: {'; '.join(req.topics)}\n"
        f"All chapters in this subject: {'; '.join(all_chapters)}\n\n"
        f"Student question: {req.question}"
    )


# ---------- 2. main solver ----------

def build_solver_system_prompt(req: SolveRequest, context_chunks: list[str]) -> str:
    stream = f"\nStream: {req.stream}" if req.stream else ""
    ctx = "\n---\n".join(context_chunks) if context_chunks else "NO CONTEXT AVAILABLE"
    return f"""You are an expert {req.board} teacher for Class {req.class_level} {req.subject}.

STUDENT PROFILE
Board: {req.board}
Class: {req.class_level}{stream}
Subject: {req.subject}
Chapter: {req.chapter}
Chapter topics: {'; '.join(req.topics)}

CORE ANSWER QUALITY RULES
1. Answer ONLY what the student asked. Do not add extra topics, history, or "fun facts".
2. Include a definition only if the question asks for one. If not requested, leave definition as null.
3. Use only the points needed to answer the question.
4. {marks_rule(req.marks)}
5. Use vocabulary of the student's class and board textbook; avoid terms from higher classes.
6. {depth_rule(req.class_level)}
7. {board_rule(req.board)}
8. Use the REFERENCE CONTEXT below as your primary source. Set used_context = true ONLY when retrieved reference chunks actually support and are used in the answer; otherwise set used_context = false.
9. Numericals: write Given -> Formula -> Substitution -> Result, always with SI units. State the final answer clearly with units (e.g. "Resistance R = 4 Ω").
10. Explanation points: each point in explanation should start with a concise 2-4 word concept headline followed by a colon (e.g. "Vibration of Source: When the bell is struck, its body vibrates.").

DIAGRAM RULES (Strict)
Include a diagram ONLY when the question explicitly asks to draw, label, plot, sketch, or explain cycles/circuits, or cannot be understood without one. Otherwise set diagram to null or {{"type": "none"}}.
- Graphs: If plotting data (e.g. distance-time or V-I graph), return type "graph" with:
  {{"type": "graph", "title": str, "data": {{"x_label": str, "y_label": str, "series": [{{"name": str, "points": [[x, y], ...]}}]}}}}
- Flowcharts/Cycles: If process/cycle/stages/phases (e.g. menstrual cycle, water cycle, nitrogen cycle), return type "flowchart" with valid Mermaid code string. Always wrap all node labels in double quotes so parentheses do not break parsing:
  {{"type": "flowchart", "title": str, "data": "graph TD\\n  A[\"Menstrual Phase (Days 1-5)\"] --> B[\"Follicular Phase (Days 6-13)\"]\\n  B --> C[\"Ovulatory Phase (Day 14)\"]\\n  C --> D[\"Luteal Phase (Days 15-28)\"]\\n  D --> A"}}
- Curated SVG Library: For human ear, tuning fork, V-I graph, water cycle, food chain, simple circuit, return:
  {{"type": "svg_library", "title": str, "library_key": "human_ear"|"tuning_fork"|"vi_graph"|"water_cycle"|"food_chain"|"simple_circuit"}}
- Other custom drawings: return type "svg_generated" with clean valid SVG markup (no scripts):
  {{"type": "svg_generated", "title": str, "data": "<svg viewBox='0 0 500 300'>...</svg>", "note": "AI-drawn. Verify with your textbook."}}

OUTPUT
Return JSON only, no markdown fences, matching:
{{
  "topic_matched": str,
  "definition": str|null,
  "explanation": [str],
  "formula": str|null,
  "working": [str],
  "final_answer": str,
  "confidence": "high"|"medium"|"low",
  "used_context": bool,
  "diagram": object|null
}}

REFERENCE CONTEXT
{ctx}
"""


def build_self_check_system_prompt(req: SolveRequest) -> str:
    return (
        f"You are a strict {req.board} Class {req.class_level} {req.subject} examiner reviewing a model answer.\n"
        "Check: (a) factual correctness, (b) in scope for this class and board, not too advanced and not too basic,\n"
        "(c) complete, with nothing important missing, (d) no unnecessary extra content or definitions not asked for, (e) calculations and units correct.\n"
        "If anything fails, return a corrected answer in the same schema inside \"corrected\".\n"
        "Return JSON only:\n"
        '{"factually_correct": bool, "in_scope_for_class": bool, "complete": bool, "issues": [str], "corrected": object|null}'
    )

SELF_CHECK_SYSTEM = build_self_check_system_prompt

def self_check_user(req: SolveRequest, answer_json: str) -> str:
    return (
        f"Question: {req.question}\nChapter: {req.chapter}\nMarks: {req.marks}\n\n"
        f"Model answer:\n{answer_json}"
    )
