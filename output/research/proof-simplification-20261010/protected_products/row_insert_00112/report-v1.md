# Protected three-row seed generated from the original two-row seed

The fixed 00112 insertion succeeds. Keep all eleven original K edges and
use only the two reserves 21020–23020 and 21030–31030. The new common-port
set is D'=K∪{these two reserves}, of size thirteen, and the new pool consists
of precisely those two edges. Thus K is exactly unchanged.

Cut second-old-row (leading digit 1) edges 12303–12323, 13203–23203 and
21201–23201. They are a matching of the existing C2 seed and none belongs to
D'. In the added row (leading digit 2), insert the first two edges as K2
paths and the displayed 47-state path from 21201 to 23201. Each replacement
has the same endpoints as its cut edge; its interior lies entirely in the
new row. The three interiors are disjoint and cover that row once. Replacing
edges of a cycle by these paths preserves one cycle, rather than requiring
an additional endpoint-pairing theorem.

Direct readback of candidate-v2.tex verifies every printed word, all thirteen
ports and the exact two-edge pool. The resulting 153-state cycle was
constructed for verification and checked for complete single coverage,
Cartesian-product adjacency including the closing edge, and all thirteen
ports in all three rows. It need not be printed. The final manuscript data
can use the 47-word path and three cuts instead of the 153-word C3 seed.
The original C2 seed and all original protected-interface witnesses remain
usable because the eleven K edges are unchanged.

Discovery was narrowly protected. The leaf condition excludes reserve
12320–12323. The 47-state core has 94 edges and exactly the three triangles
(21020,21021,21023), (21320,21321,21323), (23020,23021,23023).
Degree-two forced-edge propagation tests fifteen leaf-compatible reserve
pairs; six pass the necessary core-cycle screen. Those containing
12020–12030 force degree three at 12020, while those containing
13020–13030 leave 12030 with only one allowed core-cycle edge. No unprotected
Hamilton search was performed. For the successful pair, mandatory paths
contract the 47-core to nineteen segments. The separately bounded search
(at most 1,000,000 nodes and ten seconds) finds the certificate in twenty
nodes, about 0.001 seconds. The positive literal certificate is the result;
the screen alone would not establish Hamiltonicity.

The generic claim PC2⇒PC3 remains false. This construction uses the actual
00112 leaf structure, fixed K and printed 47-word path. Integration must
replace the old eighteen-port all-five-row assertion for this one type by
the new thirteen-port assertion. All seven old pool edges are still retained
in C2, but only the two selected reserves are required in the derived C3.
The original 153-word seed input is preserved byte for byte in the frozen
literal-input.tex, and the main manuscript was not edited by this agent.
