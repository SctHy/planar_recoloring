# Four-center local family review and manuscript candidate

The local inequality is valid: for a legal vertex v in a target component H,
let d be its degree and let g count incident source-protected edges outside
the prescribed restored target pool. A Hamilton cycle of H uses two distinct
incident edges at v and can use at most d-g edges outside the desired set.
It therefore uses at least max(0,2+g-d) desired edges. The forbidden-colour
formula d=sum_i |B_i(v) minus {u_i}| follows directly from legal one-coordinate
recolouring. This proves a statement about every target Hamilton cycle under
the fixed pool premise, without a selected-cycle retention premise.

The independent reader reviewed all 60 existing local rows with direct
legality tests rather than the author's alternative-colour neighbour formula.
It imported no author code and ran no author generator. All rows, prescribed
first normalizers, target components and literal pool overlaps agree. The
inherited 30 rows agree with v2, whose JSON bytes also equal the saved copy.
The input and result hashes are in provenance.json and the frozen manifest.

The union has thirteen ordinary-target interfaces and one constant-component
interface. Nine ordinary cases have d=3,g=2, so the pair collectively forces
an edge without either edge being individually forced by degree two. Four
ordinary cases have d=2. For 00112 -> 30112 at v=13230, d=g=2, forcing both
13030--13230 and 13230--23230. The constant case is 00001 -> 00000, restored
component 1 containing 32132; the other component is not covered.

Three centers suffice for this union. The fourth center 12132 adds no
ordinary interface and gives a redundant constant-component certificate.
The original result describes four 'protected-degree2 centers': each has two
incident source-K edges, but the source graph degrees of 12132 and 13023
are three. The unambiguous candidate gives actual target-vertex degrees and
does not assert regularity of a target graph.

The raw-only ordinary cases remain explicit limits: for source 00001,
(j,q)=(1,3) has pool edge 12132--32132 and (3,1) has pool edge
32130--32132; for source 00112, (2,3) has pool edge 13030--13230.
These local arguments prove raw K intersection but do not prove safe K
intersection. Illegal witness vertices are inapplicable; a zero local bound
is inconclusive. Hard target types are excluded from nonvacuous whole-target
Hamilton-cycle conclusions. Common-port seeds are not whole-target cycles.
Nothing here proves or refutes safe intersection for the excluded cases,
arbitrary target pools, different opponent maps, or all 53 hard interfaces.

The separated full manuscript candidate replaces fourteen individual-record
proof premises with the local bound, leaving 269 necessary individual records
and six constant-source families covering 30 cases. All 283 literal
nonconstant-source records are retained. Every one of the 53 marked C5 literal
blocks, all 41 existing theorem/lemma/proposition/corollary statements and all
55 old labels are unchanged. The live manuscript was not edited.

The candidate compiles without warnings, and rendered pages 22 and 23 were
visually checked: the alternatives table, parameter table and adjoining proof
are legible, aligned and unclipped. However, its TeX grows by 2735 bytes and
its PDF grows from 42 to 43 pages. It reduces independent proof dependencies
but does not meet a shorter-manuscript goal under the current requirement to
retain all literal blocks. Recommendation: retain this as a reviewed research
candidate, and do not adopt it solely to simplify or shorten the main text.

The original v1 candidate remains byte-for-byte unchanged. A separate corrected
replacement and one-line diff change 'Each target has degree three' to
'Each specified target vertex has degree three'. This corrects the scope of
the degree statement without rewriting the historical artifact.

Python 3.14.6 supplied exact local finite readback. The mathematical argument
is stated above and in symbolic-family-candidate.tex; successful execution is
only evidence for its recorded finite premises. The computation-record
validator checks schema, file existence and hashes, not mathematical truth,
independent peer review, graph coverage or theorem completion.
