# Major revision notes

This revision addresses the P0/P1 proof gaps identified by the referees and synchronizes the article,
finite verifiers, and submission package. The delivered artifacts are a 30-page article and a 14-page certificate supplement;
both the article and supplement were compiled twice with pdfLaTeX.

Later revision of 2026-10-16: at most eleven distinct pentagons.

- Extended Theorems 1.3 and 5.4 from at most nine to at most eleven distinct `5`-cycles,
  and strengthened the two-degeneracy Corollary 5.3 accordingly. The proof uses the earlier
  shared-hub path reductions, the existing subcubic theorem (now Theorem 5.14), and seven
  further local reductions in Lemma 5.13. The last structural case deletes an entire
  pentagon or hexagon together with a degree-two tail.
- Added seven unchanged literal cycle families under `supplement/data/degree-two/`,
  documented in supplement Appendix F. They contain 421 templates and 96,036 template
  states, covering 8,704 labelled boundaries and 158,976 directed interfaces.
  `verify_degree_two_families.py` checks the fixed models, complete local state coverage,
  possible port aliases and all selected-cycle overlaps. The independent
  `verify_degree_two_interfaces.py` restores physical labels and rechecks every interface.
  Both require at least two common selected-cycle edges and agree on all reported totals
  and minimum margins; shared-port recolourings are checked as simultaneous moves.
- The complete replay now has six positive suites and thirty-one rejected negative cases.
  The four preceding positive report payloads change only in their certificate-source hash;
  the fifteen preceding rejection records are preserved and sixteen new cases are added.
  Two new reports record the degree-two cycles and independent physical interface replay;
  the summary updates the suite counts and scope.
- The article has 30 pages and the supplement has 14 pages. Article pages 1-3, 14-16,
  19-21 and 27-30, and supplement page 14 were rendered and inspected without clipping,
  overlap or broken formulas. The final root logs have no warnings, undefined references
  or overfull/underfull boxes. Supplement Table F.1 records the same seven finite
  families as the article's verification table.
- The unbounded restoration and structural induction remain analytic arguments. The
  unrestricted Hamiltonian and Hamilton-connected thresholds remain in `[4,5]`; a
  vertex-minimal counterexample to the unrestricted four-colour Hamiltonian assertion
  must have at least twelve distinct `5`-cycles.

Earlier revision of 2026-10-16: at most nine distinct pentagons.

- Extended the four-colour Hamiltonian subclass from at most seven to at most nine distinct
  `5`-cycles (Theorems 1.3 and 5.4). Corollary 5.3 proves two-degeneracy of this class;
  the new structural induction uses the shared-hub path reductions in Lemmas 5.11 and 5.12.
- Added the order-four and order-five literal cycle families to `supplement/data/`, unchanged
  from the reviewed research archive, and documented them in supplement Appendix E.
  `verify_shared_hub_paths.py` checks all 64 and 256 labelled boundaries and all 576 and
  3,072 directed one-port interfaces. The minimum common cycle-edge counts are 3 and 5.
- The complete replay now has four positive suites and fifteen rejected negative cases.
  The historical literal certificate blocks are preserved. Existing positive report payloads
  change only in their certificate-source hash; six new negative cases and the shared-hub
  report record the added scope. The arbitrary-length splice and structural induction remain
  analytic proofs, and the general bounds on both girth-five thresholds remain `[4,5]`.
- The new article has 28 pages and the supplement has 13 pages. Article pages 1-3, 14-15,
  19-20 and 26-28, and supplement pages 1, 12 and 13 were rendered and inspected without
  clipping, overlap or broken formulas. The final root logs have no warnings, undefined
  references or overfull/underfull boxes.

Earlier revision history (through 2026-10-15):

The naming-style revision follows the article's numbering-first rule: 36 visible square-bracket titles from theorem/lemma/proposition/corollary environments were removed,
while all internal `\label`s and cross-references were retained. The four local facts in the protected-pentagon section became Claims 1--4,
and ordinary working terms remain lowercase. The introduction threshold table was narrowed and centered. The supplement,
certificate records, and historical full manuscript were not changed.

This review pass also corrected the face count in the structural lemma for two separated pentagons. Let
`epsilon = 1_{z in B}`, so `p_H = epsilon` and `q_H = r - epsilon + q'`;
therefore the article uses
`f_5^in = ell + 6 - 2r - 2epsilon - 2q' + L`.
The lower bound in each of the three branches explicitly uses `epsilon + q' <= 1`; finite checks,
analytic proofs, and the unresolved general problem remain separated as described below.

Review pass of 2026-10-14 (article text only; certificates, checkers and supplement PDF unchanged):

- Closed a normalization gap in the two-pentagon restoration. With each boundary's own canonical map,
  88 of the 30,840 overlapping labelled interfaces (for example `00002 -> 00003`) have no common protected edge.
  Restoration maps are now propagated along a bottom Hamilton path relative to the source, which is exactly
  what Claim 2 certifies; a direct replay of this rule over all 2,304 labelled boundaries, all admissible maps
  and all one-entry changes found a common protected edge in all 75,120 overlapping cases. Claim 3 is now
  stated and proved on that path, without wrap-around. Since 2026-10-15 this replay, together with the 88
  canonical-map failures and the printed `00002 -> 00003` example, is part of `verify_protected_pentagons.py`
  and its report; the certificate source is unchanged.
- Merged the single-vertex Hamiltonian lift with the closed-lifting claim of the vertex-pancyclicity proof
  (Lemma 2.2 now gives all cycle lengths), shortened the endpoint interchange in Lemma 2.4, dropped an unused
  palette bound in Lemma 3.6, weakened Claim 4 to `r >= Delta`, and removed redundant text in Theorem 5.4 and Lemma 5.14.
- Defined `H = G - S` in the second case of Theorem 4.5, removed an incorrect justification in Lemma 5.1,
  made `epsilon` component-local and named the second pentagon correctly in Lemma 5.16.
- Theorem numbering and page counts are unchanged (27-page article, 12-page supplement).

Repository cleanup of 2026-10-15 (no change to the article, supplement or certificate data):

- Removed four legacy scripts from the package: the compatibility entry points `check_adjacent_pair_cycles.py`
  and `verify_pentagon.py`, and the unused sanity checks `check_rook_splice.py` and `check_path232_structural.py`.
  None was an input to `verify_all.py`; the package now has 23 delivered files.
- `verify_all.py --check-manifest` ignores operating-system metadata (`.DS_Store`, `._*`), so the read-only
  check also passes inside a Finder-browsed package directory.

Main mathematical revisions:

- Rewrote the `subdivided-star lift`. Tree edges are constructed explicitly by repeated-colour type,
  with the list intersections needed whenever the centre colour changes; the triangular and square interfaces of non-binary fibres are handled,
  and auxiliary vertices are explicitly nonadjacent to the centre, so the conflict raised in the original review cannot occur.
- Wrote the `(2,3,2)` bad-run splice as an inductive invariant for arbitrary length:
  four interface edges remain at the first layer and at least two usable internal edges remain at the newest layer.
- Expressed component-graph connectivity, the protected-edge product, and tree splicing in the pentagon restoration as separate numbered facts,
  specifying product coordinates, pool/reserve edges, common protected edges, and the stepwise splicing invariant.
- In the protected-product proof, made the product-coordinate transport `Phi_1 x Phi_2` of common protected edges explicit,
  and wrote the two component-graph reset indices as paths to a common checkpoint; a label-transition table records connectivity of the actual component graph.
- Expanded the face-length count with bridges, the outer-face count after pentagon deletion, bridge double counting,
  and the dual-propagation closure proof in the unique degree-two branch; corrected the `Subcubic blocks` theorem label.
- Added the frozen-colouring definition, the connectivity/Hamiltonicity distinction in the work of Bartier et al.,
  an explicit six-colour model for the icosahedron, and the arrangement-graph parameter convention to the article.

Finite certificates and reproduction:

- `verify_protected_pentagons.py` now replays all `23^2 = 529` product types, two-row/three-row seeds,
  protected-edge retention, and alternating reserve splicing; the current report records 16,008 product block cycles.
- `verify_all.py --write-reports` explicitly generates the three positive reports, nine negative-case reports, and the summary;
  running without a flag keeps the same write behavior.
- `verify_all.py --check-manifest` is now read-only: it checks only the byte counts, SHA-256 hashes, and manifest coverage of every delivered package file,
  without overwriting any report.
- Reports no longer write `platform.python_version()`; their bytes and manifest hashes remain stable across supported Python 3.10+ versions.
- The complete check currently has three positive suites and nine rejected negative cases; the certificate-source SHA-256 remains
  `104d1d399dcebfa4a6411933989a01d24f771400a9d5bbdf98a9808c874c0410`.
- The certificates cover only the listed finite local states, interfaces, and product replays. Arbitrary-length bad-run lifting,
  component-graph/tree-splicing over arbitrary base cycles, and structural induction remain analytic arguments in the article;
  finite passes must not be read as global formal verification.

Delivery checks:

- The root article and the independent build under `output/publication/` are both 27 pages; both supplements are 12 pages.
- `manifest.json` and `output/publication.zip` were regenerated; the ZIP contains the delivery files directly and no LaTeX auxiliary files,
  caches, or temporary renders.
- Author, affiliation, contact, and funding/data/AI declarations still need to be filled from actual information before submission;
  this revision does not invent them.
