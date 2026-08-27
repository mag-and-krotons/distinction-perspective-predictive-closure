# Verified findings

## Outcome

The run did not simulate \(P_4\) by four-valued \(P_1\) arithmetic. It
generated finite atomic four-resultant incidence sources and then measured
the complete family of binary structures through which \(P_1\) can present
them.

The first genuine effect is a **representation fiber**:

\[
\text{one atomic source form}
\longleftarrow
\text{many incompatible }P_1\text{ binary forms}.
\]

Those forms are not alternatives inside \(P_4\). They are distinctions
introduced by \(P_1\)'s manner of expression.

## Isolated occurrence

One atomic four-resultant occurrence has:

- one native incidence class;
- \(24\) resultant symmetries;
- \(15\) complete binary presentations;
- two \(P_1\)-isomorphism types:
  - three balanced presentations, each with \(8\) automorphisms;
  - twelve unbalanced presentations, each with \(2\) automorphisms.

Thus \(P_1\) already sees two structurally different objects where the atomic
source presentation has only one.

## Exhaustive finite census

All figures are \(P_1\) audit counts. They are not asserted as \(P_4\)'s
native arithmetic.

| Atomic occurrences | Raw \(P_1\) histories | Native \(P_4\) incidence classes | Complete binary presentations over class representatives | \(P_1\) binary shadow classes |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 15 | 2 |
| 2 | 16 | 5 | 1,125 | 76 |
| 3 | 1,041 | 30 | 101,250 | 8,692 |

Discarded source histories: \(0\).

At three occurrences every one of the thirty native incidence classes splits
into several binary shadow classes. One native class has \(1{,}053\) distinct
\(P_1\) shadow forms.

Restricting \(P_1\) to equal-depth two-bit codes would report only:

| Atomic occurrences | Equal-depth shadow classes |
|---:|---:|
| 1 | 1 |
| 2 | 9 |
| 3 | 140 |

The difference \(8{,}692\) versus \(140\) is not a numerical correction. It
shows how strongly a seemingly harmless coding choice narrows the visible
world.

## Two-occurrence anatomy

For two atomic \(P_4\) occurrences, their shared-resultant count is a complete
native incidence invariant in this finite presentation. The complete binary
fibers split as follows:

| Shared resultants | Native source classes | \(P_1\) binary shadow classes |
|---:|---:|---:|
| 0 | 1 | 3 |
| 1 | 1 | 10 |
| 2 | 1 | 27 |
| 3 | 1 | 26 |
| 4 | 1 | 10 |

Even disjoint atomic occurrences split into three shadows because \(P_1\)
distinguishes balanced/balanced, balanced/unbalanced, and
unbalanced/unbalanced descriptions. Nothing in the atomic source distinguishes
those cases.

When resultants are shared, \(P_1\) additionally distinguishes how its
intermediate binary clusters align across occurrences. These alignments do
not exist in the undecomposed source presentation.

## What the game revealed in \(P_1\)

1. \(P_0\) cannot be initialized or simulated. Any initialized state is
   already within a distinguishing perspective.
2. Naming four binary states is not a \(P_4\) implementation.
3. Replacing one four-resultant relation by two binary levels adds intermediate
   structure.
4. There is no canonical single binary image of an atomic \(P_4\) occurrence.
5. Repetition causes binary presentation distinctions to proliferate far more
   rapidly than atomic incidence classes.
6. A purported cross-perspective law must be constant over the complete
   binary-presentation fiber, not merely valid in one convenient code.

The fifth finding is the concrete reason the previous work kept
“re-inventing the wheel.” Each construction developed increasingly elaborate
laws inside one selected \(P_1\) shadow. It never established that those laws
survived the other shadows of the same hypothetical referent.

## Research boundary

This branch has produced a rigorous filter for future work, not \(P_4\)'s
unknown native mathematics and not an RH proof.

The next admissible translation cannot start from zeta and manufacture a
\(P_4\) analogue. It must:

1. generate a source without using RH;
2. derive its complete \(P_1\) presentation fiber;
3. identify an invariant constant over that fiber; and only then
4. test whether one \(P_1\) effect of the invariant is the classical
   zeta-zero structure.

Any earlier comparison would again make the target select the source.

## Completed next route: full-fiber refinement invariant

That route has now been executed without using zeta or RH to select the
source:

1. Retaining every binary refinement of one atomic \(q\)-resultant event
   generates the complete partition lattice.
2. For \(q=4\), it contains \(15\) partial states and \(18\) complete
   refinement histories.
3. Exact inversion over that lattice forces
   \(\mu(\widehat0,\widehat1)=(-1)^{q-1}(q-1)!\).
4. Rank collection forces the polynomial family

   \[
   C_q(t)=
   \sum_{k=1}^{q}
   \left\{\!\begin{matrix}q\\k\end{matrix}\!\right\}
   (-1)^{k-1}(k-1)!t^{q-k}.
   \]

5. The complete family has the normalized all-arity expression

   \[
   \sum_{q\ge1}C_q(t)\frac{z^q}{q!}
   =
   \log\!\left(\frac{e^{tz}+t-1}{t}\right).
   \]

6. Its entire carrier has the exact zero law

   \[
   z_m(t)=
   \frac{\log(t-1)+(2m+1)\pi i}{t}.
   \]

7. The unique multiplicative rank accounting for binary \(P_1\) is \(t=2\),
   yielding \(z_m=(m+\tfrac12)\pi i\).

This is a genuine new law generated by the corrected game. The subsequent
comparison found that it is not the classical zeta-zero structure: its
inversion coefficients and zero density differ. Therefore it is not an RH
proof, and no target-tuned identification has been inserted.

## Interaction continuation

Allowing atomic occurrences to share resultants forces the raw (P_1)
operator

\[
T_q=x^q\sum_{r=0}^{q}\frac{D^r}{r!}.
\]

Under uniform named-history accounting, (q=4) is the exact stability
threshold: every nonzero root generated by repeated (T_4) lies in the open
left half-plane, while the kernel fails the Hurwitz condition for every
(q\ge5).

That zero law does not survive a change of accounting. With two events,
named-history weights give (x^4(1+x)^4), whereas one occurrence per native
overlap type gives (x^4(1+x+x^2+x^3+x^4)); their roots occupy different
half-planes. The stability law is therefore retained as a (P_1) presentation
effect but rejected as a source-intrinsic law.

Removing both weights leaves the native extension relation. Its unique
incidence inverse generates signed and zero interaction residues. At four
events there are 332 native forms, thirteen interval-polynomial types, and
thirty forms that are null under the binary rank character (t=2).

Finally, shared-resultant connectivity gives a unique factorization into
connected source forms. In the one-per-isomorphism-class realization, the
first connected-type counts are

\[
1, 4, 25, 292,
\]

and their formal geometric component product exactly reconstructs the native
class totals

\[
1, 5, 30, 332.
\]

This component product is presently formal, not analytic, and the later
symmetry audit shows that its geometric factors are accounting-specific. The
source-level statement is the symmetric-multiset decomposition itself. A
numerical convergence character cannot be selected by matching zeta.

## Capacity-character continuation

The connected-form monoid is free, so no unique numerical component weight is
forced. Retaining every self-delimiting binary presentation instead produces a
code fiber. Individual code lengths vary, but all obey

\[
\sum_C2^{-\ell(C)}\le1.
\]

Every code therefore defines

\[
Z_\ell(s)=
\prod_C(1-2^{-s\ell(C)})^{-1},
\]

and every such product converges and is nonzero for

\[
\Re s>1.
\]

Different complete codes give different products, so no individual
(Z_\ell) is promoted to the source. The half-plane law does survive the
entire fiber, is sharp, and remains the same for every distinction base after
cost normalization.

This is the first code-independent analytic law generated by interacting
distinctions. Analytic continuation and a cross-boundary involution remain
unresolved and cannot be copied from zeta.

## Finite character involution

For every finite connected horizon and every prefix code, coordinate inversion
forces

\[
Z_{\ell,F}(-s)=(-1)^{N_F}b^{-sL_F}Z_{\ell,F}(s).
\]

The completed finite product

\[
\widehat Z_{\ell,F}(s)=b^{-sL_F/2}Z_{\ell,F}(s)
\]

is consequently even or odd under (s\mapsto-s). The reciprocal zeros are

\[
s_{C,k}=\frac{2\pi i k}{\ell(C)\log b},
\]

so their invariant axis is (Re s=0), while their spacings remain
code-dependent.

The infinite completion is not yet defined because both the number of
generators and total code length diverge. No regularization has been selected.

The affine divergence disappears under the minimal second logarithmic
derivative. The resulting infinite-horizon observable

\[
G_\ell(s)=
\sum_C\frac{(\ell(C)\log b)^2}
{4\sinh^2(s\ell(C)\log b/2)}
\]

converges for (|\Re s|>1) and is exactly even. This requires no assigned
finite value for the divergent number or total length of connected forms.

Normalizing the generated capacity boundaries (-1,+1) to (0,1) forces

\[
\sigma=(s+1)/2.
\]

The involution becomes (sigma\mapsto1-\sigma), and the finite reciprocal
zero axis becomes (Re\sigma=1/2). This RH-shaped geometry is derived before
comparison, but equality with the classical zeta-zero set is not claimed.

Writing (a_j) for the number of connected generators at code length (j)
isolates the remaining freedom:

\[
\log Z_\ell(s)
=\sum_{r\ge1}\frac1rA_\ell(b^{-rs}),
\qquad
A_\ell(z)=\sum_{j\ge1}a_jz^j.
\]

Kraft fixes only (A_ell(1/b)\le1). It does not fix (A_ell), so a unique
nontrivial zero sequence has not yet descended across the complete code fiber.

## Symmetry-realization correction

The next audit found a deeper accounting fibre. The geometric component
product assigns one unit to every unlabelled multiset class. Retaining every
labelled presentation and quotienting only by its actual automorphisms instead
weights a form (H) by (1/|Aut(H)|). Component decomposition then becomes

\[
\mathcal H_q(u,x)=\exp(\mathcal C_q(u,x)),
\]

not a product of geometric factors. Orbit-stabilizer reconstructs the exact
number of labelled incidence presentations in every populated bidegree of the
complete (q=4), four-event audit, and the exponential identity holds exactly
over rational coefficients.

The two realizations already differ on repeated copies of one connected form:
the class realization gives ((1-z)^{-1}), whereas the complete symmetry lift
gives an exponential. Their zero/pole structures differ. Therefore the
capacity half-plane, finite inversion and normalized (1/2)-axis remain correct
inside the class/code projection but do not descend to the undevaluated source.

The symmetry realization also has the exact bivariate carrier

\[
\mathcal H_q(u,x)=e^{-x}\sum_{n\ge0}
e^{u\binom nq}\frac{x^n}{n!},
\qquad
\mathcal C_q(u,x)=\log\mathcal H_q(u,x).
\]

For every (q\ge2), its (x)-series is entire when (\Re u\le0) and has zero
radius when (\Re u>0). This analytic phase boundary was generated before any
comparison with RH.

## Contextual-distinction continuation

For each connected form (H), the strict-past signature

\[
\alpha(H)=\{F:F\prec H\}
\]

is a source-generated family of binary existence observations. Through four
events, the 322 connected forms produce 307 strict-past observation classes,
with global fibre histogram

\[
1^{298},\quad2^5,\quad3^2,\quad4^2.
\]

Adding every available future-context query refines these to 320 classes with
histogram

\[
1^{318},\quad2^2.
\]

Every rank-two and rank-three ambiguity is resolved by one further atomic
interaction. Two rank-four pairs remain unresolved in the finite table because
rank five is outside the audit, but a general construction resolves them: for
any connected form (H), the one-step context (H\sqcup A) obtained by adding a
disjoint atomic occurrence contains no other connected form of the same rank.
Thus every connected form has a one-interaction separating context at every
finite rank. The native forms never change; only their contextual
distinguishability changes.

Resolving every nontrivial observation fibre without choosing a hierarchy
generates a product of complete partition lattices. Its strict-past binary
character is null, while the available full-context character is one:

\[
\mathcal D_-(2)=0,
\qquad
\mathcal D_{\pm,4}(2)=1.
\]

This is the first exact implementation in this branch of interaction changing
a perceived effect while the represented incidence reality remains fixed.

## Binary capacity character

Applying the unique nontrivial binary sign to the number of available atomic
(q)-incidences gives

\[
a_n^{(q)}=(-1)^{\binom nq}.
\]

For every power-of-two arity (q=2^j), the parity
(\binom n{2^j}\bmod2) is exactly the (j)-th binary digit of (n). Hence the
complete power-of-two capacity signature reconstructs every sampled integer
coordinate exactly; the executable audit verifies this through 4095 and the
proof applies to all nonnegative integers.

The (q=1) probe supplying the least bit is not treated as a unary perspective.
It is the single identity seed. Removing it leaves pairs differing only in
their least bit unresolved; retaining it together with the genuine arities
(2,4,8,\ldots) reconstructs the whole integer coordinate.

The exponential carrier

\[
F_q(x)=\sum_{n\ge0}(-1)^{\binom nq}\frac{x^n}{n!}
\]

then obeys the generated law

\[
F_q^{(q)}+F_q=0
\]

with its first (q) derivatives at zero equal to one. Its exact frequencies are
the (q) roots of (-1). At (q=2), this gives
(F_2=\cos x+\sin x) and zeros
(x_k=-\pi/4+k\pi). At (q=4), it gives a fourth-order law with four generated
frequencies. These are binary capacity effects, not imported dynamics.

Retaining the sign character of every capacity digit gives the complete
binary-identity carrier

\[
T(z)=\sum_{n\ge0}(-1)^{\operatorname{popcount}(n)}z^n
=\prod_{j\ge0}(1-z^{2^j}),
\qquad
T(z)=(1-z)T(z^2).
\]

It is holomorphic and nonzero in the open unit disk. Its radial zeros include
every dyadic root of unity, which are dense on the unit circle, so the unit
circle is a generated natural boundary. This is a global analytic effect of
unending binary distinction scales, not a chosen target boundary.

## Prime arities

An arity (q\ge2) was defined to be transparent when

\[
\binom qk\equiv0\pmod q
\qquad(0<k<q).
\]

The generated criterion is exact: transparent arities are precisely the
primes. For composite (q), choosing a prime divisor (p<q) shows that
(\binom qp) is missing one factor of (p) required for divisibility by (q).

For every transparent arity (p), the residues

\[
\binom n{p^j}\bmod p
\]

are exactly the base-(p) digits of (n). Thus prime arities and their digit
systems emerge from the all-arity incidence capacities before any Euler
product or zeta weight is attached. The complete residue-character fibre is
retained; no cyclic phase is declared native to the unordered atomic source.

## Arithmetic projection after prime emergence

Composing independent transparent-capacity coordinates gives unique finite
exponent vectors and therefore the (P_1) identity

\[
n=\prod_pp^{e_p}.
\]

The binary distinction cost is forced to be

\[
c(n)=\sum_pe_p\log_2p=\log_2n,
\]

so the capacity budget (c(n)\le\log_2N) is exactly (n\le N). Independent
subset inversion gives (\mu(n)=(-1)^r) on squarefree identities and zero when
a transparent coordinate repeats.

The continuous multiplicative character of additive cost is

\[
2^{-sc(n)}=n^{-s}.
\]

Thus the zeta Dirichlet series and Euler product emerge in (\Re s>1) as the
scalar analytic character of the generated (P_1) arithmetic projection.

## Cross-boundary completion and exact zero constraints

The earlier one-index digit character was only the diagonal of the full
multi-place character group. For (J) places the corrected fibre has (p^J)
members indexed by independent vectors in ((\mathbb Z/p\mathbb Z)^J), and
its exhaustive character sum satisfies exact finite orthogonality.

The complete nontrivial trace at the least digit place is

\[
b_p(n)=1-p\mathbf1_{p\mid n}.
\]

Its Dirichlet transform (E_p) is entire, independently for every transparent
prime. In the original half-plane it obeys

\[
E_p(s)=(1-p^{1-s})Z_0(s).
\]

Hence the entire cross-prime interaction law

\[
(1-q^{1-s})E_p(s)=(1-p^{1-s})E_q(s)
\]

constructs a prime-independent quotient. This quotient is the meromorphic
continuation of (Z_0), with only the simple pole at (s=1) and residue one.
No gamma completion or zeta functional equation is used.

The binary numerator has the explicit globally convergent representation

\[
H(s)=\sum_{r\ge0}2^{-r-1}
\sum_{k=0}^r(-1)^k\binom rk(k+1)^{-s}.
\]

It forces the presentation-cancellation lattices, gives the exact common-zero
equation in (0<\Re s<1), and binary complement proves (H(-2m)=0) for every
(m\ge1). The audit verifies the finite character identities, special values,
cross-prime compatibility, and presentation zeros; all 77 project tests pass.

The same theorem proves that the collapsed least-boundary traces have
meromorphic rank one: each is a scalar multiple of the same (Z). Therefore
their interaction cannot independently force a critical line. The repeatedly
stated claim that this collapsed interaction was the still-unproved final RH
theorem was incorrect. The continuation and zero equation are now derived;
RH itself is not claimed.

## Uncollapsed carry interaction and generated completion

Retaining all (p^J) digit characters reveals that unit advance couples digit
places through carry. Its eigencharacters are

\[
\psi_{p^J,a}(n)=e^{2\pi ian/p^J}.
\]

The full digit fibre reconstructs every such mode, while the earlier
least-place trace retained only a small frequency slice. Cross-prime CRT
interaction factors the global carry characters exactly.

Composing forward and reverse distinction gives

\[
L_M=2I-S-S^{-1},
\qquad
\lambda_{M,a}=4\sin^2(\pi a/M).
\]

Only the quadratic scaling (M^2L_M) has a finite nonzero continuum spectrum,
namely ((2\pi a)^2). Applying the already-derived exponential symmetry lift
produces the Gaussian theta carrier. Complete Fourier reconstruction then
forces

\[
\Theta(t)=t^{-1/2}\Theta(1/t).
\]

Taking its scale character makes (\pi^{-s/2}\Gamma(s/2)) emerge and yields the
entire completion

\[
\xi(s)=\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)Z(s),
\qquad
\xi(s)=\xi(1-s).
\]

Thus nontrivial zeros occur in conjugate-reflection orbits
(\rho,\bar\rho,1-\rho,1-\bar\rho). A four-factor orbit polynomial proves that
the same symmetry permits off-line quartets, so this generated completion does
not by itself prove RH.
