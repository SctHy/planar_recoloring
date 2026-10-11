# Six-reserve factor transfer and clique integration review

## Six-reserve version

The proposed version uses the proved cut bound and Akiyama–Avis–Era only
to obtain a P2/P3 factor F in each complete listed-C5 component B. Since
every B vertex has at least one factor neighbour, Delta(B)<=7 implies
that any selected quotient-tree connectors have physical load at most 6:

    degree_added(v) <= degree_B(v) - degree_F(v) <= 7 - 1 = 6.

Connectivity of B makes its factor quotient connected. Choose a spanning
tree with one actual B edge per quotient edge; all these edges are outside
F. The contracted tree has no cycles or repeated connections, so every
parent-before-child splice joins two currently disjoint product cycles.

For a Hamiltonian A, the P2/P3 block cycles use at most the original first
two pool edges, preserving the original last six and K_A in every row.
For hard A, the already specified two-/three-row seeds contain every D_A
edge in every row and therefore retain both K_A and the last six pool
edges. Their first special pool edge need not be used now; leaving it
unused does not change K_A, which was defined by removing all seven
pool edges.

At the current parent row at most five of its six reserved edges have
already been consumed. The fresh child factor block retains all six.
Thus the original ordinary two-edge switch applies without changing
any pool, K_A definition, seed, or protected-interface identity.
The 313 protected-interface witnesses remain verbatim valid because their
premises are the unchanged K_A sets.

Boundary cases: a single factor component has no connectors and its
P2/P3 seed already finishes the product; P3 middle rows have an even
stronger load bound 5, but the uniform bound 6 is sufficient. All fixed-list
listed-C5 components are nontrivial by the repeated-colour argument.

This version removes arbitrary-r strip construction and the 590-state
factor table as proof premises, exactly as the EZ load-3 version does.
It keeps the existing elementary maximum-degree-seven lemma. Since no
reserve or protected-set definition is reduced, introducing EZ Theorem
3.5 provides no further simplification for the manuscript. The load-3
version remains a valid stronger research candidate.

## Clique theorem integration

The unified clique-extension theorem has genuine exact content:
binary-interface bipartiteness is equivalent to absence of the sole
cyclic bridge-selection obstruction. Its three conclusions correctly
separate their hypotheses: cyclic bipartiteness is needed for its Hami/VP
arguments; HC uses E and R without that condition.

Nevertheless its underlying proof is the same path/cycle fibre method.
It does not lower k, remove the arrangement-graph branch, or remove reset.
Its benefits in Sections 2–3 are eliminating repeated proofs:

- Introduce available-list geometry once, replacing its definitions and
  overlap calculations in both degenerate proofs and single-HC lifting.
- Prove binary-interface bipartiteness once, replacing the VP exceptional
  parity chain and the one-vertex Hamiltonian lift's separate permutation
  argument.
- Prove the reset path and same-fibre endpoint constructions once, then
  obtain both degenerate HC and single-vertex HC by checking E and R.
- Prove local cycles 3–6 and the complete integer-interval coverage once;
  degenerate VP becomes an induction invoking the general conclusion.

The independent-set/product-fibre restoration lemmas in Section 3 are not
covered: their fibres are products, can be wholly binary, and use
reachable-set or edge-splice arguments. They must not be deleted on the
strength of the clique theorem.

For a manuscript focused on planar thresholds, a tailored one-vertex
lifting package could be more readable than introducing B_pq, E and R
as separate abstractions. If the abstract theorem is integrated, the old
duplicate proofs must actually be removed; retaining them would merely
add packaging. This is an exposition/maintenance improvement, whereas
the analytic path-factor transfer replaces finite factor dependence with
a universal structural argument.
