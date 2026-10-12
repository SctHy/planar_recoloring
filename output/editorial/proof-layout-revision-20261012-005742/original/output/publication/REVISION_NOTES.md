# Formal manuscript revision notes

This round follows the narrative structure used for combinatorics manuscripts in [openai/math](https://github.com/openai/math):
front-load the main results, position prior work, explain the proof route, give the complete proofs, and provide a supplementary certificate.
The writing format is used as a reference only; no mathematical conclusion from the reference manuscript is borrowed or used as a proof here.

The main article was reorganized from 28 pages to 26 pages. The introduction now gives three main theorems,
and the threshold table includes the bipartite and block-subcubic cases. The abstract explicitly includes the block-subcubic result,
which is stated as a formal theorem in the article. The existing Hamiltonian-cycle upper bound for degenerate graphs and the forest result of
Choo–MacGillivray are distinguished accurately; the Hamilton-connected and vertex-pancyclic strengthenings are proved in the article.
The added unified optimality proof uses permutation parity; no unproved exact Hamiltonian threshold is claimed for general degenerate graphs.

After unifying the shared clique-fibre definition, the two degenerate-graph proofs remove repeated setup while retaining the
same-fibre endpoint path construction, the parity obstruction for the closed-cycle lift, and all length intervals.
The adjacent-vertex restoration description now includes the actual containment changes between three- and four-element lists.
Three duplicate proof end markers were removed, excess spacing caused by the empty author field was removed from the title,
references were sorted by first author, and the bibliography was placed together on a separate page.

The standalone certificate supplement has 14 pages. The 53 marked data blocks in the original 41-page full manuscript
are preserved byte for byte; the old full manuscript and unused fragments remain in the workspace and are excluded from the submission package.
The supplement also lists seven short adjacent-pair cycles and marks the three path cycles actually used in the article.

Verification coverage:

- Adjacent pairs: 53 endpoint paths, 225 labelled list pairs, 3,225 interfaces, and 27,600 entry states;
  endpoint feasibility was also checked by exact subset dynamic programming.
- Paths: 60 valid boundaries, 72 distinct permitted cycles, 504 directed boundary transitions, and 720 cycle pairs;
  at least two safe common edges were retained, and square support at adjacent bad boundaries was checked.
- Pentagons: 23 complete component types, 2,304 labelled boundaries, and all 313 standard-source interfaces;
  47 individual records, 236 selector cases, and 30 constant-family cases form a complete partition.
  The two difficult components retain all 13 common edges layer by layer across the two-row and three-row seeds, and the pools were checked.
- Nine invalid-input rejection tests passed, including invalid individual interface edges and witnesses removed by a pool.

Both final PDFs compiled without warnings, undefined references, or overfull/underfull boxes.
All pages received text-boundary checks; page overviews and key pages for the article and supplement received visual review.

The delivered artifact is a research manuscript with editorial work and exact finite-certificate review completed.
Author metadata and the journal template must be completed from actual information; the complete analytic proof still requires independent peer review.
The general planar girth-five four-colour problem remains open.
