"""Complete ordinary carrier of the power-of-two capacity signature."""

from __future__ import annotations


def identity_sign(value: int) -> int:
    if value < 0:
        raise ValueError("identity coordinate must be nonnegative")
    return -1 if value.bit_count() & 1 else 1


def finite_identity_coefficients(bit_count: int) -> tuple[int, ...]:
    """Coefficients of product_{j<bit_count}(1-z^(2^j))."""

    if bit_count < 0:
        raise ValueError("bit_count must be nonnegative")
    coefficients = [1]
    for bit in range(bit_count):
        shift = 1 << bit
        updated = coefficients + [0] * shift
        for index, coefficient in enumerate(coefficients):
            updated[index + shift] -= coefficient
        coefficients = updated
    return tuple(coefficients)


def identity_series_value(coordinate: complex, terms: int) -> complex:
    if terms < 1:
        raise ValueError("terms must be positive")
    value = 0j
    power = 1 + 0j
    for index in range(terms):
        value += identity_sign(index) * power
        power *= coordinate
    return value


def identity_product_value(coordinate: complex, factors: int) -> complex:
    if factors < 0:
        raise ValueError("factors must be nonnegative")
    value = 1 + 0j
    for bit in range(factors):
        value *= 1 - coordinate ** (1 << bit)
    return value


def audit(max_bits: int) -> dict:
    if max_bits < 1:
        raise ValueError("max_bits must be positive")
    return {
        "status": (
            "ordinary P1 carrier of the complete power-of-two capacity "
            "signature; one identity seed retained explicitly"
        ),
        "max_bits_audited": max_bits,
        "all_finite_products_match_identity_signs": all(
            finite_identity_coefficients(bits)
            == tuple(identity_sign(value) for value in range(1 << bits))
            for bits in range(max_bits + 1)
        ),
        "binary_self_similarity_verified": all(
            identity_sign(2 * value) == identity_sign(value)
            and identity_sign(2 * value + 1) == -identity_sign(value)
            for value in range(1 << max_bits)
        ),
        "generated_product": "T(z)=product_{j>=0}(1-z^(2^j))",
        "generated_recursion": "T(z)=(1-z)T(z^2)",
        "analytic_law": (
            "T is holomorphic and nonzero for |z|<1; the unit circle is a "
            "natural boundary because radial zeros occur at every dyadic root"
        ),
    }
