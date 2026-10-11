# Four residual hard--hard weak-port certificates

All four designated actual interfaces pass. The first normalizers were
independently recomputed in the specified offset/direction/permutation order,
then compared with the saved original case map. The actual live main hard
COMMON/PORTS and POOL blocks match the frozen basis input exactly.

| Source edit | Prescribed map `(offset, direction, permutation)` | Source protected port | Target protected port |
| --- | --- | --- | --- |
| 00001 position4->2 | `(0,+1,[0,2,1,3])` | 13210--23210 | 13120--23120 |
| 00001 position4->3 | `(0,+1,[0,2,3,1])` | 12310--32310 | 13120--23120 |
| 00112 position0->2 | `(0,-1,[2,1,0,3])` | 12023--13023 | 13020--13023 |
| 00112 position3->2 | `(1,-1,[0,2,1,3])` | 13030--13230 | 32030--32031 |

For the first pair, the fixed target port13120--23120 works for both
actual prescribed maps; the suggested inverse images are confirmed.
For the latter two interfaces, the two reflection/colour maps are
involutions swapping the two listed port pairs. Each interface needs only
one named source port and one image membership. This is shorter in proof
dependencies than deriving a joint endpoint-support graph. The two00112
arguments use different pairs; no claim that one fixed port handles both
is needed or made.

The proof is the designated-port criterion: e in actual K_source and g(e)
in actual K_target imply e in K_source and restored K_target. The script
checks seven distinct standard-K memberships, pool exclusion, forward and
inverse identities, legality of source endpoints at both actual boundaries,
and the four original map identities. It does not enumerate paired-K
intersections or require either hard graph to have a Hamilton cycle. The
hard sets are common seed ports minus their two-edge pools.

The saved v4 uniform relative-map-group capacity criterion remains
inconclusive for 00001 position4->2, 00001 position4->3, and00112
position0->2. Its surviving missing budgets and minimum retaining vectors
are retained in the result. These are failures of a uniform group bound,
not failures of actual common-port membership. For00112 position3->2,
the old group capacity is already positive in coordinates2 and4.
No capacity producer or joint support graph was rerun.

The frozen v3 P2/P3 residual descriptions apply respectively to00001
position4->3 and00112 position0->2. They do not describe both00112
interfaces. The new named-port proof removes the need to invoke those
support shapes for these four cases; it does not alter their old evidence.

The four case identities exactly equal v6's ending remainder. Appending
them to its forty-nine retained identities gives exactly the saved
fifty-three-case hard-interface universe. This completes coverage using
the mixed degree and weak-transport mechanisms, with their original
specified maps, bases and pools. The earlier forty-nine mathematical
dependencies are inherited rather than re-reviewed here. This is not a
single symbolic uniform classification of all53, not whole-template
symmetry, and not a statement about arbitrary pools or normalizers.

Python3.14.6 executed only the four designated checks. The first attempt
failed while reading the live manuscript because the root path was one
level too shallow; no port check had run. That failure is retained, the
path was corrected, and the same authorized four checks then passed.
No prior producer, full fibre, Hamilton search or manuscript edit was
performed. The computation-record validator checks schema and hashes only,
not mathematics, external review or theorem completion.
