# Finite certificates

`article_certificates.tex` / `.pdf` is the standalone certificate supplement.
Its marked data blocks, the literal shared-hub path arrays in `data/`, and
the seven degree-two arrays in `data/degree-two/` are
the inputs to the exact readers below, which need Python 3.10 or later and no
third-party libraries. The arrays are located relative to the reader, including
when a positional path selects another supplement source.

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
| `verify_all.py` | All six readers, agreement between both degree-two readers, and 31 rejection tests for missing or duplicate data, malformed cycles, invalid palette digits or word lengths, altered models or omitted aliases, inconsistent coverage counts, invalid individual witnesses, a witness removed by a pool and altered selectors, plus the read-only manifest check. |
| `certificate_core.py` | Parsing and exact graph helpers shared by the readers. |

Boundary digit `4` means a full list only in the pentagon data. State words use
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
restoration and eleven-pentagon structural induction are analytic. Exploratory
full-graph lift tests and obstruction searches are not certificate premises.

These checks concern the finite local lemmas and replay the \(23^2\) product
cycles plus their alternating reserve splices. Arbitrary-length bad-run
lifting, component-graph connectivity along an arbitrary bottom Hamilton path,
spanning-tree splicing, and the structural inductions are analytic proofs in
the article. General planar girth-five four-colour Hamiltonicity and
Hamilton-connectedness remain open in this manuscript. The computation is not
a formal proof-assistant verification of the whole article.
