from __future__ import annotations

import unittest

from binary_capacity_character import (
    binary_capacity_closed,
    binary_capacity_egf,
    binary_capacity_sign,
    binary_no_unused_carrier,
    capacity_digits,
    reconstruct_from_capacity_digits,
)


class BinaryCapacityCharacterTests(unittest.TestCase):
    def test_capacity_parities_are_exact_binary_digits(self) -> None:
        for value in range(4096):
            digits = capacity_digits(value)
            self.assertEqual(reconstruct_from_capacity_digits(digits), value)
            for bit, digit in enumerate(digits):
                self.assertEqual(digit, (value >> bit) & 1)

    def test_power_of_two_signs_are_antiperiodic(self) -> None:
        for arity in (1, 2, 4, 8, 16, 32):
            for value in range(500):
                self.assertEqual(
                    binary_capacity_sign(value + arity, arity),
                    -binary_capacity_sign(value, arity),
                )

    def test_generated_differential_recurrence(self) -> None:
        # Coefficients of F_q^(q)+F_q vanish exactly.
        for arity in (1, 2, 4, 8, 16):
            for value in range(500):
                self.assertEqual(
                    binary_capacity_sign(value + arity, arity)
                    + binary_capacity_sign(value, arity),
                    0,
                )

    def test_finite_exponential_form_matches_generated_series(self) -> None:
        for arity in (1, 2, 4, 8):
            for coordinate in (-1.2, 0.3 + 0.7j, 1.1 - 0.2j):
                self.assertAlmostEqual(
                    abs(
                        binary_capacity_closed(arity, coordinate)
                        - binary_capacity_egf(arity, coordinate, 100)
                    ),
                    0.0,
                    places=11,
                )

    def test_arity_two_has_explicit_real_zero_law(self) -> None:
        from cmath import cos, pi, sin

        for coordinate in (-2.0, 0.2 + 0.4j, 1.7):
            self.assertAlmostEqual(
                abs(
                    binary_capacity_closed(2, coordinate)
                    - (cos(coordinate) + sin(coordinate))
                ),
                0.0,
                places=12,
            )
        for index in range(-8, 9):
            zero = -pi / 4 + index * pi
            self.assertAlmostEqual(
                abs(binary_capacity_closed(2, zero)),
                0.0,
                places=11,
            )


if __name__ == "__main__":
    unittest.main()
