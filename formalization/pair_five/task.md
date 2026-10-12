# Chapter 4 adjacent-pair certificate replay

Reproduce the finite input for the adjacent-pair fibre lemma in Chapter 4.
The generator reads the literal Appendix A words from
`supplement/article_certificates.tex`, checks the seven representative types,
and writes `pair_five_data.json`. `PlanarRecoloring/PairFive.lean` contains the
corresponding literal path tables and rechecks their coverage, adjacency,
normalised small-list interface exits, Hamilton paths, and Hamilton cycles in
Lean's kernel.

The result is an exact finite replay. It does not formalise the planar Euler
arguments, the external three-colouring theorem, or the arbitrary-length
induction in the article.
