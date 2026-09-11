# Exploratory difficulty evidence

The public task packet and exact target were frozen before one `gpt-6-astra` xhigh static-artifact
probe. It returned a valid 1728-spin vector at energy -2572, gap 20, score approximately 0.9923;
422 cubes were at -6 and 10 at -4. The controller independently recomputed that energy.
The frozen result artifact SHA-256 is
`8c5b3da6114765054b8aff3ba07fba322ed3931ec8f2683b425ef2f5dd723ec3`; a separate H200 host
running Python 3.10.12 and standard-library integer arithmetic independently reproduced energy
-2572 and gap 20 from that artifact.

This was one rough instruction-scoped probe, not formal SLE calibration, a compiler or harness run,
a success-rate estimate, secure filesystem isolation, or evidence of general computational
hardness. A near-one score is a very strong approximation; the only screen criterion it missed was
exact attainment. The fixed instance and target were not resampled or changed afterward. Formal
calibration evidence is absent and lifecycle freezing has not occurred.
