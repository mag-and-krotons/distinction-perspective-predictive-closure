"""The complete P1 counting shadow of interacting atomic distinctions.

Starting from no presented event, one atomic q-resultant event is adjoined at
each step.  If n resultants are already presented, a new event may share any
r of them, 0 <= r <= q, and creates q-r fresh resultants.  Every choice is
retained.  No probability, geometry, update preference, or target sequence is
used.

The coefficient of x**n in A_m^(q)(x) is the number of retained raw P1
histories with m events and n presented resultants.  Resultant renamings
permute the histories, so their complete aggregate is unchanged.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial


Polynomial = tuple[int, ...]  # ascending powers


def trim(coefficients: list[int]) -> Polynomial:
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)


def interaction_step(coefficients: Polynomial, arity: int) -> Polynomial:
    """Apply T_q = x^q sum_{r=0}^q D^r/r! exactly.

    For c*x^n, D^r/r! contributes c*binom(n,r)*x^(n-r).  The
    binomial coefficient is exactly the number of r-member sharing choices.
    Multiplication by x^q records the q-r newly introduced resultants.
    """

    if arity < 1:
        raise ValueError("arity must be positive")
    output = [0] * (len(coefficients) + arity)
    for current_resultants, count in enumerate(coefficients):
        if count == 0:
            continue
        for shared in range(min(arity, current_resultants) + 1):
            final_resultants = current_resultants + arity - shared
            output[final_resultants] += count * comb(current_resultants, shared)
    return trim(output)


def interaction_polynomial(arity: int, event_count: int) -> Polynomial:
    """A_m^(q), with A_0=1 and A_(m+1)=T_q A_m."""

    if event_count < 0:
        raise ValueError("event_count must be nonnegative")
    polynomial: Polynomial = (1,)
    for _ in range(event_count):
        polynomial = interaction_step(polynomial, arity)
    return polynomial


def evaluate(coefficients: Polynomial, value: int) -> int:
    return sum(coefficient * value**power for power, coefficient in enumerate(coefficients))


def history_count(arity: int, event_count: int) -> int:
    return evaluate(interaction_polynomial(arity, event_count), 1)


def normalized_kernel_descending(arity: int) -> tuple[int, ...]:
    """Coefficients of q! E_q(z), from z^q down to z^0.

    E_q(z)=sum_{r=0}^q z^r/r! is forced by the permitted sharing counts.
    """

    if arity < 1:
        raise ValueError("arity must be positive")
    return tuple(
        factorial(arity) // factorial(power)
        for power in range(arity, -1, -1)
    )


def routh_first_column(descending: tuple[int, ...]) -> tuple[Fraction, ...]:
    """Exact Routh first column for a real polynomial.

    The finite audits used here encounter no zero pivot.  A zero pivot is
    reported rather than repaired by an auxiliary convention.
    """

    if len(descending) < 2 or descending[0] == 0:
        raise ValueError("a nonconstant polynomial with nonzero lead is required")
    degree = len(descending) - 1
    columns = (degree + 2) // 2
    table = [
        [Fraction(0) for _ in range(columns)]
        for _ in range(degree + 1)
    ]
    for column, value in enumerate(descending[0::2]):
        table[0][column] = Fraction(value)
    for column, value in enumerate(descending[1::2]):
        table[1][column] = Fraction(value)
    for row in range(2, degree + 1):
        pivot = table[row - 1][0]
        if pivot == 0:
            raise ZeroDivisionError("zero Routh pivot")
        for column in range(columns - 1):
            table[row][column] = (
                pivot * table[row - 2][column + 1]
                - table[row - 2][0] * table[row - 1][column + 1]
            ) / pivot
    return tuple(row[0] for row in table)


def is_strictly_hurwitz(descending: tuple[int, ...]) -> bool:
    """Whether every root lies in the open left half-plane."""

    try:
        column = routh_first_column(descending)
    except ZeroDivisionError:
        return False
    return all(value > 0 for value in column) or all(value < 0 for value in column)


def nonzero_core_descending(coefficients: Polynomial) -> tuple[int, ...]:
    """Remove the forced zero at x=0 and return descending coefficients."""

    first_nonzero = next(
        (index for index, coefficient in enumerate(coefficients) if coefficient),
        None,
    )
    if first_nonzero is None:
        raise ValueError("zero polynomial")
    return tuple(reversed(coefficients[first_nonzero:]))


def third_hurwitz_determinant_of_kernel(arity: int) -> int:
    """The third Hurwitz determinant of q! E_q, for q >= 4."""

    if arity < 4:
        raise ValueError("the third determinant in this form requires arity >= 4")
    q = arity
    return q * q * (q - 1) * (q - 2) * (-q * q + 5 * q - 2)


def audit(arity: int, max_events: int) -> dict:
    rows = []
    for event_count in range(1, max_events + 1):
        polynomial = interaction_polynomial(arity, event_count)
        core = nonzero_core_descending(polynomial)
        rows.append(
            {
                "events_P1_coordinate": event_count,
                "minimum_presented_resultants": next(
                    i for i, coefficient in enumerate(polynomial) if coefficient
                ),
                "maximum_presented_resultants": len(polynomial) - 1,
                "retained_raw_histories": sum(polynomial),
                "coefficient_count": sum(coefficient != 0 for coefficient in polynomial),
                "nonzero_zero_set_strictly_left_half_plane": (
                    True if len(core) == 1 else is_strictly_hurwitz(core)
                ),
            }
        )
    return {
        "arity_P1_coordinate": arity,
        "kernel_coefficients_descending": normalized_kernel_descending(arity),
        "kernel_strictly_left_half_plane": is_strictly_hurwitz(
            normalized_kernel_descending(arity)
        ),
        "third_kernel_Hurwitz_determinant": (
            third_hurwitz_determinant_of_kernel(arity) if arity >= 4 else None
        ),
        "event_layers": rows,
    }
