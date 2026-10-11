# Deletion-count simplification of the path232 safe-edge proof

The complete candidate replaces the ten-entry safe-common-edge table by
one cycle-deletion inequality, six common-graph capacity counts, and three
square/hexagon support arguments. It preserves all three original cycle
words and every allowed colour image and path reversal. No main file was
edited. The compact v2 has the same mathematical assertions as full v1.

The inequality is general: when a cycle loses q outside path components,
it retains n−q edges on the common vertex set. Each cycle loses at most f
forbidden edges, and both eligible edge sets fit in a universe of size
m−f−k if k other edges are used by neither. Inclusion–exclusion gives
2n−q_C−q_D−m−f+k. The outside set may be empty, with q=0. Its nonempty
components are paths because the common vertex set is nonempty.

The common-grid counts have direct list proofs. With Q_A denoting the
palette minus A, the common endpoint/middle lists are:

| Interface | Left / middle / right lists | Fixed-middle layers | Middle-edge multiplicities |
|---|---|---|---|
| aab→aac | Q_a / Q_a / Q_{b,c} | C4,C4,K2 at b,c,d | 2,1,1 |
| aab→acb | Q_a / Q_{a,c} / Q_b | K2×K3,C4 at b,d | 2 |
| aab→cab | Q_{a,c} / Q_a / Q_b | K3,C4,K2 at b,c,d | 2,0,1 |
| abc→abd | Q_a / Q_b / Q_{c,d} | K3,C4,C4 at a,c,d | 2,2,2 |
| aab→bab | Q_{a,b} / Q_a / Q_b | K2×K3,K2,K2 at b,c,d | 2,2,0 |
| aba→cba | Q_{a,c} / Q_b / Q_a | K2×K3,C4,K2 at a,c,d | 4,2,1 |

Each fixed-middle layer is a complete Cartesian grid. A bridge between
middle colours v,v′ allows precisely |L\{v,v′}|·|R\{v,v′}| endpoint
pairs. This proves every graph-size count without a state-graph kernel.
Special-edge counts follow from the natural E special edges bcd–dcd and
bdc–cdc, including the target special set in the E–E interface.

The new substantive omission mechanisms are:

- E–M: the two row triangles of the common middle-b prism each have one
  E edge. M0 uses two edges including it; M1 uses one edge. Thus either
  selected orientation leaves at least one row edge unused by both.
  Their outside component count is at most 2+3, giving 20−5−15+2=2.
- M–A: both M directions isolate bab within the middle-a grid, while
  A(cba) uses bab–dab there. Both therefore omit bab–bac and bab–bad.
  Every inter-grid edge of M/A has the excluded middle-boundary colour b
  at an endpoint, so dad–dcd is also absent. Both outside component
  counts are two, giving 24−4−21+3=2.
- A–A endpoint: both cycles omit the two middle-a triangle edges at bab.
  This turns a coarse lower bound of one into 22−4−17+2=3.

These omissions are properties of the original selected cycle families.
The proof does **not** say that every Hamilton cycle in a path232 fibre
has these supports or shares two safe edges. E/A edge-set uniqueness and
the two M orientations follow from their fixed-boundary stabilizers; the
direct nine-family classification preserves the original universal
quantifier over all allowed cycles.

The full v1 contains twelve explicit deletion-class path identities.
The exact checker reads those paths from TeX, verifies every vertex and
edge against the frozen cycles, and checks six retention families under
384 colour/reversal actions. Previously frozen independent support checks
cover another 288 actions, including all four M–M orientation pairs.
These are consistency checks for the analytic proof, not its replacement.
No Hamilton-cycle search was performed.

Editorial comparison: after stripping TeX commands/comments, the current
proof plus target conventions/table has 408 alphabetic tokens, full v1
881, compact v2 653. This metric counts symbolic words but excludes the
old numerical triple words, so it is only approximate. The candidate is
a method simplification and removes all ten interface edge records and
orbit bookkeeping; it is not yet a demonstrated page-count saving.
The original three cycle words and their support properties remain proof
input. The safe-edge lemma statement and all downstream bad-block and
lifting arguments are unchanged.

Frozen artifacts: `table-free-safe-proof-candidate-v1.tex` and its exact
record; `table-free-safe-proof-candidate-v2.tex` and its literal readback.
Independent pure-proof review is assigned to restoration_simplify.
