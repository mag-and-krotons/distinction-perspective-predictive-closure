from __future__ import annotations

import unittest

from interaction_closure import (
    history_count,
    interaction_polynomial,
    interaction_step,
    is_strictly_hurwitz,
    nonzero_core_descending,
    normalized_kernel_descending,
    third_hurwitz_determinant_of_kernel,
)
from primitive import exact_layers


class InteractionClosureTests(unittest.TestCase):
    def test_first_P4_polynomials_are_exact(self) -> None:
        self.assertEqual(interaction_polynomial(4, 1), (0, 0, 0, 0, 1))
        self.assertEqual(
            interaction_polynomial(4, 2),
            (0, 0, 0, 0, 1, 4, 6, 4, 1),
        )
        self.assertEqual(
            interaction_polynomial(4, 3),
            (0, 0, 0, 0, 1, 24, 136, 304, 321, 180, 62, 12, 1),
        )

    def test_operator_equals_direct_sharing_count(self) -> None:
        source = (3, 0, 2, 5, 0, 7)
        expected = [0] * 10
        for n, count in enumerate(source):
            if not count:
                continue
            from math import comb

            for shared in range(min(4, n) + 1):
                expected[n + 4 - shared] += count * comb(n, shared)
        while len(expected) > 1 and expected[-1] == 0:
            expected.pop()
        self.assertEqual(interaction_step(source, 4), tuple(expected))

    def test_polynomial_counts_match_exhaustive_generator(self) -> None:
        layers = exact_layers(4, 3)
        for events in range(1, 4):
            self.assertEqual(history_count(4, events), len(layers[events]))

    def test_P4_history_sequence(self) -> None:
        self.assertEqual(
            [history_count(4, events) for events in range(1, 7)],
            [1, 16, 1041, 168481, 54344712, 30663168463],
        )

    def test_kernel_has_sharp_arity_four_stability_boundary(self) -> None:
        self.assertEqual(
            [is_strictly_hurwitz(normalized_kernel_descending(q)) for q in range(1, 9)],
            [True, True, True, True, False, False, False, False],
        )

    def test_third_determinant_changes_sign_after_four(self) -> None:
        self.assertGreater(third_hurwitz_determinant_of_kernel(4), 0)
        for arity in range(5, 20):
            self.assertLess(third_hurwitz_determinant_of_kernel(arity), 0)

    def test_generated_P4_layers_are_stable(self) -> None:
        for events in range(1, 21):
            core = nonzero_core_descending(interaction_polynomial(4, events))
            if len(core) > 1:
                self.assertTrue(is_strictly_hurwitz(core))


if __name__ == "__main__":
    unittest.main()
