# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This package contains the revised 43-page article, its standalone 17-page finite-certificate supplement, the LaTeX sources, exact Python readers, and reproducibility reports. For nonempty planar graphs of girth at least five, the article proves Hamiltonicity at every `k >= 4` in each of these classes:

- Graphs with at most twenty-five distinct `5`-cycles (Theorems 1.3 and 5.45).
- Graphs whose every block is subcubic (Theorem 5.41).
- Graphs with at most six vertices of degree at least four (Theorem 5.44).
- Two-degenerate graphs with at most seven vertices of degree at least four (Corollary 5.38).

A heavy vertex has degree at least four. Two-degeneracy means that every nonempty subgraph has a vertex of degree at most two. Each displayed class has uniform Hamiltonian threshold four; its Hamilton-connected threshold remains between four and five. Corollary 5.3 retains the earlier two-degeneracy statement for graphs with at most eleven distinct `5`-cycles.

The new connected-cycle certificates cover two ordinary pentagons sharing an edge, with or without the possible middle chord, an order-seven path with three contacts at a common retained hub, and two ordinary pentagons joined by one or two edges. Their five literal arrays contain 771 templates and 2,491,162 states, covering 75,008 labelled boundaries and 2,577,024 directed physical interfaces. A separate reader reproduces every interface histogram using its own graph, contact and spatial contracts.

The bowtie certificates contain 558 fibres and 845,440 states, with 1,116 Hamilton cycles in products with `K2` and `K3`. They check 2,251,776 directed factor interfaces for both the full protected matching and its core after two reserve edges are removed. Core overlap minima are nine and twenty-four for the bare and chorded models. Complete clique partitions and quotient trees have physical connector capacity at most two. The same 558 clique trees support both the ordinary-pentagon/bowtie and paired-bowtie product arguments. The ordinary seed extract is compared exactly with the supplement's existing marked cycles, pools, hard seeds and protected sets; its `P2/P3` seeds are also valid in `K2/K3`.

The earlier adjacent-pair, `(2,3,2)`-path, protected-pentagon, shared-hub path, further degree-two and pentagonal-reservoir certificates remain in the delivery. The reservoir reader reconstructs every component, selects a cycle in each, and checks bilateral non-killability and every overlapping component pair; a disconnected fibre is treated through its components. The protected-pentagon suite retains all 529 component-product replays, 16,008 finite product blocks and 75,120 overlapping relative-normalization cases. Restoration maps for ordinary pentagons propagate relative to the preceding bottom colouring, as proved in the article.

The exact replay has twelve positive suites and ninety-seven fail-closed rejection cases. It preserves the preceding eight local readers, twelve literal data files, fifty-eight marked certificate blocks and the first fifty-three rejection records. The new revision adds ten literal inputs, five Python files and four positive reports. Its finite checks certify local coverage, adjacency, protection, complete possible aliases, row retention and interface margins. Arbitrary-length lifting, generalized protected products, component-graph connectivity, tree splicing and the planar structural inductions remain analytic arguments.

Seven supplied research archives were also replayed completely, including their manifests, with byte-identical reports. Those original regressions and geometric fixtures are audit evidence outside this delivery. The redundant order-ten path family and the path partitions for the older 2,982 bowtie boundary templates are omitted from the publication dependencies. The archives refer to the older `f229669` manuscript; this adoption starts from repository commit `6b0374b`. Equality of the imported literals does not identify those manuscript revisions. Exact archive identities and import mappings are recorded in `supplement/reports/data-provenance.json`.

The repository article source/PDF and the copies at the package root are kept byte-identical; the standalone certificate source/PDF likewise match the copies under `supplement/`. From this directory, run:

    python3 supplement/verify_all.py --write-reports
    python3 supplement/verify_all.py --check-manifest
    pdflatex main.tex
    pdflatex main.tex
    cd supplement
    pdflatex article_certificates.tex
    pdflatex article_certificates.tex

The first command regenerates the finite verification reports. The second is read-only: it checks the manifest and every delivered file without rewriting reports. Running `verify_all.py` without a flag remains an alias for `--write-reports`. Python 3.10 or later and standard-library modules suffice. Report bytes are independent of the interpreter patch version. Compilation uses pdfLaTeX with its default output location; auxiliary files are excluded from the ZIP. The manifest covers all 64 delivered files other than `manifest.json` itself.

The unrestricted questions remain open: `4 <= h(P5) <= 5` and `4 <= hc(P5) <= 5`. A vertex-minimal four-colour Hamiltonian counterexample must have at least twenty-six distinct `5`-cycles and seven heavy vertices; if it has a degree-two vertex, it has at least eight heavy vertices. The sharper face restriction for at most twenty-seven pentagons assumes minimum degree at least three. These are necessary conditions, not examples of counterexamples. Author names, affiliations, contact details and journal-specific declarations remain placeholders because no author metadata was supplied.

`REVISION_NOTES.md` preserves the revision history. `computation-record.json` records the commands, finite scope and artifact hashes.
