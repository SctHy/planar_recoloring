# The listed pentagon 00112 is traceable

The graph has 51 vertices and 100 edges. Its only leaves are `12303`, with
neighbor `12323`, and `13203`, with neighbor `23203`. Consequently any Hamilton
path must have those two endpoints. The following sequence is a Hamilton path:

```text
12303 12323 12023 13023 13020 12020 12320 32320 31320
21320 21323 21303 21203 21201 21301 21321 31321 32321
32301 31301 31201 31231 31230 21230 21231 21031 21030
31030 31031 32031 32021 31021 31020 32020 32030 12030
13030 13230 23230 23030 23020 21020 21021 21023 23023
23021 23031 23231 23201 23203 13203
```

Every word is a proper coloring of C5 and avoids the excluded color at its
position in `00112`. Each consecutive pair differs in exactly one coordinate.
The sequence has 51 distinct words, equal to the whole listed state set. These
three exact checks prove traceability; the search algorithm is not needed to
trust the resulting certificate. The independent state-set check also matches
the projection of the existing frozen two-row seed.

## Initial cut checks and bounded discovery

For endpoints a,b, a Hamilton path implies
`c(B-S) <= |S|+1-|S intersect {a,b}|`: deleting an endpoint does not create an
extra path component. All 272052 cuts of size at most four satisfy this
strengthened necessary bound. The complete layers checked had sizes
1, 51, 1275, 20825, 249900. This did not itself prove traceability; it motivated
the bounded local path discovery.

The discovery budget was ten seconds and two million nodes. A deterministic
remaining-degree search with degree and connectivity pruning found the path
in 56 nodes, about 0.0015 seconds, with two memoized failed states. This was a
search of the fixed 51-state listed pentagon only, not the original graph.
`find_hamilton_path.py` rechecks the returned path directly as words, without
using the search adjacency bitsets.

## Direction of use in protected products

For the current constant-source product candidate, the protected first factor
is A=C15, and this listed graph plays the second factor B. Following the
Hamilton path of B orders the copies of A and requires no protected edges
inside B. Thus this certificate supplies exactly the traceability assumption
needed in that direction.

If instead 00112 plays a first factor whose existing K must be retained, this
particular path is not a direct replacement of the current seeds. It contains
8 of the 11 existing protected K edges and omits
`21020--31020`, `21030--21230`, `32030--32031`. No constrained-path search was
performed, and no nonexistence claim is made for a path containing those edges.

## Reproduction and evidence

Run `python3 check_small_cuts.py 4` and `python3 find_hamilton_path.py` in this
directory. All calculations use exact finite words, integers, and edge sets.
The available backend is Python 3.14.3. The frozen input SHA-256 is
`714dd7fa30ea60e9e54a9ce798763000c2bd91ec3f9884ece02f7b4e94a8dd63`.

`path-results.json` gives the complete path certificate. `results.json` gives
the bounded cut checks. The cut tests have bounded scope; the displayed path
is a complete proof certificate for this fixed graph. The manuscript, formal
research library, and original literal records remain unchanged.
