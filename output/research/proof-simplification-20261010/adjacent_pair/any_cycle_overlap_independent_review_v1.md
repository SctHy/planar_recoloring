# Independent analytic review of arbitrary adjacent-pair cycles

Status: PASS. The source is `any_cycle_overlap_candidate_v1.tex`; no main
file was edited and no complete Hamilton-cycle/list kernel was enumerated.

The exact quantifier is valid: A, B and any changed list are arbitrary
three-element subsets of one fixed four-element palette. The old and new
Hamilton cycles are arbitrary, independently chosen, and may be obtained
by different colour normalizations. Either first or second coordinate list
may change. An unchanged fibre is included. The statement does not cover
simultaneous changes of both lists, and the restoration application does
not require that case because its two exterior vertices are physically
distinct. Their colours are allowed to be equal.

For unchanged equal lists the entire fibre is C6. For unequal lists, if
their common colours are r,s, the states rs and sr have degree two. They
are nonadjacent, so their four incident edges are distinct and every
Hamilton cycle contains all four.

For a genuine change in A, its old/new excluded colours are different.
If either A equals B, their common first list is {a,b} and the fixed
second list is {a,b,c}. The common graph is exactly the P4
ab--ac--bc--ba. The endpoints ab and ba have degree two in both full
fibres, so its two end edges belong to both arbitrary cycles. This covers
both equality-to-inequality and inequality-to-equality transitions.

Otherwise all three excluded colours a,b,c are pairwise distinct, and
the fourth is d. The common graph has the five vertices ca,cb,cd,da,db.
Its edges are the triangle on ca,cb,cd, plus ca--da, cb--db and da--db:
exactly six edges. The old outside vertices are ba and bd. In the old
fibre bd has precisely the neighbours ba and cd, forcing the segment
ba--bd--cd in any Hamilton cycle. Thus the two outside vertices are
adjacent on that seven-vertex cycle; removing them leaves one path on
the five common vertices, with exactly four edges. The new fibre has
the corresponding forced segment ab--ad--cd. Its arbitrary cycle also
uses four of the same six edges. Inclusion-exclusion gives two common
edges. There is no implicit cycle-template assumption in this argument.

The minimum two is attained. In palette 0123 with old A=123, new A=023,
and B=013, the cycles
`10 13 23 20 21 31 30` and `01 03 23 21 20 30 31` share only
`20--21` and `30--31`. These cycles and the two normalized common
graphs were checked directly by the accompanying small script.

The adjacent-degree-two restoration can retain only its first displayed
seven-state cycle `(ab,ad,bd,ba,ca,cd,cb)` for A={a,b,c}, B={a,b,d}.
The normalized version `01 03 13 10 20 23 21` was checked. No second
template or template-pair inspection is needed. Cut one edge of the
bottom Hamilton cycle and process the resulting layer path: the current
last fibre has lost at most its incoming reference-cycle edge, while the
next fibre is fresh. Of at least two common reference edges one remains
available, and the ordinary two-edge switch joins the cycles. This proves
the original restoration conclusion with exactly its existing hypotheses.

The candidate needs no mathematical correction. Optional clarifications
are only expository: say that the outside vertices are adjacent on the
Hamilton cycle, and spell out the six common edges if desired. Keep the
actual exterior vertices distinct even when their colours coincide.
