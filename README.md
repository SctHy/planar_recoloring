# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This repository contains the manuscript and the finite certificate readers for the paper on
Hamiltonian and Hamilton-connected recolouring graphs of planar graphs. The manuscript is kept at
the repository root. No external image assets are required: the article and its finite diagrams are
typeset directly in LaTeX.

## Main results

For a graph \(G\), write

\[
D(G)=\sum_{v\in V(G)}\max\{\deg_G(v)-3,0\},
\]

and call a vertex heavy when its degree is at least four. The common threshold is 7 for planar
graphs, 5 for triangle-free and bipartite planar graphs, and 4 for planar graphs of girth at least
six and for forests; the bound \(d+3\) is sharp for \(d\)-degenerate graphs. The article proves
Hamiltonicity for every palette size \(k\ge 4\) for planar graphs of girth at least five in each
of these classes:

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

The `supplement/` directory contains the literal finite data and exact Python readers used by
Appendices A--J. The readers check finite legality, coverage, selected cycles and seeds, protected
edges, physical aliases, interfaces, and clique trees. The unbounded lifting, product, splicing,
and structural-induction arguments remain analytic arguments in the article.

Fourteen reader suites cover the shared-hub, degree-two, pentagonal-reservoir, extended-cycle,
bowtie, and hinged-pair families, including independent physical-interface checks. See
[`supplement/README.md`](supplement/README.md) for the data contracts and reader responsibilities.

## Repository layout

```text
main.pdf                         Compiled manuscript
main.tex                         Main LaTeX source, bibliography, and analytic proofs
supplement/
├── article_certificates.pdf     Standalone certificate appendix
├── article_certificates.tex     Standalone rendering wrapper
├── article_certificates_body.tex  Appendix A--J body loaded by main.tex
├── data/                         Literal finite certificate inputs
├── verify_all.py                 Runs the finite readers
└── verify_*.py                   Exact primary and independent readers
output/
└── research/                     Dated research records and review notes
```

The dated folders in `output/research/` retain open-problem investigations. They are separate from
the finite certificate inputs used by the article.

## Reproduce and build

Run these commands from the repository root. Python 3.10 or later and `pdfLaTeX` are required; the
Python readers have no third-party dependencies. Reader output is written to a temporary directory
so that generated validation files do not become part of the source tree.

```sh
python3 supplement/verify_all.py --write-reports \
  --report-dir /tmp/planar-recoloring-reports
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The finite checks are evidence for the stated local lemmas, not a formal verification of the whole
article. The unrestricted planar girth-five Hamiltonian and Hamilton-connectedness thresholds remain
open.
