# Fixed 00001 protected row insertion

The original K12 cannot be retained by any one-row matching insertion,
regardless of the two-row seed or the number of cuts. The sign partition
has X20 independent and Y24 with exactly two Y edges. If r counts Y-edge
cuts and q the Y edges in the new-row forest, degree balance gives r+q=4.
Both are therefore two, forcing the four Y-edge endpoints to form two K2
components. The original K edge 12313--12323 conflicts with this. The
independent reader has verified the count proof and all literal graph data.

Deleting only that K edge breaks two self-type interfaces. Adding either
13120--23120 or 21320--31320 repairs all313 interface memberships and passes
the initial degree and forced-cycle screens. However, a second exact
endpoint-matching obstruction remains: the protected edges13210--23210,
13230--13232,13230--23230 make13210 a forest endpoint with no possible cut
partner. This excludes every number of cuts and every two-row seed. The
proof is in endpoint-obstruction-v1.tex. Consequently one of those three
protected edges must also be removed. The raw40-state core has no leaves;
the earlier tentative four-leaf/six-cut shortcut was false and is preserved
separately as a failed structural guess.

The successful redesign is K11=(oldK12 minus12313--12323 and13230--23230)
plus13120--23120. Its two reserves are the old pool edges21210--21213 and
21230--31230, giving D13. All283 individual interfaces and all30 images of
the six constant-source families have common auxiliary edges; exactly three
individual witnesses need the printed replacements. No constant-family
rule changes.

A protected two-row seed was obtained through specified local changes and
rectangle switches. The first protected factor merge used4 nodes/.0013s;
after the second K deletion, another merge used3 nodes. Both searches had
explicit50000-node/10-second limits. Two repeated rectangle toggles cancel,
so the final cycle is reconstructed from the original88-word seed by seven
listed small boundary toggles. The final two-row cycle has allD13 edges in
both rows and three unprotected disjoint cuts in row digit1:
12312--12313,13212--13213,13210--13230.

The new row consists of the first two K2 edges and a40-state protected path
from13210 to13230. Forced-path contraction leaves11 segments; bounded DFS
found the path in12 nodes/.0014s under a1-million-node/10-second limit.
Replacing the three cuts by those new-row paths with vertical endpoints
subdivides edges of a single cycle, so it gives a Hamilton cycle of all132
states. Full reconstruction checks all132 distinct states, every Cartesian
edge including closure, and every D13 edge in every row. No generic
unprotected Hamilton search and no original-graph search were performed.

candidate-v1.tex is the complete seven-toggle/path/port/interface candidate.
check_candidate_v1.py reads its TeX literally and reconstructs both cycles;
candidate-readback-v1.json is PASS. Independent sibling checks separately
generated the44-state graph and reconstructed the successful132-state cycle
without importing the discovery code. The earlier core40-path-results-v1
UNKNOWN output is retained byte-for-byte; its19 attempted cuts actually all
failed degree closure, and the broader status was kept UNKNOWN. The later
successful v2 uses a different auxiliary set and is a separate artifact.

For the manuscript, printing the new88-word two-row seed directly and the
40-word core path avoids introducing the seven-toggle method into the
exposition. The original132-word three-row seed can then be replaced by the
same three-path insertion rule already used for00112, reducing the state
certificate by92 words. The seven-toggle derivation remains reproducible
research provenance. Main manuscript and old frozen seed/table bytes have
not been edited by this agent.
