# Independent230 HH coordinate-capacity count: PASS

The independent reader parsed the full actual phase6 source, SHA256
`7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`,
and generated all21 supplied single-row HC components and their pools.
The component registry includes the two constant15-cycles, but they
contribute zero HH interfaces: their changed-boundary neighbours are hard
components, outside this calculation. Only19 source component types have
actual cases. The standard ordinary/starred labels were extracted from
the source markers, including the eleven FHC labels encoding the star as4.

Every listed cyclic word covers the proper states of its component once,
every consecutive and closing edge changes one coordinate, and every pool
is a subset of its corresponding selected cycle. Each source boundary
change was independently normalized by the prescribed lexicographic rule.
The target cycle and pool were restored through that actual map. Exactly
230 source/position/new-colour/target-component keys have nonempty common
state sets and both sides in the HC-minus-pool domain. There are52 omitted
transitions to a hard target; there are no empty state-set intersections
among the generated HH cases. Both hard source types are excluded at the
registry stage.

For each coordinatei, let J_i be its edges in the common raw state graph.
The independently computed six arrays are

```
a_i  = number of source-cycle edges in J_i
b_i  = number of restored target-cycle edges in J_i
m_i  = |J_i|
f_i  = |F intersect J_i|,  F=(source pool union restored target pool)
rC_i = number of source-cycle edges in F intersect J_i
rD_i = number of target-cycle edges in F intersect J_i
```

Removing F from either selected edge set gives safe-set sizes a_i−rC_i
and b_i−rD_i in a common universe of m_i−f_i edges. Inclusion-exclusion
therefore gives the refined bound

```
a_i + b_i - m_i - rC_i - rD_i + f_i.
```

The coarser bound a_i+b_i−m_i−f_i follows by replacing each removal
count by at most f_i. The refined bound is always at least the coarse
bound. The checker counts the two selected cycles separately and never
constructs their actual edge intersection.

Every one of the six five-coordinate arrays, normalizer, common-state
count, bound array and hit-coordinate list matches the frozen peer JSON
exactly across all230 keys. Source grouping also agrees. A case is counted
as covered when at least one coordinate has lower bound≥1:

| Count | Covered | Not established by this count |
| --- | ---: | ---: |
| Coarse pool-union subtraction | 216/230 | 14 |
| Refined actual pool-removal subtraction | 222/230 | 8 |

The eight refined uncovered cases are:

| Source | Changed position | New colour | Canonical target |
| --- | ---: | ---: | --- |
| 00014:0 | 0 | 3 | 01124:0 |
| 00123:0 | 0 | 3 | 00123:0 |
| 01014:0 | 0 | 2 | 01024:0 |
| 01014:0 | 0 | 3 | 01024:0 |
| 01014:0 | 2 | 2 | 01024:0 |
| 01124:0 | 1 | 2 | 01024:0 |
| 01124:0 | 2 | 2 | 00124:0 |
| 01204:0 | 2 | 0 | 00104:0 |

Nonpositive bounds are inconclusive; they do not refute the existing
protected common-edge witnesses in those cases.

Constant-source HH interfaces=0 and constant-target HH interfaces=0,
confirmed independently, rather than hidden in the230 coverage numerator.
The ordinary constant-source family proofs are not covered by this count.
Hard00001 and00112 cases use K=D\pool, so neither side containing a hard
component is included. The complete313-interface claim is not established
by this230-case exercise.

These are exact bounded supporting counts for the existing selected cycles
and pools. They are not an analytic derivation of the cycle-retention
counts across general boundary families, not a result for arbitrary
Hamilton cycles, and not a proof of the remaining eight HH cases. No peer
helper imports, Hamilton searches, actual C-intersect-D edge computation
or main-manuscript edits were performed. The corrected typical-note-v2
review is separate from this coverage review.
