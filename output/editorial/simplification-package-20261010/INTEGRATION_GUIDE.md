# Integration guide

The fragment files are deliberately separate so the original proof can be reviewed one local change at a time.

## 1. Adjacent-pair reset

In the triangle-free five-colour section, replace `Lemma pair-five-endpoints` and its proof by `adjacent_pair_compact_lemma.tex`. Keep the reset lemma and its proof. Change the first sentence of the reset proof to cite `Lemma pair-five-edge-cycles` and use its common-interface exit statement. Delete the 53 endpoint words and the counts table from the appendix. The new edge-cycle lemma is exactly what the first propagation step needs; the appended rook-splice lemma supplies Hamilton-connectedness for 342, 343, 443 and 444, which the later reset step still calls. The old endpoint classification is removed.

The accompanying checker `check_adjacent_pair_cycles.py` confirms the seven representative cycles, their edge-orbit coverage, and the common-neighbour property for every allowed interface. The seven short cycles remain in the proof text; the 53 paths do not.

## 2. `(2,3,2)` restoration

Replace the displayed `001`, `010`, `012` cyclic words and the selected-layer paragraph by `path232_structural_replacement.tex`. Keep the seven short safe-port arithmetic identities, or move them into the supplement; no table environment is needed. The structural lemma builds the 14/17/16-state cycles from `K_2\square K_2`, `K_2\square K_3`, `K_2\square K_3`/`K_3\square K_3` layer cycles and four matching switches. The checker `check_path232_structural.py` expands the construction and verifies coverage and one-coordinate adjacency.

## 3. Protected pentagons

Replace the printed ordinary cycles, starred cycles, matching chain, pools and 47 exceptional records by `protected_pentagon_compact_lemma.tex`, and put the records into a machine-readable certificate consumed by the supplementary verifier. Keep the protected-set invariant and the component-tree splice proof in the article. The protected condition quantifies over every physical product row, so a statement that each fibre merely has a Hamilton cycle is insufficient.

## 4. What remains finite

The compact manuscript is a presentation refactor. It does not turn the protected-pentagon certificate into a general theorem. A rigorous final version must either include the verifier/certificate as supplementary proof data or replace that finite kernel by a new structural argument. The same standard applies to the finite `C_5` four-colour certificate.
