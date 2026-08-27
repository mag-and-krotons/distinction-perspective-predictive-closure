# Post-freeze arithmetic comparison

The source invariant in `REFINEMENT_THEOREMS.md` was generated and frozen
before this comparison.

## 1. What classical arithmetic uses

For a squarefree integer with \(r\) distinct prime factors, its divisors are
described in \(P_1\) by choosing whether each prime is present or absent.
The resulting refinement object is the binary subset structure on \(r\)
independent choices.

Exact inversion on that structure gives

\[
\mu_{\mathrm{arith}}(n)=(-1)^r.
\]

These are the squarefree coefficients in

\[
\frac1{\zeta(s)}
=
\sum_{n\ge1}\frac{\mu_{\mathrm{arith}}(n)}{n^s}.
\]

## 2. What the atomic co-resultant source produced

The complete refinement shadow of one atomic \(r\)-resultant distinction
instead gives

\[
\mu_{\mathrm{atomic}}(r)
=
(-1)^{r-1}(r-1)!.
\]

The two sequences are not the same:

| \(r\) | Arithmetic subset inversion | Atomic co-resultant inversion |
|---:|---:|---:|
| 2 | \(+1\) | \(-1\) |
| 3 | \(-1\) | \(+2\) |
| 4 | \(+1\) | \(-6\) |
| 5 | \(-1\) | \(+24\) |

Converting the second column into the first would require the externally
chosen normalization

\[
-\frac{1}{(r-1)!}.
\]

That normalization did not emerge from the atomic source and therefore cannot
be inserted into the translation.

## 3. Generated analytic expression

Collecting the complete frozen refinement polynomials over all arities gives

\[
\sum_{q\ge1}C_q(t)\frac{z^q}{q!}
=
\log\!\left(\frac{e^{tz}+t-1}{t}\right).
\]

For binary \(P_1\), \(t=2\), and its entire carrier is

\[
Q_2(z)=\frac{e^{2z}+1}{2}.
\]

The generated zero formula is therefore

\[
z_m=\left(m+\tfrac12\right)\pi i.
\]

This formula was frozen before comparison with the Riemann zeros.

## 4. Exact comparison result

The generated invariant has a rigorous zero-location law, but it does **not**
have the classical zeta-zero structure as its \(P_1\) effect:

- its finite-\(q\) expressions form the real-rooted interlacing family
  \(C_q(t)\);
- its all-arity carrier is \((e^{tz}+t-1)/t\);
- at the binary value its zeros are exactly equally spaced;
- classical reciprocal-zeta coefficients come from independent binary subset
  choices, not atomic co-resultant refinement.

Therefore the present atomic source is not yet proved to be the shared
referent whose \(P_1\) effect is RH. Declaring the two inversions identical
would erase precisely the perspective difference the project requires us to
retain.

Even shifting \(z\mapsto s-\tfrac12\) because the generated zeros occupy an
axis would be an imported target alignment. No such shift or translation was
produced by the source.

There is also a decisive density mismatch under every fixed affine
coordinate change. The positive-imaginary zeros of \(Q_2\) satisfy

\[
N_{Q_2}(T)=\frac{T}{\pi}+O(1),
\]

whereas the nontrivial zeta zeros satisfy the Riemann--von Mangoldt law

\[
N_\zeta(T)
=
\frac{T}{2\pi}\log\!\frac{T}{2\pi}
-\frac{T}{2\pi}
+O(\log T).
\]

An affine map can rescale a linear density but cannot create the
\(T\log T\) term. Hence the generated zero family is not an affine
re-expression of the classical zeta-zero family. A more general
cross-perspective map remains logically possible, but it must itself emerge
from a source invariant; choosing it to fit the target would repeat the
original error.

This is a completed comparison, not a claim that no suitable source exists.
It says exactly what this independently generated source does in \(P_1\), and
why its first invariant is not the classical RH structure.
