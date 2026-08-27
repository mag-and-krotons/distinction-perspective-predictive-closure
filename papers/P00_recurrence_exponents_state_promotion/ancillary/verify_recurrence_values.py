from __future__ import annotations
import math

EIGENVALUES=(0.35301358,0.27498875,0.19041902)
chi=math.log(EIGENVALUES[0])
assert abs(chi-(-1.0412496))<2e-6
assert all(0<x<1 for x in EIGENVALUES)

# Critical-band examples: all have zero exponential rate but distinct secondary behavior.
def estimate(seq, n=20000):
    return math.log(abs(seq(n))/abs(seq(1)))/n
examples={
    'inverse_linear':lambda n:1/n,
    'constant':lambda n:1.0,
    'logarithmic':lambda n:math.log1p(n),
    'quadratic':lambda n:n*n,
    'subexponential':lambda n:math.exp(math.sqrt(n)),
}
for name,f in examples.items():
    assert abs(estimate(f))<0.02, (name,estimate(f))
print(f'dominant_transient_chi={chi:.10f}')
print('critical_band_examples=PASS')
