"""Public-input-only replica-exchange Ising search, with a fixed operation budget.

Independent implementation of standard Metropolis/replica-exchange updates.
No saved spins, planting secret, evaluator import, file access, or instance seed.
Its scientific qualification must be established separately from executability.
"""
import numpy as np


def _graph(problem):
    n, length = problem['n'], problem['L']
    edges = np.asarray(problem['edges'], dtype=np.int64)
    neighbours = [[] for _ in range(n)]
    couplings = [[] for _ in range(n)]
    for u, v, coupling in edges:
        neighbours[int(u)].append(int(v)); couplings[int(u)].append(int(coupling))
        neighbours[int(v)].append(int(u)); couplings[int(v)].append(int(coupling))
    if any(len(row) != 6 for row in neighbours):
        raise ValueError('reference requires the documented degree-six graph')
    indices = np.arange(n)
    parity = ((indices % length) + (indices // length) % length + indices // (length * length)) % 2
    if np.any(parity[edges[:, 0]] == parity[edges[:, 1]]):
        raise ValueError('reference requires the documented bipartite lattice')
    colours = [indices[parity == value] for value in (0, 1)]
    return edges, np.asarray(neighbours), np.asarray(couplings), colours


def _energies(spins, edges):
    return np.sum(spins[:, edges[:, 0]] * spins[:, edges[:, 1]] * edges[None, :, 2], axis=1)


def _quench(spins, neighbours, couplings, colours):
    """Strictly decreasing checkerboard flips; finite termination, no neutral cycling."""
    while True:
        changed = False
        for sites in colours:
            fields = np.sum(spins[:, neighbours[sites]] * couplings[None, sites, :], axis=2)
            flip = spins[:, sites] * fields > 0
            changed = changed or bool(np.any(flip))
            spins[:, sites] *= np.where(flip, -1, 1).astype(np.int8)
        if not changed:
            return spins


def search(problem, replicas=24, sweeps=1024, exchange=True, quench=True, seed=1729):
    edges, neighbours, couplings, colours = _graph(problem)
    rng = np.random.default_rng(seed)
    spins = (2 * rng.integers(0, 2, size=(replicas, problem['n'])) - 1).astype(np.int8)
    betas = 1.0 / np.geomspace(0.35, 3.5, replicas)
    energies = _energies(spins, edges)
    index = int(np.argmin(energies))
    best_energy, best = int(energies[index]), spins[index].copy()
    for sweep in range(sweeps):
        for sites in colours:
            fields = np.sum(spins[:, neighbours[sites]] * couplings[None, sites, :], axis=2)
            delta = -2 * spins[:, sites] * fields
            accept = rng.random(delta.shape) < np.exp(-np.maximum(delta, 0) * betas[:, None])
            spins[:, sites] *= np.where(accept, -1, 1).astype(np.int8)
        energies = _energies(spins, edges)
        index = int(np.argmin(energies))
        if energies[index] < best_energy:
            best_energy, best = int(energies[index]), spins[index].copy()
        if exchange:
            left = np.arange(sweep % 2, replicas - 1, 2)
            right = left + 1
            log_accept = (betas[left] - betas[right]) * (energies[left] - energies[right])
            selected = left[np.log(rng.random(len(left))) < log_accept]
            saved = spins[selected].copy()
            spins[selected] = spins[selected + 1]
            spins[selected + 1] = saved
    if quench:
        best = _quench(best[None, :].copy(), neighbours, couplings, colours)[0]
    return [int(value) for value in best]


def greedy_multistart(problem, restarts=256, seed=1729):
    edges, neighbours, couplings, colours = _graph(problem)
    rng = np.random.default_rng(seed)
    spins = (2 * rng.integers(0, 2, size=(restarts, problem['n'])) - 1).astype(np.int8)
    _quench(spins, neighbours, couplings, colours)
    best = spins[int(np.argmin(_energies(spins, edges)))]
    return [int(value) for value in best]


def solve_ising(problem):
    return greedy_multistart(problem)
