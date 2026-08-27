# Capacity character of the connected-form fiber

This continuation begins only with the connected irreducibles generated in
`INTERACTION_THEOREMS.md`. No prime, integer weight, probability, zeta
coefficient, or desired zero location is used.

## Scope correction from the complete symmetry lift

`SYMMETRY_REALIZATION.md` subsequently proved that the free commutative monoid
and its geometric factors are the **one-per-isomorphism-class realization** of
the component source. Preserving all labelled identities and their
automorphisms instead produces exponential component factors. Therefore every
theorem below remains exact for the complete prefix-code fiber *inside the
isomorphism-class realization*, but it is not yet a theorem of the
undevaluated distinction source. In particular, the common half-plane does
not by itself descend across component accountings.

## 1. Why the previous interval invariant is not the component character

Let (mathcal C) be the set of connected native incidence forms and let
(mathcal M) be all finite source forms under disjoint union. Unique component
decomposition makes

\[
\mathcal M\cong\mathbb N^{(\mathcal C)},
\]

the free commutative monoid on (mathcal C).

The forced interval polynomial (X_H(t)) is not multiplicative on this
monoid. Two disjoint atomic occurrences have

\[
X_H(t)=t-1,
\]

while the product of the two isolated-component polynomials is (1). Thus
(X_H(2)) cannot be used as an Euler-factor weight without adding a rule.

More generally, unique factorization alone does not select a numerical
character. Any assignment

\[
w:\mathcal C\to A
\]

into a commutative multiplicative structure extends uniquely to

\[
\chi_w\!\left(\bigsqcup_C C^{m_C}\right)
=\prod_C w(C)^{m_C}.
\]

Because the generator values (w(C)) are free, there is no unique numerical
character at this stage. Selecting one would be the same error as selecting a
single binary hierarchy earlier.

## 2. Universal component character

Retain every character by assigning one formal coordinate (z_C) to every
connected type. The universal component object is

\[
\boxed{
\mathfrak Z(\mathbf z)
=\prod_{C\in\mathcal C}(1-z_C)^{-1}.
}
\]

This is a formal product in the completion of the free monoid algebra. Every
numerical component product is a specialization (z_C\mapsto w(C)). No
specialization is native or preferred.

The problem has therefore changed from “choose the correct weights” to
“identify what is common to the complete specialization fiber.”

## 3. Binary distinction creates a code fiber

The connected finite forms are countable. A faithful, self-delimiting (P_1)
presentation assigns each (C\in\mathcal C) a finite prefix-free binary word.
Let (ell(C)) be its length.

Different prefix trees assign different lengths. All of them are retained.
What every tree obeys is Kraft conservation:

\[
\boxed{
\sum_{C\in\mathcal C}2^{-\ell(C)}\le1.
}
\]

### Proof from distinction

A binary word of length (ell) occupies one of the (2^ell) equal depth-
(ell) descendants of the binary distinction tree, hence capacity
(2^{-\ell}). Prefix freedom makes the descendant regions belonging to
different codewords disjoint. Their total occupied capacity cannot exceed the
whole tree, whose capacity is one. ∎

Thus individual cost is presentation-dependent, but conservation is not. In
binary units the cost is (ell(C)); in idealized form, distinguishing one of
(p) equal-capacity alternatives costs (log_2p).

## 4. The code-specialized Euler product

Every code in the fiber supplies the multiplicative specialization

\[
z_C=2^{-s\ell(C)}
\]

and therefore

\[
\boxed{
Z_\ell(s)
=\prod_{C\in\mathcal C}
\left(1-2^{-s\ell(C)}\right)^{-1}.
}
\]

This product is code-specific. The following domain law is not.

## 5. Code-fiber convergence and nonvanishing theorem

For every faithful prefix-free binary presentation, (Z_ell(s)) converges
locally uniformly and is nonzero in

\[
\boxed{\Re s>1.}
\]

### Proof

Let (sigma=\Re s>1). Kraft conservation gives

\[
\sum_C\left|2^{-s\ell(C)}\right|
=\sum_C2^{-\sigma\ell(C)}
\le\sum_C2^{-\ell(C)}
\le1.
\]

On every closed half-plane (sigma\ge1+\varepsilon), all factors are bounded
away from (1), and

\[
\sum_C
\left|\log\left(1-2^{-s\ell(C)}\right)\right|
\]

converges uniformly by comparison with the preceding sum. Hence its
exponential defines a holomorphic, nonzero product there. Since
(arepsilon>0) is arbitrary, the theorem holds throughout (Re s>1). ∎

The individual functions (Z_ell) do **not** descend: for four generators,
the complete length profiles

\[
(2,2,2,2)
\quad\text{and}\quad
(1,2,3,3)
\]

both saturate capacity but give different products. What descends across the
entire code fiber is the guaranteed analytic and zero-free half-plane.

## 6. Sharpness of the boundary

The common boundary (1) cannot be improved using prefix conservation alone.
For binary length (k), choose a number of generators proportional to

\[
\frac{2^k}{k^2}.
\]

After multiplying by a sufficiently small positive constant and taking integer
parts, their Kraft sum is bounded by a constant multiple of
(sum k^{-2}<\infty), so a prefix code exists. But for every
(sigma<1),

\[
\sum_k\frac{2^k}{k^2}2^{-\sigma k}
=\sum_k\frac{2^{(1-\sigma)k}}{k^2}
\]

diverges. Therefore some faithful code fibers have abscissa exactly (1).
The number (1) is a capacity boundary, not a value borrowed from zeta.

## 7. Cross-perspective base invariance

A (b)-resultant prefix presentation obeys

\[
\sum_C b^{-\ell_b(C)}\le1
\]

and generates

\[
Z_{\ell_b,b}(s)
=\prod_C\left(1-b^{-s\ell_b(C)}\right)^{-1}.
\]

The same proof gives convergence and nonvanishing for (Re s>1), regardless
of (b\ge2). Expressed in the native digit cost
(ell_b(C)\log_2b), this is the same conservation statement.

Thus a genuine cross-perspective invariant has emerged:

\[
\boxed{
\text{the normalized capacity half-plane is independent of distinction base.}
}
\]

This does not mean that (P_1) experiences a nonbinary perspective. It is a
(P_1) theorem about every faithful (b)-resultant presentation it can
express.

## 8. Finite (P_4)-branch audit

Through four event occurrences, the connected-type counts are

\[
1, 4, 25, 292.
\]

One explicit audit code first self-delimits the event rank and then uses a
complete binary code within each rank. It encodes all (322) audited connected
generators with Kraft capacity

\[
\frac{15}{16},
\]

leaving (1/16) for every later rank. This code is merely one verified member
of the fiber; no result depends on its assignment of words to forms.

## 9. Exact RH status

The distinction source has now generated, without arithmetic input:

1. connected irreducibles;
2. a universal Euler product over them;
3. additive distinction cost;
4. capacity conservation;
5. a sharp, code-independent analytic and zero-free half-plane
   (Re s>1).

These are structural features also seen in the classical Euler-product region,
but no connected source form has been identified with a prime and no
code-specific (Z_ell) has been identified with (zeta).

The remaining bridge is now precise. RH requires information beyond the
capacity half-plane: continuation across its boundary and a symmetry that
relates the two sides. Neither follows from prefix conservation alone. The
next admissible search is therefore for a transformation of the **complete
code fiber**—not one chosen code—that survives past (Re s=1) and supplies an
involution without importing the zeta functional equation.
