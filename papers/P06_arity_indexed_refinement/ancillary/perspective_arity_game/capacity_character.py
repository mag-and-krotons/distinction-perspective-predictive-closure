"""Capacity characters on the isomorphism-class component realization.

No connected class is assigned a preferred numerical weight.  A faithful P1
presentation instead gives the countable connected class generators a
prefix-free binary code.  Different codes are retained as a fiber.  Kraft
conservation is common to that code fiber.  ``SYMMETRY_REALIZATION.md`` proves
that treating each isomorphism class as one generator is itself a P1
decategorification, so these analytic laws are conditional on that
realization and are not promoted to the undevaluated source.
"""

from __future__ import annotations

from fractions import Fraction
from collections import Counter
from typing import Iterable


def kraft_sum(lengths: Iterable[int], base: int = 2) -> Fraction:
    if base < 2:
        raise ValueError("base must have at least two resultants")
    total = Fraction(0)
    for length in lengths:
        if length < 0:
            raise ValueError("code lengths must be nonnegative")
        total += Fraction(1, base**length)
    return total


def is_prefix_free(words: Iterable[str]) -> bool:
    ordered = sorted(words)
    if len(ordered) != len(set(ordered)):
        return False
    return all(
        not right.startswith(left)
        for left, right in zip(ordered, ordered[1:])
    )


def binary_complete_length_profile(symbol_count: int) -> tuple[int, ...]:
    """Least-maximum-length complete binary profile for N symbols.

    For N>1, lengths are L-1 and L where L=ceil(log_2 N).  The number at
    length L-1 is 2^L-N; Kraft equality determines the rest.  No assignment
    of words to source forms is selected here.
    """

    if symbol_count < 1:
        raise ValueError("at least one symbol is required")
    if symbol_count == 1:
        return (0,)
    maximum = (symbol_count - 1).bit_length()
    shorter = 2**maximum - symbol_count
    return (maximum - 1,) * shorter + (maximum,) * (symbol_count - shorter)


def canonical_binary_words(lengths: Iterable[int]) -> tuple[str, ...]:
    """One audit realization of a valid ordered binary length profile."""

    ordered = sorted(lengths)
    if not ordered:
        return ()
    if kraft_sum(ordered) > 1:
        raise ValueError("length profile violates binary capacity")
    code = 0
    previous = ordered[0]
    words: list[str] = []
    for length in ordered:
        code <<= length - previous
        words.append(format(code, f"0{length}b") if length else "")
        code += 1
        previous = length
    if not is_prefix_free(words):
        raise AssertionError("canonical construction failed prefix freedom")
    return tuple(words)


def unary_rank_prefix(rank: int) -> str:
    """One explicit self-delimiting rank presentation, not a native choice."""

    if rank < 1:
        raise ValueError("rank must be positive")
    return "1" * (rank - 1) + "0"


def ranked_connected_code(
    connected_counts: tuple[int, ...],
) -> tuple[tuple[int, int, str], ...]:
    """One complete audit code for connected types grouped by event rank.

    Rank uses the prefix-free words 0, 10, 110, ... .  Within each rank an
    optimal complete binary profile is used.  Assigning the resulting words
    to individual native forms remains arbitrary and is not interpreted.
    """

    result: list[tuple[int, int, str]] = []
    for rank, count in enumerate(connected_counts, start=1):
        prefix = unary_rank_prefix(rank)
        local_words = canonical_binary_words(
            binary_complete_length_profile(count)
        )
        result.extend(
            (rank, index, prefix + word)
            for index, word in enumerate(local_words)
        )
    words = tuple(word for _, _, word in result)
    if not is_prefix_free(words):
        raise AssertionError("ranked code is not prefix-free")
    return tuple(result)


def absolute_character_sum(
    lengths: Iterable[int],
    sigma: float,
    base: int = 2,
) -> float:
    """sum base^(-sigma*length), the absolute Euler-log first order."""

    if base < 2:
        raise ValueError("base must have at least two resultants")
    return sum(base ** (-sigma * length) for length in lengths)


def finite_component_product(
    lengths: Iterable[int],
    parameter: complex,
    base: int = 2,
) -> complex:
    """Finite specialization product_C (1-base^(-s*l_C))^-1."""

    value = 1 + 0j
    for length in lengths:
        if length <= 0:
            raise ValueError("global connected codes require positive lengths")
        value /= 1 - base ** (-parameter * length)
    return value


def finite_completed_product(
    lengths: Iterable[int],
    parameter: complex,
    base: int = 2,
) -> complex:
    """Completion with the half-prefactor forced by character inversion."""

    frozen = tuple(lengths)
    total_length = sum(frozen)
    return base ** (-parameter * total_length / 2) * finite_component_product(
        frozen,
        parameter,
        base,
    )


def reciprocal_zero(length: int, index: int, base: int = 2) -> complex:
    """A zero of 1-base^(-s*length), in the cost-dual coordinate."""

    if length <= 0:
        raise ValueError("length must be positive")
    if base < 2:
        raise ValueError("base must have at least two resultants")
    from cmath import pi

    return 2j * pi * index / (length * log_base_natural(base))


def finite_log_curvature(
    lengths: Iterable[int],
    parameter: complex,
    base: int = 2,
) -> complex:
    """Second logarithmic derivative of the component product.

    Each summand is a^2/(4*sinh(a*s/2)^2), with a=length*log(base).
    It is termwise even and removes the affine inversion cocycle.
    """

    from cmath import sinh

    value = 0j
    for length in lengths:
        if length <= 0:
            raise ValueError("global connected codes require positive lengths")
        scale = length * log_base_natural(base)
        denominator = 4 * sinh(parameter * scale / 2) ** 2
        if denominator == 0:
            raise ZeroDivisionError("parameter is a pole of the log curvature")
        value += scale * scale / denominator
    return value


def length_enumerator(lengths: Iterable[int]) -> dict[int, int]:
    return dict(sorted(Counter(lengths).items()))


def finite_log_via_length_enumerator(
    lengths: Iterable[int],
    parameter: complex,
    terms: int,
    base: int = 2,
) -> complex:
    """Truncated sum_r A(base^(-r*s))/r for a finite code."""

    if terms < 1:
        raise ValueError("terms must be positive")
    enumerator = length_enumerator(lengths)
    value = 0j
    for repeat in range(1, terms + 1):
        value += sum(
            count * base ** (-repeat * parameter * length)
            for length, count in enumerator.items()
        ) / repeat
    return value


def log_base_natural(base: int) -> float:
    from math import log

    return log(base)


def unit_strip_coordinate(capacity_coordinate: complex) -> complex:
    """Normalize capacity boundaries -1,+1 to conventional 0,1."""

    return (capacity_coordinate + 1) / 2


def capacity_strip_coordinate(unit_coordinate: complex) -> complex:
    return 2 * unit_coordinate - 1


def normalized_reciprocal_zero(length: int, index: int, base: int = 2) -> complex:
    return unit_strip_coordinate(reciprocal_zero(length, index, base))


def audit(connected_counts: tuple[int, ...]) -> dict:
    code = ranked_connected_code(connected_counts)
    lengths = tuple(len(word) for _, _, word in code)
    return {
        "connected_counts_by_event_rank": connected_counts,
        "encoded_connected_generators": len(code),
        "prefix_free": is_prefix_free(word for _, _, word in code),
        "finite_horizon_Kraft_sum": str(kraft_sum(lengths)),
        "Kraft_sum_as_float": float(kraft_sum(lengths)),
        "absolute_character_sums": {
            str(sigma): absolute_character_sum(lengths, sigma)
            for sigma in (1.0, 1.25, 1.5, 2.0)
        },
        "total_code_length": sum(lengths),
        "length_enumerator": length_enumerator(lengths),
        "finite_completion_parity": (
            "even" if len(lengths) % 2 == 0 else "odd"
        ),
        "interpretation": (
            "the displayed code is one audit member; only prefix capacity and "
            "the resulting Re(s)>1 convergence law descend across all codes"
        ),
    }
