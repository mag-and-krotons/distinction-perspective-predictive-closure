from __future__ import annotations
import numpy as np
rng=np.random.default_rng(777)
for _ in range(500):
    U=rng.normal(size=(5,3))+1j*rng.normal(size=(5,3))
    a=np.linalg.eigvalsh(U@U.conj().T)
    b=np.linalg.eigvalsh(U.conj().T@U)
    a=a[a>1e-9]; b=b[b>1e-9]
    assert np.allclose(a,b,rtol=1e-9,atol=1e-9)
for _ in range(500):
    Ux=rng.normal(size=(4,4)); Uy=rng.normal(size=(4,4)); Vx=rng.normal(size=(4,4)); Vy=rng.normal(size=(4,4))
    d1=Ux@Vy-Uy@Vx
    d2=Vx@Uy-Vy@Ux
    assert abs(np.trace(d1+d2))<1e-9
# Scaling check.
Ux=rng.normal(size=(4,4)); Uy=rng.normal(size=(4,4)); Vx=rng.normal(size=(4,4)); Vy=rng.normal(size=(4,4))
def values(e):
    off=e*(Ux-Uy)
    diag=e*e*(Ux@Vy-Uy@Vx)
    return np.linalg.norm(off),np.linalg.norm(diag)
a1,b1=values(1e-2);a2,b2=values(2e-2)
assert abs(a2/a1-2)<1e-10 and abs(b2/b1-4)<1e-10
print('conversion_isospectrality_trials=500 PASS')
print('trace_exchange_trials=500 PASS')
print('first_second_order_scaling=PASS')
