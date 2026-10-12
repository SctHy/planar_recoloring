# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

The main article is `planar_recoloring_hamilton_thresholds.tex` / `.pdf`;
the standalone certificate supplement is `supplement/article_certificates.tex` / `.pdf`.
`output/publication/` contains the organized submission files, review reports, and file hashes;
`output/publication.zip` is the same package.

This revision follows the common narrative structure used by [OpenAI math manuscripts](https://github.com/openai/math):
the introduction lists the three main theorems, positions the relation to prior work and the strengthening in this paper,
explains the proof route, moves the long certificates to a separately compilable supplement, and retains explicit open questions.
The article does not use old proof fragments that failed review.

Main revisions:

- Rewrote the abstract and introduction; moved the threshold table earlier and added the bipartite and block-subcubic classes.
- Unified the fibre notation shared by the degenerate-graph proofs and compressed repeated steps; completed the unified optimality proof for `d+3` for Hamilton-connectedness and vertex-pancyclicity.
- Promoted the existing block-subcubic result to a formal theorem and explained that the total cutvertex degree can be unbounded.
- Corrected the description and verification scope of the three-element/four-element list changes in adjacent-vertex restoration.
- Completed the checks for protected pentagon edges, target-pool avoidance, two-row/three-row seeds, and all 313 interfaces.
- Used the three path cycles actually adopted in the article to verify all symmetric images and safe common edges.
- Replaced process-oriented research notes with the final certificate contract and reproduction commands.

Run from this directory:

```sh
python3 supplement/verify_all.py
python3 build.py
```

Verification requires Python 3.10 or later; compilation requires `latexmk` and pdfLaTeX.
The Python code uses only the standard library. Compilation intermediates are placed in `.latex-build/`.
Certificate format, check coverage, and historical-file notes are described in
[supplement/README.md](supplement/README.md).

Before submission, enter the actual author, affiliation, and contact information, and handle author declarations,
AI-use disclosure, and the template required by the target journal. The current artifact is a research manuscript
with editorial work and finite-certificate review completed; the complete analytic proof still requires independent peer review.
The general planar girth-five four-colour case is not presented as a solved theorem.

The pre-revision manuscript and hash manifest are preserved in
`output/editorial/publication-revision-20261012-001822/original/` and its sibling `original-manifest.json`.
The historical 41-page full version remains unchanged.
