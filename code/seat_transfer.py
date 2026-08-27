"""Finite semantics for regenerative answers and seat transfer.

The module treats an answer as an enacted protocol that expands a recipient
ground's answerability on delayed cases.  It deliberately contains no
consciousness predicate and no claim that a finite decision tree is the full
theory.  Its job is to make the native distinctions executable:

* a transferred artifact is fixed before the delayed case is selected;
* the old standing may merge cases that require different answers;
* a seat asks local doings and branches on locally produced marks;
* an exact seat separates every old-standing answer conflict;
* replay and mark-merging expose whether local production is necessary;
* a seat can be transported between differently named grounds when the
  translations commute.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from typing import Any, Hashable, Iterable, Mapping, Sequence, TypeAlias


Case: TypeAlias = Hashable
Standing: TypeAlias = Hashable
Action: TypeAlias = Hashable
Mark: TypeAlias = Hashable
Answer: TypeAlias = Hashable


class GroundValidationError(ValueError):
    """The finite ground is incomplete or internally inconsistent."""


class NoSeatAvailable(RuntimeError):
    """No protocol over the declared doings separates every answer conflict."""


class TranslationCollision(RuntimeError):
    """A proposed mark translation merges branches that require different use."""


@dataclass(frozen=True)
class FiniteGround:
    """A finite delayed-question ground.

    ``standing`` is everything available before the transferred seat is
    enacted. ``response[(case, action)]`` is the mark locally produced by
    performing an action in a case. ``answer`` is used only to validate a seat;
    the synthesizer is therefore an exact finite witness, not a discovery
    system for unknown natural answers.
    """

    cases: tuple[Case, ...]
    actions: tuple[Action, ...]
    standing: Mapping[Case, Standing]
    response: Mapping[tuple[Case, Action], Mark]
    answer: Mapping[Case, Answer]

    def validate(self) -> None:
        if not self.cases:
            raise GroundValidationError("a ground needs at least one case")
        if len(set(self.cases)) != len(self.cases):
            raise GroundValidationError("case names must be unique")
        if len(set(self.actions)) != len(self.actions):
            raise GroundValidationError("action names must be unique")
        for case in self.cases:
            if case not in self.standing:
                raise GroundValidationError(f"missing old standing for {case!r}")
            if case not in self.answer:
                raise GroundValidationError(f"missing target answer for {case!r}")
            for action in self.actions:
                if (case, action) not in self.response:
                    raise GroundValidationError(
                        f"missing local mark for case {case!r}, action {action!r}"
                    )

    def local_mark(self, case: Case, action: Action) -> Mark:
        return self.response[(case, action)]


@dataclass(frozen=True)
class Leaf:
    answer: Answer


@dataclass(frozen=True)
class Ask:
    action: Action
    branches: tuple[tuple[Mark, "SeatTree"], ...]

    def branch(self, mark: Mark) -> "SeatTree":
        for edge_mark, child in self.branches:
            if edge_mark == mark:
                return child
        raise KeyError(f"seat has no branch for mark {mark!r}")


SeatTree: TypeAlias = Leaf | Ask


@dataclass(frozen=True)
class Seat:
    """One protocol root for each old standing available to the recipient."""

    roots: tuple[tuple[Standing, SeatTree], ...]

    def root(self, standing: Standing) -> SeatTree:
        for root_standing, tree in self.roots:
            if root_standing == standing:
                return tree
        raise KeyError(f"seat has no root for standing {standing!r}")


@dataclass(frozen=True)
class Execution:
    case: Case
    old_standing: Standing
    transcript: tuple[tuple[Action, Mark], ...]
    answer: Answer

    @property
    def generated_standing(self) -> tuple[Standing, tuple[tuple[Action, Mark], ...]]:
        return (self.old_standing, self.transcript)


def _stable(values: Iterable[Hashable]) -> tuple[Hashable, ...]:
    return tuple(sorted(values, key=repr))


def tree_depth(tree: SeatTree) -> int:
    if isinstance(tree, Leaf):
        return 0
    return 1 + max(tree_depth(child) for _, child in tree.branches)


def tree_node_count(tree: SeatTree) -> int:
    if isinstance(tree, Leaf):
        return 1
    return 1 + sum(tree_node_count(child) for _, child in tree.branches)


def seat_depth(seat: Seat) -> int:
    return max(tree_depth(tree) for _, tree in seat.roots)


def seat_node_count(seat: Seat) -> int:
    return sum(tree_node_count(tree) for _, tree in seat.roots)


def old_conflicts(ground: FiniteGround) -> tuple[tuple[Case, Case], ...]:
    """Pairs merged by old standing that require different answers."""

    ground.validate()
    conflicts: list[tuple[Case, Case]] = []
    for index, left in enumerate(ground.cases):
        for right in ground.cases[index + 1 :]:
            if (
                ground.standing[left] == ground.standing[right]
                and ground.answer[left] != ground.answer[right]
            ):
                conflicts.append((left, right))
    return tuple(conflicts)


def old_answerable(ground: FiniteGround) -> bool:
    return not old_conflicts(ground)


def action_indistinguishable_pairs(
    ground: FiniteGround,
) -> tuple[tuple[Case, Case], ...]:
    """Old-standing pairs no adaptive protocol over current actions can split."""

    ground.validate()
    pairs: list[tuple[Case, Case]] = []
    for index, left in enumerate(ground.cases):
        for right in ground.cases[index + 1 :]:
            if ground.standing[left] != ground.standing[right]:
                continue
            if all(
                ground.local_mark(left, action) == ground.local_mark(right, action)
                for action in ground.actions
            ):
                pairs.append((left, right))
    return tuple(pairs)


def install_action(
    ground: FiniteGround,
    action: Action,
    marks: Mapping[Case, Mark],
) -> FiniteGround:
    """Return a new ground in which an enacted seat has added one doing.

    The function does not pretend to manufacture the physical response law. It
    records the exact before/after boundary once a constructor has made the new
    doing available.
    """

    ground.validate()
    if action in ground.actions:
        raise GroundValidationError(f"action {action!r} already exists")
    if set(marks) != set(ground.cases):
        raise GroundValidationError("new action needs exactly one mark per case")
    response = dict(ground.response)
    response.update({(case, action): marks[case] for case in ground.cases})
    extended = FiniteGround(
        cases=ground.cases,
        actions=ground.actions + (action,),
        standing=dict(ground.standing),
        response=response,
        answer=dict(ground.answer),
    )
    extended.validate()
    return extended


def action_partition(
    ground: FiniteGround, action: Action
) -> tuple[tuple[Case, ...], ...]:
    ground.validate()
    cells: dict[Mark, list[Case]] = {}
    for case in ground.cases:
        cells.setdefault(ground.local_mark(case, action), []).append(case)
    ordered = sorted(cells.values(), key=lambda cell: tuple(map(repr, cell)))
    return tuple(tuple(cell) for cell in ordered)


def action_is_partition_new(
    before: FiniteGround, after: FiniteGround, new_action: Action
) -> bool:
    """Whether the installed doing induces no old action's case partition."""

    if new_action in before.actions or new_action not in after.actions:
        return False
    new_partition = action_partition(after, new_action)
    return all(
        action_partition(before, old_action) != new_partition
        for old_action in before.actions
    )


def tool_birth_certificate(
    before: FiniteGround, after: FiniteGround, new_action: Action
) -> dict[str, Any]:
    """Certify that an installed doing crosses an old action boundary."""

    before.validate()
    after.validate()
    if before.cases != after.cases:
        raise GroundValidationError("tool birth comparison needs identical cases")
    if dict(before.standing) != dict(after.standing):
        raise GroundValidationError("old standing changed during action installation")
    if dict(before.answer) != dict(after.answer):
        raise GroundValidationError("target answer changed during action installation")
    if new_action in before.actions or new_action not in after.actions:
        raise GroundValidationError("comparison does not add the declared action")

    locked_pairs = action_indistinguishable_pairs(before)
    locked_conflicts = [
        (left, right)
        for left, right in locked_pairs
        if before.answer[left] != before.answer[right]
    ]
    newly_split = [
        (left, right)
        for left, right in locked_conflicts
        if after.local_mark(left, new_action) != after.local_mark(right, new_action)
    ]

    try:
        synthesize_seat(before)
        before_has_seat = True
    except NoSeatAvailable:
        before_has_seat = False
    try:
        after_seat = synthesize_seat(after)
        after_has_exact_seat = seat_is_exact(after, after_seat)
    except NoSeatAvailable:
        after_seat = None
        after_has_exact_seat = False

    return {
        "old_action_count": len(before.actions),
        "new_action_count": len(after.actions),
        "new_action_absent_before": new_action not in before.actions,
        "new_action_partition_is_new": action_is_partition_new(
            before, after, new_action
        ),
        "old_protocol_locked_conflicts": len(locked_conflicts),
        "locked_conflicts_split_by_new_action": len(newly_split),
        "old_exact_seat_exists": before_has_seat,
        "extended_exact_seat_exists": after_has_exact_seat,
        "extended_worst_case_doings": (
            seat_depth(after_seat) if after_seat is not None else None
        ),
        "crosses_old_tool_boundary": (
            bool(locked_conflicts)
            and len(newly_split) == len(locked_conflicts)
            and not before_has_seat
            and after_has_exact_seat
        ),
        "constructs_physical_tool": False,
        "establishes_consciousness": False,
    }


def synthesize_seat(ground: FiniteGround) -> Seat:
    """Synthesize an exact minimum-worst-depth adaptive seat.

    Ties are broken by total node count and then action representation.  The
    algorithm works inside each old-standing fiber because the recipient may
    condition its first doing on what it already distinguishes.
    """

    ground.validate()

    @lru_cache(maxsize=None)
    def solve(cases: tuple[Case, ...]) -> SeatTree | None:
        answers = {ground.answer[case] for case in cases}
        if len(answers) == 1:
            return Leaf(next(iter(answers)))

        candidates: list[tuple[int, int, str, Ask]] = []
        for action in ground.actions:
            cells: dict[Mark, list[Case]] = {}
            for case in cases:
                cells.setdefault(ground.local_mark(case, action), []).append(case)
            if len(cells) <= 1:
                continue

            branches: list[tuple[Mark, SeatTree]] = []
            failed = False
            for mark in _stable(cells):
                child_cases = tuple(sorted(cells[mark], key=repr))
                child = solve(child_cases)
                if child is None:
                    failed = True
                    break
                branches.append((mark, child))
            if failed:
                continue

            node = Ask(action=action, branches=tuple(branches))
            candidates.append(
                (tree_depth(node), tree_node_count(node), repr(action), node)
            )

        if not candidates:
            return None
        candidates.sort(key=lambda item: item[:3])
        return candidates[0][3]

    roots: list[tuple[Standing, SeatTree]] = []
    standings = _stable({ground.standing[case] for case in ground.cases})
    for standing in standings:
        cases = tuple(
            sorted(
                (case for case in ground.cases if ground.standing[case] == standing),
                key=repr,
            )
        )
        tree = solve(cases)
        if tree is None:
            unresolved = [
                pair
                for pair in old_conflicts(ground)
                if ground.standing[pair[0]] == standing
            ]
            raise NoSeatAvailable(
                f"declared doings cannot separate conflicts at {standing!r}: "
                f"{unresolved!r}"
            )
        roots.append((standing, tree))
    return Seat(tuple(roots))


def execute_seat(
    ground: FiniteGround,
    seat: Seat,
    case: Case,
    *,
    replay_marks: Sequence[Mark] | None = None,
) -> Execution:
    """Enact a seat, optionally replaying another execution's local marks."""

    ground.validate()
    if case not in ground.cases:
        raise KeyError(case)
    node = seat.root(ground.standing[case])
    transcript: list[tuple[Action, Mark]] = []
    replay_index = 0

    while isinstance(node, Ask):
        if replay_marks is None:
            mark = ground.local_mark(case, node.action)
        else:
            if replay_index >= len(replay_marks):
                raise ValueError("replay transcript ended before the seat stopped")
            mark = replay_marks[replay_index]
            replay_index += 1
        transcript.append((node.action, mark))
        node = node.branch(mark)

    return Execution(
        case=case,
        old_standing=ground.standing[case],
        transcript=tuple(transcript),
        answer=node.answer,
    )


def execute_all(ground: FiniteGround, seat: Seat) -> tuple[Execution, ...]:
    return tuple(execute_seat(ground, seat, case) for case in ground.cases)


def seat_is_exact(ground: FiniteGround, seat: Seat) -> bool:
    try:
        executions = execute_all(ground, seat)
    except (KeyError, ValueError):
        return False
    return all(execution.answer == ground.answer[execution.case] for execution in executions)


def generated_partition(
    ground: FiniteGround, seat: Seat
) -> tuple[tuple[Case, ...], ...]:
    """Partition of cases by old standing plus locally enacted transcript."""

    cells: dict[Hashable, list[Case]] = {}
    for execution in execute_all(ground, seat):
        cells.setdefault(execution.generated_standing, []).append(execution.case)
    ordered = sorted(cells.values(), key=lambda cell: tuple(map(repr, cell)))
    return tuple(tuple(cell) for cell in ordered)


def old_partition(ground: FiniteGround) -> tuple[tuple[Case, ...], ...]:
    ground.validate()
    cells: dict[Standing, list[Case]] = {}
    for case in ground.cases:
        cells.setdefault(ground.standing[case], []).append(case)
    ordered = sorted(cells.values(), key=lambda cell: tuple(map(repr, cell)))
    return tuple(tuple(cell) for cell in ordered)


def binary_answerability_count(partition: Sequence[Sequence[Case]]) -> int:
    """Number of binary questions constant on the cells of a partition."""

    return 2 ** len(partition)


def answerability_gain(ground: FiniteGround, seat: Seat) -> int:
    return binary_answerability_count(generated_partition(ground, seat)) - binary_answerability_count(
        old_partition(ground)
    )


def conflict_transcripts_separate(ground: FiniteGround, seat: Seat) -> bool:
    executions = {execution.case: execution for execution in execute_all(ground, seat)}
    return all(
        executions[left].generated_standing != executions[right].generated_standing
        for left, right in old_conflicts(ground)
    )


def replay_exposes_local_production(ground: FiniteGround, seat: Seat) -> bool:
    """Whether some old conflict is answered wrongly under cross-case replay."""

    executions = {execution.case: execution for execution in execute_all(ground, seat)}
    for donor, recipient in old_conflicts(ground):
        donor_marks = tuple(mark for _, mark in executions[donor].transcript)
        try:
            replayed = execute_seat(
                ground, seat, recipient, replay_marks=donor_marks
            )
        except (KeyError, ValueError):
            return True
        if replayed.answer != ground.answer[recipient]:
            return True
    return False


def regenerative_certificate(ground: FiniteGround, seat: Seat) -> dict[str, Any]:
    conflicts = old_conflicts(ground)
    return {
        "artifact_fixed_before_case": True,
        "old_answerable": not conflicts,
        "conflict_count": len(conflicts),
        "seat_exact": seat_is_exact(ground, seat),
        "conflicts_separated_by_local_transcript": conflict_transcripts_separate(
            ground, seat
        ),
        "cross_case_replay_breaks_exactness": replay_exposes_local_production(
            ground, seat
        ),
        "old_binary_answerability": binary_answerability_count(old_partition(ground)),
        "generated_binary_answerability": binary_answerability_count(
            generated_partition(ground, seat)
        ),
        "binary_answerability_gain": answerability_gain(ground, seat),
        "worst_case_doings": seat_depth(seat),
        "seat_nodes": seat_node_count(seat),
        "establishes_consciousness": False,
    }


def translate_tree(
    tree: SeatTree,
    action_map: Mapping[Action, Action],
    mark_map: Mapping[Mark, Mark],
    answer_map: Mapping[Answer, Answer],
) -> SeatTree:
    if isinstance(tree, Leaf):
        return Leaf(answer_map[tree.answer])

    translated: dict[Mark, SeatTree] = {}
    for source_mark, child in tree.branches:
        target_mark = mark_map[source_mark]
        target_child = translate_tree(child, action_map, mark_map, answer_map)
        if target_mark in translated and translated[target_mark] != target_child:
            raise TranslationCollision(
                f"translated mark {target_mark!r} merges unequal residual seats"
            )
        translated[target_mark] = target_child
    branches = tuple((mark, translated[mark]) for mark in _stable(translated))
    return Ask(action=action_map[tree.action], branches=branches)


def translate_seat(
    seat: Seat,
    standing_map: Mapping[Standing, Standing],
    action_map: Mapping[Action, Action],
    mark_map: Mapping[Mark, Mark],
    answer_map: Mapping[Answer, Answer],
) -> Seat:
    roots_by_standing: dict[Standing, SeatTree] = {}
    for source_standing, tree in seat.roots:
        target_standing = standing_map[source_standing]
        target_tree = translate_tree(tree, action_map, mark_map, answer_map)
        if (
            target_standing in roots_by_standing
            and roots_by_standing[target_standing] != target_tree
        ):
            raise TranslationCollision(
                f"standing translation merges unequal roots at {target_standing!r}"
            )
        roots_by_standing[target_standing] = target_tree
    return Seat(
        tuple(
            (standing, roots_by_standing[standing])
            for standing in _stable(roots_by_standing)
        )
    )


def translation_commutes(
    source: FiniteGround,
    target: FiniteGround,
    case_map: Mapping[Case, Case],
    standing_map: Mapping[Standing, Standing],
    action_map: Mapping[Action, Action],
    mark_map: Mapping[Mark, Mark],
    answer_map: Mapping[Answer, Answer],
) -> bool:
    source.validate()
    target.validate()
    try:
        for source_case in source.cases:
            target_case = case_map[source_case]
            if standing_map[source.standing[source_case]] != target.standing[target_case]:
                return False
            if answer_map[source.answer[source_case]] != target.answer[target_case]:
                return False
            for source_action in source.actions:
                target_action = action_map[source_action]
                if (
                    mark_map[source.local_mark(source_case, source_action)]
                    != target.local_mark(target_case, target_action)
                ):
                    return False
    except KeyError:
        return False
    return True


def transported_seat_is_exact(
    source: FiniteGround,
    target: FiniteGround,
    source_seat: Seat,
    case_map: Mapping[Case, Case],
    standing_map: Mapping[Standing, Standing],
    action_map: Mapping[Action, Action],
    mark_map: Mapping[Mark, Mark],
    answer_map: Mapping[Answer, Answer],
) -> bool:
    if not translation_commutes(
        source,
        target,
        case_map,
        standing_map,
        action_map,
        mark_map,
        answer_map,
    ):
        return False
    try:
        target_seat = translate_seat(
            source_seat, standing_map, action_map, mark_map, answer_map
        )
    except TranslationCollision:
        return False
    return seat_is_exact(target, target_seat)


def fixed_view_accuracy(ground: FiniteGround, view: Mapping[Standing, Answer]) -> float:
    """Accuracy of an answer deposited before the delayed case is distinguished."""

    ground.validate()
    correct = sum(
        view.get(ground.standing[case], object()) == ground.answer[case]
        for case in ground.cases
    )
    return correct / len(ground.cases)


def _origin_ground() -> FiniteGround:
    cases = ("quiet-red", "quiet-blue", "noisy-red", "noisy-blue")
    actions = ("look-colour", "test-noise")
    standing = {case: "unresolved" for case in cases}
    answer = {
        "quiet-red": "quiet-red",
        "quiet-blue": "quiet-blue",
        "noisy-red": "noisy-red",
        "noisy-blue": "noisy-blue",
    }
    response = {
        ("quiet-red", "look-colour"): "warm",
        ("quiet-blue", "look-colour"): "cool",
        ("noisy-red", "look-colour"): "warm",
        ("noisy-blue", "look-colour"): "cool",
        ("quiet-red", "test-noise"): "still",
        ("quiet-blue", "test-noise"): "still",
        ("noisy-red", "test-noise"): "moving",
        ("noisy-blue", "test-noise"): "moving",
    }
    return FiniteGround(cases, actions, standing, response, answer)


def _translated_ground() -> FiniteGround:
    cases = ("case-0", "case-1", "case-2", "case-3")
    actions = ("seat-A", "seat-B")
    standing = {case: "blank" for case in cases}
    answer = {
        "case-0": 10,
        "case-1": 20,
        "case-2": 30,
        "case-3": 40,
    }
    response = {
        ("case-0", "seat-A"): "left",
        ("case-1", "seat-A"): "right",
        ("case-2", "seat-A"): "left",
        ("case-3", "seat-A"): "right",
        ("case-0", "seat-B"): "flat",
        ("case-1", "seat-B"): "flat",
        ("case-2", "seat-B"): "rough",
        ("case-3", "seat-B"): "rough",
    }
    return FiniteGround(cases, actions, standing, response, answer)


def _tool_birth_grounds() -> tuple[FiniteGround, FiniteGround]:
    full = _origin_ground()
    old_action = "test-noise"
    before = FiniteGround(
        cases=full.cases,
        actions=(old_action,),
        standing=dict(full.standing),
        response={
            (case, old_action): full.local_mark(case, old_action)
            for case in full.cases
        },
        answer=dict(full.answer),
    )
    after = install_action(
        before,
        "look-colour",
        {case: full.local_mark(case, "look-colour") for case in full.cases},
    )
    return before, after


def demonstration() -> dict[str, Any]:
    source = _origin_ground()
    target = _translated_ground()
    seat = synthesize_seat(source)

    case_map = {
        "quiet-red": "case-0",
        "quiet-blue": "case-1",
        "noisy-red": "case-2",
        "noisy-blue": "case-3",
    }
    standing_map = {"unresolved": "blank"}
    action_map = {"look-colour": "seat-A", "test-noise": "seat-B"}
    mark_map = {"warm": "left", "cool": "right", "still": "flat", "moving": "rough"}
    answer_map = {
        "quiet-red": 10,
        "quiet-blue": 20,
        "noisy-red": 30,
        "noisy-blue": 40,
    }

    certificate = regenerative_certificate(source, seat)
    before_tool, after_tool = _tool_birth_grounds()
    certificate.update(
        {
            "fixed_view_accuracy": fixed_view_accuracy(
                source, {"unresolved": "quiet-red"}
            ),
            "translation_commutes": translation_commutes(
                source,
                target,
                case_map,
                standing_map,
                action_map,
                mark_map,
                answer_map,
            ),
            "translated_seat_exact": transported_seat_is_exact(
                source,
                target,
                seat,
                case_map,
                standing_map,
                action_map,
                mark_map,
                answer_map,
            ),
            "tool_birth": tool_birth_certificate(
                before_tool, after_tool, "look-colour"
            ),
        }
    )

    try:
        translate_seat(
            seat,
            standing_map,
            action_map,
            {
                "warm": "merged",
                "cool": "merged",
                "still": "flat",
                "moving": "rough",
            },
            answer_map,
        )
        certificate["collapsed_mark_translation_rejected"] = False
    except TranslationCollision:
        certificate["collapsed_mark_translation_rejected"] = True

    return certificate


if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2, sort_keys=True))
