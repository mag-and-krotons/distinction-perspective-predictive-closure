# Character inversion and the finite-horizon symmetry

This result acts on the complete component-character construction from
`CAPACITY_THEOREMS.md`. It does not select a code or import a target line.

## Scope correction

The later complete symmetry audit in `SYMMETRY_REALIZATION.md` shows that the
geometric component factor is specific to the one-per-isomorphism-class
realization. The identity-and-symmetry-preserving realization has exponential
factors and no reciprocal-zero grid. The inversion, completion and normalized
central axis proved below are therefore valid laws of the geometric/code
projection, not yet cross-accounting laws of the distinction source. They are
retained as discovered \(P_1\) effects rather than erased.

## 1. Universal factor inversion

For a finite set (F\subset\mathcal C) of connected generators, write

\[
\mathfrak Z_F(\mathbf z)=\prod_{C\in F}(1-z_C)^{-1}.
\]

Inverting every character coordinate gives the exact identity

\[
\begin{aligned}
\mathfrak Z_F(\mathbf z^{-1})
&=\prod_{C\in F}(1-z_C^{-1})^{-1}\\
&=(-1)^{|F|}\left(\prod_{C\in F}z_C\right)
\mathfrak Z_F(\mathbf z).
\end{aligned}
\]

This is forced separately by every geometric component factor. It is
therefore independent of how connected forms are named or ordered.

## 2. Code specialization

For any prefix-code member (ell) in base (b), specialize

\[
z_C=b^{-s\ell(C)}.
\]

For a finite horizon (F), let

\[
N_F=|F|,
\qquad
L_F=\sum_{C\in F}\ell(C).
\]

The universal inversion becomes

\[
\boxed{
Z_{\ell,F}(-s)
=(-1)^{N_F}b^{-sL_F}Z_{\ell,F}(s).
}
\]

The half-prefactor is uniquely fixed by requiring the residual factor under
(s\mapsto-s) to be constant. Define

\[
\boxed{
\widehat Z_{\ell,F}(s)
=b^{-sL_F/2}Z_{\ell,F}(s).
}
\]

Then

\[
\boxed{
\widehat Z_{\ell,F}(-s)
=(-1)^{N_F}\widehat Z_{\ell,F}(s).
}
\]

Thus every finite code presentation has the same *form* of involution. Its
parity depends only on the number of retained connected generators.

## 3. Generated reciprocal-zero axis

The reciprocal finite product is

\[
P_{\ell,F}(s)
=\prod_{C\in F}\left(1-b^{-s\ell(C)}\right).
\]

Each factor vanishes exactly at

\[
\boxed{
s_{C,k}
=\frac{2\pi i k}{\ell(C)\log b},
\qquad k\in\mathbb Z.
}
\]

Therefore every finite reciprocal zero lies on

\[
\boxed{\Re s=0.}
\]

The individual spacings and multiplicities vary with the code. The axis does
not. No shift to (1/2), affine identification with a classical variable, or
zeta datum was used.

For positive height (T), the finite zero count is

\[
N_F(T)
=\sum_{C\in F}
\left\lfloor\frac{T\ell(C)\log b}{2\pi}\right\rfloor
=\frac{T\log b}{2\pi}L_F+O(N_F).
\]

The density is consequently code- and horizon-dependent even though the axis
is common.

## 4. Why this is not yet an infinite functional equation

As the horizon grows through all connected forms,

\[
N_F\to\infty,
\qquad
L_F\to\infty.
\]

The completion factor (b^{-sL_F/2}) therefore has no unrenormalized limit.
Capacity proves convergence on (Re s>1), while inversion formally reflects
that region to (Re s<-1). It does not define the intervening strip.

Choosing a subtraction for (L_F), summing the divergent parity, or assigning
a continuation by analogy would be an additional law. None is inserted.

At this historical stage of the geometric/code projection, the open problem
was:

\[
\boxed{
\text{derive a code-fiber-invariant renormalization of }(N_F,L_F)
\text{ from distinction itself.}
}
\]

The later symmetry audit showed that this was not the source-level route:
geometric factors already depended on one-per-class accounting. The result is
therefore retained as the exact boundary of that projection, not presented as
the current research frontier.

## 5. Counterterm-free infinite exterior observable

The finite logarithmic relation has the form

\[
\log Z_{\ell,F}(-s)
=\log Z_{\ell,F}(s)
-sL_F\log b+i\pi N_F
\]

up to branch choice. Its divergence is affine in (s). One derivative leaves
the divergent constant (L_F\log b); two derivatives annihilate both
divergent terms. This fixes the minimal counterterm-free operation.

Define

\[
\boxed{
G_\ell(s)
=\frac{d^2}{ds^2}\log Z_\ell(s)
=\sum_{C\in\mathcal C}
\frac{(\ell(C)\log b)^2}
{4\sinh^2\!\left(s\ell(C)\log b/2\right)}.
}
\]

Every summand is even, so wherever the series exists,

\[
\boxed{G_\ell(-s)=G_\ell(s).}
\]

For (|\Re s|>1), the terms are bounded by a constant times

\[
\ell(C)^2b^{-|\Re s|\ell(C)}.
\]

Polynomial growth in (ell) can be absorbed into an arbitrarily small loss
in the exponent; Kraft conservation then proves local uniform convergence.
Thus every infinite prefix-code presentation has a well-defined even
meromorphic exterior observable on

\[
\boxed{|\Re s|>1.}
\]

This removes the divergent finite-horizon completion without assigning a
regularized value to (N_F) or (L_F). The observable still depends on the
code lengths, but its evenness, pole axis and guaranteed exterior domain are
common to the full code fiber.

It does not yet continue through (|\Re s|\le1). The remaining question is no
longer how to cancel the affine divergence; it is whether the complete code
fiber supplies boundary data strong enough to determine continuation through
the capacity strip.

## 6. Unit-strip normalization theorem

The capacity theorem and its inversion produce two boundaries before any
comparison:

\[
\Re s=1,
\qquad
\Re s=-1.
\]

The unique orientation-preserving affine coordinate that sends these ordered
boundaries to (0) and (1) is

\[
\boxed{
\sigma=\frac{s+1}{2},
\qquad
s=2\sigma-1.
}
\]

This is a normalization of the already generated capacity strip; it is not a
shift selected from a target zero line. Under it,

\[
s\mapsto-s
\quad\Longleftrightarrow\quad
\sigma\mapsto1-\sigma,
\]

and

\[
\Re s=0
\quad\Longleftrightarrow\quad
\boxed{\Re\sigma=\tfrac12}.
\]

Consequently the finite reciprocal zeros become

\[
\boxed{
\sigma_{C,k}
=\frac12+
\frac{\pi i k}{\ell(C)\log b}.
}
\]

The completed finite character, written

\[
\widetilde Z_{\ell,F}(\sigma)
=\widehat Z_{\ell,F}(2\sigma-1),
\]

satisfies

\[
\widetilde Z_{\ell,F}(1-\sigma)
=(-1)^{N_F}\widetilde Z_{\ell,F}(\sigma).
\]

Thus the geometry “unit strip, reflection about (1/2), central zero axis”
is not assumed. It is the normalized image of binary capacity plus character
inversion.

This theorem still does not identify (widetilde Z_{ell,F}) with the Riemann
zeta function. The ordinates depend on code lengths, and the infinite
continuation across the capacity strip remains unproved. What has been derived
is the same *geometric form* from the distinction source alone.

## 7. Length-enumerator obstruction theorem

Let

\[
a_j=\#\{C:\ell(C)=j\},
\qquad
A_\ell(z)=\sum_{j\ge1}a_jz^j.
\]

Kraft conservation is exactly

\[
A_\ell(1/b)\le1.
\]

In the convergence half-plane, expanding every geometric logarithm gives

\[
\boxed{
\log Z_\ell(s)
=\sum_{r\ge1}\frac{1}{r}
A_\ell\!\left(b^{-rs}\right).
}
\]

### Proof

Absolute convergence permits rearrangement:

\[
\begin{aligned}
\log Z_\ell(s)
&=\sum_C\sum_{r\ge1}\frac{b^{-rs\ell(C)}}r\\
&=\sum_{r\ge1}\frac1r
\sum_{j\ge1}a_j(b^{-rs})^j.
\end{aligned}
\]

The inner sum is (A_ell(b^{-rs})). ∎

This formula isolates the continuation problem completely. Prefix capacity
constrains (A_ell) at (1/b), but does not determine the function. Distinct
faithful codes can give different length enumerators and hence different
singularities, continuations and nontrivial zero patterns.

Therefore neither capacity, component factorization nor finite inversion can
by itself predict a unique nontrivial zero sequence. Any such prediction must
come from an additional relation that fixes (A_ell) across the complete
code fiber—or replaces code length by a source-determined character. Choosing
that relation from the known Riemann zeros would be target fitting.

There is a universal factor zero grid

\[
s=\frac{2\pi i n}{\log b},
\qquad n\in\mathbb Z,
\]

common to all integer-length codes, but this is the trivial periodic grid of
the component factors. It is not the classical nontrivial zeta-zero sequence.

The projection branch therefore ended with the following unresolved
code-specific question:

\[
\boxed{
\text{derive }A_\ell\text{ (or its code-independent replacement) from the
native extension structure itself.}
}
\]

The later transparent-arity branch replaces arbitrary code length by the
source-derived cost \(\log_2n\); the cross-boundary and uncollapsed-fibre
documents continue from that replacement. This boxed question is historical,
not a still-repeated claim about what remains to be done.
