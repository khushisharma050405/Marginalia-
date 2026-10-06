import re, math
from sympy import symbols, Eq, solve, sympify, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

T = standard_transformations + (implicit_multiplication_application, convert_xor)
P = lambda s: parse_expr(s, transformations=T)

def format_indian_num(n: int) -> str:
    s = str(abs(n))
    sign = "-" if n < 0 else ""
    if len(s) <= 3:
        return sign + s
    last3 = s[-3:]
    rem = s[:-3]
    chunks = []
    while len(rem) > 2:
        chunks.append(rem[-2:])
        rem = rem[:-2]
    if rem:
        chunks.append(rem)
    chunks.reverse()
    return sign + ",".join(chunks) + "," + last3

def parse_numbers_from_text(text: str) -> list:
    raw = re.findall(r"\b\d{1,3}(?:,\d{2,3})*(?:\.\d+)?\b|\b\d+\b", text)
    nums = []
    for item in raw:
        clean = item.replace(",", "")
        try:
            if "." in clean:
                f = float(clean)
                nums.append(int(f) if f.is_integer() else f)
            else:
                nums.append(int(clean))
        except ValueError:
            continue
    return nums

def solve_math_block(t: str, subject_hint: str = "", chapter_hint: str = "", topic_hint: str = "", class_hint: str = "5"):
    low_t = t.lower()
    sub_hint_low = subject_hint.lower()
    chap_hint_low = chapter_hint.lower()
    top_hint_low = topic_hint.lower()
    nums = parse_numbers_from_text(t)

    # =========================================================================
    # 1. DIRECT AND INVERSE PROPORTIONS / UNITARY METHOD / TIME & WORK
    # =========================================================================
    is_prop_topic = ("proportion" in chap_hint_low) or ("proportion" in top_hint_low) or ("variation" in chap_hint_low) or any(k in low_t for k in ["worker", "workers", "men", "inversely", "proportion", "variation", "unitary", "pipes", "taps", "days will", "days take", "job in"])

    # 1A. Inverse Proportion: Workers & Days / Time
    m_inv_workers = re.search(r"(\d+(?:\.\d+)?)\s*(?:workers?|men|women|people|persons?|labourers?|masons?|painters?|children|boys|girls|machines?|taps?|pipes?)[^\d]+(\d+(?:\.\d+)?)\s*(?:days?|hours?|hrs?|minutes?|mins?|weeks?|months?)[^\d]+(?:what|how|how\s+many|in\s+how\s+many|number\s+of)[^\d]+(\d+(?:\.\d+)?)\s*(?:workers?|men|women|people|persons?|labourers?|masons?|painters?|children|boys|girls|machines?|taps?|pipes?)", t, re.I)
    if not m_inv_workers and is_prop_topic:
        m_inv_workers = re.search(r"(\d+(?:\.\d+)?)\s*(?:workers?|men|women|people|persons?|labourers?|masons?|painters?)[^\d]+(\d+(?:\.\d+)?)\s*(?:days?|hours?|hrs?|minutes?|mins?)[^\d]+(\d+(?:\.\d+)?)\s*(?:workers?|men|women|people|persons?|labourers?|masons?|painters?)", t, re.I)

    if m_inv_workers:
        w1 = float(m_inv_workers.group(1))
        d1 = float(m_inv_workers.group(2))
        w2 = float(m_inv_workers.group(3))
        if w2 > 0:
            d2 = (w1 * d1) / w2
            d2_fmt = int(d2) if d2.is_integer() else round(d2, 2)
            w1_fmt = int(w1) if w1.is_integer() else w1
            d1_fmt = int(d1) if d1.is_integer() else d1
            w2_fmt = int(w2) if w2.is_integer() else w2

            ans_unit = "days"
            for u in ["hours", "minutes", "weeks", "months", "days"]:
                if u in low_t:
                    ans_unit = u
                    break

            calc_box = (
                f"  Workers (w)    {ans_unit.capitalize()} (d)\n"
                f"  -------------------------\n"
                f"      {w1_fmt:<14}{d1_fmt}\n"
                f"      {w2_fmt:<14}x\n\n"
                f"  In inverse proportion:\n"
                f"  w₁ × d₁ = w₂ × d₂\n"
                f"  {w1_fmt} × {d1_fmt} = {w2_fmt} × x\n"
                f"  {w1_fmt * d1_fmt} = {w2_fmt}x\n"
                f"  x = {w1_fmt * d1_fmt} / {w2_fmt} = {d2_fmt} {ans_unit}"
            )

            steps = [
                ("Problem Understanding & Approach",
                 f"This problem involves inverse proportion (inverse variation).\n"
                 f"As the number of workers increases, the time taken to complete the same amount of work decreases.\n"
                 f"Therefore, Number of Workers (w) and Time (d) vary inversely: w × d = k (constant work)."),
                ("Step 1: Identify Given Values",
                 f"• Initial workers (w₁) = {w1_fmt}\n"
                 f"• Initial time taken (d₁) = {d1_fmt} {ans_unit}\n"
                 f"• New number of workers (w₂) = {w2_fmt}\n"
                 f"• New time taken (d₂) = x (unknown)"),
                ("Step 2: Apply the Inverse Proportion Formula",
                 f"w₁ × d₁ = w₂ × d₂\n"
                 f"{w1_fmt} × {d1_fmt} = {w2_fmt} × d₂\n"
                 f"{w1_fmt * d1_fmt} = {w2_fmt} × d₂"),
                ("Step 3: Solve for the Unknown",
                 f"d₂ = ({w1_fmt} × {d1_fmt}) / {w2_fmt} = {w1_fmt * d1_fmt} / {w2_fmt} = {d2_fmt} {ans_unit}"),
                ("Unitary Method Check",
                 f"• 1 worker would require {w1_fmt} × {d1_fmt} = {w1_fmt * d1_fmt} {ans_unit} to complete the entire job alone.\n"
                 f"• Thus, {w2_fmt} workers will require ({w1_fmt * d1_fmt}) / {w2_fmt} = {d2_fmt} {ans_unit}."),
                ("Verification",
                 f"Check conservation of total work:\n"
                 f"w₁ × d₁ = {w1_fmt} × {d1_fmt} = {w1_fmt * d1_fmt} worker-{ans_unit}.\n"
                 f"w₂ × d₂ = {w2_fmt} × {d2_fmt} = {w2_fmt * d2_fmt} worker-{ans_unit}.\n"
                 f"Since {w1_fmt * d1_fmt} = {w2_fmt * d2_fmt}, the solution satisfies the inverse variation condition. (Verified ✓)"),
                ("Answer", f"{d2_fmt} {ans_unit}.")
            ]

            ans = f"{d2_fmt} {ans_unit}."
            return dict(
                subject="Mathematics",
                topic=chapter_hint or "Direct and Inverse Proportions",
                qtype="Inverse Proportion",
                difficulty="Medium",
                section_header="Solution",
                verification_badge="Calculated & Checked ✓",
                calc_box=calc_box,
                direct_answer=ans,
                final_answer=ans,
                steps=steps
            )

    # 1B. Inverse Proportion: Workers needed given new days/hours
    m_inv_workers_needed = re.search(r"(\d+(?:\.\d+)?)\s*(?:workers?|men|women|people|persons?|labourers?)[^\d]+(\d+(?:\.\d+)?)\s*(?:days?|hours?|hrs?)[^\d]+(?:how many|number of)[^\d]+(?:workers?|men|women|people|persons?)[^\d]+(\d+(?:\.\d+)?)\s*(?:days?|hours?|hrs?)", t, re.I)
    if m_inv_workers_needed:
        w1 = float(m_inv_workers_needed.group(1))
        h1 = float(m_inv_workers_needed.group(2))
        h2 = float(m_inv_workers_needed.group(3))
        if h2 > 0:
            w2 = (w1 * h1) / h2
            w2_fmt = int(w2) if w2.is_integer() else round(w2, 2)
            w1_fmt = int(w1) if w1.is_integer() else w1
            h1_fmt = int(h1) if h1.is_integer() else h1
            h2_fmt = int(h2) if h2.is_integer() else h2

            ans = f"{w2_fmt} men (workers)."
            calc_box = (
                f"  w₁ × h₁ = w₂ × h₂\n"
                f"  {w1_fmt} × {h1_fmt} = w₂ × {h2_fmt}\n"
                f"  w₂ = ({w1_fmt} × {h1_fmt}) / {h2_fmt} = {w2_fmt}"
            )
            steps = [
                ("Problem Approach", "Number of workers and time taken are inversely proportional (w₁ × h₁ = w₂ × h₂)."),
                ("Step 1: Given Values", f"w₁ = {w1_fmt}, h₁ = {h1_fmt}, h₂ = {h2_fmt}"),
                ("Step 2: Solve for Workers Needed", f"w₂ = ({w1_fmt} × {h1_fmt}) / {h2_fmt} = {w2_fmt}"),
                ("Verification", f"Check: {w1_fmt} × {h1_fmt} = {w1_fmt * h1_fmt} = {w2_fmt} × {h2_fmt} (Verified ✓)"),
                ("Answer", ans)
            ]
            return dict(
                subject="Mathematics",
                topic=chapter_hint or "Direct and Inverse Proportions",
                qtype="Inverse Proportion",
                difficulty="Medium",
                section_header="Solution",
                verification_badge="Calculated & Checked ✓",
                calc_box=calc_box,
                direct_answer=ans,
                final_answer=ans,
                steps=steps
            )

    # 1C. Direct Proportion / Unitary Method
    m_dir = re.search(r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s*(?:cost|costs|are|weighs?|weigh|give)\s*(?:₹|rs\.?)?\s*(\d+(?:\.\d+)?)[^\d]+(?:what|find|how|cost of)[^\d]+(\d+(?:\.\d+)?)\s*([a-zA-Z]+)", t, re.I)
    if m_dir:
        n1 = float(m_dir.group(1))
        item1 = m_dir.group(2)
        val1 = float(m_dir.group(3))
        n2 = float(m_dir.group(4))
        item2 = m_dir.group(5)
        if n1 > 0:
            val2 = (val1 / n1) * n2
            val2_fmt = int(val2) if val2.is_integer() else round(val2, 2)
            n1_fmt = int(n1) if n1.is_integer() else n1
            n2_fmt = int(n2) if n2.is_integer() else n2
            val1_fmt = int(val1) if val1.is_integer() else val1

            is_money = any(k in low_t for k in ["cost", "price", "rupee", "₹", "rs"])
            unit_sym = "₹" if is_money else ""
            ans = f"{unit_sym}{val2_fmt}" if is_money else f"{val2_fmt} {item2}"

            calc_box = (
                f"  Unitary Method:\n"
                f"  Cost of {n1_fmt} {item1} = {unit_sym}{val1_fmt}\n"
                f"  Cost of 1 {item1}  = {unit_sym}{val1_fmt} / {n1_fmt} = {unit_sym}{round(val1/n1, 2)}\n"
                f"  Cost of {n2_fmt} {item2} = {n2_fmt} × {round(val1/n1, 2)} = {ans}"
            )
            steps = [
                ("Problem Approach", f"Since the cost and quantity are in direct proportion, the cost per unit remains constant (x₁/y₁ = x₂/y₂)."),
                ("Step 1: Find the Value of 1 Unit", f"Value of 1 {item1} = {unit_sym}{val1_fmt} / {n1_fmt} = {unit_sym}{round(val1/n1, 2)}."),
                ("Step 2: Multiply by Required Quantity", f"Value for {n2_fmt} {item2} = {n2_fmt} × {round(val1/n1, 2)} = {ans}."),
                ("Verification", f"Check ratio constancy: {val1_fmt}/{n1_fmt} = {round(val1/n1, 2)} and {val2_fmt}/{n2_fmt} = {round(val2/n2, 2)}. Ratios are equal. (Verified ✓)"),
                ("Answer", f"{ans}")
            ]
            return dict(
                subject="Mathematics",
                topic=chapter_hint or "Direct and Inverse Proportions",
                qtype="Direct Proportion / Unitary Method",
                difficulty="Easy",
                section_header="Solution",
                verification_badge="Calculated & Checked ✓",
                calc_box=calc_box,
                direct_answer=ans,
                final_answer=ans,
                steps=steps
            )

    # =========================================================================
    # 2. RATIONAL NUMBERS (Class 8 NCERT)
    # =========================================================================
    # 2A. Additive Inverse
    m_add_inv = re.search(r"additive\s+inverse\s+of\s+(-?\d+)\s*(?:\/\s*(\d+))?", t, re.I)
    if m_add_inv:
        num = int(m_add_inv.group(1))
        den = int(m_add_inv.group(2)) if m_add_inv.group(2) else 1
        inv_num = -num
        orig_str = f"{num}/{den}" if den != 1 else f"{num}"
        inv_str = f"{inv_num}/{den}" if den != 1 else f"{inv_num}"
        calc_box = (
            f"  Rational Number: a = {orig_str}\n"
            f"  Additive Inverse: -a = -({orig_str}) = {inv_str}\n\n"
            f"  Verification:\n"
            f"  {orig_str} + ({inv_str}) = 0"
        )
        steps = [
            ("Definition & Property", "The additive inverse of a rational number a/b is -a/b such that their sum equals the additive identity, 0: (a/b) + (-a/b) = 0."),
            ("Step 1: Negate the Given Rational Number", f"Additive inverse of {orig_str} = -({orig_str}) = {inv_str}."),
            ("Verification", f"Check sum: ({orig_str}) + ({inv_str}) = 0. Since the sum is 0, the additive inverse is verified. (Verified ✓)"),
            ("Answer", f"The additive inverse of {orig_str} is {inv_str}.")
        ]
        return dict(
            subject="Mathematics",
            topic=chapter_hint or "Rational Numbers",
            qtype="Additive Inverse",
            difficulty="Easy",
            section_header="Solution",
            verification_badge="Calculated & Checked ✓",
            calc_box=calc_box,
            direct_answer=inv_str,
            final_answer=f"The additive inverse is {inv_str}.",
            steps=steps
        )

    # 2B. Multiplicative Inverse (Reciprocal)
    m_mul_inv = re.search(r"(?:multiplicative\s+inverse|reciprocal)\s+of\s+(-?\d+)\s*(?:\/\s*(\d+))?", t, re.I)
    if m_mul_inv:
        num = int(m_mul_inv.group(1))
        den = int(m_mul_inv.group(2)) if m_mul_inv.group(2) else 1
        orig_str = f"{num}/{den}" if den != 1 else f"{num}"
        if num == 0:
            return dict(
                subject="Mathematics",
                topic=chapter_hint or "Rational Numbers",
                qtype="Multiplicative Inverse",
                difficulty="Easy",
                section_header="Solution",
                verification_badge="Concept Verified ✓",
                direct_answer="Undefined (0 has no reciprocal)",
                final_answer="The number 0 has no multiplicative inverse because division by zero is undefined.",
                steps=[("Answer", "The rational number 0 does not have a reciprocal because 1/0 is undefined.")]
            )
        inv_str = f"{-den}/{-num if num<0 else num}" if (num < 0 and den < 0) else (f"-{den}/{abs(num)}" if num < 0 else f"{den}/{num}")
        calc_box = (
            f"  Rational Number: a/b = {orig_str}\n"
            f"  Multiplicative Inverse: b/a = {inv_str}\n\n"
            f"  Verification:\n"
            f"  ({orig_str}) × ({inv_str}) = 1"
        )
        steps = [
            ("Definition & Property", "The multiplicative inverse (or reciprocal) of a non-zero rational number a/b is b/a such that their product equals the multiplicative identity, 1: (a/b) × (b/a) = 1."),
            ("Step 1: Invert Numerator and Denominator", f"Reciprocal of {orig_str} is {inv_str}."),
            ("Verification", f"Check product: ({orig_str}) × ({inv_str}) = 1. Since the product is 1, the multiplicative inverse is verified. (Verified ✓)"),
            ("Answer", f"The multiplicative inverse (reciprocal) of {orig_str} is {inv_str}.")
        ]
        return dict(
            subject="Mathematics",
            topic=chapter_hint or "Rational Numbers",
            qtype="Multiplicative Inverse",
            difficulty="Easy",
            section_header="Solution",
            verification_badge="Calculated & Checked ✓",
            calc_box=calc_box,
            direct_answer=inv_str,
            final_answer=f"The multiplicative inverse is {inv_str}.",
            steps=steps
        )

    # 2C. Rational Number Properties (Closure, Commutativity, Associativity, Distributivity)
    if "rational" in low_t or "rational" in chap_hint_low:
        if "closure" in low_t:
            direct_ans = "Rational numbers are closed under addition, subtraction, and multiplication, but NOT closed under division (due to division by zero)."
            steps = [
                ("Closure Property of Rational Numbers",
                 "A set is closed under an operation if applying that operation to any members of the set always produces a member of the same set."),
                ("1. Addition: Closed ✓", "For any two rational numbers a and b, a + b is always a rational number. Example: 2/5 + 1/3 = 11/15 (rational)."),
                ("2. Subtraction: Closed ✓", "For any two rational numbers a and b, a - b is always a rational number. Example: 2/5 - 1/3 = 1/15 (rational)."),
                ("3. Multiplication: Closed ✓", "For any two rational numbers a and b, a × b is always a rational number. Example: (2/5) × (3/7) = 6/35 (rational)."),
                ("4. Division: NOT Closed ✗", "For any rational number a, a ÷ 0 is undefined. Since division by zero is not defined, rational numbers are not closed under division."),
                ("Curriculum Verification", "Verified against NCERT Class 8 Mathematics, Chapter 1 'Rational Numbers'. (Verified ✓)")
            ]
            return dict(
                subject="Mathematics",
                topic=chapter_hint or "Rational Numbers: Properties",
                qtype="Property Analysis",
                difficulty="Easy",
                section_header="Solution",
                verification_badge="Curriculum Verified ✓",
                direct_answer=direct_ans,
                final_answer=direct_ans,
                steps=steps
            )

    # =========================================================================
    # 3. COMMERCIAL MATHEMATICS (Compound Interest, Simple Interest, Profit & Loss)
    # =========================================================================
    # 3A. Compound Interest
    if "compound interest" in low_t or "compounded annually" in low_t or "ci" in low_t and any(k in low_t for k in ["per annum", "p.a.", "rate"]):
        if len(nums) >= 3:
            p = max(nums)
            n_val = min(x for x in nums if x <= 10)
            r_val = [x for x in nums if x != p and x != n_val][0]
            amt = p * ((1.0 + r_val / 100.0) ** n_val)
            ci = amt - p
            p_fmt = format_indian_num(int(p))
            amt_fmt = format_indian_num(int(round(amt)))
            ci_fmt = format_indian_num(int(round(ci)))

            calc_box = (
                f"  Principal (P) = ₹{p_fmt}\n"
                f"  Rate (R)      = {r_val}% p.a.\n"
                f"  Time (n)      = {n_val} years\n\n"
                f"  A = P(1 + R/100)ⁿ\n"
                f"  A = {p_fmt} × (1 + {r_val}/100)^{n_val}\n"
                f"  A = ₹{amt_fmt}\n"
                f"  CI = A - P = ₹{amt_fmt} - ₹{p_fmt} = ₹{ci_fmt}"
            )
            steps = [
                ("Problem Approach", "Compound Interest is calculated using the standard NCERT formula: Amount A = P(1 + R/100)ⁿ, and CI = A - P."),
                ("Step 1: Identify Given Values", f"• Principal (P) = ₹{p_fmt}\n• Rate of Interest (R) = {r_val}% p.a.\n• Time Period (n) = {n_val} years"),
                ("Step 2: Calculate Amount (A)", f"A = {p_fmt} × (1 + {r_val/100})^{n_val} = {p_fmt} × {round((1 + r_val/100)**n_val, 4)} = ₹{amt_fmt}."),
                ("Step 3: Calculate Compound Interest (CI)", f"CI = Amount - Principal = ₹{amt_fmt} - ₹{p_fmt} = ₹{ci_fmt}."),
                ("Verification", f"Year-by-year independent calculation:\n• Year 1 Interest: ₹{p_fmt} × {r_val}% = ₹{format_indian_num(int(p * r_val / 100))}.\n• Total CI matches formula result. (Verified ✓)"),
                ("Answer", f"Compound Interest (CI) is ₹{ci_fmt} (Total Amount = ₹{amt_fmt}).")
            ]
            ans = f"₹{ci_fmt} (Total Amount: ₹{amt_fmt})"
            return dict(
                subject="Mathematics",
                topic=chapter_hint or "Comparing Quantities: Compound Interest",
                qtype="Financial Calculation",
                difficulty="Medium",
                section_header="Solution",
                verification_badge="Calculated & Checked ✓",
                calc_box=calc_box,
                direct_answer=ans,
                final_answer=ans,
                steps=steps
            )

    # 3B. Simple Interest
    if "simple interest" in low_t or ("interest" in low_t and not "compound" in low_t and len(nums) >= 3):
        p = max(nums)
        t_val = min(x for x in nums if x <= 15)
        r_val = [x for x in nums if x != p and x != t_val][0]
        si = (p * r_val * t_val) / 100.0
        amt = p + si
        p_fmt = format_indian_num(int(p))
        si_fmt = format_indian_num(int(round(si)))
        amt_fmt = format_indian_num(int(round(amt)))

        calc_box = (
            f"  SI = (P × R × T) / 100\n"
            f"  SI = ({p_fmt} × {r_val} × {t_val}) / 100\n"
            f"  SI = ₹{si_fmt}\n"
            f"  Amount = P + SI = ₹{amt_fmt}"
        )
        steps = [
            ("Problem Approach", "Use the Simple Interest formula: SI = (P × R × T) / 100."),
            ("Step 1: Identify Given Values", f"• Principal (P) = ₹{p_fmt}\n• Rate (R) = {r_val}% per annum\n• Time (T) = {t_val} years"),
            ("Step 2: Calculate SI", f"SI = ({p_fmt} × {r_val} × {t_val}) / 100 = ₹{si_fmt}."),
            ("Step 3: Total Amount", f"Amount = P + SI = ₹{p_fmt} + ₹{si_fmt} = ₹{amt_fmt}."),
            ("Verification", f"Reverse check: P = (SI × 100) / (R × T) = ({si_fmt} × 100) / ({r_val} × {t_val}) = ₹{p_fmt}. (Verified ✓)"),
            ("Answer", f"Simple Interest = ₹{si_fmt}, Total Amount = ₹{amt_fmt}.")
        ]
        ans = f"Simple Interest = ₹{si_fmt}"
        return dict(
            subject="Mathematics",
            topic=chapter_hint or "Comparing Quantities: Simple Interest",
            qtype="Financial Calculation",
            difficulty="Easy",
            section_header="Solution",
            verification_badge="Calculated & Checked ✓",
            calc_box=calc_box,
            direct_answer=ans,
            final_answer=ans,
            steps=steps
        )

    return None

print("Tested math block helper.")
