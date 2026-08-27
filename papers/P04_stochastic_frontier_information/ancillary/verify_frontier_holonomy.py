from __future__ import annotations
import itertools,math,random
random.seed(777)

def audit_frame(n:int):
    labels=[random.randrange(max(1,n//3)) for _ in range(n)]
    marks=[random.randrange(3) for _ in range(n)]
    cells={}
    for i,l in enumerate(labels): cells.setdefault(l,[]).append(i)
    delta=sum(len({marks[i] for i in ids})-1 for ids in cells.values())
    pguess=sum(max(sum(1 for i in ids if marks[i]==b) for b in set(marks[i] for i in ids)) for ids in cells.values())/n
    sfi=-math.log2(pguess)
    assert (sfi>1e-14)==(delta>0)
    assert sfi+1e-14>=math.log2(n/(n-delta))
for n in range(2,42):
    for _ in range(25): audit_frame(n)

for n in range(3,7):
    for signs in itertools.product((-1,1),repeat=n):
        prod=math.prod(signs)
        valid=False
        for vals in itertools.product((-1,1),repeat=n):
            if all(vals[(i+1)%n]==signs[i]*vals[i] for i in range(n)):
                valid=True; break
        assert valid==(prod==1),(n,signs)
print('random_full_support_frames=1000 PASS')
print('cycle_sign_patterns_n3_to_n6=PASS')
