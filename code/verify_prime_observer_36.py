#!/usr/bin/env python3
"""Exact finite verifier for the nine-state / 36-relation closure theorem."""
from __future__ import annotations
import cmath, itertools, json, math

PRIMES=(2,3,5,7)
COMPOSITES=(4,6,8,9)
PAIRS=((2,9),(3,8),(5,6),(7,4))

def sigma(d:int)->int: return (1-d)%10

def matmul(a,b):
    n=len(a); return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def matsub(a,b): return [[x-y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]

def generator(a,b,n=9):
    m=[[0]*n for _ in range(n)]
    ia,ib=a-1,b-1
    m[ia][ib]=1; m[ib][ia]=-1
    return m

def mobius_digit(d:int)->int:
    if d==1:return 1
    if d in PRIMES:return -1
    if d==6:return 1
    return 0

def static_class(d:int)->str:
    if d==0:return 'zero'
    if d==1:return 'unit'
    if d in PRIMES:return 'prime'
    if d==6:return 'squarefree-composite'
    return 'repeated-prime'

def predictive_state(n:int):
    support=set()
    for p in PRIMES:
        e=0
        while n%p==0:
            n//=p;e+=1
        if e>=2:return ('repeat',)
        if e==1:support.add(p)
    if n!=1:return ('outside-digit-prime-alphabet',n,tuple(sorted(support)))
    return ('support',tuple(sorted(support)))

def update(state,p):
    if state[0]=='repeat':return state
    if state[0]!='support':raise ValueError(state)
    s=set(state[1])
    if p in s:return ('repeat',)
    s.add(p);return ('support',tuple(sorted(s)))

def dft_mag(x):
    n=len(x); out=[]
    for k in range(n):
        z=sum(x[j]*cmath.exp(-2j*math.pi*j*k/n) for j in range(n))
        out.append(round(abs(z),12))
    return out

def main():
    assert [sigma(d) for d in range(10)]==[1,0,9,8,7,6,5,4,3,2]
    assert all(sigma(sigma(d))==d for d in range(10))
    assert all(sigma(p) in COMPOSITES for p in PRIMES)
    assert {frozenset((p,sigma(p))) for p in PRIMES}=={frozenset(x) for x in PAIRS}
    edges=list(itertools.combinations(range(1,10),2))
    assert len(edges)==36
    unit=[e for e in edges if 1 in e]
    ret=[e for e in edges if frozenset(e) in {frozenset(x) for x in PAIRS}]
    transverse=[e for e in edges if e not in unit and e not in ret]
    assert (len(unit),len(ret),len(transverse))==(8,4,24)
    gens=[generator(*x) for x in PAIRS]
    zero=[[0]*9 for _ in range(9)]
    for i in range(4):
        for j in range(i+1,4):
            assert matsub(matmul(gens[i],gens[j]),matmul(gens[j],gens[i]))==zero
    # Static five-class reporter is not a congruence under prime multiplication.
    assert static_class(2)==static_class(3)=='prime'
    assert static_class(2*2)!=static_class(3*2)
    # Complete support state updates deterministically.
    assert update(predictive_state(2),2)==('repeat',)
    assert update(predictive_state(3),2)==predictive_state(6)
    # Prime/composite indicator sequences are cyclically isospectral.
    p=[1 if d in PRIMES else 0 for d in range(10)]
    c=[1 if d in COMPOSITES else 0 for d in range(10)]
    assert dft_mag(p)==dft_mag(c)
    result={
      'status':'PASS','states':9,'relations':36,'decomposition':[8,4,24],
      'prime_return_sectors':list(PRIMES),'static_five_class_false_closure':True,
      'commuting_return_generators':4,'fourier_magnitude_match':True,
      'physical_quantum_number_claimed':False,'absolute_111_hz_constant_claimed':False,
    }
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
