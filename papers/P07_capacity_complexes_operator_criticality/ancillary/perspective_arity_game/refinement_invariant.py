"""The complete P1 refinement shadow of an atomic Pq distinction.

No target function is used.  A partition records only which co-resultants a
P1 presentation has or has not yet distinguished.  Retaining every possible
binary refinement produces the complete finite refinement structure.
"""

from __future__ import annotations

import cmath
from functools import lru_cache
from math import factorial
from typing import Iterable


Block = tuple[int, ...]
Partition = tuple[Block, ...]


def canonical_partition(blocks: Iterable[Iterable[int]]) -> Partition:
    return tuple(
        sorted(
            (tuple(sorted(block)) for block in blocks),
            key=lambda block: (block[0], len(block), block),
        )
    )


def relabel_partition(partition: Partition, permutation: tuple[int, ...]) -> Partition:
    """Apply a P1 name permutation without changing the represented state."""

    if sorted(permutation) != list(range(len(permutation))):
        raise ValueError("permutation must contain each label exactly once")
    return canonical_partition(
        tuple(permutation[value] for value in block)
        for block in partition
    )


@lru_cache(maxsize=None)
def partitions_of(values: tuple[int, ...]) -> tuple[Partition, ...]:
    """All set partitions, generated without selecting a block order."""

    if not values:
        return ((),)
    first, *rest = values
    smaller = partitions_of(tuple(rest))
    result: set[Partition] = set()
    for partition in smaller:
        # The new resultant may form a new indistinguishability block.
        result.add(canonical_partition(((first,), *partition)))
        # Or it may remain indistinguishable from any existing block.
        for index in range(len(partition)):
            blocks = list(partition)
            blocks[index] = tuple(sorted((*blocks[index], first)))
            result.add(canonical_partition(blocks))
    return tuple(sorted(result, key=lambda p: (len(p), p)))


def partition_lattice(arity: int) -> tuple[Partition, ...]:
    if arity < 1:
        raise ValueError("arity must be positive")
    return partitions_of(tuple(range(arity)))


def refines(finer: Partition, coarser: Partition) -> bool:
    """Whether every finer block lies inside a coarser block."""

    coarser_sets = tuple(frozenset(block) for block in coarser)
    return all(
        any(frozenset(block) <= target for target in coarser_sets)
        for block in finer
    )


def covers(coarser: Partition, finer: Partition) -> bool:
    """One P1 binary distinction: exactly one block becomes two."""

    return (
        len(finer) == len(coarser) + 1
        and refines(finer, coarser)
    )


def cover_map(arity: int) -> dict[Partition, tuple[Partition, ...]]:
    lattice = partition_lattice(arity)
    return {
        source: tuple(target for target in lattice if covers(source, target))
        for source in lattice
    }


def maximal_binary_refinement_chains(arity: int) -> tuple[tuple[Partition, ...], ...]:
    """Every P1 history from one block to singleton blocks."""

    bottom = canonical_partition((range(arity),))
    top = canonical_partition((range(i, i + 1) for i in range(arity)))
    successors = cover_map(arity)
    chains: list[tuple[Partition, ...]] = []

    def visit(path: tuple[Partition, ...]) -> None:
        current = path[-1]
        if current == top:
            chains.append(path)
            return
        for target in successors[current]:
            visit(path + (target,))

    visit((bottom,))
    return tuple(chains)


def mobius_from_indiscrete(arity: int) -> dict[Partition, int]:
    """Incidence inverse forced by the complete refinement order."""

    lattice = partition_lattice(arity)
    bottom = canonical_partition((range(arity),))
    values: dict[Partition, int] = {bottom: 1}
    for target in sorted(lattice, key=lambda partition: len(partition)):
        if target == bottom:
            continue
        values[target] = -sum(
            value
            for source, value in values.items()
            if source != target and refines(target, source)
        )
    return values


def characteristic_coefficients(arity: int) -> dict[int, int]:
    """Coefficients by exponent, highest exponent first when rendered."""

    coefficients: dict[int, int] = {}
    for partition, value in mobius_from_indiscrete(arity).items():
        rank = len(partition) - 1
        exponent = (arity - 1) - rank
        coefficients[exponent] = coefficients.get(exponent, 0) + value
    return coefficients


def evaluate_polynomial(coefficients: dict[int, int], value: int) -> int:
    return sum(coefficient * value**exponent for exponent, coefficient in coefficients.items())


def recurrence_characteristic_coefficients(arity: int) -> dict[int, int]:
    """Generate C_q from C_{q+1}=(t-1)(q C_q-t C'_q)."""

    coefficients = {0: 1}  # C_1(t)
    for current_arity in range(1, arity):
        polar_part = {
            exponent: (current_arity - exponent) * coefficient
            for exponent, coefficient in coefficients.items()
        }
        updated: dict[int, int] = {}
        for exponent, coefficient in polar_part.items():
            updated[exponent + 1] = updated.get(exponent + 1, 0) + coefficient
            updated[exponent] = updated.get(exponent, 0) - coefficient
        coefficients = {e: c for e, c in updated.items() if c}
    return coefficients


def expected_chain_count(arity: int) -> int:
    """Product of all choices when merging singleton blocks pairwise."""

    result = 1
    for block_count in range(arity, 1, -1):
        result *= block_count * (block_count - 1) // 2
    return result


def expected_top_mobius(arity: int) -> int:
    return (-1) ** (arity - 1) * factorial(arity - 1)


def carrier_value(rank_weight: float, coordinate: complex) -> complex:
    """The normalized all-arity carrier Q_t(z)."""

    if rank_weight == 0:
        raise ValueError("rank_weight must be nonzero")
    return (cmath.exp(rank_weight * coordinate) + rank_weight - 1) / rank_weight


def carrier_zero(rank_weight: float, index: int) -> complex:
    """The exact zero z_index(t), for a positive real t > 1."""

    if rank_weight <= 1:
        raise ValueError("zero formula requires rank_weight > 1")
    return (
        cmath.log(rank_weight - 1) + (2 * index + 1) * cmath.pi * 1j
    ) / rank_weight


def audit(arity: int) -> dict:
    lattice = partition_lattice(arity)
    chains = maximal_binary_refinement_chains(arity)
    mobius = mobius_from_indiscrete(arity)
    top = canonical_partition((range(i, i + 1) for i in range(arity)))
    encountered = {partition for chain in chains for partition in chain}
    common = set(chains[0]).intersection(*map(set, chains[1:])) if chains else set()
    characteristic = characteristic_coefficients(arity)
    predicted = recurrence_characteristic_coefficients(arity)

    return {
        "arity_P1_coordinate": arity,
        "partial_distinguishability_states": len(lattice),
        "maximal_binary_refinement_histories": len(chains),
        "expected_history_count": expected_chain_count(arity),
        "all_states_occur_in_some_history": encountered == set(lattice),
        "states_common_to_every_history": len(common),
        "common_states_are_only_endpoints": len(common) == 2 if arity > 1 else len(common) == 1,
        "top_inversion_weight": mobius[top],
        "expected_top_inversion_weight": expected_top_mobius(arity),
        "characteristic_coefficients_by_exponent": {
            str(exponent): characteristic[exponent]
            for exponent in sorted(characteristic, reverse=True)
        },
        "characteristic_matches_source_recurrence": (
            characteristic == predicted
        ),
        "binary_P1_evaluation_at_t_2": evaluate_polynomial(characteristic, 2),
    }
