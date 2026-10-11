# Protected-pentagon interface simplification attempt

The two requested shortcuts do not replace the current 313 identities.
This conclusion applies to the current fixed cycles, seeds, pools, K sets,
and normalization convention; it does not rule out other analytic methods
or redesigned certificates.

## Exact computation scope

The 23 component state sets were generated directly from their fixed C5
lists (at most 4^5 candidate words per boundary). Their legal one-coordinate
edges and degrees were generated without Hamilton search. Current cyclic
words, two/three-row seeds, common internal seed edges, pools and 313
interfaces were read from a frozen copy of the manuscript's literal
blocks. Every printed interface witness was checked in the exact common-K
intersection after the prescribed target restoration.

The scope is a fixed finite local certificate. Python 3.14.3 standard-library
sets, permutations and exact integer words were used. The script is
`check_interfaces.py`; frozen input, provenance and results are adjacent.

## Low-degree/forced-edge attempt

| Property | Interfaces |
| --- | ---: |
| All interfaces checked | 313 |
| A common state has degree <=2 in both components | 89 |
| An incident edge is legal on both sides | 89 |
| Such an edge remains in both current K sets | 61 |
| Both sides have specified Hamilton component cycles | 230 |
| Both Hamilton sides have a common degree-two forced edge | 29 |
| The forced edge also remains protected on both sides | 26 |

Allowing the forcing endpoint to be different on the two sides gives the
same last two counts (29 and 26), so that broader elementary rule does not
cover more interfaces.

A Hamilton/Hamilton failure is source `00011:0`, position 1 changed to
excluded colour 1, with target `00101:0`. It has 32 common states, 54
common legal edges, and 16 common protected edges, but no common
degree-two forced edge. Its printed protected witness is
`12103--12123`. Thus the actual common protected edge exists, while the
proposed low-degree certificate does not.

A pool failure is source `00011:0`, position 3 changed to excluded colour
2, with target `00012:0`. Its sole dual-degree-two state is `21303`, and
its sole common forced edge is `21203--21303`. That edge is in the source
pool, so it is not protected. There remain 11 different common K edges;
the printed witness is `12102--32102`.

A hard-component failure is source `00001:0`, position 0 changed to
excluded colour 2, target `00012:0`: it has 31 common states and two
common K edges, but no dual-low-degree state at all.

### Why original component degrees do not force common seed edges

In a Hamiltonian component, degree two forces both incident edges in any
Hamilton cycle. This rule is valid only for a cycle of that component.
Hard components instead use cycles of A square P2 and A square P3. An
original degree-two state has product degree three at an end row and four
at a middle row, so its original edges need not be forced.

There is an even stronger obstruction at an original leaf w. In
A square P3, both end-row copies of w have degree two and force their
vertical edges into the middle copy. The middle copy then already has
two forced vertical edges, so its original internal edge is excluded
from every Hamilton cycle. Therefore an edge incident with an original
leaf cannot be a common internal edge retained in every P3 seed row.
The presence of low-degree states in a hard component does not certify
the required all-row common edge.

## Natural stabilizer attempt

For each source, enumerate the 240 transformations D5 times S4. Retain
only transformations preserving its labelled boundary, its actual
component state set, and its current protected edge set K.

Every one of the 23 such source stabilizers is trivial. Consequently all
313 complete interfaces are singleton orbits under these stabilizers.
There is no available symmetry reduction that keeps the current source
objects and K definitions intact.

The diagnostic count 312 in the JSON ignores target-component identity
and merges the two constant target components for one source parameter.
It is not a valid reduction. The valid full-interface orbit count is 313.

Even a nontrivial source stabilizer would not suffice by itself: transport
of a printed witness also requires equivariance of the chosen restored
target K under canonical normalization. Boundary/component symmetry alone
does not imply symmetry of arbitrarily chosen cycles, pools or K sets.

## What remains established

The script independently verifies that all 313 current witnesses are
present in both actual protected sets. The failures concern the two
proposed replacements, not the existing interface lemma. In particular,
common-state counts were never used to infer common-cycle-edge counts.
No main-manuscript changes or formal MRS updates were made.
