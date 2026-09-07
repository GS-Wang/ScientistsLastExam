"""Trusted deterministic evaluator for the fixed L=12 F6 Ising candidate.

The public instance is hash-bound before parsing and converted to immutable tuples.  A fresh
JSON-shaped copy is passed to the candidate; scoring always uses the trusted tuples, so mutation
of the candidate payload cannot change the objective or the exact lower bound.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

INSTANCE_PATH = Path(__file__).resolve().parents[1] / "instance.json"
INSTANCE_SHA256 = "bcb95c8bcbf1de65b4757f1d83418e8ab3a4d3277f7d6424837c5440faeee4a6"
MAX_INSTANCE_BYTES = 128 * 1024
EXPECTED_L = 12
EXPECTED_N = 1728
EXPECTED_EDGE_COUNT = 5184
HAMILTONIAN = "sum J_ij*s_i*s_j"
BASELINE_ENERGY = 0
LOWER_BOUND = -2592


def _is_literal_int(value) -> bool:
    return type(value) is int


def _read_instance(path: Path = INSTANCE_PATH, expected_sha256: str = INSTANCE_SHA256) -> dict:
    """Read a bounded, hash-pinned public instance and validate its complete schema."""
    path = Path(path)
    size = path.stat().st_size
    if size > MAX_INSTANCE_BYTES:
        raise ValueError("instance exceeds size limit")
    raw = path.read_bytes()
    if len(raw) != size or hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("instance SHA-256 mismatch")
    problem = json.loads(raw)
    if not isinstance(problem, dict) or set(problem) != {"L", "n", "hamiltonian", "edges"}:
        raise ValueError("instance has unexpected public keys")
    if (not _is_literal_int(problem["L"]) or problem["L"] != EXPECTED_L
            or not _is_literal_int(problem["n"]) or problem["n"] != EXPECTED_N
            or problem["hamiltonian"] != HAMILTONIAN):
        raise ValueError("instance header mismatch")
    edges = problem["edges"]
    if not isinstance(edges, list) or len(edges) != EXPECTED_EDGE_COUNT:
        raise ValueError("instance edge count mismatch")
    seen = set()
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 3:
            raise ValueError("malformed edge")
        u, v, coupling = edge
        if not all(_is_literal_int(value) for value in edge):
            raise ValueError("edge entries must be literal integers")
        if not (0 <= u < v < EXPECTED_N) or coupling not in (-1, 1):
            raise ValueError("edge value outside the fixed contract")
        if (u, v) in seen:
            raise ValueError("duplicate edge")
        seen.add((u, v))
    return problem


_INSTANCE = _read_instance()
_TRUSTED_EDGES = tuple(tuple(edge) for edge in _INSTANCE["edges"])


def _public_problem() -> dict:
    """Return the exact documented payload as a fresh candidate-owned object."""
    return {
        "L": EXPECTED_L,
        "n": EXPECTED_N,
        "hamiltonian": HAMILTONIAN,
        "edges": [list(edge) for edge in _TRUSTED_EDGES],
    }


def _energy(spins, edges=_TRUSTED_EDGES) -> int:
    """Evaluate H=sum J*s[u]*s[v], with each stored edge counted exactly once."""
    return sum(coupling * spins[u] * spins[v] for u, v, coupling in edges)


def _invalid(failure_kind: str) -> dict:
    return {
        "combined_score": 0.0,
        "valid": 0.0,
        "ground_state_hit": False,
        "failure_kind": failure_kind,
    }


def _metrics_for_energy(energy: int) -> dict:
    """Normalize an already validated exact energy and fail closed below the proved bound."""
    if not _is_literal_int(energy) or energy < LOWER_BOUND:
        return _invalid("energy_below_proved_bound")
    progress = (BASELINE_ENERGY - energy) / (BASELINE_ENERGY - LOWER_BOUND)
    score = min(1.0, max(0.0, float(progress)))
    return {
        "combined_score": score,
        "valid": 1.0,
        "energy": energy,
        "gap": energy - LOWER_BOUND,
        "ground_state_hit": energy == LOWER_BOUND,
        "baseline_energy": BASELINE_ENERGY,
        "lower_bound": LOWER_BOUND,
    }


def evaluate(solve_ising) -> dict:
    try:
        spins = solve_ising(_public_problem())
    except Exception:  # noqa: BLE001 - candidate failure is a finite invalid result
        return _invalid("candidate_raised")
    if not isinstance(spins, list) or len(spins) != EXPECTED_N:
        return _invalid("malformed_shape")
    if any(not _is_literal_int(spin) or spin not in (-1, 1) for spin in spins):
        return _invalid("non_literal_spin")
    return _metrics_for_energy(_energy(spins))
