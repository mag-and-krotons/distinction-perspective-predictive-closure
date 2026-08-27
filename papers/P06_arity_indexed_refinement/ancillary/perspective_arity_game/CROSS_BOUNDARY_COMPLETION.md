# Cross-boundary completion from complete prime-arity fibres

This is the boundary theorem that the preceding branch left open. It starts
with the already-derived arithmetic identity and cost character

\[
Z_0(s)=\sum_{n\ge1}n^{-s},\qquad \Re s>1,
\]

and with the transparent prime arities. It does **not** assume a gamma
completion, a functional equation, random signs, orthogonality between
primes, square-root cancellation, or a desired zero line.

The result has two parts. First, the full prime-arity fibres produce entire
boundary numerators whose compatibility gives a meromorphic continuation of
\(Z_0\). Second, their interaction gives exact zero constraints. It also
proves a limitation: after taking the complete least-boundary trace, the
prime family has analytic rank one, so that collapsed family cannot by itself
force a critical line.

## 1. Completeness correction

For a transparent arity \(p\), the first \(J\) generated capacity digits form

\[
D_{p,J}=(\mathbb Z/p\mathbb Z)^J.
\]

Its complete character fibre is its full dual. A character is indexed by an
independent vector

\[
\mathbf r=(r_0,\ldots,r_{J-1})\in(\mathbb Z/p\mathbb Z)^J
\]

and acts on the capacity digits of \(n\) by

\[
\boxed{
\chi_{p,\mathbf r}(n)
=\exp\!\left(\frac{2\pi i}{p}
  \sum_{j=0}^{J-1}r_jd_{p,j}(n)\right).
}
\]

The earlier family with one index \(r\) at every place retained only

\[
(r,r,\ldots,r),
\]

the diagonal \(p\)-element subfibre of a \(p^J\)-element fibre. It was
complete for one digit occurrence, but not for their interaction. Nothing in
that diagonal result is deleted; it is now classified correctly.

The full fibre obeys the exact finite orthogonality identity

\[
\boxed{
\sum_{\mathbf r}
\chi_{p,\mathbf r}(n)\overline{\chi_{p,\mathbf r}(m)}
=p^J\mathbf1_{n\equiv m\pmod{p^J}}.
}
\]

This identity is not a randomness assumption. It is the exhaustive sum over
all co-resultant characters of the finite distinction fibre.

## 2. The complete boundary trace

At digit place \(j\), retain every nontrivial character and do not select one.
Their negative complete trace is

\[
b_{p,j}(n)
=-\sum_{r=1}^{p-1}\exp\!\left(\frac{2\pi i r\,d_{p,j}(n)}p\right)
=
\begin{cases}
1-p,&d_{p,j}(n)=0,\\
1,&d_{p,j}(n)\ne0.
\end{cases}
\]

The least place is the interface seen by unit advance of the generated
integer identity. There

\[
d_{p,0}(n)=0\quad\Longleftrightarrow\quad p\mid n,
\]

so write

\[
\boxed{
b_p(n)=
\begin{cases}
1-p,&p\mid n,\\
1,&p\nmid n.
\end{cases}}
\]

One full period sums to zero. This cancellation is forced by character
completeness; no sign pattern has been chosen.

Define the prime boundary numerator initially by

\[
E_p(s)=\sum_{n\ge1}\frac{b_p(n)}{n^s}.
\]

It converges for \(\Re s>0\), because the periodic partial sums of \(b_p\)
are bounded. In \(\Re s>1\), absolute rearrangement gives

\[
\begin{aligned}
E_p(s)
&=\sum_{n\ge1}n^{-s}
 -p\sum_{m\ge1}(pm)^{-s}\\
&=\boxed{(1-p^{1-s})Z_0(s)}.
\end{aligned}
\]

Thus the multiplier is not inserted. It is the exact complete-character
trace of one prime-resultant boundary.

## 3. Each prime numerator is entire

This can be proved independently for every \(p\), before forming a quotient.
For \(t>0\), the periodic trace has exponential carrier

\[
B_p(t)
=\sum_{n\ge1}b_p(n)e^{-nt}
=\frac1{e^t-1}-\frac{p}{e^{pt}-1}.
\]

The two \(1/t\) singularities cancel. Hence \(B_p(t)\) is analytic at
\(t=0\) and decays exponentially at infinity. The normalized Laplace-Mellin
identity for \(n^{-s}\) therefore gives \(E_p\) in \(\Re s>0\).

For completeness, the continuation argument is as follows. On \((0,1)\),
subtract the first \(M\) terms of the Taylor series of \(B_p(t)\). The
remainder integral is analytic for \(\Re s>-M\); the subtracted monomials
produce only simple terms \(c_m/(s+m)\). The zeros of the elementary Mellin
normalization at \(s=0,-1,-2,\ldots\) cancel those terms. Since \(M\) is
arbitrary,

\[
\boxed{E_p(s)\text{ is entire for every transparent }p.}
\]

This proof uses the elementary integral representation of a power only as a
convergence lemma. No \(\Gamma(s/2)\), completed zeta function, or zeta
symmetry is assumed or placed in the resulting object.

## 4. Binary distinction gives an explicit global series

For \(p=2\), the trace is \(b_2(n)=(-1)^{n+1}\). The exhaustive binary
complete-difference transform gives

\[
\boxed{
H(s)=
\sum_{r=0}^{\infty}\frac1{2^{r+1}}
\sum_{k=0}^{r}(-1)^k\binom rk(k+1)^{-s}.
}
\]

In \(\Re s>1\), put \(a_k=(k+1)^{-s}\). The generating identity

\[
\sum_{r\ge k}\binom rk2^{-r-1}=1
\]

allows an absolutely convergent interchange and yields

\[
H(s)=\sum_{k\ge0}(-1)^ka_k=E_2(s).
\]

The series is entire, not merely conditionally meaningful. One direct
compact-set bound is obtained from

\[
D_r(s)=\sum_{k=0}^r(-1)^k\binom rk(k+1)^{-s}.
\]

For a compact set \(K\), the normalized Laplace representation is valid for
all sufficiently large \(r\), because its integrand behaves as
\(t^{r+s-1}\) at zero. Splitting at \(t=1\), and then putting \(u=e^{-t}\)
on the tail, gives constants \(C_K,A_K\) with

\[
|D_r(s)|\le
C_K\frac{(1+\log r)^{A_K}}r,
\qquad s\in K.
\]

The extra factor \(2^{-r-1}\) proves local uniform convergence on all of
\(\mathbb C\). Thus \(H=E_2\) is an explicit, globally convergent function
generated by binary distinction alone.

## 5. Cross-prime compatibility constructs the continuation

Write

\[
D_p(s)=1-p^{1-s}.
\]

In \(\Re s>1\), every independently constructed numerator satisfies
\(E_p=D_pZ_0\). Therefore, for every pair of transparent primes,

\[
\boxed{D_q(s)E_p(s)=D_p(s)E_q(s).}
\]

Both sides are entire, so the identity theorem extends this relation to every
\(s\in\mathbb C\). This is the cross-prime interaction law.

For distinct primes \(p\ne q\), the zero sets of \(D_p\) and \(D_q\) meet
only at \(s=1\). Indeed,

\[
D_p(s)=0
\quad\Longleftrightarrow\quad
s=1+\frac{2\pi i k}{\log p},
\]

and a nonzero common ordinate would make \(\log p/\log q\) rational, hence
\(p^a=q^b\) for positive integers \(a,b\), impossible for distinct primes.

Consequently, for every \(s\ne1\), choose any prime with \(D_p(s)\ne0\) and
define

\[
\boxed{Z(s)=\frac{E_p(s)}{D_p(s)}.}
\]

Cross-prime compatibility proves that the value is independent of the chosen
prime. It is locally holomorphic because a nonvanishing denominator remains
nonvanishing in a neighbourhood.

At \(s=1\), direct partial sums give

\[
E_p(1)
=\lim_{M\to\infty}(H_{pM}-H_M)
=\log p,
\]

while

\[
D_p(s)=(s-1)\log p+O((s-1)^2).
\]

Hence \(Z\) has exactly one simple pole there, with residue one. We have
therefore derived

\[
\boxed{
Z_0(s)\text{ has a meromorphic continuation to }\mathbb C,
\text{ with only the simple pole }s=1.
}
\]

No gamma factor or previously known zeta functional equation entered this
construction.

## 6. The zero constraints that actually follow

### 6.1 Presentation-cancellation zeros

At

\[
s_{p,k}=1+\frac{2\pi i k}{\log p},\qquad k\ne0,
\]

we have \(D_p(s_{p,k})=0\). Choose a distinct prime \(q\); then
\(D_q(s_{p,k})\ne0\), and compatibility forces

\[
\boxed{E_p(s_{p,k})=0.}
\]

These are zeros of the \(p\)-presentation numerator, not zeros of \(Z\).
They cancel the denominator introduced by that presentation.

### 6.2 Common-source zeros

At every \(\rho\ne1\),

\[
\boxed{
Z(\rho)=0
\quad\Longleftrightarrow\quad
E_p(\rho)=0\text{ for every transparent }p.
}
\]

If one chosen \(p\) also has \(D_p(\rho)\ne0\), its single equality
\(E_p(\rho)=0\) is already equivalent. In particular, throughout

\[
0<\Re s<1,
\]

all \(D_p\) are nonzero because \(|p^{1-s}|=p^{1-\Re s}>1\). Therefore

\[
\boxed{
0<\Re\rho<1:\quad
Z(\rho)=0
\Longleftrightarrow
H(\rho)=0
\Longleftrightarrow
E_p(\rho)=0\ \forall p.
}
\]

The globally convergent equation \(H(\rho)=0\) is consequently an explicit
zero-prediction equation produced by the distinction construction.

### 6.3 Negative even zeros from binary complement

The negative-integer values of \(H\) have exponential generating function

\[
\begin{aligned}
A(t)
&=\sum_{m\ge0}H(-m)\frac{t^m}{m!}\\
&=\sum_{r\ge0}\frac{e^t(1-e^t)^r}{2^{r+1}}\\
&=\frac{e^t}{1+e^t}
\end{aligned}
\]

near \(t=0\). Binary complement gives

\[
A(t)+A(-t)=1.
\]

Thus every positive even coefficient vanishes:

\[
\boxed{H(-2m)=0\quad(m\ge1).}
\]

Since \(D_2(-2m)\ne0\), these are zeros of \(Z\), not presentation
cancellations. They have emerged without Bernoulli numbers, a gamma factor,
or a borrowed functional equation.

All coefficients in the binary construction are real, so it also forces

\[
Z(\overline s)=\overline{Z(s)};
\]

nonreal zeros occur in conjugate pairs.

## 7. The rank-one theorem and the corrected RH status

After the complete least-boundary trace is taken,

\[
E_p(s)=D_p(s)Z(s).
\]

Hence the family \(\{E_p\}_p\), over the field of meromorphic scalar
functions, has rank one. Every cross-prime relation among these collapsed
traces factors through the single carrier \(Z\). Therefore:

\[
\boxed{
\text{the collapsed prime-boundary interactions cannot independently force}
\ \Re\rho=\tfrac12.
}
\]

This is not another unperformed “remaining theorem.” It is a proved no-go
result for the route that had repeatedly been described as the missing step.
That description was wrong. The route does accomplish three substantive
things: global continuation, the exact presentation-zero lattice, and an
explicit common-zero equation. It does not prove RH.

The source has also shown exactly where information was lost: taking
\(-\sum_{r=1}^{p-1}\) at one place collapses the \(p^J\)-member complete
character fibre to one scalar. Any further zero-location law must be sought
in the uncollapsed vectors \(\chi_{p,\mathbf r}\) and their cross-place
interactions, not asserted to arise from the rank-one traces already summed.

