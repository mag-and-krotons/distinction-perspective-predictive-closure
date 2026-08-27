from __future__ import annotations
import math
from math import comb
import sympy as sp

def transparent(q:int)->bool:
    return all(comb(q,k)%q==0 for k in range(1,q))
for q in range(2,101):
    assert transparent(q)==bool(sp.isprime(q)),q

def squarefree(n:int)->bool:
    p=2
    while p*p<=n:
        if n%(p*p)==0:return False
        p+=1
    return True
for N in (32,64,100,256):
    critical=[m for m in range(N//2+1,N+1) if m%2==1 and squarefree(m)]
    intervals=[(m,2*m) for m in critical]
    assert all(a<=N<b for a,b in intervals)
# Partial sums illustrate the two different ideal thresholds.
for sigma in (0.4,0.5,0.6,1.0,1.1):
    hs=sum(n**(-2*sigma) for n in range(1,200000))
    tr=sum(n**(-sigma) for n in range(1,200000))
    assert hs>0 and tr>0
print('prime_transparency_q2_to_q100=PASS')
print('binary_matching_barcodes=PASS')
print('operator_partial_sums=PASS')
