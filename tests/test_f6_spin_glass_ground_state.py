"""Behavioral and attack checks for the bounded F6 spin-glass candidate."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sle.registry import find_task  # noqa: E402

TASK = ROOT / "benchmarks/Physics/F6SpinGlassGroundState"
EXPECTED_INSTANCE_SHA256 = "bcb95c8bcbf1de65b4757f1d83418e8ab3a4d3277f7d6424837c5440faeee4a6"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load %s" % path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


class F6SpinGlassGroundStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evaluator = _load(TASK / "verification/evaluator.py", "f6_oracle")
        cls.reference = _load(
            TASK / "verification/reference_construction.py", "f6_reference"
        )
        cls.baseline = _load(TASK / "solution.py", "f6_baseline")
        cls.instance_bytes = (TASK / "instance.json").read_bytes()
        cls.problem = json.loads(cls.instance_bytes)

    def test_known_small_hamiltonian_energies_use_the_documented_sign_once(self):
        edges = ((0, 1, 1), (1, 2, -1))
        self.assertEqual(self.evaluator._energy([1, 1, 1], edges), 0)
        self.assertEqual(self.evaluator._energy([1, -1, -1], edges), -2)
        self.assertEqual(self.evaluator._energy([-1, 1, 1], edges), -2)

    def test_every_f6_template_has_minimum_minus_six_and_degeneracy_sixteen(self):
        templates = self.reference.f6_templates()
        self.assertEqual(len(templates), 8)
        for couplings in templates:
            energies = [
                self.reference.local_energy(bits, couplings) for bits in range(256)
            ]
            self.assertEqual(min(energies), -6)
            self.assertEqual(energies.count(-6), 16)

    def test_generated_control_has_partition_counts_and_an_attaining_witness(self):
        control, witness = self.reference.build_control_instance(4)
        audit = self.reference.audit_instance_structure(control)
        self.assertEqual(control["n"], 64)
        self.assertEqual(len(control["edges"]), 192)
        self.assertEqual(audit["cube_count"], 16)
        self.assertEqual(audit["cubes_per_vertex"], 2)
        self.assertEqual(audit["edges_per_cube"], 12)
        self.assertEqual(audit["local_minimum"], -6)
        self.assertEqual(audit["local_degeneracy"], 16)
        self.assertEqual(
            self.evaluator._energy(witness, tuple(map(tuple, control["edges"]))), -96
        )

    def test_fixed_asset_fingerprint_structure_and_exact_cube_bound(self):
        self.assertEqual(hashlib.sha256(self.instance_bytes).hexdigest(), EXPECTED_INSTANCE_SHA256)
        self.assertEqual(set(self.problem), {"L", "n", "hamiltonian", "edges"})
        self.assertEqual(self.problem["L"], 12)
        self.assertEqual(self.problem["n"], 1728)
        self.assertEqual(self.problem["hamiltonian"], "sum J_ij*s_i*s_j")
        self.assertEqual(len(self.problem["edges"]), 5184)
        self.assertEqual(len({(u, v) for u, v, _ in self.problem["edges"]}), 5184)
        audit = self.reference.audit_instance_structure(self.problem)
        self.assertEqual(audit["cube_count"], 432)
        self.assertEqual(audit["cubes_per_vertex"], 2)
        self.assertEqual(audit["edges_per_cube"], 12)
        self.assertEqual(audit["local_minimum"], -6)
        self.assertEqual(audit["local_degeneracy"], 16)
        self.assertEqual(audit["summed_cube_lower_bound"], -2592)

    def test_deterministic_all_plus_one_baseline_is_valid_zero(self):
        first = self.evaluator.evaluate(self.baseline.solve_ising)
        second = self.evaluator.evaluate(self.baseline.solve_ising)
        self.assertEqual(first, second)
        self.assertEqual(first["valid"], 1.0)
        self.assertEqual(first["energy"], 0)
        self.assertEqual(first["gap"], 2592)
        self.assertEqual(first["combined_score"], 0.0)
        self.assertFalse(first["ground_state_hit"])

    def test_malformed_candidate_outputs_are_finite_invalid_zero(self):
        cases = {
            "none": None,
            "string": "invalid",
            "tuple": tuple([1] * 1728),
            "zero": [1] * 1727 + [0],
            "minus_two": [1] * 1727 + [-2],
            "short": [1] * 1727,
            "long": [1] * 1729,
            "nan": [1] * 1727 + [float("nan")],
            "infinity": [1] * 1727 + [float("inf")],
            "bool": [1] * 1727 + [True],
            "float": [1] * 1727 + [1.0],
            "huge_integer": [1] * 1727 + [10**1000],
            "claimed_energy": {"spins": [1] * 1728, "energy": -2592},
        }
        for name, payload in cases.items():
            with self.subTest(name=name):
                metrics = self.evaluator.evaluate(lambda _problem, value=payload: value)
                self.assertEqual(metrics["valid"], 0.0)
                self.assertEqual(metrics["combined_score"], 0.0)
                self.assertTrue(math.isfinite(metrics["combined_score"]))

        def raises(_problem):
            raise RuntimeError("candidate-controlled detail")

        metrics = self.evaluator.evaluate(raises)
        self.assertEqual(metrics["valid"], 0.0)
        self.assertEqual(metrics["combined_score"], 0.0)
        self.assertTrue(math.isfinite(metrics["combined_score"]))

    def test_global_spin_reversal_preserves_energy_and_score(self):
        spins = [1 if (i % 5) else -1 for i in range(1728)]
        opposite = [-spin for spin in spins]
        first = self.evaluator.evaluate(lambda _problem: spins)
        second = self.evaluator.evaluate(lambda _problem: opposite)
        self.assertEqual(first["energy"], second["energy"])
        self.assertEqual(first["combined_score"], second["combined_score"])

    def test_candidate_input_mutation_cannot_change_trusted_scoring(self):
        seen = []

        def mutate(problem):
            seen.append(set(problem))
            problem["n"] = 1
            problem["edges"].clear()
            problem["hamiltonian"] = "candidate claim"
            problem["lower_bound"] = -10**9
            return [1] * 1728

        attacked = self.evaluator.evaluate(mutate)
        clean = self.evaluator.evaluate(self.baseline.solve_ising)
        self.assertEqual(seen, [{"L", "n", "hamiltonian", "edges"}])
        self.assertEqual(attacked["energy"], 0)
        self.assertEqual(attacked["gap"], 2592)
        self.assertEqual(attacked["combined_score"], 0.0)
        self.assertEqual(attacked, clean)

    def test_an_energy_below_the_proved_bound_is_never_accepted(self):
        metrics = self.evaluator._metrics_for_energy(-2594)
        self.assertEqual(metrics["valid"], 0.0)
        self.assertEqual(metrics["combined_score"], 0.0)
        self.assertFalse(metrics["ground_state_hit"])

    def test_instance_reader_rejects_corruption_and_oversize_before_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "instance.json"
            path.write_bytes(self.instance_bytes + b" ")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                self.evaluator._read_instance(path, EXPECTED_INSTANCE_SHA256)

            path.write_bytes(b"x" * (self.evaluator.MAX_INSTANCE_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "size limit"):
                self.evaluator._read_instance(path, EXPECTED_INSTANCE_SHA256)

    def test_public_mount_contract_exposes_instance_but_not_verification(self):
        spec = find_task("Physics/F6SpinGlassGroundState", include_uncertified=True)
        self.assertEqual(
            spec.agent_files,
            ["Task.md", "solution.py", "instance.json", "frontier_eval/constraints.txt"],
        )
        for relative in spec.agent_files:
            self.assertTrue((spec.task_dir / relative).is_file(), relative)
        self.assertFalse(any(path.startswith("verification/") for path in spec.agent_files))
        self.assertFalse(any(path.startswith("references/") for path in spec.agent_files))

    def test_import_and_evaluation_do_not_write_into_the_task_package(self):
        before = _tree_digest(TASK)
        self.evaluator.evaluate(self.baseline.solve_ising)
        after = _tree_digest(TASK)
        self.assertEqual(before, after)


class PublicMethodControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = _load(TASK / 'verification/reference_tempering.py', 'f6_tempering')
        construction = _load(TASK / 'verification/reference_construction.py', 'f6_controls')
        cls.problem, _ = construction.build_control_instance(4)

    def test_vector_energy_and_checkerboard_quench_match_independent_edge_sum(self):
        import numpy as np
        problem = self.problem
        edges, neighbours, couplings, colours = self.reference._graph(problem)
        spins = np.array([[1 if (i * 17 + j) % 5 else -1 for i in range(problem['n'])]
                          for j in range(3)], dtype=np.int8)
        before = self.reference._energies(spins, edges)
        expected = [sum(j * int(row[u]) * int(row[v]) for u, v, j in problem['edges'])
                    for row in spins]
        self.assertEqual(before.tolist(), expected)
        self.reference._quench(spins, neighbours, couplings, colours)
        after = self.reference._energies(spins, edges)
        self.assertTrue(np.all(after <= before))
        self.assertTrue(np.all(after >= -96))
        fields = np.sum(spins[:, neighbours] * couplings[None, :, :], axis=2)
        self.assertTrue(np.all(-2 * spins * fields >= 0))

    def test_replica_search_is_per_call_deterministic_and_returns_only_legal_spins(self):
        import numpy as np
        first = self.reference.search(self.problem, replicas=6, sweeps=8)
        np.random.seed(99)
        np.random.random(1000)
        second = self.reference.search(self.problem, replicas=6, sweeps=8)
        self.assertEqual(first, second)
        self.assertEqual(len(first), self.problem['n'])
        self.assertTrue(all(type(value) is int and value in (-1, 1) for value in first))

    def test_each_standalone_variant_changes_only_its_entrypoint_invocation(self):
        source = (TASK / 'verification/reference_tempering.py').read_text()
        for filename, replacement in (
            ('probe_greedy_multistart.py', '    return greedy_multistart(problem)\n'),
            ('ablation_no_exchange.py', '    return search(problem, exchange=False)\n'),
            ('ablation_no_quench.py', '    return search(problem, quench=False)\n'),
        ):
            with self.subTest(filename=filename):
                self.assertEqual((TASK / 'verification' / filename).read_text(),
                                 source.replace('    return search(problem)\n', replacement))


if __name__ == "__main__":
    unittest.main()
