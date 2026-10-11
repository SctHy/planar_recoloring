# General protected capacity: finite coverage and proof scope

The set-theoretic capacity lemmas hold for arbitrary edge bases, without a Hamilton-cycle assumption. The finite input is the actual phase-6 protected system, frozen from source SHA256 `7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`. No main manuscript was changed.

Write `K=A\P`, `L=B\Q`, and `W=V(K)∩V(L)`. Here `W` is a joint-port-support candidate universe, not the full recolouring fibre. In coordinate `j`, the common legal graph induced by `W` has `m_j` edges; the two protected sets individually retain `x_j,y_j`. Thus `x_j+y_j−m_j≥1` guarantees a common protected edge. Removing the forbidden union from this universe gives the separately stated refinement. This is proved set theory, whereas the coverage figures below are finite selected-basis counts.

| Input group | Full-fibre refined coordinate coverage | W plain coordinate coverage | W refined coordinate coverage | Changed-coordinate W coverage |
|---|---:|---:|---:|---:|
| HH | 222/230 | 218/230 | 222/230 | 90/230 refined |
| Nonconstant-source cases incident with a hard component | 18/53 | 53/53 | 53/53 | 8/53 |
| Constant-source cases | 30/30 | 30/30 | 30/30 | 0/30 |

Total refined coverage rises from 270/313 to 305/313. The 53-case group includes two hard-to-constant cases; it does not mean that both endpoints are nonconstant. No actual `K∩L` edge set, Hamilton-cycle search, or new cycle selection was computed. The 230 original HH vectors were inherited exactly, including normalizers and forbidden-edge deductions.

Taking all coordinates together, the plain `|K∩H[W]|+|L∩H[W]|−|H[W]|` bound covers 48/53 hard-incidence cases and all 30 constant-source cases. The global refined bound covers 49/53 and 30/30. These bounds range respectively from −1 to 4 and from 1 to 2. Consequently, a whole-support count cannot replace coordinate selection for all 53 cases.

The two canonical hard protected sets each have 11 edges and 20 endpoint states. Their endpoint-induced support graphs each have 17 edges. For `00001`, protected/support coordinate counts are `(5,2,0,2,2)` / `(6,2,1,4,4)`; coordinate 1 is saturated. For `00112`, they are `(3,1,3,2,2)` / `(4,3,3,4,3)`; coordinate 2 is saturated. Target coordinates transport as `s+εk mod 5` under the actual normalizer. A protected port of the opposite side in this saturated coordinate is sufficient without comparing individual edges. This fixed-coordinate shortcut covers 32/53 and 10/30. Allowing any coordinate saturated by the hard side covers 46/53 and 30/30; allowing either side to saturate a coordinate covers 50/53 and 30/30. All 30 constant cases have a coordinate profile `(x,y,m,f,rK,rL)=(1,1,1,0,0,0)`.

With maximum refined bound and smallest-coordinate tie break, the 53 hard-incidence cases have 14 distinct best scalar profiles. Of these, only `(2,2,3,0,0,0)` (two cases) and `(5,2,6,1,1,0)` (one case) do not have either side saturated at the best coordinate. These are exactly the three cases that have no saturated coordinate on either side: `00001:0,1,1→00101:0`; `00012:0,2,1→00112:0`; and its reverse `00112:0,2,0→00012:0`. They admit a strict-majority capacity count, but the present record does not give a universal symbolic reason that the required coordinate always exists.

The proven new structural rule is therefore conditional saturation/strict-majority retention on a joint endpoint-support universe. Its finite application succeeds in all 53 hard-incidence and all 30 constant-source interfaces. It does not yet remove 305 mathematical cases: deriving the support and retention shapes uniformly from the displayed bases, without 313 scalar checks, remains the analytic simplification task. The eight uncovered coordinate-capacity cases are the previously recorded HH residuals, treated separately by triangle/square support research.

Reproduction: run `general_capacity_baseline_v1.py`, then `port_support_capacity_v2.py`, then `summarize_general_capacity_v2.py`. The latter reads only the frozen JSON counts, computes no graph, and records the input hashes. The scripts' embedded output hashes describe their current exact input; elapsed-time fields need not reproduce byte-for-byte.
