# Companion certificate source

The article source at `../planar_recoloring_hamilton_thresholds.tex` is the compact presentation adopted from the simplification package. The file `planar_recoloring_hamilton_thresholds_full.tex` is the pre-adoption 41-page source and retains the literal finite certificates and appendices used by the compact article.

The Python files are bounded replay/check scripts:

- `verify_pentagon.py` replays the protected-pentagon records in the full source.
- `check_adjacent_pair_cycles.py` checks the seven short adjacent-pair cycle orbits and interface exits.
- `check_rook_splice.py` checks the row/column splice construction and its four exceptional paths.
- `check_path232_structural.py` checks the expanded normalized `(2,3,2)` cycles.

The proposed fragment files are retained for review. They are not silently treated as adopted proof text. In particular, the path fragment has a parameter typo in the `010` case, and the protected-pentagon compact fragment needs an explicit target-pool condition in its interface witness before it can replace the full records.
