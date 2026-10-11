# Constant C15 orbit pools: exact local result

All nine pool choices preserve a common protected edge at every one of the 313
existing directed interfaces. The stricter proposed statement that the
canonical target-K family is rotation-equivariant is false. Nevertheless, a
weaker edge-by-edge transport certificate succeeds: each of the six
constant-source rotation orbits has a protected edge whose five rotations
belong to the five actual target K sets. This permits a six-record certificate
for those thirty interfaces, if stated as the explicit finite transport
identity below. It does not permit a claim that the entire target family is
equivariant.

This is a research alternative. The original manuscript and its 313 literal
records were not changed. The other 21 components, their cycles/seeds, pools,
and K sets are identical to the frozen existing input. There was no Hamilton
search.

## Feasibility and protected product

Coordinate rotation fixes each of the two constant components as a set and
acts on its C15 edges in three orbits of size five. A selected orbit O is a
pool, and K=E(C15) minus O is rotation-invariant with ten edges. Allocate any
two distinct edges a,b of O to the small seeds. For P2, splice two copies of
the C15 at a. For P3, first splice rows 1,2 at a, then splice rows 2,3 at b.
Both constructions preserve K in every row. All three edges of O minus {a,b}
remain available in every row for external joins.

The previously verified Ellingham--Zha theorem supplies a connected factor
extension with at most three added edges incident to each physical state.
Each joining edge therefore has an unused reserve in both rows. This is the
same row-count argument as the manuscript's six-reserve version with three
in place of six. It requires the load-three theorem and its component-cut
hypothesis; the AAE isolated-vertex condition alone does not supply that
hypothesis. If the manuscript retains only the shorter isolated-vertex proof,
this alternative needs the earlier complete cut bound as well. This extra
proof/dependency cost is material relative to saving 24 interface records.

## All nine choices

Orbit indices 0,1,2 are defined by the exact lexicographic edge lists in
`results.json`, not by an ambiguous visual ordering.

| Pool orbit in component 0 | Pool orbit in component 1 | Common K at all 313 | Old witnesses requiring reselection | Six transported witnesses |
|---:|---:|:---:|---:|:---:|
| 0 | 0 | yes | 14 | yes |
| 0 | 1 | yes | 17 | yes |
| 0 | 2 | yes | 15 | yes |
| 1 | 0 | yes | 5 | yes |
| 1 | 1 | yes | 8 | yes |
| 1 | 2 | yes | 6 | yes |
| 2 | 0 | yes | 9 | yes |
| 2 | 1 | yes | 12 | yes |
| 2 | 2 | yes | 10 | yes |

All 313 reselected witnesses for every choice, every changed old witness, and
all thirty transported constant-source witnesses are saved separately in
`results.json`. The frozen original literal input remains byte-identical.

## Failure of full target equivariance

There are thirty constant-source records and four nonidentity rotations for
each. Full target-K equality fails in 72 of these 120 tests. For example, take
source `00000:0`, change position 0 to excluded colour 1, and rotate by
rho_2(w)_j=w_(j+2 mod 5). The changed position becomes 3. Both transformed
and actual target K sets have twelve edges, but their symmetric difference
has sixteen edges. The transformed set contains `12302--32302`, which the
actual canonical target K omits. Thus source-K invariance cannot justify
equivariance of target K.

## Exact weaker identity for thirty-to-six compression

Let T_(j,c)^i be the actual target K, restored from the prescribed canonical
normalization into the coordinates of constant source component i, after
position j changes from excluded colour 0 to c. For each i in {0,1} and
c in {1,2,3}, form the finite set

    W_(i,c) = E(C15_i) intersect
              intersection_(r=0,...,4) rho_(-r)(T_(-r mod 5,c)^i).

Every W_(i,c) has exactly two edges, listed below. For all nine selected pool
pairs, W_(i,c) minus O_i is nonempty: its two edges lie in different rotation
orbits, whereas O_i is only one orbit. Pick e in that difference. Since O_i is
rotation-invariant, rho_r(e) belongs to source K; by the displayed identity it
also belongs to the actual target K at position -r. This supplies all five
interfaces from one witness without assuming any target-set equality.

| Source component | New excluded colour | Exact two-edge W |
|---|---:|---|
| `00000:0` | 1 | `23121--23123`, `31312--32312` |
| `00000:0` | 2 | `12123--13123`, `31231--31232` |
| `00000:0` | 3 | `12312--12313`, `21231--23231` |
| `00000:1` | 1 | `21213--23213`, `32131--32132` |
| `00000:1` | 2 | `13212--13213`, `31321--32321` |
| `00000:1` | 3 | `12132--13132`, `21321--21323` |

For the choice (1,0), which changes the fewest old witnesses, one may use the
six position-0 seeds, in the same order as this table:

    23121--23123, 31231--31232, 21231--23231,
    21213--23213, 31321--32321, 21321--21323.

The code explicitly validates each of their thirty rotated edges against the
actual normalized target, as well as deriving them by intersection. The
remaining 283 records stay as individual records; a certificate using this
specific compression would have 283+6=289 representative records. There is
no evidence here that the remaining 283 can also be compressed.

## Reproduction and limits

Run `python3 check_orbit_pools.py` in this directory. It imports only the frozen
helper `base_check.py` and reads `literal-input.tex`; it does not read or write
the manuscript. All graph-state and edge computations are exact integer/tuple
sets. Runtime was about 0.22 seconds on the available Python 3.14.3 backend.
The input SHA-256 is
`714dd7fa30ea60e9e54a9ce798763000c2bd91ec3f9884ece02f7b4e94a8dd63`.

The computation proves the finite stated identities for the existing 23
types and normalization, together with the nine explicitly redesigned pool
pairs. It is not an analytic replacement of the full interface calculation,
and it gives no general target-equivariance theorem. The algebraic seed and
row-reserve argument above is separate from the finite interface membership
checks. No integration into the main proof has been performed.
