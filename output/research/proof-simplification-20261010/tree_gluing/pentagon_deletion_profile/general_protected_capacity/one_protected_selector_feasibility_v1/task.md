# Frozen one-protected-side source selectors: next-stage feasibility

Compute exact minimum source-word covers using only the already frozen
`one_protected_vs_hc_v2/symmetric-one-sided-results-v2.json` observations.
Compare all 236 covered nonconstant interfaces, their 111 interfaces outside the
current 125 three-edge-union family, and the additional words needed when the
existing 48 source-word memberships are retained. Keep original interface
identities, original first normalization maps, directions, component IDs,
ordinary pools and restored hard bases unchanged.

At a common actual word, a fixed protected K has g incident edges in the full
star of the opposite Hamilton-cycle side and outside that side's prescribed
pool. A whole-component Hamilton cycle uses two incident edges, so its
intersection with these safe edges is at least max(0,2+g-d). Positive local
certificates therefore have d-g<=1. Only the opposite side is arbitrary; the K
side stays fixed. A direction may vary by interface but must be saved explicitly.

This job is exact finite mask optimization over saved observations. It must not
generate graph vertices or neighbors, renormalize interfaces, enumerate K/K
intersections, search Hamilton cycles, modify any earlier frozen artifact,
produce a full manuscript candidate, or edit Main. Report minimum memberships,
source rows, distinct words and explicit finite-scope limitations. Deliver code,
results, feasibility report and a validated schema/hash computation record.
