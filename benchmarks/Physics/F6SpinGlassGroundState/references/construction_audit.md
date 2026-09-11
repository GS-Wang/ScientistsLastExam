# Public construction controls and fixed-instance boundary

`verification/reference_construction.py` independently enumerates the eight F6 coupling templates,
all 256 local spin states, and disclosed deterministic small control instances. The control's
returned gauge is a positive witness for that newly constructed control only. The same code audits
that each fixed-instance edge lies in one parity cube, each spin lies in two cubes, every vertex has
degree six, and all 432 cubes have minimum -6 with 16 minimizers.

It deliberately does not solve the fixed L=12 instance. The hard instance's attaining vector,
private gauge and generation secret remain outside the repository. Fixed-target attainability was
audited with the external witness described in `known_best.md`; external statistical-physics review
is pending.

Future generators belong outside this package and must keep disclosed instance material separate
from server-held seeds or witnesses. The now-public fixed input is unsuitable for future blind or
anti-contamination claims.
