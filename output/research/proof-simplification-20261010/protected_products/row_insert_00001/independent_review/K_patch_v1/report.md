# Independent one-edge protected-set patch review: PASS

Let `h=12313--12323` and let `K` be the old twelve-edge set. Both candidates `(K minus h) plus g` pass the interface-membership review, with `g=13120--23120` or `g=21320--31320`. This assertion concerns local memberships; neither a protected two-row seed nor a protected three-row seed has been constructed here.

Only 24 of the 283 individual records involve `00001`. Inspecting their old witness on every modified source side and its normalized image on every modified target side shows that exactly the three previously identified witnesses are damaged. Therefore 280 old valid witness certificates remain valid by containment. For each patch the three damaged interfaces are repaired explicitly. For the preferred edge `13120--23120`, the two self-type common sets are

```
position4->2: {13120--23120, 13210--23210}
position4->3: {12310--32310}.
```

The canonical inverse permutations are respectively `(0,2,1,3)` and `(0,3,1,2)`. They send the new edge to `13210--23210` and `12310--32310`, which are old protected edges. For `g=21320--31320`, the corresponding images are `12310--32310` and `13210--23210`. The third damaged interface, position1 changed to3, retains three common edges for either patch, including `21313--21323`.

The four canonical target edges used by the existing six constant-source families remain in both patched sets. The source constant sets and the normalization identity are unchanged, so that proof still covers its thirty interfaces. Together with the inherited 280 individual certificates and three repaired records, this accounts for all 313 cases without reconstructing every graph or replaying every interface kernel.

After deleting the four endpoints of the two same-sign edges, the remaining graph `H40` has forty states. Six of the seven old reserves avoid those deleted vertices, giving fifteen unordered reserve pairs. Independently replaying the necessary propagation for each pair and each patch gives the same forced edges, available-edge counts, degree distributions and round counts as the discovery results. Every forced subgraph is acyclic with maximum degree at most two, and every vertex has an available incident edge. A saturated forced degree of two excludes every other incident edge; a unique available incident edge is forced by the no-isolate condition. These rules are sound necessary tests.

Passing these tests does not supply a spanning linear forest, its required endpoint matching, or either product seed. The original seed has no same-sign internal edges and cannot directly support the one-row insertion. A new or locally modified seed must first be constructed and checked. No such search was performed in this review, and the manuscript is unchanged.
