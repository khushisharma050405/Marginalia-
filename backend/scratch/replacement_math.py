# scratch replacement test
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

print("Replacement test ready")
