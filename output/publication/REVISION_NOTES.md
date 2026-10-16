# Major revision notes

This revision addresses the P0/P1 proof gaps identified by the referees and synchronizes the article,
finite verifiers, and submission package. The delivered artifacts are a 44-page article
and an 18-page certificate supplement, each compiled twice with pdfLaTeX.

Latest revision of 2026-10-16: thirty-one pentagons, excess nine and seven heavy vertices.

- Extended Theorem 1.3 to at most thirty-one distinct `5`-cycles, total excess
  `D(G) <= 9`, at most seven heavy vertices, and two-degenerate graphs with at
  most thirty-three distinct `5`-cycles or `D(G) <= 13`. Here
  `D(G) = sum_v max(deg_G(v)-3,0)`. Heavy degrees are unrestricted in the
  seven-heavy class. The detailed results are Theorems 5.45--5.47 and
  Corollary 5.48. The block-subcubic Theorem 5.41 and eleven-cycle
  two-degeneracy Corollary 5.3 are retained. All Hamiltonian conclusions hold
  for every `k >= 4`; no four-colour Hamilton-connectedness assertion is added.
- Added exactly two unchanged literal files under `supplement/data/hinged-pairs/`.
  The bare/chorded models have 379/31 templates and 241,774/26,051 factor states.
  Their complete `K2/K3/P3` seeds contain 1,934,192/208,408 states and cover
  430,080/16,896 directed physical interfaces. Full matching overlap minima
  are 6/21 and post-reserve core minima are 6/20. The 410 clique trees contain
  133,811 blocks, including 203 triangles, with physical connector capacity two.
  Appendix J records the finite contract; the `P3` seeds are additional checked
  witnesses, while restoration uses the clique-product lemma.
- Added `hinged_pair_core.py`, `verify_hinged_pairs.py` and
  `verify_hinged_pair_interfaces.py`, with strict raw schemas before decoding.
  Both readers check complete seed coverage and row retention. The direct reader
  freezes its own graph/contact/spatial contracts and physically restores every
  labelled boundary without importing a primary reader or report. Both complete
  full/core histograms and digests agree. The existing ordinary seeds and bowtie
  clique trees are reused; no ordinary-block array or duplicate bowtie data is added.
- The complete replay has fourteen positive suites and 132 rejection cases.
  All sixty earlier marked blocks, twelve local readers, twenty-two literal inputs
  and ninety-seven rejection records are preserved. Thirty-five new cases include
  valid local seeds with a failed reserve-core interface, a path substituted for
  a clique, a legal quotient tree exceeding physical capacity, malformed raw
  palettes/schemas, and missing or mismatched marked coverage counts. Earlier
  positive payloads change only in their certificate-source hash.
- Replayed the new archive's twelve original readers and manifest read-only in
  43.625 and 0.033 seconds, preserving all ninety source files and reports byte
  for byte. The previous seven archive replays and provenance records remain.
  The new archive declares baseline `f229669`; adoption starts at `996265a`.
  Its two full fourteen-vertex recolouring-graph regressions cover 3,391,200 states;
  eighteen fixed-boundary products cover 3,157,772 states; the selected four-layer
  subgraph has 82,120 states. These scopes remain distinct from the universal proof.
- Replaced the former six-heavy completed-dual argument and removed its unused
  Tsai--West reference. The new analytic neighbourhood/excess proof gives the
  stronger seven-heavy and thirty-one-pentagon classes. The revised degree-two
  proof uses no order-ten path: a degree-two vertex in a minimum counterexample
  requires at least thirty-four distinct pentagons and excess fourteen; a unique
  degree-two vertex requires forty-two and sixteen. The finite readers certify
  local premises, rather than these arbitrary-order arguments.
- The article has 44 pages and the supplement has 18 pages. Table 7.1 is on
  article page 43 and Table J.1 is on certificate page 18. The delivery has
  65 computation-record artifacts and 71 manifest entries. The two new reports
  record the primary seeds/trees and independent physical interfaces.
- The unrestricted thresholds remain `[4,5]`. A minimum counterexample has at
  least thirty-two distinct `5`-cycles, eight heavy vertices and excess ten.
  With at most thirty-three distinct `5`-cycles it has minimum degree three,
  `D=10`, `Q=e=0`, no ordinary facial pentagon, and thirty-two pentagonal faces;
  all other faces are hexagons. Its heavy-degree multiset is `(4^6,5^2)`,
  `(4^8,5)` or `(4^10)`, and all remaining vertices have degree three.
  These are necessary conditions, with no counterexample asserted.

Earlier revision of 2026-10-16: twenty-five pentagons and six heavy vertices.

- Extended Theorem 1.3 to graphs with at most twenty-five distinct `5`-cycles,
  graphs with at most six heavy vertices, and two-degenerate graphs with at most
  seven heavy vertices. A heavy vertex has degree at least four. The detailed
  results are Theorems 5.45 and 5.44 and Corollary 5.38; the retained block-subcubic
  result is Theorem 5.41. The conclusions hold for every `k >= 4` and do not add
  a four-colour Hamilton-connectedness assertion.
- Added five unchanged literal connected-cycle families: adjacent ordinary
  pentagons with or without the possible middle chord, a three-contact order-seven
  path, and ordinary pentagons with one or two joining edges. Appendix H records
  771 templates and 2,491,162 states, covering 75,008 labelled boundaries and
  2,577,024 directed interfaces. Two new exact readers check complete cycles,
  possible alias matchings and independent physical interface histograms.
- Added the bare and chorded bowtie `K2/K3` seeds, 558 clique trees and a small
  ordinary-pentagon seed extract. Appendix I records 845,440 bowtie states,
  1,116 seed cycles and 2,251,776 directed interfaces before and after reserving
  two matching edges. The core overlap minima are nine and twenty-four. Every
  clique partition and quotient tree is checked, including physical connector
  capacity two; the same clique trees support both product families. Exact
  comparison with the preceding marked ordinary data preserves the protected
  sets and reserve IDs required by relative normalization.
- The new delivery adds ten literal inputs, five Python files and four positive
  reports. It preserves the preceding eight local readers, twelve literal inputs,
  fifty-eight marked blocks and fifty-three rejection records. Twelve positive
  suites and ninety-seven rejection cases cover the finite contract. The new
  rejection cases include legal local seeds with an invalid post-reserve interface,
  a path substituted for a three-vertex clique, and a legal quotient tree with
  excessive physical connector capacity. Earlier positive payloads change only
  in their certificate-source binding.
- Replayed all seven supplied research packages and their manifests, preserving
  their supplied reports byte for byte. This external audit includes the original
  order-ten path, product/layer regressions and geometric fixtures. The delivered
  proof omits the redundant order-ten path family and replaces the path partitions
  for the older 2,982 bowtie boundary templates with the paired package's
  558 clique trees.
  The supplied archive manuscript baseline is `f229669`; adoption starts from
  `6b0374b`. Literal equality does not assert equality of these manuscript revisions.
- Added the analytic degree-two bounds, angular charging and six-star structural
  argument. A minimum counterexample with a degree-two vertex has at least eight
  heavy vertices and more than twenty-five pentagons. The six-heavy structural
  theorem completes the twenty-five-pentagon induction. The exact checks certify
  the finite local premises; these arbitrary-order arguments remain analytic.
- The article has 43 pages and the supplement has 17 pages. Table 7.1 is on
  article page 42; Tables H.1 and I.1 are on certificate pages 16 and 17.
  The package has 58 computation-record artifacts and 64 manifest entries.
- The unrestricted thresholds remain `[4,5]`. A vertex-minimal four-colour
  Hamiltonian counterexample has at least twenty-six distinct `5`-cycles and
  seven heavy vertices. The sharper necessary face conditions for at most
  twenty-seven pentagons assume minimum degree at least three; degree-two
  cases with twenty-six or twenty-seven pentagons are not eliminated.

Earlier revision of 2026-10-16: fifteen pentagons and pentagonal reservoirs.

- Extended the Hamiltonian subclass to at most fifteen distinct `5`-cycles. Added the
  class with at most one vertex of degree at least four, without a pentagon or maximum-degree
  bound, and two-degenerate graphs with at most three such vertices or at most seventeen
  distinct `5`-cycles. All conclusions hold for every `k >= 4`; no four-colour
  Hamilton-connected conclusion is added. The fifteen-cycle result is Theorem 5.4,
  the one-heavy-vertex result is Theorem 5.27, and the two-degenerate classes are
  Corollary 5.29. The earlier eleven-cycle two-degeneracy Corollary 5.3 is unchanged,
  and the block-subcubic class remains covered by Theorem 5.25.
- Added three unchanged literal families under `supplement/data/pentagonal-reservoirs/`:
  `reservoir-family.json`, `pentagon-full-family.json` and `pentagon-pendant-family.json`.
  They contain 781 boundary templates, 786 component cycles and 101,121 template states,
  covering 17,664 labelled boundaries and 486,912 directed boundary interfaces.
  `verify_pentagonal_reservoirs.py` checks complete state/component coverage, all possible
  port identifications and overlapping component interfaces.
  `verify_pentagonal_reservoir_interfaces.py` independently restores physical labels and
  reproduces the full interface histograms. A disconnected reservoir fibre is handled
  through its component cycles, not described as a Hamiltonian fibre.
- Added the analytic component-tree lift, degree-two heavy-vertex budgets, and the
  one-exception structural lemma, including bridges, cutvertices and shared exterior
  neighbours. The fifteen-cycle proof and the stronger degree-two restrictions use
  these lemmas together with the stated inherited restorations. The finite reservoir
  data and restoration are Lemmas 5.14 and 5.15; the budgets are Lemma 5.17 and the
  one-exception structural result is Lemma 5.26. Proposition 5.28 excludes degree-two
  vertices in a minimal counterexample with at most seventeen pentagons.
- Preserved all 57 preceding marked certificate blocks, the six preceding local readers
  and nine preceding JSON witnesses. The replay now has eight positive suites and
  fifty-three rejected negative cases. The six preceding positive report payloads change
  only in their certificate-source hash; all thirty-one earlier rejection records remain,
  with twenty-two added cases. Two new reports record the reservoir component cycles and
  independent physical interfaces; the summary updates the counts and scope.
- The article has 35 pages and the supplement has 15 pages. Article pages 1-3, 14-15,
  19-23 and 30-35, and supplement pages 14-15 were rendered and inspected without clipping,
  overlap or broken formulas. Final root logs have no warnings, undefined references or
  overfull/underfull boxes. The article's verification table is Table 7.1 on page 34.
- The unrestricted thresholds remain `[4,5]`. A vertex-minimal four-colour Hamiltonian
  counterexample must have at least sixteen distinct `5`-cycles. If it has at most
  seventeen, it must have exactly two degree-four vertices and otherwise degree three,
  with only pentagonal and hexagonal faces except possibly one heptagon.

Earlier revision of 2026-10-16: at most eleven distinct pentagons.

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
