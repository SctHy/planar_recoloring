# Major revision notes

This revision addresses the P0/P1 proof gaps identified by the referees and synchronizes the article,
finite verifiers, and submission package. The delivered artifacts are a 27-page article and a 12-page certificate supplement;
both the article and supplement were compiled twice with pdfLaTeX.

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
