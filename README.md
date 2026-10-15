# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

| Path | Contents |
| --- | --- |
| `main.tex` / `main.pdf` | The article (27 pages). |
| `supplement/` | Standalone certificate supplement `article_certificates.tex` / `.pdf` (12 pages), the exact Python readers, and their reports; see [supplement/README.md](supplement/README.md). |
| `output/publication/`, `output/publication.zip` | Submission bundle: article, supplement, readers, reports, `computation-record.json`, `manifest.json`, `REVISION_NOTES.md`. The ZIP packages exactly the manifest files. |
| `output/research/` | Dated research folders on the open girth-five four-colour problem. |
| `formalization/` | Lean 4 (4.34.1) formalization of parts of the article; scope in `formalization/README.md` and `formalization/STATUS.md`. |

## Results and open problems

The common Hamiltonian and Hamilton-connected thresholds are `7` for planar graphs,
`5` for triangle-free and bipartite planar graphs, and `4` for planar graphs of girth
at least six and for forests; `d+3` is sharp for `d`-degenerate graphs. At four colours
the article proves Hamiltonicity for planar girth-five graphs with at most seven
`5`-cycles and for those whose blocks are subcubic. For all planar girth-five graphs,
`4 <= h(P5) <= 5` and `4 <= hc(P5) <= 5` remain open.

The finite readers certify only the listed local data. Arbitrary-length lifting,
component-graph connectivity, tree splicing and the structural inductions are analytic
arguments in the article.

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
