from __future__ import annotations
import itertools
S=range(4)
functions=list(itertools.product((0,1),repeat=4))
checked=0
for K1 in functions:
  for K2 in functions:
    fibres={}
    for s in S: fibres.setdefault((K1[s],K2[s]),[]).append(s)
    for J in functions:
      boundary=any(J[a]!=J[b] for ids in fibres.values() for a in ids for b in ids)
      factors=all(len({J[s] for s in ids})==1 for ids in fibres.values())
      assert (not boundary)==factors
      checked+=1
for dG,dQ in ((2,2),(3,3),(2,4)):
    omitted=(dG*dG-1)*(dQ*dQ-1)
    joint=(dG*dQ)**2-1
    marg=(dG*dG-1)+(dQ*dQ-1)
    assert joint-marg==omitted
print(f'factorization_cases={checked} PASS')
print('joint_coordinate_count=PASS')
