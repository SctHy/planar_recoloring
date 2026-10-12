# Simplified revision notes

The article has 24 pages and the standalone certificate supplement has 12 pages; before simplification they had 26 and 14 pages, respectively.
The article retains 11pt type and one-inch margins.

Proof simplification:

- New Lemma 2.4 unifies the endpoint lift for a single vertex. Its assumptions explicitly require a Hamilton-connected base graph,
  a non-neighbour, and a base-graph move preserving each available colour. The same-fibre endpoint path construction is proved once.
- The Hamilton-connected proof for degenerate graphs is reduced to induction, the complete-graph case, and colour-preserving moves.
  The state-degree criterion is checked only for the final assumption of the common lemma in Lemma 3.6.
- The three adjacent-pair interface cases are handled uniformly with the common list intersection `A ∩ A'`; the change remains confined to one list.
- Repeated Hamiltonian corollaries, the closing counterexample list, and the displayed thresholds were removed; the concrete lower-bound proofs remain in the corresponding theorems.
- Section 5 was reduced from eleven subsections to six, with paragraph headings guiding the internal steps.

Layout cleanup:

- The 53 endpoint paths are grouped by type in two columns, with each type kept in one column.
- Nonconstant splice pools use two columns; longer constant pools remain full width.
- The supplement's introductory text was compressed, unnecessary forced page breaks were removed, and the complete bibliography was placed on the final article page.
- Both PDFs compiled without warnings, undefined references, or overfull/underfull boxes.
  All 36 pages received text-boundary and page-overview checks; key two-column pages received an additional review.

Mathematical boundary:

A pentagon may have two C15 components. Restoration must retain the protected edges, avoid the source and target pools,
and use at least ten common edges to compensate for edges removed during spanning-tree splicing.
These conditions and their full argument remain in place.
The local existence of cycles has not been substituted for a proof of restoration for arbitrary lengths; the general girth-five four-colour problem remains open.
A substantially shorter treatment requires a new structural argument.

Certificates:

The 53 marked data blocks in the original 41-page full manuscript remain byte-identical; all 55 marked data blocks
and 53 endpoint paths in the preceding standalone supplement are also identical.
The checker code was not changed.
Three exact finite check suites and nine invalid-input rejection tests passed, including all 313 pentagon interfaces,
the two-row and three-row seeds for both difficult components, 13 common ports per layer, and target-pool avoidance.

This is a research manuscript with editorial work and finite-certificate review completed.
The complete analytic proof still requires independent peer review; before submission, fill in the actual author,
affiliation, contact information, and journal declarations.
