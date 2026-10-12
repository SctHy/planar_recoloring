# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

The main article is `main.tex` / `.pdf`.
The standalone certificate supplement is `supplement/article_certificates.tex` / `.pdf`.
`output/publication/` contains the organized submission files, review reports, and file
hashes; `output/publication.zip` is the same bundle.

The Lean 4 formalization corresponding to the article proofs is in `formalization/`.
It fixes Lean 4.34.1 and checks, in the kernel, finite recolouring-graph and Hamilton
property definitions, recolouring and colour-permutation interfaces, the three-layer
bridge-colour lemma, strict splicing interfaces for arbitrary fibre chains and restored
vertices, cyclic bridge-colour selection, path-parity obstructions in binary products,
the permutation-parity obstruction for the six three-colour states of `K_2`, the
two-isolated-vertex two-colour obstruction, and the frozen cube four-colouring. Section
3 also provides relation-level `HamiltonPathOn`/`HamiltonCycleOn` certificates, restored-
vertex bridges, and the binary-product endpoint-parity interface. Chapter 4 now also
contains the arbitrary finite adjacent-pair reset with layer-tagged Hamilton paths.
It also checks the integer algebra of the five-face identity once the three planar
counting equations are supplied. Planar structural inductions, external lemmas, and the Appendix B--D certificates remain
pending formalization within the boundaries listed in `formalization/README.md`.

The current minor-revision manuscript has 27 article pages and a 12-page standalone
certificate supplement. The article retains 11pt type and one-inch margins; endpoint
constructions were factored into common lemmas, adjacent-pair interface arguments were
merged, and repeated counterexamples and threshold explanations were tightened. The
supplement uses two columns for endpoint paths and splice pools while preserving the
literal certificates. The introduction lists the three main theorems, states how they
relate to prior work and the proof route, moves the long certificates into a separately
compilable supplement, and retains explicit open problems. The article does not use old
proof fragments that failed review.

Main revisions:

- Rewrote the abstract and introduction; moved the threshold table earlier and added
  the bipartite and block-subcubic classes.
- Unified the fibre notation shared by the degenerate-graph proof and compressed
  repeated steps; completed the uniform optimality proof for `d+3` for
  Hamilton-connectedness and vertex-pancyclicity.
- Promoted the existing block-subcubic result to a formal theorem and explained that a
  cutvertex may have unbounded total degree.
- Corrected the description and checking scope for the three-element/four-element list
  change in adjacent-vertex restoration.
- Completed checks of protected pentagon edges, target-pool exclusions, two-layer and
  three-layer seeds, and all 313 interfaces.
- Used the three path cycles actually adopted in the article to verify every symmetric
  image and safe common edge.
- Replaced process-oriented research records with the final certificate contract and
  reproduction commands.
- Applied numbering-first result formatting, removed bracketed headings from the main
  article, and changed the four local protected-pentagon facts to Claims 1--4.
- Narrowed and centred the introduction's threshold table while retaining the complete
  class and threshold information.

The repository article and `output/publication/main.tex` / `.pdf` are kept in sync. The
standalone certificate and `output/publication/supplement/article_certificates.tex` /
`.pdf` are also kept in sync. The submission directory contains the same-version
checkers, reports, `computation-record.json`, and `manifest.json`; `output/publication.zip`
directly packages these delivered files without LaTeX auxiliary files or caches.
Author, affiliation, correspondence, funding, data, AI, and conflict-of-interest
statements have not yet been supplied; the current sources and submission bundle retain
empty placeholders to be filled with the actual information before submission.

Run the following from the current directory:

```sh
python3 supplement/verify_all.py --write-reports
python3 supplement/verify_all.py --check-manifest
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The first command explicitly generates finite-verification reports; running
`verify_all.py` without an option remains an alias for `--write-reports`. The second
command read-only checks `output/publication/manifest.json`, delivered-file sizes, and
SHA-256 values; it does not rewrite reports or other delivered files. Reports do not
contain interpreter patch versions, so their manifest hashes are stable on supported
Python 3.10+ environments. Verification uses only the standard library, and compilation
uses pdfLaTeX directly. Compile each document twice to resolve cross-references; PDFs and
compilation auxiliaries are generated beside their sources by default, and auxiliary
files are ignored by Git.
Certificate format, check coverage, and historical-file notes are in
[supplement/README.md](supplement/README.md).

The pre-edit manuscript and hash manifest are preserved in
`output/editorial/publication-revision-20261012-001822/original/` and its sibling
`original-manifest.json`. The historical 41-page full manuscript is unchanged.
The 26-page article, 14-page supplement, and complete bundle from before the current
simplification are also preserved in
`output/editorial/proof-layout-revision-20261012-005742/original/`, with the revision
diff and layout-check results stored alongside them.
