from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Sequence


@dataclass(frozen=True)
class Case:
    name: str
    source_state: tuple[Hashable, ...]
    coarse_report: Hashable
    continuation: str
    correct_output: Hashable


@dataclass(frozen=True)
class RepairResult:
    baseline_correct: int
    repaired_correct: int
    total: int
    promoted_coordinates: tuple[int, ...]


def baseline_predict(cases: Sequence[Case]) -> dict[tuple[Hashable, str], Hashable]:
    """Memorize the first answer for each coarse report and continuation.

    This deliberately models false closure: future-distinct sources are merged.
    """
    model: dict[tuple[Hashable, str], Hashable] = {}
    for case in cases:
        model.setdefault((case.coarse_report, case.continuation), case.correct_output)
    return model


def essential_coordinates(cases: Sequence[Case]) -> tuple[int, ...]:
    """Return coordinates required to make every covered continuation deterministic."""
    if not cases:
        return ()
    width = len(cases[0].source_state)
    essential: list[int] = []
    for j in range(width):
        for a in cases:
            for b in cases:
                if a.continuation != b.continuation:
                    continue
                if all(a.source_state[k] == b.source_state[k] for k in range(width) if k != j):
                    if a.source_state[j] != b.source_state[j] and a.correct_output != b.correct_output:
                        essential.append(j)
                        break
            if j in essential:
                break
    # Close under collisions: add the least coordinate that separates each unresolved pair.
    chosen = set(essential)
    changed = True
    while changed:
        changed = False
        for a in cases:
            for b in cases:
                if a.continuation != b.continuation or a.correct_output == b.correct_output:
                    continue
                if all(a.source_state[k] == b.source_state[k] for k in chosen):
                    for k in range(width):
                        if a.source_state[k] != b.source_state[k]:
                            chosen.add(k)
                            changed = True
                            break
    return tuple(sorted(chosen))


def repaired_predict(cases: Sequence[Case], coordinates: Iterable[int]) -> dict[tuple[tuple[Hashable, ...], str], Hashable]:
    coords = tuple(coordinates)
    model: dict[tuple[tuple[Hashable, ...], str], Hashable] = {}
    for case in cases:
        key = (tuple(case.source_state[k] for k in coords), case.continuation)
        prior = model.get(key)
        if prior is not None and prior != case.correct_output:
            raise ValueError(f"representation remains insufficient for {case.name}")
        model[key] = case.correct_output
    return model


def evaluate(cases: Sequence[Case]) -> RepairResult:
    base = baseline_predict(cases)
    b_correct = sum(base[(c.coarse_report, c.continuation)] == c.correct_output for c in cases)
    coords = essential_coordinates(cases)
    repaired = repaired_predict(cases, coords)
    r_correct = sum(repaired[(tuple(c.source_state[k] for k in coords), c.continuation)] == c.correct_output for c in cases)
    return RepairResult(b_correct, r_correct, len(cases), coords)


def fixture() -> list[Case]:
    """Six collision families spanning provenance, time, role, and relation structure."""
    return [
        Case("source-a", ("source-a", "same-value", "writer"), "same-value", "next", "retain-a"),
        Case("source-b", ("source-b", "same-value", "writer"), "same-value", "next", "retain-b"),
        Case("early", ("sensor", 0, "phase-early"), "sensor", "forecast", "rise"),
        Case("late", ("sensor", 0, "phase-late"), "sensor", "forecast", "fall"),
        Case("author", ("person-1", "statement", "author"), "statement", "credit", "person-1"),
        Case("reporter", ("person-2", "statement", "reporter"), "statement", "credit", "person-2"),
        Case("pair-ab", ("A", "B", "compatible"), "A+B", "compose", "joint"),
        Case("pair-ac", ("A", "C", "exclusive"), "A+B", "compose", "branch"),
        Case("tool-old", ("task", "tool-v1", "unsupported"), "task", "execute", "fail"),
        Case("tool-new", ("task", "tool-v2", "supported"), "task", "execute", "pass"),
        Case("coarse-history", ("state", "depth-1", "history-x"), "state", "predict", "left"),
        Case("deep-history", ("state", "depth-2", "history-y"), "state", "predict", "right"),
    ]


if __name__ == "__main__":
    result = evaluate(fixture())
    print(result)
