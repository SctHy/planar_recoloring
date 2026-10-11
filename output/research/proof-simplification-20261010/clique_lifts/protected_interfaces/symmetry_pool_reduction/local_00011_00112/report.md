# A four-case nonconstant normalization family

The fixed 00011→00112 orbit at changed position 0/2 and new excluded color 2/3
has a short normalization identity. It requires two pool reductions, but no
cycle or hard seed change. The candidate is saved in `candidate.tex`; it is
not integrated into the manuscript.

For source 00011 retain its old first two pool edges and its old last two:
`12102--13102`, `13102--13103`, `31202--31302`, `32130--32132`.
For hard target 00112 choose two old common reserve edges:
`12020--12030`, `13020--13030`. The latter choice avoids both the target
edge to be protected and the leaf-neighbor reserve `12320--12323`; avoidance
of that reserve is convenient for independent seed-insertion research, but
is not needed by this normalization proof.

The new K sets contain the old ones, so every already valid interface survives
by monotonicity. Ordinary seed cuts remain the original first two edges. Both
hard reserves occur in every row of both existing seeds. Thus the existing
ordered-block construction still applies with two alternating reserves.

Take e=`13202--13203`, reflect at R(x)_i=x_(2-i), and optionally swap colors
2,3. The four source images are
`13202--13203`, `12302--12303`, `23120--23130`, `32120--32130`.
All lie in the printed source cycle and outside its new pool.

Both changed boundaries have two adjacent equal pairs and a singleton, which
is the standard type 00112. The canonical normalization starts at coordinate 1, reads forward for a
change at position 0 and backward for a change at position 2, and swaps 2,3
exactly when the new excluded color is 3. These formulas give the first viable
normalizers in the manuscript's prescribed order: for `q0011`, both orders
starting at 0 begin with distinct entries; for `00q11`, the forward order at
0 has the wrong pair positions, and the backward order at 0 and forward order
at 1 begin with distinct entries. The next order reads the two equal pairs
first, followed by the changed singleton. Applying either direction to
the appropriately reflected source edge produces the same target edge
f=`32021--32031`. This is one printed common seed edge, outside the new target
pool. The algebraic identity, rather than an assertion of target equivariance,
proves the family.

This is a genuine uniform argument for those four cases: two coordinate
directions and one canonical target edge. It saves three interface records,
and removes nine pool-edge entries, but its added explanatory prose may exceed
the saved table space. It does not settle the other nonconstant orbits or
repair the previously proved global support-symmetry obstruction.

`check_four_family.py` verifies only these four normalizers, their memberships,
pool subset relations, and the two hard reserve edges in all five existing
seed rows. No full 313/283 kernel or Hamilton search was run here. Preservation
of other interfaces is the subset/monotonicity proof, not a new full replay.
The original frozen literal input remains byte-identical, and the main
manuscript remains unchanged.
