# Selected-cycle coordinate-capacity feasibility

This bounded study uses the phase6 frozen manuscript, SHA256 `7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`. It preserves every selected cycle and pool and does not edit the main manuscript. The original ten-entry path232 table-free proof is a separate completed analytic candidate; this pentagon extension remains a feasibility study.

For coordinate j, let a,b count the two selected cycles separately inside the common legal edge universe of size m. Let F be the union of restored pool edges in that universe, f=|F|, and rC,rD the respective cycle losses to F. Inclusion–exclusion gives the safe lower bound a+b−m−rC−rD+f; replacing each r by f gives a+b−m−f. Only HH components use K=C minus pool. Hard D minus pool components are excluded.

The actual phase6 C1/FHC cycle words and pools were read directly. All 230 HH interfaces were independently enumerated from standard-source boundaries and the specified first normalizer. No Hamilton-cycle search or actual C/D common-edge intersection was computed.

## Results

- Coarse coordinate capacity covers 216/230; exact pool-loss capacity covers 222/230.
- The changed boundary coordinate alone covers 77 coarse and 90 refined cases.
- Refined best-coordinate distribution (smallest-index tie): j0=154, j1=43, j2=20, j3=11, j4=2.
- Best coordinate equals the changed coordinate in 40 cases; this does not support a universal changed-coordinate rule.
- All 1,150 scalar layers have 1,047 distinct (a,b,m,f,rC,rD) profiles; the 230 refined best choices have 216 distinct profiles, and the 222 positive choices have 208. Equal numbers are not proved symbolic or symmetry families.
- Constant source/target HH interface counts are both zero. The six constant-source families go to a hard target and are not included.

The corrected typical interface 00101→10101 has actual slice counts (a,b,m,f)=(6,6,7,1), yielding four protected common edges. The frozen v1 typical note had omitted 21310–31310 from its exact count and incorrectly asserted invariance of the entire selected slice; corrected v2 retains the seven-edge-universe proof and explicitly states that the entire six-edge slice is not invariant.

## Source and target distribution

| Component | Source total / coarse / refined | Target total / coarse / refined |
|---|---:|---:|
| 00004:0 | 12 / 12 / 12 | 2 / 2 / 2 |
| 00011:0 | 9 / 9 / 9 | 6 / 6 / 6 |
| 00012:0 | 11 / 11 / 11 | 13 / 13 / 13 |
| 00014:0 | 12 / 11 / 11 | 18 / 18 / 18 |
| 00101:0 | 13 / 13 / 13 | 8 / 7 / 8 |
| 00102:0 | 11 / 11 / 11 | 13 / 12 / 13 |
| 00104:0 | 12 / 12 / 12 | 18 / 17 / 17 |
| 00114:0 | 12 / 12 / 12 | 4 / 4 / 4 |
| 00121:0 | 13 / 12 / 13 | 15 / 14 / 15 |
| 00123:0 | 11 / 9 / 10 | 11 / 10 / 10 |
| 00124:0 | 12 / 12 / 12 | 24 / 23 / 23 |
| 01012:0 | 15 / 13 / 15 | 17 / 17 / 17 |
| 01014:0 | 12 / 9 / 9 | 4 / 4 / 4 |
| 01023:0 | 15 / 14 / 15 | 15 / 13 / 15 |
| 01024:0 | 12 / 12 / 12 | 24 / 19 / 20 |
| 01104:0 | 12 / 12 / 12 | 6 / 6 / 6 |
| 01124:0 | 12 / 10 / 10 | 12 / 11 / 11 |
| 01204:0 | 12 / 11 / 11 | 12 / 12 / 12 |
| 01234:0 | 12 / 11 / 12 | 8 / 8 / 8 |

## Eight inconclusive refined cases

| Source | Changed position | New colour | Target | Best refined lower bound |
|---|---:|---:|---|---:|
| 00123:0 | 0 | 3 | 00123:0 | -1 |
| 00014:0 | 0 | 3 | 01124:0 | 0 |
| 01014:0 | 0 | 2 | 01024:0 | 0 |
| 01014:0 | 0 | 3 | 01024:0 | -3 |
| 01014:0 | 2 | 2 | 01024:0 | -2 |
| 01124:0 | 1 | 2 | 01024:0 | 0 |
| 01124:0 | 2 | 2 | 00124:0 | 0 |
| 01204:0 | 2 | 0 | 00104:0 | 0 |

Negative or zero bounds are inconclusive, not failures of the original common-edge identities.

## Genuine triangle refinement

Only these eight cases were tested further, ignoring K2 single-edge rows. Of 85 K3 rows, exactly one supports the capacity rule: source 01124, position1→2, canonical target01024; physical coordinate3 with other colours (3,0,2,2) gives triangle {30202,30212,30232}. Each selected cycle retains two triangle edges and the pool union removes none, so 2+2−3 gives one protected common edge. The corresponding symbolic proof is frozen in uncovered_K3_support_candidate_v2.tex. The other seven cases have no tested K3 support. Thus the combined finite capacity checks cover 223/230, but this is not an analytic classification theorem.

## Research boundary

The high finite coverage is a promising mechanism; printing 222 numeric profiles instead of 222 witnesses would merely exchange data. The 208 distinct positive best profiles show that numerical equality alone gives little compression. A manuscript simplification still needs several proved symbolic source/target families that explain the capacity inequalities. This turn freezes the feasibility evidence and one hand-proved typical family; it does not remove any pentagon interface record.

Authoritative input: phase6-selected-input-v2.tex and phase6-input-provenance-v2.json. The earlier input v1 omitted FHC blocks and is retained as failed-prefix provenance, not used by the successful count.

Records: hh-coordinate-capacity-results-v1.json; hh-coordinate-capacity-summary-v1.json; hh-uncovered-triangle-capacity-results-v2.json. The original scripts and SHA256 fingerprints are in those records.
