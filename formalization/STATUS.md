# Lean formalization audit of the article results

The audit target is the current repository version of `main.tex`. The table below lists
each labelled `theorem`, `lemma`, `proposition`, `claim`, and `remark` in the article
(46 items in total). “Partial” means that Lean contains a strict local special case or
lower-bound fragment that cannot replace the article statement with its full quantifiers
and assumptions. “Finite certificate” means that the supplement's Python checker
provides finite data evidence, which is not a Lean proof.

This run deliberately skips the Appendix B--D formalization. The main-text frontier
claims and the structural or literature-dependent planar theorems remain identified
as open formalization work below; no appendix checker is counted as a Lean proof.

## Reusable Lean content already covered

The following declarations can themselves be checked by the Lean kernel; they are not
complete replacements for the article labels:

| File | Kernel-checked content |
| --- | --- |
| `PlanarRecoloring/Core.lean` | `FiniteGraph`, `Coloring`, `Proper`, single-vertex recolouring adjacency, and available colours; reflexivity and symmetry of adjacency; explicit-list `Consecutive` and `SpanningPath`. |
| `PlanarRecoloring/Bridge.lean` | `exists_avoiding_of_two`, `exists_avoiding_of_three`, `bridge_colours_three`, and `cyclic_three_colours`: strict local bridge steps for linear and cyclic three-layer configurations. |
| `PlanarRecoloring/LowerBound.lean` | The four-vertex hypercube of two isolated vertices with two-colour states: `q2_not_hamilton_connected` and `q2_has_no_triangle`, the `d=0` obstruction fragment of `prop:degenerate-sharp`. |
| `PlanarRecoloring/Frozen.lean` | Properness of the cube four-colouring, each coordinate-flip edge, and `cube_colouring_is_frozen`. This is a finite local model for the triangle-free lower bound, not a proof of `thm:trianglefree-hc`. |
| `PlanarRecoloring/Hamilton.lean` | List definitions of `HamiltonPath`, `HamiltonCycle`, `HamiltonConnected`, and `VertexPancyclic`, path reversal, explicit-list lemmas, injective vertex-list transport for `HamiltonPathOn`, and the generic `HamiltonPathOn.splice` cut-and-join theorem; no global threshold in the article is proved. |
| `PlanarRecoloring/P3Obstruction.lean` | The twelve-state `P_3` recolouring graph, proper-state representatives, symmetry, and a kernel-checked bounded search proving that no spanning cycle exists. |
| `PlanarRecoloring/PairFive.lean` | Literal Appendix A cycle and endpoint tables, canonical certificate predicates, the complete 15-mask list, and the indexed interface-exit certificate. |
| `PlanarRecoloring/PairFiveTransport.lean` | Palette/permutation transport, list-level Hamilton path/cycle transport, all labelled small-mask Hamilton-connected witnesses for the four 4-containing types, edge-on-cycle witnesses for every labelled adjacent-pair fibre, and the one-edge Hamilton-path transport used at interfaces. |
| `PlanarRecoloring/PairFiveReset.lean` | The arbitrary finite adjacent-pair reset induction under the article's explicit layer-transition hypotheses, with a layer-tagged `HamiltonPathOn` conclusion so equal assignments in different fibres remain distinct vertices. |
| `PlanarRecoloring/PairFour.lean` | Canonical Hamilton cycles for all labelled three-by-three four-colour fibres and a checked two-common-edge count for every allowed one-list transition. |
| `PlanarRecoloring/FaceIdentity.lean` | The exact integer algebra for the five-face identity, the subcubic face-count identity, and the resulting twelve-face arithmetic lower bound; the planar source of those equations remains structural input. |
| `PlanarRecoloring/Fibre.lean` | `FibrePath`, `ClosedFibrePath`, no-repetition splicing of disjoint lists, interface-edge splicing with different internal relations on the two sides, and preservation of consecutiveness. This is a two-fibre abstraction, not the article's cyclic multi-fibre lift. |
| `PlanarRecoloring/FibreChain.lean` | Flattened paths for any nonempty fibre chain, coverage, endpoints, no repetition, bridge consecutiveness, and the closing-bridge interface. |
| `PlanarRecoloring/FibreHamilton.lean` | Conversion of a fibre path covering all of `Fin n` to `HamiltonPath`, and of a closed fibre chain to `HamiltonCycle`; the given fibre paths and interface edges are still assumptions. |
| `PlanarRecoloring/Extension.lean` | The `Option (Fin n)` restored-vertex model; extension properness criteria, fibre reconstruction, within-fibre adjacency, and cross-fibre adjacency for a shared colour. |
| `PlanarRecoloring/PermutationParity.lean` | The six-state representation of `K_2` for `d=1,k=3`, permutation-parity edge flips, absence of a Hamilton path for the specified endpoints, and triangle-freeness. |
| `PlanarRecoloring/ProductParity.lean` | List representation of binary products, xor parity of single-coordinate flips, parity propagation along index paths, and the odd-cycle obstruction. |
| `PlanarRecoloring/BinaryEndpoints.lean` | Generic path-list concatenation/insertion lemmas and a kernel-checked sufficient construction for arbitrary opposite-parity binary-product endpoints. |
| `PlanarRecoloring/BinaryEndpointParity.lean` | Exact binary-product endpoint theorem: for nonempty fixed-length Boolean words, a spanning path exists exactly for opposite xor parity endpoints. |
| `PlanarRecoloring/ArrangementParity.lean` | Completed-arrangement model, exchange relation symmetry, inversion-parity append interface, exchange-parity calculation, the generic edge-flip triangle obstruction, and a finite bipartite Hamilton-connected obstruction. |
| `PlanarRecoloring/TernaryProduct.lean` | Hamilton-connectedness of the binary-word graph product with `K_3`, for every word length, with explicit state enumeration and coverage. This is the nonbinary-factor product fragment; arbitrary finite factors remain open. |
| `PlanarRecoloring/P3Strip.lean` | A literal 24-state Hamilton cycle for `R_3(P_3) □ P_2`, giving the two-layer finite base case of the Chapter 4 bad-run construction. The arbitrary-length strip and square-splicing induction remain open. |
| `PlanarRecoloring/CycleSplicing.lean` | Concrete cycle witnesses, selected-edge cuts, cyclic rotation to endpoint Hamilton paths, and two-cycle splicing from explicit cross edges and disjointness. This is the generic cut-and-join interface used by the restoration arguments. |
| `PlanarRecoloring/CyclicLists.lean` | Cyclic choices for arbitrary length when at least one layer has three colours; the first and last bridge colours are also proved different. |
| `PlanarRecoloring/CyclicBinary.lean` | Alternating cyclic choices for an even number of copies when all lists are equal and have exactly two colours, a strict proof that odd numbers of copies cannot form a cycle, and rotation proofs for heterogeneous pairs at arbitrary linear positions and across the written cut. |
| `PlanarRecoloring/ColourLists.lean` | Finite-set versions of the complete cyclic list-choice and endpoint bridge-colour lemmas, using duplicate-free lists and extensional membership for set equality. |
| `PlanarRecoloring/General.lean` | List interfaces for symmetric/loopless graphs, edges, and degeneracy; available colours, explicit single-vertex recolouring, colour permutations, and basic lemmas. The file is imported by the root module and passes kernel checking, but these interfaces do not prove the article's global labels. |
| `PlanarRecoloring/CompleteFibreCycle.lean` | Given duplicate-free complete fibres, endpoint witnesses, pairwise disjointness, and cyclic bridge edges, constructs the fibre Hamilton paths and the resulting Hamilton cycle; no clique path is assumed as an opaque input. |
| `PlanarRecoloring/Restoration.lean` | Abstract two-fibre component-label transitions, independent reset reachability to `(none, none)`, and the finite protected-port inequality used by bounded-degree tree splicing. |

None of the modules above contains `axiom`, `sorry`, or `admit`. These foundational
interfaces in the formalization directory still do not replace the article theorems
listed below, especially statements involving planar embeddings, general restoration
existence, or assumptions from external literature.

## Label-by-label conclusions

### Degenerate graphs and fibre interfaces

| Article label | Status | Corresponding content or gap |
| --- | --- | --- |
| `thm:main-degenerate` | Pending formalization | Aggregate theorem; its Hamilton-connectedness, vertex-pancyclicity, and exact threshold are unproved. |
| `lem:list-cycle` | **Kernel-checked** | `ColourLists.lean:finite_list_cycle` proves the complete finite-set exception statement: duplicate-free lists have at least two colours, the number of layers is at least three, and the only excluded case is an odd number of identical two-element sets. Set equality is extensional membership, independent of list order. |
| `lem:single-lift` | **Partial** | `CompleteFibreCycle.lean` now constructs each complete-fibre Hamilton path from finite duplicate-free fibre data and endpoint witnesses, while `Extension.lean` supplies the restored-colouring relation. The article's degree-derived fibre lists, bridge selection, and planar induction remain unproved. |
| `lem:bridge-colours` | **Kernel-checked** | `ColourLists.lean:finite_bridge_colours` proves the complete finite-set statement for arbitrary length, including endpoint avoidance and the one-layer case. Its hypotheses are duplicate-free lists of size at least two and one list of size at least three; the latter also ensures nonemptiness. |
| `lem:clique-endpoints` | **Partial** | `Complete.lean` and `Extension.fibre_hamiltonPathOn_of_mem` prove endpoint Hamilton paths for any explicitly enumerated fibre list whose relation is complete on that list; the article's cyclic base-path splice and deletion-one-state endpoint argument remain unproved. |
| `thm:degenerate-hc` | Pending formalization (external dependency) | Requires the Hamilton-connected result for the permutation graph `A_{k,n}` cited in the article (`HLTH04`) and the complete induction. |
| `thm:degenerate-vp` | Pending formalization | Requires the closed lift, coverage of the length interval, and the exceptional two-colour cases. |
| `rem:not-edge-pancyclic` | **Kernel-checked local counterexample** | `StarObstruction.lean` proves the specified star edge is legal and has no common adjacent state, hence lies in no triangle; it does not assert that every recolouring edge lacks cycles. |
| `prop:degenerate-sharp` | **Partial** | `LowerBound.lean` proves the four-vertex hypercube obstruction at `d=0`; `PermutationParity.lean` proves the six-state `d=1,k=3` parity obstruction; and `ArrangementParity.lean` proves the generic finite bipartite Hamilton-connected obstruction for any duplicate-free arrangement enumeration of size at least three. A canonical all-permutations enumeration and the article-level `K_{d+1}` state-space identification remain unformalized. |
| `thm:main-planar` | Pending formalization | Aggregate theorem; depends on the planar, triangle-free, and forest results below. |
| `lem:product` | **Partial** | `ProductParity.lean` encodes the binary-product single-coordinate-flip parity obstruction. `BinaryEndpointParity.lean` proves the full fixed-length Boolean endpoint equivalence (nonempty words), `BinaryHamilton.lean` supplies the Gray-code base construction, and `TernaryProduct.lean` proves Hamilton-connectedness for the binary-word graph product with `K_3`. The general finite-factor formulation and the article's full restoration application remain unproved. |
| `lem:path-fibre` | Pending formalization | Reachable-exit induction for multi-coordinate fibres along a path is not encoded. |
| `lem:independent-hc` | Pending formalization | Hamilton-connected restoration for independent-set fibres is not encoded. |
| `lem:fibre-lift` | **Partial** | `Fibre.lean` and `FibreChain.lean` prove path splicing for disjoint pairs and arbitrary linear fibre chains; `FibreHamilton.lean` provides relation-level conversions; `CycleSplicing.lean` cuts concrete cycle edges and joins two disjoint cycles from explicit cross edges; and `Extension.lean` connects restoration bridges to a closed chain. The cyclic layering, endpoint matching, and fibre-path existence required by the article are not encoded. |
| `lem:independent-restoration` | Pending formalization | Hamilton-cycle restoration for independent sets is not encoded. |
| `lem:single-hc` | Pending formalization | Single-vertex Hamilton-connected restoration under the minimum-state degree condition is not encoded. |

### Planar and triangle-free classes

| Article label | Status | Corresponding content or gap |
| --- | --- | --- |
| `lem:marked-five` | Pending formalization (structural) | Planar triangulations, Euler counting, and the two degree-five vertices at distance three have no planar-embedding data structure or proof. |
| `thm:planar-hc` | Pending formalization (external dependency) | Depends on `lem:marked-five`, degenerate restoration, the seven-colour degree count, and the icosahedron frozen colouring; the article also cites `BP16`. |
| `lem:pair-five-endpoints` | **Kernel-checked finite certificate** | `PairFive.lean` replays all seven representative cycle tables and 53 endpoint words; `PairFiveTransport.lean` transports them through the recorded colour permutations and coordinate swaps, covering all 225 ordered pairs of small masks. The planar application remains outside this finite state layer. |
| `lem:pair-five-reset` | **Kernel-checked under explicit fibre hypotheses** | `PairFiveReset.lean` proves the arbitrary finite reachable-exit induction, selects the internal common-interface state while avoiding the two prescribed states, and converts the resulting chain to a layer-tagged `HamiltonPathOn`. The planar structural induction and the external three-colouring input remain outside this theorem. |
| `thm:trianglefree-hc` | Pending formalization (external dependency) | Depends on the Grötzsch three-colouring theorem, the adjacent-pair restoration above, and the complete planar induction; the four-dimensional cube lower bound is only a local Lean model. |
| `lem:marked-two` | Pending formalization (structural) | Girth-six planar Euler counting and the two degree-two vertices at distance three are not encoded. |
| `thm:girth6-hc` | Pending formalization (external dependency) | Depends on `lem:marked-two`, independent-set restoration, the degenerate theorem, and the period-three frozen-colouring counterexample. |
| `thm:forest-hc` | **Partial** | `P3Obstruction.lean` now proves the finite `\R_3(P_3)` no-Hamilton-cycle certificate, and `PermutationParity.lean` proves the `\R_3(K_2)` Hamilton-connected lower bound. The one-degenerate upper-bound induction and the full forest threshold theorem remain unformalized. |

The article also has an unlabelled bipartite corollary after `thm:trianglefree-hc`; it
has no Lean proof either.

### Four-colour subclasses of girth five

| Article label | Status | Corresponding content or gap |
| --- | --- | --- |
| `thm:main-four` | Pending formalization | Aggregate theorem; the Hamiltonian proofs for the two girth-five subclasses are not encoded. |
| `lem:subdivided-star-four-subclass` | Pending formalization | The four bottom cycles, tree exchanges, and product-fibre lift are not encoded. |
| `lem:five-face-identity-subclass` | **Partial** | `FaceIdentity.lean` proves the exact integer consequence `p = 12 + Q + 2D - 2s` from the three displayed counting equations. Face lengths, planar embeddings, facial simplicity, and the derivation of those equations are not encoded. |
| `cor:seven-pentagons-two-degenerate` | **Partial** | `five_face_count_at_least_twelve` proves the arithmetic core that a minimum-degree-three plane graph with nonnegative excess terms has at least twelve five-faces. The planar subgraph extraction and distinct-face-to-cycle argument remain structural. |
| `thm:seven-pentagons` | Pending formalization (external dependency) | Depends on the two structural results above, `lem:single-lift`, `lem:adjacent-two-four`, `lem:subdivided-star-four-subclass`, and the three-colouring input. |
| `lem:adjacent-two-four` | **Partial finite certificate** | `PairFour.lean` checks every labelled three-by-three fibre cycle and the two-common-edge invariant for all allowed one-list transitions; `CycleSplicing.lean` supplies the generic two-cycle edge-cut splice. The base recolouring-cycle enumeration and the complete arbitrary splice into `R_4(G)` remain unproved. |
| `lem:separated-two-g5` | Pending formalization (external dependency) | Depends on the Grötzsch three-colouring theorem and `lem:independent-restoration`. |
| `prop:badrun` | **Partial finite certificate** | `P3Strip.lean` gives a kernel-checked 24-state Hamilton cycle for the base case `\ell=2`. The arbitrary-length strip induction, retained-edge invariant, and three-square splicing remain unproved. |
| `lem:pathsafe` | Finite certificate, not Lean-formalized | Appendix B remains covered only by the existing supplement checker; its cycle and safe-edge data were intentionally left out of Lean in this round. |
| `lem:badblock` | Finite certificate, not Lean-formalized | Depends on `prop:badrun` and arbitrary-length bad-segment splicing with safe-edge preservation. |
| `lem:path232` | Finite certificate, not Lean-formalized | Depends on the good/bad boundary certificates above and block splicing of the bottom Hamilton cycle. |
| `thm:subcubic` | Pending formalization (finite certificate and external dependencies) | Depends on the pentagon appendices C--D, the Grötzsch three-colouring theorem, face counting, and `lem:two-pentagons-restore`. |

### Protected pentagons and block-subcubic graphs

| Article label | Status | Corresponding content or gap |
| --- | --- | --- |
| `lem:pentagon-path-blocks` | Finite certificate, not Lean-formalized | The 23 component blocks in Appendix C are checked by the checker; the corresponding Lean state graph is not defined. |
| `lem:pentagon-protection` | Finite certificate, not Lean-formalized | Finite records support the 2,304 boundaries and 313 standard source interfaces in Appendices C--D. |
| `lem:protected-product` | Pending formalization (depends on finite certificates) | Arbitrary component splicing of product cycles and protected edges has no Lean proof. |
| `lem:pentagon-overlap` | Pending formalization | The combinatorial count of at least ten common states for overlapping components is not encoded. |
| `lem:pentagon-component-graph` | **Partial abstract reset** | `Restoration.lean` proves the exact one-factor/product label transitions and reachability of the common `(none, none)` reset state. The article's geometric overlap-to-component-edge argument and its actual base-cycle component graph remain unproved. |
| `lem:protected-tree-splicing` | **Partial port count** | `Restoration.exists_unused_protected_port` proves the numerical fresh-port inequality behind the induction. The cycle-cutting invariant, protected-edge cross-edge realization, and final tree splice remain unproved. |
| `lem:two-pentagons-restore` | Pending formalization | Synchronized external changes, the component graph, and tree splicing for two pentagons are not encoded. |
| `lem:subcubic-face-count` | **Partial** | `FaceIdentity.subcubic_face_count_arithmetic` checks the exact integer consequence from the face-length, degree-sum, and Euler equations. Face walks, girth, and the planar derivation remain structural. |
| `lem:two-separated-five-faces` | Pending formalization (structural) | The complete argument using bridges, dual triangulations, and two-sided face counting is not encoded. |
| `thm:subcubic` | Pending formalization | Aggregate theorem; its induction also depends on every gap in this section. |
| `thm:block-subcubic` | Pending formalization | Block-cut trees, end-block face counting, and pentagon restoration are not encoded. |

## Boundary between external results and finite evidence

The following inputs cannot currently be replaced by “a Lean interface”:

1. The Hamilton-connected result for the permutation graph in `HLTH04`, the Grötzsch
   three-colouring theorem, and the literature results cited in the article as `ChMa11`,
   `BP16`, and so on have not been imported or formalized.
2. Planar embeddings, faces, duals, girth, block-cut trees, and the Euler formula are
   not defined in this directory. Therefore all `marked-*`, face-count, and block-
   structure statements remain mathematical content awaiting formalization.
3. `supplement/verify_all.py` and its companion checkers verify only literal finite
   certificates (properness, coverage, symmetry orbits, interface edges, and protected
   pools). The article explicitly states that they do not verify arbitrary-length lifts,
   product cycles of unlisted orders, existence of the bottom Hamilton cycle, or tree
   splicing. The adjacent-pair reset is now proved separately in Lean from its explicit
   finite interface hypotheses; these scripts do not establish that theorem.

## Reproducible execution record

The following commands were run during the audit:

```sh
cd formalization
lake build
lake env lean PlanarRecoloring/General.lean
lake env lean PlanarRecoloring/PairFiveReset.lean
lake env lean PlanarRecoloring/CyclicBinary.lean
lake env lean PlanarRecoloring/ColourLists.lean
lake env lean PlanarRecoloring/CompleteFibreCycle.lean
lake env lean PlanarRecoloring/BinaryEndpointParity.lean
lake env lean PlanarRecoloring/ArrangementParity.lean
lake env lean PlanarRecoloring/Restoration.lean
```

The root Lake target built successfully, and the standalone `General.lean`,
`P3Obstruction.lean`, `PairFiveTransport.lean`, `PairFiveReset.lean`,
`CompleteFibreCycle.lean`, `BinaryEndpointParity.lean`, `ArrangementParity.lean`,
and `Restoration.lean` checks also succeeded. The current
formalization directory contains no `axiom`, `sorry`, or `admit`. The relation-level
Hamilton certificates follow only from explicit finite paths and bridge assumptions.
“Build succeeded” means only that Lean accepted the current source files; it does not
mean that any article label still listed as pending has been formalized.
