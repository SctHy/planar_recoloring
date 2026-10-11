# Independent review: constant pools and protected interfaces

Status: mathematical PASS within the scope below. No main-manuscript edit.
Frozen literal input SHA256:
`714dd7fa30ea60e9e54a9ce798763000c2bd91ec3f9884ece02f7b4e94a8dd63`.

`independent_review.py` imports no code from the candidate checker. It
reconstructs every listed component state set, the prescribed cycles/common
edge sets, the normalization and all overlapping one-entry target components.
This independently recovers exactly the 313 interface parameters, verifies
all old literal witnesses, and checks all nine new pool choices in both source
and target roles. Every choice passes. Choice `(1,0)` invalidates only five
old literal witnesses, the minimum over the nine choices. Four have constant
source; the sole other one is `00001:0`, position 4, new excluded colour 0,
target `00000:1`, whose replacement is `12132--32132`.

## Stronger short proof than five-rotation replay

The original candidate's six witnesses are valid, but the statement
"source K is rotation-invariant, so one target witness suffices" would be
false: the canonical target K family fails full equivariance in 72 of its
120 nonidentity rotation tests. The five-rotation intersection certificate
correctly avoids that inference.

There is a shorter mathematical reason. A boundary with four 0 entries and
one q entry has only two possible normalizing coordinate directions. Its
colour permutation is forced to the lexicographically first permutation
taking 0 to 0 and q to 1. Pulling every target back to changed position 0
therefore produces exactly two protected sets, rather than five unrelated
sets. The six selected witnesses have their two standard images among only
four protected edges of type 00001. See `two_orientation_candidate.tex`.
The independent checker verifies all displayed source memberships, all
twelve images and the algebraic identity for every position. Thus 30
position-specific cases can be replaced by six parameter families, six
source memberships, four target memberships, and one uniform normalization
argument. This is a modest mathematical case reduction, not merely hiding
the 30 cases inside a five-rotation computer assertion. It does not remove
the remaining 283 individual directed-interface cases or any component type.

## Mixed product proof and external theorem

A five-edge constant pool genuinely has enough edges: the first two are
distinct cuts for the P2/P3 seed splices, and its last three remain in every
physical row. Keep the original six reserves for all other 21 component
types. The product argument does not require all pools to have one common
size; only a common set of three surviving reserve edges for each fixed A.
For hard A the already verified P2/P3 seeds retain the common-edge set in
every row, so any three old reserve edges can be selected.

For a general B component, first choose a P2/P3 factor. The analytic cut
bound `c(B-S) <= 2|S|` for every nonempty S applies because B is a component
of the complete fixed-list recolouring graph of the triangle-free C5.
All B components are nontrivial: lists have size at least three, and a
repeated colour gives an equal-neighbour corner with another legal colour.
For empty S, connectivity gives `c(B)=1<3`. Ellingham--Zha Theorem 3.5,
with g=2, k=3, then adds exactly c(F)-1 actual B edges connecting the specified
factor components, with added incidence at each physical B vertex at most
three. Contraction is a tree. This is an added-edge bound, not a bound on
the vertex's total degree including its original path edges. The theorem
was rechecked in the authors' PDF:
https://math.vanderbilt.edu/ellingmn/paper/ttw/b-eps.pdf (Theorem 3.5, p. 9
in PDF numbering, printed p. 8).

Process this tree parent before child. Before any join at a parent physical
row at most two of its three chosen reserves have been cut, while all three
survive in the fresh child row. Cut the same unused A edge on both sides
and use the two Cartesian cross edges supplied by the B joining edge.
This joins the cycles and preserves every K_A edge in every physical row.
The argument covers arbitrary old/new A pools mixed with arbitrary B types.

## Integration scope and cost

The candidate excerpt cannot be integrated solely by replacing the two
constant pools. At review time the main product proof still uses physical
load six (main lines 1702--1728), and the printed path-factor proof establishes
the isolated-vertex condition rather than the full component cut bound.
Integration needs the full cut-bound proof, the EZ citation/application,
the load-three mixed product proof, the two ordered pool changes, the six
parameter-family proof, and the one nonconstant-source witness replacement.
Source normalization, all other pools/seeds/cycles and the 23 component types
can remain as currently specified.

Expanded labelled standard-source interface coverage stays 313; the appendix
may print 283 individual records plus six parameter-family representatives,
289 representatives in all. Claims of "only 289 interfaces" would be false.
The result proves exactly the previous protected-product/lift conclusions,
not any stronger graph-class or palette threshold theorem.

Recommendation: worth integrating if the manuscript accepts the analytic
full-cut/EZ dependency. Use the two-direction proof, not the five-rotation
W formula as a replacement for a proof. If avoiding this added external
dependency is the editorial priority, retain the current six-reserve product
and treat this as an optional research candidate; a five-edge pool alone
would not support the current load-six argument.

## Better integration route if both hard factors are traceable

`traceable_factor_product.tex` proves a general alternative: a Hamilton path
in B can be divided into consecutive P2/P3 blocks. Its specified A products
are joined in a chain using one fixed surviving reserve edge. Each physical
row is an outer endpoint of at most one block boundary because every block
has at least two rows. Thus the reserve is never reused in a physical row.
No protection condition on the B Hamilton path is required: B merely supplies
the Cartesian cross edges. This works for every old/new A pool configuration.

This replacement retains all original pools, K sets, P2/P3 seeds and all 313
interface witnesses. Only two new full-component path words are needed,
because the other 21 B types already have Hamilton cycles. If both paths
are independently verified, it is shorter than the analytic-factor route
and does not need AAE, the degree-seven lemma, the full-cut bound or EZ.
The same route also permits the optional five-edge constant redesign and
six-family interface reduction without any EZ dependency.

At this review checkpoint the 51-state path for 00112 is present; the
44-state 00001 result remains UNKNOWN in its current results.json. Therefore
the generic lemma is proved, but its universal 23-type application is
conditional until the second path is obtained and checked. In the current
main source the two auxiliary lemmas are used only by protected-product;
the factor lemma also has descriptive references in validation/appendix
paragraphs. If replaced, remove/update those references and the sole AAE80
citation/bibliographic entry as appropriate. Do not describe a timed-out
00001 search as either traceability or nontraceability evidence.

## Final route: ordered blocks, with no 00001 Hamilton-path assumption

The conditional route above is superseded by a directly certified ordered
matching for 00001. Reordering its original 22 matching edges gives a path
in the 22-vertex matching quotient. The complete certificate has 44 state
words and 21 endpoint bits; the bits specify the actual connector from
the selected endpoint of pair i to the first endpoint of pair i+1.
The final graph checker reconstructs all 44 legal states and 74 edges,
checks every matching edge and connector, and confirms maximum physical
connector load two. The independent second reviewer also passed the literal
certificate. This does not imply a Hamilton path of the 44-state graph.

All 23 types therefore have ordered P2/P3 blocks joined consecutively:
21 by their existing cycles, 00112 by its verified path, and 00001 by this
matching chain. Two fixed reserve edges, alternated at successive interfaces,
suffice for all A products. Even if both joins of a middle block fall on the
same physical row, they cut distinct A edges. All original pools, protection
sets, seeds and 313 interface witnesses survive unchanged. Neither AAE,
the degree-seven lemma, the full-cut bound nor EZ is needed.

The exact independent-set computation also returned alpha=22. A displayed
22-element independent set and the old perfect matching prove this value
directly; it supplies no nontraceability obstruction.

Final candidate: `../ordered_block_product_candidate.tex`. The complete
root manuscript candidate `../../continuation-3/ordered-block-candidate.tex`
was read back and passed: all 50 original literal blocks are byte-for-byte
preserved, both added blocks match the independently checked literal data,
all internal reference labels resolve, and the removed auxiliary labels,
AAE80 citation and bibliography entry are absent. Audit record:
`full-candidate-readback-review.json`. No main file was edited by this agent.
