# Complete-refinement invariant

This structure was generated and frozen before comparison with arithmetic or
RH.

## 1. Partial distinguishability

Within a \(P_1\) presentation of \(q\) co-resultants, a partial state of
distinguishability is completely described by a partition of the resultants:

- members of one block have not been distinguished by that presentation;
- members of different blocks have been distinguished.

One further binary distinction splits exactly one block into two. Retaining
every possible split generates every partition and every maximal refinement
history from one block to singleton blocks.

No partition is chosen as the native \(P_q\) state. The entire structure is
the complete \(P_1\) shadow of all binary expressions.

Because relabelling the \(q\) resultants merely permutes this partition
structure, its unlabeled isomorphism class satisfies the complete-fiber
descent criterion in Theorem 7. This is the exact sense in which the
construction is independent of a selected binary hierarchy.

## 2. Complete-history theorem

Every partition of the \(q\) presented resultants lies on at least one maximal
binary refinement history.

### Proof

Starting from the one-block partition, split blocks until the desired
partition is reached. Then split its remaining nonsingleton blocks until the
singleton partition is reached. Every step is binary and no desired block is
crossed. Thus the desired partition belongs to a complete history. ∎

The only states common to every history are the one-block and singleton
endpoints. Any intermediate distinction selected by one binary expression is
absent from another.

## 3. Number of complete binary histories

Read a history in reverse. With \(k\) current blocks, any pair may be merged,
giving \(\binom{k}{2}\) choices. Therefore

\[
\boxed{
H_q
=
\prod_{k=2}^{q}\binom{k}{2}
=
\frac{q!(q-1)!}{2^{q-1}}.
}
\]

For \(q=4\), this gives \(H_4=18\). The fifteen binary trees counted in the
earlier theorem become eighteen histories because each balanced tree permits
its two lower splits in either order.

## 4. Inversion law forced by refinement

Let \(\widehat0\) be the one-block state. Define the unique coefficients
\(\mu(\widehat0,\pi)\) by

\[
\sum_{\widehat0\le\sigma\le\pi}
\mu(\widehat0,\sigma)
=
\begin{cases}
1,&\pi=\widehat0,\\
0,&\pi\ne\widehat0.
\end{cases}
\]

These coefficients are not chosen signs. They are forced by requiring exact
recovery across the complete refinement order.

At the singleton endpoint \(\widehat1\),

\[
\boxed{
\mu(\widehat0,\widehat1)
=(-1)^{q-1}(q-1)!.
}
\]

More generally, if \(\pi\) has \(k\) blocks, then

\[
\boxed{
\mu(\widehat0,\pi)=(-1)^{k-1}(k-1)!.
}
\]

### Proof

The interval from the one-block state to a \(k\)-block state depends only on
how those \(k\) blocks may themselves be grouped. Its forced inverse
therefore depends only on \(k\). The identity

\[
\log\!\bigl(1+(e^x-1)\bigr)=x
\]

has coefficient

\[
\sum_{j=1}^{k}
\left\{\!\begin{matrix}k\\j\end{matrix}\!\right\}
(-1)^{j-1}(j-1)!
=0
\qquad(k>1).
\]

This is exactly the defining cancellation for the incidence inverse, with
the \(j=1\) term supplying the one-block state. Induction gives the displayed
formula. ∎

The exhaustive program independently verifies the endpoint sequence

\[
-1,\ 2,\ -6,\ 24,\ -120,\ 720
\]

for \(2\le q\le7\).

## 5. Characteristic law

Collect the inversion coefficients by refinement rank. The resulting
polynomial is

\[
\boxed{
C_q(t)
=
\sum_{k=1}^{q}
\left\{\!\begin{matrix}q\\k\end{matrix}\!\right\}
(-1)^{k-1}(k-1)!\,t^{q-k},
}
\]

where the bracketed coefficient counts the complete partitions having \(k\)
blocks. This is a count discovered from the complete refinement structure,
not an assumed arithmetic coefficient.

For the hypothetical four-resultant source,

\[
\boxed{
C_4(t)
=t^3-7t^2+12t-6
=(t-1)(t^2-6t+6).
}
\]

This law was obtained from the complete refinement structure, not from one
binary code. It is unchanged when resultants are renamed, binary branches are
swapped, or refinement histories are reordered.

It remains a \(P_1\) expression of the full presentation fiber. It is not
asserted to be \(P_4\)'s unknowable native polynomial.

## 6. Generated recurrence

The partition-count recurrence gives

\[
\boxed{
C_{q+1}(t)
=(t-1)\bigl(qC_q(t)-tC_q'(t)\bigr),
\qquad C_1(t)=1.
}
\]

### Proof

Let the bracketed coefficient in the definition of \(C_q\) be denoted
\(S(q,k)\). Adding one presented resultant either creates a new block or
joins one of the existing \(k\) blocks, so

\[
S(q+1,k)=kS(q,k)+S(q,k-1).
\]

Substitution into the definition of \(C_{q+1}\), followed by grouping equal
powers of \(t\), gives the displayed differential recurrence. ∎

The executable audit also constructs the complete partition structure
directly and checks the recurrence through \(q=7\).

## 7. Real-root and interlacing law

Every zero of \(C_q\) is real, positive and simple. The least zero is always
\(1\), and the remaining zeros of \(C_{q+1}\) strictly interlace those of
\(C_q\).

### Proof

The claim holds for \(C_2(t)=t-1\). Suppose

\[
C_q(t)=\prod_{j=1}^{q-1}(t-r_j),
\qquad
0<r_1<\cdots<r_{q-1}.
\]

Away from those roots, zeros of

\[
qC_q-tC_q'
\]

are zeros of

\[
h(t)
=q-\sum_{j=1}^{q-1}\frac{t}{t-r_j}.
\]

On every interval not containing an \(r_j\),

\[
h'(t)
=
\sum_{j=1}^{q-1}\frac{r_j}{(t-r_j)^2}
>0.
\]

Immediately to the right of each \(r_j\), \(h=-\infty\); immediately to the
left of \(r_{j+1}\), \(h=+\infty\). Hence there is exactly one zero between
successive roots. There is one further zero beyond the largest root because
\(h\) rises from \(-\infty\) to \(1\). There is none below the least positive
root. Multiplication by \(t-1\) adds the new least root \(1\). Induction proves
the claim. ∎

This is the first nontrivial location law generated by the corrected game.

## 8. All-arity expression

Collecting the frozen polynomials by arity gives

\[
\boxed{
\sum_{q\ge1}C_q(t)\frac{z^q}{q!}
=
\log\!\left(
\frac{e^{tz}+t-1}{t}
\right).
}
\]

This follows by summing the complete \(k\)-block partition counts; no
zero-location target is used.

### Proof

For fixed \(k\), the labelled partition count has exponential generating
function

\[
\sum_{q\ge k}
\left\{\!\begin{matrix}q\\k\end{matrix}\!\right\}
\frac{(tz)^q}{q!}
=\frac{(e^{tz}-1)^k}{k!}.
\]

The division by \(q!\) removes the ordering of the \(q\) presented labels; it
is fixed by their full relabelling symmetry. Multiplying by
\((-1)^{k-1}(k-1)!t^{-k}\) and summing over \(k\) gives

\[
\sum_{k\ge1}\frac{(-1)^{k-1}}{k}
\left(\frac{e^{tz}-1}{t}\right)^k
=
\log\!\left(\frac{e^{tz}+t-1}{t}\right).
\]

Thus the expression is generated by the source counts and their symmetry
normalization. ∎

Exponentiating isolates the entire carrier

\[
\boxed{
Q_t(z)=\frac{e^{tz}+t-1}{t}.
}
\]

Its zeros are explicit:

\[
\boxed{
z_m(t)
=
\frac{\log(t-1)+(2m+1)\pi i}{t},
\qquad m\in\mathbb Z,\quad t>1.
}
\]

Thus they occupy one vertical line in the \(P_1\) coordinate \(z\).

## 9. Why the \(P_1\) evaluation is \(t=2\)

The exponent \(q-k\) is the number of binary refinement steps still required
to pass from a \(k\)-block state to full distinction. Suppose a local
evaluation:

1. depends only on this remaining rank;
2. assigns one binary distinction its two co-resultants; and
3. composes multiplicatively when refinement segments are concatenated.

Writing its rank-\(r\) weight as \(w_r\), these conditions force

\[
w_0=1,\qquad w_1=2,\qquad w_{r+s}=w_rw_s,
\]

and therefore uniquely

\[
\boxed{w_r=2^r.}
\]

Consequently the rank character selected by \(P_1\)'s primitive distinction
is exactly evaluation at \(t=2\). This does not claim that the source has the
number two internally; it identifies the unique multiplicative accounting
performed by its binary presentation.

At this evaluation,

\[
Q_2(z)=\frac{e^{2z}+1}{2}=e^z\cosh z,
\]

and therefore

\[
\boxed{
z_m(2)=\left(m+\tfrac12\right)\pi i.
}
\]

The same binary evaluation gives the exact parity cancellation

\[
\boxed{
C_{2m+1}(2)=0\qquad(m\ge1),
}
\]

because

\[
\sum_{q\ge1}C_q(2)\frac{z^q}{q!}
=z+\log\cosh z
\]

has no odd powers beyond its initial \(z\).
