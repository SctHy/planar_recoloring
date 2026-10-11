# The listed pentagon 00001 is not traceable

There is a short structural obstruction, with an explicit 20-vertex cut. The
graph has 44 states and 74 edges. It splits into a 24-state core R3(P4), where
the last color is 0, and two induced P10 paths, where the last color is 2 or 3.
These paths are exactly the constant C15 components after deleting the five
consecutive states whose last color is 1.

The two ears, in path order, are:

```text
23123 13123 12123 12323 12313 12312 32312 31312 31212 31232
21323 21313 21213 23213 13213 13212 13232 13132 12132 32132
```

Their endpoint images in the core are respectively `23120,31230` and
`21320,32130`, obtained by changing the last color to 0. In fact every ear
state has an edge to its corresponding core state; the word “ear” here
describes the induced outside path, not a path attached only at its ends.

## Sign and cut proof

Orient the three colors cyclically 1→2→3→1, and put epsilon(a,b)=+1 when b
follows a and -1 otherwise. For a state w, define

    sigma(w) = epsilon(w1,w2) epsilon(w3,w4),
    chi(w)   = sigma(w) if w5=0, and -sigma(w) otherwise.

A move at any of the first four positions flips exactly one factor of sigma,
so flips chi. A last-position move between 0 and 2 or 3 also flips chi.
A last-position move between 2 and 3 is possible only when w1=w4=1, so its
prefix must be `1231` or `1321`. Thus the only same-sign edges are
`12312--12313` and `13212--13213`; both have chi=-1.

The core has twelve states of each sigma sign: replacing w1 by the other
color different from w2 gives a sign-reversing involution. Along each P10
the unique same-sign edge is central and has chi=-1. The other eight edges
flip chi, yielding six negative and four positive states per ear. Therefore
the full graph has 24 negative and 20 positive states.

Take S to be the twenty chi-positive states. After deleting S, the twenty-four
remaining states have only the two disjoint edges displayed above, hence
twenty-two components. Every traceable graph satisfies
`c(B-S) <= |S|+1`, since deleting |S| vertices from a spanning path leaves at
most |S|+1 pieces. Here 22>21, proving nontraceability.

The exact cut is:

```text
12120 12132 12310 12323 13123 13130 13210 13232 21210 21313
21320 23120 23213 23230 31212 31230 31310 32130 32312 32320
```

This is also an edge-capacity obstruction: a path covering 24 negative and
20 positive vertices needs at least three negative-negative edges, but the
whole graph has only two.

## Why the proposed core-path construction fails

The core's two sigma classes both have twelve states. Each of the four ear
endpoint images has sigma=+1. Every Hamilton path in this balanced bipartite
core must have opposite-sign endpoints. Hence neither ear's two endpoint
images can be joined by a 24-state core Hamilton path. The proposed 34-cycle
construction fails already at this endpoint condition, independently of the
stronger full-graph nontraceability proof.

## Maximum independent set is exactly 22

The core involution gives twelve disjoint matching edges. Each P10 gives five
more, so the whole graph has a perfect matching of twenty-two edges. Every
independent set has size at most twenty-two. Conversely, take the negative
class and remove one endpoint from each of its two internal edges: this gives
an independent set of twenty-two. Both exact certificates are in `results.json`.
Thus the suggested independent-set threshold 23 does not explain the failure;
the 20-cut does.

## Compatibility with ordered-block product gluing

This obstruction rules out using a Hamilton path of B=00001. It does not
prevent partitioning B into P2/P3 blocks whose quotient has a Hamilton path.
The quotient orders whole blocks and merely specifies one actual B edge at
each interface; it need not lift to a Hamilton path of B.

For such an ordered block family, use the existing protected product seed
inside every block. Choose two distinct common reserve edges e,f of A.
At interface i use e for odd i and f for even i, deleting their copies in
the two incident physical rows and adding the two crossing product edges.
The two interfaces of any intermediate block use different reserves. This
holds even if both interfaces meet the same physical B state. Consequently
each requested edge is still present when used, every splice joins two
disjoint cycles, and every K_A edge remains in every row. The argument uses
the old seeds and old pools; it requires neither traceability of B nor an
external factor/load theorem. A proposed quotient ordering must still be
verified independently against actual B edges.

## Verification and boundaries

`check_structure.py` generates the 44 legal states and all 74 single-coordinate
edges independently, checks equality with the frozen graph input, checks the
two C15 deletions and P10s, verifies all sign claims, and emits the explicit
cut, matching, and independent set. It does not perform a Hamilton-path search.
Its exact run took about 0.0012 seconds on Python 3.14.3.

The graph-input SHA-256 is
`021ee260d2a7a8848d4b984bdae1d2dfd5be95db2d3dd70daa1bcbe92be150e3`.
The original literal-input SHA-256 remains
`714dd7fa30ea60e9e54a9ce798763000c2bd91ec3f9884ece02f7b4e94a8dd63`.
The earlier UNKNOWN search artifacts, manuscript, and formal research library
were not modified. Nontraceability is established by the cut certificate,
not by a failed or bounded search.
