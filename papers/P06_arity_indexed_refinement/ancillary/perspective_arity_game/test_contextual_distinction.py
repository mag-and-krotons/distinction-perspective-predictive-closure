from __future__ import annotations

import unittest

from contextual_distinction import (
    ambiguity_characteristic,
    complete_context_signature,
    connected_keys,
    descendant_map,
    disjoint_context_isolates_connected_form,
    evaluate,
    fiber_size_histogram,
    fibers,
    future_separation_delay,
    strict_past_signature,
)
from native_extension import native_extension_data


class ContextualDistinctionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = native_extension_data(4, 4)
        cls.descendants = descendant_map(cls.data)

    def test_strict_past_fibers_are_exact(self) -> None:
        expected = {
            1: {1: 1},
            2: {4: 1},
            3: {1: 9, 2: 3, 3: 2, 4: 1},
            4: {1: 288, 2: 2},
        }
        for level, histogram in expected.items():
            classes = fibers(
                connected_keys(self.data, level),
                lambda key: strict_past_signature(self.data, key),
            )
            self.assertEqual(fiber_size_histogram(classes), histogram)

    def test_one_more_interaction_separates_every_rank_two_and_three_form(self) -> None:
        for level in (2, 3):
            keys = connected_keys(self.data, level)
            classes = fibers(
                keys,
                lambda key: complete_context_signature(
                    self.data,
                    key,
                    self.descendants,
                ),
            )
            self.assertEqual(fiber_size_histogram(classes), {1: len(keys)})

            past = fibers(
                keys,
                lambda key: strict_past_signature(self.data, key),
            )
            for source_fiber in past:
                for left_index, left in enumerate(source_fiber):
                    for right in source_fiber[left_index + 1 :]:
                        self.assertEqual(
                            future_separation_delay(self.data, left, right),
                            1,
                        )

    def test_horizon_four_retains_two_unresolved_pairs(self) -> None:
        keys = connected_keys(self.data, 4)
        classes = fibers(
            keys,
            lambda key: complete_context_signature(
                self.data,
                key,
                self.descendants,
            ),
        )
        self.assertEqual(fiber_size_histogram(classes), {1: 288, 2: 2})

    def test_one_disjoint_future_event_separates_every_connected_form(self) -> None:
        for level in range(2, 5):
            for history in self.data.representatives[level].values():
                from native_extension import incidence_components

                if len(incidence_components(history)) == 1:
                    self.assertTrue(
                        disjoint_context_isolates_connected_form(history, 4)
                    )

    def test_context_changes_binary_effect_without_changing_forms(self) -> None:
        past_classes = []
        context_classes = []
        for level in range(1, 5):
            keys = connected_keys(self.data, level)
            past_classes.extend(
                fibers(keys, lambda key: strict_past_signature(self.data, key))
            )
            context_classes.extend(
                fibers(
                    keys,
                    lambda key: complete_context_signature(
                        self.data,
                        key,
                        self.descendants,
                    ),
                )
            )

        self.assertEqual(
            fiber_size_histogram(tuple(past_classes)),
            {1: 298, 2: 5, 3: 2, 4: 2},
        )
        self.assertEqual(
            fiber_size_histogram(tuple(context_classes)),
            {1: 318, 2: 2},
        )
        self.assertEqual(evaluate(ambiguity_characteristic(tuple(past_classes)), 2), 0)
        self.assertEqual(evaluate(ambiguity_characteristic(tuple(context_classes)), 2), 1)


if __name__ == "__main__":
    unittest.main()
