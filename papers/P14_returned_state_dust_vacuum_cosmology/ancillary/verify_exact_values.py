from __future__ import annotations
from math import sqrt,asinh,log
Ol=2/3; Om=1/3
z_eq=2**(1/3)-1
z_acc=2**(2/3)-1
H0t0=2/(3*sqrt(Ol))*asinh(sqrt(Ol/Om))
DeltaN=2*log(2)/3
assert abs(z_eq-0.259921050)<5e-10
assert abs(z_acc-0.587401052)<5e-10
assert abs(H0t0-0.9358813101)<5e-11
assert abs(DeltaN-0.4620981204)<5e-11
assert abs((0.5*Om-Ol)-(-0.5))<1e-15
print(f'z_eq={z_eq:.12f}')
print(f'z_acc={z_acc:.12f}')
print(f'H0t0={H0t0:.12f}')
print(f'DeltaN={DeltaN:.12f}')
print('exact_branch_values=PASS')
print('observational_status=MODEL_TEST_REQUIRED')
