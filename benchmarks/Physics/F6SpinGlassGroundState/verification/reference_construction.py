"""Independent public F6-family construction and positive controls.

This module demonstrates attainability for newly generated deterministic controls.  It does not
contain the private witness, gauge, seed, or a solver for the fixed L=12 benchmark instance.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product

LOCAL_EDGES = tuple(
    (vertex, vertex ^ (1 << axis))
    for vertex in range(8)
    for axis in range(3)
    if not vertex & (1 << axis)
)
LOCAL_FACES = tuple(
    tuple(
        index
        for index, (u, v) in enumerate(LOCAL_EDGES)
        if ((u >> axis) & 1) == side and ((v >> axis) & 1) == side
    )
    for axis in range(3)
    for side in (0, 1)
)


def local_energy(bits: int, couplings) -> int:
    return sum(
        coupling * (1 if ((bits >> u) & 1) == ((bits >> v) & 1) else -1)
        for (u, v), coupling in zip(LOCAL_EDGES, couplings)
    )


def f6_templates() -> tuple[tuple[int, ...], ...]:
    """Enumerate the eight three-positive-edge patterns frustrating all six faces."""
    templates = []
    for positive in combinations(range(12), 3):
        if all(sum(index in positive for index in face) % 2 == 1 for face in LOCAL_FACES):
            templates.append(tuple(1 if index in positive else -1 for index in range(12)))
    return tuple(templates)


def cubes(length: int) -> tuple[tuple[int, ...], ...]:
    if type(length) is not int or length < 4 or length % 2:
        raise ValueError("length must be an even integer at least four")

    def vertex(x: int, y: int, z: int) -> int:
        return (x % length) + length * (y % length) + length * length * (z % length)

    return tuple(
        tuple(
            vertex(x + (bits & 1), y + ((bits >> 1) & 1), z + ((bits >> 2) & 1))
            for bits in range(8)
        )
        for x, y, z in product(range(length), repeat=3)
        if x % 2 == y % 2 == z % 2
    )


def build_control_instance(length: int = 4) -> tuple[dict, list[int]]:
    """Build a small disclosed deterministic F6 control together with its witness."""
    templates = f6_templates()
    n = length**3
    gauge = [1 if ((index * 17 + index // 3 + 5) % 7) < 4 else -1 for index in range(n)]
    edge_map = {}
    for cube_index, vertices in enumerate(cubes(length)):
        couplings = templates[cube_index % len(templates)]
        for (a, b), coupling in zip(LOCAL_EDGES, couplings):
            u, v = sorted((vertices[a], vertices[b]))
            if (u, v) in edge_map:
                raise AssertionError("cube edge partition overlaps")
            edge_map[u, v] = coupling * gauge[u] * gauge[v]
    problem = {
        "L": length,
        "n": n,
        "hamiltonian": "sum J_ij*s_i*s_j",
        "edges": [[u, v, coupling] for (u, v), coupling in sorted(edge_map.items())],
    }
    return problem, gauge


def audit_instance_structure(problem: dict) -> dict:
    """Independently verify the cube partition and local F6 lower bound."""
    length = problem["L"]
    n = problem["n"]
    edge_map = {}
    degree = Counter()
    for u, v, coupling in problem["edges"]:
        key = tuple(sorted((u, v)))
        if key in edge_map or coupling not in (-1, 1):
            raise ValueError("invalid or duplicate edge")
        edge_map[key] = coupling
        degree.update(key)

    memberships = Counter()
    used_edges = Counter()
    local_minima = []
    local_degeneracies = []
    for vertices in cubes(length):
        memberships.update(vertices)
        couplings = []
        for a, b in LOCAL_EDGES:
            key = tuple(sorted((vertices[a], vertices[b])))
            if key not in edge_map:
                raise ValueError("cube edge missing")
            used_edges[key] += 1
            couplings.append(edge_map[key])
        energies = [local_energy(bits, couplings) for bits in range(256)]
        minimum = min(energies)
        local_minima.append(minimum)
        local_degeneracies.append(energies.count(minimum))

    if set(edge_map) != set(used_edges) or set(used_edges.values()) != {1}:
        raise ValueError("edges do not form a disjoint cube partition")
    if len(memberships) != n or set(memberships.values()) != {2}:
        raise ValueError("each vertex must belong to exactly two cubes")
    if len(degree) != n or set(degree.values()) != {6}:
        raise ValueError("periodic cubic degree must be six")
    if set(local_minima) != {-6} or set(local_degeneracies) != {16}:
        raise ValueError("cube is not in the F6 family")
    return {
        "cube_count": len(local_minima),
        "cubes_per_vertex": 2,
        "edges_per_cube": len(LOCAL_EDGES),
        "local_minimum": -6,
        "local_degeneracy": 16,
        "summed_cube_lower_bound": sum(local_minima),
    }
