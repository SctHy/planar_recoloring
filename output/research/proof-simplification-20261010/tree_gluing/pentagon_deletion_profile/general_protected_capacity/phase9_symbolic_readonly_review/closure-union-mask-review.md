# Independent mathematical and code read-only review

This review reads the actual forced-star lemma/checker and union-mask
selector checker. It does not replay the230-interface computations or run
new graph searches. The four hard--hard port certificates are already
frozen in hard_hard_weak_transport_v1 and are a separate result.

## Sound forced-star closure

The necessity lemma is correct conditional on existence of a Hamilton
cycle in the full input component. Initially every Hamilton cycle uses
allowed edges and contains the empty forced set. If a vertex has only
two allowed edges, both must occur in every Hamilton cycle. If it has
two forced edges, all other incident edges must be absent. These facts
are undirected and preserve the invariant at both endpoints. Performing
the implications simultaneously is sound: an edge cannot be both newly
forced and excluded while an existing Hamilton cycle satisfies the
previous invariant. The code's symmetry updates and assertions implement
this exactly. It does not infer Hamiltonicity from successful closure.

The local pair families list every two-neighbour subset of the final
allowed star containing all forced neighbours. Actual Hamilton-cycle
stars belong to these families, but some listed stars may not extend to
Hamilton cycles. Minimizing the pool-free intersection over this larger
family is therefore a valid lower bound. In the code, a shared neighbour
w represents exactly the same edge x--w in both stars, and unsafe=P union
restoredQ correctly removes either pool. The baseline four-degree bound
is a valid comparison; closure only restricts its candidate pairs.

The checker generates legal words from the palette and list condition,
generates actual one-coordinate neighbours, checks closure and connectedness
of each nonconstant ordinary component, and restores both adjacency and
forced/allowed stars through the same first normalizer. The normalizer
order matches offsets0..4, signs+1,-1, and lexicographic permutations.
The star digit4 is retained by normalization and excludes no palette
colour in the legality/neighbour tests. Hard and constant types are
explicitly excluded. Parsed individual witness endpoints are unused;
selected cycle words and edge sets do not define the generated graphs.

A small00123 neighbourhood calculation performed earlier in this agent's
v2 review independently supports the closure mechanism, without another
run here:

```
N(21301) = {21201,31301}
N(32301) = {31301,32302}
N(31301) = {21301,31201,31302,32301}
```

Thus21301--31301 and32301--31301 are forced by degree two at the
outer endpoints. At31301 they exhaust the cycle degree, so
31301--31201 and31301--31302 are excluded. This checks a local
part of the reported00123 propagation, not its full14-forced/8-excluded
count or the global coverage totals. The recorded125/230 and no improved
interface maximum remain inherited exact experiment results.

## Three-edge incident-union condition

Let x be legal in both full components. If
|N_source(x) union N_target(x)|<=3, each arbitrary Hamilton cycle uses
two neighbours from this same incident-edge universe. Two2-element sets
inside a universe of at most3 have a common member. A common member is
automatically a legal common edge. If every common incident edge avoids
both prescribed pools (f=0), that edge is safe. This argument also covers
union size2, where both edges are forced; the statement should use <=3,
not equality3, when applied to the complete125-case selector.

For a single changed non-star boundary entry j:a->q, the only target
mutation absent from the source star is recolouring x_j to the old
forbidden colour a. Since x is common and q!=a, this mutation is legal
exactly when a is absent from the two neighbours of x_j. Thus the full
incident union has size d_source+alpha with
alpha=1[a notin{x_(j-1),x_(j+1)}]. The non-star and common-state
qualifiers are necessary. This is an incident union at the same vertex,
not an assertion that each edge in that union belongs to both graphs.
Existence of the two component Hamilton cycles is a separate premise.

## Mask dynamic programming

find_union_covers.py filters the frozen positive certificates by f=0
and d_source+d_target-d_common<=3, and requires a surviving certificate
for each of the125 input cases. Each candidate word gets the bit mask
of exactly the cases it covers within its source type. At each word the
DP keeps the old states and adds that word once to every preceding mask.
For a fixed achieved mask, a shorter selected subset dominates a longer
one because every future word adds the same mask independently of the
past choice. At equal length the lexicographically first sorted subset
also dominates for the stated deterministic tie rule. This is valid
because words are processed in sorted order and are never revisited.
The full-mask state consequently has minimum cardinality among these
frozen candidate words, separately for each source.

The coverage readback checks at least one selected witness at every
input interface. The code performs no graph, neighbour, normalizer or
Hamilton operation. Its48 row memberships are the sum of per-source
minimum membership counts under the fixed candidate/pool data.
Its27 distinct words are a count of the chosen minima, not a globally
minimum distinct-word solution across source types. Different pools,
candidate sets or mathematical mechanisms are outside its optimality.

Verdict: all three mathematical implications and the inspected code
implementations are sound within these stated assumptions. This review
does not independently replay the finite counts, review the upcoming
full manuscript candidate, or establish a broader uniform theorem.
