# Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs

This package contains the revised 50-page article, its 18-page finite-certificate
supplement, sources, exact Python readers and reproducibility reports. For
nonempty finite simple planar graphs of girth at least five, the article proves
Hamiltonicity for every k >= 4 in each of these classes:

- At most 33 distinct 5-cycles (Theorems 1.3 and 5.50).
- Total degree excess D(G) <= 10 (Theorems 1.3 and 5.48).
- At most seven heavy vertices, with unrestricted degrees (Theorem 5.49).
- Two-degenerate with D(G) <= 13 (Corollary 5.51).
- Every block subcubic (Theorem 5.41).

Here D(G) = sum_v max(deg_G(v)-3,0); a heavy vertex has degree at least four.
Every stated class has uniform Hamiltonian threshold four and Hamilton-connected
threshold in [4,5]. The former two-degenerate 33-cycle alternative is subsumed
by the full 33-cycle theorem. Corollary 5.3 retains the two-degeneracy conclusion
under eleven distinct 5-cycles.

The latest revision adds an analytic equality ledger and rigidity argument at
D=10. It introduces no colouring-cycle data or certificate reader. The original
33 archive's three geometry/algebra/rejection readers and manifest pass read-only,
with all 56 source files unchanged. They check nonexhaustive spherical fixtures,
loss identities and bounded cases, not the universal analytic proof. Its proposed
two-degenerate 37-cycle/D15 bounds depend on an undelivered four-contact P10
restoration and are not adopted. Exact replay and scope details are in
supplement/reports/data-provenance.json.

The fourteen publication suites and 132 actual-reader rejection cases are
retained. The 24 literal inputs and all 61 marked blocks are unchanged, as are
the sixteen finite reports after replay. The readers certify complete finite
states/components, selected cycles and seeds, protection, physical aliases and
interfaces, and clique trees. Appendices A-J document their contracts. Ordinary
restoration maps propagate relative to the preceding bottom colouring.
Arbitrary-order products, lifting, splicing, the structural inductions and the
new equality rigidity remain analytic arguments.

Earlier archive replay records and the completed 31-archive replay remain in
the provenance. Incomplete inherited replay attempts in the 33 continuation
are recorded separately from completed checks. No duplicate ordinary/bowtie
data, order-ten path or older path-partition arrays are delivered.

Root and standalone sources and PDFs are byte-identical. From this directory:

    python3 supplement/verify_all.py --write-reports
    python3 supplement/verify_all.py --check-manifest
    pdflatex main.tex
    pdflatex main.tex
    cd supplement
    pdflatex article_certificates.tex
    pdflatex article_certificates.tex

Python 3.10+ and its standard library suffice. The first command regenerates
reports; the manifest command is read-only. The ZIP has exactly the 71 manifest
files and manifest.json, with no top-level folder or build auxiliaries.

The unrestricted thresholds remain 4 <= h(P5) <= 5 and 4 <= hc(P5) <= 5.
A vertex-minimal four-colour Hamiltonian counterexample has at least 34 distinct
5-cycles, eight heavy vertices and D>=11. A degree-two vertex requires 34 cycles
and D>=14; if unique, 42 and 16. Remark 6.1 describes necessary D=11 conditions
only for minimum degree at least three and at most 35 distinct cycles. It does
not exclude that regime or degree-two cases with 34/35 cycles. Author metadata
and journal-specific declarations remain placeholders.

REVISION_NOTES.md records the history. computation-record.json records the
commands, finite scope and artifact hashes.
