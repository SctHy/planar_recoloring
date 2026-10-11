# Aggregate degree-capacity review and v2 exact calculation

The v1 conditional proof is correct. At a common vertex, the two source
Hamilton-cycle incidences lose at most outside and common-pool incidences.
The target Hamilton cycle selects two of its full graph degree d_t incidences.
Summing the resulting 4-d_t-minus-loss lower bounds and dividing by two is
valid even when some local lower bounds are negative. Both Hamilton cycles
must span their stated full components. The common-endpoint recolouring edge
sets must coincide. Hard common-port seeds do not satisfy these hypotheses.

The v1 script uses the C1/FHC blocks as unordered state sets, not as cycle
edges. It reads source/target case identities, boundary edit, group and
normalizer from the saved interface input, never its selected-basis edge
counts. Imported root_set_functions exports edge/restore/endpoints; its
main function is guarded and not executed. Therefore neither the v1 nor v2
bound consumes selected C/D edges, a cycle intersection or retention count.
The complete-state premise is inherited from the earlier source-bound
313-case reader, whose code explicitly compared the printed component words
with all legal fibres. V2 rechecks its source and code identities rather than
replaying that earlier full check. This is citation-based input assurance.

For a single boundary edit a common state has at most one source neighbour
outside the target, and an outside source state has at most two neighbours
in the common set. Consequently v1's min(2|O|, graph cut) always equals its
graph cut. Its margin is the sum of the node quantities
L(v)=4-d_s(v)-d_t(v)+d_c(v)-f(v) over its chosen S. Selecting all L(v)>0
already removes the negative contributions. Equivalently, select all
r(v)=4-d_t(v)-f(v)>0: the added outside cost is at most one, so this
selector maximizes the new capacity objective too. Positive r automatically
has d_t<=3. This proves optimization without flow or subset search.

The node computation's 51 omitted common vertices do not hide additional
positive L vertices: an omitted vertex has both edges of its printed source
cycle in the source pool. Each such incidence is either outside-common or
in the common pool union, so d_s-d_c+f>=2. Since d_t>=2, L<=0. V2 also
computes its bounds on all printed common states and compares case identities
with the saved 125 result, independently confirming the equality.

V2 defines J from source graph edges inside O that have a full-source-degree
two endpoint. Every source Hamilton cycle contains J. At outside vertex w,
the remaining cross-edge capacity is 2-d_J(w). The strengthened loss bound
is the sum over O of min(number of S neighbours, remaining capacity), plus
the common-pool incidences at S. The conditional proof and optimal-selector
proof are given in analytic-capacity-candidate.tex.

The exact calculation on 230 interfaces gives:

| Bound | Positive interfaces | Largest guaranteed edge count |
| --- | ---: | ---: |
| v1 all-low-degree selector | 97 | 5 |
| Optimized original graph-cut selector | 125 | 6 |
| Forced internal-O edge capacities | 125 | 6 |

There are no new covered interfaces beyond the 125 node cases. Two already
covered interfaces improve their guaranteed count from one to two:
00123 position2->3 and position4->1, each normalizing to 00121.
In each, outside vertex 31301 has forced edges to 21301 and 32301,
so its outside-to-S capacity is zero. Its one possible S incidence is
therefore eliminated from the loss bound. The margin grows from two to
three, yielding ceil(3/2)=2. The old 00101 position0->1 example still has
margin zero and bound zero; there is no collision with the earlier
selected-cycle three-common-edge counterexample.

All six original v1 input/code/proof/result hashes were checked before and
after execution, and remain unchanged. Python 3.14.6 completed 249540 exact
one-coordinate candidate tests. V2 only generated local legal neighbours
from supplied printed states, with no palette^5 state enumeration, Hamilton
search, selected-cycle edge intersection or explicit whole-state graph.
The mathematical theorem is the conditional capacity inequality; the 230
positive-count results are finite input evidence. This does not settle
arbitrary interfaces, arbitrary pools, hard-source/target whole-HC cases,
or any unresolved girth-five Hamiltonicity theorem. No manuscript edit was
made. The computation-record validator checks schema and hashes only.
