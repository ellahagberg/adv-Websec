import sys
from fractions import Fraction

a = list(map(int, sys.stdin.read().split()))
k, n = a[0], a[1]
p = [(a[i], a[i + 1]) for i in range(2, len(a), 2)]

s = Fraction(0, 1)
for i, (xi, yi) in enumerate(p):
    num = 1
    den = 1
    for j, (xj, _) in enumerate(p):
        if i != j:
            num *= -xj
            den *= (xi - xj)
    s += Fraction(yi * num, den)

print(int(s))
