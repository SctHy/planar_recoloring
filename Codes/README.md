# Local constructions and finite verification

The article includes `local_constructions.tex` after its references as Appendices A--J.
These appendices appear in `../main.pdf`; the accompanying explicit constructions are in `data/`.

The verification programs enumerate the proper colourings of each local graph and check the
specified paths and cycles, their complete vertex coverage and adjacency, auxiliary and protected
edges, permissible identifications of boundary positions, and common edges at boundary transitions.
The product constructions also use partitions into edges and triangles joined by trees, with at
most two joining edges incident with any vertex.

## Finite verification

Run from the repository root with Python 3.10 or later and the standard library:

```sh
python3 Codes/verify_all.py --write-reports \
  --report-dir /tmp/planar-recoloring-reports
```

The temporary reports record finite computations on the listed local graphs and their boundary
colourings. The general lifting, product, splicing and structural-induction arguments are proved
in the article.

## Families of local constructions

| Programs | Mathematical content |
| --- | --- |
| `verify_adjacent_pairs.py`, `verify_path232.py` | Endpoint paths, transition cycles and safe edges. |
| `verify_protected_pentagons.py` | Pentagon components, protected edges and product cycles. |
| `verify_shared_hub_paths.py` | Paths with a common outside neighbour and their boundary transitions. |
| `verify_degree_two_*.py` | Degree-two configurations and independent checks of chosen-cycle intersections. |
| `verify_pentagonal_reservoir*.py` | Pentagon components and independent checks of chosen-cycle intersections. |
| `verify_extended_cycle*.py` | Linked pentagons, shared-edge pentagons and a three-contact path. |
| `verify_bowtie*.py` | Bowtie product cycles, clique partitions, trees and protected-edge intersections. |
| `verify_hinged_pair*.py` | Hinged-pair product cycles, clique partitions, trees and protected-edge intersections. |
| `finite_graphs.py` | Common operations on finite graphs, paths and cycles. |
| `bowtie_core.py`, `hinged_pair_core.py` | The fixed local graphs, boundary colourings and symmetries. |

The `data/` subdirectories correspond to these families. The graphs, boundary conventions and
normalizations are specified in the respective appendices. Any change to a local construction
must be checked again by the corresponding programs.
