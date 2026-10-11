# Complete preferred 00001 redesign: PASS

This review checks the actual frozen candidate `candidate-v1.tex`, SHA256 `07c0a2c7873b15f1cb6e52a51f0fcecb355561c2d3ea1b7b4d1ebc8c29efe4b2`, together with the successful two-row and three-row certificate JSON files. The scripts use no peer graph, edge, DFS or Hamilton-search helper.

The redesigned protected set is exactly

```
Knew = (Kold minus {12313--12323, 13230--23230})
       plus {13120--23120}.
```

It has eleven edges. Adding the reserves `21210--21213` and `21230--31230` gives the thirteen-edge common set `D`. The candidate's printed definitions agree exactly with the checked sets.

Generating the legal words directly from boundary `00001` gives 44 states and 74 original-graph edges. The returned new two-row cycle covers each of the 88 product states exactly once and has only legal Cartesian-product edges. The candidate's seven literal path toggles, applied directly to the old printed cycle, give cycle-size lists

```
88; 39,49; 5,7,37,39; 5,7,76; 12,76; 16,72; 88.
```

Every stage has degree two and legal edges. The final edge set equals the successful 88-word cycle exactly. It retains every edge of `D` in both rows and contains the three specified matching cuts in old row digit 1.

The printed forty-state path has endpoints `13210,13230` and contains exactly all legal states other than `12312,12313,13212,13213`. Every consecutive edge is legal and all thirteen `D` edges occur in the path. Together with the two new-row edges `12312--12313` and `13212--13213`, it partitions the new row. The three old-row cuts are pairwise vertex-disjoint, present in the actual new cycle, and disjoint from `D`. Replacing them by their same-endpoint new-row paths subdivides three cycle edges. Independent reconstruction agrees **word for word** with all 132 supplied derived words, covers every three-row product state exactly once, and checks every cyclic product edge. All thirteen ports occur in each row of both seeds.

The interface audit inspects the 24 old individual records involving `00001` for a deleted source witness or a deleted canonical target image. Exactly three require replacement. Their new witnesses are `21313--21323`, `13120--23120`, and `12310--32310`, with exact source/target memberships verified. The other 280 valid old certificates are inherited. The four canonical target edges used by the unchanged six constant-source families all remain protected. Consequently all 313 interfaces are accounted for by the old valid certificates, these three explicit repairs, and the existing normalization identity, without a full graph/interface-kernel replay.

The candidate's three-table-row repair statements and English descriptions of the prescribed forward and inverse colour maps agree with these computations. In particular, the first target normalizer sends its replacement to `21231--23231` in `K00102`; the second exchanges the two common edges by the colour transposition `(1 2)`; the third inverse map sends the new edge to `12310--32310`.

The previous all-seed endpoint obstruction required protection of `13230--23230`. The new design drops that edge, so it does not contradict the obstruction. This is a complete positive certificate for the specified local seeds and memberships, not a universal implication from an arbitrary two-row cycle. No seed search, Hamilton search, manuscript edit, or formal archive update was performed by this reviewer.
