# Phase11 fixed K plus necessary HC edges

This branch adds exactly one finite interface to the236 one-fixed-K positives:
source00112, position1 changed to3, actual target03112, original first map
`[2,+1,2013]`, normalized target00123. The fixed source safe port
`12320–32320` maps to the standard target forced edge`31201–31231`.
Every whole-component target HC contains this edge, which avoids its prescribed
pool. The source K stays fixed. Conditional adoption would give237 covered
nonconstant interfaces and46 residual individual interfaces; Main is not edited.

## Why the remaining scope reduces to one graph

The frozen closure result saves graph summaries and selected positive local
witnesses, not complete forced/allowed edge sets. Of its19 HC types,18 exclude
no edge and stabilize within at most two passes. With no exclusions, allowed
stars remain full and all forced edges have an original degree-two endpoint.
If such an edge belongs to the safe fixed K, its degree-two endpoint was
already a positive original one-sided observation. Both endpoints of a safe
fixed edge belong to the HC component and are fixed-K endpoints, so the saved
checker included that endpoint. The allowed-star test is also identical to
the original degree test. This proves no gain for globally negative fixed-K
interfaces on those18 types; individual vertex bounds can still increase.

Exactly39 of the42 eligible residual interfaces are settled by that argument.
All28 residual ordinary/ordinary interfaces are among them. The5 hard/hard
interfaces remain ineligible because neither supplies a whole-component HC.
Only3 mixed residual interfaces have00123 on the HC side and need its changed
allowed/forced edge sets.

| Original interface | Direction | Saved candidate states | Closure bound | Outcome |
| --- | --- | ---: | ---: | --- |
| 00112 position1→3 | F | 15 | 1 | Newly covered |
| 00112 position2→3 | F | 13 | 0 | Criterion inconclusive |
| 00123 position2→2 | R | 13 | 0 | Criterion inconclusive |

The42-case audit therefore finds no further ordinary/ordinary gain and only
one mixed gain. A zero result is a limitation of this necessity criterion,
not a nonintersection or Hamiltonicity claim.

## General criterion and the short positive proof

On the whole-HC side, let A contain every possible HC edge and F contain edges
forced in every HC. At a common actual state v, let S be fixed-K incident edges
belonging to the full HC graph and avoiding its pool. The fixed K already
excludes its own pool. Any HC has at least
`max(0, |F∩S|, 2−|A(v)\S|)` safe edges at v. Thus either a forced safe edge or
at most one allowed unsafe incident edge is sufficient. This uses HC existence
as a premise; surviving necessity closure never establishes HC existence.

The new port needs only four directly checked full stars in standard00123:

| v | N(v) |
| --- | --- |
| 21301 | 21201,31301 |
| 23201 | 21201,23231 |
| 32301 | 31301,32302 |
| 31201 | 21201,31202,31231,31301 |

The first three degree-two vertices force two HC edges at21201 and at31301.
Their edges to31201 are excluded. The two remaining neighbors31202 and31231
are consequently forced at31201. The original map sends the specified source
edge to31201–31231. Independent parsing verifies source protected-K membership
and both pool exclusions. This analytic proof needs neither the other forced
edges nor a HC search. It asserts this one interface; no uniform symbolic
classification of all remaining interfaces is inferred.

In actual source coordinates,12320 has full HC neighbors10320,12020,12323,32320
and only the safe K neighbor32320. Its originald4/g1 bound is zero; necessity
closure leaves allowed and forced neighbors10320,32320. At32320 the same safe
edge is forced although the originalfull degree is five. Both give bound one.

## Actual limited computation and verification

CPython3.14.6 executed one independently implemented00123 graph and closure:
57 legal states,122 full edges,14 forced edges,8 excluded edges,5 passes. These
five summary fields exactly reproduce the frozen author result. The graph is
generated from legality, not selected cycle edges; the frozen printed word set
is read only as a57-vertex component identity/completeness cross-check.

The program evaluates precisely41 saved candidate-state observations in the
three mixed interfaces. It independently parses the hard00112 protected basis
and fixed pools, applies the saved original maps without normalizing again,
and matches every full-star and safe-K list. It saves all allowed, forced and
unsafe stars, including the two inconclusive interfaces, and the entire single
closure trace. The material run took0.045 seconds. Input SHA256 values were
checked unchanged before and after.

An independent checker then verifies only the four displayed full stars by
direct coordinate legality, the fixed-K port membership, two pool exclusions,
the actual original map identity and legality at both original boundaries.
It does not rebuild the57-state graph. An independent peer reviewed the
no-exclusion negative argument and confirmed that complete endpoint checking
is the required premise.

No18-graph regeneration,230-interface paired-HC run,959493 pair comparisons,
HC search, paired-K intersection enumeration, Main edit or frozen-input mutation
occurs. The finite237 count inherits the earlier236 case set. It remains a
one-fixed-side statement; it is not an arbitrary-both-HC theorem. The extra
four-star proof has not been measured in a full manuscript, so no page or proof
length reduction is claimed.

The standard computation record binds the exact input/code/result/report files.
Its validator checks schema and hashes only, not the mathematical lemma or
the graph algorithm's correctness.
