# Binary capacity character

This branch begins with the symmetry carrier already generated in
`SYMMETRY_REALIZATION.md`:

\[
\mathcal H_q(u,x)
=e^{-x}\sum_{n\ge0}e^{u\binom nq}\frac{x^n}{n!}.
\]

No arithmetic target or desired zero is used.

## 1. The unique nontrivial binary sign

For \(n\) presented resultants, \(\binom nq\) is the number of available
atomic \(q\)-incidences in this \(P_1\) symmetry realization. A binary flip
has two multiplicative characters: the trivial character \(1\) and the
nontrivial sign \(-1\). Applying the nontrivial character to every available
incidence gives the forced sign

\[
\boxed{a_n^{(q)}=(-1)^{\binom nq}.}
\]

Writing the sign as \(e^{i\pi\binom nq}\) is only its complex \(P_1\)
coordinate. The structural operation is parity.

The resulting exponential carrier is

\[
F_q(x)=\sum_{n\ge0}a_n^{(q)}\frac{x^n}{n!},
\qquad
\boxed{\mathcal B_q(x)=e^{-x}F_q(x).}
\]

Thus \(\mathcal B_q(x)=\mathcal H_q(i\pi,x)\) in the symmetry realization.

## 2. Capacity-digit theorem and the one seed

Let the incidence-size probe be \(q=2^j\). Then

\[
\boxed{
\binom n{2^j}\bmod2
=\text{the }j\text{-th binary digit of }n.
}
\]

### Proof from binary distinction

Write \(n=\sum_j b_j2^j\), where \(b_j\in\{0,1\}\). In binary
coefficient arithmetic,

\[
(1+y)^{2^j}=1+y^{2^j},
\]

because every intermediate binomial coefficient is even. Hence

\[
(1+y)^n
=\prod_{j:b_j=1}(1+y^{2^j})
\quad(\bmod 2).
\]

The coefficient of \(y^{2^j}\) is \(b_j\): distinct lower powers sum to at
most \(2^j-1\), so no other subset contributes that exponent. But the same
coefficient is \(\binom n{2^j}\bmod2\). ∎

Consequently

\[
\boxed{
n\longmapsto
\left(\binom n1,\binom n2,\binom n4,\ldots\right)\bmod2
}
\]

is injective and is exactly the ordinary binary expansion. The integer label
has therefore not been inserted into this signature: the family of atomic
incidence capacities at power-of-two arities reconstructs it.

There is an essential boundary at \(j=0\). The probe

\[
\binom n1\bmod2=n\bmod2
\]

is not a hypothetical unary distinguishing perspective; a one-resultant
relation would not be a distinction. It is the **single identity seed** that
asks whether the least binary alternative is present. The genuine atomic
incidence arities \(2,4,8,\ldots\) then recover every higher bit.

If the seed probe is omitted, two coordinates differing only in their least
bit remain indistinguishable. If it is retained, every finite nonnegative
integer is reconstructed. Thus this branch gives an exact form of

\[
\boxed{
\text{one seeded distinction}\quad+\quad
\text{all generated higher capacities}\quad=\quad
\text{complete }P_1\text{ integer identity}.}
\]

## 3. Generated differential law

For \(q=2^j\), the digit theorem gives

\[
a_{n+q}^{(q)}=-a_n^{(q)}.
\]

Termwise differentiation of the entire exponential series therefore yields

\[
\boxed{
F_q^{(q)}(x)+F_q(x)=0,
\qquad
F_q^{(r)}(0)=1\quad(0\le r<q).
}
\]

This is a concrete example of the same source structure appearing in \(P_1\)
as a differential law: the source operation is incidence distinction; the
ODE is its binary capacity character.

## 4. Exact finite exponential form

The sign sequence has period \(2q\) and anti-period \(q\). Let

\[
\omega=e^{\pi i/q}.
\]

Only the odd Fourier modes survive, and direct finite inversion gives

\[
\boxed{
F_q(x)=
\sum_{\substack{1\le k<2q\\k\text{ odd}}}
\frac{2}{q(1-\omega^{-k})}e^{\omega^kx}.
}
\]

Equivalently, its characteristic frequencies are precisely the \(q\) roots
of \(\lambda^q=-1\). No continuation or regularization is required.

At \(q=2\),

\[
F_2(x)=\cos x+\sin x,
\]

so this first nontrivial carrier has the exact zero law

\[
\boxed{x_k=-\frac\pi4+k\pi.}
\]

At \(q=4\), the independently generated law is

\[
F_4^{(4)}+F_4=0,
\qquad
F_4(0)=F_4'(0)=F_4''(0)=F_4'''(0)=1.
\]

Its four frequencies are the fourth roots of \(-1\). This is the correct
\(P_1\) binary-capacity effect of the four-resultant symmetry carrier; it is
not asserted to be \(P_4\)'s native dynamics.

## 5. Research consequence

Three layers are now distinct:

1. the undevaluated incidence source;
2. the full identity-and-symmetry realization;
3. the nontrivial binary capacity character of that realization.

The third layer derives binary arithmetic identity from one explicit seed and
a differential law,
but a fixed \(q\) gives a finite exponential polynomial and therefore does
not yet have the Riemann-zero structure. The next admissible continuation is
the **complete power-of-two arity family**, because together those capacities
distinguish every \(P_1\) integer coordinate. Selecting one arity or one zero
alignment from the target would again narrow the source prematurely.

## 6. Complete binary-identity carrier

Retain the nontrivial sign from every capacity digit. For

\[
n=\sum_j b_j2^j,
\]

the total character is

\[
\tau(n)=\prod_j(-1)^{b_j}=(-1)^{\sum_jb_j}.
\]

Every integer is a unique finite choice of the powers \(2^j\). Therefore its
ordinary carrier factorizes without an added coefficient law:

\[
\boxed{
T(z)=\sum_{n\ge0}\tau(n)z^n
=\prod_{j\ge0}(1-z^{2^j}).
}
\]

Separating the seeded least bit from the remaining bits gives the generated
self-similarity

\[
\boxed{T(z)=(1-z)T(z^2).}
\]

For \(|z|<1\), the sum \(\sum_j|z|^{2^j}\) converges, so the product is
holomorphic and nonzero. Every dyadic root of unity is a radial zero: after
some index all powers of that root are one, and the corresponding factors
tend to zero radially. Dyadic roots are dense on the unit circle. If analytic
continuation existed through any boundary arc, its boundary values would have
dense zeros and hence vanish identically, contradicting nonvanishing inside.
Thus

\[
\boxed{|z|=1\text{ is a natural boundary of }T.}
\]

This boundary is not inserted geometry. It is generated by the unending
binary distinction scales \(1,2,4,\ldots\).
