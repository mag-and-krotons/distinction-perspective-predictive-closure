"""Unweighted native extension relation and its forced incidence inverse.

The raw interaction polynomial counts separately named P1 histories.  This
module removes that accounting choice.  Each native incidence isomorphism
class is one node; an edge records only that deleting one atomic occurrence
from a child can produce the parent.  The resulting finite extension poset
has a unique Möbius inverse and therefore needs no probability or uniform
weight on histories.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from math import comb

from primitive import History, exact_layers, native_classes, native_key


NativeKey = tuple


@dataclass(frozen=True)
class NativeExtensionData:
    arity: int
    max_events: int
    representatives: dict[int, dict[NativeKey, History]]
    level: dict[NativeKey, int]
    parents: dict[NativeKey, frozenset[NativeKey]]
    ancestors: dict[NativeKey, frozenset[NativeKey]]
    mobius_from_initial: dict[NativeKey, int]
    initial: NativeKey


@lru_cache(maxsize=None)
def native_extension_data(arity: int, max_events: int) -> NativeExtensionData:
    if arity < 2:
        raise ValueError("native presented branch requires arity >= 2")
    if max_events < 1:
        raise ValueError("max_events must be positive")

    raw_layers = exact_layers(arity, max_events)
    representatives: dict[int, dict[NativeKey, History]] = {}
    for event_count in range(1, max_events + 1):
        classes = native_classes(raw_layers[event_count], arity)
        representatives[event_count] = {
            key: histories[0] for key, histories in classes.items()
        }

    level = {
        key: event_count
        for event_count, layer in representatives.items()
        for key in layer
    }
    initial = next(iter(representatives[1]))
    parents: dict[NativeKey, frozenset[NativeKey]] = {initial: frozenset()}
    ancestors: dict[NativeKey, frozenset[NativeKey]] = {initial: frozenset()}
    mobius: dict[NativeKey, int] = {initial: 1}

    for event_count in range(2, max_events + 1):
        for key, representative in representatives[event_count].items():
            direct = frozenset(
                native_key(
                    representative[:index] + representative[index + 1 :],
                    arity,
                )
                for index in range(event_count)
            )
            parents[key] = direct
            lower = set(direct)
            for parent in direct:
                lower.update(ancestors[parent])
            ancestors[key] = frozenset(lower)
            mobius[key] = -sum(mobius[ancestor] for ancestor in lower)

    return NativeExtensionData(
        arity=arity,
        max_events=max_events,
        representatives=representatives,
        level=level,
        parents=parents,
        ancestors=ancestors,
        mobius_from_initial=mobius,
        initial=initial,
    )


def interval_characteristic(
    data: NativeExtensionData,
    key: NativeKey,
) -> tuple[int, ...]:
    """Ascending coefficients of the forced rank polynomial X_H(t)."""

    top_level = data.level[key]
    coefficients = [0] * top_level
    for source in data.ancestors[key] | {key}:
        exponent = top_level - data.level[source]
        coefficients[exponent] += data.mobius_from_initial[source]
    return tuple(coefficients)


def evaluate(coefficients: tuple[int, ...], value: int) -> int:
    return sum(coefficient * value**power for power, coefficient in enumerate(coefficients))


def raw_two_event_polynomial(arity: int) -> tuple[int, ...]:
    """Every named sharing choice is counted separately."""

    return (0,) * arity + tuple(comb(arity, power) for power in range(arity + 1))


def native_two_event_support_polynomial(arity: int) -> tuple[int, ...]:
    """Every overlap isomorphism type is given one occurrence."""

    return (0,) * arity + (1,) * (arity + 1)


def incidence_components(history: History) -> tuple[tuple[int, ...], ...]:
    """Unique components of atomic occurrences joined by shared resultants."""

    unseen = set(range(len(history)))
    components: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        component = {start}
        frontier = [start]
        while frontier:
            source = frontier.pop()
            source_resultants = set(history[source])
            linked = {
                target
                for target in unseen
                if source_resultants.intersection(history[target])
            }
            unseen.difference_update(linked)
            component.update(linked)
            frontier.extend(sorted(linked))
        components.append(tuple(sorted(component)))
    return tuple(sorted(components))


def connected_class_counts(data: NativeExtensionData) -> tuple[int, ...]:
    """c_m: native types with m events and one incidence component."""

    return tuple(
        sum(
            len(incidence_components(history)) == 1
            for history in data.representatives[event_count].values()
        )
        for event_count in range(1, data.max_events + 1)
    )


def euler_transform(connected_counts: tuple[int, ...]) -> tuple[int, ...]:
    """One-per-isomorphism-class component realization.

    The returned tuple includes the empty coefficient u_0=1.  This is a
    formal identity after giving every unlabelled multiset class coefficient
    one, not an analytic convergence assertion and not the only numerical
    realization of the identity-preserving source groupoid.
    """

    maximum = len(connected_counts)
    totals = [1]
    for n in range(1, maximum + 1):
        divisor_sum = [0] * (n + 1)
        for k in range(1, n + 1):
            divisor_sum[k] = sum(
                divisor * connected_counts[divisor - 1]
                for divisor in range(1, k + 1)
                if k % divisor == 0
            )
        numerator = sum(divisor_sum[k] * totals[n - k] for k in range(1, n + 1))
        if numerator % n:
            raise AssertionError("Euler transform did not remain integral")
        totals.append(numerator // n)
    return tuple(totals)


def audit(arity: int, max_events: int) -> dict:
    data = native_extension_data(arity, max_events)
    connected_counts = connected_class_counts(data)
    reconstructed_totals = euler_transform(connected_counts)
    layers = []
    for event_count, layer in data.representatives.items():
        mobius_histogram = Counter(
            data.mobius_from_initial[key] for key in layer
        )
        polynomial_histogram = Counter(
            interval_characteristic(data, key) for key in layer
        )
        binary_histogram = Counter(
            evaluate(interval_characteristic(data, key), 2) for key in layer
        )
        layers.append(
            {
                "events_P1_coordinate": event_count,
                "native_incidence_classes": len(layer),
                "connected_native_classes": connected_counts[event_count - 1],
                "component_product_reconstructs_total": (
                    reconstructed_totals[event_count] == len(layer)
                ),
                "mobius_residue_histogram": {
                    str(value): count
                    for value, count in sorted(mobius_histogram.items())
                },
                "distinct_interval_characteristic_polynomials": len(
                    polynomial_histogram
                ),
                "binary_rank_character_histogram": {
                    str(value): count
                    for value, count in sorted(binary_histogram.items())
                },
                "binary_null_classes": binary_histogram[0],
                "all_noninitial_polynomials_vanish_at_one": all(
                    event_count == 1
                    or evaluate(interval_characteristic(data, key), 1) == 0
                    for key in layer
                ),
            }
        )
    return {
        "status": (
            "unweighted native extension relation; no uniform history or "
            "isomorphism-class accounting is used in its Mobius values"
        ),
        "arity_P1_coordinate": arity,
        "two_event_accounting_counterexample": {
            "raw_named_history_coefficients": raw_two_event_polynomial(arity),
            "one_per_native_class_coefficients": (
                native_two_event_support_polynomial(arity)
            ),
            "interpretation": (
                "these accountings have different zero geometry, so neither "
                "zero law descends from the unweighted source relation"
            ),
        },
        "layers": layers,
        "component_factorization": {
            "connected_counts_by_event_number": connected_counts,
            "all_native_counts_including_empty": reconstructed_totals,
            "formal_identity": (
                "in the one-per-isomorphism-class realization, "
                "U(y)=product_{m>=1}(1-y^m)^(-c_m); no analytic "
                "convergence, zero set, or accounting descent is asserted"
            ),
        },
    }
