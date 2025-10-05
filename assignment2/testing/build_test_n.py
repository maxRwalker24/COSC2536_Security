import time
from sympy import factorint

p = 1000003
q = 999004247
n = p * q

t0 = time.time()
factors = factorint(n)
t1 = time.time()
print("sympy.factorint found:", factors, "in", t1 - t0, "s")
