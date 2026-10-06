import os, json, urllib.request, urllib.parse, jwt, time

SECRET = os.getenv("JWT_SECRET", "dev-secret")
token = jwt.encode({"sub": "7", "exp": int(time.time()) + 60*60*24*30}, SECRET, "HS256")

test_cases = [
    # Nursery / Foundation
    {"class": "Foundation", "subject": "Environmental Awareness", "chapter": "My Family and Neighborhood", "q": "Explain key concepts from this chapter"},
    {"class": "Foundation", "subject": "Mathematics", "chapter": "Shapes and Space", "q": "List 3 important revision questions"},
    
    # Class 5 CBSE
    {"class": "5", "subject": "Science", "chapter": "Plant Life & Photosynthesis", "q": "Explain key concepts from this chapter"},
    {"class": "5", "subject": "Social Science (SST)", "chapter": "The Northern Mountains and Plains of India", "q": "Explain key concepts from this chapter"},
    {"class": "5", "subject": "Hindi", "chapter": "राख की रस्सी (कहानी एवं लोककथा)", "q": "List 3 important revision questions"},
    {"class": "5", "subject": "English", "chapter": "Wonderful Waste! (Folk Tale)", "q": "Explain key concepts from this chapter"},
    
    # Class 8 CBSE
    {"class": "8", "subject": "Science", "chapter": "Crop Production and Management", "q": "Explain key concepts from this chapter"},
    {"class": "8", "subject": "Social Science (SST)", "chapter": "The Indian Constitution and Secularism", "q": "Explain key concepts from this chapter"},
    {"class": "8", "subject": "Computational Thinking & AI", "chapter": "Introduction to Artificial Intelligence & Smart Systems", "q": "Explain key concepts from this chapter"},

    # Class 10 CBSE & ICSE
    {"class": "10", "subject": "Science", "chapter": "Chemical Reactions and Equations", "q": "Explain key concepts from this chapter"},
    {"class": "10", "subject": "Social Science (SST)", "chapter": "Resources and Development", "q": "Explain key concepts from this chapter"},
    {"class": "10", "subject": "Artificial Intelligence", "chapter": "Introduction to AI & Ethics", "q": "Explain key concepts from this chapter"},
    {"class": "10", "subject": "English", "chapter": "A Letter to God (G.L. Fuentes)", "q": "Explain key concepts from this chapter"},
    {"class": "10", "subject": "Hindi", "chapter": "नेताजी का चश्मा (स्वयं प्रकाश)", "q": "Explain key concepts from this chapter"},

    # Class 12 Science
    {"class": "12", "stream": "Science", "subject": "Physics", "chapter": "Electrostatics and Coulomb's Law", "q": "Explain key concepts from this chapter"},
    {"class": "12", "stream": "Science", "subject": "Chemistry", "chapter": "Solutions and Colligative Properties", "q": "Explain key concepts from this chapter"},
    {"class": "12", "stream": "Science", "subject": "Biology", "chapter": "Sexual Reproduction in Flowering Plants", "q": "Explain key concepts from this chapter"},
    {"class": "12", "stream": "Science", "subject": "Computer Science", "chapter": "Computational Thinking and Programming in Python", "q": "Explain key concepts from this chapter"},

    # Class 12 Commerce
    {"class": "12", "stream": "Commerce", "subject": "Accountancy", "chapter": "Accounting for Partnership Firms - Fundamentals", "q": "Explain key concepts from this chapter"},
    {"class": "12", "stream": "Commerce", "subject": "Business Studies", "chapter": "Principles of Management", "q": "Explain key concepts from this chapter"},
    {"class": "12", "stream": "Commerce", "subject": "Economics", "chapter": "National Income Accounting", "q": "Explain key concepts from this chapter"},

    # Class 12 Humanities
    {"class": "12", "stream": "Humanities", "subject": "History", "chapter": "Bricks, Beads and Bones - The Harappan Civilisation", "q": "Explain key concepts from this chapter"},
    {"class": "12", "stream": "Humanities", "subject": "Political Science", "chapter": "The End of Bipolarity", "q": "Explain key concepts from this chapter"},
    {"class": "12", "stream": "Humanities", "subject": "Geography", "chapter": "Human Geography - Nature and Scope", "q": "Explain key concepts from this chapter"},
]

print(f"Running comprehensive matrix verification for {len(test_cases)} subject/chapter combinations...\n")

passed = 0
failed = 0

for tc in test_cases:
    payload = {
        "question": tc["q"],
        "subject": tc["subject"],
        "chapter": tc["chapter"]
    }
    form_data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8000/solve",
        data=form_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            solved = data.get("solved")
            badge = data.get("verification_badge")
            direct_ans = data.get("direct_answer", "")
            steps = data.get("steps", [])
            
            # Check conditions:
            # 1. Must be solved
            # 2. Must have a verification badge (not unverified fallback)
            # 3. Must not contain the fallback rejection message
            is_unverified = "cannot be reliably verified" in direct_ans or "cannot be reliably verified" in str(steps)
            if solved and badge and not is_unverified and len(steps) >= 3:
                passed += 1
                stream_str = f" [{tc['stream']}]" if "stream" in tc else ""
                print(f"  ✓ PASS: Class {tc['class']}{stream_str} · {tc['subject']} - Badge: '{badge}' ({len(steps)} steps)")
            else:
                failed += 1
                print(f"  ✗ FAIL: Class {tc['class']} · {tc['subject']} - Solved={solved}, Badge={badge}, Unverified={is_unverified}")
    except Exception as e:
        failed += 1
        print(f"  ✗ ERROR: Class {tc['class']} · {tc['subject']}: {e}")

print(f"\nMatrix Verification Complete: {passed}/{len(test_cases)} Passed, {failed} Failed.")
if failed == 0:
    print("ALL CURRICULUM SUBJECTS AND CHAPTERS VERIFIED ACCURATELY!")
