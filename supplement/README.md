# Finite certificates

`article_certificates.tex` / `.pdf` (12 pages) is the standalone certificate
supplement. Its marked data blocks are the only input to the exact readers below,
which need Python 3.10 or later and no third-party libraries.

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
| `verify_all.py` | All three readers, nine rejection tests (missing data, malformed cycles, invalid individual witnesses, a witness removed by a pool, altered selectors), and the read-only manifest check. |
| `certificate_core.py` | Parsing and exact graph helpers shared by the readers. |

Boundary digit `4` means a full list only in the pentagon data. State words use
`0,1,2,3`; in six-digit words the first digit is the path row. Edges are unordered
pairs. Normalization enumerates starts `0,...,4`, signs `+1,-1`, and colour
permutations in lexicographic order, taking the first listed standard type.
Individual interface edges are expressed in source coordinates; target vertices,
protected edges and pools are restored to those coordinates before comparison.
The 47 individual records, 236 selector cases and 30 constant-family cases must
partition all enumerated interfaces. Missing or duplicate records fail.

These checks concern the finite local lemmas and replay the \(23^2\) product
cycles plus their alternating reserve splices. Arbitrary-length bad-run
lifting, component-graph connectivity along an arbitrary bottom Hamilton path,
spanning-tree splicing, and the structural inductions are analytic proofs in
the article. General planar girth-five four-colour Hamiltonicity and
Hamilton-connectedness remain open in this manuscript. The computation is not
a formal proof-assistant verification of the whole article.
