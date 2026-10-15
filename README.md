# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

| Path | Contents |
| --- | --- |
| `main.tex` / `main.pdf` | The article (35 pages). |
| `supplement/` | Standalone certificate supplement `article_certificates.tex` / `.pdf` (15 pages), the exact Python readers, and their reports; see [supplement/README.md](supplement/README.md). |
| `output/publication/`, `output/publication.zip` | Submission bundle: article, supplement, readers, reports, `computation-record.json`, `manifest.json`, `REVISION_NOTES.md`. The ZIP packages exactly the manifest files. |
| `output/research/` | Dated research folders on the open girth-five four-colour problem. |
| `formalization/` | Lean 4 (4.34.1) formalization of parts of the article; scope in `formalization/README.md` and `formalization/STATUS.md`. |

## Results and open problems

The common Hamiltonian and Hamilton-connected thresholds are `7` for planar graphs,
`5` for triangle-free and bipartite planar graphs, and `4` for planar graphs of girth
at least six and for forests; `d+3` is sharp for `d`-degenerate graphs. At four colours
the article proves Hamiltonicity for planar girth-five graphs with at most fifteen
distinct `5`-cycles, for those whose blocks are subcubic, and for those with at
most one vertex of degree at least four. It also covers two-degenerate planar
girth-five graphs with at most three vertices of degree at least four or at
most seventeen distinct `5`-cycles. For all planar
girth-five graphs,
`4 <= h(P5) <= 5` and `4 <= hc(P5) <= 5` remain open.

The finite readers certify only the listed local data. Arbitrary-length lifting,
component-graph connectivity, tree splicing and the structural inductions are analytic
arguments in the article.

The fifteen-cycle result adds three pentagonal restoration families to the
earlier shared-hub paths and seven degree-two reductions. Their literal component
cycles and all possible physical interfaces have primary and independent direct
readers. The reservoir family permits two components and requires at least four
common selected-cycle edges for every overlapping pair; the arbitrary-order
spanning-tree splice is proved in the article. The eleven-cycle
two-degeneracy corollary retains its original bound.
A vertex-minimal counterexample to the unrestricted four-colour Hamiltonian
assertion must therefore have at least sixteen distinct `5`-cycles and at least
two vertices of degree at least four.

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
