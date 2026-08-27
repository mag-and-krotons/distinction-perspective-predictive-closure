from __future__ import annotations

from math import log2
import unittest

from arithmetic_emergence import (
    binary_distinction_cost,
    generated_mobius,
    reconstruct_factorization,
    transparent_factorization,
)


class ArithmeticEmergenceTests(unittest.TestCase):
    def test_every_identity_has_exact_transparent_factorization(self) -> None:
        for value in range(1, 10000):
            factors = transparent_factorization(value)
            self.assertEqual(reconstruct_factorization(factors), value)
            self.assertEqual(tuple(sorted(factors)), factors)

    def test_distinction_cost_is_exact_logarithmic_cost(self) -> None:
        for value in range(1, 10000):
            self.assertAlmostEqual(
                binary_distinction_cost(value),
                log2(value),
                places=12,
            )

    def test_generated_mobius_sequence(self) -> None:
        expected = (
            1,
            -1,
            -1,
            0,
            -1,
            1,
            -1,
            0,
            0,
            1,
            -1,
            0,
            -1,
            1,
            1,
            0,
            -1,
            0,
            -1,
            0,
        )
        self.assertEqual(
            tuple(generated_mobius(value) for value in range(1, 21)),
            expected,
        )

    def test_budget_is_exactly_identity_bound(self) -> None:
        for capacity in (2, 3, 10, 100, 997):
            budget = log2(capacity)
            self.assertEqual(
                [
                    value
                    for value in range(1, capacity + 10)
                    if binary_distinction_cost(value) <= budget + 1e-12
                ],
                list(range(1, capacity + 1)),
            )


if __name__ == "__main__":
    unittest.main()
