# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This package contains the article (24 pages), its standalone finite-certificate
supplement (12 pages), their LaTeX sources, the exact Python readers, and reports.
The reference format is a conventional mathematical research article: main
statements and literature comparison in the introduction, followed by proof
strategy, the proofs, reproducibility information and references.

The concise revision extracts one shared endpoint-lifting lemma, combines the
adjacent-pair interface cases, removes repeated sharpness descriptions and
consolidates proof subdivisions. Endpoint words and nonconstant splice pools
use two columns. The article keeps its 11pt body and one-inch margins.

From this directory, run:

    python3 supplement/verify_all.py
    pdflatex planar_recoloring_hamilton_thresholds.tex
    pdflatex planar_recoloring_hamilton_thresholds.tex
    cd supplement
    pdflatex article_certificates.tex
    pdflatex article_certificates.tex

Python 3.10 or later suffices for verification; no third-party Python libraries
are used. Building uses pdfLaTeX directly with the listed standard TeX packages.
Run it twice for each document to resolve cross-references. PDFs and auxiliary
files are generated beside their sources; auxiliary files are omitted from the
submission ZIP. Native compilation was checked from this standalone directory
with TeX Live 2025. Existing finite-check reports from Python 3.14.6 are reused
because the certificate source and readers are unchanged. See supplement/README.md
for the data format and finite coverage, and supplement/reports/ for the reports.

The article's analytic inductions and splicing arguments are not formalized in a
proof assistant. The exact checks verify the local finite certificates described
in Section 7. The full planar girth-five four-colour Hamiltonian and
Hamilton-connected questions remain open in the article.

Fill in the actual authors, affiliations and contact details in both LaTeX
preambles before submitting. Adapt to the chosen journal's template and author
requirements. Independent review of the analytic proofs remains a submission
step. No acceptance or publication is claimed.

REVISION_NOTES.md describes the editorial changes in Chinese.
computation-record.json records the computation scope, implementation and hashes.
manifest.json hashes every delivered file except itself. Historical drafts and
unadopted proof fragments are not needed to rebuild or verify this package.
