# Exact local result and shorter protected-product proof

The 44-state component B_00001 is **not traceable**. For prefix colors 1,2,3,
orient the cycle 1→2→3→1 and put σ=o(x0,x1)o(x2,x3). Set χ=σ when x4=0 and
χ=−σ when x4 is 2 or 3. The set S={χ=+1} has twenty vertices. The other
twenty-four vertices induce only the two disjoint edges 12312–12313 and
13212–13213. Hence c(B−S)=22>|S|+1=21. This is an exact, structural
nontraceability certificate, independently verified from all 4^5 words.

The earlier small-cut checks and unsuccessful bounded discovery outputs
remain unchanged. They do not prove this conclusion. All cuts through size
four passed; the first and second DFS budgets ended with UNKNOWN, the
endpoint-rotation run reached length 43, and the last fixed-start search
exhausted the 21230 orbit without a path. The later sign cut supersedes the
open status without overwriting those search records.

The proposed “all 23 factors are traceable” shortcut therefore fails. A
strictly sufficient weaker property holds: all factors have an ordered
P2/P3 block partition with one actual edge between every pair of consecutive
blocks. Twenty-one factors obtain it from their existing Hamilton cycles;
00112 obtains it from the new, independently checked 51-word Hamilton path.
For 00001 the new literal certificate contains 22 matching pairs and 21
outgoing-endpoint bits. Each connector enters a_(i+1), and its outgoing
endpoint is a_i or b_i according to the bit. Independently parsing the TeX
confirms all forty-four states occur once, every matching/connector edge is
legal, and contracting the matching pairs gives exactly the ordered path.
Physical connector load is at most two (counts 0:11, 1:24, 2:9).

Use two distinct fixed reserve edges e,f in the existing P2/P3 product seeds
and alternate e,f at successive block interfaces. Every block meets at most
two interfaces, so no seed edge is cut twice, including when both connectors
use the same physical row. A two-edge splice joins the accumulated cycle
to the next fresh cycle and preserves K in every row. This is stated in
`../ordered-block-product-v1.tex`. It keeps every original K set, both hard
seeds, all original pools and all 313 interface records. It also supports
the optional constant five-edge orbit pools because two of their last three
edges can serve as reserves.

The finite cost is 51 words for 00112 and 44 words plus 21 bits for 00001.
In return the product argument needs neither the AAE path-factor theorem,
the degree-seven lemma, a connected-factor extension theorem, nor general
quotient-tree load analysis. This is a candidate proof; the main manuscript
was not edited here. No original-graph search was performed, and the
three-row hard seeds remain necessary premises of this particular proof.
