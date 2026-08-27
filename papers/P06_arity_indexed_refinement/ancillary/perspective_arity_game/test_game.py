from __future__ import annotations

import unittest

from primitive import (
    all_binary_presentations,
    binary_fiber,
    binary_tree_shape,
    complete_binary_tree_orbits,
    complete_binary_trees_of_four,
    exact_layers,
    isolated_binary_tree_automorphisms,
    isolated_native_automorphisms,
    native_classes,
    native_key,
)


class PerspectiveArityGameTests(unittest.TestCase):
    def test_expected_raw_layers(self) -> None:
        self.assertEqual([len(x) for x in exact_layers(2, 4).values()], [1, 4, 29, 321])
        self.assertEqual([len(x) for x in exact_layers(4, 3).values()], [1, 16, 1041])

    def test_expected_native_classes(self) -> None:
        p1 = exact_layers(2, 4)
        self.assertEqual(
            [len(native_classes(layer, 2)) for layer in p1.values()],
            [1, 3, 8, 23],
        )
        p4 = exact_layers(4, 3)
        self.assertEqual(
            [len(native_classes(layer, 4)) for layer in p4.values()],
            [1, 5, 30],
        )

    def test_resultant_and_event_relabelling_do_not_change_native_key(self) -> None:
        history = ((0, 1, 2, 3), (2, 3, 4, 5))
        relabelled_and_reordered = ((14, 15, 12, 13), (10, 11, 12, 13))
        self.assertEqual(native_key(history, 4), native_key(relabelled_and_reordered, 4))

    def test_all_three_binary_presentations_are_retained(self) -> None:
        history = ((0, 1, 2, 3),)
        self.assertEqual(len(tuple(all_binary_presentations(history))), 3)
        self.assertEqual(sum(map(len, binary_fiber(history).values())), 3)

    def test_all_complete_binary_trees_are_retained(self) -> None:
        trees = complete_binary_trees_of_four((0, 1, 2, 3))
        self.assertEqual(len(trees), 15)
        self.assertEqual(
            {shape: sum(binary_tree_shape(tree) == shape for tree in trees) for shape in ("balanced", "unbalanced")},
            {"balanced": 3, "unbalanced": 12},
        )

    def test_one_isolated_event_has_two_P1_shapes_and_less_symmetry(self) -> None:
        history = ((0, 1, 2, 3),)
        self.assertEqual(len(binary_fiber(history)), 1)
        representatives, orbit_sizes = complete_binary_tree_orbits(history)
        self.assertEqual(len(representatives), 2)
        self.assertEqual(sorted(orbit_sizes), [3, 12])
        self.assertEqual(sum(orbit_sizes), 15)
        self.assertEqual(isolated_native_automorphisms(4), 24)
        self.assertEqual(isolated_binary_tree_automorphisms(), 8)

    def test_no_binary_presentation_is_removed_from_any_native_class(self) -> None:
        for event_count, layer in exact_layers(4, 3).items():
            for histories in native_classes(layer, 4).values():
                fiber = binary_fiber(histories[0])
                self.assertEqual(
                    sum(len(presentations) for presentations in fiber.values()),
                    3**event_count,
                )
                _, orbit_sizes = complete_binary_tree_orbits(histories[0])
                self.assertEqual(sum(orbit_sizes), 15**event_count)

    def test_complete_two_event_shadow_counts_by_overlap(self) -> None:
        observed = {}
        for histories in native_classes(exact_layers(4, 2)[2], 4).values():
            history = histories[0]
            overlap = len(set(history[0]) & set(history[1]))
            representatives, _ = complete_binary_tree_orbits(history)
            observed[overlap] = len(representatives)
        self.assertEqual(observed, {0: 3, 1: 10, 2: 27, 3: 26, 4: 10})


if __name__ == "__main__":
    unittest.main()
