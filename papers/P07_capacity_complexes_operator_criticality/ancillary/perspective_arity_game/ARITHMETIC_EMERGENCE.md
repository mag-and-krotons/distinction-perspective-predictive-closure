# Arithmetic projection from transparent arities

This branch begins after primes have emerged as transparent arities. It does
not identify an atomic composite perspective with a hierarchy of prime
perspectives. It constructs the arithmetic identity system that \(P_1\)
obtains by composing independent transparent-capacity coordinates.

## 1. Independent transparent coordinates

For each transparent arity \(p\), let \(e_p\) record how many times its
capacity coordinate is composed in the \(P_1\) identity projection. Only
finitely many \(e_p\) are nonzero. The resulting identity coordinate is

\[
\boxed{n=\prod_{p\text{ transparent}}p^{e_p}.}
\]

The existence and uniqueness of this vector follow by repeatedly extracting
the least transparent divisor. If a prime \(p\) divides a product, its
transparency implies the usual cancellation step, so it divides one factor;
induction gives uniqueness.

This is the familiar prime factorization theorem, but its generators were not
assumed here: the preceding capacity law selected exactly those arities.

## 2. Distinction cost

Distinguishing among \(p\) equal-capacity alternatives requires
\(\log_2p\) binary capacity units. Independent composition adds costs, so

\[
\begin{aligned}
c(n)
&=\sum_p e_p\log_2p\\
&=\boxed{\log_2n}.
\end{aligned}
\]

The budget law is therefore exact:

\[
\boxed{
c(n)\le\log_2N
\quad\Longleftrightarrow\quad
n\le N.
}
\]

The familiar integer cutoff has emerged as conservation of binary
distinction capacity.

## 3. Independent-selection inversion

For a squarefree identity

\[
n=p_1p_2\cdots p_r,
\]

the partial transparent-coordinate selections form the Boolean subset lattice
on \(r\) independent choices. Exact incidence inversion gives

\[
\boxed{\mu(n)=(-1)^r.}
\]

If a transparent coordinate is repeated, the inverse is zero. Thus

\[
\boxed{
\mu(n)=
\begin{cases}
(-1)^r,&n\text{ has }r\text{ distinct transparent factors},\\
0,&n\text{ contains a repeated transparent factor}.
\end{cases}}
\]

This is now derived from the independent transparent-coordinate refinement,
not identified with the factorial inversion of one atomic co-resultant event.

## 4. The generated analytic character

An analytic character of additive cost satisfies

\[
w_s(c_1+c_2)=w_s(c_1)w_s(c_2).
\]

In the continuous scalar realization, write

\[
w_s(c)=2^{-sc}.
\]

Using the derived cost gives

\[
\boxed{w_s(c(n))=2^{-s\log_2n}=n^{-s}.}
\]

Consequently, in its absolute-convergence region,

\[
\boxed{
Z_{P_1}(s)
=\sum_{n\ge1}n^{-s}
=\prod_{p\text{ transparent}}(1-p^{-s})^{-1}.
}
\]

This is the Riemann zeta function as the scalar analytic character of the
generated \(P_1\) arithmetic projection. The geometric factors are legitimate
here because exponent vectors are in bijection with the already reconstructed
integer identities; they are not being promoted backward to the undevaluated
incidence groupoid.

Its inverse is the generated independent-selection character

\[
\frac1{Z_{P_1}(s)}
=\sum_{n\ge1}\frac{\mu(n)}{n^s}.
\]

## 5. Boundary at this stage

This establishes why zeta and its Möbius inverse arise in \(P_1\) from
distinction capacity. The positive cost monoid alone does not cross
\(\Re s=1\). `CROSS_BOUNDARY_COMPLETION.md` performs that next step: it
repairs the multi-place character fibre, constructs an independent entire
boundary numerator for every transparent prime, and derives their exact
compatibility and common-zero law without importing the classical gamma
completion or a zeta symmetry.
