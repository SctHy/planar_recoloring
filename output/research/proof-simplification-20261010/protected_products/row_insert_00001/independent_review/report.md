# Independent degree-balance obstruction: PASS

The fixed `00001` state graph has a sign partition `X` of size 20 and `Y` of size 24. The class `X` is independent. The only edges within `Y` are `12312--12313` and `13212--13213`. Independent enumeration from the five forbidden boundary colours gives exactly 44 legal states and 74 edges and verifies these assertions.

Consider any two-row seed and a matching `M` of its internal edges in the row to be cut. Write `t` for the number of cross-class matching edges and `r` for the number of `Y--Y` matching edges. Its endpoint counts in `X,Y` are respectively `t,t+2r`. A one-row insertion with no untouched vertices of the new row requires a spanning linear forest `L` with no isolated vertices whose degree-one vertices are exactly those endpoints. If `q` is its number of `Y--Y` edges, its degree sums give

\[
(48-t-2r)-(40-t)=2q,
\qquad r+q=4.
\]

Both `r` and `q` are at most two, so both equal two. Thus both available `Y--Y` edges occur in `M` and in `L`. All four of their endpoints are degree-one vertices of `L`, so each already has its unique incident edge in `L`. The old twelve-edge protected set includes `12313--12323`; this would give `12313` a second incident edge in `L`, a contradiction. Consequently **no two-row seed permits such an insertion while retaining the old protected set in the new row**.

The fixed printed old seed has 38 internal edges in each of its two rows, all crossing the classes. For this particular seed `r=0`, which would force `q=4`. Hence the printed seed admits no such one-row insertion even without any protection requirement.

These arguments apply only to insertion by deleting an internal matching and adding a spanning linear forest with exactly its endpoints. They do not rule out changing the seed, sacrificing a protected edge, using a broader rewiring, or a separate three-row construction. No Hamilton search was performed.
