import json
import unittest

from seat_transfer import (
    Ask,
    FiniteGround,
    GroundValidationError,
    Leaf,
    NoSeatAvailable,
    TranslationCollision,
    _origin_ground,
    _tool_birth_grounds,
    _translated_ground,
    action_indistinguishable_pairs,
    action_is_partition_new,
    action_partition,
    answerability_gain,
    binary_answerability_count,
    conflict_transcripts_separate,
    demonstration,
    execute_all,
    execute_seat,
    fixed_view_accuracy,
    generated_partition,
    old_answerable,
    old_conflicts,
    old_partition,
    regenerative_certificate,
    replay_exposes_local_production,
    seat_depth,
    seat_is_exact,
    seat_node_count,
    synthesize_seat,
    tool_birth_certificate,
    translate_seat,
    translation_commutes,
    transported_seat_is_exact,
)


class NativeSeatTests(unittest.TestCase):
    def setUp(self):
        self.ground = _origin_ground()
        self.seat = synthesize_seat(self.ground)

    def test_old_standing_really_merges_required_answers(self):
        self.assertFalse(old_answerable(self.ground))
        self.assertEqual(len(old_conflicts(self.ground)), 6)

    def test_fixed_view_cannot_answer_delayed_case_family(self):
        accuracy = fixed_view_accuracy(
            self.ground, {"unresolved": "quiet-red"}
        )
        self.assertEqual(accuracy, 0.25)

    def test_synthesized_seat_is_exact(self):
        self.assertTrue(seat_is_exact(self.ground, self.seat))
        for execution in execute_all(self.ground, self.seat):
            self.assertEqual(execution.answer, self.ground.answer[execution.case])

    def test_two_local_doings_are_necessary_in_worst_case(self):
        self.assertEqual(seat_depth(self.seat), 2)
        self.assertEqual(seat_node_count(self.seat), 7)

    def test_generated_transcripts_split_every_old_conflict(self):
        self.assertTrue(conflict_transcripts_separate(self.ground, self.seat))
        self.assertEqual(len(generated_partition(self.ground, self.seat)), 4)

    def test_binary_answerability_strictly_expands(self):
        self.assertEqual(binary_answerability_count(old_partition(self.ground)), 2)
        self.assertEqual(
            binary_answerability_count(generated_partition(self.ground, self.seat)),
            16,
        )
        self.assertEqual(answerability_gain(self.ground, self.seat), 14)

    def test_cross_case_replay_exposes_local_production(self):
        self.assertTrue(replay_exposes_local_production(self.ground, self.seat))
        donor = execute_seat(self.ground, self.seat, "quiet-red")
        donor_marks = tuple(mark for _, mark in donor.transcript)
        replayed = execute_seat(
            self.ground,
            self.seat,
            "noisy-blue",
            replay_marks=donor_marks,
        )
        self.assertEqual(replayed.answer, "quiet-red")
        self.assertNotEqual(replayed.answer, self.ground.answer["noisy-blue"])

    def test_regenerative_certificate_keeps_claim_ceiling(self):
        certificate = regenerative_certificate(self.ground, self.seat)
        self.assertTrue(certificate["seat_exact"])
        self.assertTrue(certificate["cross_case_replay_breaks_exactness"])
        self.assertFalse(certificate["old_answerable"])
        self.assertFalse(certificate["establishes_consciousness"])

    def test_no_declared_doing_means_no_seat_for_a_real_conflict(self):
        ground = FiniteGround(
            cases=("x", "y"),
            actions=(),
            standing={"x": "same", "y": "same"},
            response={},
            answer={"x": 0, "y": 1},
        )
        with self.assertRaises(NoSeatAvailable):
            synthesize_seat(ground)

    def test_a_doing_that_never_splits_is_not_a_seat(self):
        ground = FiniteGround(
            cases=("x", "y"),
            actions=("repeat",),
            standing={"x": "same", "y": "same"},
            response={("x", "repeat"): "same", ("y", "repeat"): "same"},
            answer={"x": 0, "y": 1},
        )
        with self.assertRaises(NoSeatAvailable):
            synthesize_seat(ground)

    def test_an_old_answerable_ground_needs_only_leaves(self):
        ground = FiniteGround(
            cases=("x", "y"),
            actions=(),
            standing={"x": "left", "y": "right"},
            response={},
            answer={"x": 0, "y": 1},
        )
        seat = synthesize_seat(ground)
        self.assertTrue(seat_is_exact(ground, seat))
        self.assertEqual(seat_depth(seat), 0)
        self.assertTrue(all(isinstance(tree, Leaf) for _, tree in seat.roots))

    def test_missing_local_mark_is_rejected(self):
        ground = FiniteGround(
            cases=("x",),
            actions=("look",),
            standing={"x": "s"},
            response={},
            answer={"x": 0},
        )
        with self.assertRaises(GroundValidationError):
            ground.validate()


class ToolBirthTests(unittest.TestCase):
    def setUp(self):
        self.before, self.after = _tool_birth_grounds()

    def test_old_actions_lock_answer_conflicts(self):
        locked = action_indistinguishable_pairs(self.before)
        locked_conflicts = [
            pair
            for pair in locked
            if self.before.answer[pair[0]] != self.before.answer[pair[1]]
        ]
        self.assertEqual(len(locked_conflicts), 2)
        with self.assertRaises(NoSeatAvailable):
            synthesize_seat(self.before)

    def test_installed_doing_has_a_new_partition(self):
        self.assertTrue(
            action_is_partition_new(self.before, self.after, "look-colour")
        )
        self.assertNotEqual(
            action_partition(self.before, "test-noise"),
            action_partition(self.after, "look-colour"),
        )

    def test_installed_doing_crosses_old_tool_boundary(self):
        certificate = tool_birth_certificate(
            self.before, self.after, "look-colour"
        )
        self.assertFalse(certificate["old_exact_seat_exists"])
        self.assertTrue(certificate["extended_exact_seat_exists"])
        self.assertTrue(certificate["crosses_old_tool_boundary"])
        self.assertFalse(certificate["constructs_physical_tool"])

    def test_extended_ground_now_has_an_exact_regenerative_seat(self):
        seat = synthesize_seat(self.after)
        self.assertTrue(seat_is_exact(self.after, seat))
        self.assertTrue(replay_exposes_local_production(self.after, seat))


class SeatTransportTests(unittest.TestCase):
    def setUp(self):
        self.source = _origin_ground()
        self.target = _translated_ground()
        self.seat = synthesize_seat(self.source)
        self.case_map = {
            "quiet-red": "case-0",
            "quiet-blue": "case-1",
            "noisy-red": "case-2",
            "noisy-blue": "case-3",
        }
        self.standing_map = {"unresolved": "blank"}
        self.action_map = {"look-colour": "seat-A", "test-noise": "seat-B"}
        self.mark_map = {
            "warm": "left",
            "cool": "right",
            "still": "flat",
            "moving": "rough",
        }
        self.answer_map = {
            "quiet-red": 10,
            "quiet-blue": 20,
            "noisy-red": 30,
            "noisy-blue": 40,
        }

    def test_translation_commutes_despite_different_symbols(self):
        self.assertTrue(
            translation_commutes(
                self.source,
                self.target,
                self.case_map,
                self.standing_map,
                self.action_map,
                self.mark_map,
                self.answer_map,
            )
        )

    def test_translated_seat_answers_target_ground(self):
        self.assertTrue(
            transported_seat_is_exact(
                self.source,
                self.target,
                self.seat,
                self.case_map,
                self.standing_map,
                self.action_map,
                self.mark_map,
                self.answer_map,
            )
        )
        translated = translate_seat(
            self.seat,
            self.standing_map,
            self.action_map,
            self.mark_map,
            self.answer_map,
        )
        self.assertTrue(seat_is_exact(self.target, translated))

    def test_mark_translation_cannot_merge_unequal_residual_seats(self):
        collapsed = dict(self.mark_map)
        collapsed["warm"] = "colour"
        collapsed["cool"] = "colour"
        with self.assertRaises(TranslationCollision):
            translate_seat(
                self.seat,
                self.standing_map,
                self.action_map,
                collapsed,
                self.answer_map,
            )

    def test_noncommuting_response_translation_is_detected(self):
        wrong = dict(self.mark_map)
        wrong["warm"] = "right"
        self.assertFalse(
            translation_commutes(
                self.source,
                self.target,
                self.case_map,
                self.standing_map,
                self.action_map,
                wrong,
                self.answer_map,
            )
        )

    def test_transport_preserves_regenerative_structure_not_literal_marks(self):
        translated = translate_seat(
            self.seat,
            self.standing_map,
            self.action_map,
            self.mark_map,
            self.answer_map,
        )
        source_transcripts = {e.transcript for e in execute_all(self.source, self.seat)}
        target_transcripts = {e.transcript for e in execute_all(self.target, translated)}
        self.assertNotEqual(source_transcripts, target_transcripts)
        self.assertEqual(len(source_transcripts), len(target_transcripts))
        self.assertTrue(conflict_transcripts_separate(self.target, translated))

    def test_committed_demonstration_is_serializable_and_exact(self):
        result = demonstration()
        json.dumps(result, sort_keys=True)
        self.assertEqual(result["fixed_view_accuracy"], 0.25)
        self.assertEqual(result["worst_case_doings"], 2)
        self.assertTrue(result["translated_seat_exact"])
        self.assertTrue(result["collapsed_mark_translation_rejected"])


if __name__ == "__main__":
    unittest.main()
