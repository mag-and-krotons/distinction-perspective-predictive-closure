from __future__ import annotations

import unittest

from capacity_character import (
    absolute_character_sum,
    binary_complete_length_profile,
    canonical_binary_words,
    finite_component_product,
    finite_completed_product,
    finite_log_curvature,
    finite_log_via_length_enumerator,
    is_prefix_free,
    kraft_sum,
    ranked_connected_code,
    reciprocal_zero,
    normalized_reciprocal_zero,
    capacity_strip_coordinate,
    unit_strip_coordinate,
)


class CapacityCharacterTests(unittest.TestCase):
    def test_complete_binary_profiles(self) -> None:
        for count in range(1, 1000):
            lengths = binary_complete_length_profile(count)
            self.assertEqual(len(lengths), count)
            self.assertEqual(kraft_sum(lengths), 1)
            self.assertTrue(is_prefix_free(canonical_binary_words(lengths)))

    def test_distinct_codes_have_same_capacity_but_different_products(self) -> None:
        balanced = (2, 2, 2, 2)
        unbalanced = (1, 2, 3, 3)
        self.assertEqual(kraft_sum(balanced), 1)
        self.assertEqual(kraft_sum(unbalanced), 1)
        self.assertNotEqual(
            finite_component_product(balanced, 2),
            finite_component_product(unbalanced, 2),
        )

    def test_ranked_connected_audit_code(self) -> None:
        code = ranked_connected_code((1, 4, 25, 292))
        words = tuple(word for _, _, word in code)
        self.assertEqual(len(words), 322)
        self.assertTrue(is_prefix_free(words))
        # The first four rank prefixes use only a finite part of the infinite
        # unary rank code, so future ranks retain the remaining capacity.
        self.assertEqual(kraft_sum(map(len, words)), 15 / 16)

    def test_capacity_bound_is_base_independent(self) -> None:
        binary_lengths = (1, 2, 3, 3)
        ternary_lengths = (1, 1, 1)
        self.assertEqual(kraft_sum(binary_lengths, 2), 1)
        self.assertEqual(kraft_sum(ternary_lengths, 3), 1)
        for sigma in (1.0, 1.25, 2.0, 5.0):
            self.assertLessEqual(
                absolute_character_sum(binary_lengths, sigma, 2),
                1.0,
            )
            self.assertLessEqual(
                absolute_character_sum(ternary_lengths, sigma, 3),
                1.0,
            )

    def test_finite_completed_involution(self) -> None:
        for lengths in ((2, 2, 2, 2), (1, 2, 3, 3), (1, 3, 3)):
            for base in (2, 3, 5):
                for parameter in (0.7 + 0.2j, 1.4 - 0.3j, 2.1 + 1.1j):
                    left = finite_completed_product(lengths, -parameter, base)
                    right = (-1) ** len(lengths) * finite_completed_product(
                        lengths,
                        parameter,
                        base,
                    )
                    self.assertAlmostEqual(abs(left - right), 0.0, places=10)

    def test_finite_reciprocal_zeros_lie_on_invariant_axis(self) -> None:
        import cmath

        for base in (2, 3, 4, 7):
            for length in range(1, 12):
                for index in range(-5, 6):
                    zero = reciprocal_zero(length, index, base)
                    self.assertAlmostEqual(zero.real, 0.0, places=14)
                    self.assertAlmostEqual(
                        abs(1 - cmath.exp(-zero * length * cmath.log(base))),
                        0.0,
                        places=11,
                    )

    def test_log_curvature_removes_affine_cocycle(self) -> None:
        for lengths in ((2, 2, 2, 2), (1, 2, 3, 3), (1, 3, 3, 5, 8)):
            for base in (2, 3, 7):
                for parameter in (0.4 + 0.7j, 1.3 - 0.2j, 2.2 + 1.4j):
                    self.assertAlmostEqual(
                        abs(
                            finite_log_curvature(lengths, -parameter, base)
                            - finite_log_curvature(lengths, parameter, base)
                        ),
                        0.0,
                        places=11,
                    )

    def test_capacity_strip_normalization(self) -> None:
        self.assertEqual(unit_strip_coordinate(-1), 0)
        self.assertEqual(unit_strip_coordinate(1), 1)
        self.assertEqual(unit_strip_coordinate(0), 0.5)
        for value in (-3 + 2j, -1, 0, 1, 4 - 7j):
            self.assertAlmostEqual(
                abs(capacity_strip_coordinate(unit_strip_coordinate(value)) - value),
                0.0,
                places=14,
            )
        for base in (2, 3, 5):
            for length in range(1, 10):
                for index in range(-4, 5):
                    zero = normalized_reciprocal_zero(length, index, base)
                    self.assertAlmostEqual(zero.real, 0.5, places=14)
                    self.assertAlmostEqual(
                        abs(
                            capacity_strip_coordinate(1 - zero)
                            + capacity_strip_coordinate(zero)
                        ),
                        0.0,
                        places=13,
                    )

    def test_length_enumerator_reconstructs_product_log(self) -> None:
        import cmath

        for lengths in ((2, 2, 2, 2), (1, 2, 3, 3), (1, 3, 3, 5, 8)):
            for base in (2, 3):
                parameter = 1.7
                direct = cmath.log(finite_component_product(lengths, parameter, base))
                expanded = finite_log_via_length_enumerator(
                    lengths,
                    parameter,
                    terms=200,
                    base=base,
                )
                self.assertAlmostEqual(abs(direct - expanded), 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
