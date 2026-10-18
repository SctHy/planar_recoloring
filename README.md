# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

The manuscript and the finite certificate readers for the paper *Hamiltonian and Hamilton-connected thresholds
for planar recolouring graphs*.

## Recolouring graphs

For a graph $`G`$ and a palette of $`k`$ labelled colours, the recolouring graph $`\mathcal R_k(G)`$ has the
proper colourings of $`G`$ as vertices, and two colourings are adjacent when they differ at one vertex of $`G`$.
A Hamilton cycle in $`\mathcal R_k(G)`$ is a cyclic listing of all proper colourings in which successive
colourings differ at one vertex, a colouring Gray code. The graph $`\mathcal R_k(G)`$ is Hamilton-connected if it
has a Hamilton path between any two of its vertices, and vertex-pancyclic if every vertex lies on a cycle of each
length from $`3`$ to the number of vertices.

For a class $`\mathcal C`$ of graphs, the Hamiltonian threshold $`h(\mathcal C)`$ and the Hamilton-connected
threshold $`\mathrm{hc}(\mathcal C)`$ are the least $`q`$ such that $`\mathcal R_k(G)`$ is Hamiltonian,
respectively Hamilton-connected, for every $`G\in\mathcal C`$ and every $`k\ge q`$.

## Main results

- If $`G`$ is nonempty and $`d`$-degenerate and $`k\ge d+3`$, then $`\mathcal R_k(G)`$ is Hamilton-connected and
  vertex-pancyclic. The palette bound $`d+3`$ is sharp for both properties and for Hamiltonicity.
- The common Hamiltonian and Hamilton-connected thresholds are $`7`$ for planar graphs, $`5`$ for triangle-free and
  bipartite planar graphs, and $`4`$ for planar graphs of girth at least six and for forests. The table also gives
  the palette sizes proved for vertex-pancyclicity.

| Graph class | Threshold | Vertex-pancyclic for |
| --- | --- | --- |
| Planar | 7 | $`k\ge 8`$ |
| Triangle-free planar, bipartite planar | 5 | $`k\ge 6`$ |
| Planar, girth at least six | 4 | $`k\ge 5`$ |
| Forests | 4 | $`k\ge 4`$ |

Write $`\mathcal P_5`$ for the planar graphs of girth at least five and

$$
D(G)=\sum_{v\in V(G)}\max\left\lbrace\deg_G(v)-3,0\right\rbrace .
$$

The article proves that $`\mathcal R_k(G)`$ is Hamiltonian for every $`k\ge 4`$ for $`G\in\mathcal P_5`$ in each of
these classes, so the uniform Hamiltonian threshold is four in each of them:

- $`D(G)\le 10`$;
- at most seven vertices of degree at least four, with unrestricted degrees;
- at most thirty-three distinct $`5`$-cycles;
- two-degenerate graphs with $`D(G)\le 13`$;
- graphs whose blocks all have maximum degree at most three, so cutvertices may have arbitrarily large degree.

Hamilton-connectedness remains open for these four-colour classes. The article also shows that a planar graph of
girth at least five with at most eleven distinct $`5`$-cycles is two-degenerate.

For all of $`\mathcal P_5`$ the thresholds are not determined:

$$
4\le h(\mathcal P_5)\le 5,\qquad 4\le \mathrm{hc}(\mathcal P_5)\le 5 .
$$

A minimum counterexample to four-colour Hamiltonicity in $`\mathcal P_5`$ must have at least thirty-four distinct
$`5`$-cycles, at least eight vertices of degree at least four, and $`D(G)\ge 11`$. If it contains a degree-two
vertex, it has at least thirty-four distinct $`5`$-cycles and $`D(G)\ge 14`$, and if that vertex is unique these
bounds become forty-two and sixteen.

## The paper

The manuscript is in the repository root:

- `main.pdf`, the compiled article;
- `main.tex`, the LaTeX source with the bibliography and the analytic proofs, which loads
  `Codes/article_certificates_body.tex` as Appendices A--J;
- `Codes/article_certificates.tex` and `Codes/article_certificates.pdf`, a standalone rendering of the finite
  certificate appendices.

Each document is compiled with pdfLaTeX, run twice:

```sh
pdflatex main.tex
pdflatex main.tex
cd Codes
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

## Repository layout

```text
main.pdf                           Compiled manuscript
main.tex                           Main LaTeX source, bibliography, and analytic proofs
Codes/
├── README.md                      Reader groups, data format, and how to run the readers
├── article_certificates.pdf       Standalone certificate appendix
├── article_certificates.tex       Standalone rendering wrapper
├── article_certificates_body.tex  Appendix A--J body loaded by main.tex
├── data/                          Literal finite certificate inputs
├── verify_all.py                  Runs all finite readers
├── verify_*.py                    Exact primary and independent readers
└── *_core.py                      Shared parsing and model helpers
```

The readers use Python 3.10 or later and the standard library only. They check finite local evidence: legality,
coverage, selected cycles and seeds, protected edges, physical aliases, interfaces, and clique trees. The lifting,
product, splicing, and structural-induction arguments remain analytic arguments in the article. Reader reports are
temporary and are not included in the repository; see [`Codes/README.md`](Codes/README.md) for the command that
regenerates them.
