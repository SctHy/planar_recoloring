# Exact compressed source selectors for three-edge-union certificates

Extend the dedicated three-edge-union proof beyond the two complete source families. Read only the independently frozen230-case graph-local result. Every one of its125 positive interfaces has a certificate with no common incident pool edge and union of the two full incident stars of order at most three. For each source type, find an exact minimum-cardinality state set covering all its positive cases using those frozen certificates.

Feasibility: at most20 candidate words per source and at most15 covered interfaces, so dynamic programming over at most2^15 interface masks and20 candidate words is tiny. Use exact CPython3.14.6 stdlib; no new adjacency computation, normalizer recomputation, state-graph enumeration or Hamilton search. Cached current inventory lists Mathematica and Sage unavailable. Do not claim minimum over changed pools or alternative mechanisms, or joint minimum of distinct words across sources.

Deliver frozen masks, minimum-per-source selectors, complete125case-to-state map, a table-only candidate and size comparison. This is a compact finite certificate proposal. A full actual-manuscript source/pool review remains necessary before adopting any reduction.
