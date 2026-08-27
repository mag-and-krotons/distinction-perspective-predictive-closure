from __future__ import annotations

import unittest

from binary_identity_carrier import (
    finite_identity_coefficients,
    identity_product_value,
    identity_series_value,
    identity_sign,
)


class BinaryIdentityCarrierTests(unittest.TestCase):
    def test_finite_products_generate_all_identity_signs(self) -> None:
        for bits in range(15):
            self.assertEqual(
                finite_identity_coefficients(bits),
                tuple(identity_sign(value) for value in range(1 << bits)),
            )

    def test_binary_self_similarity(self) -> None:
        for value in range(10000):
            self.assertEqual(identity_sign(2 * value), identity_sign(value))
            self.assertEqual(identity_sign(2 * value + 1), -identity_sign(value))

    def test_product_matches_series_inside_unit_disk(self) -> None:
        for coordinate in (-0.7, 0.2 + 0.4j, 0.8j):
            self.assertAlmostEqual(
                abs(
                    identity_product_value(coordinate, 14)
                    - identity_series_value(coordinate, 1 << 14)
                ),
                0.0,
                places=10,
            )

    def test_finite_functional_equation(self) -> None:
        for coordinate in (-0.6, 0.3 + 0.5j, 0.7j):
            left = identity_product_value(coordinate, 12)
            right = (1 - coordinate) * identity_product_value(
                coordinate * coordinate,
                11,
            )
            self.assertAlmostEqual(abs(left - right), 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
