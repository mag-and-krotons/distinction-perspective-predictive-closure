"""Executable reference model for native-order distinction transport.

The implementation is deliberately finite.  It trains a GF(2) bilinear
effect predictor from opaque actor/probe coordinates, uses behavior rather
than generator labels to form distinctions, transports a one-example teaching
message to a heterogeneous receiver, and preserves the sender-blind
``C=1,S=0`` case before active recovery.

Nothing here claims access to a unique natural-language chain of thought.  The
effect predictor is identified only by consequences under the declared probe
set; the supplied gauge-relative coordinates are not claimed to be a learned
minimal quotient.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import itertools
import json
from dataclasses import dataclass, field, replace
from typing import Any, Iterable, Mapping, Sequence

import numpy as np


SEED = 73_421
DIMENSION = 4


def _plain(value: Any) -> Any:
    """Convert values to a deterministic JSON-safe representation."""

    if dataclasses.is_dataclass(value):
        return _plain(dataclasses.asdict(value))
    if isinstance(value, np.ndarray):
        return value.astype(int).tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in sorted(value.items(), key=lambda p: str(p[0]))}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    if isinstance(value, set):
        return sorted(_plain(item) for item in value)
    return value


def _canonical(value: Any) -> bytes:
    return json.dumps(_plain(value), sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _xor_dot(left: Sequence[int], right: Sequence[int]) -> int:
    return int(sum(int(a) * int(b) for a, b in zip(left, right)) % 2)


def _gf2_inverse(matrix: np.ndarray) -> np.ndarray:
    """Invert a square binary matrix by Gauss-Jordan elimination."""

    a = np.asarray(matrix, dtype=np.uint8) % 2
    n = a.shape[0]
    aug = np.concatenate([a.copy(), np.eye(n, dtype=np.uint8)], axis=1)
    for column in range(n):
        pivots = np.flatnonzero(aug[column:, column])
        if not len(pivots):
            raise ValueError("singular GF(2) matrix")
        pivot = column + int(pivots[0])
        if pivot != column:
            aug[[column, pivot]] = aug[[pivot, column]]
        for row in range(n):
            if row != column and aug[row, column]:
                aug[row] ^= aug[column]
    return aug[:, n:] % 2


def _gf2_solve(features: np.ndarray, targets: np.ndarray) -> np.ndarray:
    """Return one exact solution of an overdetermined consistent GF(2) system."""

    x = np.asarray(features, dtype=np.uint8) % 2
    y = np.asarray(targets, dtype=np.uint8).reshape(-1, 1) % 2
    aug = np.concatenate([x.copy(), y], axis=1)
    rows, columns = x.shape
    pivot_rows: list[tuple[int, int]] = []
    active = 0
    for column in range(columns):
        candidates = np.flatnonzero(aug[active:, column])
        if not len(candidates):
            continue
        pivot = active + int(candidates[0])
        if pivot != active:
            aug[[active, pivot]] = aug[[pivot, active]]
        for row in range(rows):
            if row != active and aug[row, column]:
                aug[row] ^= aug[active]
        pivot_rows.append((active, column))
        active += 1
        if active == rows:
            break
    for row in range(rows):
        if not aug[row, :columns].any() and aug[row, columns]:
            raise ValueError("inconsistent GF(2) training effects")
    solution = np.zeros(columns, dtype=np.uint8)
    for row, column in reversed(pivot_rows):
        remainder = _xor_dot(aug[row, column + 1 : columns], solution[column + 1 :])
        solution[column] = int(aug[row, columns]) ^ remainder
    if not np.array_equal((x @ solution) % 2, targets.astype(np.uint8) % 2):
        raise AssertionError("learned effect law does not fit its observations")
    return solution


def _random_invertible_gauge(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    while True:
        candidate = rng.integers(0, 2, size=(DIMENSION, DIMENSION), dtype=np.uint8)
        try:
            _gf2_inverse(candidate)
        except ValueError:
            continue
        return candidate


@dataclass(frozen=True)
class Intervention:
    """A world input and its unrelated opaque observer coordinate."""

    vector: tuple[int, ...]
    opaque_id: str
    opaque_vector: tuple[int, ...]


@dataclass(frozen=True)
class RunResult:
    output: int


@dataclass(frozen=True)
class CausalProgram:
    name: str
    coefficients: tuple[int, ...]
    bias: int = 1

    def run(self, intervention: Intervention) -> RunResult:
        return RunResult(self.bias ^ _xor_dot(self.coefficients, intervention.vector))


@dataclass(frozen=True)
class OpaqueActorState:
    """Actor coordinates after a gauge transformation; no generator label."""

    bias: int
    coordinates: tuple[int, ...]


def form_opaque_actor_probe(
    program: CausalProgram, world_probe: Sequence[int], gauge_seed: int
) -> tuple[OpaqueActorState, tuple[int, ...]]:
    """Form dual opaque coordinates under a caller-chosen fresh gauge.

    This helper exposes the physical coordinate formation, not an outcome or
    generator identifier.  It lets independent tests evaluate new programs,
    gauges, and probes without relying on engine-reported pass/fail flags.
    """

    gauge = _random_invertible_gauge(gauge_seed)
    gauge_inverse = _gf2_inverse(gauge)
    c = np.asarray(program.coefficients, dtype=np.uint8)
    x = np.asarray(tuple(world_probe), dtype=np.uint8)
    h = (gauge_inverse.T @ c) % 2
    v = (gauge @ x) % 2
    return (
        OpaqueActorState(program.bias, tuple(int(item) for item in h)),
        tuple(int(item) for item in v),
    )


@dataclass(frozen=True)
class NativeState:
    bias: int
    coordinates: tuple[int, ...]

    @property
    def state_id(self) -> str:
        return _digest((self.bias, self.coordinates))[:16]


class NativeObserver:
    """Learn a probe-effect law from numeric effects only.

    The feature class is bilinear, but its coefficients are fit by GF(2)
    elimination.  The expected diagonal law is never assigned to ``weights``;
    it must be recovered from observed actor effects.
    """

    def __init__(self, weights: np.ndarray, training_bytes: bytes) -> None:
        self.weights = np.asarray(weights, dtype=np.uint8).copy()
        self.training_bytes = bytes(training_bytes)
        self._probe_vectors: dict[str, tuple[int, ...]] = {}

    @staticmethod
    def _features(state: NativeState | OpaqueActorState, probe: Sequence[int]) -> np.ndarray:
        h = np.asarray(state.coordinates, dtype=np.uint8)
        v = np.asarray(tuple(probe), dtype=np.uint8)
        return np.concatenate(
            [np.asarray([state.bias], dtype=np.uint8), np.outer(h, v).reshape(-1)]
        )

    @classmethod
    def learn(
        cls, heldout_states: set[tuple[int, tuple[int, ...]]] | None = None
    ) -> "NativeObserver":
        """Fit on anonymous effects from whole non-reference programs.

        Reference programs have Hamming-weight-one dependencies.  Training
        actors use only zero-, two-, and four-way dependencies, and training
        gauges are disjoint from the evaluation gauge.  The observer therefore
        has to learn the common effect operation instead of memorizing one of
        the three evaluated programs or their coordinate frame.
        """

        heldout_states = heldout_states or set()
        rows: list[np.ndarray] = []
        outputs: list[int] = []
        training_coefficients = (
            (0, 0, 0, 0),
            (1, 1, 0, 0),
            (1, 0, 1, 0),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (0, 1, 0, 1),
            (0, 0, 1, 1),
            (1, 1, 1, 1),
        )
        # These are effect observations.  No program identity, source profile,
        # or intervention name is present in the training record.
        for gauge_seed in (SEED + 101, SEED + 202, SEED + 303):
            gauge = _random_invertible_gauge(gauge_seed)
            gauge_inverse = _gf2_inverse(gauge)
            for bias in (0, 1):
                for coefficients in training_coefficients:
                    c = np.asarray(coefficients, dtype=np.uint8)
                    h = (gauge_inverse.T @ c) % 2
                    state = OpaqueActorState(bias, tuple(int(item) for item in h))
                    if (state.bias, state.coordinates) in heldout_states:
                        continue
                    for world_probe in itertools.product((0, 1), repeat=DIMENSION):
                        v = (gauge @ np.asarray(world_probe, dtype=np.uint8)) % 2
                        rows.append(cls._features(state, v))
                        outputs.append(bias ^ _xor_dot(coefficients, world_probe))
        x = np.vstack(rows).astype(np.uint8)
        y = np.asarray(outputs, dtype=np.uint8)
        weights = _gf2_solve(x, y)
        training_bytes = x.tobytes() + y.tobytes()
        return cls(weights, training_bytes)

    def register_probe(self, probe: Intervention) -> None:
        self._probe_vectors[probe.opaque_id] = tuple(probe.opaque_vector)

    def encode(self, opaque_state: OpaqueActorState) -> NativeState:
        # The representation is opaque/gauged. Its native meaning is supplied
        # by the learned response law, not by an external semantic label.
        return NativeState(opaque_state.bias, tuple(opaque_state.coordinates))

    def predict(self, latent: NativeState, probe_id: str) -> int:
        vector = self._probe_vectors[probe_id]
        return self.predict_vector(latent, vector)

    def predict_vector(self, latent: NativeState, opaque_probe: Sequence[int]) -> int:
        """Predict a fresh anonymous probe not present in the ID registry."""

        features = self._features(latent, opaque_probe)
        return int((features @ self.weights) % 2)

    def fingerprint(self) -> str:
        return _digest((self.weights.tolist(), self._probe_vectors))


@dataclass(frozen=True)
class CarrierSymbol:
    coordinates: tuple[int, ...]
    output: int


@dataclass(frozen=True)
class Carrier:
    """A bandwidth-limited causal example, not a rule name or truth table."""

    symbols: tuple[CarrierSymbol, ...]


@dataclass(frozen=True)
class ReceiverState:
    coefficients: tuple[int, ...]
    bias: int
    nuisance_sensitive: bool = False

    def respond(self, intervention: Intervention) -> int:
        value = self.bias ^ _xor_dot(self.coefficients, intervention.vector)
        if self.nuisance_sensitive and intervention.vector[-1]:
            value ^= 1
        return value


@dataclass
class FrozenReceiver:
    """Infer a dependency from examples, then execute it on unseen inputs."""

    candidates: tuple[tuple[int, ...], ...]
    preference: tuple[int, ...]
    nuisance_sensitive: bool = False

    def consume(self, carrier: Carrier) -> ReceiverState:
        surviving: list[tuple[int, ...]] = []
        for coefficients in self.candidates:
            if all(
                (1 ^ _xor_dot(coefficients, symbol.coordinates)) == symbol.output
                for symbol in carrier.symbols
            ):
                surviving.append(coefficients)
        if not surviving:
            selected = self.candidates[self.preference[0]]
        else:
            selected = next(
                self.candidates[index]
                for index in self.preference
                if self.candidates[index] in surviving
            )
        return ReceiverState(tuple(selected), 1, self.nuisance_sensitive)

    def fingerprint(self) -> str:
        return _digest((self.candidates, self.preference, self.nuisance_sensitive))


@dataclass(frozen=True)
class Metrics:
    C: int
    I: int
    S: int
    R: int


@dataclass(frozen=True)
class Commitment:
    predicted_effects: tuple[tuple[str, int], ...]
    receiver_model_version: str


@dataclass(frozen=True)
class Receipt:
    entry_count: int
    root_hash: str
    manifest_hash: str


class AppendOnlyLedger:
    """Hash chain verified against a separately retained prefix receipt."""

    def __init__(self, manifest_hash: str) -> None:
        self.manifest_hash = manifest_hash
        self.entries: list[dict[str, Any]] = []

    def append(self, kind: str, payload: Any) -> int:
        previous = self.entries[-1]["entry_hash"] if self.entries else self.manifest_hash
        entry = {
            "index": len(self.entries),
            "kind": str(kind),
            "payload": _plain(payload),
            "previous_hash": previous,
        }
        entry["entry_hash"] = _digest(entry)
        self.entries.append(entry)
        return int(entry["index"])

    def seal(self) -> Receipt:
        root = self.entries[-1]["entry_hash"] if self.entries else self.manifest_hash
        return Receipt(len(self.entries), root, self.manifest_hash)

    def verify(self, receipt: Receipt) -> bool:
        if receipt.manifest_hash != self.manifest_hash:
            return False
        if receipt.entry_count > len(self.entries):
            return False
        previous = self.manifest_hash
        for index, entry in enumerate(self.entries[: receipt.entry_count]):
            candidate = copy.deepcopy(entry)
            recorded = candidate.pop("entry_hash", None)
            if candidate.get("index") != index or candidate.get("previous_hash") != previous:
                return False
            if _digest(candidate) != recorded:
                return False
            previous = str(recorded)
        return previous == receipt.root_hash

    def unsafe_replace_payload(self, index: int, payload: Any) -> None:
        self.entries[index]["payload"] = _plain(payload)

    def unsafe_recompute_chain(self) -> None:
        previous = self.manifest_hash
        for index, entry in enumerate(self.entries):
            entry["index"] = index
            entry["previous_hash"] = previous
            candidate = copy.deepcopy(entry)
            candidate.pop("entry_hash", None)
            entry["entry_hash"] = _digest(candidate)
            previous = entry["entry_hash"]


@dataclass
class FrozenSnapshot:
    actor: CausalProgram
    candidates: tuple[CausalProgram, ...]
    gauge: tuple[tuple[int, ...], ...]
    observer: NativeObserver | None
    receiver: FrozenReceiver
    evaluator_id: str
    rng_seed: int
    environment_version: str
    interventions: dict[str, Intervention]
    reentered_receiver_state: NativeState | None
    snapshot_id: str
    component_hashes: tuple[tuple[str, str], ...]

    def run(self, intervention: Intervention) -> RunResult:
        return self.actor.run(intervention)


@dataclass
class Episode:
    metrics: Metrics
    ledger: AppendOnlyLedger
    receipt: Receipt
    carrier: Carrier
    commitment: Commitment
    evaluator_id: str
    receiver_effects: dict[str, int]
    source_effects: dict[str, int]
    committed_receiver_prediction: tuple[tuple[str, int], ...]
    commitment_step: int
    first_receiver_observation_step: int
    branch_snapshot_ids: dict[str, str]
    frozen_components: tuple[str, ...]
    snapshot: FrozenSnapshot
    native_state_ids: tuple[str, ...]
    observer_training_intervention_ids: tuple[str, ...]
    observer_holdout_intervention_ids: tuple[str, ...]
    opaque_actor_state: OpaqueActorState
    raw_actor_effects: dict[str, int]
    actual_receiver_state: ReceiverState
    evaluation_probe_ids: tuple[str, ...]


@dataclass
class Recovery:
    before: Episode
    after: Episode
    probes_used: int
    original_carrier: Carrier
    original_commitment: Commitment
    original_evaluator_id: str
    ledger: AppendOnlyLedger
    separator_commit_step: int
    probe_effect_step: int
    recovery_probe_ids: tuple[str, ...]
    evaluation_probe_ids: tuple[str, ...]
    recovered_native_state: NativeState | None = None


@dataclass(frozen=True)
class ReentryInterchangeResult:
    baseline_output: int
    correct_patch_output: int
    predicted_target_output: int
    reverse_patch_output: int
    equal_norm_shuffle_output: int
    null_patch_output: int


@dataclass
class NativeContinuation:
    """A continuation whose future behavior consumes a re-entered native state."""

    observer: NativeObserver
    native_state: NativeState

    def patch(self, state: NativeState) -> None:
        self.native_state = state

    def step(self, probe_id: str) -> int:
        return self.observer.predict(self.native_state, probe_id)


class NativeOrderEngine:
    """Reference implementation of commit/fork/observe/re-enter/transport."""

    def __init__(self, ablation: str | None = None) -> None:
        valid = {None, "no_transport", "no_self_observer", "no_active_probe", "no_invariance"}
        if ablation not in valid:
            raise ValueError(f"unknown ablation: {ablation}")
        self.ablation = ablation
        self._candidate_programs = (
            CausalProgram("route-amber", (1, 0, 0, 0)),
            CausalProgram("route-cobalt", (0, 1, 0, 0)),
            CausalProgram("route-vermillion", (0, 0, 1, 0)),
        )
        # The public contrast is a pair with the same baseline endpoint.  A
        # third anonymous candidate is retained internally so one binary
        # recovery answer cannot identify the receiver by construction.
        self.reference_programs = self._candidate_programs[:2]
        self._gauge = _random_invertible_gauge(SEED + 991)
        self._gauge_inverse = _gf2_inverse(self._gauge)
        self.interventions = self._build_interventions()
        self.observer: NativeObserver | None = (
            None if ablation == "no_self_observer" else NativeObserver.learn()
        )
        if self.observer is not None:
            for probe in self.interventions.values():
                self.observer.register_probe(probe)
        self.receiver = FrozenReceiver(
            candidates=tuple(p.coefficients for p in self._candidate_programs),
            # On ambiguity the actual receiver chooses cobalt.
            preference=(1, 2, 0),
            nuisance_sensitive=ablation == "no_invariance",
        )
        self.evaluator_id = "eval:" + _digest(("CISR", sorted(self.interventions)))[:16]
        self._live_nonce = 0
        self._rng_seed = SEED
        self._environment_version = "env:finite-gf2-v1"
        self._reentered_receiver_state: NativeState | None = None
        self._snapshot = self._freeze_snapshot()
        self._trusted_receipts: dict[str, Receipt] = {}
        self._occurrence_counter = 0

    def _build_interventions(self) -> dict[str, Intervention]:
        vectors = {
            "baseline": (0, 0, 0, 0),
            # This separator is deliberately not any candidate coefficient.
            # It conveys an effect, not a one-symbol generator identifier.
            "carrier": (0, 1, 1, 0),
            "recovery_one": (0, 1, 0, 0),
            "recovery_two": (0, 0, 1, 0),
            "irrelevant": (0, 0, 0, 1),
            "evaluation_one": (1, 1, 0, 0),
            "relevant": (1, 0, 1, 0),
            "composed": (1, 1, 1, 0),
            "post_eval_one": (0, 1, 0, 1),
            "post_eval_two": (0, 0, 1, 1),
            "post_eval_composed": (1, 1, 0, 1),
        }
        probes: dict[str, Intervention] = {}
        for index, (role, vector) in enumerate(vectors.items()):
            opaque_vector = tuple(int(v) for v in (self._gauge @ np.asarray(vector, dtype=np.uint8)) % 2)
            opaque_id = hashlib.sha256(
                f"{SEED}:probe:{index}:{opaque_vector}".encode("utf-8")
            ).hexdigest()[:20]
            probes[role] = Intervention(vector, opaque_id, opaque_vector)
        return probes

    def _opaque_state(
        self,
        program: CausalProgram,
        gauge: Sequence[Sequence[int]] | None = None,
    ) -> OpaqueActorState:
        # h = G^{-T} c, while v = G x, so h^T v = c^T x.
        active_gauge = (
            np.asarray(gauge, dtype=np.uint8)
            if gauge is not None
            else self._gauge
        )
        gauge_inverse = _gf2_inverse(active_gauge)
        c = np.asarray(program.coefficients, dtype=np.uint8)
        h = (gauge_inverse.T @ c) % 2
        return OpaqueActorState(program.bias, tuple(int(value) for value in h))

    def _freeze_snapshot(self) -> FrozenSnapshot:
        component_hashes = {
            "actor": _digest(self.reference_programs[0]),
            "candidates": _digest(self._candidate_programs),
            "gauge": _digest(self._gauge),
            "interventions": _digest(self.interventions),
            "observer": self.observer.fingerprint() if self.observer is not None else "absent",
            "receiver": self.receiver.fingerprint(),
            "evaluator": _digest(self.evaluator_id),
            "rng": _digest(self._rng_seed),
            "environment": _digest(self._environment_version),
            "receiver_model_state": _digest(self._reentered_receiver_state),
        }
        snapshot_id = _digest(component_hashes)
        return FrozenSnapshot(
            actor=copy.deepcopy(self.reference_programs[0]),
            candidates=copy.deepcopy(self._candidate_programs),
            gauge=tuple(tuple(int(v) for v in row) for row in self._gauge),
            observer=copy.deepcopy(self.observer),
            receiver=copy.deepcopy(self.receiver),
            evaluator_id=self.evaluator_id,
            rng_seed=self._rng_seed,
            environment_version=self._environment_version,
            interventions=copy.deepcopy(self.interventions),
            reentered_receiver_state=copy.deepcopy(self._reentered_receiver_state),
            snapshot_id=snapshot_id,
            component_hashes=tuple(sorted(component_hashes.items())),
        )

    def _snapshot_opaque_state(self, program: CausalProgram) -> OpaqueActorState:
        return self._opaque_state(program, self._snapshot.gauge)

    @staticmethod
    def _snapshot_checks(snapshot: FrozenSnapshot) -> dict[str, str]:
        return {
            "actor": _digest(snapshot.actor),
            "candidates": _digest(snapshot.candidates),
            "gauge": _digest(snapshot.gauge),
            "interventions": _digest(snapshot.interventions),
            "observer": (
                snapshot.observer.fingerprint()
                if snapshot.observer is not None
                else "absent"
            ),
            "receiver": snapshot.receiver.fingerprint(),
            "evaluator": _digest(snapshot.evaluator_id),
            "rng": _digest(snapshot.rng_seed),
            "environment": _digest(snapshot.environment_version),
            "receiver_model_state": _digest(snapshot.reentered_receiver_state),
        }

    def _validate_internal_snapshot(self) -> None:
        if self._snapshot_checks(self._snapshot) != dict(self._snapshot.component_hashes):
            raise RuntimeError("internal frozen snapshot was mutated")

    def _carrier(self) -> Carrier:
        source = self._snapshot.actor
        interventions = self._snapshot.interventions
        if self.ablation == "no_transport":
            probe = interventions["baseline"]
        else:
            probe = interventions["carrier"]
        return Carrier((CarrierSymbol(probe.vector, source.run(probe).output),))

    def _sender_initial_receiver_model(self, carrier: Carrier) -> ReceiverState:
        # The sender starts with a deliberately wrong finite receiver model.
        # For the informative carrier it selects vermillion; for an
        # uninformative carrier it selects cobalt. The actual S score is still
        # derived prospectively from the model's response profile, never set as
        # a bit by this branch.
        symbol = carrier.symbols[0]
        candidates = self._snapshot.candidates
        if symbol.coordinates == self._snapshot.interventions["carrier"].vector:
            coefficients = candidates[2].coefficients
        else:
            coefficients = candidates[1].coefficients
        return ReceiverState(coefficients, 1, False)

    @staticmethod
    def _effect_profile(state: ReceiverState, probes: Iterable[Intervention]) -> tuple[tuple[str, int], ...]:
        return tuple((probe.opaque_id, state.respond(probe)) for probe in probes)

    def _manifest(
        self, carrier: Carrier, commitment: Commitment, occurrence_id: int
    ) -> dict[str, Any]:
        snap = self._snapshot
        return {
            "snapshot_id": snap.snapshot_id,
            "actor": _digest(snap.actor),
            "candidates": _digest(snap.candidates),
            "gauge": _digest(snap.gauge),
            "interventions": _digest(snap.interventions),
            "observer": snap.observer.fingerprint() if snap.observer is not None else "absent",
            "receiver": snap.receiver.fingerprint(),
            "evaluator": snap.evaluator_id,
            "rng": snap.rng_seed,
            "environment": snap.environment_version,
            "receiver_model_state": _digest(snap.reentered_receiver_state),
            "carrier": _digest(carrier),
            "commitment": _digest(commitment),
            "occurrence_id": occurrence_id,
        }

    @staticmethod
    def _ledger_payload(ledger: AppendOnlyLedger, kind: str) -> Any:
        matches = [entry["payload"] for entry in ledger.entries if entry["kind"] == kind]
        if len(matches) != 1:
            raise ValueError(f"sealed episode must contain exactly one {kind!r} entry")
        return matches[0]

    def _validate_episode_against_prefix(self, episode: Episode) -> None:
        """Reject substituted report fields before recovery can observe them."""

        if not episode.ledger.verify(episode.receipt):
            raise ValueError("recovery rejected: invalid sealed episode prefix")
        if len(episode.ledger.entries) != episode.receipt.entry_count:
            raise ValueError("recovery rejected: unsealed ledger tail or repeated recovery")
        manifest = self._ledger_payload(episode.ledger, "frozen_manifest")
        committed = self._ledger_payload(episode.ledger, "prospective_receiver_commitment")
        carried = self._ledger_payload(episode.ledger, "carrier_emission")
        scored = self._ledger_payload(episode.ledger, "independent_metrics")
        if carried != _plain(episode.carrier):
            raise ValueError("recovery rejected: carrier differs from sealed occurrence")
        if committed != _plain(episode.commitment):
            raise ValueError("recovery rejected: commitment differs from sealed occurrence")
        if scored != _plain(episode.metrics):
            raise ValueError("recovery rejected: metrics differ from sealed occurrence")
        if manifest.get("evaluator") != episode.evaluator_id:
            raise ValueError("recovery rejected: evaluator differs from sealed occurrence")
        if manifest.get("snapshot_id") != episode.snapshot.snapshot_id:
            raise ValueError("recovery rejected: snapshot differs from sealed occurrence")
        component_hashes = dict(episode.snapshot.component_hashes)
        checks = self._snapshot_checks(episode.snapshot)
        if checks != component_hashes:
            raise ValueError("recovery rejected: snapshot components were mutated")
        if {
            "actor": manifest.get("actor"),
            "candidates": manifest.get("candidates"),
            "gauge": manifest.get("gauge"),
            "interventions": manifest.get("interventions"),
            "observer": manifest.get("observer"),
            "receiver": manifest.get("receiver"),
            "evaluator": _digest(manifest.get("evaluator")),
            "rng": _digest(manifest.get("rng")),
            "environment": _digest(manifest.get("environment")),
            "receiver_model_state": manifest.get("receiver_model_state"),
        } != checks:
            raise ValueError("recovery rejected: snapshot does not match sealed manifest")

    def run_sender_blind(self) -> Episode:
        self._validate_internal_snapshot()
        snap = self._snapshot
        source = snap.actor
        interventions = snap.interventions
        observer = snap.observer
        carrier = self._carrier()
        predicted_receiver = self._sender_initial_receiver_model(carrier)
        evaluation_roles = ("evaluation_one", "relevant", "composed")
        evaluation_probes = tuple(interventions[role] for role in evaluation_roles)
        if snap.reentered_receiver_state is not None and observer is not None:
            predicted_profile = tuple(
                (probe.opaque_id, observer.predict(snap.reentered_receiver_state, probe.opaque_id))
                for probe in evaluation_probes
            )
            receiver_model_version = "reentered-native-receiver-model-v2"
        else:
            predicted_profile = self._effect_profile(predicted_receiver, evaluation_probes)
            receiver_model_version = "wrong-finite-receiver-model-v1"
        commitment = Commitment(predicted_profile, receiver_model_version)
        occurrence_id = self._occurrence_counter
        self._occurrence_counter += 1

        manifest = self._manifest(carrier, commitment, occurrence_id)
        ledger = AppendOnlyLedger(_digest(manifest))
        ledger.append("frozen_manifest", manifest)
        commitment_step = ledger.append("prospective_receiver_commitment", commitment)
        ledger.append("carrier_emission", carrier)

        actual_receiver = snap.receiver.consume(carrier)
        receiver_effects = {
            role: actual_receiver.respond(interventions[role])
            for role in ("baseline", "relevant", "irrelevant", "composed")
        }
        source_effects = {
            role: source.run(interventions[role]).output
            for role in ("baseline", "relevant", "irrelevant", "composed")
        }
        first_receiver_observation_step = ledger.append(
            "receiver_hidden_evaluation",
            {
                "effects_by_role": receiver_effects,
                "effects_by_probe": {
                    probe.opaque_id: actual_receiver.respond(probe)
                    for probe in evaluation_probes
                },
            },
        )

        actual_eval_profile = self._effect_profile(actual_receiver, evaluation_probes)
        C = int(all(actual_receiver.respond(p) == source.run(p).output for p in evaluation_probes))
        I = int(
            actual_receiver.respond(interventions["irrelevant"])
            == actual_receiver.respond(interventions["baseline"])
        )
        S = int(predicted_profile == actual_eval_profile)
        metrics = Metrics(C=C, I=I, S=S, R=0)
        ledger.append("independent_metrics", metrics)
        receipt = ledger.seal()
        # The anchor is retained outside the mutable Episode object.  A caller
        # may rewrite a local chain and issue itself a new Receipt, but it
        # cannot replace the engine's original sealed scar.
        session_key = receipt.manifest_hash
        if session_key in self._trusted_receipts:
            raise RuntimeError("duplicate sealed session manifest")
        self._trusted_receipts[session_key] = copy.deepcopy(receipt)

        opaque_state = self._snapshot_opaque_state(source)
        raw_effects = {
            intervention.opaque_id: source.run(intervention).output
            for intervention in interventions.values()
        }
        training_roles = ("baseline", "carrier", "recovery_one", "recovery_two")
        holdout_roles = ("irrelevant", "evaluation_one", "relevant", "composed")
        native_ids = (
            tuple(
                observer.encode(self._snapshot_opaque_state(program)).state_id
                for program in snap.candidates
            )
            if observer is not None
            else ()
        )
        branch_ids = {
            role: self._snapshot.snapshot_id
            for role in ("baseline", "carrier", "relevant", "irrelevant", "composed")
        }
        return Episode(
            metrics=metrics,
            ledger=ledger,
            receipt=receipt,
            carrier=carrier,
            commitment=commitment,
            evaluator_id=snap.evaluator_id,
            receiver_effects=receiver_effects,
            source_effects=source_effects,
            committed_receiver_prediction=predicted_profile,
            commitment_step=commitment_step,
            first_receiver_observation_step=first_receiver_observation_step,
            branch_snapshot_ids=branch_ids,
            frozen_components=("actor", "observer", "receiver", "evaluator", "rng", "environment", "receiver_model_state"),
            snapshot=copy.deepcopy(self._snapshot),
            native_state_ids=native_ids,
            observer_training_intervention_ids=tuple(
                interventions[role].opaque_id for role in training_roles
            ),
            observer_holdout_intervention_ids=tuple(
                interventions[role].opaque_id for role in holdout_roles
            ),
            opaque_actor_state=opaque_state,
            raw_actor_effects=raw_effects,
            actual_receiver_state=actual_receiver,
            evaluation_probe_ids=tuple(probe.opaque_id for probe in evaluation_probes),
        )

    def recover(self, episode: Episode, max_probes: int = 2) -> Recovery:
        trusted = self._trusted_receipts.get(episode.receipt.manifest_hash)
        if trusted != episode.receipt:
            raise ValueError("recovery rejected: receipt is not the external sealed anchor")
        self._validate_episode_against_prefix(episode)
        snap = episode.snapshot
        observer = snap.observer
        ledger = episode.ledger
        recovery_roles = ("recovery_one", "recovery_two")
        recovery_probes = tuple(snap.interventions[role] for role in recovery_roles)
        evaluation_probes = tuple(
            snap.interventions[role]
            for role in ("post_eval_one", "post_eval_two", "post_eval_composed")
        )
        sealed_receiver_state = snap.receiver.consume(episode.carrier)
        can_probe = self.ablation != "no_active_probe" and observer is not None
        candidates = list(snap.candidates)
        probes_used = 0
        used_probes: list[Intervention] = []
        separator_commit_step = -1
        probe_effect_step = -1
        if can_probe:
            remaining_probes = list(recovery_probes)
            while remaining_probes and probes_used < max_probes and len(candidates) > 1:
                # Select from learned anonymous response predictions.  The
                # selector never reads receiver outcomes or program names.
                partitions: list[tuple[int, int, Intervention, tuple[int, ...]]] = []
                for order, candidate_probe in enumerate(remaining_probes):
                    signature = tuple(
                        observer.predict(
                            observer.encode(self._opaque_state(program, snap.gauge)),
                            candidate_probe.opaque_id,
                        )
                        for program in candidates
                    )
                    split_score = min(signature.count(0), signature.count(1))
                    partitions.append((split_score, -order, candidate_probe, signature))
                _, _, probe, signature = max(partitions, key=lambda item: (item[0], item[1]))
                remaining_probes.remove(probe)
                candidate_ids = tuple(
                    observer.encode(self._opaque_state(program, snap.gauge)).state_id
                    for program in candidates
                )
                commit_index = ledger.append(
                    "separator_precommit",
                    {
                        "candidate_native_states": candidate_ids,
                        "selected_probe": probe.opaque_id,
                        "predicted_partition": signature,
                    },
                )
                if separator_commit_step < 0:
                    separator_commit_step = commit_index
                    probe_effect_step = len(ledger.entries)
                observed = sealed_receiver_state.respond(probe)
                predicted = {
                    observer.encode(self._opaque_state(program, snap.gauge)).state_id: observer.predict(
                        observer.encode(self._opaque_state(program, snap.gauge)), probe.opaque_id
                    )
                    for program in candidates
                }
                ledger.append(
                    "receiver_recovery_effect",
                    {"probe": probe.opaque_id, "observed": observed, "predicted": predicted},
                )
                candidates = [
                    program
                    for program in candidates
                    if predicted[
                        observer.encode(self._opaque_state(program, snap.gauge)).state_id
                    ]
                    == observed
                ]
                used_probes.append(probe)
                probes_used += 1
        else:
            separator_commit_step = ledger.append(
                "separator_unavailable_precommit", {"ablation": self.ablation}
            )
            probe_effect_step = len(ledger.entries)
            ledger.append("recovery_unavailable", {"ablation": self.ablation})

        recovered_state: NativeState | None = None
        if len(candidates) == 1 and can_probe:
            recovered_program = candidates[0]
            assert observer is not None
            recovered_state = observer.encode(self._opaque_state(recovered_program, snap.gauge))
            new_predicted_profile = tuple(
                (
                    probe.opaque_id,
                    observer.predict(recovered_state, probe.opaque_id),
                )
                for probe in evaluation_probes
            )
            # Persist the re-entered state only after observing and scoring the
            # separator. Future episodes consume it prospectively.
            self._reentered_receiver_state = recovered_state
            actual_profile = self._effect_profile(sealed_receiver_state, evaluation_probes)
            S_after = int(new_predicted_profile == actual_profile)
            ledger.append(
                "post_reentry_prospective_commitment",
                {"native_state": recovered_state.state_id, "prediction": new_predicted_profile},
            )
            ledger.append("disjoint_post_recovery_evaluation", actual_profile)
            # Recovery is an after-scoring model update. Bind it into a new
            # versioned snapshot for subsequent episodes; the old snapshot and
            # receipt remain unchanged.
            self._snapshot = self._freeze_snapshot()
        else:
            new_predicted_profile = episode.committed_receiver_prediction
            S_after = episode.metrics.S

        R = int(
            episode.metrics.C == 1
            and episode.metrics.S == 0
            and S_after == 1
            and bool(used_probes)
            and set(p.opaque_id for p in used_probes).isdisjoint(
                p.opaque_id for p in evaluation_probes
            )
        )
        after_metrics = Metrics(episode.metrics.C, episode.metrics.I, S_after, R)
        ledger.append("post_recovery_metrics", after_metrics)
        after_receipt = ledger.seal()
        after = replace(
            episode,
            metrics=after_metrics,
            receipt=after_receipt,
            carrier=copy.deepcopy(episode.carrier),
            commitment=copy.deepcopy(episode.commitment),
            evaluator_id=episode.evaluator_id,
            committed_receiver_prediction=new_predicted_profile,
        )
        return Recovery(
            before=episode,
            after=after,
            probes_used=probes_used,
            original_carrier=copy.deepcopy(episode.carrier),
            original_commitment=copy.deepcopy(episode.commitment),
            original_evaluator_id=episode.evaluator_id,
            ledger=ledger,
            separator_commit_step=separator_commit_step,
            probe_effect_step=probe_effect_step,
            recovery_probe_ids=tuple(probe.opaque_id for probe in used_probes),
            evaluation_probe_ids=tuple(probe.opaque_id for probe in evaluation_probes),
            recovered_native_state=recovered_state,
        )

    def reentry_interchange_test(self) -> ReentryInterchangeResult:
        snap = self._snapshot
        observer = snap.observer
        if observer is None:
            raise RuntimeError("native continuation unavailable without self-observer")
        source, rival, third = snap.candidates
        probe = snap.interventions["carrier"]
        source_state = observer.encode(self._opaque_state(source, snap.gauge))
        rival_state = observer.encode(self._opaque_state(rival, snap.gauge))
        third_state = observer.encode(self._opaque_state(third, snap.gauge))
        continuation = NativeContinuation(observer, rival_state)
        baseline = continuation.step(probe.opaque_id)
        continuation.patch(source_state)
        target = continuation.step(probe.opaque_id)

        # Find an equal-Hamming-norm control that preserves the baseline effect.
        norm = sum(source_state.coordinates)
        shuffle_state = third_state
        for coordinates in itertools.product((0, 1), repeat=DIMENSION):
            candidate = NativeState(source_state.bias, tuple(coordinates))
            if (
                sum(coordinates) == norm
                and candidate != source_state
                and observer.predict(candidate, probe.opaque_id) == baseline
            ):
                shuffle_state = candidate
                break
        continuation.patch(third_state)
        reverse = continuation.step(probe.opaque_id)
        continuation.patch(shuffle_state)
        shuffled = continuation.step(probe.opaque_id)
        continuation.patch(rival_state)
        null = continuation.step(probe.opaque_id)
        return ReentryInterchangeResult(
            baseline_output=baseline,
            correct_patch_output=target,
            predicted_target_output=source.run(probe).output,
            reverse_patch_output=reverse,
            equal_norm_shuffle_output=shuffled,
            null_patch_output=null,
        )

    def mutate_live_components_for_test(self) -> None:
        """Mutate every live component; previously frozen snapshots remain pure."""

        self._live_nonce += 1
        self.reference_programs = (
            CausalProgram("mutated-live-actor", (1, 1, 1, 1), 0),
            *self.reference_programs[1:],
        )
        if self.observer is not None:
            self.observer.weights ^= 1
        self.receiver.preference = tuple(reversed(self.receiver.preference))
        self.evaluator_id = "mutated-evaluator"
        self._rng_seed += 1
        self._environment_version = "mutated-environment"
        # A subsequent episode receives a new complete snapshot. Previously
        # returned snapshots remain immutable and independently executable.
        self._candidate_programs = (
            self.reference_programs[0],
            self.reference_programs[1],
            self._candidate_programs[2],
        )
        self._snapshot = self._freeze_snapshot()


def build_reference_engine(ablation: str | None = None) -> NativeOrderEngine:
    """Build a deterministic finite native-order distinction experiment."""

    return NativeOrderEngine(ablation=ablation)
