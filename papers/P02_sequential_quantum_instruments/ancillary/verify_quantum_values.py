from __future__ import annotations
import math
import numpy as np

def h2(p: float) -> float:
    if p in (0.0,1.0): return 0.0
    return -p*math.log2(p)-(1-p)*math.log2(1-p)

expected={4:(1.6009,1.0000,0.5000),6:(1.3546,0.8113,0.7500),8:(1.2333,0.6009,0.8536)}
for n,(seed,rate,guess) in expected.items():
    seed_calc=1+h2(math.sin(math.pi/(2*n))**2)
    rate_calc=h2(math.cos(math.pi/n)**2)
    guess_calc=math.cos(math.pi/n)**2
    assert abs(seed_calc-seed)<6e-5,(n,seed_calc)
    assert abs(rate_calc-rate)<6e-5,(n,rate_calc)
    assert abs(guess_calc-guess)<6e-5,(n,guess_calc)

sqrt5=math.sqrt(5)
r_no=2*(5+sqrt5)/(15+sqrt5)
c_min=6*(5+sqrt5)/(5*(15+sqrt5))
r_uniform=2*(5+sqrt5)/(35-3*sqrt5)
yes_only=5*(3-sqrt5)/2
assert abs(r_no-0.8396425434)<5e-11
assert abs(c_min-0.5037855260)<5e-11
assert abs(r_uniform-0.5115311845)<5e-11
assert abs(yes_only-1.9098300563)<5e-11

C=np.array([
[0.43696297,0.19810609,0.20644079,0.14060033],
[0.16017410,0.46165671,0.13951861,0.22362294],
[0.24443666,0.11892971,0.46061556,0.17659060],
[0.15842628,0.22130750,0.19342504,0.45918613],
],dtype=float)
assert np.allclose(C.sum(axis=0),1,atol=2e-8)
w,v=np.linalg.eig(C)
idx=int(np.argmin(np.abs(w-1)))
pi=np.real(v[:,idx]); pi=pi/pi.sum()
assert np.allclose(pi,[0.24327934,0.24563854,0.24991431,0.26116781],atol=2e-8)
nontriv=sorted([float(np.real(x)) for x in w if abs(x-1)>1e-6],reverse=True)
assert np.allclose(nontriv,[0.35301358,0.27498875,0.19041902],atol=2e-8)
H=lambda a: -sum(float(x)*math.log2(float(x)) for x in a if x>0)
stationary_entropy=H(pi)
entropy_rate=sum(float(pi[j])*H(C[:,j]) for j in range(4))
predictive=stationary_entropy-entropy_rate
pguess=sum(float(pi[j])*float(np.max(C[:,j])) for j in range(4))
min_entropy=-math.log2(pguess)
assert abs(stationary_entropy-1.9994586368)<2e-9
assert abs(entropy_rate-1.8413629168)<3e-9
assert abs(predictive-0.1580957201)<3e-9
assert abs(pguess-0.4547437955)<5e-9
assert abs(min_entropy-1.1368741409)<2e-8
print('entropy_table=PASS')
print('kcbs_thresholds=PASS')
print('marked_transition=PASS')
print(f'stationary_entropy={stationary_entropy:.10f}')
print(f'entropy_rate={entropy_rate:.10f}')
print(f'predictive_information={predictive:.10f}')
