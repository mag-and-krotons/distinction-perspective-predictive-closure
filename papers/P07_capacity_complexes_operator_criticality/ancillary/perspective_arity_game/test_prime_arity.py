from __future__ import annotations

import unittest

from prime_arity import (
    finite_digit_character_coefficients,
    is_transparent_arity,
    prime_capacity_digits,
    reconstruct_prime_capacity_digits,
    trial_is_prime,
)


class PrimeArityTests(unittest.TestCase):
    def test_transparent_arities_are_exactly_primes(self) -> None:
        for arity in range(2, 500):
            self.assertEqual(is_transparent_arity(arity), trial_is_prime(arity))

    def test_capacity_residues_are_base_prime_digits(self) -> None:
        for prime in (2, 3, 5, 7, 11, 13):
            for value in range(2000):
                digits = prime_capacity_digits(value, prime)
                self.assertEqual(
                    reconstruct_prime_capacity_digits(digits, prime),
                    value,
                )
                expected = []
                remainder = value
                while remainder:
                    expected.append(remainder % prime)
                    remainder //= prime
                self.assertEqual(digits, tuple(expected or (0,)))

    def test_composite_arity_is_rejected_by_digit_law(self) -> None:
        for arity in (4, 6, 8, 9, 10, 12, 15, 21, 25):
            self.assertFalse(is_transparent_arity(arity))
            with self.assertRaises(ValueError):
                prime_capacity_digits(100, arity)

    def test_finite_character_product_matches_digit_sum(self) -> None:
        from cmath import exp, pi

        for prime in (2, 3, 5, 7):
            for character_index in range(prime):
                root = exp(2j * pi * character_index / prime)
                coefficients = finite_digit_character_coefficients(
                    prime,
                    character_index,
                    4,
                )
                for value, coefficient in enumerate(coefficients):
                    digit_sum = sum(prime_capacity_digits(value, prime))
                    self.assertAlmostEqual(
                        abs(coefficient - root**digit_sum),
                        0.0,
                        places=10,
                    )


if __name__ == "__main__":
    unittest.main()
