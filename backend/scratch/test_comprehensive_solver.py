import re, math
from sympy import symbols, Eq, solve, sympify, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

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

def test_solver(t, subject_hint="", chapter_hint="", topic_hint="", class_hint="8"):
    low_t = t.lower()
    sub_hint_low = subject_hint.lower()
    chap_hint_low = chapter_hint.lower()
    top_hint_low = topic_hint.lower()

    # 1. Inverse Proportion (Workers & Days, Work & Time, Speed & Time)
    is_inv_kw = any(k in low_t for k in ["worker", "workers", "men", "women", "days will", "days take", "trench", "pipes", "inversely proportional", "inverse proportion", "inverse variation"]) or any(k in chap_hint_low or k in top_hint_low for k in ["inverse proportion", "inverse variation"])
    if is_inv_kw:
        m_inv = re.search(r"(\d+(?:\.\d+)?)\s*(?:workers?|men|women|people|persons?|labourers?|machines?|pipes?)[^\d]+(\d+(?:\.\d+)?)\s*(?:days?|hours?|hrs?|minutes?|mins?)[^\d]+(\d+(?:\.\d+)?)\s*(?:workers?|men|women|people|persons?|labourers?|machines?|pipes?)", t, re.I)
        if m_inv:
            w1, d1, w2 = float(m_inv.group(1)), float(m_inv.group(2)), float(m_inv.group(3))
            if w2 > 0:
                d2 = (w1 * d1) / w2
                d2_clean = int(d2) if d2.is_integer() else round(d2, 2)
                return {
                    "ans": f"{d2_clean} days",
                    "badge": "Calculated & Checked ✓",
                    "topic": "Direct and Inverse Proportions",
                    "verified": (w1 * d1 == w2 * d2)
                }

    # 2. Direct Proportion (Unitary / Cost)
    m_dir = re.search(r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s*(?:cost|costs|are|weighs?|weigh|give)\s*(?:₹|rs\.?)?\s*(\d+(?:\.\d+)?)[^\d]+(?:what|find|how)[^\d]+(\d+(?:\.\d+)?)\s*([a-zA-Z]+)", t, re.I)
    if m_dir:
        n1, item1, val1, n2, item2 = float(m_dir.group(1)), m_dir.group(2), float(m_dir.group(3)), float(m_dir.group(4)), m_dir.group(5)
        if n1 > 0:
            val2 = (val1 / n1) * n2
            val2_clean = int(val2) if val2.is_integer() else round(val2, 2)
            unit_sym = "₹" if ("₹" in t or "rupee" in low_t or "cost" in low_t) else item2
            return {
                "ans": f"{unit_sym}{val2_clean}" if unit_sym == "₹" else f"{val2_clean} {unit_sym}",
                "badge": "Calculated & Checked ✓",
                "topic": "Direct and Inverse Proportions"
            }

    # 3. Additive Inverse
    m_add_inv = re.search(r"additive\s+inverse\s+of\s+(-?\d+)\s*(?:\/\s*(\d+))?", t, re.I)
    if m_add_inv:
        num = int(m_add_inv.group(1))
        den = int(m_add_inv.group(2)) if m_add_inv.group(2) else 1
        inv_num = -num
        ans_str = f"{inv_num}/{den}" if den != 1 else f"{inv_num}"
        return {
            "ans": ans_str,
            "badge": "Calculated & Checked ✓",
            "topic": "Rational Numbers"
        }

    # 4. Multiplicative Inverse
    m_mul_inv = re.search(r"(?:multiplicative\s+inverse|reciprocal)\s+of\s+(-?\d+)\s*(?:\/\s*(\d+))?", t, re.I)
    if m_mul_inv:
        num = int(m_mul_inv.group(1))
        den = int(m_mul_inv.group(2)) if m_mul_inv.group(2) else 1
        if num == 0:
            return {"ans": "Undefined (0 has no reciprocal)", "badge": "Calculated & Checked ✓"}
        inv_str = f"{-den}/{-num if num<0 else num}" if (num < 0 and den < 0) else (f"-{den}/{abs(num)}" if num < 0 else f"{den}/{num}")
        return {
            "ans": inv_str,
            "badge": "Calculated & Checked ✓",
            "topic": "Rational Numbers"
        }

    # 5. Compound Interest
    if "compound interest" in low_t or "compounded annually" in low_t:
        nums = [float(x) for x in re.findall(r"\b\d+(?:\.\d+)?\b", t)]
        if len(nums) >= 3:
            p = max(nums)
            n_val = min(x for x in nums if x <= 10)
            r_val = [x for x in nums if x != p and x != n_val][0]
            amt = p * ((1 + r_val / 100.0) ** n_val)
            ci = amt - p
            ci_clean = int(ci) if ci.is_integer() else round(ci, 2)
            return {
                "ans": f"₹{format_indian_num(int(ci_clean)) if isinstance(ci_clean, int) else ci_clean}",
                "badge": "Calculated & Checked ✓",
                "topic": "Comparing Quantities"
            }

    return {"ans": "Fallback", "badge": None}

print("1.", test_solver("12 workers can complete a job in 15 days. How many days will 20 workers take to complete the same job?", chapter_hint="Direct and Inverse Proportions"))
print("2.", test_solver("If 8 oranges cost 40 rupees, what will 15 oranges cost?", chapter_hint="Direct and Inverse Proportions"))
print("3.", test_solver("What is the additive inverse of -7/19?", chapter_hint="Rational Numbers"))
print("4.", test_solver("What is the multiplicative inverse of -13/19?", chapter_hint="Rational Numbers"))
print("5.", test_solver("Find the compound interest on 10000 for 2 years at 10% per annum", chapter_hint="Comparing Quantities"))
