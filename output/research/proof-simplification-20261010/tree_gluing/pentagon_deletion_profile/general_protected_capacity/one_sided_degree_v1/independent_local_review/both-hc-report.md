# Graph-only local intersection for arbitrary Hamilton cycles

The conditional graph lemma is correct. Exact evaluation on the original 10,379
ordinary-source/ordinary-target candidate vertices covers **125 of 230** interfaces.
It includes all 66 interfaces in the preceding source-degree-two subfamily and
adds 59. A separate check of 51 omitted printed common vertices proves that they
cannot contribute a positive bound, so 125/230 is also the coverage on all 10,430
printed common vertices. These are exact finite statistics, not a uniform C5
coverage theorem. The original computation files and manuscript are unchanged.

## Analytic local lemma

Let A and B be graph components with a common vertex v. Let P and Q be fixed
edge pools on the source and restored target. Write

- `d_s = |N_A(v)|`, `d_t = |N_B(v)|`;
- `d_c = |N_A(v) ∩ N_B(v)|`;
- `f = |{vw : w ∈ N_A(v) ∩ N_B(v), vw ∈ P ∪ Q}|`.

The safe common incident universe S(v) has size `h=d_c−f`. Any Hamilton cycle of
A uses two incident edges at v and at most `d_s−h` incident edges outside S(v).
Hence it uses at least `max(0,2−d_s+h)` edges of S(v). The target cycle analogously
uses at least `max(0,2−d_t+h)` safe incident edges. Inclusion-exclusion inside the
same universe S(v) gives

`|(E(H_A) \ P) ∩ (E(H_B) \ Q) ∩ δ(v)| ≥ max(0,4−d_s−d_t+d_c−f)`.

The untruncated expression is sufficient whenever it is positive; positivity
forces both individual retention lower bounds to be positive. The checker also
checks equality with the individually truncated inclusion-exclusion expression.
Pool edges are removed by a **union**, so an edge lying in both pools is counted
once. This lemma holds for every pair of Hamilton cycles and does not use their
actual edge sets. A whole-component Hamilton-cycle premise is required on each
side; both hard source and hard target cases are excluded.

The simple new case is a common cubic star: `d_s=d_t=d_c=3` and `f=0`. Two
two-element subsets of the same three incident edges meet. The degree-two cases
are the same count with a forced pair on at least one side.

## Exact execution and preserved scope correction

`extract_both_hc.py` reconstructs prescribed pools and first normalizers from the
frozen phase6 source; at the preceding independent check's candidate vertices it
builds N_A and N_B only by the one-coordinate allowed-list formula. The original
one-sided computation had already independently verified those candidate lists.
No peer helpers are imported, no full legal-state graph is enumerated, and no
Hamilton cycle is searched. CPython 3.14.6 executed the code.

The first invocation incorrectly asserted that the old source-K endpoint
candidate set equalled the complete intersection of the printed components.
It failed before writing a result. The diagnosis is retained in
`both-hc-attempt-1-failure.txt`; this is a correction to the candidate scope,
not a failure of the graph lemma.

The corrected primary invocation retains exactly the original candidate scope:
10,379 vertices, with 51 printed common vertices omitted across 51 interfaces.
For an omitted vertex v, both incident edges of the known selected source cycle
lie in P; otherwise v would be a source-K endpoint. Those two distinct edges
are nonsafe relative to S(v), regardless of whether they are target legal.
Consequently `d_s−d_c+f ≥ 2`. Since `d_t≥2` under the target-Hamilton-cycle
premise, the local expression is at most

`4−d_t−(d_s−d_c+f) ≤ 2−d_t ≤ 0`.

Thus the original candidates suffice to find every positive local certificate,
although they are not the complete printed common-vertex set. The separately
executed `check_omitted.py` verifies exactly these 51 vertices, including both
source-cycle incident pool edges, the local degrees and the nonpositive bound.
It does not rerun the primary 10,379-vertex extraction. Its result is retained
separately as `omitted-vertices-results.json`.

| Positive vertex certificate | Count |
| --- | ---: |
| d_s=2,d_t=2,d_c=1,f=0 | 18 |
| d_s=2,d_t=2,d_c=2,f=0 | 11 |
| d_s=2,d_t=2,d_c=2,f=1 | 5 |
| d_s=2,d_t=3,d_c=2,f=0 | 137 |
| d_s=3,d_t=2,d_c=2,f=0 | 126 |
| d_s=3,d_t=3,d_c=3,f=0 | 92 |

Several vertices can certify one interface. All 66 preceding arbitrary-two-cycle
source-degree-two interfaces remain covered, and 59 further interfaces are covered.

## Short selector rules and complete finite source groups

Suppose boundary coordinate j changes from a to b. If a common legal state x
has `{x_(j−1),x_(j+1)}={a,b}`, both old and new boundary colours are already
excluded by the neighbours. The two allowed lists at j coincide. All other lists
are unchanged, so `N_A(x)=N_B(x)`. If their common degree is three and no incident
edge lies in either fixed pool, x supplies the common cubic star above. This is
a symbolic sufficient condition. Pool avoidance still needs its own justification
for the prescribed normalized pool; arbitrary colour or dihedral transport does
not automatically preserve that pool.

A second sufficient rule is the local degree-two condition on either side:
when one degree is two and the other is at most three, the displayed bound
requires one safe common edge if both degrees are two, and two safe common edges
if the other degree is three. It includes both the source-degree-two and the
target-degree-two cases.

Two ordinary source groups have complete finite coverage:

| Source | Eligible ordinary targets | Local bound covers | Cubic star alone |
| --- | ---: | ---: | ---: |
| 01023 | 15 | 15 | 11 |
| 01124 | 12 | 12 | 4 |

For 01023 the four cases outside the cubic-star rule are edits at position/colour
`(0,1)`, `(1,0)`, `(3,3)`, and `(4,2)`. They have certificates
`d_s=3,d_t=2,d_c=2,f=0`. Thus a cubic-star rule followed by the degree-two rule
covers all fifteen prescribed interfaces. For 01124 the preceding source-degree-two
rule covers eleven of twelve; a cubic star supplies the remaining interface.
No source group is fully covered by the cubic-star rule alone.

`extract_families.py` reads the frozen primary result, checks the neighbour-colour
selector condition for every cubic-star certificate, and retains one certificate
for each of these 27 interfaces in `local-family-extract.json`. Its table also
records eligible, covered, cubic-star and degree-two counts for all source types.
This extraction makes the two short local rules reviewable without substituting
a list of 125 numbers for a proof. It does not prove a uniform source-type family
under the prescribed first normalizer or an equivariant transport of the pools.

## Limits

The analytic lemma and omitted-vertex implication are general graph arguments.
The 125/230 count and complete 15/15 and 12/12 source groups apply only to the
frozen specified interfaces. The graph-local bound itself uses full local
neighbourhoods and the fixed pool union; it never uses selected source/target
cycle-edge intersections. Selected source cycle edges are used only to recover
the old candidate scope and justify omission of its 51 missing vertices.

This intersection statement does not establish that arbitrary Hamilton cycles
contain every fixed pool edge needed for a splicing construction. Completeness
of the supplied component word lists comes from the frozen manuscript context;
this branch does not repeat a full-state completeness check. The standard
computation-record validator checks fields and hashes, not the lemma or global
mathematical completion.
