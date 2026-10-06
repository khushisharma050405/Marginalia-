"""Authentic NCERT, CBSE & ICSE Curriculum Practice Question Generator
Covers all grade levels: Foundation (Nursery/LKG/UKG), Primary (1-5), Middle School (6-8), Secondary (9-10), and Senior Secondary (11-12 Streams).
Generates strictly topic-matched questions with grade-accurate vocabulary, numbers, and conceptual difficulty (Easy, Medium, Hard).
Enforces zero cross-grade leakage: elementary word problems are strictly barred from middle/high school topics.
"""

import random
import re

def format_indian_num(n: int) -> str:
    s = str(n)
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rem = s[:-3]
    chunks = []
    while len(rem) > 2:
        chunks.append(rem[-2:])
        rem = rem[:-2]
    if rem:
        chunks.append(rem)
    chunks.reverse()
    return ",".join(chunks) + "," + last3


def validate_question_topic(prompt: str, topic_name: str, chapter_name: str, subject_name: str, class_level: str) -> bool:
    """Strictly validates whether a generated or stored question prompt belongs to the assigned curriculum topic.
    Returns True if valid, False if mismatched.
    """
    if not prompt or not topic_name:
        return True

    p_low = prompt.lower()
    t_low = (topic_name or "").lower()
    ch_low = (chapter_name or "").lower()
    s_low = (subject_name or "").lower()
    c_str = str(class_level).strip()

    # Rule 0: Foundation Grade Protection (Nursery, LKG, UKG, Class 1-2)
    if c_str in ("Nursery", "LKG", "UKG", "1", "2"):
        advanced_red_flags = [
            "adverb", "passive voice", "synonym of", "antonym of the word", "constitution",
            "quadratic", "photosynthesis", "mitochondria", "ohm's law", "linear equation",
            "panchayati raj", "dandi march", "amendment", "universal adult franchise"
        ]
        if any(flag in p_low for flag in advanced_red_flags):
            return False

    # Rule 1: CRITICAL - Purge elementary addition word problems from Grade 6 and above
    try:
        grade_num = int(re.sub(r"[^\d]", "", c_str) or "0")
    except Exception:
        grade_num = 0

    if grade_num >= 6 or c_str in ("11", "12", "11_Science", "12_Science", "11_Commerce", "12_Commerce", "11_Humanities", "12_Humanities"):
        elementary_red_flags = [
            "library received", "hindi books this month", "english books and",
            "caught on both days", "fisherman caught", "boat travels 20 km",
            "chocolates did she have", "pencils are in each box", "how many books did the library receive"
        ]
        if any(flag in p_low for flag in elementary_red_flags):
            return False

    # Rule 2: Mathematics - Class 8 Rational Numbers Properties
    if any(k in s_low for k in ["math", "algebra", "arithmetic"]) and ("rational" in ch_low or "rational" in t_low):
        if "closure" in t_low or "commutativ" in t_low or "associativ" in t_low or "distributiv" in t_low:
            valid_keywords = ["closure", "commutative", "associative", "distributive", "property", "rational", "closed under", "identity", "inverse", "+", "×", "/", "-", "multiplication", "addition"]
            if not any(k in p_low for k in valid_keywords):
                return False
            # Disallow unrelated questions
            if any(k in p_low for k in ["triangle", "quadrilateral", "speed of", "boat", "km/h", "cylinder", "probability"]):
                return False

        if "identity" in t_low or "inverse" in t_low:
            if not any(k in p_low for k in ["additive", "multiplicative", "identity", "inverse", "reciprocal", "0", "1", "/"]):
                return False

    # Rule 3: Mathematics - Class 8 Direct and Inverse Proportions
    if any(k in s_low for k in ["math", "algebra", "arithmetic"]) and ("proportion" in ch_low or "proportion" in t_low):
        valid_prop = ["proportion", "variation", "inversely", "directly", "workers", "days", "speed", "unitary", "hours", "ratio", "constant", "job", "complete", "cost of", "petrol", "trench", "taps", "pipes"]
        if not any(k in p_low for k in valid_prop):
            return False
        if any(k in p_low for k in ["quadrilateral", "cylinder", "photosynthesis", "cell", "respiration", "roots of"]):
            return False

    # Rule 4: Mathematics - Linear Equations
    if any(k in s_low for k in ["math", "algebra", "arithmetic"]) and ("linear equation" in ch_low or "equation" in t_low):
        valid_linear = [
            "solve", "equation", "variable", "value of x", "x =", "find x", "root", "+", "-", "=",
            "find its length", "perimeter", "ratio", "differ by", "numbers are in the ratio",
            "consecutive integers", "linear", "breadth", "dimensions", "width"
        ]
        if not any(k in p_low for k in valid_linear):
            return False

    # Rule 5: Mathematics - Quadrilaterals & Geometry
    if any(k in s_low for k in ["math", "geometry"]) and ("quadrilateral" in ch_low or "polygon" in t_low or "parallelogram" in t_low):
        valid_quad = [
            "quadrilateral", "polygon", "parallelogram", "rhombus", "rectangle", "square",
            "kite", "trapezium", "angle", "diagonal", "interior", "exterior", "degree", "°",
            "convex", "concave", "sides", "vertices", "adjacent", "opposite"
        ]
        if not any(k in p_low for k in valid_quad):
            return False

    # Rule 6: Science vs Mathematics cross-leakage
    if ("science" in s_low or "physics" in s_low or "chem" in s_low or "bio" in s_low) and not any(k in s_low for k in ["social", "sst", "computer"]):
        if any(k in p_low for k in ["solve for x", "quadratic equation", "x^2", "lcm of", "hcf of", "factorise", "rational number"]):
            return False

    # Rule 7: English vs Math/Science cross-leakage
    if "english" in s_low:
        if any(k in p_low for k in ["calculate", "solve", "km/h", "speed", "photosynthesis", "quadratic", "resistor"]):
            return False

    # Rule 8: Hindi vs English cross-leakage
    if "hindi" in s_low:
        if not re.search(r"[\u0900-\u097F]", prompt):
            return False

    # Rule 9: Science and CS Intra-Domain Coherence
    context = ch_low + " " + t_low
    # 9A. Electricity / Circuits in non-electrical topics
    if any(k in p_low for k in ["ohm's law", "resistor", "resistance", "electric current", "voltage"]):
        if not any(k in context for k in ["electric", "current", "circuit", "potential", "resistor", "resistance", "electricity", "conductor"]):
            return False

    # 9B. Cell / Biology in non-biological topics
    if any(k in p_low for k in ["mitochondria", "powerhouse of the cell", "chlorophyll", "chloroplast", "rbc", "wbc", "photosynthesis"]):
        if not any(k in context for k in ["cell", "tissue", "life process", "biology", "plant", "living", "reproduction", "organism", "evs"]):
            return False

    # 9C. Optics / Mirror / Lens in non-optics topics
    if any(k in p_low for k in ["mirror formula", "hypermetropia", "myopia", "concave lens", "convex lens", "refraction of light"]):
        if not any(k in context for k in ["light", "optics", "eye", "lens", "mirror", "reflection", "refraction"]):
            return False

    # 9D. CS Search/Sort vs AI metrics
    if any(k in p_low for k in ["domains of artificial intelligence", "precision", "recall", "f1 score"]):
        if any(k in context for k in ["search", "sort", "stack", "queue", "loop", "string", "tuple", "list", "array"]):
            return False

    return True


# -----------------------------------------------------------------------------
# HIGH-PRECISION CURRICULUM QUESTION POOLS & PROCEDURAL TEMPLATES
# -----------------------------------------------------------------------------

def gen_rational_numbers_q(topic_name: str, difficulty: str):
    t_low = topic_name.lower()

    if "closure" in t_low or "commutativ" in t_low or "associativ" in t_low or "distributiv" in t_low:
        items = [
            (
                "Which of the following operations is NOT closed for rational numbers?",
                "Division (due to division by zero)",
                ["Addition", "Subtraction", "Multiplication"],
                "Division by zero is undefined, so the set of rational numbers is not closed under division.",
                "Easy"
            ),
            (
                "Which property is expressed by the statement: (a/b) + (c/d) = (c/d) + (a/b)?",
                "Commutative property of addition",
                ["Associative property of addition", "Distributive property", "Closure property"],
                "Changing the order of terms in addition without changing the sum demonstrates the Commutative Property.",
                "Easy"
            ),
            (
                "Evaluate using the distributive property: (7/5) × (-3/12) + (7/5) × (5/12)",
                "7/30",
                ["7/12", "-7/30", "1/6"],
                "Using a(b + c) = (7/5) × [(-3/12) + (5/12)] = (7/5) × (2/12) = (7/5) × (1/6) = 7/30.",
                "Medium"
            ),
            (
                "Is subtraction of rational numbers commutative? (i.e. is a - b = b - a always true?)",
                "No, subtraction is never commutative for distinct rational numbers",
                ["Yes, subtraction is always commutative", "Only for positive rational numbers", "Only for integer numerators"],
                "For example, 1/2 - 1/3 = 1/6, whereas 1/3 - 1/2 = -1/6. Since 1/6 ≠ -1/6, subtraction is not commutative.",
                "Easy"
            ),
            (
                "Which property states that a × (b + c) = a × b + a × c for all rational numbers a, b, c?",
                "Distributive property of multiplication over addition",
                ["Associative property of multiplication", "Commutative property of addition", "Identity property"],
                "Distributing multiplication across addition terms is known as the Distributive Property.",
                "Easy"
            ),
            (
                "The statement [(-2/3) + (3/5)] + (-5/6) = (-2/3) + [(3/5) + (-5/6)] demonstrates which property?",
                "Associative property of addition",
                ["Commutative property of addition", "Distributive property", "Closure property"],
                "Grouping terms differently in addition without altering the sum demonstrates the Associative Property.",
                "Medium"
            ),
            (
                "Calculate using the distributive property: (-3/4) × (2/3) + (-3/4) × (-7/6)",
                "3/8",
                ["-3/8", "9/8", "-1/2"],
                "(-3/4) × [2/3 - 7/6] = (-3/4) × [4/6 - 7/6] = (-3/4) × (-3/6) = (-3/4) × (-1/2) = 3/8.",
                "Hard"
            ),
            (
                "Which of the following is true regarding rational numbers?",
                "Rational numbers are closed under addition, subtraction, and multiplication",
                ["Rational numbers are closed under all four operations", "Rational numbers are not closed under subtraction", "Rational numbers are not closed under multiplication"],
                "The result of adding, subtracting, or multiplying two rational numbers is always a rational number.",
                "Medium"
            ),
            (
                "If x = -1/2, y = 2/3, and z = -3/4, which identity verifies associativity under multiplication?",
                "(x × y) × z = x × (y × z)",
                ["x × (y + z) = x × y + x × z", "x + y = y + x", "x × y = y × x"],
                "Associativity of multiplication states that grouping factors in any order yields the same product: (x × y) × z = x × (y × z).",
                "Medium"
            ),
            (
                "Using distributivity, find: (9/16 × 4/12) + (9/16 × -3/9)",
                "0",
                ["3/16", "-3/16", "1/16"],
                "4/12 = 1/3 and -3/9 = -1/3. So (9/16) × (1/3 - 1/3) = (9/16) × 0 = 0.",
                "Hard"
            )
        ]
        return random.choice(items)

    elif "identity" in t_low or "inverse" in t_low:
        items = [
            (
                "What is the additive inverse of -7/19?",
                "7/19",
                ["-19/7", "19/7", "-7/19"],
                "The additive inverse of a rational number a is -a, such that a + (-a) = 0. Thus, -(-7/19) = 7/19.",
                "Easy"
            ),
            (
                "What is the multiplicative inverse (reciprocal) of -13/19?",
                "-19/13",
                ["19/13", "13/19", "-13/19"],
                "The multiplicative inverse of a/b is b/a such that (a/b) × (b/a) = 1. Reciprocal of -13/19 is -19/13.",
                "Easy"
            ),
            (
                "What is the additive identity for rational numbers?",
                "0",
                ["1", "-1", "Does not exist"],
                "For any rational number a, a + 0 = 0 + a = a. Hence, 0 is the additive identity.",
                "Easy"
            ),
            (
                "What is the multiplicative identity for rational numbers?",
                "1",
                ["0", "-1", "Infinity"],
                "For any rational number a, a × 1 = 1 × a = a. Hence, 1 is the multiplicative identity.",
                "Easy"
            ),
            (
                "Which rational number does NOT have a multiplicative inverse (reciprocal)?",
                "0",
                ["1", "-1", "1/2"],
                "Division by zero is undefined, so 0 has no reciprocal.",
                "Easy"
            ),
            (
                "What is the multiplicative inverse of the product: (-5/8) × (-3/7)?",
                "56/15",
                ["15/56", "-56/15", "-15/56"],
                "(-5/8) × (-3/7) = 15/56. The reciprocal of 15/56 is 56/15.",
                "Medium"
            ),
            (
                "If the sum of a rational number and its additive inverse is multiplied by its multiplicative inverse, what is the result?",
                "0",
                ["1", "-1", "Undefined"],
                "A rational number plus its additive inverse is 0. 0 multiplied by any defined number is 0.",
                "Medium"
            )
        ]
        return random.choice(items)

    else: # Rational numbers between two numbers
        items = [
            (
                "How many rational numbers exist between any two distinct rational numbers?",
                "Infinitely many",
                ["Only 1", "Exactly 10", "A finite countable number"],
                "Between any two rational numbers, there are infinitely many rational numbers (density property).",
                "Easy"
            ),
            (
                "Find a rational number exactly halfway between 1/4 and 1/2:",
                "3/8",
                ["2/6", "5/8", "1/3"],
                "Mean = (1/4 + 1/2) / 2 = (1/4 + 2/4) / 2 = (3/4) / 2 = 3/8.",
                "Medium"
            ),
            (
                "Which of the following rational numbers lies strictly between -2/5 and 1/2?",
                "0",
                ["-3/5", "3/4", "-1"],
                "Converting to decimals: -2/5 = -0.4 and 1/2 = 0.5. 0 lies between -0.4 and 0.5.",
                "Medium"
            ),
            (
                "Find three rational numbers between -3/2 and 5/3:",
                "-1/2, 0, 1/2",
                ["-2, -3, -4", "2, 3, 4", "-5/2, -6/2, -7/2"],
                "-3/2 = -1.5 and 5/3 ≈ 1.67. The values -1/2 (-0.5), 0, and 1/2 (0.5) lie strictly between them.",
                "Hard"
            )
        ]
        return random.choice(items)


def gen_proportions_q(topic_name: str, difficulty: str):
    t_low = topic_name.lower()

    if "inverse" in t_low or "work" in t_low:
        pairs = [
            (12, 15, 20, 9, "workers", "days"),
            (15, 8, 20, 6, "workers", "hours"),
            (6, 12, 9, 8, "pipes", "hours"),
            (8, 25, 20, 10, "workers", "days"),
            (10, 6, 15, 4, "machines", "days"),
            (60, 4, 80, 3, "km/h speed", "hours"),
            (45, 6, 90, 3, "km/h speed", "hours"),
            (50, 30, 75, 20, "students", "days"),
            (16, 15, 24, 10, "men", "days"),
            (30, 12, 40, 9, "laborers", "days"),
            (5, 36, 9, 20, "taps", "hours"),
            (4, 45, 6, 30, "pumps", "minutes"),
            (25, 16, 20, 20, "painters", "days"),
            (18, 10, 15, 12, "masons", "days")
        ]
        w1, t1, w2, t2, unit_w, unit_t = random.choice(pairs)
        prompt = f"If {w1} {unit_w} can complete a job in {t1} {unit_t}, how many {unit_t} will {w2} {unit_w} take to complete the same job?"
        ans = f"{t2} {unit_t}"
        dist = [f"{t2 + 3} {unit_t}", f"{t2 - 2 if t2 > 2 else t2 + 5} {unit_t}", f"{int(round((w1*t1)/float(w2-1 if w2>1 else 2)))} {unit_t}"]
        exp = (
            f"The number of {unit_w} and {unit_t} are in inverse proportion (w₁ × t₁ = w₂ × t₂).\n"
            f"{w1} × {t1} = {w2} × t₂\n"
            f"{w1 * t1} = {w2} × t₂\n"
            f"t₂ = {w1 * t1} / {w2} = {t2} {unit_t}."
        )
        return prompt, ans, dist, exp, difficulty or "Medium"

    else: # Direct proportion
        pairs = [
            (8, 240, 15, 450, "metres of cloth", "cost in ₹"),
            (5, 2500, 12, 6000, "workers' daily wages", "wages in ₹"),
            (4, 60, 10, 150, "litres of petrol", "distance in km"),
            (6, 42, 11, 77, "notebooks", "cost in ₹"),
            (3, 180, 7, 420, "hours of travel", "distance in km"),
            (12, 108, 20, 180, "kg of sugar", "cost in ₹"),
            (5, 75, 8, 120, "pens", "cost in ₹"),
            (9, 360, 14, 560, "books", "cost in ₹"),
            (2, 50, 7, 175, "kg of apples", "cost in ₹"),
            (15, 45, 25, 75, "envelopes", "cost in ₹"),
            (20, 100, 35, 175, "sheets of paper", "weight in grams"),
            (10, 80, 16, 128, "litres of milk", "cost in ₹"),
            (7, 350, 12, 600, "tickets", "fare in ₹"),
            (4, 32, 9, 72, "cups of flour", "number of cakes"),
            (8, 96, 13, 156, "hours of machine work", "units produced")
        ]
        x1, y1, x2, y2, item1, item2 = random.choice(pairs)
        prompt = f"If {x1} {item1} corresponds to {y1} {item2}, what will {x2} {item1} correspond to under direct proportion?"
        ans = f"{y2}"
        dist = [f"{y2 + 30}", f"{y2 - 25 if y2 > 25 else y2 + 50}", f"{y2 + 100}"]
        exp = (
            f"Since the quantities vary directly, x₁ / y₁ = x₂ / y₂ (or unitary method: value per unit = {y1}/{x1} = {y1//x1}).\n"
            f"For {x2} units: {x2} × {y1//x1} = {y2}."
        )
        return prompt, ans, dist, exp, difficulty or "Medium"


def gen_linear_equations_q(topic_name: str, difficulty: str):
    items = [
        (
            "Solve the linear equation for x: 3x + 15 = 42",
            "x = 9",
            ["x = 7", "x = 11", "x = 8"],
            "3x = 42 - 15 => 3x = 27 => x = 27 / 3 = 9.",
            "Easy"
        ),
        (
            "Solve for x: 5x + 9 = 5 + 3x",
            "x = -2",
            ["x = 2", "x = -4", "x = 4"],
            "5x - 3x = 5 - 9 => 2x = -4 => x = -2.",
            "Medium"
        ),
        (
            "Solve the equation with variable on both sides: 8x + 4 = 3(x - 1) + 7",
            "x = 0",
            ["x = 1", "x = -1", "x = 2"],
            "8x + 4 = 3x - 3 + 7 => 8x + 4 = 3x + 4 => 8x - 3x = 4 - 4 => 5x = 0 => x = 0.",
            "Medium"
        ),
        (
            "The perimeter of a rectangle is 13 cm and its width is 11/4 cm. Find its length (l):",
            "15/4 cm (3 3/4 cm)",
            ["13/4 cm", "17/4 cm", "7/2 cm"],
            "Perimeter = 2(l + w) => 13 = 2(l + 11/4) => 13/2 = l + 11/4 => l = 26/4 - 11/4 = 15/4 cm.",
            "Hard"
        ),
        (
            "Two numbers are in the ratio 5:3. If they differ by 18, what are the numbers?",
            "45 and 27",
            ["50 and 32", "40 and 22", "35 and 17"],
            "Let the numbers be 5x and 3x. 5x - 3x = 18 => 2x = 18 => x = 9. Numbers are 5(9)=45 and 3(9)=27.",
            "Medium"
        ),
        (
            "Solve the equation: 3x = 2x + 18",
            "x = 18",
            ["x = 9", "x = 36", "x = 6"],
            "Transposing 2x to LHS: 3x - 2x = 18 => x = 18.",
            "Easy"
        ),
        (
            "Solve: 5t - 3 = 3t - 5",
            "t = -1",
            ["t = 1", "t = -2", "t = 2"],
            "5t - 3t = -5 + 3 => 2t = -2 => t = -1.",
            "Easy"
        ),
        (
            "Solve: 4z + 3 = 6 + 2z",
            "z = 3/2",
            ["z = 2", "z = 1/2", "z = 3"],
            "4z - 2z = 6 - 3 => 2z = 3 => z = 3/2.",
            "Medium"
        ),
        (
            "The ages of Hari and Harry are in the ratio 5:7. Four years from now the ratio of their ages will be 3:4. Find Hari's present age:",
            "20 years",
            ["28 years", "15 years", "25 years"],
            "Let ages be 5x and 7x. (5x + 4)/(7x + 4) = 3/4 => 4(5x + 4) = 3(7x + 4) => 20x + 16 = 21x + 12 => x = 4. Hari = 5(4) = 20 years.",
            "Hard"
        ),
        (
            "Solve for x: (x + 1) / (2x + 3) = 3/8",
            "x = 1/2",
            ["x = 2", "x = 1", "x = -1/2"],
            "Cross-multiplying: 8(x + 1) = 3(2x + 3) => 8x + 8 = 6x + 9 => 2x = 1 => x = 1/2.",
            "Medium"
        )
    ]
    return random.choice(items)


def gen_quadrilaterals_q(topic_name: str, difficulty: str):
    items = [
        (
            "What is the sum of interior angles of a convex polygon with n sides?",
            "(n - 2) × 180°",
            ["(n - 1) × 180°", "n × 180°", "(n - 2) × 360°"],
            "According to the angle sum property of polygons, the sum of interior angles is (n - 2) × 180°.",
            "Easy"
        ),
        (
            "What is the sum of the measures of the exterior angles of any convex polygon?",
            "360°",
            ["180°", "540°", "Depends on number of sides"],
            "The sum of the exterior angles of any convex polygon is always constant at 360°.",
            "Easy"
        ),
        (
            "In a parallelogram ABCD, if ∠A = 70°, what is the measure of adjacent angle ∠B?",
            "110°",
            ["70°", "90°", "120°"],
            "Adjacent angles of a parallelogram are supplementary: ∠A + ∠B = 180° => ∠B = 180° - 70° = 110°.",
            "Easy"
        ),
        (
            "Which quadrilateral has all four sides equal and diagonals that bisect each other at right angles (90°)?",
            "Rhombus",
            ["Rectangle", "Trapezium", "Kite"],
            "A rhombus has all four sides equal, and its diagonals are perpendicular bisectors of each other.",
            "Medium"
        ),
        (
            "A regular polygon has each exterior angle equal to 45°. How many sides does it have?",
            "8 sides (Octagon)",
            ["6 sides", "10 sides", "12 sides"],
            "Number of sides n = 360° / (each exterior angle) = 360° / 45° = 8 sides.",
            "Medium"
        ),
        (
            "The angles of a quadrilateral are in the ratio 3:5:9:13. Find the smallest angle:",
            "36°",
            ["45°", "30°", "60°"],
            "Sum of ratio parts = 3 + 5 + 9 + 13 = 30. Total angles = 360°. 1 part = 360°/30 = 12°. Smallest angle = 3 × 12° = 36°.",
            "Medium"
        ),
        (
            "How many diagonals does a convex hexagon (6 sides) have?",
            "9 diagonals",
            ["6 diagonals", "12 diagonals", "15 diagonals"],
            "Formula for diagonals: n(n - 3) / 2 = 6(3) / 2 = 9 diagonals.",
            "Medium"
        ),
        (
            "Which geometric property distinguishes a square from a general rhombus?",
            "All four interior angles are 90° (right angles)",
            ["All four sides are equal", "Diagonals are perpendicular", "Opposite angles are equal"],
            "Both shapes have four equal sides and perpendicular diagonals, but a square additionally has four right angles.",
            "Easy"
        ),
        (
            "What is the minimum interior angle possible for a regular polygon?",
            "60° (Equilateral Triangle)",
            ["45°", "90°", "30°"],
            "The regular polygon with the fewest sides is an equilateral triangle (3 sides), having interior angles of 180° / 3 = 60°.",
            "Easy"
        ),
        (
            "Which quadrilateral has exactly one pair of parallel opposite sides?",
            "Trapezium",
            ["Parallelogram", "Rhombus", "Kite"],
            "By definition, a trapezium has at least/exactly one pair of parallel sides.",
            "Easy"
        )
    ]
    return random.choice(items)


def gen_squares_roots_q(topic_name: str, difficulty: str):
    items = [
        (
            "Which of the following cannot be the unit digit of a perfect square number?",
            "2, 3, 7, or 8",
            ["0, 1, 4", "5 or 6", "9"],
            "Square numbers can only end in 0, 1, 4, 5, 6, or 9 in the units place. They never end in 2, 3, 7, or 8.",
            "Easy"
        ),
        (
            "What is the Pythagorean triplet whose smallest member is 6?",
            "6, 8, 10",
            ["6, 7, 8", "6, 9, 12", "6, 12, 14"],
            "For member 2m = 6 => m = 3. The other members are m² - 1 = 8 and m² + 1 = 10. Triplet is 6, 8, 10.",
            "Medium"
        ),
        (
            "What is the square root of 7056 using prime factorisation?",
            "84",
            ["74", "86", "94"],
            "7056 = 2⁴ × 3² × 7² => √7056 = 2² × 3 × 7 = 4 × 21 = 84.",
            "Medium"
        ),
        (
            "What is the smallest number by which 180 must be multiplied so that the product becomes a perfect square?",
            "5",
            ["2", "3", "7"],
            "180 = 2² × 3² × 5. To make it a square, 5 needs a pair, so multiply by 5 (180 × 5 = 900 = 30²).",
            "Hard"
        )
    ]
    return random.choice(items)


def gen_comparing_quantities_q(topic_name: str, difficulty: str):
    items = [
        (
            "A table marked at ₹15,000 is sold for ₹12,000. What is the discount percentage?",
            "20%",
            ["15%", "25%", "30%"],
            "Discount = MP - SP = 15000 - 12000 = ₹3000. Discount % = (3000 / 15000) × 100 = 20%.",
            "Medium"
        ),
        (
            "Calculate the compound interest on ₹10,000 for 2 years at 10% per annum compounded annually:",
            "₹2,100",
            ["₹2,000", "₹2,200", "₹1,100"],
            "A = P(1 + R/100)ⁿ = 10000(1.10)² = 10000 × 1.21 = ₹12,100. CI = A - P = 12100 - 10000 = ₹2,100.",
            "Medium"
        ),
        (
            "An article was purchased for ₹1,239 including GST of 18%. Find the price of the article before GST was added:",
            "₹1,050",
            ["₹1,000", "₹1,100", "₹1,020"],
            "Price × 1.18 = 1239 => Price = 1239 / 1.18 = ₹1,050.",
            "Hard"
        )
    ]
    return random.choice(items)


def gen_mensuration_q(topic_name: str, difficulty: str):
    items = [
        (
            "What is the formula for the area of a trapezium with parallel sides 'a' and 'b' and height 'h'?",
            "Area = 1/2 × (a + b) × h",
            ["Area = (a + b) × h", "Area = 1/2 × a × b × h", "Area = a × b × h"],
            "Area of a trapezium is half the sum of parallel sides multiplied by the perpendicular distance between them.",
            "Easy"
        ),
        (
            "The area of a trapezium is 34 cm² and the length of one parallel side is 10 cm and its height is 4 cm. Find the other parallel side:",
            "7 cm",
            ["6 cm", "8 cm", "9 cm"],
            "34 = 1/2 × (10 + b) × 4 => 34 = 2(10 + b) => 17 = 10 + b => b = 7 cm.",
            "Medium"
        ),
        (
            "Find the total surface area of a cylinder with radius r = 7 cm and height h = 10 cm (Take π = 22/7):",
            "748 cm²",
            ["440 cm²", "616 cm²", "850 cm²"],
            "TSA = 2πr(r + h) = 2 × (22/7) × 7 × (7 + 10) = 44 × 17 = 748 cm².",
            "Medium"
        ),
        (
            "What is the volume of a cuboid of dimensions 8 cm × 5 cm × 4 cm?",
            "160 cm³",
            ["80 cm³", "140 cm³", "180 cm³"],
            "Volume = length × breadth × height = 8 × 5 × 4 = 160 cm³.",
            "Easy"
        )
    ]
    return random.choice(items)


def gen_exponents_q(topic_name: str, difficulty: str):
    items = [
        (
            "What is the value of 3⁻²?",
            "1/9",
            ["-9", "-6", "9"],
            "Using the law a⁻ᵐ = 1/aᵐ, 3⁻² = 1/(3²) = 1/9.",
            "Easy"
        ),
        (
            "Simplify: (2⁻¹ × 4⁻¹) ÷ 2⁻²",
            "1/2",
            ["1/4", "1", "2"],
            "(1/2 × 1/4) ÷ (1/4) = (1/8) × 4 = 1/2.",
            "Medium"
        ),
        (
            "Express the number 0.000007 in standard scientific notation:",
            "7 × 10⁻⁶",
            ["7 × 10⁻⁵", "0.7 × 10⁻⁵", "7 × 10⁻⁷"],
            "Moving the decimal point 6 places to the right gives 7 × 10⁻⁶.",
            "Easy"
        )
    ]
    return random.choice(items)


# -----------------------------------------------------------------------------
# TRUE / FALSE QUESTION GENERATOR
# -----------------------------------------------------------------------------

def gen_curriculum_tf_question(topic_name: str, chapter_name: str, subject_name: str, class_level: str, difficulty: str = "Medium"):
    low_t = (topic_name or "").lower()
    low_ch = (chapter_name or "").lower()
    low_s = (subject_name or "").lower()

    tf_pool = []

    # 1. Computer Science & AI
    if any(k in low_s for k in ["computer", "ai", "artificial", "it", "python", "computational"]):
        tf_pool.extend([
            ("State True or False: In computational thinking, decomposition refers to breaking down a complex problem into smaller, manageable parts.", "True", ["False"], "True. Decomposition divides complex systems or challenges into smaller sub-components for easier problem solving.", "Easy"),
            ("State True or False: In Python, a tuple is mutable and elements can be re-assigned after initialization.", "False", ["True"], "False. Tuples are immutable sequence types in Python; attempting item assignment raises a TypeError.", "Easy"),
            ("State True or False: In standard flowcharts, a diamond symbol represents a decision or conditional test branching.", "True", ["False"], "True. Diamond symbols denote conditional operations (e.g. Yes/No, True/False).", "Easy"),
            ("State True or False: The three primary technical domains of AI are Data Science, Computer Vision, and Natural Language Processing.", "True", ["False"], "True. AI applications are categorized into Data Science, Computer Vision (CV), and NLP.", "Easy"),
            ("State True or False: The 4Ws Problem Canvas in AI project scoping stands for Who, What, Where, and Why.", "True", ["False"], "True. The 4Ws canvas systematically frames problem stakeholders, context, and impact.", "Easy"),
            ("State True or False: Binary search can be executed directly on an unsorted array without prior sorting.", "False", ["True"], "False. Binary search strictly requires the sequence of elements to be sorted monotonically.", "Medium"),
            ("State True or False: In computing, exactly 8 bits make up one byte.", "True", ["False"], "True. One byte is universally defined as a collection of 8 bits.", "Easy"),
            ("State True or False: An HC-SR04 ultrasonic sensor measures distance by calculating the time-of-flight of high-frequency sound waves.", "True", ["False"], "True. Ultrasonic sensors calculate distance = (time × speed of sound) / 2.", "Medium")
        ])

    # 2. Science (Physics, Chemistry, Biology, EVS)
    elif any(k in low_s for k in ["science", "physics", "chem", "bio", "evs", "environment"]):
        tf_pool.extend([
            ("State True or False: Mitochondria are known as the powerhouse of the cell because they synthesize ATP.", "True", ["False"], "True. Mitochondria produce cellular energy through aerobic respiration.", "Easy"),
            ("State True or False: Blue litmus paper turns red when introduced into an acidic solution.", "True", ["False"], "True. Acids turn blue litmus red, whereas bases turn red litmus blue.", "Easy"),
            ("State True or False: According to the Law of Conservation of Mass, matter can be created and destroyed during chemical reactions.", "False", ["True"], "False. Mass can neither be created nor destroyed in a chemical reaction; total mass is conserved.", "Easy"),
            ("State True or False: The SI unit of force is the Newton (N).", "True", ["False"], "True. Force is measured in Newtons (N) where 1 N = 1 kg·m/s².", "Easy"),
            ("State True or False: Sound waves can propagate through a complete physical vacuum.", "False", ["True"], "False. Sound requires a mechanical material medium (solid, liquid, or gas) to travel.", "Easy"),
            ("State True or False: Photosynthesis in green plants takes place inside chloroplasts containing chlorophyll.", "True", ["False"], "True. Chloroplasts contain chlorophyll pigments that absorb photon energy from sunlight.", "Easy"),
            ("State True or False: Pure distilled water at 25°C has a neutral pH of exactly 7.", "True", ["False"], "True. At 25°C, pure water has [H+] = [OH-] = 10^-7 M, corresponding to pH 7.", "Easy")
        ])

    # 3. Social Science
    elif any(k in low_s for k in ["social", "sst", "hist", "geo", "civic", "pol", "eco"]):
        tf_pool.extend([
            ("State True or False: Dr. B.R. Ambedkar was the Chairman of the Drafting Committee of the Constituent Assembly.", "True", ["False"], "True. Dr. B.R. Ambedkar served as the chief architect and Drafting Committee Chairman.", "Easy"),
            ("State True or False: Mahatma Gandhi inaugurated the Civil Disobedience Movement with the Dandi Salt March in 1930.", "True", ["False"], "True. The historic Dandi March occurred in March-April 1930.", "Easy"),
            ("State True or False: Under Universal Adult Franchise in India, the minimum voting age is 21 years.", "False", ["True"], "False. The 61st Constitutional Amendment Act reduced the voting age to 18 years.", "Easy"),
            ("State True or False: The Godavari is the longest river system in Peninsular India, often called 'Dakshin Ganga'.", "True", ["False"], "True. The Godavari river is the largest river in Peninsular India.", "Easy"),
            ("State True or False: The primary sector of the economy includes manufacturing factories and heavy industries.", "False", ["True"], "False. Manufacturing belongs to the Secondary sector; Primary sector extracts natural resources.", "Easy"),
            ("State True or False: Black soil is also called Regur soil and has high moisture retention ideal for cotton.", "True", ["False"], "True. Regur soil in the Deccan trap is clayey and ideal for cotton cultivation.", "Easy")
        ])

    # 4. English
    elif "english" in low_s:
        tf_pool.extend([
            ("State True or False: In the sentence 'The brave girl ran quickly', the word 'quickly' functions as an adverb.", "True", ["False"], "True. 'Quickly' modifies the verb 'ran', indicating manner of action.", "Easy"),
            ("State True or False: The words 'Ancient' and 'Modern' are synonyms.", "False", ["True"], "False. 'Ancient' and 'Modern' are direct antonyms (opposites).", "Easy"),
            ("State True or False: In Robert Frost's poem 'Dust of Snow', the crow shakes fine snow from a hemlock tree onto the poet.", "True", ["False"], "True. The unexpected snow from the hemlock tree lifts the poet's mood.", "Easy"),
            ("State True or False: The sentence 'A beautiful song was sung by her' is written in the passive voice.", "True", ["False"], "True. The grammatical subject receives the action performed by the agent.", "Easy")
        ])

    # 5. Hindi
    elif "hindi" in low_s:
        tf_pool.extend([
            ("बताइए सही या गलत: किसी व्यक्ति, वस्तु, स्थान या भाव के नाम को संज्ञा कहते हैं।", "True", ["False"], "सही। किसी भी व्यक्ति, प्राणी, स्थान या भाव के नाम को संज्ञा कहा जाता है।", "Easy"),
            ("बताइए सही या गलत: 'दिन' का विलोम शब्द 'प्रकाश' होता है।", "False", ["True"], "गलत। 'दिन' का विपरीत (विलोम) शब्द 'रात' होता है।", "Easy"),
            ("बताइए सही या गलत: 'आँखों का तारा' मुहावरे का अर्थ अत्यधिक प्यारा होना है।", "True", ["False"], "सही। 'आँखों का तारा' अत्यधिक प्रिय व्यक्ति के लिए प्रयुक्त होता है।", "Easy"),
            ("बताइए सही या गलत: 'सूर्योदय' शब्द गुण स्वर संधि का उदाहरण है।", "True", ["False"], "सही। सूर्य + उदय (अ + उ = ओ) गुण स्वर संधि का निर्माण करता है।", "Easy")
        ])

    # 6. Mathematics (Default / Math)
    else:
        tf_pool.extend([
            ("State True or False: The sum of all three interior angles in any triangle is always 180°.", "True", ["False"], "True. The angle sum property of any Euclidean triangle guarantees the total is 180°.", "Easy"),
            ("State True or False: The sum of all interior angles of any convex quadrilateral is 360°.", "True", ["False"], "True. Dividing a quadrilateral into two triangles gives 2 × 180° = 360°.", "Easy"),
            ("State True or False: In the Indian numeral system, 1 crore equals 100 lakhs.", "True", ["False"], "True. 1 Crore = 1,00,00,000 = 100 × 1,00,000 (100 lakhs).", "Easy"),
            ("State True or False: An angle measuring exactly 90 degrees is called an acute angle.", "False", ["True"], "False. An angle measuring exactly 90° is a right angle; acute angles are strictly less than 90°.", "Easy"),
            ("State True or False: Zero (0) is the additive identity for all rational numbers.", "True", ["False"], "True. For any rational number a, a + 0 = 0 + a = a.", "Easy"),
            ("State True or False: Rational numbers are closed under division by zero.", "False", ["True"], "False. Division by zero is undefined; rational numbers are not closed under division.", "Medium")
        ])

    valid_pool = [item for item in tf_pool if validate_question_topic(item[0], topic_name, chapter_name, subject_name, class_level)]
    if valid_pool:
        picked = random.choice(valid_pool)
        return picked[0], picked[1], picked[2], picked[3], picked[4]
    return None


# -----------------------------------------------------------------------------
# FILL IN THE BLANK QUESTION GENERATOR
# -----------------------------------------------------------------------------

def gen_curriculum_fib_question(topic_name: str, chapter_name: str, subject_name: str, class_level: str, difficulty: str = "Medium"):
    low_t = (topic_name or "").lower()
    low_ch = (chapter_name or "").lower()
    low_s = (subject_name or "").lower()

    fib_pool = []

    # 1. Computer Science & AI
    if any(k in low_s for k in ["computer", "ai", "artificial", "it", "python", "computational"]):
        fib_pool.extend([
            ("Fill in the blank: In computational thinking, breaking down a complex problem into smaller parts is called _____.", "Decomposition", ["Pattern Recognition", "Abstraction", "Algorithm Design"], "Decomposition divides complex problems into smaller, manageable sub-components.", "Easy"),
            ("Complete the statement: In Python, an immutable sequence defined with parentheses () is called a _____.", "Tuple", ["List", "Dictionary", "Set"], "Tuples are immutable sequences enclosed in parentheses ().", "Easy"),
            ("Fill in the blank: In flowcharts, a _____ symbol represents a decision or conditional test.", "diamond", ["rectangle", "oval", "parallelogram"], "A diamond represents a conditional test (True/False branching).", "Easy"),
            ("Complete the statement: The three core domains of AI are Data Science, Computer Vision, and _____.", "Natural Language Processing (NLP)", ["Robotics", "Web Development", "Cloud Architecture"], "Data Science, Computer Vision (CV), and NLP are the 3 technical domains of AI.", "Easy"),
            ("Fill in the blank: In the AI Project Cycle, the 4Ws Canvas stands for Who, What, Where, and _____.", "Why", ["When", "Which", "Whom"], "The 4Ws canvas addresses Who, What, Where, and Why.", "Easy"),
            ("Complete the statement: In computing, 8 bits make up one _____.", "byte", ["nibble", "kilobyte", "word"], "One byte is universally defined as a group of 8 bits.", "Easy")
        ])

    # 2. Science
    elif any(k in low_s for k in ["science", "physics", "chem", "bio", "evs", "environment"]):
        fib_pool.extend([
            ("Fill in the blank: The organelle known as the powerhouse of the cell is the _____.", "Mitochondria", ["Nucleus", "Ribosome", "Chloroplast"], "Mitochondria synthesize cellular energy (ATP) through respiration.", "Easy"),
            ("Complete the statement: The SI unit of electrical resistance is the _____.", "Ohm (Ω)", ["Ampere (A)", "Volt (V)", "Watt (W)"], "Electrical resistance is measured in Ohms (Ω) where V = IR.", "Easy"),
            ("Fill in the blank: Acids turn blue litmus paper _____.", "red", ["blue", "green", "yellow"], "Acids turn blue litmus red, whereas bases turn red litmus blue.", "Easy"),
            ("Complete the statement: Newton's First Law of Motion is also known as the Law of _____.", "Inertia", ["Gravitation", "Momentum", "Friction"], "Newton's First Law establishes the principle of inertia.", "Easy"),
            ("Fill in the blank: In plant leaves, the green pigment essential for photosynthesis is _____.", "Chlorophyll", ["Carotene", "Anthocyanin", "Hemoglobin"], "Chlorophyll absorbs photon energy from sunlight.", "Easy")
        ])

    # 3. Social Science
    elif any(k in low_s for k in ["social", "sst", "hist", "geo", "civic", "pol", "eco"]):
        fib_pool.extend([
            ("Fill in the blank: Dr. B.R. Ambedkar was the Chairman of the _____ Committee of the Constituent Assembly.", "Drafting", ["Advisory", "Union Powers", "Steering"], "Dr. Ambedkar chaired the Drafting Committee of the Indian Constitution.", "Easy"),
            ("Complete the statement: Mahatma Gandhi launched the historic Salt March to Dandi in the year _____.", "1930", ["1920", "1942", "1919"], "The Salt Satyagraha began in March 1930.", "Easy"),
            ("Fill in the blank: The minimum age required for Indian citizens to vote under Universal Adult Franchise is _____ years.", "18", ["21", "16", "25"], "The voting age was set to 18 by the 61st Amendment.", "Easy"),
            ("Complete the statement: The largest river system in Peninsular India is the _____ river.", "Godavari", ["Krishna", "Cauvery", "Narmada"], "The Godavari is known as Dakshin Ganga.", "Easy"),
            ("Fill in the blank: Agriculture, forestry, and fishing constitute the _____ sector of the economy.", "Primary", ["Secondary", "Tertiary", "Quaternary"], "The Primary sector extracts natural environmental resources.", "Easy")
        ])

    # 4. English
    elif "english" in low_s:
        fib_pool.extend([
            ("Fill in the blank: The antonym (opposite) of the word 'ANCIENT' is _____.", "Modern", ["Historic", "Antique", "Elderly"], "'Modern' is the direct antonym of ancient.", "Easy"),
            ("Complete the sentence: In 'The brave girl ran quickly', the word 'quickly' is an _____.", "adverb", ["adjective", "noun", "verb"], "'Quickly' describes manner of action, functioning as an adverb.", "Easy"),
            ("Fill in the blank: In Robert Frost's poem 'Dust of Snow', the crow shook snow from a _____ tree.", "hemlock", ["banyan", "pine", "oak"], "The poisonous hemlock tree is used symbolically by Robert Frost.", "Easy")
        ])

    # 5. Hindi
    elif "hindi" in low_s:
        fib_pool.extend([
            ("रिक्त स्थान की पूर्ति कीजिए: किसी व्यक्ति, वस्तु, स्थान या भाव के नाम को _____ कहते हैं।", "संज्ञा", ["सर्वनाम", "विशेषण", "क्रिया"], "किसी व्यक्ति, वस्तु या स्थान के नाम को संज्ञा कहते हैं।", "Easy"),
            ("रिक्त स्थान भरें: 'दिन' का विलोम शब्द _____ होता है।", "रात", ["सुबह", "शाम", "दोपहर"], "'दिन' का विलोम शब्द 'रात' होता है।", "Easy"),
            ("रिक्त स्थान भरें: 'आँखों का तारा' मुहावरे का अर्थ बहुत _____ होना है।", "प्यारा", ["गुस्सा", "चालाक", "अंधा"], "'आँखों का तारा' बहुत प्यारे व्यक्ति को कहते हैं।", "Easy")
        ])

    # 6. Mathematics (Default)
    else:
        fib_pool.extend([
            ("Fill in the blank: The sum of interior angles in any triangle is _____.", "180°", ["360°", "90°", "270°"], "The angle sum of any triangle is always 180°.", "Easy"),
            ("Fill in the blank: In the Indian place value system, 1 crore is equivalent to _____ lakhs.", "100", ["10", "1,000", "50"], "1 Crore = 100 Lakhs = 1,00,00,000.", "Easy"),
            ("Complete the statement: The additive identity for rational numbers is _____.", "0", ["1", "-1", "undefined"], "Adding 0 leaves any rational number unchanged: a + 0 = a.", "Easy"),
            ("Fill in the blank: An angle measuring strictly between 90° and 180° is called an _____ angle.", "obtuse", ["acute", "right", "reflex"], "An angle between 90° and 180° is an obtuse angle.", "Easy"),
            ("Complete the statement: The perimeter of a square with side length s is given by _____.", "4s", ["s²", "2s", "4 + s"], "Perimeter of square = 4 × side length.", "Easy")
        ])

    valid_pool = [item for item in fib_pool if validate_question_topic(item[0], topic_name, chapter_name, subject_name, class_level)]
    if valid_pool:
        picked = random.choice(valid_pool)
        return picked[0], picked[1], picked[2], picked[3], picked[4]
    return None


# -----------------------------------------------------------------------------
# MASTER TOPIC QUESTION GENERATOR
# -----------------------------------------------------------------------------

def generate_topic_questions(topic_id: int, topic_name: str, chapter_name: str, subject_name: str, class_level: str, difficulty: str = "Medium", count: int = 10):
    diff = difficulty.capitalize() if difficulty else "Medium"
    low_t = (topic_name or "").lower()
    low_ch = (chapter_name or "").lower()
    low_s = (subject_name or "").lower()
    c_str = str(class_level).strip()

    questions = []
    generated_prompts = set()

    for i in range(count * 6): # loop more to ensure unique questions
        if len(questions) >= count:
            break

        prompt, ans_str, dist, explanation, q_diff = None, None, None, None, diff

        # Balanced distribution: 1 True/False, 1 Fill-in-the-Blank, 1 MCQ
        target_mode = i % 3
        if target_mode == 1:
            res_tf = gen_curriculum_tf_question(topic_name, chapter_name, subject_name, class_level, diff)
            if res_tf and res_tf[0] not in generated_prompts:
                prompt, ans_str, dist, explanation, q_diff = res_tf
        elif target_mode == 2:
            res_fib = gen_curriculum_fib_question(topic_name, chapter_name, subject_name, class_level, diff)
            if res_fib and res_fib[0] not in generated_prompts:
                prompt, ans_str, dist, explanation, q_diff = res_fib

        # =========================================================================
        # 1. MATHEMATICS (Class-Stratified)
        # =========================================================================
        if prompt:
            pass
        elif "math" in low_s or "algebra" in low_s or "geom" in low_s:

            # --- Class 8 Math Topics ---
            if "rational" in low_ch or "rational" in low_t:
                res = gen_rational_numbers_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            elif "proportion" in low_ch or "proportion" in low_t or "unitary" in low_t or "variation" in low_t:
                res = gen_proportions_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            elif "linear equation" in low_ch or "equation" in low_t:
                res = gen_linear_equations_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            elif "quadrilateral" in low_ch or "polygon" in low_t or "parallelogram" in low_t:
                res = gen_quadrilaterals_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            elif "square" in low_ch or "square root" in low_t:
                res = gen_squares_roots_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            elif "compare" in low_ch or "discount" in low_t or "interest" in low_t or "gst" in low_t:
                res = gen_comparing_quantities_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            elif "mensuration" in low_ch or "trapezium" in low_t or "cylinder" in low_t:
                res = gen_mensuration_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            elif "exponent" in low_ch or "power" in low_t or "standard form" in low_t:
                res = gen_exponents_q(topic_name, diff)
                prompt, ans_str, dist, explanation, q_diff = res

            # --- Class 9 & 10 Math Topics ---
            elif "quadratic" in low_ch or "quadratic" in low_t:
                roots_bank = [(2, 3, "x² - 5x + 6 = 0"), (1, 4, "x² - 5x + 4 = 0"), (-2, 5, "x² - 3x - 10 = 0"), (3, 3, "x² - 6x + 9 = 0")]
                r1, r2, eq_str = random.choice(roots_bank)
                prompt = f"What are the roots of the quadratic equation {eq_str}?"
                ans_str = f"{r1} and {r2}" if r1 != r2 else f"Equal roots: {r1}"
                dist = [f"{-r1} and {-r2}", f"{r1 + 1} and {r2 - 1}", f"{r1 * 2} and {r2}"]
                explanation = f"Factorising {eq_str} gives (x - {r1})(x - {r2}) = 0. Hence, roots are {ans_str}."

            elif "trigonometr" in low_ch or "trig" in low_t:
                trig_items = [
                    ("What is the value of sin 30° + cos 60°?", "1", ["1/2", "√3", "0"], "sin 30° = 1/2 and cos 60° = 1/2. Their sum is 1/2 + 1/2 = 1."),
                    ("Which fundamental trigonometric identity is always true for an acute angle θ?", "sin² θ + cos² θ = 1", ["sin² θ - cos² θ = 1", "tan² θ + 1 = sin² θ", "sec² θ + tan² θ = 1"], "The Pythagorean trigonometric identity states that sin² θ + cos² θ = 1."),
                    ("If tan θ = 4/3, what is the value of sin θ?", "4/5", ["3/5", "5/4", "3/4"], "Opposite = 4, Adjacent = 3 => Hypotenuse = √(4² + 3²) = 5. Therefore, sin θ = Opposite/Hypotenuse = 4/5.")
                ]
                picked = random.choice(trig_items)
                prompt, ans_str, dist, explanation = picked

            elif "arithmetic progression" in low_ch or " ap " in (" " + low_ch + " "):
                a_val, d_val = random.choice([(2, 3), (5, 4), (7, 2), (10, 5)])
                prompt = f"In an Arithmetic Progression (AP) with first term a = {a_val} and common difference d = {d_val}, what is the 10th term (a₁₀)?"
                t10 = a_val + (10 - 1) * d_val
                ans_str = str(t10)
                dist = [str(t10 + d_val), str(t10 - d_val), str(t10 + 2)]
                explanation = f"aₙ = a + (n - 1)d => a₁₀ = {a_val} + 9 × {d_val} = {a_val} + {9 * d_val} = {t10}."

            # --- Class 5 & Primary Math Topics ---
            elif "fish tale" in low_ch or any(k in low_t for k in ["lakh", "crore", "large number", "speed = distance", "mini bank", "place value and comma"]):
                if "speed" in low_t or "distance" in low_t or "time" in low_t:
                    items = [
                        ("A motor boat travels at a uniform speed of 20 km/h. How far will it travel in 4 hours?", "80 km", ["60 km", "100 km", "24 km"], "Distance = Speed × Time = 20 km/h × 4 h = 80 km."),
                        ("A traditional log boat takes 3 hours to travel 12 km. What is the speed of the log boat?", "4 km/h", ["3 km/h", "5 km/h", "36 km/h"], "Speed = Distance / Time = 12 km / 3 h = 4 km/h."),
                        ("If a machine boat travels at 25 km/h, how many hours will it take to travel a distance of 100 km?", "4 hours", ["3 hours", "5 hours", "2.5 hours"], "Time = Distance / Speed = 100 km / 25 km/h = 4 hours.")
                    ]
                elif "bank" in low_t or "loan" in low_t:
                    items = [
                        ("Jhansi took a bank loan of ₹21,000 to buy a log boat. She pays back ₹2,000 every month for 1 year (12 months). How much total money did she pay back?", "₹24,000", ["₹21,000", "₹22,000", "₹26,000"], "Total repayment = 12 months × ₹2,000/month = ₹24,000 (Interest paid = ₹3,000)."),
                        ("Gracy took a loan of ₹4,000 to buy fishing nets. She paid back ₹345 every month for one year. What was her total repayment to the bank?", "₹4,140", ["₹4,000", "₹4,200", "₹3,900"], "Total paid = 12 × ₹345 = ₹4,140."),
                    ]
                elif "place value" in low_t or "comma" in low_t:
                    items = [
                        ("In the number 57,84,320, what is the place value of the digit 7?", "7,00,000 (Seven Lakhs)", ["70,000", "7,000", "70,00,000"], "7 is in the lakhs place, so its place value is 7 × 1,00,000 = 7,00,000."),
                        ("In the Indian place value system, where is the first comma placed when reading from right to left?", "After the first 3 digits (hundreds place)", ["After 2 digits", "After 4 digits", "After 5 digits"], "The Indian system groups the first 3 digits (ones, tens, hundreds), followed by periods of 2 digits (thousands, lakhs, crores)."),
                        ("How many lakhs make one crore in the Indian numeral system?", "100 lakhs", ["10 lakhs", "1,000 lakhs", "50 lakhs"], "1 Crore = 1,00,00,000 = 100 × 1,00,000 (100 lakhs).")
                    ]
                else:
                    items = [
                        ("How many zeros are there in 1 crore (1,00,00,000)?", "7 zeros", ["5 zeros", "6 zeros", "8 zeros"], "In the Indian system, 1 Lakh has 5 zeros (1,00,000) and 1 Crore has 7 zeros (1,00,00,000)."),
                        ("How many zeros are there in 1 lakh (1,00,000)?", "5 zeros", ["4 zeros", "6 zeros", "7 zeros"], "1 lakh is written as 1,00,000 with exactly 5 zeros."),
                        ("Which of the following represents 'Fifty Lakhs' in standard Indian numeral format?", "50,00,000", ["5,00,000", "500,000", "5,00,00,000"], "Fifty lakhs has 50 followed by five zeros: 50,00,000.")
                    ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif "shapes and angles" in low_ch or any(k in low_t for k in ["angle", "right angle", "acute", "obtuse", "clock angle"]):
                items = [
                    ("What is an angle measuring less than 90° called?", "Acute angle", ["Right angle", "Obtuse angle", "Straight angle"], "An angle between 0° and 90° is an acute angle."),
                    ("What is the measure of a right angle?", "90°", ["45°", "180°", "60°"], "A right angle measures exactly 90 degrees."),
                    ("What is an angle measuring greater than 90° but less than 180° called?", "Obtuse angle", ["Acute angle", "Right angle", "Reflex angle"], "An angle strictly between 90° and 180° is an obtuse angle."),
                    ("What angle do the hour and minute hands of a clock form at 3:00?", "90° (Right angle)", ["180°", "60°", "45°"], "At 3:00, the minute hand points to 12 and the hour hand to 3, forming a 90° right angle."),
                    ("What angle do the hands of a clock form at 6:00?", "180° (Straight angle)", ["90°", "120°", "360°"], "At 6:00, the hands point in opposite directions, forming a straight line of 180°.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif "how many squares" in low_ch or "area and its boundary" in low_ch or any(k in low_t for k in ["boundary", "grid", "footprint"]):
                items = [
                    ("What is the area of a rectangle with length 12 cm and breadth 8 cm?", "96 cm²", ["40 cm²", "90 cm²", "100 cm²"], "Area = length × breadth = 12 cm × 8 cm = 96 cm²."),
                    ("What is the perimeter (boundary) of a square with side 9 cm?", "36 cm", ["81 cm", "27 cm", "18 cm"], "Perimeter of square = 4 × side = 4 × 9 cm = 36 cm."),
                    ("If the perimeter of a rectangle is 30 cm and its length is 10 cm, what is its breadth?", "5 cm", ["10 cm", "15 cm", "7.5 cm"], "Perimeter = 2(l + b) => 30 = 2(10 + b) => 15 = 10 + b => b = 5 cm.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif "parts and wholes" in low_ch or any(k in low_t for k in ["fraction", "whole", "half", "quarter"]):
                items = [
                    ("How many 25-paise coins make 1 rupee?", "4 coins", ["2 coins", "5 coins", "10 coins"], "1 Rupee = 100 paise. 100 / 25 = 4 coins (each coin is 1/4 of a rupee)."),
                    ("What is 3/4 of a rupee in paise?", "75 paise", ["50 paise", "25 paise", "80 paise"], "3/4 × 100 paise = 75 paise."),
                    ("Which fraction is equivalent to 2/3?", "4/6", ["3/4", "2/6", "5/6"], "Multiplying numerator and denominator of 2/3 by 2 gives 4/6.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif "multiple" in low_ch or "factor" in low_ch or any(k in low_t for k in ["factor tree", "common factor", "common multiple"]):
                items = [
                    ("What is the smallest common multiple (LCM) of 4 and 6?", "12", ["24", "8", "2"], "Multiples of 4: 4, 8, 12, 16... Multiples of 6: 6, 12, 18... Smallest common is 12."),
                    ("Which of the following numbers is a factor of 36?", "9", ["5", "7", "8"], "36 is exactly divisible by 9 (36 / 9 = 4)."),
                    ("What is the highest common factor (HCF) of 12 and 18?", "6", ["3", "4", "12"], "Factors of 12: 1,2,3,4,6,12. Factors of 18: 1,2,3,6,9,18. Common: 1,2,3,6. HCF = 6.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            # --- Foundation Grade Math (Nursery, LKG, UKG, 1, 2) ---
            elif str(class_level) in ("Nursery", "LKG", "UKG", "1", "2"):
                items = [
                    ("How many sides does a triangle have?", "3 sides", ["4 sides", "2 sides", "5 sides"], "A triangle is a closed shape with exactly three straight sides."),
                    ("Which number comes immediately after 7?", "8", ["6", "9", "10"], "Counting upwards: 5, 6, 7, 8."),
                    ("If you have 2 apples and get 2 more, how many apples do you have in total?", "4 apples", ["3 apples", "5 apples", "6 apples"], "2 + 2 = 4."),
                    ("What is the shape of a round coin or a full moon?", "Circle", ["Square", "Triangle", "Rectangle"], "A round coin has the geometric shape of a circle."),
                    ("Which is larger: 5 or 9?", "9 is larger", ["5 is larger", "Both are equal", "Cannot be determined"], "In whole numbers, 9 is greater than 5.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            # Substantive Grade-Adaptive Math Curriculum Bank
            else:
                items = [
                    (f"What is the sum of all interior angles in any triangle?", "180°", ["360°", "90°", "270°"], "The angle sum property of a triangle states that the sum of all three angles is always 180°."),
                    (f"What is the distance between the origin (0, 0) and the point (3, 4)?", "5 units", ["7 units", "12 units", "25 units"], "Using the distance formula: d = √(3² + 4²) = √(9 + 16) = √25 = 5 units."),
                    (f"For any two positive integers a and b, what is the relationship between their HCF and LCM?", "HCF(a, b) × LCM(a, b) = a × b", ["HCF(a, b) + LCM(a, b) = a × b", "HCF(a, b) / LCM(a, b) = a + b", "LCM(a, b) - HCF(a, b) = a × b"], "The product of the HCF and LCM of two numbers always equals the product of the two numbers."),
                    (f"What is the probability of an impossible event that cannot occur?", "0", ["1", "0.5", "-1"], "The probability of an impossible event is 0, while that of a sure event is 1."),
                    (f"Which formula correctly gives the volume of a cylinder with base radius r and height h?", "πr²h", ["2πrh", "πr²", "(1/3)πr²h"], "The volume of a right circular cylinder is the base area times height: V = πr²h."),
                    (f"What is the empirical relationship connecting Mean, Median, and Mode in statistics?", "3 Median = Mode + 2 Mean", ["Median = 3 Mode + 2 Mean", "Mode = 3 Median + 2 Mean", "2 Median = Mode + 3 Mean"], "Karl Pearson's empirical relationship states that 3 Median = Mode + 2 Mean.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

        # =========================================================================
        # 2. SCIENCE (Class-Stratified: Physics, Chemistry, Biology)
        # =========================================================================
        elif any(k in low_s for k in ["science", "physics", "chem", "bio", "evs", "environmental"]) and not any(k in low_s for k in ["social", "sst", "computer", "ai"]):
            sci_context = low_ch + " " + low_t
            if str(class_level) in ("Nursery", "LKG", "UKG", "1", "2"):
                items = [
                    ("Which sense organ helps us to see the world around us?", "Eyes", ["Ears", "Nose", "Tongue"], "Our eyes allow us to see colors, shapes, and light."),
                    ("Which of the following is a living thing?", "A tree", ["A chair", "A pencil", "A car"], "Trees grow, take in nutrients, and reproduce, making them living things."),
                    ("Which part of a plant grows beneath the soil to absorb water?", "Roots", ["Flowers", "Leaves", "Fruits"], "Roots anchor the plant into the ground and absorb water and minerals.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif any(k in sci_context for k in ["atom", "molecule", "chemical combination"]):
                items = [
                    ("Which law of chemical combination states that in a compound, elements are always present in definite proportions by mass?", "Law of Constant Proportions (Proust)", ["Law of Conservation of Mass", "Law of Multiple Proportions", "Avogadro's Law"], "Proust stated that in a chemical substance, the elements are always present in definite proportions by mass."),
                    ("Which law states that mass can neither be created nor destroyed in a chemical reaction?", "Law of Conservation of Mass", ["Law of Constant Proportions", "Law of Reciprocal Proportions", "Boyle's Law"], "Lavoisier established that mass is conserved during chemical reactions."),
                    ("What is the ratio of hydrogen to oxygen by mass in pure water (H₂O)?", "1:8", ["1:2", "2:1", "1:16"], "Mass of 2 H = 2 u, mass of 1 O = 16 u. Ratio by mass = 2:16 = 1:8."),
                    ("According to Dalton's Atomic Theory, what are all matter made of?", "Indivisible particles called atoms", ["Continuous fluids", "Pure energy waves", "Plasmatic clusters"], "Dalton proposed that all matter is composed of tiny, indivisible particles called atoms.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif any(k in sci_context for k in ["motion", "force", "friction", "gravitation", "sound", "pressure", "work", "energy"]):
                items = [
                    ("Which force always opposes the relative motion between two surfaces in contact?", "Frictional force", ["Gravitational force", "Electrostatic force", "Magnetic force"], "Friction acts parallel to contacting surfaces and opposes their relative motion."),
                    ("What is the SI unit of force?", "Newton (N)", ["Joule", "Pascal", "Watt"], "Force is measured in Newtons (N), where 1 N = 1 kg·m/s²."),
                    ("Which of Newton's laws of motion defines inertia: an object remains at rest or in uniform motion unless acted upon by an external force?", "First Law of Motion", ["Second Law of Motion", "Third Law of Motion", "Law of Gravitation"], "Newton's First Law is also known as the Law of Inertia."),
                    ("What is the approximate acceleration due to gravity (g) near the Earth's surface?", "9.8 m/s²", ["9.8 m/s", "8.9 m/s²", "10.8 m/s²"], "Standard acceleration due to Earth's gravity is 9.8 m/s².")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif any(k in sci_context for k in ["light", "optics", "reflection", "refraction"]):
                items = [
                    ("What is the mirror formula relating focal length f, image distance v, and object distance u?", "1/f = 1/v + 1/u", ["1/f = 1/v - 1/u", "f = v + u", "1/f = 2(v + u)"], "The mirror formula is 1/f = 1/v + 1/u."),
                    ("Which phenomenon causes a pencil dipped in a glass of water to appear bent at the surface?", "Refraction of light", ["Reflection of light", "Total internal reflection", "Dispersion"], "Light changes direction as it travels from water to air due to differing optical densities (refraction)."),
                    ("What type of lens is used to correct hypermetropia (far-sightedness)?", "Convex lens", ["Concave lens", "Cylindrical lens", "Bifocal lens"], "A converging (convex) lens brings nearby diverging rays into focus on the retina.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif any(k in sci_context for k in ["electric", "current", "resistor", "resistance", "circuit", "ohm"]):
                items = [
                    ("State Ohm's Law relationship between voltage (V), current (I), and resistance (R):", "V = I × R", ["I = V × R", "R = V × I", "P = V × I"], "Ohm's Law states that current is directly proportional to voltage at constant temperature: V = IR."),
                    ("What is the SI unit of electrical resistance?", "Ohm (Ω)", ["Ampere (A)", "Volt (V)", "Watt (W)"], "Resistance is measured in Ohms (symbol: Ω)."),
                    ("Three resistors of 2 Ω, 3 Ω, and 5 Ω are connected in series. What is the equivalent resistance?", "10 Ω", ["1 Ω", "30 Ω", "5 Ω"], "In series, R_total = R₁ + R₂ + R₃ = 2 + 3 + 5 = 10 Ω.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif any(k in sci_context for k in ["chemical", "reaction", "acid", "base", "salt"]):
                items = [
                    ("What type of chemical reaction is: 2Mg + O₂ → 2MgO?", "Combination reaction", ["Decomposition reaction", "Displacement reaction", "Double displacement"], "Two reactants combine to form a single product, defining a combination reaction."),
                    ("What gas is released when an acid reacts with an active metal?", "Hydrogen gas (H₂)", ["Oxygen gas (O₂)", "Carbon dioxide (CO₂)", "Nitrogen gas (N₂)"], "Acids react with metals to produce a salt and liberate hydrogen gas: Zn + 2HCl → ZnCl₂ + H₂↑."),
                    ("What color does blue litmus paper turn when dipped into an acidic solution?", "Red", ["Blue", "Green", "Yellow"], "Acids turn blue litmus red, whereas bases turn red litmus blue.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            elif any(k in sci_context for k in ["cell", "tissue", "life process", "living", "organ", "unit of life", "fundamental unit"]):
                items = [
                    ("Which organelle is known as the 'powerhouse of the cell'?", "Mitochondria", ["Nucleus", "Ribosome", "Golgi apparatus"], "Mitochondria produce cellular energy in the form of ATP molecules."),
                    ("Which blood cells are responsible for carrying oxygen throughout the human body?", "Red Blood Cells (Erythrocytes)", ["White Blood Cells", "Platelets", "Plasma"], "Hemoglobin in red blood cells binds and transports oxygen from lungs to body tissues."),
                    ("What green pigment in chloroplasts is essential for capturing solar energy during photosynthesis?", "Chlorophyll", ["Carotene", "Anthocyanin", "Hemoglobin"], "Chlorophyll traps photons from sunlight to power the synthesis of glucose.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

            else:
                items = [
                    ("What is the SI unit of work and energy?", "Joule (J)", ["Watt", "Pascal", "Newton"], "Work and energy are measured in Joules (J), where 1 J = 1 N·m = 1 kg·m²/s²."),
                    ("Which process describes the direct transition of a substance from solid to gas without entering the liquid state?", "Sublimation", ["Evaporation", "Condensation", "Deposition"], "Sublimation occurs in substances like camphor, naphthalene, and dry ice."),
                    ("How many chambers does the normal human heart possess?", "4 chambers", ["2 chambers", "3 chambers", "5 chambers"], "The human heart has four chambers: two upper atria and two lower muscular ventricles."),
                    ("What is the standard unit of temperature in the International System of Units (SI)?", "Kelvin (K)", ["Celsius (°C)", "Fahrenheit (°F)", "Calorie"], "Kelvin (K) is the SI base unit of thermodynamic temperature."),
                    ("The atomic number of an element is uniquely determined by the number of which subatomic particle in its nucleus?", "Protons", ["Neutrons", "Electrons", "Quarks"], "The atomic number (Z) is defined strictly by the count of protons inside the atomic nucleus.")
                ]
                prompt, ans_str, dist, explanation = random.choice(items)

        # =========================================================================
        # 3. SOCIAL SCIENCE (History, Civics, Geography, Economics)
        # =========================================================================
        elif any(k in low_s for k in ["social", "sst", "hist", "geo", "pol", "civic", "eco"]):
            if "nationalism" in low_ch or "dandi" in low_t or "gandhi" in low_t:
                items = [
                    ("In which year did Mahatma Gandhi lead the historic Dandi March (Salt Satyagraha)?", "1930", ["1920", "1942", "1919"], "Mahatma Gandhi began the Salt March to Dandi on March 12, 1930, inaugurating the Civil Disobedience Movement."),
                    ("Where was the historic 1929 Indian National Congress session held under the presidency of Jawaharlal Nehru where 'Purna Swaraj' (Complete Independence) was declared?", "Lahore", ["Calcutta", "Nagpur", "Karachi"], "The Lahore Congress of December 1929 formalized the demand for Purna Swaraj."),
                    ("Which British officer ordered the tragic firing on peaceful citizens gathered at Jallianwala Bagh in Amritsar in 1919?", "General Dyer", ["Lord Dalhousie", "Lord Curzon", "Lord Mountbatten"], "General Reginald Dyer ordered the massacre on Baisakhi day, April 13, 1919.")
                ]
            elif "constitution" in low_ch or "power sharing" in low_ch or "federalism" in low_ch or "civic" in low_s:
                items = [
                    ("Who is universally recognized as the Father and Chief Architect of the Indian Constitution?", "Dr. B.R. Ambedkar", ["Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Vallabhbhai Patel"], "Dr. B.R. Ambedkar was the Chairman of the Drafting Committee of the Constituent Assembly."),
                    ("What is the minimum voting age for Indian citizens under Universal Adult Franchise?", "18 years", ["21 years", "16 years", "25 years"], "The 61st Constitutional Amendment Act reduced the voting age from 21 to 18 years."),
                    ("Which form of government shares power constitutionally between central and state governments?", "Federalism", ["Unitary system", "Monarchy", "Autocracy"], "Federalism establishes dual levels of government with distinct constitutional jurisdictions.")
                ]
            elif "resource" in low_ch or "agriculture" in low_ch or "river" in low_ch or "geo" in low_s:
                items = [
                    ("Which river is revered as the 'Dakshin Ganga' due to its length and spiritual significance in Peninsular India?", "Godavari", ["Krishna", "Cauvery", "Mahanadi"], "The Godavari is the longest peninsular river system in India."),
                    ("Which cropping season in India begins with the onset of the Southwest monsoon in June/July?", "Kharif season", ["Rabi season", "Zaid season", "Winter season"], "Kharif crops (such as rice, maize, cotton, and groundnut) are sown at the beginning of the monsoon."),
                    ("Which black soil is renowned as the ideal soil for growing cotton in India?", "Black soil (Regur)", ["Alluvial soil", "Red soil", "Laterite soil"], "Black or Regur soil in the Deccan trap region has high clay content and moisture retention, ideal for cotton.")
                ]
            else:
                items = [
                    ("Which institution is the apex court and guardian of the Constitution in the Indian judicial system?", "Supreme Court of India", ["High Court", "District Court", "Lok Adalat"], "The Supreme Court located in New Delhi is the highest judicial forum and final court of appeal under the Constitution of India."),
                    ("Which line of longitude serves as the Standard Meridian of India for Indian Standard Time (IST)?", "82°30' E", ["80°00' E", "75°30' E", "90°00' E"], "The 82°30' E longitude passing through Mirzapur in Uttar Pradesh is taken as the standard time for the entire nation."),
                    ("Which sector of the economy encompasses agriculture, fishing, animal husbandry, and forestry?", "Primary sector", ["Secondary sector", "Tertiary sector", "Quaternary sector"], "The primary sector directly extracts and relies upon natural environmental resources."),
                    ("In which historic year did India attain independence from British colonial rule?", "1947", ["1950", "1942", "1930"], "India gained national independence on August 15, 1947.")
                ]
            prompt, ans_str, dist, explanation = random.choice(items)

        # =========================================================================
        # 4. ENGLISH
        # =========================================================================
        elif "english" in low_s:
            if str(class_level) in ("Nursery", "LKG", "UKG", "1", "2"):
                items = [
                    ("Which letter comes immediately after 'B' in the English alphabet?", "C", ["D", "A", "E"], "'C' is the third letter, following 'B'."),
                    ("Which word rhymes with 'CAT'?", "BAT", ["DOG", "SUN", "PIG"], "'BAT' and 'CAT' share the same ending sound '-at'."),
                    ("What is the opposite of 'HOT'?", "COLD", ["WARM", "SUNNY", "BIG"], "'COLD' is the exact opposite temperature of 'HOT'."),
                    ("Which letter is a vowel?", "A", ["B", "M", "T"], "The vowels in English are A, E, I, O, U."),
                    ("Complete the popular rhyme: 'Twinkle, twinkle, little ___'?", "Star", ["Moon", "Sun", "Cloud"], "The classic nursery rhyme line is 'Twinkle, twinkle, little star'.")
                ]
            elif "mandela" in low_ch or "apartheid" in low_t:
                items = [
                    ("In 'Long Walk to Freedom', who did Nelson Mandela thank during his historic presidential inauguration?", "The people of South Africa and international guests", ["Only his family members", "The previous colonial rulers", "Military generals alone"], "Mandela thanked the international leaders and the resilient South African people for celebrating a common victory for justice, peace, and human dignity."),
                    ("According to Nelson Mandela, what are the 'twin obligations' of every human being?", "Obligations to family and obligations to one's country and people", ["Obligations to earn wealth and travel the world", "Obligations to religion and military service", "Obligations to school and friends"], "Mandela stated that every man has obligations to his parents, wife, and children, and obligations to his community and nation."),
                    ("How does Nelson Mandela define true courage in his autobiography?", "Courage is not the absence of fear, but the triumph over it", ["Courage means never feeling any fear", "Courage means avoiding all dangerous situations", "Courage means physical violence against enemies"], "Mandela learned that the brave man is not he who does not feel afraid, but he who conquers that fear.")
                ]
            elif "letter to god" in low_ch or "lencho" in low_t:
                items = [
                    ("In the story 'A Letter to God', why did Lencho write a letter addressed to God?", "His ripe corn crop was destroyed by a severe hailstorm", ["He needed money to buy a new house", "He wanted to thank God for excessive rainfall", "He wanted a job in the city"], "A heavy hailstorm devastated Lencho's entire field, leaving his family facing hunger."),
                    ("How much money in pesos did Lencho ask God to send him in his letter?", "100 pesos", ["50 pesos", "70 pesos", "500 pesos"], "Lencho asked for 100 pesos to sow his field again and live until the next crop."),
                    ("How much money was the postmaster able to collect and send to Lencho?", "70 pesos", ["100 pesos", "50 pesos", "30 pesos"], "The postmaster gave part of his salary and collected 70 pesos from colleagues and friends."),
                    ("What did Lencho call the post office employees after receiving only 70 pesos?", "A bunch of crooks", ["Helpful angels", "Generous donors", "Selfless servants"], "Lencho mistakenly believed that God could not have made a mistake and that the post office staff stole 30 pesos.")
                ]
            elif "flying" in low_ch or "seagull" in low_t or "aeroplane" in low_t:
                items = [
                    ("In 'His First Flight', what finally compelled the frightened young seagull to fly?", "Extreme hunger and the sight of fish in his mother's beak", ["A sudden gust of wind", "His siblings pushing him off the ledge", "A predator attacking the nest"], "Maddened by hunger, the young seagull dived at the fish held by his mother and found his wings spreading naturally."),
                    ("In 'The Black Aeroplane', which aircraft was the narrator flying from France to England?", "Old Dakota DS 088", ["Boeing 737", "Spitfire MK IX", "Airbus A320"], "The narrator was piloting his old Dakota DS 088 on his way to join his family for breakfast."),
                    ("What was unusual about the black aeroplane that guided the pilot through the storm clouds?", "It had no lights on its wings and vanished from radar", ["It flew backwards", "It was painted fluorescent red", "It communicated via radio loudspeaker"], "The mysterious black plane flew silently without lights and could not be detected on the control tower radar.")
                ]
            elif "frost" in low_ch or "dust of snow" in low_ch or "fire and ice" in low_ch:
                items = [
                    ("In Robert Frost's poem 'Dust of Snow', what natural element changes the poet's gloomy mood?", "A crow shaking snow from a hemlock tree onto him", ["A bright morning sunrise", "The melodious song of a nightingale", "A warm cup of coffee"], "The simple, unexpected falling of fine snow from a poisonous hemlock tree saved a part of the poet's day from regret."),
                    ("In Robert Frost's poem 'Fire and Ice', what destructive human emotions are symbolized by Fire and Ice?", "Fire symbolizes Greed/Desire; Ice symbolizes Hatred/Coldness", ["Fire symbolizes Joy; Ice symbolizes Peace", "Fire symbolizes Anger; Ice symbolizes Love", "Fire symbolizes Wisdom; Ice symbolizes Foolishness"], "The poet equates destructive fire with insatiable desire and frigid ice with callous human hatred.")
                ]
            else:
                items = [
                    ("Identify the adverb of manner in: 'The brave soldier fought courageously in battle.'", "courageously", ["brave", "soldier", "battle"], "'Courageously' describes how the action (fought) was performed, functioning as an adverb."),
                    ("Choose the correct passive voice: 'The author wrote an inspiring novel.'", "An inspiring novel was written by the author.", ["An inspiring novel had written by author.", "An inspiring novel was being written.", "An inspiring novel is written."], "Simple past 'wrote' becomes 'was written' in passive voice."),
                    ("What is the antonym of the word 'ANCIENT'?", "Modern", ["Historic", "Antique", "Elderly"], "'Modern' refers to the present or recent times, which is the direct opposite of ancient.")
                ]
            prompt, ans_str, dist, explanation = random.choice(items)

        # =========================================================================
        # 5. HINDI
        # =========================================================================
        elif "hindi" in low_s:
            if str(class_level) in ("Nursery", "LKG", "UKG", "1", "2"):
                items = [
                    ("हिंदी वर्णमाला का पहला स्वर कौन सा है?", "अ", ["क", "म", "र"], "हिंदी वर्णमाला में स्वरों की शुरुआत 'अ' से होती है।"),
                    ("'दिन' का विलोम (उलटा) शब्द क्या है?", "रात", ["सुबह", "शाम", "दोपहर"], "'दिन' का विपरीत शब्द 'रात' होता है।"),
                    ("'सूरज' हमें क्या देता है?", "धूप और रोशनी", ["बर्फ", "अंधेरा", "पानी"], "सूरज से हमें प्रकाश (धूप) और ऊर्जा मिलती है।")
                ]
            else:
                items = [
                    ("किसी व्यक्ति, वस्तु, स्थान या भाव के नाम को क्या कहते हैं?", "संज्ञा", ["सर्वनाम", "विशेषण", "क्रिया"], "किसी व्यक्ति, प्राणी, वस्तु, स्थान अथवा भाव के नाम को संज्ञा कहा जाता है।"),
                    ("'आँखों का तारा' मुहावरे का सही अर्थ क्या है?", "बहुत प्यारा होना", ["कम दिखाई देना", "गुस्सा होना", "धोखा देना"], "'आँखों का तारा' मुहावरे का अर्थ अत्यधिक प्रिय अथवा प्यारा होना है।"),
                    ("'सूर्योदय' शब्द का सही संधि विच्छेद क्या होगा?", "सूर्य + उदय (गुण स्वर संधि)", ["सूर्य + दय", "सूर्यो + दय", "सूर्या + उदय"], "सूर्य + उदय मिलकर 'सूर्योदय' बनता है, जो गुण स्वर संधि का उदाहरण है।")
                ]
            prompt, ans_str, dist, explanation = random.choice(items)

        # =========================================================================
        # 6. COMPUTER SCIENCE & ARTIFICIAL INTELLIGENCE
        # =========================================================================
        elif any(k in low_s for k in ["computer", "ai", "artificial", "it", "python"]):
            cs_context = low_ch + " " + low_t + " " + low_s
            if any(k in cs_context for k in ["search", "sort", "array", "stack", "queue"]):
                items = [
                    ("What is the essential prerequisite condition for performing Binary Search on a sequence?", "The elements must be sorted", ["The elements must be unique", "The array size must be a power of 2", "All elements must be positive"], "Binary search requires that elements are arranged in monotonic sorted order."),
                    ("What is the worst-case time complexity of Binary Search on a sorted list of n elements?", "O(log n)", ["O(n)", "O(n²)", "O(1)"], "Binary search repeatedly divides the search space in half, giving logarithmic time complexity O(log n)."),
                    ("In the worst case, how many comparisons does Linear Search make on an array of size n?", "n comparisons", ["log n comparisons", "n/2 comparisons", "1 comparison"], "If the target is at the end or not present, linear search examines every element once.")
                ]
            elif any(k in cs_context for k in ["python", "list", "dict", "tuple", "loop", "string", "function", "variable", "code"]):
                items = [
                    ("In Python, which built-in data type is mutable and defined with square brackets []?", "List", ["Tuple", "String", "Integer"], "Python lists are mutable ordered sequences defined using square brackets."),
                    ("In Python, which data structure stores key-value pairs and is enclosed in curly braces {}?", "Dictionary (dict)", ["List", "Tuple", "Set"], "Dictionaries store mappings of unique keys to values in Python: {key: value}."),
                    ("Which keyword is used to define a user-defined function in Python?", "def", ["function", "fun", "define"], "The 'def' keyword is used to declare a function header in Python syntax."),
                    ("What is the output of len([10, 20, 30, 40]) in Python?", "4", ["3", "5", "40"], "The len() function returns the total number of elements in the collection, which is 4.")
                ]
            elif any(k in cs_context for k in ["ai", "artificial", "intelligence", "machine learning", "model"]):
                items = [
                    ("What are the three primary domains of Artificial Intelligence?", "Data Science, Computer Vision, and Natural Language Processing", ["Hardware, Software, and Network", "Python, Java, and C++", "Robotics, Mechanics, and Civil"], "AI applications are classified into Data Science, Computer Vision (CV), and NLP."),
                    ("What evaluation metric measures True Positives divided by total actual positives: TP / (TP + FN)?", "Recall", ["Precision", "Accuracy", "F1 Score"], "Recall measures how well a machine learning classifier identifies all positive instances."),
                    ("What metric measures True Positives divided by total predicted positives: TP / (TP + FP)?", "Precision", ["Recall", "Accuracy", "F1 Score"], "Precision evaluates the exactness of positive model predictions.")
                ]
            else:
                items = [
                    ("Which logic gate produces an output of 1 (True) only when both of its inputs are 1?", "AND gate", ["OR gate", "NOT gate", "XOR gate"], "An AND gate gives a high output if and only if all inputs are high."),
                    ("In computing, how many bits make up one byte?", "8 bits", ["4 bits", "16 bits", "32 bits"], "One byte is universally defined as a sequence of 8 bits."),
                    ("In Python, which built-in data type is mutable and defined with square brackets []?", "List", ["Tuple", "String", "Integer"], "Python lists are mutable ordered sequences defined using square brackets.")
                ]
            prompt, ans_str, dist, explanation = random.choice(items)

        # =========================================================================
        # 7. COMMERCE, SANSKRIT & SPECIALIZED CURRICULUM SUBJECTS
        # =========================================================================
        elif any(k in low_s for k in ["account", "business", "commerce", "finance"]):
            items = [
                ("In double-entry bookkeeping, which fundamental accounting equation must always balance?", "Assets = Liabilities + Capital", ["Assets = Liabilities - Capital", "Liabilities = Assets + Capital", "Capital = Assets + Liabilities"], "The fundamental accounting equation states that a firm's total resources (Assets) are financed by claims of creditors (Liabilities) and owners (Capital)."),
                ("How many general principles of management were formulated by Henri Fayol?", "14 principles", ["10 principles", "12 principles", "16 principles"], "Henri Fayol formulated 14 principles of management including Division of Work, Authority & Responsibility, and Unity of Command."),
                ("Which four elements constitute the traditional Marketing Mix (4 Ps)?", "Product, Price, Place, and Promotion", ["People, Process, Profit, and Product", "Planning, Pricing, Packaging, and Promoting", "Production, Purchasing, Positioning, and Profit"], "The 4 Ps of marketing are Product, Price, Place, and Promotion."),
                ("In financial accounting, which accounts are increased by a debit entry?", "Assets and Expenses", ["Liabilities and Revenues", "Capital and Liabilities", "Revenues and Gains"], "Under standard rules of accounting, debits increase asset and expense accounts, while credits increase liability, equity, and revenue accounts.")
            ]
            prompt, ans_str, dist, explanation = random.choice(items)

        elif "sanskrit" in low_s:
            items = [
                ("संस्कृत में 'पठति' रूप किस लकार एवं पुरुष का है?", "लट् लकार, प्रथम पुरुष, एकवचन", ["लृट् लकार, मध्यम पुरुष", "लङ् लकार, उत्तम पुरुष", "लोट् लकार, प्रथम पुरुष"], "'पठति' लट् लकार (वर्तमान काल) प्रथम पुरुष एकवचन का मानक रूप है।"),
                ("प्रसिद्ध सूक्ति 'विद्या ददाति विनयं' का सही अर्थ क्या है?", "विद्या विनम्रता प्रदान करती है", ["विद्या धन देती है", "विद्या बल देती है", "विद्या अहंकार देती है"], "संस्कृत सूक्ति के अनुसार सच्ची विद्या मनुष्य को विनम्र और शीलवान बनाती है।"),
                ("'बालकः कन्दुकेन क्रीडति' — इस वाक्य में साधन के अर्थ में कौन सा कारक है?", "करण कारक (तृतीया विभक्ति)", ["कर्म कारक", "अपादान कारक", "अधिकरण कारक"], "क्रिया के साधन में करण कारक और तृतीया विभक्ति का प्रयोग होता है।")
            ]
            prompt, ans_str, dist, explanation = random.choice(items)

        else:
            items = [
                (f"In the study of {topic_name} under {subject_name}, what is the primary analytical objective?", f"Applying standard verified principles and standard formulas of {topic_name}", [f"Using unverified empirical estimations", f"Omitting foundational principles", f"Applying methods from unrelated domains"], f"Class {class_level} {subject_name} requires systematic and verified application of {topic_name} rules."),
                (f"When evaluating exam questions on {topic_name}, which approach guarantees curriculum accuracy?", f"Step-by-step reasoning verified by curriculum benchmarks", [f"Guessing without calculation", f"Changing question parameters", f"Using unofficial conventions"], f"Standard board examinations enforce verified step-by-step logic.")
            ]
            prompt, ans_str, dist, explanation = random.choice(items)

        if not prompt or not ans_str:
            continue
        dist = dist or []
        if prompt in generated_prompts:
            continue
        generated_prompts.add(prompt)

        # Adapt True/False variety if targeted
        if target_mode == 1 and not (prompt.lower().startswith("state true or false") or prompt.lower().startswith("बताइए") or ans_str in ["True", "False"]):
            tf_p = f"State True or False: In {topic_name}, {prompt.rstrip('?')} is {ans_str}."
            if validate_question_topic(tf_p, topic_name, chapter_name, subject_name, class_level):
                prompt = tf_p
                ans_str = "True"
                dist = ["False"]
                explanation = f"True. {explanation}"

        # Adapt Fill-in-the-blank variety if targeted
        elif target_mode == 2 and "_____" not in prompt and ans_str not in ["True", "False"]:
            fib_p = f"Complete the statement for {topic_name}: {prompt.rstrip('?')} — the correct answer is _____."
            if validate_question_topic(fib_p, topic_name, chapter_name, subject_name, class_level):
                prompt = fib_p

        # Assemble and shuffle options
        if ans_str in ["True", "False"] or (isinstance(dist, list) and set(dist + [ans_str]) == {"True", "False"}):
            opts = ["True", "False"]
            correct_idx = 0 if ans_str == "True" else 1
        elif ans_str in ["सही", "गलत"] or (isinstance(dist, list) and set(dist + [ans_str]) == {"सही", "गलत"}):
            opts = ["सही", "गलत"]
            correct_idx = 0 if ans_str == "सही" else 1
        elif prompt.lower().startswith("state true or false") or prompt.lower().startswith("true or false"):
            opts = ["True", "False"]
            correct_idx = 0 if ans_str.strip().lower() == "true" else 1
        else:
            opts = [ans_str] + [d for d in dist if d != ans_str][:3]
            while len(opts) < 4:
                opts.append(f"Option {len(opts) + 1}")
            random.shuffle(opts)
            correct_idx = opts.index(ans_str)

        if not validate_question_topic(prompt, topic_name, chapter_name, subject_name, class_level):
            continue

        questions.append((prompt, opts, correct_idx, explanation, q_diff))

    return questions
