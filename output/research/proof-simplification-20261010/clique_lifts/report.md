# Clique lifting investigation

The proved candidate in `unified_clique_lift.tex` defines binary interface
graphs B_{pq}. Their bipartiteness is exactly equivalent to existence of
proper cyclic bridge labels on every base cycle. For actual recolouring
fibres, one short permutation-sign lemma proves all these graphs bipartite.
A single clique-extension theorem then supplies Hamiltonian,
vertex-pancyclic, and Hamilton-connected lifting, with explicit extra
conditions E (each available colour has an external neighbour) and R
(every near-spanning path has a three-element intersection).

This is a proved abstraction of the existing method, not a new threshold
proof. It does not remove the complete-graph arrangement branch or prove
that R may be discarded.

## Attempted stronger shortcut

The exact script exhausts the K3 base with all three-element lists from a
five-element palette, up to permutation of the three base vertices. It
checks interfaces of size at least two, condition E, and absence of the
binary odd-cycle obstruction. All 30 admissible classes are
Hamilton-connected. This is only bounded evidence for dropping R; no
universal conclusion follows. Python 3.14.3 standard-library memoized
Hamilton-path search was used; local Mathematica and Sage executables were
unavailable. K3, C4, and the known common-pair odd obstruction serve as
elementary boundary checks.

An attempted proof of vertex-pancyclicity using a doubled Hamilton path,
instead of vertex-pancyclic induction, encounters a concrete obstruction:
at an internal fibre whose incoming and outgoing interfaces are both the
same forced pair {p,q}, two vertex-disjoint strands must be the singleton
vertices p and q. They cannot also cover a third fibre vertex. Thus simple
out-and-back path lifting does not replace the cyclic argument. A path on
three base vertices with lists {p,q,r_i} illustrates the obstruction.

## HC does not replace VP

The Wagner graph, with vertices Z/8Z, edges i--(i+1), and i--(i+4), is
Hamilton-connected and triangle-free. By dihedral symmetry it suffices to
join 0 to 1,2,3,4, respectively, with these Hamilton paths:

- 0,4,5,6,7,3,2,1
- 0,1,5,4,3,7,6,2
- 0,4,5,1,2,6,7,3
- 0,1,2,3,7,6,5,4

Every consecutive difference is +/-1 or 4 modulo 8. The three neighbours
of any vertex are pairwise nonadjacent, so there is no triangle. Therefore
the general implication Hamilton-connected => vertex-pancyclic is false.
This is a complete elementary counterexample, not an extrapolation from
the finite search.

## Status

- Binary-interface equivalence and the conditional extension theorem:
  elementary proofs supplied; not formally verified.
- Recolouring binary-interface bipartition: elementary proof supplied.
- Drop R from Hamilton-connected lifting: unresolved candidate.
- Obtain VP from HC alone: disproved by the Wagner graph.
- Doubled-path replacement: the proposed simple construction fails at
  consecutive identical binary interfaces.
- Main manuscript and formal research records: unchanged by this agent.
