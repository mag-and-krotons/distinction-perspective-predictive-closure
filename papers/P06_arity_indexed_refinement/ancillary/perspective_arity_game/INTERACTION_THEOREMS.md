# Interaction closure: derivation, correction, and surviving laws

Everything below is expressed in (P_1). The only source operation remains
atomic distinction. Interaction means only that two atomic occurrences may
share co-resultants. No probability, metric, field, arithmetic, or RH datum is
introduced.

## 1. Complete raw interaction recurrence

Let (a^{(q)}_{m,n}) be the number of retained, separately distinguished
(P_1) histories having (m) atomic (q)-resultant occurrences and (n)
presented resultants. Define

\[
A^{(q)}_m(x)=\sum_n a^{(q)}_{m,n}x^n,
\qquad A^{(q)}_0(x)=1.
\]

If the next occurrence shares (r) of the (n) existing resultants, there
are \(\binom nr\) named sharing choices and (q-r) fresh resultants. Retaining
all (0\le r\le q) therefore forces

\[
\boxed{
A^{(q)}_{m+1}(x)
=x^q\sum_{r=0}^{q}\frac{1}{r!}
\frac{d^r}{dx^r}A^{(q)}_m(x).
}
\]

Write

\[
E_q(z)=\sum_{r=0}^{q}\frac{z^r}{r!},
\qquad T_q=x^qE_q(D).
\]

Then (A_{m+1}^{(q)}=T_qA_m^{(q)}). Equivalently, the event-coordinate
exponential series satisfies the generated evolution equation

\[
\frac{\partial\mathcal A_q}{\partial u}
=x^qE_q(\partial_x)\mathcal A_q,
\qquad
\mathcal A_q(0,x)=1.
\]

Here (u), (x), event number and resultant number are (P_1) audit
coordinates. They are not asserted to be time, space, or native quantities in
another perspective.

For (q=4), the first layers are

\[
\begin{aligned}
A_1(x)&=x^4,\\
A_2(x)&=x^4(x+1)^4,\\
A_3(x)&=x^{12}+12x^{11}+62x^{10}+180x^9+321x^8\\
&\quad+304x^7+136x^6+24x^5+x^4.
\end{aligned}
\]

At (x=1), the retained raw-history sequence begins

\[
1, 16, 1041, 168481, 54344712, 30663168463.
\]

The executable recurrence exactly agrees with the earlier exhaustive
generator through three events.

## 2. A sharp stability threshold in that accounting

The kernel (E_q) has every zero in the open left half-plane exactly for
(1\le q\le4).

### Proof

After multiplying by (q!), its leading coefficients are

\[
z^q+qz^{q-1}+q(q-1)z^{q-2}
+q(q-1)(q-2)z^{q-3}+\cdots.
\]

For (q\ge4), the third Hurwitz determinant is

\[
\begin{aligned}
\Delta_3
&=a_1a_2a_3-a_3^2-a_1^2a_4\\
&=q^2(q-1)(q-2)(-q^2+5q-2).
\end{aligned}
\]

It is positive at (q=4) and negative for every (q\ge5), so stability is
impossible from (q=5) onward. The lower Hurwitz tests give

\[
E_1, E_2, E_3, E_4
\quad\text{strictly left-half-plane stable}.
\]

For (q=4), this stability propagates through every raw interaction layer.
Factor

\[
E_4(z)=c\prod_{j=1}^{4}(z-\rho_j),
\qquad \Re\rho_j<0.
\]

If all zeros (alpha_ell) of (f) obey
(Re\alpha_ell\le0), then for (Re z>0),

\[
\Re\frac{f'(z)}{f(z)}
=\sum_ell\Re\frac{1}{z-\alpha_ell}>0.
\]

Consequently (f'(z)-\rho_jf(z)) cannot vanish there, because that would
require (f'(z)/f(z)=\rho_j) with negative real part. Each factor
(D-\rho_j) preserves exclusion of the right half-plane. Multiplication by
(x^4) only adds zeros at (0). Induction proves

\[
\boxed{
\text{every nonzero zero of }A_m^{(4)}(x)
\text{ has }\Re x<0.
}
\]

This is an exact and previously unassumed (P_1) law. It is retained—but the
next theorem shows why it is not a law of the unweighted source relation.

## 3. Accounting non-descent theorem

For two atomic (q)-resultant occurrences, let (r) be their overlap. The
possible native overlap forms are simply (r=0,1,\ldots,q).

Counting every named sharing choice gives

\[
R_2^{(q)}(x)
=\sum_{r=0}^{q}\binom qr x^{2q-r}
=x^q(1+x)^q.
\]

Giving each native overlap isomorphism type one occurrence gives instead

\[
N_2^{(q)}(x)
=\sum_{r=0}^{q}x^{2q-r}
=x^q(1+x+\cdots+x^q).
\]

At (q=4), the nonzero zeros of (R_2) are all (-1). The nonzero zeros of
(N_2) are the fifth roots of unity other than (1), two of which have
positive real part. Therefore

\[
\boxed{
\text{the raw left-half-plane law changes when the accounting changes.}
}
\]

It does not descend to the unweighted atomic interaction source. Uniformly
counting named histories and uniformly counting native forms are two distinct
(P_1) assumptions. Neither may be silently promoted to (P_4).

This is why the stability theorem is kept as a discovered presentation effect
rather than discarded or misreported as a cross-perspective law.

## 4. Minimal surviving structure: the native extension relation

Remove both accountings. Each native incidence isomorphism class is one node.
For classes (F) and (H), write

\[
F\preceq H
\]

when deleting atomic occurrences from (H), followed by erasing all names and
event order, can produce (F). This records only whether the relation exists,
not how many named deletions produce it.

The resulting extension relation is graded by event number in (P_1). Its
incidence inverse is unique:

\[
\mu(H_1,H_1)=1,
\qquad
\mu(H_1,H)
=-\sum_{H_1\preceq F\prec H}\mu(H_1,F),
\]

where (H_1) is the one-occurrence source form. This uses only (P_1)'s
binary statement “the relation exists / does not exist.” No probability or
path multiplicity occurs.

For (q=4), exhaustive native reduction gives:

| Atomic occurrences | Native forms | Forced Möbius residues |
|---:|---:|---|
| 1 | 1 | (1:1) |
| 2 | 5 | (-1:5) |
| 3 | 30 | (0:9, 1:18, 2:3) |
| 4 | 332 | (-4:1, -3:43, -2:38, -1:141, 0:109) |

The notation (v:c) means residue (v) occurs for (c) native forms; these
occurrence counts are audit metadata, while each individual residue is fixed
by its own lower interval.

## 5. Forced interval polynomial and binary character

For an individual source form (H), define

\[
\boxed{
X_H(t)=
\sum_{H_1\preceq F\preceq H}
\mu(H_1,F)t^{r(H)-r(F)}.
}
\]

This is attached to one extension interval, so it does not aggregate different
source forms. It is unchanged by every relabelling. For (H\ne H_1), forced
inversion gives

\[
X_H(1)=0.
\]

As in the isolated refinement branch, the unique rank-local character that
assigns two outcomes to one (P_1) distinction and composes under successive
distinctions is (t^r=2^r). Thus

\[
K_1(H):=X_H(2)
\]

is a derived binary interaction index. It is not assumed to be probability,
knowledge, or native (P_4) quantity.

For three occurrences, if (d(H)) is the number of distinct two-occurrence
parent forms, then

\[
X_H(t)=t^2-d(H)t+d(H)-1
=(t-1)(t-d(H)+1).
\]

The thirty native forms split into:

| (d(H)) | Forms | (X_H(t)) | (K_1(H)) |
|---:|---:|---|---:|
| 1 | 9 | (t(t-1)) | 2 |
| 2 | 18 | ((t-1)^2) | 1 |
| 3 | 3 | ((t-1)(t-2)) | 0 |

Thus three genuinely existing interaction forms are **binary-null under this
invariant**. This does not mean that they do not exist or that (P_1) can
never detect them; it means the complete lower-interval contribution cancels
under the primitive binary rank character.

At four occurrences there are thirteen interval-polynomial types. The 332
native forms have

\[
K_1(H)\in\{-1,0,1,2,3,4,5\},
\]

with exactly thirty binary-null forms. Signed and null effects therefore arise
from interaction alone; they were not inserted into the primitive.

## 6. Irreducibles and the formal component product

Two event occurrences lie in the same incidence component when a chain of
shared resultants joins them. Every finite source form decomposes uniquely as
a multiset of connected forms. In the realization that gives each unlabelled
multiset class coefficient one, let (c_m) be the number of connected native
types with (m) occurrences, and (u_m) the number of all native types. This
gives the formal identity

\[
\boxed{
U(y)=\sum_{m\ge0}u_my^m
=\prod_{m\ge1}(1-y^m)^{-c_m}.
}
\]

For (q=4), the audited values are

\[
(c_1,c_2,c_3,c_4)=(1,4,25,292),
\]

and the formal product reconstructs

\[
(u_0,u_1,u_2,u_3,u_4)=(1,1,5,30,332).
\]

The connected forms are irreducible only with respect to disjoint incidence
composition. They are not identified with primes or any prior arithmetic
objects.

The product is formal and accounting-specific. The complete symmetry lift in
`SYMMETRY_REALIZATION.md` later shows that retaining labelled identities and
their automorphisms gives an exponential component law instead. The
source-level invariant is the symmetric-multiset decomposition; treating the
geometric factors as a source analytic zero formula would be an imported
assumption.

## 7. Exact RH status after this extension

The interaction extension produced three genuine results:

1. a differential evolution law for complete named-history accounting;
2. a sharp arity-four half-plane stability threshold within that accounting;
3. after removing the accounting, a native extension poset, forced signed
   residues, binary-null interaction forms, and unique connected-component
   factorization.

It did **not** produce a canonical global analytic function. The sole rule now
gives a family \(\{X_H\}\), a component groupoid, and a fibre of numerical
realizations. Combining all intervals into one analytic zero set requires a
realization and convergence character that emerge from interaction rather
than being selected from the target.

Therefore no RH claim is made here. The precise next bridge condition is:

\[
\boxed{
\text{derive the }P_1\text{ realization from contextual distinction itself,
without choosing an accounting or weights from zeta.}
}
\]

Only after that character is frozen can its (P_1) zero structure be compared
with the classical zeta structure.
