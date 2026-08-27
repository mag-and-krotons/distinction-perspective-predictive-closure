from __future__ import annotations
import csv
from pathlib import Path

def mobius_sieve(n:int):
    mu=[0]*(n+1); primes=[]; composite=[False]*(n+1); mu[1]=1
    for i in range(2,n+1):
        if not composite[i]: primes.append(i); mu[i]=-1
        for p in primes:
            if i*p>n: break
            composite[i*p]=True
            if i%p==0:
                mu[i*p]=0; break
            mu[i*p]=-mu[i]
    return mu
expected={10:(-1,11),100:(1,143),1000:(2,1479),10000:(-23,15829),100000:(-48,157055),1000000:(212,1645995)}
mu=mobius_sieve(max(expected)); M=[0]*len(mu)
for i in range(1,len(mu)):M[i]=M[i-1]+mu[i]
for N,(mn,an) in expected.items():
    A=sum(M[N//q]**2 for q in range(1,N+1))
    assert M[N]==mn,(N,M[N],mn)
    assert A==an,(N,A,an)
print('mertens_capacity_table=PASS')
