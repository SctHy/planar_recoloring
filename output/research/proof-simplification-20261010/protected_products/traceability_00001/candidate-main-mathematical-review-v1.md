# Readback of the ordered-block manuscript candidate

Read `continuation-3/ordered-block-candidate.tex`, ordered-path-block lemma
at lines 1595–1610 and protected-product proof at lines 1662–1680.

**PASS.** The component enumeration is complete: 21 specified Hamilton
cycles, the independently verified 51-state path for 00112, and the
independently verified 22 matching-block chain for 00001 cover all 23 types.
Partitioning a traceable factor into pairs and one optional triple is valid
for every order at least two. The nontraceable 00001 factor requires only
the contracted block chain, never a Hamilton path of its state graph.

Two distinct reserve edges suffice. Alternating them ensures that the two
interfaces incident to an intermediate block never cut the same edge. This
continues to hold if both joins use the same physical row or the two reserve
edges have a shared A endpoint. At each stage the chosen edge is still an
edge of the accumulated Hamilton cycle; the corresponding fresh block has
its untouched copy. Removing the two edges and adding Cartesian cross edges
merges the two cycles and preserves degree two. Every K_A edge survives in
every physical row. The printed seeds retain the selected reserves in all
rows, so there is no hidden all-row assumption.

The candidate preserves the original K sets, pools, seeds and 313 interface
premises. No additional mathematical hypothesis is required. This is a
read-only mathematical review; manuscript compilation and reference checks
belong to the integrating parent task.
