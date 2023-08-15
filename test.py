import sympy as sp
from math import log10
equation ="0.261319+0.801567*x-0.220531*x^2"
print(equation)
x = sp.symbols('x')
equation_sympy = sp.sympify(equation)
solutions = sp.solveset(sp.Eq(equation_sympy,0.85),x)
print(solutions)
print(log10(7))