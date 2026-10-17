# Finite certificates

The main article loads `article_certificates_body.tex` after its references as Appendices A--J.
`article_certificates.tex` and `article_certificates.pdf` provide a standalone rendering of the same
appendices. The `data/` directory contains the literal finite inputs used by the readers.

The readers use Python 3.10 or later and the standard library only. They cover shared-hub paths,
degree-two families, pentagonal reservoirs, extended cycles, bowties, and hinged pairs. Their checks
include finite legality, complete coverage, selected cycles and seeds, protected edges, physical
aliases, interface transitions, and clique trees. The general lifting, product, splicing, and
structural-induction arguments remain analytic arguments in the article.

## Run the readers

From the repository root:

```sh
python3 supplement/verify_all.py --write-reports \
  --report-dir /tmp/planar-recoloring-reports
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The reader command prints the result of each suite and writes local machine-readable output to the
selected temporary directory. Those generated files are validation output, not article source.

## Reader groups

| Reader | Scope |
| --- | --- |
| `verify_adjacent_pairs.py`, `verify_path232.py` | Shared endpoint paths and transition cycles. |
| `verify_protected_pentagons.py` | Protected pentagon components, seeds, ports, and product cycles. |
| `verify_shared_hub_paths.py` | Shared-hub path families and physical interfaces. |
| `verify_degree_two_*.py` | Degree-two families and independent interface replay. |
| `verify_pentagonal_reservoir*.py` | Reservoir components and independent interface replay. |
| `verify_extended_cycle*.py` | Extended-cycle families and independent interface replay. |
| `verify_bowtie*.py` | Bowtie seeds, clique partitions, trees, and interfaces. |
| `verify_hinged_pair*.py` | Hinged-pair seeds, clique partitions, trees, and interfaces. |
| `certificate_core.py` | Shared parsing and exact graph helpers. |
| `bowtie_core.py`, `hinged_pair_core.py` | Model-specific helpers and literal data contracts. |

The computation checks finite local evidence only. It does not formalize the whole article or replace
the analytic proofs.
