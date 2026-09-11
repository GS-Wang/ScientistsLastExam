# Fixed target and score anchor

The exact target is `H=-2592`, not a public record. The fixed public L=12 graph decomposes into
432 edge-disjoint F6 cubes. Exhaustive enumeration of 256 assignments for each F6 coupling class
gives local minimum -6 and degeneracy 16, hence `H >= 432*(-6) = -2592`.

Attainability was checked before the exploratory solver dispatch using a separately held private
witness. Its JSON-content SHA-256 is
`dc0b9f5a6315c2ba591e45aaaa436be98916395c1d7b8d359f6ad6bb98602748`; independent exact integer
evaluation gave -2592. The hash records provenance but does not itself prove content or energy.
For a maintainer audit, obtain that witness outside the repository, verify its content hash, require
1728 literal integer ±1 entries, and recompute the energy against `instance.json`. The evaluator
does not require, load or expose it.

A separate H200 host running Python 3.10.12 and standard-library integer arithmetic independently
rehashed the external witness to the same value and recomputed energy -2592, gap 0. This was
static-data verification only: no candidate program ran and it does not certify the evaluation
sandbox or substitute for external statistical-physics review.

The all-plus-one state has energy 0. A valid energy E scores
`max(0,(0-E)/(0-(-2592)))`, with an upper limit of 1 justified by the cube lower bound. Raw energy,
gap and exact hit remain separate. This is a bounded fixed-instance candidate, not an uncapped
record task.

Primary source: Hamze et al., *From Near to Eternity: Spin-glass planting, tiling puzzles, and
constraint satisfaction problems*, Phys. Rev. E 97, 043303 (2018), DOI
`10.1103/PhysRevE.97.043303`, arXiv:`1711.04083`. The local construction is independently
implemented; no Chook code is copied and no license grant for Chook is assumed.

## 1. Truth-blind method candidate

`verification/reference_tempering.py` is a fresh implementation of Metropolis updates on the
public bipartite graph with 24 temperatures and 1024 sweeps, adjacent replica exchange and a
final strict local quench. It uses only `problem`, a per-call fixed random generator, and the
public integer energy; there is no evaluator import, saved spin vector or file access.
The method basis is [Hukushima and Nemoto](https://arxiv.org/abs/cond-mat/9512035).
Its finite search leaves an observed energy gap of 36. That gap is an observation, not evidence
of deliberate scientifically justified headroom or of a fully qualified reference.

## 2. Baseline

The shipped all-plus candidate scores exactly zero, with energy 0. Both Linux runs reproduce
that result. No invalid candidate was used to establish the shortcut comparison.

## 3. Capability ablations

| Fixed method | Energy | Combined score | Gap to exact target | Effect vs full method |
|---|---:|---:|---:|---|
| All-plus baseline | 0 | 0 | 2592 | Baseline |
| Replica exchange, 24 temperatures, 1024 sweeps | -2556 | 0.9861111111111112 | 36 | Method candidate |
| Greedy strict descent, 256 starts | -2048 | 0.7901234567901234 | 544 | Lower-cost probe |
| No exchange, independent temperature chains | -2552 | 0.9845679012345679 | 40 | Drops only 4 energy units / 0.0015432098765432 score |
| No final quench | -2556 | 0.9861111111111112 | 36 | No measured effect |

The no-exchange candidate is the same source except for its entrypoint argument. Its high score
is a substantive limitation: most of the observed result comes from independent fixed-temperature
Metropolis chains. Removing final quench changes no reported metric. This zero-effect stage is
not credited as a useful capability, and the two ablations do not establish an adequate ladder.

## 4. Shortcut probes and admission decision

The 256-start greedy descent is separated from the full method by the pre-measurement 0.1
relative margin. The stronger no-exchange program, frozen before any pilot evaluation, is now
also declared as a shortcut candidate. Its 0.9845679012345679 exceeds the unchanged threshold
`0.9861111111111112 * 0.9 = 0.8875`; consequently the shortcut separation condition fails.
Expected scores are measured declarations, not a passing gate or a certified reference.

This was a fixed five-program, two-repeat pilot, not the hundreds-to-thousands search required
by CONTRIBUTING item 12. No parameter grid or heldout-based selection occurred. Nothing here
establishes model difficulty; the strong generic near-optimum is a reason to retain the task
on this review branch rather than admit it on the strength of a weaker probe.

## 5. Frontier draw

There are zero new model calls. The original separately held Astra static artifact at energy
-2572 / score 0.9922839506172839 remains exploratory and is not a SLE first-proposal run. It
already exceeds the new method candidate, which further prevents claiming that the method is
an adequate admission threshold without stronger evidence. No model routing, run ID or draw
was invented, and `calibration_evidence_status` remains `missing`.

## 6. Construction errors and repairs

The old wrapper caught evaluator errors and wrote a sentinel score. The repair uses the shared
standard-library launcher with explicit task ID, 600-second timeout and private full-metric
opt-in. Generated inventory counts now include the fixed-combinatorial category while
preserving main's tasks and framework fixes. The original graph, integer oracle, score anchor
and private witness provenance were not changed. The private witness was not accessed or
regraded during this repair.

## 7. Robustness, provenance and unresolved scope

All five programs were evaluated twice on clean Linux source
`13a3dfb3f6aaf5076b3a2e003a1ac7e1c1a80edc`, with runtime source SHA-256
`8159a99d54894dd304e3ac48956cd05d4389f12a041f5d5d86a2c079641c2c86`, Python 3.8.10,
NumPy 1.24.4 and SciPy 1.10.1, thread counts one. Every run was valid and all five complete
metric pairs were identical. Task/runtime/candidate source hashes were unchanged throughout.
The public scalar aggregate is `.research/pr47_method_qualification_2026-09-11.json`; the
fixed driver is `.research/audit_pr47_methods_2026-09-11.py`. Full metric originals are retained
in a separate access-restricted directory, outside the checkout. No raw spins or credentials
are published in that aggregate.

At that same source revision, 148 targeted Linux tests passed with no skips, including task
math and malformed controls, inventory, taxonomy, task cards and shared wrapper/sandbox tests.
This was not the repository's entire test suite. Post-measurement edits record results and
add the strong alternative to the declaration; they are not a rerun at a new package hash.
A full Frontier-Eng paper-appendix comparison, independent domain review, adequate capability
ladder and actual first-proposal calibration are still missing. All these limitations remain
visible; the candidate is not certified and is not recommended for main admission yet.
