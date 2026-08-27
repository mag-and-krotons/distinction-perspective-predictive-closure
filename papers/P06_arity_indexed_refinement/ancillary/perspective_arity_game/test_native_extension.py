from __future__ import annotations

from collections import Counter
import unittest

from native_extension import (
    connected_class_counts,
    euler_transform,
    evaluate,
    incidence_components,
    interval_characteristic,
    native_extension_data,
    native_two_event_support_polynomial,
    raw_two_event_polynomial,
)


class NativeExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = native_extension_data(4, 4)

    def test_native_class_counts(self) -> None:
        self.assertEqual(
            [len(self.data.representatives[level]) for level in range(1, 5)],
            [1, 5, 30, 332],
        )

    def test_two_event_accountings_are_distinct(self) -> None:
        self.assertEqual(
            raw_two_event_polynomial(4),
            (0, 0, 0, 0, 1, 4, 6, 4, 1),
        )
        self.assertEqual(
            native_two_event_support_polynomial(4),
            (0, 0, 0, 0, 1, 1, 1, 1, 1),
        )

    def test_mobius_residue_histograms(self) -> None:
        expected = {
            1: {1: 1},
            2: {-1: 5},
            3: {0: 9, 1: 18, 2: 3},
            4: {-4: 1, -3: 43, -2: 38, -1: 141, 0: 109},
        }
        for level, histogram in expected.items():
            self.assertEqual(
                Counter(
                    self.data.mobius_from_initial[key]
                    for key in self.data.representatives[level]
                ),
                Counter(histogram),
            )

    def test_every_noninitial_characteristic_vanishes_at_one(self) -> None:
        for level in range(2, 5):
            for key in self.data.representatives[level]:
                self.assertEqual(
                    evaluate(interval_characteristic(self.data, key), 1),
                    0,
                )

    def test_three_event_characteristic_types(self) -> None:
        observed = Counter(
            interval_characteristic(self.data, key)
            for key in self.data.representatives[3]
        )
        self.assertEqual(
            observed,
            Counter({(0, -1, 1): 9, (1, -2, 1): 18, (2, -3, 1): 3}),
        )

    def test_binary_rank_character_histograms(self) -> None:
        expected = {
            2: {1: 5},
            3: {0: 3, 1: 18, 2: 9},
            4: {-1: 21, 0: 30, 1: 104, 2: 101, 3: 58, 4: 17, 5: 1},
        }
        for level, histogram in expected.items():
            self.assertEqual(
                Counter(
                    evaluate(interval_characteristic(self.data, key), 2)
                    for key in self.data.representatives[level]
                ),
                Counter(histogram),
            )

    def test_unique_component_factorization_counts(self) -> None:
        connected = connected_class_counts(self.data)
        self.assertEqual(connected, (1, 4, 25, 292))
        self.assertEqual(euler_transform(connected), (1, 1, 5, 30, 332))
        for level in range(1, 5):
            for history in self.data.representatives[level].values():
                components = incidence_components(history)
                self.assertEqual(
                    sorted(index for component in components for index in component),
                    list(range(level)),
                )

    def test_interval_polynomial_is_not_component_multiplicative(self) -> None:
        # Two disjoint atomic occurrences have X_H=t-1.  Each isolated
        # component is the initial form with polynomial 1, whose product is 1.
        disjoint_key = next(
            key
            for key, history in self.data.representatives[2].items()
            if not set(history[0]).intersection(history[1])
        )
        self.assertEqual(interval_characteristic(self.data, disjoint_key), (-1, 1))
        self.assertNotEqual(interval_characteristic(self.data, disjoint_key), (1,))


if __name__ == "__main__":
    unittest.main()
