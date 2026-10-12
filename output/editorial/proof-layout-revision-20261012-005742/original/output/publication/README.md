# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This package contains the article (26 pages), its standalone finite-certificate
supplement (14 pages), their LaTeX sources, the exact Python readers, and reports.
The reference format is a conventional mathematical research article: main
statements and literature comparison in the introduction, followed by proof
strategy, the proofs, reproducibility information and references.

From this directory, run:

    python3 supplement/verify_all.py
    python3 build.py

Python 3.10 or later suffices for verification; no third-party Python libraries
are used. Building requires latexmk and pdfLaTeX with the listed standard TeX
packages. Intermediate files go in .latex-build/. PDFs remain beside their sources.
The commands were checked from this standalone directory on Python 3.14.6 and
TeX Live 2025 / latexmk 4.87. See supplement/README.md for the data format and
finite coverage. Existing reports are in supplement/reports/.

The article's analytic inductions and splicing arguments are not formalized in a
proof assistant. The exact checks verify the local finite certificates described
in Section 7. The full planar girth-five four-colour Hamiltonian and
Hamilton-connected questions remain open in the article.

Fill in the actual authors, affiliations and contact details in both LaTeX
preambles before submitting. Adapt to the chosen journal's template and author
requirements. Independent review of the analytic proofs remains a submission
step. No acceptance or publication is claimed.

REVISION_NOTES.md describes the editorial changes in English.
computation-record.json records the computation scope, implementation and hashes.
manifest.json hashes every delivered file except itself. Historical drafts and
unadopted proof fragments are not needed to rebuild or verify this package.
