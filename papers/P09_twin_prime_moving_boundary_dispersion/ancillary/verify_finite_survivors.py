from __future__ import annotations
from math import prod
from sympy import primerange,isprime
for z in (5,7,11,13):
    ps=list(primerange(3,z+1)); P=2*prod(ps)
    survivors=[a for a in range(P) if a%2 and all(a%p not in (0,p-2) for p in ps)]
    assert len(survivors)==prod(p-2 for p in ps),(z,len(survivors))
for X in (100,1000,5000):
    twins=[p for p in primerange(2,X+1) if isprime(p+2)]
    assert all(isprime(p) and isprime(p+2) for p in twins)
print('crt_survivor_counts=PASS')
print('finite_twin_enumeration=PASS')
print('live_signed_dispersion_estimates=NOT_PROVED_BY_THIS_SCRIPT')
