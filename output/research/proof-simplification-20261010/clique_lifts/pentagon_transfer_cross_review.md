# Independent read-only mathematical check of analytic_factor_transfer.tex

Checked the complete candidate and the protected-product setup in the
main manuscript (lines 1628–1638 and 1686–1717 at review time).
No edits to either file were made by this reviewer.

The analytic transfer passes this elementary mathematical review.
It is not formal verification or a formal MRS review.

## External theorem quantifiers

- Egawa–Furuya–Ozeki, Theorem A, PDF page 2, states the Akiyama–Avis–Era
  criterion: a graph has a {P2,P3}-factor iff i(G-X) <= 2|X| for every
  X subset V(G). Source: https://tgt.ynu.ac.jp/ozeki/2015EFO.pdf
- Ellingham–Zha, Theorem 3.5, PDF page 9, has the case g>=2,k>=2:
  c(G-S) < (k-1)|S|+3 for every S subset V(G). Its conclusion applies
  to the specified spanning subgraph F, gives c(F)-1 added edges, and
  limits the number of those edges at each physical vertex to k.
  Thus g=2,k=3 gives exactly the claimed added load 3.
  Source: https://math.vanderbilt.edu/ellingmn/paper/ttw/b-eps.pdf

## Local cut proof

Representatives of different Y-S components at a fixed s cannot change
the same original coordinate: the resulting states would be adjacent.
For distinct coordinates, two legal moves fail to commute exactly when
the original vertices are adjacent and the target colours agree. Three
pairwise noncommuting representatives would therefore create a triangle
in the original graph. Hence alpha(C_s)<=2.

For a fixed component D, commuting partners have distinct coordinates,
so their double-move states are distinct. Each double state is adjacent
to both component representatives. It must lie in S, otherwise the two
components are joined in Y-S. It is also distinct from s. Therefore
d_C_s(D)+1 <= b(D). Caro–Wei and summation over s give
c(Y-S)<=2|S| for every nonempty S.

The argument requires Y to be an entire component of the complete
fixed-list recolouring graph. An arbitrary connected subgraph or filtered
state set would not justify retaining the double-move states in Y.
The candidate states this full-component scope correctly.

## Empty and extreme cuts

- S empty: a nontrivial connected Y has i(Y)=0 and c(Y)=1<3.
- S=V(Y): the empty graph has i=c=0, satisfying both criteria.
- Y of order 2: the factor consists of P2 and no added edges are needed.
- A factor with one component: its contracted tree is a single vertex;
  the product seed itself is the finished protected cycle.

For a specified F, the connected quotient has c(F) vertices and c(F)-1
edges, so it is a tree. In parent-before-child order, a parent physical
row has used at most two splice edges before its current edge (total
physical added degree at most 3), and the fresh child factor block has
used none. Choosing any three distinct last-six pool edges therefore
always leaves an available common edge for the ordinary two-edge switch.

The P2/P3 initial product cycles preserve all last-six pool edges and
K_A. For Hamiltonian A, the two joins of the P3 seed use the distinct
first two pool edges. For hard A, the already supplied P2/P3 seeds have
the stated common internal edges in every row. No arbitrary strip length
or replacement of protected interfaces is being inferred.

## Listed C5 has no isolated states

Every proper colouring of five vertices with a four-colour palette
repeats a colour. The repeated vertices are nonadjacent and hence have
a common neighbour on C5. At that neighbour only their common colour
is forbidden, so a list of size at least 3 retains at least 2 colours,
one different from the current colour. Thus every state has a legal move
within the complete fixed-list graph. All its components are nontrivial.

## Scope retained

The analytic lemma does not imply Hamiltonicity of arbitrary full
recolouring graphs. The product conclusion still requires the existing
23 component cycles/seeds, the exact K_A sets and pools, and all 313
protected-interface identities. Only the path-factor table and arbitrary
strip-length construction cease to be proof premises.
