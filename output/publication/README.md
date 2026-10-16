# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This package contains the revised 44-page article, its standalone 18-page finite-certificate supplement, the LaTeX sources, exact Python readers and reproducibility reports. For nonempty planar graphs of girth at least five, the article proves Hamiltonicity for every `k >= 4` in these classes:

- Graphs with at most thirty-one distinct `5`-cycles (Theorems 1.3 and 5.47).
- Graphs with total degree excess `D(G) <= 9` (Theorem 5.45).
- Graphs with at most seven heavy vertices, with unrestricted heavy degrees (Theorem 5.46).
- Two-degenerate graphs with at most thirty-three distinct `5`-cycles or `D(G) <= 13` (Corollary 5.48).
- Graphs whose every block is subcubic (Theorem 5.41).

Here `D(G) = sum_v max(deg_G(v)-3,0)`, and a heavy vertex has degree at least four. Two-degeneracy means that every nonempty subgraph has a vertex of degree at most two. Each stated class has uniform Hamiltonian threshold four; its Hamilton-connected threshold remains between four and five. Corollary 5.3 retains the earlier two-degeneracy statement for graphs with at most eleven distinct `5`-cycles.

The new local factor consists of two pentagons sharing an edge, with one shared endpoint of original degree four and all seven other vertices of degree three. Its bare and chorded models have 410 normalized templates and 267,825 states. The literal arrays contain 1,230 `K2/K3/P3` product seeds with 2,142,600 seed states, covering 17,408 labelled boundaries and 446,976 directed factor interfaces. Full-matching overlap minima are six and twenty-one; core minima after two reserves are removed are six and twenty. Every matching edge is retained in every physical row. Complete clique partitions and quotient trees contain 133,811 blocks, including 203 triangles, and have physical connector capacity at most two. Both readers validate raw schemas and complete seed coverage; the independent reader restores every physical boundary without reading a primary report. The `P3` seeds are additional checked witnesses; the restoration proofs use the clique-product contract.

The preceding connected-cycle, bowtie, pentagonal-reservoir, further degree-two, shared-hub, protected-pentagon, adjacent-pair and `(2,3,2)`-path certificates remain in the delivery. The existing 558 bowtie clique trees and source-bound ordinary-pentagon seeds are reused. No duplicate ordinary-block array or bowtie data is added. The order-ten path family and the path partitions for the older 2,982 bowtie boundary templates remain outside the delivered dependencies. Ordinary restoration maps continue to propagate relative to the preceding bottom colouring.

The replay has fourteen positive suites and 132 actual-reader rejection cases. It preserves the preceding twelve local readers, twenty-two literal inputs, sixty marked blocks and the first ninety-seven rejection records. This revision adds two unchanged gzip inputs, three Python files and two positive reports. The finite checks certify local state coverage, adjacency, complete possible aliases, row protection, clique trees and interface margins. Arbitrary-order protected products, restoration, component-graph connectivity, tree splicing and structural inductions remain analytic arguments. The new excess and neighbourhood proof supersedes the former completed-dual argument and its unused reference.

The seven preceding archive replay records are retained. The thirty-one-pentagon archive's twelve original suites and manifest also pass read-only, leaving all ninety source files and supplied reports byte-identical. Its full-graph, product, selected-layer, geometry and algebra regressions are recorded separately from the delivered proof dependencies. The archive refers to the older `f229669` manuscript; this adoption starts from repository commit `996265a`. Literal equality does not identify these manuscript revisions. Exact archive identities, replay receipts and import mappings are in `supplement/reports/data-provenance.json`.

The root and standalone article and supplement copies are kept byte-identical. From this directory, run:

    python3 supplement/verify_all.py --write-reports
    python3 supplement/verify_all.py --check-manifest
    pdflatex main.tex
    pdflatex main.tex
    cd supplement
    pdflatex article_certificates.tex
    pdflatex article_certificates.tex

The first command regenerates reports; the second checks the manifest read-only. Running without a flag remains an alias for `--write-reports`. Python 3.10 or later and standard-library modules suffice. Report bytes are independent of the interpreter patch version. Compilation uses pdfLaTeX with its default output location; auxiliary files are excluded from the ZIP. The manifest covers all 71 delivered files other than `manifest.json` itself.

The unrestricted bounds remain `4 <= h(P5) <= 5` and `4 <= hc(P5) <= 5`. A vertex-minimal four-colour Hamiltonian counterexample has at least thirty-two distinct `5`-cycles, eight heavy vertices and `D(G) >= 10`. A degree-two vertex requires at least thirty-four distinct `5`-cycles and `D(G) >= 14`; if unique, the bounds are forty-two and sixteen. Under an at-most-thirty-three-cycle hypothesis, a minimum counterexample has minimum degree three, `D=10`, no ordinary facial pentagon, no face longer than six, and exactly thirty-two pentagonal faces. Its heavy-degree multiset is six fours and two fives, eight fours and one five, or ten fours; all other degrees are three. These are necessary conditions, not examples of counterexamples. Author metadata and journal-specific declarations remain placeholders.

`REVISION_NOTES.md` preserves the history. `computation-record.json` records the commands, finite scope and artifact hashes.
