# Fixed-support symmetry fails; weak transport gives a print candidate

None of the 21 nonconstant specified cycle/common-seed supports has a
nonidentity natural boundary symmetry. More strongly, no strict reduction of
its old pool can produce a seed-compatible K invariant under any nonidentity
natural boundary action. This excludes the proposed globally symmetric K
route without a cycle or seed redesign.

There is a different finite print-compression candidate: the 283 interfaces
split into 147 natural interface orbits. A witness transport core succeeds
for 133 orbits, covering 246 interfaces. The other 14 orbits contain 37
interfaces, which remain individual records. The resulting file has
133+37=170 representatives, saving 113 printed records. This count is identical
for the existing nonconstant pools and the tested four/two-edge pools.

This is not currently a shorter analytic proof. Each successful transport
family still needs its displayed edge memberships verified against the actual
chosen source and normalized target supports. No common structural argument
like the constant case's two normalization directions and four target edges
has been proved for these 133 families. The candidate is preserved separately
and is not recommended for automatic manuscript integration.

## Exact obstruction to globally symmetric K

Let E be the fixed cycle edge set or the hard common-seed edge set. For a
nonidentity natural action g, every g-invariant K contained in E lies in

    J_g = intersection_(r=0,...,order(g)-1) g^r(E).

For an ordinary component, remove from J_g the complete g-orbits of the two
already-used seed-cut edges as well. Call the resulting maximal allowed set
J'_g. Then every compatible pool must delete at least |E minus J'_g| edges.
For a hard component J'_g=J_g, because every edge of its specified common set
occurs in all five seed rows.

The following table minimizes this exact deletion bound over every nonidentity
natural boundary action. All values exceed the old pool size, so even keeping
the old number of pool edges would not suffice, much less shrinking it.

| Type | Natural boundary group size | Fixed support stabilizer size | Minimum necessary pool deletions | Old pool size |
|---|---:|---:|---:|---:|
| 00001 | 4 | 1 | 11 | 7 |
| 00011 | 4 | 1 | 12 | 8 |
| 00012 | 2 | 1 | 20 | 8 |
| 00101 | 4 | 1 | 16 | 8 |
| 00102 | 2 | 1 | 27 | 8 |
| 00112 | 2 | 1 | 14 | 7 |
| 00121 | 2 | 1 | 24 | 8 |
| 00123 | 2 | 1 | 20 | 8 |
| 01012 | 2 | 1 | 46 | 8 |
| 01023 | 2 | 1 | 28 | 8 |
| 0000* | 12 | 1 | 16 | 8 |
| 0001* | 2 | 1 | 26 | 8 |
| 0010* | 2 | 1 | 33 | 8 |
| 0011* | 4 | 1 | 14 | 8 |
| 0012* | 1 | 1 | no nonidentity action | 8 |
| 0101* | 4 | 1 | 35 | 8 |
| 0102* | 1 | 1 | no nonidentity action | 8 |
| 0110* | 4 | 1 | 36 | 8 |
| 0112* | 2 | 1 | 45 | 8 |
| 0120* | 2 | 1 | 54 | 8 |
| 0123* | 2 | 1 | 52 | 8 |

The actual intersection of all five hard seed rows is exactly the printed
D: nineteen edges for 00001 and eighteen for 00112. Thus no larger unprinted
common edge set is available to repair their support symmetry without changing
the seeds. `support-results.json` includes, for every rejected action, an
explicit support edge whose image leaves the fixed support, and the complete
forced-deletion set establishing each bound. These are fixed finite supports;
the result does not exclude different cycles or seeds.

## Weak transport experiment

For a fixed interface i from source t, write T_i for its actual restored
target K. Let H_t be the full natural boundary stabilizer, including coordinate
rotations/reflections and colour permutations. A group action changes the
position and new excluded colour and transports the actual target component.
Define

    W_i = intersection_(g in H_t) g^(-1)(K_t intersect T_(g i)).

If e belongs to W_i, then g(e) is a valid shared protected edge at every
interface g i. This implication is elementary and does not assume that K_t
or the canonical target K is globally invariant. The experiment computes W_i
exactly, including all actions stabilizing a record itself. This conservative
full-group test is stronger than merely choosing one favorable action per
record. No proper-subgroup or favorable-coset optimization was performed.

Crucially, target component transport is determined by its full restored
state set. The two constant target components are never identified. This
avoids the invalid 312-orbit shortcut detected in the earlier experiment.

A small successful example is source 00001, position 1 changing to excluded
colour 1, target 00101. Its seed `12132--32132` transports under coordinate
reflection (shift 3, direction -1) to `31212--31232` at position 2. Both
memberships are directly verified even though the entire source K is not
reflection-invariant.

### Exact print counts

| Nonconstant pools | All original 313 shared-K tests | Natural interface orbits | Successful families | Interfaces covered by families | Individual fallbacks | Printed representatives |
|---|:---:|---:|---:|---:|---:|---:|
| Existing eight/seven | pass | 147 | 133 | 246 | 37 | 170 |
| Four/two candidate | pass | 147 | 133 | 246 | 37 | 170 |

Both variants use the already verified constant five-edge orbit pools, with
orbit indices (1,0). The original 313 input records remain byte-identical;
new witnesses are saved separately. The manuscript's current six constant
families and 283 individual records were not changed.

`existing-nonconstant-pools-representatives.txt` is the candidate that leaves
the current nonconstant pools unchanged. Each of its family lines represents
the exact orbit recorded in `witness-orbit-results.json`; each individual line
is directly checked. The four/two version has its own independent text file.

## Failure boundaries, with all 37 interfaces preserved

Thirteen failed full-group orbits have empty W even before any pool deletions:
their raw cycle/common-seed supports already fail the required transported
edge intersection. One further four-record orbit has two raw transport seeds,
both blocked by pool choices. The full 37 interfaces and a valid separate
witness for each are in the two `*-failed-interfaces.json` files. Failure means
failure of this particular full-group single-seed compression, not failure of
the individual shared-edge lemma.

The fourteen representative failures are:

| Source | Changed position | New excluded colour | Target | Orbit size | Raw transport seeds |
|---|---:|---:|---|---:|---:|
| 00001 | 0 | 1 | 00011 | 2 | 0 |
| 00001 | 0 | 2 | 00012 | 4 | 0 |
| 00001 | 4 | 2 | 00001 | 2 | 0 |
| 00011 | 0 | 2 | 00112 | 4 | 2 |
| 00011 | 1 | 1 | 00101 | 1 | 0 |
| 00011 | 3 | 0 | 00001 | 2 | 0 |
| 00101 | 0 | 1 | 00101 | 2 | 0 |
| 00101 | 3 | 1 | 00011 | 1 | 0 |
| 00112 | 0 | 2 | 00112 | 2 | 0 |
| 00112 | 1 | 2 | 00121 | 2 | 0 |
| 00112 | 4 | 3 | 00112 | 1 | 0 |
| 0000* | 0 | 1 | 0001* | 6 | 0 |
| 0000* | 1 | 1 | 0010* | 6 | 0 |
| 0101* | 0 | 1 | 0010* | 2 | 0 |

For the exceptional 00011→00112 orbit, the raw seeds are
`13202--13203` and `31202--31302`. The former always normalizes to
`32021--32031`, currently a target reserve edge. The latter is blocked at the
source by its `31202--31302` reserve. The four/two test selected the old last
two reserves, so these particular blockers remained. This suggests a small
targeted pool repair, distinct from the impossible global-symmetry route;
a new pool choice could expose one of these orbit seeds while monotonically
retaining all old shared edges. That local repair is a next candidate, not
part of the 170-representative result recorded here.

## Safe pool reduction without symmetry

The file `four-two-pools.tex` gives an ordered candidate: for each ordinary
nonconstant type keep its old first two edges, then its old last two edges;
for each hard type keep only its old last two common edges. The old cycles and
seeds remain identical. The first two ordinary edges still perform the old
seed splices, and the two remaining edges supply the ordered-block joins.
For hard types both selected edges occur in every seed row.

Every new pool is a subset of its old pool, so the corresponding K only grows.
Hence all already valid 313 protected intersections remain valid; this is a
monotonicity proof, separately replayed by the exact checker. The reduction
removes 86 printed pool-edge entries across the 21 types. It changes neither
the product method nor the failed global symmetry conclusion.

A second possible intersection approach is the pigeonhole criterion
`|E_A intersect restored(E_B)| > |pool_A|+|pool_B|`, which guarantees a
protected common edge without choosing a witness. It holds for 180 of the
283 cases with the existing pools and 254 with the four/two candidate. Those
counts are finite observations; no uniform analytic raw-edge lower bound has
been proved for the fixed asymmetric cycles. Replacing the witness table by
254 raw-count checks would merely change the format of its finite premises.

## Reproduction and evidence

Run `python3 check_support_symmetries.py` and `python3 check_witness_orbits.py`
in this directory. They import only the frozen `base_check.py`, use exact
tuple/edge sets, and perform no Hamilton search. The support check also reads
the manuscript to verify the relevant nonconstant cycle/seed/pool tags remain
equal to the frozen input; it never writes the manuscript. The two main
computations took approximately 0.04 and 0.20 seconds on Python 3.14.3.

The frozen original input SHA-256 is
`714dd7fa30ea60e9e54a9ce798763000c2bd91ec3f9884ece02f7b4e94a8dd63`.
The checked manuscript snapshot SHA-256 is
`6ae559d6418dd963f5093ab700deb5f36b2385f130d657b20916096a55b24227`.
The scope is exactly these specified supports, natural actions, pool versions,
and listed interfaces. No new general equivariance theorem or replacement
cycle construction is claimed.
