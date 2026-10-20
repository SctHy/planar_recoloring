# Finite certificates

The main article loads `article_certificates_body.tex` after its references as Appendices A--J.
These appendices are included in `../main.pdf`. The `data/` directory contains the literal finite
inputs used by the readers.

The readers use Python 3.10 or later and the standard library only. They cover shared-hub paths,
degree-two families, pentagonal reservoirs, extended cycles, bowties, and hinged pairs. Their checks
include finite legality, complete coverage, selected cycles and seeds, protected edges, physical
aliases, interface transitions, and clique trees. The general lifting, product, splicing, and
structural-induction arguments remain analytic arguments in the article.

## Running the readers

Run all readers from the repository root:

```sh
python3 Codes/verify_all.py --write-reports \
  --report-dir /tmp/planar-recoloring-reports
```

Each reader prints whether its finite checks pass. The reports written to the report directory are temporary
and are not part of the repository; they record the outcome of finite checks only, not a proof of the article.

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

## Data format

Certificate inputs are UTF-8 JSON files, optionally gzip-compressed. The loaders below read each
family, and the readers validate its required fields before checking the graph data:

| Data family | Loader | Main fields |
| --- | --- | --- |
| Shared-hub paths | `verify_shared_hub_paths.load_family` | `path_order`, `normalization`, `records[{boundary,cycle}]` |
| Degree-two paths and stars | `verify_degree_two_families.load_family` | `kind`, graph and port metadata, `normalization`, `records[{boundary,cycle}]` |
| Pentagonal reservoirs | `verify_pentagonal_reservoirs.load_family` | `kind`, `records[{boundary,cycle(s)}]` |
| Extended cycles | `verify_extended_cycles.load_family` | `family`, `records[{boundary,cycle}]` or `templates` |
| Bowties | `bowtie_core.load_data` | `family`, `templates[{boundary,matching,cycles}]`; tree files add `indexing`, `blocks`, `connectors` |
| Hinged pairs | `hinged_pair_core.load_data` | `format`, `models` containing cycle and tree records |
| Ordinary pentagons | `verify_bowtie_families.load_ordinary` | `cycles`, `hard_cores`, `hard_ports`, `hard_seeds`, `pools`, `provenance` |

Each reader validates legal one-coordinate transitions, selected cycles or paths, complete coverage,
and the interface records needed by its appendix. The `data/` subdirectories mirror the reader
groups above; changes to a data file must be accompanied by a reader run from the repository root.
