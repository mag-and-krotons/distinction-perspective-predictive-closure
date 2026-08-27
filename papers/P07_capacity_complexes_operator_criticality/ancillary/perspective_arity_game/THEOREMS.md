# Theorems of the corrected perspective-arity game

Everything written here is a \(P_1\) statement. A “native \(P_4\)
presentation” means a \(P_1\) presentation that treats a four-resultant
relation as atomic and then removes every dependence on the presentation
labels.

## Theorem 1 — \(P_0\) is not a game state

No nonempty program object can represent \(P_0\).

### Proof

A program object is distinguishable from another object or from its absence.
It therefore already belongs to a perspective with distinction. Since
\(P_0\) is defined by no distinction, representing it as a state would negate
its definition. The token “\(P_0\)” is consequently a \(P_1\) boundary
reference, not an encoded \(P_0\) object. ∎

## Theorem 2 — one atomic \(P_4\) occurrence has full four-resultant symmetry

Every permutation of the four presented resultants preserves the sole atomic
incidence. Hence its presentation automorphism group is the full permutation
group on four resultants and has \(24\) elements.

No individual resultant, pair, triple, ordering, distance, or intermediate
split is invariantly preferred.

## Theorem 3 — \(P_1\) has fifteen complete binary presentations of four
labelled resultants

A complete non-plane binary tree with four labelled leaves has one of two
shapes.

1. The root divides the leaves \(2+2\). There are three complementary pairings.
2. The root divides them \(1+3\). Choose the singleton in four ways and the
   pair internal to the remaining triple in three ways, giving twelve.

Therefore

\[
\boxed{3+12=15}.
\]

The three balanced trees have equal-depth leaves. The twelve unbalanced trees
do not. Selecting either shape family is a \(P_1\) coding condition; the sole
distinction rule selects neither.

## Theorem 4 — no single binary hierarchy is the atomic \(P_4\) relation

Every complete binary hierarchy on four leaves contains at least one proper
non-singleton cluster. That cluster is an intermediate distinction absent
from the atomic \(P_4\) presentation.

A balanced hierarchy has \(8\) leaf automorphisms. An unbalanced hierarchy has
\(2\). Both are proper subgroups of the \(24\) automorphisms of the atomic
four-resultant occurrence.

Thus no single \(P_1\) binary hierarchy preserves the full symmetry of the
presented \(P_4\) referent:

\[
\boxed{\text{one }P_4\text{ occurrence}\not\equiv
\text{one chosen }P_1\text{ binary tree}.}
\]

The loss is not repaired by giving four leaves binary names. The intermediate
clusters remain part of the binary tree even after the names are changed.

## Theorem 5 — complete binary-presentation fiber

Let \(H\) be a finite atomic \(P_4\) incidence presentation with \(m\) event
occurrences. For every event \(e\), let \(\mathcal T(e)\) be its fifteen
complete binary presentations. Define

\[
\mathcal B(H)=\prod_{e\in H}\mathcal T(e).
\]

Then

\[
\boxed{|\mathcal B(H)|=15^m}.
\]

Every automorphism of \(H\) acts on \(\mathcal B(H)\) by relabelling
resultants and events. Two binary presentations are isomorphic as \(P_1\)
structures exactly when they belong to the same orbit of that action.
Therefore the distinct \(P_1\) shadow forms over the one source presentation
are exactly

\[
\boxed{\mathcal B(H)/\operatorname{Aut}(H)}.
\]

The quotient classifies shadows; it does not delete the underlying
assignments. The audit retains every orbit together with its exact size, whose
sum is \(15^m\).

## Theorem 6 — descent criterion for a cross-perspective law

Let \(f\) be any quantity calculated by \(P_1\) on complete binary
presentations. It defines a quantity of the atomic source presentation \(H\)
only if

\[
f(T)=f(T')
\qquad
\text{for every }T,T'\in\mathcal B(H).
\]

### Proof

Every member of \(\mathcal B(H)\) forgets to the same atomic incidence
presentation \(H\). If two such presentations give different values, the
difference is caused by a distinction retained in the binary presentation
but absent from \(H\). The value therefore cannot be determined by \(H\)
alone. Conversely, a constant value on the complete fiber is independent of
the binary choice and descends unambiguously to \(H\). ∎

This is stronger than invariance under relabelling one chosen code. A
calculation may be invariant under that code's automorphisms and still vary
between balanced and unbalanced codes.

## Theorem 7 — descent of a complete-fiber construction

The preceding criterion concerns a scalar calculated separately on each
binary presentation. There is a second admissible construction. Let
\(\mathcal B(H)\) be the *entire* presentation fiber and let \(F\) be a
construction satisfying

\[
F(g\mathcal B(H))\cong F(\mathcal B(H))
\qquad
\text{for every }g\in\operatorname{Aut}(H),
\]

where \(\cong\) removes only presentation names. Then the isomorphism class
of \(F(\mathcal B(H))\) is determined by \(H\).

### Proof

The complete fiber is determined by \(H\): it contains every faithful binary
presentation and no selected representative. An automorphism of \(H\)
permutes members of the fiber and relabels their resultants; it does not add
or remove a member. If \(F\) is unchanged up to isomorphism under that action,
its output does not depend on names, enumeration order, branch orientation,
or a preferred binary hierarchy. It therefore descends as a \(P_1\)
description of a source-determined invariant. ∎

This theorem does **not** say that the output is native mathematics inside
\(P_4\). It says precisely that \(P_1\) did not obtain it by selecting one
of its incompatible presentations.

## Consequence for the RH branch

Complex coordinates, binary trees, sums, matrices, spectra, probabilities,
and equations are \(P_1\) structures. They may be used to present a
hypothetical source, but a result calculated in one such presentation cannot
be declared a \(P_4\) law unless it passes Theorem 6.

The earlier RH attempts repeatedly selected one \(P_1\) presentation and
treated a property of it as native to another perspective. The game now gives
an exact test for that mistake. The complete-refinement construction uses
Theorem 7: it retains every binary refinement and extracts a symmetric
incidence invariant. Whether that independently generated invariant has the
classical zeta-zero structure is decided only after the invariant is frozen.
