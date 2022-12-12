# Experiment with Chebyshev's inequality
from typing import List
import sympy as sp

d = sp.Symbol('d',real=True) 
i = sp.Idx('i',d)
b = sp.IndexedBase('b')
t, lamda = sp.symbols('t lambda', real=True)
bsum = sp.Sum(b[i]**2, (i, 0, d-1))

f = t**2 * bsum
df = sp.diff(f,b[0])
sp.pprint(df)


# The one to minimize


#f = k

#def f(bs: List[sp.Symbol]) -> float:
