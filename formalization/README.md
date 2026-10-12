# Lean 4 formalization scope for `main.tex`

This directory contains the independently compilable Lean 4 core formalization
accompanying the article. The project fixes Lean 4.34.1 and depends only on `Std`,
which is distributed with Lean; mathlib is not required.

The following items have been checked by the kernel:

- `PlanarRecoloring/Core.lean` defines Boolean adjacency matrices for finite graphs,
  proper colourings, single-vertex recolouring adjacency, available colours, and the
  coverage condition for explicit list paths;
- `PlanarRecoloring/General.lean` adds interfaces for loopless symmetric simple graphs,
  list-based degeneracy, colour permutations, and preservation lemmas for properness and
  available colours after recolouring;
- `PlanarRecoloring/Hamilton.lean` defines list versions of Hamilton paths, Hamilton
  cycles, Hamilton-connectedness, and vertex-pancyclicity, and proves endpoint and
  coverage helper lemmas; reversal of list paths under symmetric relations and endpoint
  exchange for Hamilton paths are also checked by the kernel. `HamiltonPathOn.splice`
  proves the generic disjoint-path cut-and-join cycle step with explicit cross edges;
- `PlanarRecoloring/Fibre.lean` encodes a strict abstraction of the fibre-splicing
  interface in the article as `FibrePath`. It proves that disjoint fibre paths with
  different internal relations on the two sides can be spliced across an interface edge
  while preserving coverage, no repetition, and consecutiveness;
- `PlanarRecoloring/FibreChain.lean` generalizes this interface to any nonempty fibre
  chain, proving that the flattened path preserves coverage, no repetition, endpoints,
  and bridge consecutiveness, and can form a `ClosedFibrePath` across a closing bridge;
- `PlanarRecoloring/FibreHamilton.lean` connects fibre paths covering a finite graph's
  vertex set to the `HamiltonPath`/`HamiltonCycle` definitions and provides
  `HamiltonPathOn`/`HamiltonCycleOn` conversions for explicit lists, together with
  reversal of a supplied fibre path under a symmetric relation; all path-existence
  assumptions remain explicit inputs;
- `PlanarRecoloring/Extension.lean` represents restoration of one vertex with
  `Option (Fin n)`, proves the available-colour criterion for a proper extension,
  single-fibre recolouring adjacency, and cross-fibre adjacency for a shared colour, and
  encodes base-graph edges that preserve the restored vertex colour as `RestorationBridge`,
  lifting a closed fibre chain to a relation-level Hamilton-cycle certificate in the
  restored graph;
- `PlanarRecoloring/PermutationParity.lean` formalizes the six-state recolouring graph
  of `K_2` for `d=1,k=3`: every legal edge flips the parity of the three-colour
  permutation, so no six-vertex Hamilton path joins the specified endpoints, and the
  graph is triangle-free;
- `PlanarRecoloring/ProductParity.lean` defines single-coordinate flips for binary
  products represented by `List Bool`, proves that a flip changes xor parity, parity
  propagates along paths, even paths preserve endpoint parity, path length is preserved,
  and paths can be reversed, connects explicit `HamiltonPathOn` paths to this parity
  interface, and rules out odd cycles;
- `PlanarRecoloring/BinaryHamilton.lean` gives a kernel-checked reflected Gray-code
  enumeration of every binary product vertex, proves its spanning path and endpoint
  parity for the canonical endpoints, and supplies the constructive binary-product
  fragment used by the Section 3 product lemma;
- `PlanarRecoloring/BinaryEndpoints.lean` adds generic path concatenation and insertion
  operations and constructs binary-product spanning paths for arbitrary prescribed
  opposite-parity endpoints;
- `PlanarRecoloring/BinaryEndpointParity.lean` proves the exact fixed-length Boolean
  endpoint equivalence (for nonempty words): a spanning path exists exactly when the
  endpoint xor parities differ;
- `PlanarRecoloring/ArrangementParity.lean` records the completed-arrangement model,
  exchange-relation symmetry, inversion-parity append interface, and the generic
  edge-flip triangle obstruction. It also proves inversion parity flips under each
  adjacent exchange and derives the finite bipartite Hamilton-connected obstruction;
- `PlanarRecoloring/TernaryProduct.lean` proves Hamilton-connectedness of the
  binary-word graph product with `K_3` for every word length, with explicit state
  enumeration and coverage;
- `PlanarRecoloring/P3Strip.lean` gives a literal 24-state Hamilton cycle for
  `R_3(P_3) □ P_2`, the finite two-layer base case of the Chapter 4 bad-run
  construction. The arbitrary-length strip induction remains open;
- `PlanarRecoloring/CompleteFibreCycle.lean` constructs complete-fibre Hamilton paths
  from duplicate-free finite layer lists and endpoint witnesses, then closes them
  with explicit cyclic bridge hypotheses;
- `PlanarRecoloring/Restoration.lean` proves the abstract two-fibre component-label
  reset reachability and the fresh protected-port inequality used by bounded-degree
  tree splicing;
- `PlanarRecoloring/StarObstruction.lean` formalizes the stated star recolouring edge:
  it is a legal edge with no common adjacent state (hence no triangle), and the star is
  1-degenerate;
- `PlanarRecoloring/Chapter4.lean` proves the isolated-state obstruction used by the
  Chapter 4 sharpness arguments: a frozen recolouring state cannot be an endpoint of a
  spanning path to another state or lie on a Hamilton cycle over a symmetric state
  relation;
- `PlanarRecoloring/P3Obstruction.lean` gives the twelve-state encoding of the
  three-colour recolouring graph of `P_3` and a kernel-checked bounded search proving
  that it has no spanning cycle;
- `PlanarRecoloring/PairFive.lean` replays the seven Appendix A fibre types, their
  representative cycles and endpoint paths, the complete list of 15 small masks, and
  the indexed interface-exit certificate;
- `PlanarRecoloring/PairFiveTransport.lean` proves that the finite certificates are
  preserved by the recorded colour permutations and coordinate swaps, yielding the
  Hamilton-connected, edge-on-cycle, and one-interface Hamilton-path statements for
  every labelled small-mask pair;
- `PlanarRecoloring/PairFiveReset.lean` proves the arbitrary finite adjacent-pair reset
  from those interface hypotheses. It tags each layer before flattening, so equal
  assignments in different fibres remain distinct vertices, and returns a genuine
  `HamiltonPathOn` certificate;
- `PlanarRecoloring/PairFour.lean` replays canonical Hamilton cycles for all labelled
  three-by-three four-colour fibres and checks the two-common-edge invariant for every
  allowed one-list transition. The subsequent base-cycle splice remains an explicit
  hypothesis, as in the article's proof;
- `PlanarRecoloring/FaceIdentity.lean` proves the integer algebra behind the
  five-face and subcubic face-count identities once their face-length,
  degree-sum, and Euler equations are supplied. It also proves the resulting
  twelve-face arithmetic lower bound under nonnegative excess assumptions;
- `PlanarRecoloring/Bridge.lean` proves a three-layer local version of the article's
  Lemma `bridge-colours`: when the two outer layers each have at least two colours and
  the middle layer has at least three, bridge colours can avoid prescribed endpoints and
  adjacent choices can be made different; it also gives pairwise distinct choices for a
  three-layer cycle;
- `PlanarRecoloring/BridgeLists.lean` generalizes this choice to lists of arbitrary
  length: when every layer has at least two colours and at least one layer has three,
  there is a complete choice sequence avoiding the prescribed endpoints at the ends and
  having different adjacent choices;
- `PlanarRecoloring/CyclicLists.lean` closes an arbitrary-length choice sequence into a
  cycle and proves that its first and last choices differ when at least one layer has
  three colours;
- `PlanarRecoloring/CyclicBinary.lean` handles the alternating even-length special case
  in which all lists are equal and have exactly two colours, proves that odd lengths
  cannot close, and transports a heterogeneous binary construction from an arbitrary
  linear split or the written cut back to the original cycle. Its
  `cyclic_colours_list_cycle` theorem combines these cases into the full predicate-list
  exception statement used by the article;
- `PlanarRecoloring/ColourLists.lean` translates the predicate proofs to duplicate-free
  finite colour lists. `finite_list_cycle` and `finite_bridge_colours` match the full
  statements of the two corresponding article lemmas, with set equality interpreted
  extensionally rather than by list order;
- `PlanarRecoloring/LowerBound.lean` formalizes the finite obstruction for
  `degenerate-sharp` at $d=0$. With two isolated vertices using two colours, the state
  graph is a four-vertex hypercube; a parity argument shows that `00` and `11` cannot be
  joined by a three-step recolouring path, giving the Hamilton-connected lower bound,
  and also proves that this graph has no triangle;
- `PlanarRecoloring/Frozen.lean` checks the frozen property of the cube four-colouring
  used in the article: the endpoints of every cube edge have different colours, and the
  three neighbours of each vertex use exactly the other three colours.

The Chapter 4 increment is concentrated in composable certificate layers.
`HamiltonPathOn` and `HamiltonCycleOn`
express relation-level Hamilton properties using explicit finite vertex lists;
`FibrePath.toHamiltonPathOn` and `ClosedFibrePath.toHamiltonCycleOn` convert fibre
certificates directly to these properties; `FibrePath.reverse_of_symmetric` exchanges
their endpoints; and
`restoration_fibre_cycle_hamiltonCycleOn` feeds the restored-vertex bridge assumptions,
path coverage, and closing conditions into one result. The adjacent-pair layer now has
kernel-checked witnesses for all 225 ordered pairs of three- or four-element masks,
including transport of the representative Hamilton cycles, the four
Hamilton-connected types, every indexed common-interface exit, and the arbitrary-length
tagged reset induction. The twelve-state `P_3` lower-bound obstruction is also checked
by the kernel. Planar structural lemmas, general restoration existence, and external
colouring inputs remain separate interfaces. The planar source of the five-face counting
equations is still structural input. Appendix B--D are intentionally left on
the supplement/checker side in this round. The two-colour cycle-selection work in Section 2 now includes a
bidirectional construction for a heterogeneous pair at an arbitrary linear position and
across the written cut, together with the full predicate-list exception theorem. The binary product has
a concrete reflected Gray-code spanning path,
while the positive Hamilton-connected theorem for a nonbinary factor and the general
finite-factor formulation remain open interfaces. Complete-fibre cycle construction
and abstract component reset/port counting are now kernel-checked separately.

Verification:

```sh
lean PlanarRecoloring/LowerBound.lean
```

The complete Lake target requires Lean 4.34.1 and Lake. If elan is installed outside
the repository, run:

```sh
cd formalization
lake build
```

The unpacked Lean distribution on the development machine can also be used:

```sh
PATH=/tmp/lean-download/tool/lean-4.34.1-darwin_aarch64/bin:$PATH lake build
```

Individual files can be checked directly:

```sh
lean PlanarRecoloring/Core.lean
lean PlanarRecoloring/General.lean
lean PlanarRecoloring/Hamilton.lean
lean PlanarRecoloring/Fibre.lean
lean PlanarRecoloring/PermutationParity.lean
lean PlanarRecoloring/ProductParity.lean
lean PlanarRecoloring/Bridge.lean
lean PlanarRecoloring/BridgeLists.lean
lean PlanarRecoloring/CyclicLists.lean
lean PlanarRecoloring/CyclicBinary.lean
lean PlanarRecoloring/LowerBound.lean
lean PlanarRecoloring/Frozen.lean
lean PlanarRecoloring/FibreChain.lean
lean PlanarRecoloring/FibreHamilton.lean
lean PlanarRecoloring/Complete.lean
lean PlanarRecoloring/Extension.lean
lean PlanarRecoloring/BinaryHamilton.lean
lean PlanarRecoloring/BinaryEndpoints.lean
lean PlanarRecoloring/BinaryEndpointParity.lean
lean PlanarRecoloring/ArrangementParity.lean
lean PlanarRecoloring/TernaryProduct.lean
lean PlanarRecoloring/P3Strip.lean
lean PlanarRecoloring/CompleteFibreCycle.lean
lean PlanarRecoloring/Restoration.lean
lean PlanarRecoloring/StarObstruction.lean
lean PlanarRecoloring/Chapter4.lean
lean PlanarRecoloring/P3Obstruction.lean
lean PlanarRecoloring/PairFiveTransport.lean
```

This does not claim that the article's main theorems are fully formalized. Planar
embeddings and Euler counts, the Grötzsch three-colouring theorem, the
Hamilton-connected result for permutation graphs, the finite certificates in the
supplement, arbitrary-order cyclic fibre lifting, structural induction, and periodic
list selection remain interfaces awaiting formalization. They depend on external
results cited in the article, including Choo--MacGillivray and Havel, or on planar-graph
data structures not yet defined here. This directory reports only the Lean checks of
the self-contained results above; it does not use `sorry`, `axiom`, or computational
reports as substitutes for those proofs.
