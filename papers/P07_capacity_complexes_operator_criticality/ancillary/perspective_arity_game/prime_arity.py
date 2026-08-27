"""Prime arities as transparent distinction-capacity coordinates."""

from __future__ import annotations

from functools import lru_cache
from math import comb


@lru_cache(maxsize=None)
def is_transparent_arity(arity: int) -> bool:
    """Whether all intermediate q-capacities vanish modulo q."""

    if arity < 2:
        return False
    return all(comb(arity, choice) % arity == 0 for choice in range(1, arity))


@lru_cache(maxsize=None)
def trial_is_prime(value: int) -> bool:
    """Independent finite audit predicate, not used in the definition."""

    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def prime_capacity_digits(value: int, prime_arity: int) -> tuple[int, ...]:
    """Base-p digits as binomial-capacity residues at p^j."""

    if value < 0:
        raise ValueError("value must be nonnegative")
    if not is_transparent_arity(prime_arity):
        raise ValueError("capacity-digit law requires a transparent arity")
    if value == 0:
        return (0,)
    digits = []
    place = 1
    while place <= value:
        digits.append(comb(value, place) % prime_arity)
        place *= prime_arity
    return tuple(digits)


def reconstruct_prime_capacity_digits(
    digits: tuple[int, ...],
    prime_arity: int,
) -> int:
    if not is_transparent_arity(prime_arity):
        raise ValueError("capacity-digit law requires a transparent arity")
    if any(digit < 0 or digit >= prime_arity for digit in digits):
        raise ValueError("digit outside the prime-arity range")
    value = 0
    place = 1
    for digit in digits:
        value += digit * place
        place *= prime_arity
    return value


def finite_digit_character_coefficients(
    prime_arity: int,
    character_index: int,
    places: int,
) -> tuple[complex, ...]:
    """Finite product over all retained base-p digit alternatives."""

    if not is_transparent_arity(prime_arity):
        raise ValueError("character requires a transparent arity")
    if not 0 <= character_index < prime_arity or places < 0:
        raise ValueError("invalid character index or place count")
    from cmath import exp, pi

    root = exp(2j * pi * character_index / prime_arity)
    coefficients = [1 + 0j]
    place = 1
    for _ in range(places):
        updated = [0j] * (len(coefficients) + (prime_arity - 1) * place)
        for index, coefficient in enumerate(coefficients):
            for digit in range(prime_arity):
                updated[index + digit * place] += coefficient * root**digit
        coefficients = updated
        place *= prime_arity
    return tuple(coefficients)


def audit(max_arity: int, sample_limit: int) -> dict:
    if max_arity < 2 or sample_limit < 1:
        raise ValueError("max_arity and sample_limit are too small")
    transparent = tuple(
        arity for arity in range(2, max_arity + 1) if is_transparent_arity(arity)
    )
    return {
        "status": (
            "P1 audit of arities whose intermediate binomial capacities "
            "vanish in their own residue system"
        ),
        "transparent_arities": transparent,
        "transparent_arities_equal_primes": all(
            is_transparent_arity(arity) == trial_is_prime(arity)
            for arity in range(2, max_arity + 1)
        ),
        "all_prime_capacity_signatures_reconstruct_samples": all(
            reconstruct_prime_capacity_digits(
                prime_capacity_digits(value, prime),
                prime,
            )
            == value
            for prime in transparent
            for value in range(sample_limit)
        ),
        "generated_theorem": (
            "q is prime iff binomial(q,k)=0 mod q for every 0<k<q; "
            "then binomial(n,q^j) mod q is the j-th base-q digit of n"
        ),
    }
