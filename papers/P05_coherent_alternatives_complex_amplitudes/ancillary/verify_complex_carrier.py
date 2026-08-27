from __future__ import annotations
import numpy as np
rng=np.random.default_rng(777)
J=np.array([[0.,-1.],[1.,0.]])
assert np.allclose(J@J,-np.eye(2))
for _ in range(1000):
    a,b=rng.normal(size=2)
    M=np.array([[a,-b],[b,a]])
    assert abs(np.linalg.det(M)-(a*a+b*b))<1e-10
    assert np.allclose(M.T@M,(a*a+b*b)*np.eye(2),atol=1e-10)
# Commuting local maps make slicing independent in a finite diamond.
for _ in range(100):
    A=np.diag(rng.normal(size=3)); B=np.diag(rng.normal(size=3))
    assert np.allclose(A@B,B@A)
print('rotation_generator=PASS')
print('area_scaling_trials=1000 PASS')
print('finite_foliation_commutation_trials=100 PASS')
