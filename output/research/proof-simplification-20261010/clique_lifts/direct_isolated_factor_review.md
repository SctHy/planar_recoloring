# Direct isolated-state proof of the listed path-factor lemma

Status: checked elementary proof; suitable replacement for the current
factor-lemma proof. No computation, main-manuscript edit, or formal MRS
review was performed. This review concerns the complete fixed-list
recolouring graph of a finite simple triangle-free graph with a finite
palette, and one of its entire nontrivial connected components Y.

## Proposed compact proof

Fix S subset V(Y), and let I be the isolated vertices of Y-S. Every
i in I has all its Y-neighbours in S and has positive degree
b(i)=d_Y(i), because Y is nontrivial and connected.
For s in S, put I_s=N_Y(s) intersect I. Distinct states in I_s
change different original coordinates: otherwise they are adjacent
in Y-S, contradicting isolation.

Let C_s be the graph on I_s whose edges join commuting moves.
Two legal moves at different coordinates fail to commute precisely
when their original vertices are adjacent and their target colours
agree. Thus alpha(C_s)<=2, since an independent triple would give
an original triangle. A commuting partner j of i gives a legal
double-move state adjacent to i. It belongs to Y by completeness
and connectedness, and lies in S because i is isolated in Y-S.
Different partners give different double-move states, none equal
to s. Hence d_C_s(i)+1 <= b(i).

The random-ordering proof of Caro–Wei gives

    sum_{i in I_s} 1/b(i)
        <= sum_{i in I_s} 1/(d_C_s(i)+1)
        <= alpha(C_s) <= 2.

Summing over s in S, every i contributes b(i) copies of 1/b(i).
Therefore i(Y-S)=|I|<=2|S| for every S. The Akiyama–Avis–Era
criterion gives a {P2,P3}-factor.

## Checks of the potentially hidden steps

1. A legal double move is a vertex of the complete fixed-list graph X.
   Since it is adjacent to i in the entire component Y, it is in Y.
   Completeness alone establishes membership in X; the edge establishes
   membership in the chosen component. This should be stated or kept
   clearly implicit, rather than applied to a filtered connected subgraph.
2. If the double state were outside S, its edge to i would contradict
   isolation of i in Y-S. No representative-component argument is needed.
3. Distinct j change distinct coordinates. Holding i's first move fixed,
   their double states have distinct second changed coordinates, so all
   are distinct. Each changes two coordinates from s and is not s.
4. Thus those double states plus s are d_C_s(i)+1 distinct neighbours
   of i, all counted by b(i)=d_Y(i).
5. Summation is exact: N_Y(i) subset S and |N_Y(i)|=b(i), so every
   isolated i is counted with total weight exactly one.
6. S empty: I empty since Y is nontrivial connected. S=V(Y): I empty
   because no vertices remain. Both cases fit the same empty sums.
7. The claimed conclusion remains the P2/P3 factor, not the stronger
   full component cut bound c(Y-S)<=2|S|. The latter is still valid in
   the separately saved research candidate, but is unnecessary here.
8. The following C5 no-isolated-state paragraph stays unchanged and
   shows that every listed C5 component satisfies nontriviality.

## Simplification gain

This removes c(Y-S), deletion components D, chosen representatives i_D,
the component boundary quantities b(D), and the final passage from the
full cut bound to the isolated-vertex bound. It keeps the same elementary
commutation/Caro–Wei mechanism and only the AAE external criterion.
It is strictly sufficient for the integrated six-reserve product proof.

AAE criterion reference checked earlier: Egawa–Furuya–Ozeki Theorem A,
PDF page 2, https://tgt.ynu.ac.jp/ozeki/2015EFO.pdf.
