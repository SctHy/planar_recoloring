# Phase11 fixed K against necessary HC edges: bounded remaining-case check

Main has adopted the236 bidirectional one-fixed-K local certificates. Its47
remaining nonconstant interfaces are28 ordinary/ordinary,14 mixed and5 hard/hard.
Investigate whether sound forced-star necessity on the whole-HC side gives an
additional intersection with the specified fixed protected K, avoiding both
pools and retaining the original target first normalizer.

Read frozen forced-star summaries and saved one-fixed-K observations first.
Full closure edge sets are not serialized. For the18 ordinary HC types other
than00123, no edge is excluded and the final forced edges are exactly edges
incident with an original degree-two vertex. A safe fixed-K such edge was
already a positive one-sided certificate at that vertex; no remaining case
can gain globally. Do not regenerate these18 graphs or rerun230 interfaces.

Only3 remaining mixed interfaces have00123 on the whole-HC side:00112 pos1→3,
00112 pos2→3 forward, and00123 pos2→2 reverse. Generate only the00123 full legal
graph(57 vertices,122 edges), perform the sound necessity closure once, and
independently parse fixed00112 bases and pools from the frozen phase6 source.
Compare every saved local observation on these3 cases with its actual restored
HC star and fixed-K safe incidences. Check whether a forced safe edge exists
or at most one allowed incident edge is unsafe. Preserve the5 hard/hard
exclusions. No Hamilton-cycle search, paired-K intersection enumeration,
renormalization, complete230-case closure rerun, Main edit or old-file mutation.

Deliver the generic positive criterion and no-exclusion negative boundary,
exact limited result, failed/positive scope report and validated schema/hash
record. Write new assets only in fixed_K_forced_HC_v1.
