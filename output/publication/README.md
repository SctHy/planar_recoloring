# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This package contains the revised 27-page article, its standalone 12-page finite-certificate supplement, the LaTeX sources, exact Python readers, and reproducibility reports. The revision addresses the referee's proof-completeness concerns while keeping the general girth-five four-colour frontier explicit.

The article now includes a legal four-colour interface construction for the subdivided-star lift, a parameterized bad-run invariant, explicit component-graph connectivity and protected-edge tree-splicing statements, a product-level protected-pentagon replay for all 23 x 23 component pairs, and a detailed subcubic face-count/dual-propagation argument. The theorem-like results use numbering without square-bracket titles; the four protected-pentagon local facts appear as Claims 1--4 with their internal labels preserved. The finite checks and the analytic induction steps are stated as separate parts of the evidence.

The repository article source/PDF and the copies at the package root are kept byte-identical; the standalone certificate source/PDF likewise match the copies under `supplement/`. The package also carries the exact readers, reports, computation record, and manifest used for the delivered ZIP.

From this directory, run:

    python3 supplement/verify_all.py --write-reports
    python3 supplement/verify_all.py --check-manifest
    pdflatex main.tex
    pdflatex main.tex
    cd supplement
    pdflatex article_certificates.tex
    pdflatex article_certificates.tex

The first command explicitly regenerates the finite verification reports. The
second command is read-only: it checks the manifest and every delivered file,
without rewriting reports or other package files. Running `verify_all.py`
without a flag remains an alias for `--write-reports`.

Python 3.10 or later and standard-library modules suffice for verification.
Report bytes are independent of the interpreter patch version, so their
manifest hashes are stable across supported Python versions. Compilation uses
pdfLaTeX with its default output location. Auxiliary files are generated beside
their sources and are excluded from the submission ZIP. The manifest check
covers every delivered file except `manifest.json` itself.

The exact replay has three positive suites and nine fail-closed negative cases. The protected-pentagon suite checks 23 component types, all 529 component products, 16,008 finite product blocks, 313 standard-source interfaces, and the hard two-row/three-row seeds. Arbitrary-length bad-run lifting, arbitrary-order component-graph connectivity, the analytic tree-splicing induction, and the structural inductions remain mathematical arguments in the article; the scripts do not claim to formalize them.

The general four-colour Hamiltonian and Hamilton-connected questions for planar graphs of girth at least five remain open, with the stated bounds `4 <= h(P5) <= 5` and `4 <= hc(P5) <= 5`. Author names, affiliations, contact details, and journal-specific declarations remain blank placeholders because no author metadata was supplied for this revision.

`REVISION_NOTES.md` records the changes in Chinese. `computation-record.json` records the current commands, scope, and hashes. Historical drafts and unadopted proof fragments remain outside this delivery package.
