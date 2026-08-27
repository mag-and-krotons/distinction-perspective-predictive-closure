from __future__ import annotations

from math import log, pi
import unittest

from cross_boundary_completion import (
    binary_hasse_eta,
    character_orthogonality_sum,
    character_sum_digit_trace,
    complete_character_indices,
    complete_digit_trace,
    continued_zeta,
    cross_prime_residual,
    diagonal_character_indices,
    negative_integer_hasse_exact,
    presentation_zero,
    prime_boundary_numerator,
    prime_trace_dirichlet_partial,
)


class CrossBoundaryCompletionTests(unittest.TestCase):
    def test_full_character_fibre_repairs_diagonal_omission(self) -> None:
        self.assertEqual(len(complete_character_indices(3, 2)), 9)
        self.assertEqual(len(diagonal_character_indices(3, 2)), 3)
        self.assertEqual(len(complete_character_indices(5, 3)), 125)
        self.assertEqual(len(diagonal_character_indices(5, 3)), 5)

    def test_complete_fibre_is_exactly_orthogonal(self) -> None:
        for left in range(9):
            for right in range(9):
                expected = 9 if left == right else 0
                self.assertAlmostEqual(
                    character_orthogonality_sum(left, right, 3, 2).real,
                    expected,
                    places=10,
                )
                self.assertAlmostEqual(
                    character_orthogonality_sum(left, right, 3, 2).imag,
                    0,
                    places=10,
                )

    def test_complete_character_sum_forces_integer_digit_trace(self) -> None:
        for prime in (2, 3, 5, 7):
            for place in range(3):
                for value in range(prime**3):
                    self.assertAlmostEqual(
                        character_sum_digit_trace(value, prime, place).real,
                        complete_digit_trace(value, prime, place),
                        places=10,
                    )
                    self.assertAlmostEqual(
                        character_sum_digit_trace(value, prime, place).imag,
                        0,
                        places=10,
                    )

    def test_binary_complete_difference_continues_special_values(self) -> None:
        self.assertAlmostEqual(binary_hasse_eta(0).real, 0.5, places=13)
        self.assertAlmostEqual(continued_zeta(0).real, -0.5, places=13)
        self.assertAlmostEqual(continued_zeta(-1).real, -1 / 12, places=12)
        self.assertAlmostEqual(continued_zeta(2).real, pi * pi / 6, places=12)

    def test_binary_complement_forces_all_negative_even_zeros(self) -> None:
        for order in range(1, 20):
            self.assertEqual(negative_integer_hasse_exact(2 * order), 0)

    def test_prime_trace_matches_direct_series_in_initial_region(self) -> None:
        for prime in (3, 5):
            direct = prime_trace_dirichlet_partial(prime, 3, 10000)
            completed = prime_boundary_numerator(prime, 3)
            self.assertAlmostEqual(direct.real, completed.real, places=10)
            self.assertAlmostEqual(direct.imag, completed.imag, places=10)

    def test_cross_prime_interaction_identity_is_exact(self) -> None:
        for parameter in (2.3, 0.37 + 4.2j, -1.4 + 0.7j):
            self.assertLess(abs(cross_prime_residual(3, 5, parameter)), 1e-11)

    def test_each_prime_trace_has_its_forced_presentation_zeros(self) -> None:
        for prime, tolerance in ((2, 1e-12), (3, 1e-12), (5, 1e-12)):
            for index in (-2, -1, 1, 2):
                coordinate = presentation_zero(prime, index)
                self.assertAlmostEqual(coordinate.real, 1)
                self.assertAlmostEqual(
                    abs(coordinate.imag),
                    2 * pi * abs(index) / log(prime),
                )
                self.assertLess(
                    abs(prime_boundary_numerator(prime, coordinate)),
                    tolerance,
                )


if __name__ == "__main__":
    unittest.main()
