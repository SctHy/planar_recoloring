# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This package contains the revised 35-page article, its standalone 15-page finite-certificate supplement, the LaTeX sources, exact Python readers, and reproducibility reports. For nonempty planar graphs of girth at least five, the article proves Hamiltonicity at every `k >= 4` in each of these classes:

- Graphs with at most fifteen distinct `5`-cycles (Theorems 1.3 and 5.4).
- Graphs whose every block is subcubic (Theorem 5.25).
- Graphs with at most one vertex of degree at least four, with no pentagon or maximum-degree bound (Theorem 5.27).
- Two-degenerate graphs with at most three vertices of degree at least four, or with at most seventeen distinct `5`-cycles (Corollary 5.29).

Two-degeneracy means that every nonempty subgraph has a vertex of degree at most two. Corollary 5.3 retains the earlier two-degeneracy statement for graphs with at most eleven distinct `5`-cycles. No four-colour Hamilton-connected conclusion is asserted for these classes.

The article now includes a legal four-colour interface construction for the subdivided-star lift, a parameterized bad-run invariant, explicit component-graph connectivity and protected-edge tree-splicing statements, a product-level protected-pentagon replay for all 23 x 23 component pairs, and a detailed subcubic face-count/dual-propagation argument. The theorem-like results use numbering without square-bracket titles; the four protected-pentagon local facts appear as Claims 1--4 with their internal labels preserved. The finite checks and the analytic induction steps are stated as separate parts of the evidence.

The new pentagonal reservoir families treat an ordinary pentagon paired with a degree-two vertex, adjacent or nonadjacent, and a pentagon containing one degree-two vertex. They contain 781 normalized boundary templates, 786 selected component cycles and 101,121 template states, covering 17,664 labelled boundaries and 486,912 directed boundary interfaces. The nonadjacent model can have two components; its certificates select a cycle in each component. Every component overlaps a component across each interface, and every overlapping pair has at least four common selected-cycle edges. The other two models have connected fibres and at least two common edges. An independent reader restores physical colour labels and reproduces the complete interface histograms. The earlier shared-hub, further degree-two and protected-pentagon certificates remain part of the delivery.

The one-heavy-vertex theorem, with no pentagon bound, uses an analytic structural lemma producing two nonadjacent ordinary pentagons, followed by the existing two-pentagon restoration. The arbitrary-length reservoir lift and the structural inductions are analytic arguments; finite interface checks certify their stated local premises.

The repository article source/PDF and the copies at the package root are kept byte-identical; the standalone certificate source/PDF likewise match the copies under `supplement/`. The package also carries the exact readers, reports, computation record, and manifest used for the delivered ZIP.

From this directory, run:

    python3 supplement/verify_all.py --write-reports
    python3 supplement/verify_all.py --check-manifest
    pdflatex main.tex
    pdflatex main.tex
    cd supplement
    pdflatex article_certificates.tex
    pdflatex article_certificates.tex

The first command explicitly regenerates the finite verification reports. The
second command is read-only: it checks the manifest and every delivered file,
without rewriting reports or other package files. Running `verify_all.py`
without a flag remains an alias for `--write-reports`.

Python 3.10 or later and standard-library modules suffice for verification.
Report bytes are independent of the interpreter patch version, so their
manifest hashes are stable across supported Python versions. Compilation uses
pdfLaTeX with its default output location. Auxiliary files are generated beside
their sources and are excluded from the submission ZIP. The manifest check
covers every delivered file except `manifest.json` itself.

The exact replay has eight positive suites and fifty-three fail-closed negative cases. It includes the two pentagonal reservoir readers alongside the earlier degree-two, shared-hub path, adjacent-pair, `(2,3,2)`-path and protected-pentagon suites. The protected-pentagon suite checks 23 component types, all 529 component products, 16,008 finite product blocks, 313 standard-source interfaces, the hard two-row/three-row seeds, and the relative-normalization rule on all labelled boundaries (75,120 overlapping cases). Arbitrary-length lifting, arbitrary-order component-graph connectivity, tree splicing, and the structural inductions remain mathematical arguments in the article; the scripts do not claim to formalize them.

The general four-colour Hamiltonian and Hamilton-connected questions for planar graphs of girth at least five remain open, with the stated bounds `4 <= h(P5) <= 5` and `4 <= hc(P5) <= 5`. A vertex-minimal counterexample to the unrestricted four-colour Hamiltonian assertion must have at least sixteen distinct `5`-cycles. If it has at most seventeen, it has exactly two degree-four vertices, all other vertices have degree three, and its faces have lengths five or six except possibly one face of length seven. This is a necessary condition, not an example of a counterexample. Author names, affiliations, contact details, and journal-specific declarations remain blank placeholders because no author metadata was supplied for this revision.

`REVISION_NOTES.md` records the changes in English. `computation-record.json` records the current commands, scope, and hashes.
