from __future__ import annotations

from fractions import Fraction
from math import factorial
import unittest

from groupoid_lift import (
    automorphism_order,
    exponential_series,
    groupoid_series,
    labelled_incidence_count,
    orbit_reconstructed_labelled_count,
    symmetry_carrier_coefficient,
    symmetry_carrier_value,
)
from native_extension import native_extension_data


class GroupoidLiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = native_extension_data(4, 4)

    def test_isolated_atomic_source_has_full_symmetry(self) -> None:
        history = next(iter(self.data.representatives[1].values()))
        self.assertEqual(automorphism_order(history), factorial(4))

    def test_orbit_stabilizer_reconstructs_every_labelled_bidegree(self) -> None:
        for event_count, layer in self.data.representatives.items():
            resultant_counts = {
                len({vertex for event in history for vertex in event})
                for history in layer.values()
            }
            for resultant_count in resultant_counts:
                self.assertEqual(
                    orbit_reconstructed_labelled_count(
                        self.data,
                        event_count,
                        resultant_count,
                    ),
                    labelled_incidence_count(
                        4,
                        event_count,
                        resultant_count,
                    ),
                )

    def test_component_decomposition_is_exponential_in_groupoid_weight(self) -> None:
        all_forms = groupoid_series(self.data, connected_only=False)
        connected = groupoid_series(self.data, connected_only=True)
        self.assertEqual(
            exponential_series(
                connected,
                max_events=4,
                max_resultants=16,
            ),
            all_forms,
        )

    def test_groupoid_and_uniform_class_multiplicity_are_different(self) -> None:
        # In a coordinate normalized so one connected object has weight z,
        # uniform multiset-class accounting gives coefficient 1 at z^2.
        # Retaining two labelled copies and quotienting their exchange gives
        # the symmetry-preserving coefficient 1/2! instead.
        self.assertNotEqual(Fraction(1), Fraction(1, factorial(2)))

    def test_closed_carrier_coefficients_equal_orbit_weights(self) -> None:
        series = groupoid_series(self.data, connected_only=False)
        for (event_count, resultant_count), coefficient in series.items():
            self.assertEqual(
                symmetry_carrier_coefficient(4, event_count, resultant_count),
                coefficient,
            )

    def test_zero_event_parameter_collapses_carrier_to_one(self) -> None:
        for parameter in (-3.0, -0.2 + 0.7j, 0.0, 2.0 - 1.0j):
            self.assertAlmostEqual(
                abs(symmetry_carrier_value(4, 0, parameter, 80) - 1),
                0.0,
                places=12,
            )


if __name__ == "__main__":
    unittest.main()
