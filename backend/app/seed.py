import random, json
from .curriculum_data import CURRICULUM_CHAPTERS
from .curriculum_questions import SUBJECT_QUESTIONS
from .curriculum_generator import generate_topic_questions, validate_question_topic

CLASSES = ["Nursery", "LKG", "UKG"] + [str(i) for i in range(1, 13)]

def subjects_for(board, c, stream):
    if c in ("Nursery", "LKG", "UKG"):
        return ["Mathematics", "Environmental Awareness", "English", "Hindi"]
    n = int(c)
    if n <= 5:
        return ["Mathematics", "Science", "Social Science (SST)", "English", "Hindi"]
    if 6 <= n <= 8:
        # Middle School (Classes 6 - 8): Curiosity / Ganita Prakash / Exploring Society / Poorvi / Malhar + CBSE CT & AI
        return ["Mathematics", "Science", "Social Science (SST)", "English", "Hindi", "Computational Thinking & AI", "Sanskrit", "French"]
    if 9 <= n <= 10:
        # Secondary School (Classes 9 - 10)
        if board in ("ICSE", "CISCE"):
            return [
                "Mathematics", "Science", "Social Science (SST)",
                "English", "Hindi", "Robotics and Artificial Intelligence", "Computer Applications",
                "Commercial Studies", "Economics", "Environmental Applications"
            ]
        return [
            "Mathematics", "Science", "Social Science (SST)", "English", "Hindi",
            "Artificial Intelligence", "Information Technology", "Computer Applications",
            "Computational Thinking & AI", "Sanskrit", "French"
        ]
    # Senior Secondary (Classes 11 - 12)
    if board in ("ISC", "CISCE"):
        if stream == "Science":
            return ["Physics", "Chemistry", "Mathematics", "Biology", "English", "Computer Science", "Electricity & Electronics"]
        if stream == "Commerce":
            return ["Accountancy", "Business Studies", "Economics", "Mathematics", "English", "Applied Mathematics"]
        if stream == "Humanities":
            return ["History", "Political Science", "Geography", "Sociology", "Psychology", "Economics", "English"]

    if stream == "Science":
        return ["Physics", "Chemistry", "Mathematics", "Biology", "English Core", "Computer Science", "Applied Mathematics", "Artificial Intelligence", "Data Science"]
    if stream == "Commerce":
        return ["Accountancy", "Business Studies", "Economics", "Mathematics", "English Core", "Applied Mathematics", "Informatics Practices", "Financial Markets Management"]
    if stream == "Humanities":
        return ["History", "Political Science", "Geography", "Economics", "English Core", "Psychology", "Sociology", "Legal Studies"]
    return ["Mathematics", "Science", "Social Science (SST)", "English", "Hindi"]

def get_chapter_data(c, stream, s):
    # 1. Exact class and stream key, e.g. "11_Science", "12_Commerce"
    if stream:
        st_key = f"{c}_{stream}"
        if st_key in CURRICULUM_CHAPTERS and s in CURRICULUM_CHAPTERS[st_key]:
            return CURRICULUM_CHAPTERS[st_key][s]

    # 2. Exact class key, e.g. "5", "10", or "Foundation" for Nursery/LKG/UKG
    class_key = "Foundation" if c in ("Nursery", "LKG", "UKG") else str(c)
    if class_key in CURRICULUM_CHAPTERS and s in CURRICULUM_CHAPTERS[class_key]:
        return CURRICULUM_CHAPTERS[class_key][s]

    # 3. Stream or class fallback
    for alt_key in [f"{c}_Science", f"{c}_Commerce", f"{c}_Humanities", "10", "8", "5", "3", "Foundation"]:
        if alt_key in CURRICULUM_CHAPTERS and s in CURRICULUM_CHAPTERS[alt_key]:
            return CURRICULUM_CHAPTERS[alt_key][s]

    return [(f"{s}: Core Concepts", ["Overview", "Practice"]), (f"{s}: Advanced Applications", ["In-depth analysis", "Problem solving"])]

def mathq(rnd, lvl):
    a, b = rnd.randint(2, 9 + lvl * 8), rnd.randint(2, 9 + lvl * 8)
    ans = a * b + a
    opts = sorted({ans, ans + a, ans - b if ans - b > 0 else ans + 2, ans + 1})
    return (
        f"Compute: {a} × {b} + {a}",
        [str(o) for o in opts],
        opts.index(ans),
        f"Step 1: {a} × {b} = {a * b}. Step 2: Add {a} gives {ans}."
    )

def seed(cx, force=False):
    # Check if modern official subjects already exist
    existing_count = cx.execute("select count(*) n from subjects").fetchone()["n"]
    has_hindi = cx.execute("select count(*) n from subjects where name='Hindi'").fetchone()["n"] if existing_count > 0 else 0

    if existing_count > 0 and has_hindi > 0 and not force:
        return

    print("Seeding official CBSE & ICSE curriculum with real chapters, Hindi, Science, SST, Sanskrit, French...", flush=True)
    # Clear old placeholder data
    cx.execute("TRUNCATE questions, topics, chapters, subjects CASCADE;")

    rnd = random.Random(42)

    for board in ("CBSE", "ICSE"):
        for c in CLASSES:
            streams = [None] if c not in ("11", "12") else ["Science", "Commerce", "Humanities"]
            for st in streams:
                for s in subjects_for(board, c, st):
                    sid = cx.execute(
                        "insert into subjects(board, class_level, stream, name) values(%s, %s, %s, %s) returning id",
                        (board, c, st, s)
                    ).fetchone()["id"]

                    chapters = get_chapter_data(c, st, s)

                    for i, (ch_name, topics_list) in enumerate(chapters):
                        cid = cx.execute(
                            "insert into chapters(subject_id, name, ord) values(%s, %s, %s) returning id",
                            (sid, ch_name, i + 1)
                        ).fetchone()["id"]

                        for t_name in topics_list:
                            tid = cx.execute(
                                "insert into topics(chapter_id, name) values(%s, %s) returning id",
                                (cid, t_name)
                            ).fetchone()["id"]

                            # Generate authentic topic-matched questions
                            gen_qs = generate_topic_questions(
                                topic_id=tid,
                                topic_name=t_name,
                                chapter_name=ch_name,
                                subject_name=s,
                                class_level=c,
                                difficulty="Medium",
                                count=2
                            )
                            for p, o, a, exp, q_diff in gen_qs:
                                if validate_question_topic(p, t_name, ch_name, s, c):
                                    cx.execute(
                                        "insert into questions(topic_id, prompt, options, answer, explanation, difficulty, is_sample) values(%s, %s, %s, %s, %s, %s, %s)",
                                        (tid, p, json.dumps(o), a, exp, q_diff, False)
                                    )
    print("Database seeding completed successfully!", flush=True)

