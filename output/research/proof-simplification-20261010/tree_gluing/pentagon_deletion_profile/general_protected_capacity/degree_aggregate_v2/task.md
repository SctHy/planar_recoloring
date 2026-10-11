Compute the strengthened graph-only aggregate bound on the same 230 ordinary
full-component interfaces as frozen degree_aggregate_v1. Both component
Hamilton cycles are arbitrary; only full state sets, graph legality and fixed
pool unions are inputs. Construct J from internal outside-set edges having a
source-degree-two endpoint. J is forced in every source Hamilton cycle. Its
incidences reduce each outside vertex's remaining cross-edge capacity.

For a single non-star boundary edit, select all common states with
r(v)=4-d_target(v)-f(v)>0. Prove this selector maximizes this capacity bound,
using that a common state has at most one source neighbour outside the target.
Compare the new covered case identities with the stored 125-interface
two-arbitrary-HC node result. Preserve v1 bytes, write the exact outputs,
provenance, proof and computation record, and identify a small new coupling
certificate if coverage exceeds 125. Do not modify the manuscript.

Feasibility: 230 fixed fibres, each with at most 88 supplied printed states.
Only immediate legal recolourings at common or outside states are generated;
no exhaustive palette^5 state enumeration, Hamilton search, selected C/D edge
intersection, or graph-size extrapolation. Exact Python stdlib should complete
in a second with negligible memory. Complete-state and Hamiltonian input
status is inherited from the source-bound earlier 313-case readback.
