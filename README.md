# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This repository contains the manuscript and the exact finite certificate readers for the paper
on Hamiltonian and Hamilton-connected recolouring graphs of planar graphs. The manuscript is kept
at the repository root. No external image assets are required: the article and its finite diagrams
are typeset directly in LaTeX.

## Main results

For a graph \(G\), write

\[
D(G)=\sum_{v\in V(G)}\max\{\deg_G(v)-3,0\},
\]

and call a vertex heavy when its degree is at least four. The common threshold is 7 for planar graphs,
5 for triangle-free and bipartite planar graphs, and 4 for planar graphs of girth at least six and for
forests; the bound \(d+3\) is sharp for \(d\)-degenerate graphs. The article proves Hamiltonicity for
every palette size \(k\ge 4\) for planar graphs of girth at least five in each of these classes:

- \(D(G)\le 10\);
- at most seven heavy vertices, with unrestricted degrees;
- at most thirty-three distinct 5-cycles;
- two-degenerate graphs with \(D(G)\le 13\);
- graphs whose blocks are subcubic.

The corresponding Hamiltonian threshold is four in every listed class. The block-subcubic result
and the corollary that at most eleven distinct 5-cycles imply two-degeneracy are retained. For all
planar graphs of girth at least five, the unrestricted bounds

\[
4\le h(P_5)\le 5,\qquad 4\le h_c(P_5)\le 5
\]

remain open.

The paper also gives necessary conditions for a vertex-minimal counterexample to the unrestricted
four-colour Hamiltonian assertion: at least thirty-four distinct 5-cycles, at least eight heavy
vertices, and \(D(G)\ge 11\). A degree-two vertex forces at least thirty-four distinct 5-cycles
and \(D(G)\ge 14\); when it is unique, the bounds become forty-two and sixteen.

## The paper

The manuscript is in the repository root:

- `main.pdf` is the compiled article;
- `main.tex` is the main LaTeX source and loads the certificate appendix body from
  `supplement/article_certificates_body.tex`;
- `main.tex` contains the bibliography and the article's analytic proofs;
- `supplement/article_certificates.tex` and `supplement/article_certificates.pdf` provide a
  standalone rendering of the finite certificate appendices.

## Finite certificates

The `supplement/` directory contains the marked finite data, exact Python readers, independent
interface readers, and reports used by Appendices A--J. The readers use Python 3.10 or later and
the standard library only. They check finite legality, coverage, selected cycles and seeds,
protected edges, physical aliases, interfaces, and clique trees. The unbounded lifting, product,
splicing, and structural-induction arguments remain analytic arguments in the article.

Fourteen exact reader suites cover the shared-hub, degree-two, pentagonal-reservoir, extended-cycle,
bowtie, and hinged-pair families, including independent physical-interface checks. The latest archive
replay and the unadopted P10-dependent two-degenerate claims are documented in the
[research review](output/research/thirty-three-pentagons-20261016/review.md).

See [`supplement/README.md`](supplement/README.md) for the data contracts, reader responsibilities,
and the full certificate table.

## Repository layout

```text
main.pdf                         Compiled manuscript
main.tex                         Main LaTeX source, bibliography, and analytic proofs
supplement/
├── article_certificates.pdf     Standalone certificate appendix
├── article_certificates.tex     Standalone rendering wrapper
├── article_certificates_body.tex  Appendix A--J body loaded by main.tex
├── data/                         Literal finite certificate inputs
├── reports/                      Replayed certificate reports
├── verify_all.py                 Runs all readers and the manifest check
└── verify_*.py                   Exact primary and independent readers
output/
├── publication/                  Submission bundle and reproducibility metadata
├── publication.zip               ZIP generated from the publication manifest
└── research/                     Dated research records and review notes
```

The publication bundle mirrors the root manuscript and supplement. The dated folders in
`output/research/` retain open-problem investigations and are separate from the finite certificate
inputs used by the article.

## Reproduce and build

Run these commands from the repository root. Python 3.10 or later and `pdfLaTeX` are required;
the Python readers have no third-party dependencies.

```sh
python3 supplement/verify_all.py --write-reports
python3 supplement/verify_all.py --check-manifest
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The first command runs all fourteen reader suites and writes `supplement/reports/`. The manifest
check is read-only and verifies `output/publication/manifest.json` against every delivered file.
Compile each document twice so that references and certificate appendices are fully resolved.

The finite checks are evidence for the stated local lemmas, not a formal verification of the whole
article. The unrestricted planar girth-five Hamiltonian and Hamilton-connectedness thresholds remain
open.
