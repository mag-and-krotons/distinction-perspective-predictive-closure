# Uncollapsed fibres, carry interaction, and generated duality

The preceding boundary theorem summed every nontrivial least-place character
into one scalar \(E_p\). That gave the continuation and exact common-zero
equation, but it also reduced the prime family to analytic rank one. This
branch does not perform that sum. It retains the entire \(p^J\)-member fibre
and lets the already-generated integer identity act on it.

No random walk, Gaussian, gamma factor, theta identity, zeta functional
equation, or critical line is assumed. Each appears below only if it is forced
as an effect of the retained operations.

## 1. Independent digits are not stable under carry

For \(J\) base-\(p\) capacity places, the full independent-digit character
basis is

\[
\chi_{\mathbf r}(n)
=\exp\!\left(\frac{2\pi i}{p}
\sum_{j=0}^{J-1}r_jd_j(n)\right),
\qquad
\mathbf r\in(\mathbb Z/p\mathbb Z)^J.
\]

These \(p^J\) characters form a complete basis for functions on the
\(p^J\) digit states. However, unit advance in the generated integer identity
does not add independently in each digit. It carries:

\[
(p-1,p-1,\ldots,p-1)\longmapsto(0,0,\ldots,0).
\]

Let \(S\) be the complete carry successor

\[
(Sf)(n)=f(n+1\bmod p^J).
\]

Except for a small subset, one independent-digit character is not an
eigenvector of \(S\). Carry mixes it with other members of the complete fibre.
Thus carry is the first genuine cross-place interaction that was destroyed by
the earlier scalar trace.

## 2. Carry characters emerge by diagonalizing the interaction

Write \(M=p^J\). The eigencharacters of the carry cycle are

\[
\boxed{
\psi_{M,a}(n)=e^{2\pi ian/M},
\qquad a=0,1,\ldots,M-1.
}
\]

Directly,

\[
S\psi_{M,a}=e^{2\pi ia/M}\psi_{M,a}.
\]

Because the digit characters are complete, every carry character has the
exact expansion

\[
\boxed{
\psi_{M,a}(n)
=\sum_{\mathbf r}C_{a,\mathbf r}\chi_{\mathbf r}(n),
\qquad
C_{a,\mathbf r}
=\frac1M\sum_{m=0}^{M-1}
\psi_{M,a}(m)\overline{\chi_{\mathbf r}(m)}.
}
\]

For example, at \(p=3,J=2\), a generic carry mode uses several members of the
nine-element digit fibre. The modes with frequency divisible by three reduce
to a single least-digit character. Those exceptional modes are precisely the
small slice used in the earlier boundary trace.

The executable audit reconstructs every carry mode from the full digit fibre
at \((p,J)=(2,3)\) and \((3,2)\).

## 3. Cross-prime interaction and finite completion

For pairwise-coprime prime-power capacities

\[
M_1,\ldots,M_r,
\qquad M=\prod_jM_j,
\]

the complete simultaneous boundary state is determined uniquely by its local
states:

\[
\mathbb Z/M\mathbb Z
\cong\prod_j\mathbb Z/M_j\mathbb Z.
\]

This is not an imported factorization rule. The explicit interaction
idempotents are

\[
e_j=\frac{M}{M_j}
\left(\frac{M}{M_j}\right)^{-1}\pmod{M_j},
\]

and the reconstructed state is \(n=\sum_jn_je_j\pmod M\).

A global carry character factors into the local prime-power fibres. If

\[
u_j=\left(\frac{M}{M_j}\right)^{-1}\pmod{M_j},
\]

then

\[
\boxed{
e^{2\pi ian/M}
=\prod_j
e^{2\pi i(a u_j)n_j/M_j}.
}
\]

Taking every finite capacity and every reduction map gives the inverse-limit
boundary

\[
\widehat{\mathbb Z}=\varprojlim_M\mathbb Z/M\mathbb Z.
\]

Every finite character is indexed by a rational phase \(a/M\bmod1\); under
refinement these form \(\mathbb Q/\mathbb Z\). Thus the complete cross-prime
interaction generates the finite boundary and its full dual rather than one
scalar Euler factor.

## 4. The symmetric complete distinction

The forward difference is \(I-S\). Retaining rather than selecting its reverse
co-resultant gives \(I-S^{-1}\). Their complete composition is

\[
\boxed{
L_M=(I-S)(I-S^{-1})=2I-S-S^{-1}.
}

It vanishes on the undistinguished constant mode and treats both generated
directions equally. No neighbourhood or stochastic transition law has been
added.

The carry characters diagonalize it:

\[
\boxed{
L_M\psi_{M,a}
=\lambda_{M,a}\psi_{M,a},
\qquad
\lambda_{M,a}=4\sin^2\!\left(\frac{\pi a}{M}\right).
}
\]

This sine-square spectrum is therefore a new law produced by the uncollapsed
cross-place interaction.

## 5. The continuum scaling is forced

For a fixed frequency \(a\),

\[
\lambda_{M,a}
\sim\frac{(2\pi a)^2}{M^2}.
\]

If the distinction is rescaled by \(M^\alpha\), its nonconstant low modes:

- collapse to zero when \(\alpha<2\);
- diverge when \(\alpha>2\); and
- have a finite, nonzero limit only when \(\alpha=2\).

Hence

\[
\boxed{
M^2L_M\longrightarrow-\frac{d^2}{dx^2},
\qquad
M^2\lambda_{M,a}\longrightarrow(2\pi a)^2.
}
\]

The quadratic scale was not selected because a Gaussian was wanted. It is
the unique nondegenerate scale of the generated spectrum.

## 6. Exponential completion produces the Gaussian carrier

The earlier identity-and-symmetry lift proved that labelled repetitions of an
interaction exponentiate. Apply that already-derived rule to the stable
analytic half of the complete distinction:

\[
K_M(\tau)=e^{-\tau M^2L_M},
\qquad \Re\tau>0.
\]

On the \(a\)-th carry mode,

\[
K_M(\tau)\longrightarrow e^{-\tau(2\pi a)^2}.
\]

Writing \(t=4\pi\tau\), the complete limiting spectral carrier is

\[
\boxed{
\Theta(t)=\sum_{a\in\mathbb Z}e^{-\pi a^2t}.
}
\]

This is not a random-walk assumption. It is the exponential symmetry carrier
of the uniquely scaled symmetric distinction.

## 7. Character completeness forces theta duality

Let

\[
g_t(x)=e^{-\pi tx^2}.
\]

Direct evaluation of its Fourier character integral gives

\[
\widehat g_t(\xi)
=t^{-1/2}e^{-\pi\xi^2/t}.
\]

Periodize \(g_t\) over the complete integer identity. Its Fourier
coefficients are the values \(\widehat g_t(a)\) on all carry characters.
Evaluating the complete Fourier reconstruction at the identity gives

\[
\boxed{
\Theta(t)=t^{-1/2}\Theta(1/t).
}
\]

Thus theta duality is not imported. It is the continuum expression of the
same finite character completeness and carry interaction verified above.

## 8. The gamma factor and zeta symmetry emerge

For \(\Re s>1\), the Mellin character of the generated carrier is

\[
\begin{aligned}
\int_0^\infty(\Theta(t)-1)t^{s/2-1}\,dt
&=2\sum_{n\ge1}\int_0^\infty
e^{-\pi n^2t}t^{s/2-1}\,dt\\
&=2\pi^{-s/2}\Gamma(s/2)Z(s).
\end{aligned}
\]

Here

\[
\Gamma(s/2)=\int_0^\infty e^{-u}u^{s/2-1}\,du
\]

has not been appended as a guessed correction. It is the common scale integral
left after substituting \(u=\pi n^2t\). The gamma factor has therefore emerged
from the generated Gaussian carrier.

Split the integral at \(t=1\) and use the just-derived theta duality. This
gives

\[
\begin{aligned}
\Lambda(s)
&:=\pi^{-s/2}\Gamma(s/2)Z(s)\\
&=\frac1{s(s-1)}
+\frac12\int_1^\infty(\Theta(t)-1)
\left(t^{s/2-1}+t^{(1-s)/2-1}\right)dt.
\end{aligned}
\]

The integral is entire in \(s\) and visibly unchanged by \(s\mapsto1-s\).
Consequently

\[
\boxed{
\xi(s)=\frac12s(s-1)\Lambda(s)
}
\]

is entire and satisfies

\[
\boxed{
\xi(s)=\xi(1-s).
}
\]

This is the zeta completion and reflection law, derived from carry-coupled
character completeness. Neither was used as an input.

## 9. Exact zero consequences

The Euler-product result already proves that \(Z(s)\ne0\) for \(\Re s>1\).
The generated reflection confines every nontrivial zero to the unit strip.
Real source coefficients add conjugation. Therefore every nonreal zero
\(\rho\) generates the orbit

\[
\boxed{
\rho,\quad\overline\rho,\quad1-\rho,
\quad1-\overline\rho.
}
\]

The line \(\Re s=1/2\) is the fixed set of the reflected-conjugate operation.
However, an involution does not require every orbit to be fixed. For any
\(\rho\) off the line, form its complete orbit polynomial

\[
\boxed{
P_\rho(s)=
(s-\rho)(s-\overline\rho)
\bigl(s-(1-\rho)\bigr)
\bigl(s-(1-\overline\rho)\bigr).
}
\]

It obeys the same reflection and conjugation laws while its zeros remain off
the fixed line. This proves, rather than merely warns, that completion
symmetry alone cannot imply RH.

The uncollapsed branch has therefore produced genuinely new laws—carry
characters, the sine-square distinction spectrum, the forced quadratic
scale, Gaussian/theta duality, the gamma completion, and the fourfold zero
orbit. It has not proved that every orbit collapses to two points on the
critical line, so RH is not claimed.
