import jwt, os, time, json, urllib.request, urllib.parse
from typing import Any
import psycopg
from psycopg.rows import dict_row

SECRET = os.getenv("JWT_SECRET", "dev-secret")
token = jwt.encode({"sub": "7", "exp": int(time.time()) + 60*60*24*30}, SECRET, "HS256")

# Test 1: Computational Thinking & AI
form_data = urllib.parse.urlencode({
    "question": "Explain key concepts from this chapter",
    "subject": "Computational Thinking & AI",
    "chapter": "Introduction to Artificial Intelligence & Smart Systems"
}).encode("utf-8")

req = urllib.request.Request(
    "http://localhost:8000/solve",
    data=form_data,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
)
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    print("CT & AI Status:", resp.status)
    print("Solved:", res.get("solved"))
    print("Badge:", res.get("verification_badge"))
    print("Direct Answer:", res.get("direct_answer")[:100] if res.get("direct_answer") else "None")
    print("Steps count:", len(res.get("steps", [])))
    for s in res.get("steps", []):
        print("  *", s[0])

# Test 2: Practice endpoint for Class 6 CT & AI
conn: Any = psycopg.connect("postgresql://marginalia:marginalia@localhost:5432/marginalia", row_factory=dict_row)  # type: ignore
with conn.cursor() as cur:  # pylint: disable=no-member
    topic: Any = cur.execute("""
        select t.id, t.name as topic_name, c.name as ch_name, s.name as sub_name 
        from topics t 
        join chapters c on c.id = t.chapter_id 
        join subjects s on s.id = c.subject_id 
        where s.name = %s and s.class_level = %s 
        limit 1
    """, ("Computational Thinking & AI", "6")).fetchone()

if topic:
    tid = topic["id"]
    tname = topic["topic_name"]
    print(f"\nTesting practice questions for topic: {tname}")
    req_p = urllib.request.Request(
        f"http://localhost:8000/practice?topic_id={tid}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req_p) as p_resp:
        p_data = json.loads(p_resp.read().decode())
        qs = p_data if isinstance(p_data, list) else p_data.get("questions", [])
        print(f"Practice questions returned: {len(qs)}")
        tf_count = 0
        fib_count = 0
        mcq_count = 0
        for i, q in enumerate(qs):
            opts = json.loads(q["options"]) if isinstance(q["options"], str) else q["options"]
            pr = q['prompt']
            qtype = "True/False" if len(opts) == 2 and opts == ["True", "False"] else ("Fill in Blank" if "_____" in pr else "Standard MCQ")
            if qtype == "True/False": tf_count += 1
            elif qtype == "Fill in Blank": fib_count += 1
            else: mcq_count += 1
            print(f"  Q{i+1} [{qtype}]: {pr[:70]}... | Options ({len(opts)}): {opts}")
        print(f"\nSummary counts -> MCQs: {mcq_count}, True/False: {tf_count}, Fill-in-the-Blank: {fib_count}")

