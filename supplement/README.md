# Finite certificates

`article_certificates.tex` / `.pdf` is the standalone certificate supplement.
Its marked data blocks and literal files in `data/` are the inputs to twelve
exact reader suites, which need Python 3.10 or later and no third-party
libraries. The files comprise two shared-hub path arrays, seven degree-two
arrays, three pentagonal-reservoir arrays, five extended-cycle arrays, and five
bowtie files. The latter ten files support the new connected-cycle and protected
bowtie lemmas. Data paths are resolved relative to the reader, including when a
positional path selects another supplement source. No solver output or earlier
computation report is an input.

From the article directory:

```sh
python3 supplement/verify_all.py --write-reports
python3 supplement/verify_all.py --check-manifest
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The first command runs all readers and writes `supplement/reports/`; without an
option `verify_all.py` does the same. The second command is a read-only check of
`output/publication/manifest.json` and every delivered file. `--report-dir PATH`
selects another report directory, a positional path checks another source, and
each reader accepts `--json PATH`. Reports do not record the Python patch version,
so their hashes are stable on Python 3.10+. Compile each document twice with
pdfLaTeX; auxiliary files stay beside the sources and are ignored by Git.

| File | Checked finite claim |
| --- | --- |
| `verify_adjacent_pairs.py` | Seven Hamilton-cycle edge orbits, all 53 endpoint words, exact endpoint feasibility by subset dynamic programming, all 225 labelled list pairs and 3,225 physical interfaces, including 1,200 changes between containing three- and four-element lists. |
| `verify_path232.py` | The three printed normalized cycles, their 72 distinct allowed images on 60 good boundaries, all 504 directed good-boundary transitions / 720 cycle pairs, and support at adjacent bad boundaries. |
| `verify_protected_pentagons.py` | Complete component coverage, first normalization and inverse maps, all 2,304 labelled boundaries, all 23 component types, path blocks and connectors, both hard two- and three-row seeds, all pools and common ports, the full 313-interface partition, all \(23^2\) product cycles with reserve splicing, and the relative-normalization rule on all labelled boundaries and admissible maps (75,120 overlapping cases; per-boundary canonical maps fail at 88 interfaces, including `00002 -> 00003`). |
| `verify_shared_hub_paths.py` | The five and fifteen literal templates in `data/path4-family.json` and `data/path5-family.json`, exact coverage of all 64 and 256 labelled fibres, and all 576 and 3,072 directed physical interfaces. A shared-hub change affects both endpoint lists simultaneously. Minimum intersections of the chosen cycle edge sets are three and five. |
| `verify_degree_two_families.py` | Seven fixed internal graphs, exclusion lists and complete possible port aliases; 421 normalized templates with 96,036 states, all 8,704 labelled boundaries and 158,976 directed singleton/double-port interfaces. At least two edges of the simultaneously selected cycles agree at every interface. |
| `verify_degree_two_interfaces.py` | Independent physical-label transport, cycle legality and direct packed-edge intersections at all 158,976 interfaces, without importing the primary family reader or using relative-normalization caching. Full legal-state and alias-distance coverage are the primary reader's obligations. |
| `verify_pentagonal_reservoirs.py` | Three fixed pentagonal models, exact legal-state components and component Hamilton cycles, complete port aliases (31 reservoir matchings), all 486,912 directed boundary interfaces and 490,176 overlapping component pairs, with bilateral non-killability and shared-edge capacities four or two. |
| `verify_pentagonal_reservoir_interfaces.py` | Independent recursive state construction, packed-state component coverage and physical-label replay of all pentagonal interfaces and their complete shared-edge histograms, without importing the primary reader or using relative-colour caching. |
| `verify_extended_cycles.py` | Five fixed connected-cycle models, complete legal-state and alias coverage, 771 normalized templates with 2,491,162 states, all 75,008 labelled boundaries and 2,577,024 directed physical interfaces, each with at least two common chosen-cycle edges. |
| `verify_extended_cycle_interfaces.py` | Independent fixed models, legal-state coverage and physical-string transport for all extended-cycle interfaces, with complete overlap histograms and digests; no import of the primary reader or input from its report. |
| `verify_bowtie_families.py` | 558 bowtie fibre types with 845,440 states, 1,116 complete `K2`/`K3` seed cycles with 4,227,200 seed states, rowwise matching protection, all 2,251,776 directed factor interfaces, clique partitions and quotient trees of physical capacity two, and the ordinary-pentagon seed extract bound to the current marked data. |
| `verify_bowtie_interfaces.py` | Independent bowtie graph and seed reconstruction and physical-label replay of all full-matching and protected-core interfaces, reproducing their complete histograms and digests without importing the primary reader or reading its report. Clique trees and the ordinary seed extract are checked by the primary reader. |
| `verify_all.py` | All twelve readers, agreement between four primary/independent pairs, and rejection tests for missing or duplicate records, malformed cycles, invalid raw states or indices, altered models or omitted aliases, wrong input identities, inconsistent counts, invalid interface witnesses, failed protection and altered selectors, plus the read-only manifest check. |
| `certificate_core.py` | Parsing and exact graph helpers shared by the readers. |
| `bowtie_core.py` | Fixed bowtie models, strict literal schemas and primary-reader helpers; the independent bowtie reader defines its models separately. |

In Appendices C--D, boundary digit `4` denotes a full list. State words use
`0,1,2,3`; in the protected-pentagon seeds, six-digit words start with the path row. Edges are unordered
pairs. For the pentagon data, normalization enumerates starts `0,...,4`, signs `+1,-1`, and colour
permutations in lexicographic order, taking the first listed standard type.
Individual interface edges are expressed in source coordinates; target vertices,
protected edges and pools are restored to those coordinates before comparison.
The 47 individual records, 236 selector cases and 30 constant-family cases must
partition all enumerated interfaces. Missing or duplicate records fail.

For the shared-hub arrays, a boundary `(a,b_1,...,b_(r-2))` excludes
`(a,b_1,...,b_(r-2),a)` on the path. Palette normalization uses first appearances,
then unused colours in ascending order; its inverse restores every physical
boundary before interface comparison. There are no spatial symmetries or
independently chosen relative maps. Raw digits are validated before indexing.
`shared-hub-paths.json` records both input-file hashes and the finite coverage
in Appendix E; the unbounded restoration and structural induction are analytic.

Appendix F specifies the seven additional models. Their fixed file/kind
identities are `star3`, `path4heavy`, `path5heavynear`, `path5heavycenter`,
`path6`, `tailed5` and `tailed6`. Both readers enforce these identities and
validate raw integer digits and word lengths before palette indexing. Their
reports `degree-two-families.json` and `degree-two-interfaces.json` record
the input byte counts and SHA-256 hashes. Each selects cycles by the same
first-appearance convention. A repeated endpoint port is one physical move;
the additional possible alias pairs are checked as simultaneous moves with
equal old boundary entries. Several disjoint aliases need no further move
type, and the compatibility graphs admit no triple alias. The arbitrary-order
restoration and structural inductions are analytic. Exploratory
full-graph lift tests and obstruction searches are not certificate premises.

Appendix G gives the three pentagonal models and their fixed filename/kind
contracts. The reservoir fibre is disconnected exactly when the first five
boundary entries agree: the arrays give one Hamilton cycle for each component,
with exact component coverage checked by both readers. At every overlapping
component pair there are at least four common selected-cycle edges; every
component on either side has an overlapping component on the other side.
Shared moves involving either of the two degree-two ports are included. The
full-list and pendant families have connected fibres and require only two
common edges (their observed minima are eleven and eight). Unchanged boundaries
use identical cycles whose lengths also meet these capacities. These data
contain 781 boundary templates, 786 component cycles and 101,121 states.
`pentagonal-reservoirs.json` and `pentagonal-reservoir-interfaces.json` bind the
three literal file hashes. The earlier nine JSON inputs are retained separately;
the redundant alternating-hexagon witness is not a proof dependency.

Appendix H specifies the five compressed arrays in `data/extended-cycles/`:
`sharededge`, `sharededgechord`, `threecontactpath7`, `onelinkpentagons` and
`twolinkpentagons`, each with suffix `.json.gz`. The first two models consist
of pentagons sharing an edge, with an optional chord; the last two join disjoint
pentagons by one or two edges. In the path model, one retained hub changes three
local lists simultaneously. Both readers enforce the fixed graphs, exclusions,
raw schemas and file/kind identities, validate raw integers before indexing,
check complete cycle coverage and restore physical coordinates. The linked
models use eight and four spatial symmetries in addition to palette
normalization. Their complete alias matchings number 22, 4, 5, 209 and 34; no
three roles can coincide. Both readers enumerate every singleton and allowed
shared-role move, with cached repeated transports, and reproduce the full
overlap histograms and digests. Their observed intersection minima are 56, 94,
10, 219 and 390; only a margin of two is needed in the analytic splice.
`extended-cycles.json` and `extended-cycle-interfaces.json` bind the compressed
input byte counts and SHA-256 hashes.

Appendix I uses `bowseed` and `bowchord` in `data/bowties/`. For each kind,
`-seeds.json.gz` gives cycles of the fibre product with `K2` and `K3`, using
complete clique row adjacency; `-clique-trees.json.gz` partitions every fibre
into edges and triangles and gives a tree of connecting edges. At most two
connectors meet any physical fibre vertex. These are clique blocks: a
three-vertex path does not satisfy the triangle contract. Every seed retains
the full listed matching in every physical row; two matching edges are
reserves and the remainder is the protected core. The bare and chorded models
have 451 and 107 boundary types and 65,536 and 4,096 labelled boundaries.
Their full-matching overlap minima are 9 and 25, and their core minima after
removing the two reserves are 9 and 24. Both readers check all admissible
singleton and shared-role moves and reproduce both overlap histograms and
digests. The primary reader also checks all 422,601 clique blocks, including
238 triangles, and 422,043 tree connectors.

The fifth bowtie file, `ordinary-pentagon-seeds.json`, extracts twelve ordinary
components with 590 states and 24 two- and three-row seeds from eleven boundary
types in Appendices C--D. Its literal cycles, pools, protected sets, reserves
and hard seeds are checked against the current marked blocks. The old `P3`
seeds also give `K3` seeds, since every path edge is a clique edge; these
ordinary protected sets need not be matchings. `bowtie-families.json` binds all
five input hashes; `bowtie-interfaces.json` independently binds both seed-array
hashes. The generalized clique products, combined interfaces of distinct
factors and unbounded lifting are analytic arguments.

All seven source research archives were replayed during integration review.
The adopted certificates use the files listed here; the archived four-contact
ten-vertex path and the older 2,982 path-block trees are not proof dependencies.

These checks concern the finite local lemmas and replay the \(23^2\) product
cycles plus their alternating reserve splices. Arbitrary-length bad-run
lifting, component-graph connectivity along an arbitrary bottom Hamilton path,
spanning-tree splicing, and the structural inductions are analytic proofs in
the article. General planar girth-five four-colour Hamiltonicity and
Hamilton-connectedness remain open in this manuscript. The computation is not
a formal proof-assistant verification of the whole article.
