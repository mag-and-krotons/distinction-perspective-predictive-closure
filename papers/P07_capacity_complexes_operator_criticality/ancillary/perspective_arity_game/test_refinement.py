from __future__ import annotations

from itertools import permutations
import unittest

from refinement_invariant import (
    audit,
    carrier_value,
    carrier_zero,
    characteristic_coefficients,
    expected_chain_count,
    maximal_binary_refinement_chains,
    mobius_from_indiscrete,
    partition_lattice,
    relabel_partition,
    recurrence_characteristic_coefficients,
)


class RefinementInvariantTests(unittest.TestCase):
    def test_bell_counts(self) -> None:
        self.assertEqual(
            [len(partition_lattice(q)) for q in range(2, 7)],
            [2, 5, 15, 52, 203],
        )

    def test_complete_chain_counts(self) -> None:
        for arity in range(2, 7):
            self.assertEqual(
                len(maximal_binary_refinement_chains(arity)),
                expected_chain_count(arity),
            )

    def test_top_mobius_sequence(self) -> None:
        observed = []
        for arity in range(2, 8):
            top = tuple((index,) for index in range(arity))
            observed.append(mobius_from_indiscrete(arity)[top])
        self.assertEqual(observed, [-1, 2, -6, 24, -120, 720])

    def test_characteristic_recurrence(self) -> None:
        for arity in range(2, 8):
            self.assertEqual(
                characteristic_coefficients(arity),
                recurrence_characteristic_coefficients(arity),
            )

    def test_four_resultant_characteristic_is_exact(self) -> None:
        self.assertEqual(
            characteristic_coefficients(4),
            {3: 1, 2: -7, 1: 12, 0: -6},
        )

    def test_binary_evaluation_parity_law(self) -> None:
        values = []
        for arity in range(2, 11):
            coefficients = recurrence_characteristic_coefficients(arity)
            values.append(
                sum(coefficient * 2**exponent for exponent, coefficient in coefficients.items())
            )
        self.assertEqual(values, [1, 0, -2, 0, 16, 0, -272, 0, 7936])

    def test_complete_fiber_is_invariant_under_all_P4_relabellings(self) -> None:
        lattice = set(partition_lattice(4))
        chains = set(maximal_binary_refinement_chains(4))
        for permutation in permutations(range(4)):
            self.assertEqual(
                {relabel_partition(partition, permutation) for partition in lattice},
                lattice,
            )
            self.assertEqual(
                {
                    tuple(
                        relabel_partition(partition, permutation)
                        for partition in chain
                    )
                    for chain in chains
                },
                chains,
            )

    def test_generated_zero_formula(self) -> None:
        for rank_weight in (1.5, 2.0, 4.0, 9.0):
            for index in range(-5, 6):
                zero = carrier_zero(rank_weight, index)
                self.assertAlmostEqual(
                    abs(carrier_value(rank_weight, zero)),
                    0.0,
                    places=11,
                )

    def test_every_partial_state_is_retained(self) -> None:
        for arity in range(2, 7):
            row = audit(arity)
            self.assertTrue(row["all_states_occur_in_some_history"])
            self.assertTrue(row["common_states_are_only_endpoints"])


if __name__ == "__main__":
    unittest.main()
