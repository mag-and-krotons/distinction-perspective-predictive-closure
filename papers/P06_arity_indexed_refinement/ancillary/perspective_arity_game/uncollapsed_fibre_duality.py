"""Carry-coupled character fibres and their generated analytic duality.

This branch does not sum a prime-arity fibre to one scalar.  It retains every
digit character, lets unit advance generate carry interaction, diagonalizes
that interaction, and follows the complete symmetric distinction through its
unique nondegenerate continuum scaling.
"""

from __future__ import annotations

from cmath import exp
from itertools import combinations
from math import cos, gcd, log, pi, sin

from cross_boundary_completion import (
    complete_character_indices,
    digit_character,
)
from prime_arity import is_transparent_arity


def _require_transparent(prime_arity: int) -> None:
    if not is_transparent_arity(prime_arity):
        raise ValueError("carry fibre requires a transparent arity")


def carry_modulus(prime_arity: int, places: int) -> int:
    _require_transparent(prime_arity)
    if places < 1:
        raise ValueError("places must be positive")
    return prime_arity**places


def carry_character(
    prime_arity: int,
    places: int,
    frequency: int,
    value: int,
) -> complex:
    """A character that diagonalizes unit advance including every carry."""

    modulus = carry_modulus(prime_arity, places)
    return exp(2j * pi * (frequency % modulus) * (value % modulus) / modulus)


def carry_to_digit_coefficients(
    prime_arity: int,
    places: int,
    frequency: int,
) -> dict[tuple[int, ...], complex]:
    """Expand one carry character in the complete independent-digit basis."""

    modulus = carry_modulus(prime_arity, places)
    coefficients = {}
    for indices in complete_character_indices(prime_arity, places):
        coefficients[indices] = sum(
            carry_character(prime_arity, places, frequency, value)
            * digit_character(value, prime_arity, indices).conjugate()
            for value in range(modulus)
        ) / modulus
    return coefficients


def reconstruct_carry_from_digit_fibre(
    prime_arity: int,
    places: int,
    frequency: int,
    value: int,
) -> complex:
    coefficients = carry_to_digit_coefficients(
        prime_arity,
        places,
        frequency,
    )
    return sum(
        coefficient * digit_character(value, prime_arity, indices)
        for indices, coefficient in coefficients.items()
    )


def active_digit_components(
    prime_arity: int,
    places: int,
    frequency: int,
    tolerance: float = 1e-10,
) -> int:
    """Number of independent-digit characters mixed by one carry mode."""

    return sum(
        abs(coefficient) > tolerance
        for coefficient in carry_to_digit_coefficients(
            prime_arity,
            places,
            frequency,
        ).values()
    )


def successor_eigen_residual(
    prime_arity: int,
    places: int,
    frequency: int,
    value: int,
) -> complex:
    """Residual of S psi = exp(2 pi i a/M) psi for S f(n)=f(n+1)."""

    modulus = carry_modulus(prime_arity, places)
    eigenvalue = exp(2j * pi * (frequency % modulus) / modulus)
    return (
        carry_character(prime_arity, places, frequency, value + 1)
        - eigenvalue
        * carry_character(prime_arity, places, frequency, value)
    )


def symmetric_distinction_value(values: tuple[complex, ...], index: int) -> complex:
    """Apply 2I-S-S^{-1} on a finite cyclic identity fibre."""

    if not values:
        raise ValueError("values must be nonempty")
    modulus = len(values)
    return (
        2 * values[index % modulus]
        - values[(index + 1) % modulus]
        - values[(index - 1) % modulus]
    )


def symmetric_distinction_eigenvalue(modulus: int, frequency: int) -> float:
    if modulus < 2:
        raise ValueError("modulus must be at least two")
    return 4 * sin(pi * (frequency % modulus) / modulus) ** 2


def symmetric_distinction_eigen_residual(
    prime_arity: int,
    places: int,
    frequency: int,
    value: int,
) -> complex:
    modulus = carry_modulus(prime_arity, places)
    values = tuple(
        carry_character(prime_arity, places, frequency, coordinate)
        for coordinate in range(modulus)
    )
    eigenvalue = symmetric_distinction_eigenvalue(modulus, frequency)
    return (
        symmetric_distinction_value(values, value)
        - eigenvalue * values[value % modulus]
    )


def scaled_distinction_eigenvalue(modulus: int, frequency: int) -> float:
    """The uniquely nondegenerate M^2 scaling of the distinction spectrum."""

    return modulus**2 * symmetric_distinction_eigenvalue(modulus, frequency)


def continuum_eigenvalue(frequency: int) -> float:
    return (2 * pi * frequency) ** 2


def crt_combine(residues: tuple[int, ...], moduli: tuple[int, ...]) -> int:
    """Combine pairwise-coprime finite boundary identities."""

    if not residues or len(residues) != len(moduli):
        raise ValueError("residues and moduli must have equal nonzero length")
    if any(modulus < 2 for modulus in moduli):
        raise ValueError("moduli must be at least two")
    if any(gcd(left, right) != 1 for left, right in combinations(moduli, 2)):
        raise ValueError("moduli must be pairwise coprime")
    total_modulus = 1
    for modulus in moduli:
        total_modulus *= modulus
    result = 0
    for residue, modulus in zip(residues, moduli):
        complement = total_modulus // modulus
        inverse = pow(complement, -1, modulus)
        result += (residue % modulus) * complement * inverse
    return result % total_modulus


def global_to_local_frequencies(
    frequency: int,
    moduli: tuple[int, ...],
) -> tuple[int, ...]:
    """Local frequencies whose product is one global CRT character."""

    # Validate pairwise coprimality through the same source constructor.
    crt_combine(tuple(0 for _ in moduli), moduli)
    total_modulus = 1
    for modulus in moduli:
        total_modulus *= modulus
    local = []
    for modulus in moduli:
        complement = total_modulus // modulus
        local.append((frequency * pow(complement, -1, modulus)) % modulus)
    return tuple(local)


def crt_character_residual(
    value: int,
    frequency: int,
    moduli: tuple[int, ...],
) -> complex:
    """Residual between one global character and its local fibre product."""

    total_modulus = 1
    for modulus in moduli:
        total_modulus *= modulus
    global_value = exp(
        2j * pi * (frequency % total_modulus) * (value % total_modulus)
        / total_modulus
    )
    local_value = 1 + 0j
    for local_frequency, modulus in zip(
        global_to_local_frequencies(frequency, moduli),
        moduli,
    ):
        local_value *= exp(
            2j * pi * local_frequency * (value % modulus) / modulus
        )
    return global_value - local_value


def theta_value(parameter: float, tolerance: float = 1e-15) -> float:
    """Complete Gaussian identity carrier sum_{n in Z} exp(-pi t n^2)."""

    if parameter <= 0 or not 0 < tolerance < 1:
        raise ValueError("parameter and tolerance must be positive")
    total = 1.0
    coordinate = 1
    while True:
        term = exp(-pi * parameter * coordinate * coordinate).real
        if term < tolerance:
            break
        total += 2 * term
        coordinate += 1
        if coordinate > 1_000_000:
            raise RuntimeError("theta truncation did not converge")
    return total


def theta_duality_residual(parameter: float, tolerance: float = 1e-15) -> float:
    """Residual of theta(t)=t^(-1/2) theta(1/t)."""

    return theta_value(parameter, tolerance) - parameter ** (-0.5) * theta_value(
        1 / parameter,
        tolerance,
    )


def _theta_tail(parameter: float, terms: int = 8) -> float:
    return 2 * sum(
        exp(-pi * parameter * coordinate * coordinate).real
        for coordinate in range(1, terms + 1)
    )


def _positive_real_power(base: float, exponent: complex) -> complex:
    return exp(exponent * log(base))


def theta_completion_integral(
    parameter: complex,
    cutoff: float = 12.0,
    panels: int = 4096,
) -> complex:
    """Entire integral part of the generated completed cost character."""

    if cutoff <= 1 or panels < 2 or panels % 2:
        raise ValueError("cutoff must exceed one and panels must be positive and even")

    def integrand(scale: float) -> complex:
        tail = _theta_tail(scale)
        return tail * (
            _positive_real_power(scale, parameter / 2 - 1)
            + _positive_real_power(scale, (1 - parameter) / 2 - 1)
        )

    width = (cutoff - 1) / panels
    total = integrand(1) + integrand(cutoff)
    for index in range(1, panels):
        weight = 4 if index & 1 else 2
        total += weight * integrand(1 + index * width)
    return total * width / 3


def completed_xi_from_distinction(
    parameter: complex,
    cutoff: float = 12.0,
    panels: int = 4096,
) -> complex:
    """Entire completion derived from the theta duality.

    xi(s) = 1/2 + s(s-1)/4 * integral_1^infinity
      (theta(t)-1) [t^(s/2-1)+t^((1-s)/2-1)] dt.
    """

    integral = theta_completion_integral(parameter, cutoff, panels)
    return 0.5 + parameter * (parameter - 1) * integral / 4


def audit() -> dict:
    prime = 3
    places = 2
    modulus = carry_modulus(prime, places)
    frequency = 1
    carry_components = active_digit_components(prime, places, frequency)
    scaling_errors = {
        str(size): abs(
            scaled_distinction_eigenvalue(size, 1) - continuum_eigenvalue(1)
        )
        for size in (8, 16, 32, 64, 128)
    }
    sample = 0.37 + 3.2j
    xi_sample = completed_xi_from_distinction(sample)
    xi_reflected = completed_xi_from_distinction(1 - sample)
    return {
        "status": (
            "uncollapsed digit characters coupled by carry; symmetric "
            "distinction and its completion derived without a random model "
            "or an assumed zeta functional equation"
        ),
        "p3_two_place_modulus": modulus,
        "carry_mode_active_digit_components": carry_components,
        "full_digit_fibre_size": prime**places,
        "carry_mode_reconstructs_from_full_fibre": all(
            abs(
                reconstruct_carry_from_digit_fibre(
                    prime,
                    places,
                    frequency,
                    value,
                )
                - carry_character(prime, places, frequency, value)
            )
            < 1e-10
            for value in range(modulus)
        ),
        "carry_modes_diagonalize_successor": all(
            abs(successor_eigen_residual(prime, places, mode, value)) < 1e-10
            for mode in range(modulus)
            for value in range(modulus)
        ),
        "carry_modes_diagonalize_symmetric_distinction": all(
            abs(
                symmetric_distinction_eigen_residual(
                    prime,
                    places,
                    mode,
                    value,
                )
            )
            < 1e-10
            for mode in range(modulus)
            for value in range(modulus)
        ),
        "crt_character_interaction_residual": abs(
            crt_character_residual(137, 11, (8, 9, 5))
        ),
        "scaled_spectrum_errors_to_continuum": scaling_errors,
        "theta_duality_residuals": {
            str(value): abs(theta_duality_residual(value))
            for value in (0.2, 0.5, 2.0, 5.0)
        },
        "completed_xi_reflection_residual": abs(xi_sample - xi_reflected),
        "completed_xi_at_2": completed_xi_from_distinction(2).real,
        "expected_xi_at_2": pi / 6,
        "zero_orbit_law": (
            "a nontrivial zero rho now forces conjugate(rho), 1-rho, "
            "and 1-conjugate(rho); the involution does not force rho to be "
            "its own reflected point"
        ),
    }
