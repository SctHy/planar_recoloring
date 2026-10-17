# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This repository contains the manuscript and the finite certificate readers for the paper on
Hamiltonian and Hamilton-connected recolouring graphs of planar graphs. The manuscript is kept at
the repository root. No external image assets are required: the article and its finite diagrams are
typeset directly in LaTeX.

## Main results

For a graph $G$, write

$$
D(G)=\sum_{v\in V(G)}\max\left\lbrace\deg_G(v)-3,0\right\rbrace,
$$

The common threshold is 7 for planar graphs, 5 for triangle-free and bipartite planar graphs, and 4 for planar graphs of girth at least
six and for forests; the bound $d+3$ is sharp for $d$-degenerate graphs. The article proves
Hamiltonicity for every palette size $k\ge 4$ for planar graphs of girth at least five in each
of these classes:

- $D(G)\le 11$;
- at most seven vertices of degree at least four, with unrestricted degrees;
- at most thirty-five distinct 5-cycles;
- two-degenerate graphs with $D(G)\le 15$ or at most thirty-nine distinct 5-cycles;
- graphs whose blocks are subcubic.

The corresponding Hamiltonian threshold is four in every listed class. The block-subcubic result
and the corollary that at most eleven distinct 5-cycles imply two-degeneracy are retained. For all
planar graphs of girth at least five, the unrestricted bounds

$$
4\le h(P_5)\le 5,\qquad 4\le h_c(P_5)\le 5
$$

remain open.

The paper also gives necessary conditions for a vertex-minimal counterexample to the unrestricted
four-colour Hamiltonian assertion: at least thirty-six distinct 5-cycles, at least eight vertices of degree at least four, and $D(G)\ge 12$. A degree-two vertex forces at least forty distinct 5-cycles
and $D(G)\ge 16$; when it is unique, the bounds become forty-two and sixteen.

## The paper

The manuscript is in the repository root:

- `main.pdf` is the compiled article;
- `main.tex` is the main LaTeX source and loads the certificate appendix body from
  `Codes/article_certificates_body.tex`;
- `main.tex` contains the bibliography and the article's analytic proofs;
- `Codes/article_certificates.tex` and `Codes/article_certificates.pdf` provide a
  standalone rendering of the finite certificate appendices.

## Finite certificates

The `Codes/` directory contains the literal finite data and exact Python readers used by
Appendices A--J. The readers check finite legality, coverage, selected cycles and seeds, protected
edges, physical aliases, interfaces, and clique trees. The unbounded lifting, product, splicing,
and structural-induction arguments remain analytic arguments in the article.

Fourteen reader suites cover the shared-hub, degree-two, pentagonal-reservoir, extended-cycle,
bowtie, and hinged-pair families, including independent physical-interface checks. See
[`Codes/README.md`](Codes/README.md) for the data contracts and reader responsibilities.

## Repository layout

```text
main.pdf                         Compiled manuscript
main.tex                         Main LaTeX source, bibliography, and analytic proofs
Codes/
├── article_certificates.pdf     Standalone certificate appendix
├── article_certificates.tex     Standalone rendering wrapper
├── article_certificates_body.tex  Appendix A--J body loaded by main.tex
├── data/                         Literal finite certificate inputs
├── verify_all.py                 Runs the finite readers
└── verify_*.py                   Exact primary and independent readers
```

## Build

From the repository root, compile the two final PDF documents with pdfLaTeX:

```sh
pdflatex main.tex
pdflatex main.tex
cd Codes
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```
