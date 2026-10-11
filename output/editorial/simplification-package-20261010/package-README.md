# Compact proof package

The original manuscript is 41 pages after the certificate appendices are included. The compact LaTeX presentation in `planar_recoloring_hamilton_thresholds_compact.tex` is 28 pages and compiles with `pdflatex` (two passes). It keeps the arbitrary-order induction in the article and moves literal finite state words out of the article.

The four replacement fragments have different status:

- `path232_structural_replacement.tex` is a genuine structural replacement for the 14/17/16-state `(2,3,2)` cycles. It constructs them from small rook-graph layer cycles and switches. `check_path232_structural.py` checks the expanded cycles for coverage and one-coordinate adjacency. `check_rook_splice.py` records the four exceptional endpoint orbits and verifies their short paths.
- `adjacent_pair_compact_lemma.tex` is the proposed rook-fibre replacement for the 53 endpoint words. Its interface-exit argument is explicit. The row/column splice proof of edge-Hamiltonicity should be retained with the finite seven-type verifier until written out in full; deleting both the words and that verifier would be a gap.
- `protected_pentagon_compact_lemma.tex` is a certificate-compression replacement. The protected-edge invariant is stronger than local Hamiltonicity, so the canonical verifier and its machine-readable records remain part of the proof package. `verify_pentagon.py` replays the literal records in the original manuscript and ends with `RESULT PASS`.

`SIMPLIFICATION_PLAN.md` explains which tables can be removed from the article and which finite certificate obligations remain.
