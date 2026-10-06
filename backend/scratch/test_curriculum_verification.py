import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.curriculum_generator import generate_topic_questions, validate_question_topic

test_cases = [
    # 1. Foundation
    ("English", "Alphabet", "Letter Identification", "Nursery"),
    ("Mathematics", "Numbers", "Counting 1 to 20", "1"),
    ("EVS", "My Body", "Sense Organs", "2"),
    
    # 2. Middle School Mathematics
    ("Mathematics", "Rational Numbers", "Closure Property of Rational Numbers", "8"),
    ("Mathematics", "Rational Numbers", "Additive and Multiplicative Identity", "8"),
    ("Mathematics", "Direct and Inverse Proportions", "Inverse Proportion Problems", "8"),
    ("Mathematics", "Linear Equations in One Variable", "Solving Equations with Variables on Both Sides", "8"),
    ("Mathematics", "Understanding Quadrilaterals", "Angle Sum Property of a Quadrilateral", "8"),
    
    # 3. Middle / Secondary Science
    ("Science", "Atoms and Molecules", "Law of Constant Proportions", "9"),
    ("Science", "Force and Laws of Motion", "Newton's First Law of Motion", "9"),
    ("Science", "The Fundamental Unit of Life", "Cell Structure and Functions", "9"),
    ("Science", "Electricity", "Ohm's Law and Resistance", "10"),
    ("Science", "Light - Reflection and Refraction", "Mirror Formula and Lenses", "10"),
    ("Science", "Acids, Bases and Salts", "Reaction of Acids with Metals", "10"),
    
    # 4. Social Science
    ("Social Science", "Nationalism in India", "The Salt Satyagraha and Dandi March", "10"),
    ("Social Science", "Federalism", "Constitutional Power Sharing", "10"),
    ("Social Science", "Drainage", "Peninsular River Systems", "9"),
    
    # 5. Languages
    ("English", "First Flight: Nelson Mandela", "Twin Obligations", "10"),
    ("Hindi", "Vasant: Vyakaran", "Sangya ke Bhed", "8"),
    
    # 6. Computer Science & AI
    ("Computer Applications", "Python Programming", "Lists and Dictionaries", "10"),
    ("Computer Science", "Data Structures", "Linear and Binary Search", "11"),
    
    # 7. Senior Commerce & Sanskrit
    ("Accountancy", "Introduction to Accounting", "Double Entry Accounting System", "11"),
    ("Sanskrit", "Ruchira: Vyakaran", "Sandhi Prakaran", "8")
]

print("=== STARTING 23-TOPIC CURRICULUM GENERATOR RIGOROUS AUDIT ===")
all_passed = True
total_questions = 0

for subject, chapter, topic, class_lvl in test_cases:
    qs = generate_topic_questions(
        topic_id=1,
        topic_name=topic,
        chapter_name=chapter,
        subject_name=subject,
        class_level=class_lvl,
        difficulty="Medium",
        count=5
    )
    for q in qs:
        total_questions += 1
        prompt, opts, correct_idx, exp, q_diff = q
        ans = opts[correct_idx]
        
        # Check 1: No generic placeholders
        if "central concept of" in prompt.lower() or "standard definition of" in prompt.lower():
            print(f"❌ GENERIC TEMPLATE FOUND: [{subject} - Cl {class_lvl} - {chapter} -> {topic}]")
            print(f"   Prompt: {prompt}")
            all_passed = False
            break
            
        # Check 2: Validation
        is_valid = validate_question_topic(prompt, topic, chapter, subject, class_lvl)
        if not is_valid:
            print(f"❌ INVALID TOPIC MATCH: [{subject} - Cl {class_lvl} - {chapter} -> {topic}]")
            print(f"   Prompt: {prompt}")
            all_passed = False
            break

if all_passed:
    print(f"✅ ALL {total_questions} GENERATED QUESTIONS PASSED AUDIT WITH 100% TOPIC ACCURACY & ZERO GENERIC TEMPLATES!")
else:
    print("❌ SOME QUESTIONS FAILED AUDIT. SEE ABOVE.")
