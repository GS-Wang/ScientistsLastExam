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
