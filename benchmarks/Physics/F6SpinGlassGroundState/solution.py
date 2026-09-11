"""Legal deterministic baseline for F6SpinGlassGroundState.

The all-plus-one state has energy zero on the fixed instance and therefore defines score zero.
"""
from __future__ import annotations


def solve_ising(problem):
    return [1] * problem["n"]
