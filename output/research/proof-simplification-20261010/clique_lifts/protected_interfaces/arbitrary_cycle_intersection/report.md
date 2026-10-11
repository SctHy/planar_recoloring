# Counterexample to an arbitrary-cycle nine-edge bound

The proposed uniform raw-intersection assertion is false even for two ordinary Hamiltonian fibres and even if all eight of the old source pool edges remain on the changed source cycle.

Use original interface record 76. The source boundary is `00101` and the actual target boundary is `10101`; only the excluded colour at position zero changes. Both fibres have 64 states. Let `C` be the printed `C1-00101` Hamilton cycle. The target cycle is its image under reversal of the five coordinate positions followed by the colour exchange `0 <-> 1`. This is the old canonical restoration, whose normalizer is `(shift0, orientation-1, permutation1023)`.

The original source and target cycles have nine common edges. In `C`, replace

```
31020--32020, 31030--32030
```

by

```
31020--31030, 32020--32030.
```

This is a valid two-opt switch: reverse the old cyclic-word segment with zero-based indices 3 through 52. It leaves a single spanning cycle, because the new connections join the two complementary paths into one cycle. The new edges are legal recolourings. Every old source pool edge survives. With the unchanged target cycle, the resulting common-edge set is exactly

```
21010--31010 21020--23020 21020--31020 21210--21213
21210--31210 21230--31230 21320--31320 31210--31212
```

and therefore has eight edges. The complete two 64-word cycles, removed and added edges, normalization and input hash are frozen in `switch-results.json`. A separate reader with no helper import verifies the legal state sets, every cyclic edge, the exact switch, restoration, nine-to-eight intersection change, and survival of all eight source pool edges.

Discovery checked only a single fixed interface and stopped after 171 edge-pair tests and three valid switches. It did not replay the interface kernel or perform an arbitrary Hamilton-cycle search. The assertion that the printed fixed cycle pairs have at least nine raw edges remains true as a finite observation. The counterexample prevents deriving that assertion solely from arbitrary Hamiltonicity and a one-list change. It does not show failure of any actual protected intersection or rule out a pool-aware or selected-cycle structural argument. No manuscript or formal archive was edited.
