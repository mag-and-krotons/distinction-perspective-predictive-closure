from __future__ import annotations

from math import pi
import unittest

from uncollapsed_fibre_duality import (
    active_digit_components,
    carry_character,
    carry_modulus,
    completed_xi_from_distinction,
    continuum_eigenvalue,
    crt_character_residual,
    crt_combine,
    global_to_local_frequencies,
    reconstruct_carry_from_digit_fibre,
    scaled_distinction_eigenvalue,
    successor_eigen_residual,
    symmetric_distinction_eigen_residual,
    theta_duality_residual,
)


class UncollapsedFibreDualityTests(unittest.TestCase):
    def test_carry_interaction_mixes_independent_digit_characters(self) -> None:
        self.assertEqual(carry_modulus(3, 2), 9)
        self.assertGreater(active_digit_components(3, 2, 1), 1)
        self.assertEqual(active_digit_components(3, 2, 3), 1)

    def test_full_digit_fibre_reconstructs_every_carry_character(self) -> None:
        for prime, places in ((2, 3), (3, 2)):
            modulus = carry_modulus(prime, places)
            for frequency in range(modulus):
                for value in range(modulus):
                    self.assertAlmostEqual(
                        reconstruct_carry_from_digit_fibre(
                            prime,
                            places,
                            frequency,
                            value,
                        ).real,
                        carry_character(prime, places, frequency, value).real,
                        places=10,
                    )
                    self.assertAlmostEqual(
                        reconstruct_carry_from_digit_fibre(
                            prime,
                            places,
                            frequency,
                            value,
                        ).imag,
                        carry_character(prime, places, frequency, value).imag,
                        places=10,
                    )

    def test_carry_characters_diagonalize_unit_advance(self) -> None:
        for prime, places in ((2, 3), (3, 2)):
            modulus = carry_modulus(prime, places)
            for frequency in range(modulus):
                for value in range(modulus):
                    self.assertLess(
                        abs(
                            successor_eigen_residual(
                                prime,
                                places,
                                frequency,
                                value,
                            )
                        ),
                        1e-10,
                    )

    def test_symmetric_distinction_has_forced_sine_spectrum(self) -> None:
        for prime, places in ((2, 3), (3, 2)):
            modulus = carry_modulus(prime, places)
            for frequency in range(modulus):
                for value in range(modulus):
                    self.assertLess(
                        abs(
                            symmetric_distinction_eigen_residual(
                                prime,
                                places,
                                frequency,
                                value,
                            )
                        ),
                        1e-10,
                    )

    def test_quadratic_scaling_is_the_nontrivial_continuum_limit(self) -> None:
        errors = []
        for modulus in (8, 16, 32, 64, 128, 256):
            errors.append(
                abs(
                    scaled_distinction_eigenvalue(modulus, 1)
                    - continuum_eigenvalue(1)
                )
            )
        self.assertTrue(all(right < left for left, right in zip(errors, errors[1:])))
        self.assertLess(errors[-1], 0.003)

    def test_crt_interaction_factors_global_characters(self) -> None:
        moduli = (8, 9, 5)
        modulus = 8 * 9 * 5
        for value in (0, 1, 7, 137, modulus - 1):
            residues = tuple(value % part for part in moduli)
            self.assertEqual(crt_combine(residues, moduli), value % modulus)
        for frequency in (0, 1, 11, 127):
            self.assertEqual(len(global_to_local_frequencies(frequency, moduli)), 3)
            for value in (0, 1, 7, 137, modulus - 1):
                self.assertLess(
                    abs(crt_character_residual(value, frequency, moduli)),
                    1e-10,
                )

    def test_complete_gaussian_carrier_has_derived_duality(self) -> None:
        for parameter in (0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0):
            self.assertLess(abs(theta_duality_residual(parameter)), 1e-12)

    def test_generated_completion_has_reflection_and_correct_normalization(self) -> None:
        for parameter in (2, -1, 0.37 + 3.2j, 0.8 - 1.7j):
            self.assertLess(
                abs(
                    completed_xi_from_distinction(parameter)
                    - completed_xi_from_distinction(1 - parameter)
                ),
                1e-11,
            )
        self.assertAlmostEqual(
            completed_xi_from_distinction(2).real,
            pi / 6,
            places=10,
        )
        self.assertAlmostEqual(completed_xi_from_distinction(0).real, 0.5, places=12)
        self.assertAlmostEqual(completed_xi_from_distinction(1).real, 0.5, places=12)


if __name__ == "__main__":
    unittest.main()
