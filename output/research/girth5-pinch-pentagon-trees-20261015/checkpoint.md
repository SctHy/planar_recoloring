# Girth-five frontier: move bound and pentagon trees (2026-10-15)

Request: continue the research on `h(P_5)`. Outcome: **not resolved**. The
bounds `4 <= h(P_5) <= 5` and `4 <= hc(P_5) <= 5` in `main.tex` are unchanged.
Sections 1 and 2 contain analytic proofs. Section 3.1 is a conditional
connectivity argument; 3.2 contains finite checks and 3.3 is a proposed
induction, not a Hamiltonicity proof. Nothing here is used by the article.
The [review](review.md) corrects the tree interpretation and records the
verification scope, including concrete configurations absent from the scans.

## 1. Every 4-colouring has at least six moves

**Proposition.** Let `G` be a connected planar graph of girth at least five
that contains a cycle or has at least four vertices. Every proper 4-colouring
of `G` admits at least six single-vertex recolourings, and at least eight if
`delta(G) >= 3`. Thus `delta(R_4(G)) >= 6` (respectively `>= 8`). In
particular `R_4(G)` has no frozen colouring, and no colouring with fewer than
six moves.

*Proof.* Embed `G`. Every facial walk has length at least five, and a facial
walk of length five is a 5-cycle: if `G` has a cycle, each facial walk
contains one, and a tree has a single face of length `2(n-1) >= 6`. Fix a
proper 4-colouring. In every 5-cycle some vertex has its two cycle neighbours coloured alike (a
*pinch*): five vertices carry at most four colours, and equal colours sit at
distance two. Give each vertex `2d-6` and each face `l-6`; by Euler the total
is `-12`. Every 5-face takes 1 from one of its pinch vertices. A 5-face meets
`v` in one angle, and distinct 5-faces use distinct angles. Hence `v` pays at
most the number of its angles whose two neighbours agree. If `v` sees `s >= 2`
neighbour colours, the cyclic neighbour sequence has at least `s` colour
changes, so `v` pays at most `d-s`. If `s = 1`, it pays at most `d`, and a leaf
pays nothing. Faces end non-negative. The defects `6-2d+p(v)` therefore sum to
`12 + sum_{l>=6}(l-6) >= 12`. With `m(v) = 3-s` legal moves at `v`, the cases
`s = 3, 2, 1` give a defect of at most `2m(v)` for every vertex. For `d >= 3`
the bound is at most `1.5 m(v)`. Summing gives `M >= 6`, respectively
`M >= 8`. ∎

The bound six is attained by `C_5` (colouring `0,1,2,3,1`) and by `C_6`.
Exhaustive enumeration of all 168,506,880 proper 4-colourings of the
dodecahedron (scratch run, not in the reproducer) gives minimum 10, matching
the 2026-10-14 SAT value. It is not known whether eight is attained for
`delta >= 3`.

Consequence: the degree-one route to `h(P_5) = hc(P_5) = 5` is closed. A
non-Hamiltonian `R_4(G)` would need a global obstruction. As a consistency
check, a scan of all 3-connected girth-five duals of `plantri -pm5` polytopes
with at most 24 faces (about 226,000 graphs) found no colouring with at most
one move (scratch, superseded by the proposition).

## 2. Unavoidable configurations for minimum degree three

**Lemma.** Every plane graph of girth at least five and minimum degree at least
three contains one of:

- **C1** a 5-face whose vertices all have degree 3;
- **C2** an *apex face* (a 5-face with four degree-3 vertices) whose fifth
  vertex `u` has degree 4, such that the face opposite it at `u` (the face at
  `u` meeting it only in `u`) is a 5-face;
- **C3** a degree-5 vertex incident with four apex faces.

*Proof.* Suppose not. Charge `2d-6` to vertices and `l-6` to faces, where a
face length counts all its boundary components. The total is `-6(1+c)<0`,
with `c` the number of connected components. Every facial boundary walk
has length at least five, so every face of length five is a 5-cycle.
A vertex of degree at least four gives 1 to each incident apex face
whose other four vertices have degree 3, and 1/2 to every other incident
5-face. A 5-face has a vertex of degree at least four (no C1). With one such
vertex it gets 1, and with two or more it gets at least 1/2 each. A degree-4
vertex that gives 1 to a face gives 0 to the opposite face (no C2), so it pays
at most 1 to each opposite pair, at most 2 in total. A degree-5 vertex gives 1
to at most three faces (no C3), so at most `3 + 2/2 = 4`. A vertex of degree
`d >= 6` keeps `d-6 >= 0`. All charges end non-negative, a contradiction. ∎

PI shows C2 and PH shows C3; there neither C1 nor the other configuration
occurs. The lemma is a coarsening of the discharging in Bartier et al.,
SIDMA 37 (2023), Section 3.3. That discharging uses only the absence of their
two configurations, so it gives the sharper unavoidable set used below. Call
a vertex of a 5-face `f` *bad* if it has degree 3, or has degree 4 and the
5-face opposite `f` there has all its other vertices bad. Here the induction
means the least closure starting with degree-3 vertices, not a circular
assignment of bad labels. Every such graph contains

- **U1** a 5-face all of whose vertices are bad, or
- **U2** a degree-5 vertex incident with four 5-faces whose other vertices are
  all bad.

Unfolding the induction gives an abstract tree of face occurrences, with
opposite pairs at degree-4 junctions. It does not prove that the induced
union in `G` is a tree of otherwise disjoint pentagons: different branches
can share degree-3 vertices or edges, and extra internal edges can occur.
The review gives explicit plane girth-five examples. In the bare abstract
model, call the face union a *pentagon tree*. A single face is C1, and the
smallest non-trivial example is the *bowtie*, two apex faces opposite at one
degree-4 vertex. Applying this model to every U1 requires further work.

## 3. Fibre robustness of the deleted configurations

Delete a configuration `X`. A *port* is an outside neighbour, and a boundary
word colours the ports. A fibre component is *killable* by a move (port `p`
to colour `b`) if every state of the component gives colour `b` to an
`X`-neighbour of `p`. If two such moves are legal in the outside graph and
are the two cycle edges at that boundary colouring, that component has no
cross edge in the layered graph. This is the 2026-10-14 obstruction; abstract
killing moves alone do not establish the requisite bottom cycle.

**3.1 Component-graph principle.** Lift along a bottom Hamilton path. If no
fibre component is killable and some layer has a connected fibre, the
component graph is connected. *Proof:* walk from any component one layer at
a time towards that layer; non-killability supplies each step, and all walks
end at its unique component. ∎ Non-killability here must cover every actual
bottom move, including moves at shared ports. This uses the walking idea of
Claim 3 of `lem:pentagon-component-graph`; unlike that claim's separate
factor-reset argument, it assumes one connected whole layer. It proves
connectivity only.

**3.2 Exact results** (all boundary words, canonical under colour permutation;
ports distinct; `X` vertices of degree 3 unless stated; the induced graph
has exactly the listed face-union edges, with no other identifications):

| deleted configuration | `|X|` | ports | words | disconnected fibres | components killable by >= 2 moves | min component |
|---|---:|---:|---:|---:|---:|---:|
| subcubic pentagon (C1) | 5 | 5 | 51 | 1 (constant: 2×15) | 0 | 15 |
| apex 5-cycle, degree-4 apex | 5 | 6 | 187 | 5 | 2 | 1 |
| bowtie | 9 | 8 | 2,795 | 0 | 0 | 680 |
| bowtie, a degree-4 non-junction neighbour of `u` on the second face | 9 | 9 | 11,051 | 4 | 4 | 1 |
| bowtie, a degree-4 non-junction far vertex on the second face | 9 | 9 | 11,051 | 4 | 4 | 1 |
| 3-face chain, junctions at distance 2 on the middle face | 13 | 11 | 175,275 | 0 | 0 | 14,148 |
| 3-face chain, junctions adjacent on the middle face | 13 | 11 | 175,275 | 0 | 0 | 12,840 |
| PI flower (degree-4 centre, 4 apex faces) | 13 | 8 | 2,795 | 0 | 0 | 37,168 |
| C3 (degree-5 centre, 4 apex faces) | 14 | 10 | 43,947 | 0 | 0 | 46,976 |

The first five rows are checked by the standard-library reproducer and were
reproduced byte for byte in the review. The last four rows were also replayed
in full; inputs, all 32 shard outputs and coverage checks are saved in
`review-c-replay.json`. All listed counts and minima agree. Among the
reported bare pentagon trees, only the
tested **non-trivial** trees have connected fibres for every boundary word:
C1 has two components at a constant boundary. A heavy non-junction vertex
can bring back doubly killable isolated states. Deleting the bare bowtie
removes this obstruction in that finite model; it does not establish a
general restoration theorem or cover every actual U1 union.

**3.3 Possible induction in the bare model.** Remove the four non-junction
vertices of a leaf face `g`, retaining `u`. Restriction gives layers over
the remaining list instance with constraints from the deleted vertices
removed; newly exposed neighbours are not fixed boundary colours. The layers
are list-colouring graphs of the path `g-u`, depending on `u`. Their sizes
can differ and some contain isolated states (see the review), so this is
not a uniform graph bundle. Constructing a suitable Hamilton cycle in the
remaining instance and controlling its interfaces are unproved obligations.

## 4. What is still missing for `h(P_5) = 4`

1. A proof of appropriate fibre connectivity and non-killability for all
   non-trivial pentagon trees and U2 flowers with attached trees, with C1
   handled by its two-component argument. The actual induced unions,
   including branch identifications and extra internal edges, also need
   coverage. Finite bare-model checks cannot settle these unbounded families.
2. Splicing material: a simultaneous choice of a Hamilton cycle for every
   connected fibre, with at least two actual shared internal edges at each
   consecutive bottom interface and both cross edges present. Then path-order
   splicing works with one configuration. Pairwise choices depending on the
   interface do not suffice; disconnected fibres need component-level
   splicing. This material has not been established.
3. Shared ports: an outside vertex adjacent to two `X` vertices at distance at
   least three changes two lists at once. Fibres are covered by the table
   above, which includes equal entries, but killability under such
   simultaneous changes is not.
4. Degree-2 vertices. A minimum counterexample may have them. The known
   reductions leave degree-2 vertices whose pairwise common neighbours have
   degree at least four. If there are at least two, their neighbourhoods form
   a star around one hub, or three vertices on a subdivided triangle.
   Section 2 needs `delta >= 3`, so these structures, as well as a lone
   degree-2 vertex, need their own reductions or discharging.

## 5. Reproduction

```sh
python3 output/research/girth5-pinch-pentagon-trees-20261015/pinch_tree_scan.py
```

Standard library only, about three minutes. It rewrites
`pinch-tree-report.json` and imports the PI/PH construction from
`../girth5-apex-pentagon-20261014/`. The larger rows of 3.2 use the optional C
classifier. For split runs with `K r`, sum the event counts and `processed`,
take minima/maxima of extrema, and weight averages by `processed`.
Each shard's `words` is already the global canonical-word count; do not sum it.

```sh
D=output/research/girth5-pinch-pentagon-trees-20261015
cc -O3 -o /tmp/fibre_classifier $D/fibre_classifier.c
python3 $D/fibre_configs.py C3 | /tmp/fibre_classifier   # or: ... | /tmp/fibre_classifier 10 r
```

No row of 3.2 has a component killable by exactly one move.

The plantri scan and the dodecahedron enumeration were scratch computations
outside the repository; they are not proof premises.
