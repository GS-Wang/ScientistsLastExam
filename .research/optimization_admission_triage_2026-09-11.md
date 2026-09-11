# Optimization admission triage: PR47 / PR56 / PR57

2026-09-11. This is source review and a bounded repair branch, not permission to certify or merge a scientifically incomplete task. The review baseline is main `3069479717c2d0db0b040babb42390bdcbb60cb1`; contributor requirements A–F and `docs/task_admission_workflows.md` govern this review.

| PR and pinned source | Decision | Concrete scientific blockers |
|---|---|---|
| [47 F6SpinGlassGroundState](https://github.com/Geniusyingmanji/ScientistsLastExam/tree/30501b1ab634b82b8a45adec7cddbb47baaf67d8/benchmarks/Physics/F6SpinGlassGroundState) | Selected for bounded repair, admission blocked | Original `reference_construction.py` explicitly does not solve the fixed L12 instance; private attaining witness is an anchor audit, not a truth-blind candidate method. No executable shortcut contract, capability ablations, or formal SLE first-proposal draw. The static Astra artifact near 0.9923 is explicitly exploratory and cannot be relabelled calibration. |
| [56 FootballPoolCovering](https://github.com/Geniusyingmanji/ScientistsLastExam/tree/d262d530332dfa1d8971c4cb54369de88aebdb6c/benchmarks/Mathematics/FootballPoolCovering) | Hold | Data-free greedy diagnostics 0.183–0.197 are far below the attributed public-code reconstruction at 0.687021. The latter is lookup, not an independent reference. Strong reference, meaningful capability ablations and frontier draw are absent; cited lower bounds may not be attainable. |
| [57 SortingNetworkSize](https://github.com/Geniusyingmanji/ScientistsLastExam/tree/43736d7727f94667b0a735ff6246b4d39c9cdbf9/benchmarks/ComputerScience/SortingNetworkSize) | Hold | Author explicitly records no qualifying independent reference: prefix search 0.016667 vs public network lookup 0.496667. Removing uphill acceptance does not change the result; competitive reference, effective ablations and frontier draw remain absent. Lower-bound target attainability is unresolved. |

#47 has a particularly direct exact integer objective, an exhaustive local F6 bound audit and independent small-instance positive controls. This makes its engineering contract the most tractable of the three; it does not make its difficulty evidence adequate. The merge retains the contributor head as an ancestor and preserves main's framework fixes.

Repairs replace the legacy score-writing wrapper with the shared standard-library launcher, preserve the explicit 600-second budget and private full-metric opt-in, add the task's fixed-combinatorial category to generated README counts, and document nearest task distinctions. A new independently written fixed-budget replica-exchange method reads only the public graph; its scientific qualification remains pending. A 256-start strict-descent probe and exact source-matched no-exchange/no-quench ablations are standalone candidates. No private witness or saved spin vector is embedded. The task's instance, energy oracle and normalization remain unchanged.

At the implementation freeze the task card declared the executable shortcut contract with **null expected scores** and a pre-measurement relative margin 0.1. Null was not passed. The subsequent fixed measurements below establish execution but reveal insufficient separation. Post-measurement declarations record those observations and keep the original margin.

Original candidate malformed-output tests cover more than ten forms, and the underlying main wrapper tests apply to the repaired launcher. The full Frontier-Eng paper appendix comparison is still outstanding: the current repository task catalog was inspected, but the prior local appendix PDF is unavailable in this workspace. No complete novelty-clearance claim is made. Formal first-proposal calibration and external physics review also remain outstanding.

Method basis: [Hukushima–Nemoto exchange Monte Carlo](https://arxiv.org/abs/cond-mat/9512035), with a fresh independent implementation; task-family basis: [Hamze et al. F6 planting](https://arxiv.org/abs/1711.04083). These sources support method/family semantics, not this fixed instance's unmeasured model difficulty.

## Fixed Linux qualification result

Source `13a3dfb3f6aaf5076b3a2e003a1ac7e1c1a80edc` passed 148 targeted Linux tests with no
skips. The fixed driver then made exactly ten task evaluations, zero model calls and no
parameter search. All ten were valid, all five pairs had identical full metrics, and source
hashes were unchanged. Public evidence is in `pr47_method_qualification_2026-09-11.json`.

| Fixed method | Energy | Combined score | Gap to exact target | Effect vs full method |
|---|---:|---:|---:|---|
| All-plus baseline | 0 | 0 | 2592 | Baseline |
| Replica exchange, 24 temperatures, 1024 sweeps | -2556 | 0.9861111111111112 | 36 | Method candidate |
| Greedy strict descent, 256 starts | -2048 | 0.7901234567901234 | 544 | Lower-cost probe |
| No exchange, independent temperature chains | -2552 | 0.9845679012345679 | 40 | Drops only 4 energy units / 0.0015432098765432 score |
| No final quench | -2556 | 0.9861111111111112 | 36 | No measured effect |

The initial greedy-only margin is insufficient. The no-exchange alternative is now included
in the numeric shortcut declaration with its actual measured score, so the original 10%
separation requirement fails (threshold 0.8875). No-quench is an ineffective ablation. The
original exploratory Astra static result 0.9922839506172839 also exceeds this new method,
although it cannot be treated as a formal calibration. These are **C blockers**, not grounds
to weaken the probe, retune the normalization or relabel the static artifact. A and D remain
incomplete as described above. No new model draw is warranted on a claimed passing reference.

Decision: deliver the engineering repairs and negative qualification evidence on the separate
review branch; **hold PR47 admission**, as well as PR56 and PR57. A future materially revised
scientific method or contract needs its own fixed plan and new evidence. None of these tasks
is promoted or certified by this review. Card/document result recording follows the pilot
and is a separate commit; pilot source and task-package hashes retain their original values.
