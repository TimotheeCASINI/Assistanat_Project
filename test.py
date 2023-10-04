import sympy as sp
from math import log10
equation_string = "x+y"
equation_sympy = sp.sympify(equation_string)
equation =sp.Eq(equation_sympy,0)
equation2=sp.Eq(equation_sympy,0)
print(equation)
x,y = sp.symbols('x y')
#list_unknows = list(unknows)
#print(list_unknows)
#equation_sympy = sp.sympify(equation)
solutions = sp.solve((equation,equation2),(x,y))
print(solutions)

# commentaire