"""The nontrivial binary character of atomic-incidence capacity.

In the symmetry carrier, n presented resultants admit binomial(n,q) atomic
q-incidences.  P1 has one nontrivial sign character, so composing all those
binary flips gives (-1)^binomial(n,q).  For q a power of two this character is
exactly one binary digit of n and its exponential carrier obeys a finite
constant-coefficient differential law.
"""

from __future__ import annotations

from math import comb


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def incidence_capacity_parity(resultant_count: int, arity: int) -> int:
    if resultant_count < 0 or arity < 1:
        raise ValueError("resultant_count must be nonnegative and arity positive")
    return comb(resultant_count, arity) & 1


def binary_capacity_sign(resultant_count: int, arity: int) -> int:
    return -1 if incidence_capacity_parity(resultant_count, arity) else 1


def capacity_digits(resultant_count: int) -> tuple[int, ...]:
    """Recover all binary digits using the seed probe 1, then arities 2,4,... ."""

    if resultant_count < 0:
        raise ValueError("resultant_count must be nonnegative")
    if resultant_count == 0:
        return (0,)
    return tuple(
        incidence_capacity_parity(resultant_count, 1 << bit)
        for bit in range(resultant_count.bit_length())
    )


def reconstruct_from_capacity_digits(digits: tuple[int, ...]) -> int:
    if any(digit not in (0, 1) for digit in digits):
        raise ValueError("capacity digits must be binary")
    return sum(digit << bit for bit, digit in enumerate(digits))


def binary_capacity_egf(
    arity: int,
    coordinate: complex,
    terms: int,
) -> complex:
    """Truncated F_q(x)=sum_n (-1)^C(n,q) x^n/n!."""

    if arity < 1 or terms < 1:
        raise ValueError("arity and terms must be positive")
    total = 0j
    power = 1 + 0j
    factorial_n = 1
    for resultant_count in range(terms):
        if resultant_count:
            power *= coordinate
            factorial_n *= resultant_count
        total += (
            binary_capacity_sign(resultant_count, arity)
            * power
            / factorial_n
        )
    return total


def binary_capacity_closed(arity: int, coordinate: complex) -> complex:
    """Exact finite exponential form for arity 2^j."""

    if not is_power_of_two(arity):
        raise ValueError("closed anti-periodic form requires power-of-two arity")
    from cmath import exp, pi

    period = 2 * arity
    omega = exp(2j * pi / period)
    value = 0j
    for frequency in range(1, period, 2):
        coefficient = 2 / (
            arity * (1 - omega ** (-frequency))
        )
        value += coefficient * exp((omega**frequency) * coordinate)
    return value


def binary_no_unused_carrier(arity: int, coordinate: complex) -> complex:
    """P1 sign specialization H_q(i*pi,x)=exp(-x)F_q(x)."""

    from cmath import exp

    return exp(-coordinate) * binary_capacity_closed(arity, coordinate)


def audit(max_bit: int, sample_limit: int) -> dict:
    if max_bit < 0 or sample_limit < 1:
        raise ValueError("max_bit must be nonnegative and sample_limit positive")
    arities = tuple(1 << bit for bit in range(max_bit + 1))
    return {
        "status": (
            "P1 nontrivial binary sign character of source-generated incidence "
            "capacity; no RH or zeta input"
        ),
        "capacity_probe_sizes_P1_coordinate": arities,
        "unary_probe_status": (
            "q=1 is the single identity seed, not a hypothetical unary "
            "distinguishing perspective; q>=2 are atomic-incidence capacities"
        ),
        "all_sampled_integers_reconstructed_from_capacity_digits": all(
            reconstruct_from_capacity_digits(capacity_digits(value)) == value
            for value in range(sample_limit)
        ),
        "anti_periodicity_verified": {
            str(arity): all(
                binary_capacity_sign(value + arity, arity)
                == -binary_capacity_sign(value, arity)
                for value in range(sample_limit)
            )
            for arity in arities
        },
        "generated_law": (
            "for q=2^j, F_q^(q)(x)+F_q(x)=0 with initial derivatives "
            "F_q^(r)(0)=1 for 0<=r<q"
        ),
        "interpretation": (
            "one identity seed followed by capacities at arities 2,4,... "
            "exposes every binary digit of the P1 resultant-count coordinate"
        ),
    }
