# Independent analytic review: complete table-free safe-edge proof PASS

Reviewed frozen full candidate-v1 SHA256
`0abf152168c79ac5d629adfee3ce5e0b4bd9d857648bfab209d0007c46be3450`
and compact candidate-v2 SHA256
`20d7b4914f5632fac3aac03f84fd4f6d66a310a155b0856748a9334d60e7683b`.
The main manuscript was not edited. No Hamilton search was performed.

The general count is correct. If U is nonempty, a proper outside subset of
a simple cycle induces disjoint paths in that cycle; deleting q such paths
leaves exactly |U|-q edges with both ends in U. An empty outside set gives
q=0 and leaves |U| edges. If F is the common forbidden set, each cycle has
at least |U|-q-|F| safe internal edges. If R is disjoint from F and omitted
by both cycles, their common available universe has at most
|E(H)|-|F|-|R| edges. Inclusion-exclusion gives exactly the printed bound.
H need not equal the induced common graph, but it must contain every
internal edge of either cycle, as both candidate versions require. No
outside-path statement concerns the entire fibre's induced subgraph.

The classification preserves all quantifiers. Normalize an end-change
source to aab. Changing its first, middle or last boundary coordinate gives
the five equal-or-higher good families bab/cab, abb/acb, and aac; the
remaining repeated-colour target is bad. At aba, changing the middle
coordinate gives aca, changing an end to an unused colour gives cba up to
reversal, and the other good end change has lower E type. At abc, the only
equal-type families are an end change to the fourth colour (abd up to
reversal) and a middle change to that colour (adc). Other changes have E
or M type and have already been oriented from their lower-type side.
Interchanging the two unused colours gives the other representatives
without changing the selected E or either M edge set. Thus there are nine
families, with no omitted boundary transition.

The selected E cycle is fixed by the unused-colour swap. The selected M
cycle is also fixed by that swap, and reversal gives its second allowed
edge set. The selected A cycle is fixed by reversal followed by interchange
of its endpoint boundary colours. These are exactly the stabilizers of
the boundary patterns: a fixed E or A boundary has one allowed edge set;
a fixed M boundary has two. This does not assert uniqueness among all
Hamilton cycles of a fibre. The independent reader directly enumerated
all colour images and reversals of the three supplied cyclic words at
each fixed canonical boundary and confirmed counts1/2/1.

All twelve full literal deletion profiles contain every state of their
coordinate class exactly once and exactly its edges in the chosen cycle.
The compact version lists the same path orders. Their applications are:

| Family | Source outside class | Target outside class | Outside-path sum |
| --- | --- | --- | ---: |
| aab→aac | singleton-end unused colour c | singleton-end unused colour b | 2 |
| aab→acb | middle unused colour c | middle root-end colour a | 2 |
| aab→cab | repeated-end unused colour c | end middle-boundary colour a | 4 |
| abc→abd | end unused colour d | end unused colour c | 4 |
| aab→bab | source first coordinate b | target first coordinate a | 5 for M0, 4 for M1 |
| aba→cba | source first coordinate c | target first coordinate a | 4 for either M orientation |

The fixed-middle layers and inter-grid counts in the candidate give the
exact six pairs (n,m)=(10,13),(10,15),(9,11),(11,17),(10,15),(12,21).
This can be seen from the two allowed endpoint-colour lists at each middle
colour: each nonempty layer is a Cartesian product of complete graphs of
orders1,2 or3. Forbidding the displayed E special edges gives respectively
f=2,1,1,0,0,0. These are not empirical minimum counts over arbitrary cycles.

The three positive omitted-edge corrections are valid for every selected
orientation. For abc→abd, each middle-a path starts at bab by changing its
last coordinate to its respective unused colour, so both omit bab--cab
and bab--dab. These are two common nonforbidden edges.

For aab→bab, the common middle-b prism has one triangle at first colour c
and another at first colour d. E retains exactly one edge in each triangle.
The M0 target retains two edges in each triangle and contains that E edge;
their union therefore uses only two edges. M1 retains one edge in each
triangle, so its union with the one E edge uses at most two. In both cases
each triangle supplies an edge omitted by both cycles, and the triangles
are disjoint. This proves |R|≥2 without choosing a target orientation.

For aba→cba, both M orientations have no internal middle-a edge at bab.
The A(cba) middle-a path begins bab,dab, and hence omits bab--bac and
bab--bad. Every edge changing the middle coordinate in either selected
family has the excluded middle-boundary colour b in one endpoint
coordinate. The common edge dad--dcd has neither endpoint coordinate b,
so it too is omitted by both. The three edges are distinct and f=0.
This proves |R|≥3. Together the six deletion bounds are3,2,2,3,2,2;
the M1 end-to-middle case actually has the stronger bound3.

The remaining three support arguments are also complete. For aab→abb,
the common middle-c square has opposite corners bca,dcd. Both cycles
retain bca--bcd and bca--dca. The source's special edge at dcd is absent
from the target, and the target's special edge there is absent from the
source, so these two common edges are safe. For abc→adc, swapping b and d
preserves the common hexagon(bab,bad,cad,dad,dab,cab,bab); each cycle
uses five of its six edges and their intersection has at least four.
For aba→aca, every selected M orientation keeps three of the four edges
of the shared square Qd, giving at least two common edges. The last two
families have empty special sets.

The independent exact checker reads the12 literal paths and six-row count
table from the frozen candidate itself, generates only the three selected
cyclic words and their allowed canonical images, and checks14 canonical
cycle pairs:8 deletion-count pairs and6 support pairs. It imports no peer
edge, cycle, normalization, DFS or Hamilton-search helpers. All graph,
forbidden-set, omitted-edge, profile and support statements pass. Colour
permutations and path reversal preserve legal state graphs and the
definition of special edges, so the analytic equivariance argument covers
all labelled images; a further full image sweep is unnecessary.

Compact version-v2 faithfully transcribes the mathematics. A small wording
clarification is advisable: after its outside-path phrase add “in their
respective cycles”, and describe coordinate classes as inducing paths
“in the selected cycle”. Without this, a reader could momentarily read
“induce” as referring to the whole fibre. The surrounding text already
identifies the cyclic words, so this is editorial clarification, not a
mathematical gap. Frozen v1/v2 were not changed.

Conclusion: all nine families guarantee at least two safe common edges for
every pair of the originally allowed selected cycles. The safe-interface
table and target normalization/orbit conventions can be removed. The
three normalized cycle words and the square-support properties are still
needed; the proof makes no claim for arbitrary Hamilton cycles.
