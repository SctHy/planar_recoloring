# Root review of the complete selected-cycle count proof

This mathematical review concerns the frozen full candidate `table-free-safe-proof-candidate-v1.tex` (SHA-256 `0abf152168c79ac5d629adfee3ce5e0b4bd9d857648bfab209d0007c46be3450`) and compact v2 (`20d7b4914f5632fac3aac03f84fd4f6d66a310a155b0856748a9334d60e7683b`). It does not assert an arbitrary-Hamilton-cycle safe-edge theorem. Verdict: PASS, with the editorial clarification below required in an integrated version.

## General count and scope

For a simple cycle meeting a nonempty common vertex set U of size n, the vertices outside U induce paths **in the cycle**, not necessarily in the whole fibre. Deleting q such paths leaves n−q cycle edges on U, including q=0 when there are no outside vertices. If both retained edge sets lie in H, deleting the same forbidden universe F of size f loses at most f from each. Removing k other non-forbidden edges used by neither reduces the common safe universe to at most m−f−k. Inclusion–exclusion gives `2n−q_C−q_D−m−f+k`, with no omitted second F subtraction. This argument also allows H to contain unused extra edges.

In the compact proof, the phrases “outside vertices induce paths” and “classes induce P_i” must explicitly mean **in the respective selected cycles**. Otherwise a reader could mistake the claimed induced subgraph for the full list-colouring graph. This is a wording issue; the original full paths and count use cycle edges throughout.

## Exhaustive families and allowed-cycle quantifiers

After ordering E<M<A, E(aab) has eight labelled good neighbours: two aac, one abb, two acb, one bab, and two cab; the unused-colour transposition identifies each doubled family. M(aba) has two remaining same-type middle changes and four all-distinct end changes, grouped as aca and cba by reversal and unused-colour exchange. For A(abc), the two end changes to the unused colour are identified by reversal with a↔c, leaving abd and the middle change adc. Lower-type changes have already been handled. Thus the nine displayed families cover every good-to-good single-coordinate change.

The selected E cycle is fixed by unused-colour exchange; the selected A cycle is fixed by reversal with endpoint-colour exchange. Each therefore has one allowed edge set for a fixed boundary. M has precisely its two reversal images, both fixed by unused-colour exchange. The proof's two M directions retain the original universal quantifier over **all allowed cycles**, rather than choosing only a convenient target orientation.

## Six numerical families

For a fixed middle colour v, the common legal left and right lists form the Cartesian grid `K_|L\{v}| □ K_|R\{v}|`. Between middle colours v and v′, the number of common edges is `|L\{v,v′}| |R\{v,v′}|`. These formulas give all six H sizes (10/13, 10/15, 9/11, 11/17, 10/15, 12/21). The corresponding forbidden counts are 2,1,1,0,0,0: the E special edges are bcd–dcd and bdc–cdc; checking their list legality includes the target special set in the first family.

The twelve literal deletion profiles are consistent with the displayed original cyclic words. They give outside component sums 2,2,4,4, at most 5, and 4, including both M orientations. Relabelling the relevant coordinate class also gives each target profile; no new Hamilton-cycle existence assertion is needed.

The positive unused-edge counts have separate explanations:

- A(a,b,c) and A(a,b,d) omit both bab–cab and bab–dab in their common middle-a triangle, since the internal path at bab first changes its last coordinate.
- E(aab) and either M direction at bab use at most two edges in each row triangle of the common middle-b prism. The first M direction uses two and includes the E edge; the second uses one. Therefore each triangle contains an edge used by neither, proving k≥2 without fixing a target-specific shared-edge witness.
- M(aba) isolates bab within its middle-a grid in both directions; A(cba) begins that grid path bab,dab. Both omit bab–bac and bab–bad. All selected M/A middle-change edges have b in an endpoint coordinate, so neither uses dad–dcd. These three are legal, distinct, non-forbidden common-graph edges.

Substituting gives lower bounds 3,2,2,3, at least 2, and 2. The negative/positive counts are not claims about arbitrary Hamilton cycles of these graphs.

## The remaining three supports

For aab→abb, both cycles retain the two edges at bca in the common middle-c square; the special edges lie at the opposite corner dcd and are absent from the other cycle, so the two retained edges are safe. For abc→adc, each uses five of the same six-cycle edges, giving at least four common edges; both special sets are empty. For aba→aca, each M direction uses three of four edges in Q_d, giving at least two common edges; both special sets are empty. These arguments complete the original safe-common-edge lemma.

The change removes the ten individual shared-edge records and target-index/orbit bookkeeping. It retains selected-cycle support/deletion properties, six graph-capacity rows, and the original three cyclic words. It is a reduction in proof organization and pair-specific witnesses, not a claim that all finite input or all case distinctions disappear. A complete manuscript build and source-invariant audit are still separate requirements before integration.
