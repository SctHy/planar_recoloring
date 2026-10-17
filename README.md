# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

| Path | Contents |
| --- | --- |
| `main.tex` / `main.pdf` | The article. |
| `supplement/` | Shared certificate appendix body, standalone rendering wrapper `article_certificates.tex` / `.pdf`, exact Python readers, and reports; see [supplement/README.md](supplement/README.md). |
| `output/publication/`, `output/publication.zip` | Submission bundle: integrated article, reproducibility certificate source, readers, reports, `computation-record.json`, `manifest.json`, `REVISION_NOTES.md`. The ZIP packages exactly the manifest files. |
| `output/research/` | Dated research folders on the open girth-five four-colour problem. |
| `formalization/` | Lean 4 (4.34.1) formalization of parts of the article; scope in `formalization/README.md` and `formalization/STATUS.md`. |

## Results and open problems

The common Hamiltonian and Hamilton-connected thresholds are `7` for planar graphs,
`5` for triangle-free and bipartite planar graphs, and `4` for planar graphs of girth
at least six and for forests; `d+3` is sharp for `d`-degenerate graphs. Write
`D(G) = sum_v max(deg_G(v)-3, 0)` for total degree excess, and call a vertex
heavy if its degree is at least four. The integrated article proves Hamiltonicity at every
palette size at least four for planar girth-five graphs in each of these classes:

- `D(G) <= 10`;
- at most seven heavy vertices, with unrestricted degrees;
- at most thirty-three distinct `5`-cycles;
- two-degenerate with `D(G) <= 13`.

The block-subcubic result and the corollary that at most eleven distinct
`5`-cycles imply two-degeneracy are retained. Each Hamiltonian class has uniform
threshold `4`. For all planar girth-five graphs,
`4 <= h(P5) <= 5` and `4 <= hc(P5) <= 5` remain open.

A vertex-minimal counterexample to the unrestricted four-colour Hamiltonian
assertion must have at least thirty-four distinct `5`-cycles, at least eight
heavy vertices, and `D(G) >= 11`. A degree-two vertex forces at least thirty-four
distinct `5`-cycles and `D(G) >= 14`; if it is unique, the bounds become forty-two
and sixteen. Four-colour Hamilton-connectedness remains open for the stated
subclasses as well.

Fourteen exact reader suites certify the listed local data, including independent
physical-interface checks for the degree-two, pentagonal reservoir, extended
cycle, bowtie and hinged-pair families. The hinged-pair inputs supply protected
product seeds and clique trees. Arbitrary-length lifting, generalized clique
products, component-graph connectivity, tree splicing and the structural
inductions, including the equality rigidity at excess ten, are analytic
arguments in the article. The latest archive replay and the unadopted P10-dependent
two-degenerate claims are documented in
[the research review](output/research/thirty-three-pentagons-20261016/review.md).

## Verify and build

From the repository root (Python 3.10+, standard library only; pdfLaTeX):

```sh
python3 supplement/verify_all.py --write-reports
python3 supplement/verify_all.py --check-manifest
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The first command runs all readers and writes `supplement/reports/`. The second
checks, read-only, `output/publication/manifest.json` against every delivered file.

Author, affiliation and declaration fields are still empty placeholders. Earlier
manuscripts, editorial backups and superseded research records are kept only in Git
history.
