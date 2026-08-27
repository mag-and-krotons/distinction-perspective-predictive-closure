"""A P1 presentation of atomic q-resultant distinction.

Ontology is deliberately not assigned to the Python objects below.

* P0 is not represented: no distinction means no state to encode.
* P1 is the perspective in which distinction has two co-resultants.
* Pq is presented by one atomic q-place incidence.  It is never replaced by
  pairwise inequalities or by a hierarchy of P1 distinctions.

The generator retains every finite incidence continuation.  Event order,
integer names, subset enumeration, and canonical strings are P1 audit
coordinates only.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product
from math import factorial
from typing import Iterable, Iterator


Event = tuple[int, ...]
History = tuple[Event, ...]
Pairing = tuple[tuple[int, int], tuple[int, int]]
BinaryTree = tuple[tuple[int, ...], tuple[int, ...]]
Automorphism = tuple[tuple[int, ...], tuple[tuple[int, int], ...]]


def _normal_event(values: Iterable[int]) -> Event:
    event = tuple(sorted(values))
    if len(event) != len(set(event)):
        raise ValueError("one atomic event cannot repeat a presented resultant")
    return event


def resultants(history: History) -> tuple[int, ...]:
    return tuple(sorted({value for event in history for value in event}))


def initial_history(arity: int) -> History:
    if arity < 2:
        raise ValueError("a presented distinguished perspective needs arity >= 2")
    return (tuple(range(arity)),)


def expand(history: History, arity: int) -> Iterator[History]:
    """Retain every next atomic incidence compatible with arity.

    A new event may share any presented resultants and fills its remaining
    places with fresh P1 tokens.  Enumerating subsets is not asserted to be a
    Pq operation; it is how P1 verifies that no incidence possibility was
    silently removed.
    """

    existing = resultants(history)
    next_token = (max(existing) + 1) if existing else 0
    for shared_count in range(min(arity, len(existing)) + 1):
        for shared in combinations(existing, shared_count):
            fresh_count = arity - shared_count
            fresh = tuple(range(next_token, next_token + fresh_count))
            yield history + (_normal_event((*shared, *fresh)),)


def exact_layers(arity: int, max_events: int) -> dict[int, tuple[History, ...]]:
    if max_events < 1:
        raise ValueError("max_events must be >= 1")
    layers: dict[int, tuple[History, ...]] = {1: (initial_history(arity),)}
    for event_count in range(2, max_events + 1):
        layers[event_count] = tuple(
            child
            for parent in layers[event_count - 1]
            for child in expand(parent, arity)
        )
    return layers


def native_key(history: History, arity: int) -> tuple:
    """Complete finite invariant after all P1 labels and event order vanish."""

    if any(len(event) != arity for event in history):
        raise ValueError("history contains an event of the wrong arity")
    vertices = resultants(history)
    best: tuple[tuple[int, ...], ...] | None = None
    for event_order in permutations(range(len(history))):
        columns = tuple(
            sorted(
                tuple(int(vertex in history[event_index]) for event_index in event_order)
                for vertex in vertices
            )
        )
        if best is None or columns < best:
            best = columns
    if best is None:
        raise AssertionError("empty history is outside this presented branch")
    return arity, len(history), len(vertices), best


def native_classes(histories: Iterable[History], arity: int) -> dict[tuple, list[History]]:
    classes: dict[tuple, list[History]] = {}
    for history in histories:
        classes.setdefault(native_key(history, arity), []).append(history)
    return classes


def pairings_of_four(event: Event) -> tuple[Pairing, Pairing, Pairing]:
    """Every equal-depth P1 presentation of one atomic P4 event.

    This is a retained subview, not the complete binary-presentation fiber.
    """

    if len(event) != 4:
        raise ValueError("binary pairing fibers are defined here only for P4")
    a, b, c, d = event
    return (
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )


def all_binary_presentations(history: History) -> Iterator[tuple[Pairing, ...]]:
    """Retain all P1 binary hierarchies over every atomic P4 event."""

    choices = tuple(pairings_of_four(event) for event in history)
    yield from product(*choices)


def binary_presentation_key(
    history: History,
    presentation: tuple[Pairing, ...],
) -> tuple:
    """Erase all labels while retaining P1's added intermediate pairings.

    For each ordering of atomic events, P1 may also swap the two pair-groups
    inside every event.  A resultant is then represented by its group-membership
    column: 0 absent, 1 in the first pair, 2 in the second pair.  Sorting the
    columns erases resultant names.  Minimizing over event orders and pair
    swaps erases implementation order while retaining exactly the intermediate
    binary structure that P1 added.
    """

    if len(history) != len(presentation):
        raise ValueError("one binary presentation is required per atomic event")
    vertices = resultants(history)
    event_count = len(history)
    best: tuple[tuple[int, ...], ...] | None = None

    for event_order in permutations(range(event_count)):
        for flips in product((False, True), repeat=event_count):
            columns: list[tuple[int, ...]] = []
            for vertex in vertices:
                column: list[int] = []
                for position, event_index in enumerate(event_order):
                    left, right = presentation[event_index]
                    if flips[position]:
                        left, right = right, left
                    if vertex in left:
                        column.append(1)
                    elif vertex in right:
                        column.append(2)
                    else:
                        column.append(0)
                columns.append(tuple(column))
            candidate = tuple(sorted(columns))
            if best is None or candidate < best:
                best = candidate

    if best is None:
        raise AssertionError("empty history is outside this presented branch")
    return 4, event_count, len(vertices), best


def binary_fiber(history: History) -> dict[tuple, list[tuple[Pairing, ...]]]:
    """Classes in the named equal-depth P1 subview of one P4 source."""

    classes: dict[tuple, list[tuple[Pairing, ...]]] = {}
    for presentation in all_binary_presentations(history):
        key = binary_presentation_key(history, presentation)
        classes.setdefault(key, []).append(presentation)
    return classes


def isolated_native_automorphisms(arity: int) -> int:
    """P1 audit count: every permutation preserves one atomic event."""

    return factorial(arity)


def isolated_binary_tree_automorphisms() -> int:
    """P1 audit count for a chosen balanced hierarchy over four leaves."""

    # swap within either pair, and exchange the two pairs
    return 2 * 2 * 2


def complete_binary_trees_of_four(event: Event) -> tuple[BinaryTree, ...]:
    """All complete non-plane P1 binary trees on four labelled leaves.

    A rooted full binary tree on four leaves has two proper internal clusters.
    They are either two disjoint pairs (balanced shape), or a pair nested in a
    triple (unbalanced shape).  The root cluster and singleton leaves are
    implicit.  There are 3 + 12 = 15 labelled trees.
    """

    if len(event) != 4:
        raise ValueError("this finite audit implements complete trees for P4")
    universe = frozenset(event)
    trees: set[BinaryTree] = set()

    # Balanced: two complementary two-member clusters.
    for pair_values in combinations(event, 2):
        pair = frozenset(pair_values)
        complement = universe - pair
        clusters = tuple(
            sorted(
                (tuple(sorted(pair)), tuple(sorted(complement))),
                key=lambda cluster: (len(cluster), cluster),
            )
        )
        trees.add(clusters)  # type: ignore[arg-type]

    # Unbalanced: one pair nested in one triple.
    for triple_values in combinations(event, 3):
        triple = frozenset(triple_values)
        for pair_values in combinations(sorted(triple), 2):
            clusters = (
                tuple(sorted(pair_values)),
                tuple(sorted(triple)),
            )
            trees.add(clusters)

    result = tuple(sorted(trees))
    if len(result) != 15:
        raise AssertionError(f"expected 15 complete binary trees, found {len(result)}")
    return result


def binary_tree_shape(tree: BinaryTree) -> str:
    sizes = sorted(map(len, tree))
    if sizes == [2, 2]:
        return "balanced"
    if sizes == [2, 3]:
        return "unbalanced"
    raise ValueError("not a complete binary tree on four leaves")


def _transformed_column(
    column: tuple[int, ...],
    event_permutation: tuple[int, ...],
) -> tuple[int, ...]:
    transformed = [0] * len(column)
    for source_event, target_event in enumerate(event_permutation):
        transformed[target_event] = column[source_event]
    return tuple(transformed)


def native_automorphism_generators(history: History) -> tuple[Automorphism, ...]:
    """Generate the complete native automorphism action.

    Event permutations are exhaustively checked.  For every admissible event
    permutation one deterministic lift to resultants is retained.  Adjacent
    swaps inside every equal-incidence resultant class generate the kernel.
    Together these generate every automorphism of the finite incidence
    presentation, without making labels native.
    """

    event_count = len(history)
    vertices = resultants(history)
    columns = {
        vertex: tuple(int(vertex in event) for event in history)
        for vertex in vertices
    }
    target_groups: dict[tuple[int, ...], list[int]] = {}
    for vertex, column in columns.items():
        target_groups.setdefault(column, []).append(vertex)
    for group in target_groups.values():
        group.sort()

    candidates: list[Automorphism] = []
    identity_events = tuple(range(event_count))
    identity_vertices = {vertex: vertex for vertex in vertices}
    candidates.append((identity_events, tuple(sorted(identity_vertices.items()))))

    # Kernel generators: swaps invisible to native incidence.
    for group in target_groups.values():
        for index in range(len(group) - 1):
            mapping = dict(identity_vertices)
            left, right = group[index], group[index + 1]
            mapping[left], mapping[right] = right, left
            candidates.append((identity_events, tuple(sorted(mapping.items()))))

    # One lift of every admissible event permutation.
    for event_permutation in permutations(range(event_count)):
        source_groups: dict[tuple[int, ...], list[int]] = {}
        for vertex, column in columns.items():
            transformed = _transformed_column(column, event_permutation)
            source_groups.setdefault(transformed, []).append(vertex)
        if {
            key: len(group) for key, group in source_groups.items()
        } != {
            key: len(group) for key, group in target_groups.items()
        }:
            continue
        mapping: dict[int, int] = {}
        for target_column, source_group in source_groups.items():
            for source, target in zip(
                sorted(source_group),
                target_groups[target_column],
                strict=True,
            ):
                mapping[source] = target
        candidates.append((event_permutation, tuple(sorted(mapping.items()))))

    # Remove duplicate generators while preserving deterministic order.
    return tuple(dict.fromkeys(candidates))


def _transform_tree(
    tree: BinaryTree,
    vertex_mapping: dict[int, int],
) -> BinaryTree:
    return tuple(
        sorted(
            (
                tuple(sorted(vertex_mapping[vertex] for vertex in cluster))
                for cluster in tree
            ),
            key=lambda cluster: (len(cluster), cluster),
        )
    )  # type: ignore[return-value]


def complete_binary_tree_orbits(
    history: History,
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    """Classify every complete P1 binary presentation over one P4 source.

    Returns the orbit representatives (tree indices, one per native event) and
    the corresponding orbit sizes.  The unquotiented 15^m assignments remain
    fully represented by those sizes.
    """

    tree_lists = tuple(complete_binary_trees_of_four(event) for event in history)
    tree_indices = tuple(
        {tree: index for index, tree in enumerate(trees)}
        for trees in tree_lists
    )
    generators = native_automorphism_generators(history)

    actions: list[tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]] = []
    for event_permutation, mapping_items in generators:
        vertex_mapping = dict(mapping_items)
        index_maps: list[tuple[int, ...]] = []
        for source_event, target_event in enumerate(event_permutation):
            mapped_indices = []
            for tree in tree_lists[source_event]:
                mapped = _transform_tree(tree, vertex_mapping)
                mapped_indices.append(tree_indices[target_event][mapped])
            index_maps.append(tuple(mapped_indices))
        actions.append((event_permutation, tuple(index_maps)))

    assignments = set(product(range(15), repeat=len(history)))
    representatives: list[tuple[int, ...]] = []
    orbit_sizes: list[int] = []
    while assignments:
        seed = min(assignments)
        orbit = {seed}
        frontier = [seed]
        while frontier:
            current = frontier.pop()
            for event_permutation, index_maps in actions:
                transformed = [0] * len(history)
                for source_event, target_event in enumerate(event_permutation):
                    transformed[target_event] = index_maps[source_event][
                        current[source_event]
                    ]
                candidate = tuple(transformed)
                if candidate not in orbit:
                    orbit.add(candidate)
                    frontier.append(candidate)
        assignments.difference_update(orbit)
        representatives.append(min(orbit))
        orbit_sizes.append(len(orbit))

    order = sorted(range(len(representatives)), key=representatives.__getitem__)
    return (
        tuple(representatives[index] for index in order),
        tuple(orbit_sizes[index] for index in order),
    )
