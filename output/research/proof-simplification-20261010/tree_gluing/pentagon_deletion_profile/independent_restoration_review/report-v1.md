# Selected 00101→10101 coordinate count: valid after exact-count correction

The actual phase6 source SHA256 is
`7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`.
The frozen note-v1 SHA256 is
`5a0e416aea3f1bb1ff99b922caee381ac3e721ca2e01398b485baf098062020b`.
The reader independently parsed C1-00101 and its8-edge pool from that
source, generated the proper listed states and used no peer helpers or
Hamilton search.

The target's prescribed first normalizer is indeed(shift0,direction-1,
colour permutation(01)), to standard00101. Its inverse is the involution
g(x)_j=p(x_{-j mod5}). The source and restored target cycles each cover
their64 legal states. Their common state set has40 states and87 edges.

For an edge that flips physical coordinate0, both endpoints must have
colours2 and3 because this coordinate excludes both0 and1 in the common
fibre. Its neighbours must avoid2 and3. The unchanged exclusion lists
therefore force x1=1 andx4=0. All seven such common edges are exactly

```
21010--31010  (x,y)=(0,1)
21020--31020  (0,2)
21030--31030  (0,3)
21210--31210  (2,1)
21230--31230  (2,3)
21310--31310  (3,1)
21320--31320  (3,2)
```

The two internal coordinates lie in{0,2,3} and{1,2,3}, excluding equality,
so the universe has3·3−2=7 edges. The involution preserves it and acts on
the pair as(x,y)→(p(y),p(x)).

The note's five listed pairs all occur in the source cycle, but the source
also contains21310--31310 consecutively in the printed third row. Its
actual seven-universe retention count is6, not exactly5. The target also
retains6; the extra source edge(3,1) maps to the target's extra edge(0,3).
Thus the full retained source edge set is not g-invariant. The five-edge
subset listed in the note is invariant and belongs to both cycles.

The source pool meets the seven-edge universe only at21010--31010. The
involution fixes this edge, so the union of the two pools removes just
one of the seven edges. Consequently each protected cycle contains five
edges of the remaining six-edge universe, and inclusion-exclusion gives
5+5−6=4 common protected edges. Direct checking gives exactly

```
21020--31020
21210--31210
21230--31230
21320--31320
```

The original weaker argument is still valid if “uses five” is changed to
“uses at least five”: its lower bound5+5−7−1=2 follows. Alternatively use
the exact count6+6−7−1=4. The end comment must describe only the listed
five-edge subset as invariant; asserting invariance of the entire
selected first-coordinate edge set is false. Neither error changes the
desired conclusion that at least two protected common edges exist.

The coarse whole-graph deletion data are also correct: each outside set
has six paths of order2 and two of order6, hence q=8 on either side; the
pool union has3 edges in the whole common graph. The lower bound
80−16−87−3=−26 gives no conclusion. The useful capacity count is restricted
to the seven coordinate0-flip edges and uses properties of these actual
selected cycle words.

Scope is exactly this selected source cycle, its restored target and their
specified pools. No arbitrary-Hamilton-cycle statement or assertion about
other interfaces follows. The main manuscript and original note bytes
were left untouched. The correction is reported for a separately frozen
note-v2, not silently applied to note-v1.
