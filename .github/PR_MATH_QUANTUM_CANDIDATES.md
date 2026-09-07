# Three math and quantum candidate resources

This contribution adds `Mathematics/ChowlaCosineCertificate`,
`QuantumFoundations/MutuallyUnbiasedBases6`, and `QuantumFoundations/DephrasureCodeDesign`.
All remain candidates. Their scientific objectives, normalization anchors and verification
algorithms are unchanged by the packaging review corrections.

## Reference scores and what they mean

The following trusted local recomputation used Python 3.12.14, NumPy 2.2.6, SciPy 1.18.1
and SymPy 1.14.0 on macOS on 2026-09-08. Every baseline and reference was valid; repeated
reference evaluation returned exactly the same metrics on that runtime. These are construction
checks, not Linux candidate-program execution or formal model calibration.

| Task | Baseline | Reference combined score | Existing reference callable |
|---|---:|---:|---|
| ChowlaCosineCertificate | 0 | 1.000000000000 | `reference_search.sidon_certificate(problem)` |
| MutuallyUnbiasedBases6 | 0 | 1.000000000000 | `reference_bases.reference_submission(bits=32)` |
| DephrasureCodeDesign | 0 | 0.9999999999974902 (approximately 1) | `reference_codes.design_reference(problem)` |

These references are the public constructions used to define the score scale. They are not
new records or independently calibrated difficulty thresholds. Chowla's default 128-proposal
`search_certificate(problem)` scored 1.0059739799242593 in the same check, above its cheap Sidon
anchor. MUB6 returned `beyond_published_reference=false`; recovering or refining the rational
fixture is not an improvement over the paper. Dephrasure's small deviation from one is numerical
recomputation of the finite witness envelope, not a change in that envelope.

The reference modules have specialized APIs, so the following recipe explicitly adapts their
existing callables to the public evaluator contracts. It does not run untrusted submitted code.
Run from the repository root in the trusted development/test environment:

```sh
python - <<'PY'
import importlib.util
from pathlib import Path

def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

tasks = [
    ("Mathematics/ChowlaCosineCertificate", "reference_search", "build_certificate", "sidon_certificate"),
    ("Physics/MutuallyUnbiasedBases6", "reference_bases", "build_bases", "reference_submission"),
    ("Physics/DephrasureCodeDesign", "reference_codes", "design_code", "design_reference"),
]
for directory, reference_name, entrypoint, constructor in tasks:
    task = Path("benchmarks") / directory
    evaluator = load(task / "verification/evaluator.py")
    reference = load(task / "verification" / (reference_name + ".py"))
    baseline = load(task / "solution.py")
    construct = getattr(reference, constructor)
    adapted = (lambda problem: construct(bits=32)) if constructor == "reference_submission" else construct
    base_metrics = evaluator.evaluate(getattr(baseline, entrypoint))
    ref_metrics = evaluator.evaluate(adapted)
    assert ref_metrics == evaluator.evaluate(adapted)
    assert base_metrics["valid"] == ref_metrics["valid"] == 1.0
    print(directory, "baseline", base_metrics["combined_score"], "reference", ref_metrics["combined_score"])
PY
```

## Dependency boundary

SymPy is required only by the independent algebra checks in the Chowla and MUB6 tests. The
trusted oracles and candidate programs do not require it. CI keeps NumPy, SciPy, PyYAML and
pytest in the system interpreter as upstream does, installs SymPy in a test virtual environment
under `RUNNER_TEMP`, and runs the parent test suite there. A real `CandidateProxy` check verifies
that a default sandbox candidate still sees NumPy and SciPy and cannot import SymPy. The existing
per-task dependency allowlist is unchanged; these three tasks request no additional packages.

## Review scope and remaining evidence

`ShannonCapacityConstruction` was removed because the merged `InformationTheory/ShannonCapacityCertificate`
already covers its C7 instance. The binary septuple annex was removed following the maintainer's
scope decision. Their source remains recoverable from the earlier Git history.

The three retained tasks still need formal SLE calibration, external scientific review and
measured sustained headroom. Local tests and reference recomputation do not replace Linux
sandbox execution. The contributor does not regenerate maintainer-owned global frozen evidence.
