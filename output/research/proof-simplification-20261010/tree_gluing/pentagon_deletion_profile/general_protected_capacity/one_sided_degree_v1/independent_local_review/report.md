# One-sided degree criterion: independent local review

The independent implementation passes exact readback of every author record.
It reconstructs K, both fixed pools, and the first target normalizer directly
from the frozen phase6 manuscript. All 53 marked C5 blocks and the normalization
paragraph are byte equal to the current manuscript at the observed execution.
No helper from another checker is imported. No complete legal-state graph is
enumerated, and no Hamilton cycle is searched. The author code and result remain
unchanged.

## Exact finite readback

The input source SHA-256 is
`7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`.
The preserved author-result SHA-256 is
`fb21db194e918b1dc05c2d7a0a3a5826ced3f187f8fcb5bea66d747f9fdf21c9`.
Execution used CPython **3.14.6**. The initial backend inventory's Python 3.14.3
entry was stale; the affected Python entry was refreshed before computation.

The checker compares all fields of all 313 original records, including mappings,
scope exclusions, every local neighbour list, every safe-edge list, the integers
d and g, the lower bounds, certificate lists, and Boolean subcriterion flags.
This is 10,706 local observation vectors and 160,590 possible coordinate/colour
mutation alternatives under the author's counting convention.

| Quantity | Exact result |
| --- | ---: |
| Specified interfaces | 313 |
| Hard targets excluded from whole-Hamilton-cycle premise | 57 |
| Eligible target-Hamilton-cycle interfaces | 256 |
| Covered by one-sided degree bound | 200 |
| Uncovered eligible interfaces | 56 |
| Target degree-two subcriterion | 85 |
| Target degree-three with two safe incident edges | 181 |
| Intersection of the preceding subcriteria | 66 |
| Additional interfaces beyond target degree two | 115 |
| Covered ordinary sources / hard sources | 181 / 19 |

There are 163 certificates of type d2/g1, 42 of type d2/g2, and 538 of type d3/g2.
These certificate counts count vertices, so several can support the same interface.

## Mathematical implication of the local count

Let B be a target component, P_B its fixed pool, and K_A any fixed source
protected edge set. At a target vertex v, let d be its degree in B and let G(v)
be the incident edges that belong to K_A, are legal target edges, and avoid P_B.
Write g=|G(v)|. Every Hamilton cycle H_B uses exactly two incident edges at v.
At most d-g of them can lie outside G(v). Therefore

`|E(H_B) ∩ G(v)| ≥ max(0, 2 + g − d)`.

This is a general finite-graph counting implication. It does not depend on the
displayed target Hamilton cycle, and it permits a hard source because K_A is a
fixed edge set there. A hard target cannot be admitted through a nonexistent
whole-component Hamilton-cycle premise. No claim about a row of a product seed
is substituted for that premise.

For a legal C5 state x and boundary t, set

`L_i(t,x) = {0,1,2,3} \ {x_(i−1), x_(i+1), t_i}`,

omitting t_i when it is starred. Its exact degree is
`Σ_i (|L_i(t,x)|−1)`. The checker generates just these local mutations at already
specified candidate vertices. Parsing the printed cycle words is input recovery;
it is not enumeration of all `4^5` legal-state candidates.

## A strict subfamily with arbitrary Hamilton cycles on both sides

Now let A be ordinary and let H_A be **any** Hamilton cycle of A. Every edge
incident with a vertex of degree two in A belongs to H_A. Such an edge is usable
for an intersection statement when it avoids the fixed source pool P_A and the
restored target pool P_B and is legal in B. At a target vertex v, let F(v) consist
of these usable edges forced by a source degree-two endpoint. If f=|F(v)| and
`2+f−d_B(v)>0`, the same count gives

`(E(H_A) \ P_A) ∩ (E(H_B) \ P_B) ≠ ∅`

for **every pair** of source and target Hamilton cycles. This intersection claim
does not assert that an arbitrary Hamilton cycle contains every fixed pool edge
needed by an unrelated splicing construction.

There is a particularly short central-vertex condition. If x is legal for both
boundaries and has source degree two, changing one boundary coordinate alters
only one L_i and changes its size by at most one. Thus its target degree is at
most three, and a target Hamilton-cycle premise makes it two or three. A common
edge outside both fixed pools is then forced whenever either:

1. the target degree is two and at least one source incident edge is target legal
   and outside both pools; or
2. the target degree is three and both source incident edges are outside both
   pools. In this degree-increase case both source edges are automatically target
   legal: if the newly forbidden boundary colour had been an available source
   mutation, the target degree could not have increased.

This symbolic criterion has stronger quantifiers than a fixed-source-cycle
criterion. Its existence does not establish uniform coverage of all boundary
interfaces.

The finite scan is restricted to the same existing candidate vertices. It has
230 ordinary-source/ordinary-target interfaces; the remaining 26 eligible hard
sources are excluded from the arbitrary-source-Hamilton-cycle extension.

| Quantity | Exact result |
| --- | ---: |
| Central source degree-two condition | 66 / 230 |
| Allowing any degree-two source endpoint | 66 / 230 |
| Additional interfaces from that relaxation | 0 |
| Covered through target degree two | 26 |
| Covered through target degree three | 63 |
| Overlap | 23 |
| Covered through target degree three only | 40 |

The 66 covered interfaces are distributed over seven source types:

| Source type | Covered interfaces |
| --- | ---: |
| 00011 | 8 |
| 00012 | 10 |
| 00114 | 10 |
| 00121 | 8 |
| 00123 | 10 |
| 00124 | 9 |
| 01124 | 11 |

There are 137 central-vertex certificates with source degree two and target
degree three, 11 with source/target degrees two and two forced safe edges, and
23 with source/target degrees two and one forced safe edge. Seven other vertex
certificates have source degree three and target degree two, using a neighbour's
source degree-two endpoint; all their interfaces already have a central certificate.

A concrete example is the interface `00012:0`, boundary position 1, colour 1,
whose actual and standard target are both `01012:0`. At state `12303`, the source
degree contributions are `(0,0,1,1,0)`, with the two forced source neighbours
`12103` and `12323`. The target contributions are `(0,1,1,1,0)`. Both edges avoid
both prescribed pools. Every target Hamilton cycle must use at least one of them,
and every source Hamilton cycle uses both. The result file retains two local
certificates for this interface and all certificates for the remaining cases.

## Evidence limits and retained artifacts

The local counting implications above are proved analytically. The numbers
200/256 and 66/230 are exact checks on the prescribed finite interface set. They
are not uniform C5-family coverage theorems, Hamilton searches, or completion of
the global recolouring problem. Completeness of the displayed fibre components
is part of the frozen manuscript context; this branch does not repeat the old
full-state completeness verification. All incident neighbours generated at the
checked vertices belong to the specified component word sets.

`check_local.py` is independently written using integer tuple states, a linewise
marked-block parser, the allowed-list degree formula, and directly reconstructed
normalization/restoration. The preserved author result is a comparison input;
its scalar values do not generate the independent observations. The validated
computation record binds task, source, comparison input, code, result, and this
report. Record validation checks schema and hashes only. The manuscript is untouched.
