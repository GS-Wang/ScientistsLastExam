# Three-dimensional F6 spin-glass ground-state search

Find a ground-state spin configuration of the supplied nearest-neighbour Ising Hamiltonian on a
periodic cubic lattice. This is one fixed candidate instance from a scalable planted family, not
real experimental spin data and not an open-record or infinite-improvement claim.

## Function and public input

Implement:

```python
def solve_ising(problem) -> list[int]:
    ...
```

Return a flat Python list of exactly 1728 literal integers, each `-1` or `+1`. The callable does
not return a dictionary. A static research artifact may wrap the same vector as `{"spins": [...]}`;
that wrapper is not the callable contract. Booleans, floats, non-finite values, wrong lengths,
extra dictionaries and claimed energies are invalid.

`problem` is a fresh in-memory copy of the public `instance.json` and has exactly four keys:

- `L`: integer 12;
- `n`: integer 1728;
- `hamiltonian`: the string `sum J_ij*s_i*s_j`;
- `edges`: 5184 triples `[u, v, J]`, where `0 <= u < v < n` and `J` is `-1` or `+1`.

Vertex `(x,y,z)` has index `x + L*y + L*L*z`, with coordinates reduced modulo `L`. Minimize

`H(s) = sum(J * s[u] * s[v] for u, v, J in problem["edges"])`.

There is no leading minus sign and every undirected edge is stored once.

## Exact bound and score

The all-`+1` baseline has energy 0. The exact attainable lower bound is -2592. For a valid spin
vector with energy `E`,

`combined_score = max(0, (0 - E) / (0 - (-2592)))`,

with the physical bound enforcing an upper limit of 1. The evaluator separately reports exact
integer `energy`, `gap = E - (-2592)`, and `ground_state_hit`. A well-formed approximation is valid
even when it misses the ground state; values below the proved bound are rejected, and candidate
claims about their own score or energy are ignored.

## Structure available to exploit

The edges partition into 432 unit cubes whose lower-corner coordinates have equal parity. Every
edge belongs to one cube and every spin to two cubes. Each cube is gauge-equivalent to an F6 tile:
all six square faces are frustrated, its exact minimum is -6, and it has 16 minimizing assignments.
The local bounds sum to `432 * -6 = -2592`, and a private witness was independently checked to
attain them simultaneously. That witness, its gauge and generation secret are not part of this
package.

The construction follows Hamze et al., *From Near to Eternity: Spin-glass planting, tiling puzzles,
and constraint satisfaction problems*, Phys. Rev. E 97, 043303 (2018), DOI
`10.1103/PhysRevE.97.043303`, arXiv:`1711.04083`. This repository copies no Chook source code.

## Rules and boundary

- Only edit `solution.py`; keep `solve_ising(problem)` and return the flat list.
- Deterministic CPU code. The standard library, NumPy and SciPy are available; no network or
  subprocesses are available in evaluation.
- Do not read `verification/`, `frontier_eval/` or `references/`.
- The fixed input is now public and is not an anti-contamination guarantee. A future formal blind
  run requires a fresh server-held instance; hiding an answer file alone would not provide secure
  isolation.

This package is a candidate. Its fixed-instance attainability was audited privately, while
external statistical-physics review and formal SLE calibration remain pending.
