# Independent mathematical and actual-source review

The v3 two-family replacement is mathematically acceptable for the twenty-seven stated interfaces, subject to the unchanged phase8 component classification and remaining certificates. The reviewed actual full source has SHA `505c432f4a18a36056f50f5ba1a56ac4513ca02aa64520580d4de64b3dfff62f`. This review does not adopt the manuscript or review its unrelated theorems.

## Mathematical argument

At a state legal for both boundaries, every mutation in an unchanged coordinate has the same legality on both sides. In the changed coordinate `j:a→q`, the target can lose the mutation to `q` and can gain only the mutation to `a`. The latter exists exactly when `a` is absent from the two neighbour colours. Thus the union of the two complete incident stars has size `d_s+α`.

When that union has three edges, each Hamilton cycle containing the state uses two distinct incident edges from it. Two two-element subsets of a three-element set intersect. Their intersecting edge belongs to the common incident star. The condition `f=0` excludes both pools from that common star, so the edge belongs to the two specified protected sets. The actual v3 text states this condition correctly. It does not require the entire incident-star union to avoid the pools.

The earlier numeric formula is also correct: `d_t=d_s+α−β`, `d_c=d_s−β`, and safe-star inclusion–exclusion gives `max(0,4−d_s−α−f)`. The v3 proof uses the special three-edge mechanism directly and avoids needing that formula as a separate numbered lemma. Its Hamilton-cycle quantifier includes the starred source `01124`; the v1 wording “ordinary components” was potentially narrower. V3 removes that ambiguity and repairs the old 283-individual summary.

The local conclusion applies to arbitrary pairs of component Hamilton cycles, with the stated pool sets fixed. This does not make arbitrary cycles valid product gluing seeds: the subsequent product construction still requires the specified cycles and their actual printed pool/reserve edges. This pipeline is unchanged, and the reviewed cycles contain their pools.

## Actual source and complete coverage

`check_actual_sources.py` is a separate implementation. It imports no author helper and reads no author result JSON. It reads the actual frozen phase8 and v1/v2 candidate snapshots, parses the printed source sets, cycles and pools, and reimplements the printed normalizer order: start 0 through 4, sign +1 then −1, lexicographic permutations of 0,1,2,3, retaining the star.

All fifteen edits of source `01023` and twelve nonstar edits of `01124` produce exactly the twenty-seven distinct removed original interface keys and original one-based indices. Each computed target type/component equals the original reference entry. For every case, at least one word from the actual source row is in both the source cycle vertex set and the precisely restored target component. Its computed source/target/common degrees satisfy the independent direct-star and closed formulas; `d_s+α=3`, its full incident-star union has three edges, and its common incident pool union has `f=0`.

The source row annotations were checked, including every source degree and every displayed `J_t` position set. Every target pool is restored through the exact original first normalizer, with inverse colour and coordinate maps verified. Common forbidden edges are counted as a set union, so an edge present in both pools is counted once.

For the twelve selected component cycles actually needed here, every printed word is legal and unique, consecutive words including the closing pair differ in one coordinate, every pool is contained in the specified cycle, and every legal one-coordinate neighbour of every printed vertex stays inside its cycle vertex set. A connected legal vertex set closed under all such neighbours is an entire connected component. The checked component sizes are:

| Component | States |
| --- | ---: |
| `01023:0` | 66 |
| `01124:0` | 74 |
| `00123:0` | 57 |
| `00012:0` | 47 |
| `01012:0` | 68 |
| `00102:0` | 63 |
| `00121:0` | 58 |
| `00014:0` | 60 |
| `01104:0` | 74 |
| `00124:0` | 71 |
| `01024:0` | 85 |
| `01234:0` | 82 |

This selected-component closure check is not a repeat of the global twenty-three-component and 2304-boundary classification, hard seed proofs or unchanged 256 individual edges and thirty constant cases. Their existing reference proof remains an explicit dependency.

`readback_candidate_v3.py` reads the actual v3 source and verifies that all fifty-three marked blocks equal v2; fifty-two equal phase8 byte for byte, while `INTERFACES-ALL` is the same unchanged 256-row remainder. The source words, degrees, `J_t` annotations and normalizer text equal the already independently checked v2 inputs. It reuses those unchanged twenty-seven local checks without recomputing neighbours. After accounting for exactly the protected-proof paragraph, the corrected verification-note sentence, the inserted family argument and the 27-row removal, all other manuscript bytes equal phase8. The 41 mathematical statements remain 27 lemmas, 9 theorems, 3 corollaries and 2 propositions.

The source accounting is therefore `256 individual + 27 two-family + 30 six-constant-family = 313`, with no duplicate or omitted replaced index. V1/v2 source snapshots and the independent v2 result remain preserved; v3 is the final text acceptance target.

## Execution and limits

The first v3 source-readback attempt stopped at a prose delimiter that crossed a line break; it wrote no result. The corrected reader uses the structural proof-end delimiter and passed. The preserved diagnostic summary records that failure. Neither the twenty-seven-case computation nor any old producer was rerun because of this locator error.

The retained exact results are `review-results-v2.json` and `review-results-v3.json`; the independent source diff is `candidate-v3-independent.diff`. This review performs no Hamilton-cycle search, enumeration of all fibre states, whole-manuscript proof audit, visual PDF review or main manuscript edit. The standard computation-record validator checks schema, relative paths and hashes only; the mathematical assessment above comes from the stated source and proof review.
