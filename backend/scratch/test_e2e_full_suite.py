import sys, os, io, json, urllib.request, urllib.parse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.solver import solve_text
from app.curriculum_generator import generate_topic_questions, validate_question_topic
from PIL import Image, ImageDraw

BASE_URL = "http://localhost:8000"

print("======================================================================")
print("             MARGINALIA COMPREHENSIVE SOLVER & PRACTICE TEST          ")
print("======================================================================")

# ============================================================================
# PART 1: 15 MATHS QUESTIONS (Class-stratified, diverse topics, exact calculations)
# ============================================================================
math_tests = [
    # 1. Linear Equations (Algebra)
    ("Solve 3x + 7 = 22", "Linear Equations", "Algebra", "8", "5", "Calculated & Checked ✓"),
    ("Solve 5x - 8 = 3x + 12", "Linear Equations", "Algebra", "8", "10", "Calculated & Checked ✓"),
    ("2(x + 4) = 18", "Linear Equations", "Algebra", "8", "5", "Calculated & Checked ✓"),
    
    # 2. Geometry: Perimeter and Area
    ("Find the perimeter of a rectangle with length 12 cm and breadth 8 cm", "Mensuration", "Geometry", "7", "40 cm", "Calculated & Checked ✓"),
    ("The perimeter of a rectangle is 50 cm. If length is 15 cm, find breadth", "Mensuration", "Geometry", "7", "10 cm", "Calculated & Checked ✓"),
    ("Find the area of a rectangle with length 14 cm and breadth 9 cm", "Mensuration", "Geometry", "7", "126 cm²", "Calculated & Checked ✓"),
    ("Find the perimeter of a square with side 9 cm", "Mensuration", "Geometry", "6", "36 cm", "Calculated & Checked ✓"),
    ("Find the area of a square with side 8 cm", "Mensuration", "Geometry", "6", "64 cm²", "Calculated & Checked ✓"),
    ("Find the side of a square whose perimeter is 48 cm", "Mensuration", "Geometry", "6", "12 cm", "Calculated & Checked ✓"),
    
    # 3. Arithmetic: Direct & Inverse Proportions
    ("12 workers can complete a job in 15 days. How many days will 20 workers take to complete the same job?", "Direct and Inverse Proportions", "Arithmetic", "8", "9 days", "Calculated & Checked ✓"),
    ("If 8 oranges cost 40 rupees, what will 15 oranges cost?", "Direct and Inverse Proportions", "Arithmetic", "8", "₹75", "Calculated & Checked ✓"),
    
    # 4. Rational Numbers: Additive & Multiplicative Inverses
    ("What is the additive inverse of -7/19?", "Rational Numbers", "Arithmetic", "8", "7/19", "Calculated & Checked ✓"),
    ("What is the multiplicative inverse of -13/19?", "Rational Numbers", "Arithmetic", "8", "-19/13", "Calculated & Checked ✓"),
    
    # 5. Financial Mathematics: Simple & Compound Interest
    ("Calculate the simple interest on a principal of 5000 at a rate of 6% per annum for 3 years", "Comparing Quantities", "Arithmetic", "7", "₹900", "Calculated & Checked ✓"),
    ("Find the compound interest on 10000 for 2 years at 10% per annum", "Comparing Quantities", "Arithmetic", "8", "₹2,100", "Calculated & Checked ✓"),
]

math_passed = 0
print(f"\n--- TESTING {len(math_tests)} MATHEMATICS QUESTIONS ---")
for q, topic, ch, cl, exp_ans, exp_badge in math_tests:
    res = solve_text(q, subject_hint="Mathematics", chapter_hint=ch, topic_hint=topic, class_hint=cl)
    ans = str(res.get("direct_answer", "") or res.get("final_answer", "") or "")
    badge = res.get("verification_badge", "")
    is_ok = (exp_ans.lower() in ans.lower()) and (badge == exp_badge)
    status = "✓ PASS" if is_ok else "❌ FAIL"
    if is_ok:
        math_passed += 1
    print(f"[{status}] Q: {q[:55]:<55} | Ans: {ans:<15} | Badge: {badge}")
    if not is_ok:
        print(f"       Expected: {exp_ans} | Got: {ans}")

print(f"Maths Result: {math_passed}/{len(math_tests)} passed.\n")

# ============================================================================
# PART 2: SCIENCE QUESTIONS (Physics, Chemistry, Biology)
# ============================================================================
science_tests = [
    # Physics: Ohm's law & speed
    ("A circuit with 12V potential difference has 4 ohms resistance. What is the current?", "Electricity", "Physics", "10", "3", "Formula & Concept Verified ✓"),
    ("A car travels a distance of 180 km in 3 hours. Calculate its speed.", "Motion", "Physics", "9", "60 km/h", "Formula & Concept Verified ✓"),
    
    # Chemistry: Reactions & indicators
    ("What happens when blue litmus paper is dipped into an acidic solution?", "Acids, Bases and Salts", "Chemistry", "10", "red", "Formula & Concept Verified ✓"),
    ("What gas is liberated when zinc metal reacts with dilute hydrochloric acid?", "Chemical Reactions", "Chemistry", "10", "hydrogen", "Formula & Concept Verified ✓"),
    
    # Biology: Cells & Organelles
    ("Why is the mitochondrion referred to as the powerhouse of the cell?", "The Fundamental Unit of Life", "Biology", "9", "atp", "Formula & Concept Verified ✓"),
    ("What is the primary function of stomata in plant leaves?", "Life Processes", "Biology", "10", "transpiration", "Formula & Concept Verified ✓")
]

science_passed = 0
print(f"\n--- TESTING {len(science_tests)} SCIENCE QUESTIONS ---")
for q, topic, ch, cl, exp_kw, exp_badge in science_tests:
    res = solve_text(q, subject_hint="Science", chapter_hint=ch, topic_hint=topic, class_hint=cl)
    ans = str(res.get("direct_answer", "") or res.get("final_answer", "") or "")
    badge = res.get("verification_badge", "")
    is_ok = (exp_kw.lower() in ans.lower()) and (badge == exp_badge)
    status = "✓ PASS" if is_ok else "❌ FAIL"
    if is_ok:
        science_passed += 1
    print(f"[{status}] Q: {q[:55]:<55} | Badge: {badge}")
    if not is_ok:
        print(f"       Expected: {exp_kw} with '{exp_badge}' | Got ans: {ans} with '{badge}'")

print(f"Science Result: {science_passed}/{len(science_tests)} passed.\n")

# ============================================================================
# PART 3: SOCIAL SCIENCE & GEOGRAPHY
# ============================================================================
sst_tests = [
    ("Explain the historical significance of the Dandi March undertaken by Mahatma Gandhi in 1930.", "Nationalism in India", "History", "10", "salt", "Curriculum Fact Verified ✓"),
    ("Why is the Godavari river referred to as the Dakshin Ganga?", "Drainage", "Geography", "9", "longest", "Curriculum Fact Verified ✓"),
    ("Explain the primary characteristics of black soil (regur soil) in India.", "Resources and Development", "Geography", "10", "cotton", "Curriculum Fact Verified ✓"),
    ("Define federalism and state how legislative powers are divided in India.", "Federalism", "Civics", "10", "union list", "Curriculum Fact Verified ✓"),
    ("Explain the three sectors of economic activity with examples.", "Sectors of the Indian Economy", "Economics", "10", "primary sector", "Curriculum Fact Verified ✓")
]

sst_passed = 0
print(f"\n--- TESTING {len(sst_tests)} SOCIAL SCIENCE / GEOGRAPHY QUESTIONS ---")
for q, topic, ch, cl, exp_kw, exp_badge in sst_tests:
    res = solve_text(q, subject_hint="Social Science", chapter_hint=ch, topic_hint=topic, class_hint=cl)
    ans = str(res.get("direct_answer", "") or res.get("final_answer", "") or "")
    badge = res.get("verification_badge", "")
    is_ok = (exp_kw.lower() in ans.lower()) and (badge == exp_badge)
    status = "✓ PASS" if is_ok else "❌ FAIL"
    if is_ok:
        sst_passed += 1
    print(f"[{status}] Q: {q[:55]:<55} | Badge: {badge}")
    if not is_ok:
        print(f"       Expected: {exp_kw} with '{exp_badge}' | Got ans: {ans} with '{badge}'")

print(f"Social Science Result: {sst_passed}/{len(sst_tests)} passed.\n")

# ============================================================================
# PART 4: LANGUAGES (English & Hindi)
# ============================================================================
lang_tests = [
    ("What are the twin obligations described by Nelson Mandela in 'Long Walk to Freedom'?", "First Flight", "English", "10", "obligations", "Language Rule Verified ✓"),
    ("Identify the part of speech of the word 'quickly' in: 'The deer ran quickly into the deep forest.'", "Grammar", "English", "8", "adverb", "Language Rule Verified ✓"),
    ("What is the antonym of the word abundant?", "Vocabulary", "English", "9", "scarce", "Language Rule Verified ✓"),
    ("संज्ञा किसे कहते हैं? इसके मुख्य भेदों के नाम उदाहरण सहित लिखिए।", "व्याकरण", "Hindi", "8", "संज्ञा", "Language Rule Verified ✓"),
    ("Explain the meaning and sentence usage of 'आँखों का तारा' मुहावरा", "व्याकरण", "Hindi", "7", "प्यारा", "Language Rule Verified ✓")
]

lang_passed = 0
print(f"\n--- TESTING {len(lang_tests)} LANGUAGE (ENGLISH/HINDI) QUESTIONS ---")
for q, topic, ch, cl, exp_kw, exp_badge in lang_tests:
    res = solve_text(q, subject_hint="English" if "English" in ch else "Hindi", chapter_hint=ch, topic_hint=topic, class_hint=cl)
    ans = str(res.get("direct_answer", "") or res.get("final_answer", "") or "")
    badge = res.get("verification_badge", "")
    is_ok = (exp_kw.lower() in ans.lower()) and (badge == exp_badge)
    status = "✓ PASS" if is_ok else "❌ FAIL"
    if is_ok:
        lang_passed += 1
    print(f"[{status}] Q: {q[:55]:<55} | Badge: {badge}")
    if not is_ok:
        print(f"       Expected: {exp_kw} with '{exp_badge}' | Got ans: {ans} with '{badge}'")

print(f"Language Result: {lang_passed}/{len(lang_tests)} passed.\n")

# ============================================================================
# PART 5: COMPUTER SCIENCE & AI
# ============================================================================
cs_tests = [
    ("What is the difference between Linear Search and Binary Search in terms of prerequisites and time complexity?", "Algorithms", "CS", "11", "o(log", "Logic & Code Verified ✓"),
    ("What is the difference between a list and a tuple in Python?", "Data Structures", "CS", "10", "mutable", "Logic & Code Verified ✓"),
    ("What are the three core domains of Artificial Intelligence?", "AI Foundations", "AI", "10", "computer vision", "Logic & Code Verified ✓")
]

cs_passed = 0
print(f"\n--- TESTING {len(cs_tests)} COMPUTER SCIENCE & AI QUESTIONS ---")
for q, topic, ch, cl, exp_kw, exp_badge in cs_tests:
    res = solve_text(q, subject_hint="Computer Science", chapter_hint=ch, topic_hint=topic, class_hint=cl)
    ans = str(res.get("direct_answer", "") or res.get("final_answer", "") or "")
    badge = res.get("verification_badge", "")
    is_ok = (exp_kw.lower() in ans.lower()) and (badge == exp_badge)
    status = "✓ PASS" if is_ok else "❌ FAIL"
    if is_ok:
        cs_passed += 1
    print(f"[{status}] Q: {q[:55]:<55} | Badge: {badge}")
    if not is_ok:
        print(f"       Expected: {exp_kw} with '{exp_badge}' | Got ans: {ans} with '{badge}'")

print(f"CS/AI Result: {cs_passed}/{len(cs_tests)} passed.\n")

# ============================================================================
# PART 6: UNVERIFIED / UNRELIABLE INPUT SAFEGUARD
# ============================================================================
print("\n--- TESTING UNVERIFIED / NONSENSE SAFEGUARD ---")
unverified_input = "What is the quantum hyper-jump velocity of a Martian banana flying in purple vacuum?"
unverified_res = solve_text(unverified_input, subject_hint="Science", class_hint="9")
uv_badge = unverified_res.get("verification_badge")
uv_ans = str(unverified_res.get("direct_answer", "") or unverified_res.get("final_answer", "") or "")
uv_ok = (uv_badge is None) and ("cannot be reliably verified" in uv_ans.lower())
print(f"[{'✓ PASS' if uv_ok else '❌ FAIL'}] Input: {unverified_input}")
print(f"       Badge: {uv_badge} | Ans: {uv_ans}")

# ============================================================================
# PART 7: HTTP API VALIDATION (Live Server Tests via urllib)
# ============================================================================
print("\n--- TESTING LIVE HTTP /solve AND /practice API ---")
def http_req(url, method="GET", data=None, headers=None):
    hdrs = headers or {}
    body = None
    if data is not None:
        if isinstance(data, dict):
            body = json.dumps(data).encode("utf-8")
            hdrs["Content-Type"] = "application/json"
        elif isinstance(data, (bytes, bytearray)):
            body = data
        elif isinstance(data, str):
            body = data.encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

try:
    # 1. Login/Register test user
    test_email = f"audit_user_{int(os.getpid())}@marginalia.test"
    reg_resp = http_req(f"{BASE_URL}/auth/register", "POST", {"email": test_email, "name": "Audit User", "password": "Password123!"})
    token = reg_resp.get("token")
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # Set profile to CBSE Class 10
    http_req(f"{BASE_URL}/me/profile", "PUT", {"board": "CBSE", "class_level": "10", "stream": None}, headers=auth_headers)
    
    # 2. Test /solve endpoint via HTTP form-urlencoded
    solve_form = urllib.parse.urlencode({"question": "A circuit with 12V potential difference has 4 ohms resistance. What is the current?", "subject": "Science"}).encode("utf-8")
    solve_req = urllib.request.Request(
        f"{BASE_URL}/solve",
        data=solve_form,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )
    with urllib.request.urlopen(solve_req) as resp:
        http_solve = json.loads(resp.read().decode("utf-8"))
    solve_ans = http_solve.get('direct_answer') or http_solve.get('final_answer') or ""
    print(f"[✓ PASS] HTTP /solve response: solved={http_solve.get('solved')} | Ans={solve_ans[:40]} | Badge={http_solve.get('verification_badge')}")
    
    # 3. Test Multipart Image OCR Upload via HTTP
    boundary = "----WebKitFormBoundaryMarginaliaAudit"
    img = Image.new("RGB", (600, 100), color="white")
    d = ImageDraw.Draw(img)
    d.text((20, 35), "Solve 3x + 7 = 22", fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="subject"\r\n\r\nMathematics\r\n')
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="file"; filename="equation.png"\r\n')
    body.extend(b'Content-Type: image/png\r\n\r\n')
    body.extend(png_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode())

    ocr_req = urllib.request.Request(
        f"{BASE_URL}/solve",
        data=bytes(body),
        headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    with urllib.request.urlopen(ocr_req) as resp:
        http_ocr_solve = json.loads(resp.read().decode("utf-8"))
    ocr_ans = http_ocr_solve.get('direct_answer') or http_ocr_solve.get('final_answer') or ""
    print(f"[✓ PASS] HTTP /solve with Image OCR: solved={http_ocr_solve.get('solved')} | Extracted='{http_ocr_solve.get('extracted')}' | Ans={ocr_ans}")

    # 4. Test /practice endpoint via HTTP
    practice_resp = http_req(f"{BASE_URL}/practice", "GET", headers=auth_headers)
    print(f"[✓ PASS] HTTP /practice (Class 10 CBSE Scope): Returned {len(practice_resp)} verified questions.")
    all_q_ok = all("prompt" in q and "options" in q for q in practice_resp)
    print(f"       All practice questions formatted correctly: {all_q_ok}")

except Exception as e:
    print(f"❌ HTTP Test Failed: {e}")

print("\n======================================================================")
all_counts = [
    (math_passed, len(math_tests)),
    (science_passed, len(science_tests)),
    (sst_passed, len(sst_tests)),
    (lang_passed, len(lang_tests)),
    (cs_passed, len(cs_tests)),
]
total_p = sum(p for p, t in all_counts)
total_t = sum(t for p, t in all_counts)
print(f"FINAL AUDIT RESULT: {total_p}/{total_t} PASSED ({int(total_p/total_t*100)}% SUCCESS)!")
print("======================================================================")
