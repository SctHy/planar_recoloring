# Finite certificates

The submission supplement is `article_certificates.tex` / `article_certificates.pdf`.
Its literal data are the input to the following exact readers. They require
Python 3.10 or later and no third-party libraries.
The current PDF has 12 pages. Endpoint words and nonconstant splice pools
are arranged in two columns; all 55 marked blocks and all 53 endpoint words
are identical to the preceding standalone revision. The 53 historical
marked blocks remain unchanged.

From the article directory:

```sh
python3 supplement/verify_all.py --write-reports
python3 supplement/verify_all.py --check-manifest
pdflatex planar_recoloring_hamilton_thresholds.tex
pdflatex planar_recoloring_hamilton_thresholds.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The first command explicitly runs the finite readers and writes
`supplement/reports/`. The no-argument command remains an alias for
`--write-reports` for compatibility. The second command is a read-only check
of `output/publication/manifest.json` and every delivered file; it does not
rewrite reports or any package file. In a standalone publication directory,
run the same two commands from the package root after regenerating its
manifest and ZIP.

Compilation uses pdfLaTeX directly with its default output location. Run it twice
for each document to resolve cross-references; PDFs and auxiliary files remain
beside their sources. Auxiliary files are ignored by Git and omitted from the
submission ZIP.

Reports contain only Python-version-independent certificate results, so their
manifest hashes are stable across supported Python 3.10+ interpreters. A
different destination can be selected with `--report-dir PATH`. To check a
different source, pass its path as the first positional argument. Individual
readers accept `--json PATH`.

| Reader | Verified finite claim |
| --- | --- |
| `verify_adjacent_pairs.py` | Seven Hamilton-cycle edge orbits, all 53 endpoint words, exact endpoint feasibility by subset dynamic programming, all 225 labelled list pairs and 3,225 physical interfaces, including 1,200 changes between containing three- and four-element lists. |
| `verify_path232.py` | The three printed normalized cycles, their 72 distinct allowed images on 60 good boundaries, all 504 directed good-boundary transitions / 720 cycle pairs, and support at adjacent bad boundaries. |
| `verify_pentagon.py` | Entry point for `verify_protected_pentagons.py`: complete component coverage, first normalization and inverse maps, all 2,304 labelled boundaries, all 23 component types, path blocks and connectors, both hard two- and three-row seeds, all pools and common ports, the full 313-interface partition, and all \(23^2\) product cycles with reserve splicing. |
| `verify_all.py` | All three readers and nine rejection tests covering missing data, malformed cycles, invalid individual witnesses, a witness removed by a pool, and altered selectors. |

`certificate_core.py` supplies parsing and exact graph helpers.
`check_adjacent_pair_cycles.py` remains a compatibility entry point to the full
adjacent-pair reader.

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
lifting, component-graph connectivity over an arbitrary bottom Hamilton cycle,
spanning-tree splicing, and the structural inductions are analytic proofs in
the article. General planar girth-five four-colour Hamiltonicity and
Hamilton-connectedness remain open in this manuscript. The computation is not
a formal proof-assistant verification of the whole article.

## Historical files in the workspace

`planar_recoloring_hamilton_thresholds_full.tex` and its PDF are the preserved
41-page historical version. All 53 marked data blocks in its appendices were
copied byte for byte into the standalone supplement. The old structural path
checker, rook checker and proposed TeX fragments remain available as research
history. They are excluded from the submission bundle and are not additional
proof inputs. In particular, the proposed path fragment has a parameter typo,
and the proposed compact protected-pentagon fragment lacks a target-pool condition.
