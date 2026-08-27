"""Identity-and-symmetry-preserving lift of native incidence forms.

The native source is a family of finite incidence structures, not a scalar
count.  Giving every isomorphism class weight one and giving every labelled
presentation weight one are different P1 decategorifications.  This module
keeps the second route honest by dividing each isomorphism class by its full
event/resultant automorphism order.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations
from math import comb, factorial

from native_extension import NativeExtensionData, incidence_components
from primitive import History


Bidegree = tuple[int, int]
Series = dict[Bidegree, Fraction]


def automorphism_order(history: History) -> int:
    """Full automorphism order of the event/resultant incidence structure."""

    event_count = len(history)
    vertices = tuple(sorted({vertex for event in history for vertex in event}))
    columns = tuple(
        tuple(int(vertex in event) for event in history)
        for vertex in vertices
    )
    multiplicities = Counter(columns)

    # Resultants with the same incidence column may be permuted freely.
    resultant_kernel = 1
    for multiplicity in multiplicities.values():
        resultant_kernel *= factorial(multiplicity)

    # An event permutation is admissible exactly when it preserves the
    # multiset of resultant-incidence columns.
    admissible_event_permutations = 0
    for event_permutation in permutations(range(event_count)):
        transformed = Counter(
            tuple(column[index] for index in event_permutation)
            for column in columns
        )
        if transformed == multiplicities:
            admissible_event_permutations += 1

    return admissible_event_permutations * resultant_kernel


def labelled_incidence_count(
    arity: int,
    event_count: int,
    resultant_count: int,
) -> int:
    """Labelled row-q incidence matrices with no unused resultant.

    Events and resultants are both labelled.  Each event is incident with
    exactly ``arity`` distinct resultants.  Inclusion-exclusion removes
    matrices having an unused resultant.
    """

    if arity < 1 or event_count < 0 or resultant_count < 0:
        raise ValueError("arity must be positive and counts nonnegative")
    return sum(
        (-1) ** omitted
        * comb(resultant_count, omitted)
        * comb(resultant_count - omitted, arity) ** event_count
        for omitted in range(resultant_count + 1)
    )


def symmetry_carrier_coefficient(
    arity: int,
    event_count: int,
    resultant_count: int,
) -> Fraction:
    """Coefficient of u^m x^n in the symmetry-preserving carrier."""

    return Fraction(
        labelled_incidence_count(arity, event_count, resultant_count),
        factorial(event_count) * factorial(resultant_count),
    )


def symmetry_carrier_value(
    arity: int,
    event_parameter: complex,
    resultant_parameter: complex,
    resultant_terms: int,
) -> complex:
    """Truncate e^-x sum_n exp(u*binom(n,q))*x^n/n!.

    The infinite series is entire in x when Re(u)<=0 for arity>=2.  For
    positive real part it has zero x-radius and this function remains only a
    finite audit truncation.
    """

    if arity < 1 or resultant_terms < 1:
        raise ValueError("arity and resultant_terms must be positive")
    from cmath import exp

    total = 0j
    factorial_n = 1
    power = 1 + 0j
    for resultant_count in range(resultant_terms):
        if resultant_count:
            factorial_n *= resultant_count
            power *= resultant_parameter
        total += (
            exp(event_parameter * comb(resultant_count, arity))
            * power
            / factorial_n
        )
    return exp(-resultant_parameter) * total


def is_connected(history: History) -> bool:
    return len(incidence_components(history)) == 1


def groupoid_series(
    data: NativeExtensionData,
    *,
    connected_only: bool,
) -> Series:
    """Sum one over automorphism order in each bidegree."""

    result: Series = {} if connected_only else {(0, 0): Fraction(1)}
    for event_count, layer in data.representatives.items():
        for history in layer.values():
            if connected_only and not is_connected(history):
                continue
            resultant_count = len({vertex for event in history for vertex in event})
            degree = (event_count, resultant_count)
            result[degree] = result.get(degree, Fraction(0)) + Fraction(
                1,
                automorphism_order(history),
            )
    return result


def multiply_series(
    left: Series,
    right: Series,
    *,
    max_events: int,
    max_resultants: int,
) -> Series:
    result: Series = {}
    for (left_events, left_resultants), left_value in left.items():
        for (right_events, right_resultants), right_value in right.items():
            degree = (
                left_events + right_events,
                left_resultants + right_resultants,
            )
            if degree[0] > max_events or degree[1] > max_resultants:
                continue
            result[degree] = result.get(degree, Fraction(0)) + left_value * right_value
    return {degree: value for degree, value in result.items() if value}


def exponential_series(
    connected: Series,
    *,
    max_events: int,
    max_resultants: int,
) -> Series:
    """Truncated formal exp of a positive-event bivariate series."""

    if (0, 0) in connected:
        raise ValueError("connected series must have zero constant term")
    result: Series = {(0, 0): Fraction(1)}
    power: Series = {(0, 0): Fraction(1)}
    for repeat in range(1, max_events + 1):
        power = multiply_series(
            power,
            connected,
            max_events=max_events,
            max_resultants=max_resultants,
        )
        scale = factorial(repeat)
        for degree, value in power.items():
            result[degree] = result.get(degree, Fraction(0)) + value / scale
    return {degree: value for degree, value in result.items() if value}


def orbit_reconstructed_labelled_count(
    data: NativeExtensionData,
    event_count: int,
    resultant_count: int,
) -> int:
    """Recover labelled objects from isomorphism orbits."""

    return sum(
        factorial(event_count)
        * factorial(resultant_count)
        // automorphism_order(history)
        for history in data.representatives[event_count].values()
        if len({vertex for event in history for vertex in event}) == resultant_count
    )


def audit(data: NativeExtensionData) -> dict:
    all_series = groupoid_series(data, connected_only=False)
    connected = groupoid_series(data, connected_only=True)
    max_resultants = data.arity * data.max_events
    reconstructed = exponential_series(
        connected,
        max_events=data.max_events,
        max_resultants=max_resultants,
    )

    layers = []
    for event_count, layer in data.representatives.items():
        resultant_counts = sorted(
            {
                len({vertex for event in history for vertex in event})
                for history in layer.values()
            }
        )
        bidegrees = []
        for resultant_count in resultant_counts:
            orbit_count = orbit_reconstructed_labelled_count(
                data,
                event_count,
                resultant_count,
            )
            direct_count = labelled_incidence_count(
                data.arity,
                event_count,
                resultant_count,
            )
            bidegrees.append(
                {
                    "resultants_P1_coordinate": resultant_count,
                    "labelled_incidence_presentations": direct_count,
                    "orbit_reconstruction": orbit_count,
                    "exact_match": orbit_count == direct_count,
                    "groupoid_weight": str(
                        all_series[(event_count, resultant_count)]
                    ),
                }
            )
        layers.append(
            {
                "events_P1_coordinate": event_count,
                "native_classes": len(layer),
                "automorphism_order_histogram": {
                    str(order): count
                    for order, count in sorted(
                        Counter(automorphism_order(history) for history in layer.values()).items()
                    )
                },
                "bidegrees": bidegrees,
            }
        )

    return {
        "status": (
            "P1 symmetry-preserving realization of the complete labelled "
            "presentation groupoid; not promoted to a source-native scalar"
        ),
        "arity_P1_coordinate": data.arity,
        "layers": layers,
        "all_labelled_counts_reconstructed_from_orbits": all(
            row["exact_match"]
            for layer in layers
            for row in layer["bidegrees"]
        ),
        "component_groupoid_exponential_identity": all_series == reconstructed,
        "identity": (
            "H(u,x)=exp(C(u,x)) after weighting every form by the inverse "
            "of its full event/resultant automorphism order"
        ),
        "closed_carrier": (
            "H_q(u,x)=exp(-x)*sum_{n>=0} "
            "exp(u*binomial(n,q))*x^n/n!"
        ),
        "analytic_phase_for_arity_at_least_two": (
            "as an x-series it is entire for Re(u)<=0 and has zero radius "
            "for Re(u)>0"
        ),
        "non_descent": (
            "uniform isomorphism-class multiplicity gives geometric factors, "
            "whereas the full symmetry lift gives exponential factors; their "
            "analytic zero/pole laws differ"
        ),
    }
