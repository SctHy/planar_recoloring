# Girth-five frontier: apex pentagons (2026-10-14)

Request: prove `h(P_5)=4`. Outcome: **not proved**. The boundary
`4 <= h(P_5) <= 5` (and `4 <= hc(P_5) <= 5`) in `main.tex` is unchanged.
This note records what was established while attempting it. Sections 1, 2 and
4 are analytic or exactly checked; Section 3 is a finite local obstruction for
one proof method; Section 5 is exploratory evidence only.

## 1. Unavoidable configuration

**Lemma.** Every plane graph of girth at least five and minimum degree at
least three has a 5-face whose boundary is a 5-cycle with at least four
vertices of degree three; if exactly four, the fifth vertex has degree 4 or 5.

*Proof.* Work in one component. Give each vertex `3d(v)-10` and each face
`2|f|-10`; by Euler the total is `-20`. Facial walks contain a cycle, so have
length at least five, and a length-five facial walk is a simple 5-cycle. Each
vertex of degree `d>=4` sends `(3d-10)/d` to each incident face; every face
sends `1/3` to each incident degree-3 vertex. Degree-3 vertices end at `0`,
vertices of degree at least four at `0`, and faces of length `l>=6` keep at
least `(5l-30)/3>=0`. A 5-face with at most three degree-3 vertices receives at
least `2*(1/2)=1` and pays at most `1`. A 5-face with four degree-3 vertices
and fifth vertex of degree `d>=6` receives at least `4/3` and pays `4/3`. The
total is negative, so some face is one of the remaining types. ∎

Call a 5-face with exactly four degree-3 vertices an *apex pentagon*, and its
fifth vertex the apex.

## 2. Witnesses that apex pentagons are unavoidable

The duals of the snub cube and snub dodecahedron, built as Cayley maps of
`S_4` and `A_5` and checked as sphere maps by the reproducer, are:

| graph | vertices | edges | degrees | girth | 5-faces | each face |
|---|---:|---:|---|---:|---:|---|
| PI (pentagonal icositetrahedron) | 38 | 60 | 32×3, 6×4 | 5 | 24 | 3,3,3,3,4 |
| PH (pentagonal hexecontahedron) | 92 | 150 | 80×3, 12×5 | 5 | 60 | 3,3,3,3,5 |

Both apex degrees in the lemma therefore occur, and a 5-face of degree-3
vertices need not exist. These graphs have no vertex of degree at most two
and no degree-3 pentagon, so none of the reductions in `main.tex` applies to
them. They lie outside both proved subclasses: each is one 3-connected block of
internal maximum degree 4 or 5, with at least 24 or 60 five-cycles. Any proof of
`h(P_5)=4` must restore an apex pentagon or some larger configuration present
in these graphs.

## 3. Local obstruction to arbitrary-base-cycle restoration

Let `v x_1 x_2 x_3 x_4` be an apex pentagon, `y_i` the outside neighbour of
`x_i`. The two natural deletions are the path `{x_1,...,x_4}` (lists
`[4]-{f(v),f(y_1)}`, `[4]-{f(y_2)}`, `[4]-{f(y_3)}`, `[4]-{f(v),f(y_4)}`)
and, for a degree-4 apex, the whole 5-cycle (apex list of size at least two).
Over all labelled boundary words:

| deletion | boundary words | disconnected fibres | with an isolated state | with a state of local degree <= 1 |
|---|---:|---:|---:|---:|
| path `x_1..x_4` | 1024 | 48 | 24 | 288 |
| whole 5-cycle, degree-4 apex | 4096 | 76 | 48 | 912 |

In PI, for both deletions, the reproducer finds a proper colouring `f` of
`H=G-X`, an isolated local state `s` over `f`, and at least two legal
recolourings `g_1,g_2` of `H` at `f`, each giving an outside neighbour the
colour that `s` uses on its pentagon neighbour. Over any bottom Hamilton cycle
containing `g_1 f g_2`, the layered graph has `(f,s)` as an isolated vertex.
Hence a restoration lemma of the form used in `lem:path232` and
`lem:two-pentagons-restore` ("if `R_4(H)` is Hamiltonian then so is
`R_4(G)`", proved by lifting an arbitrary bottom Hamilton cycle along its own
edges) cannot be certified locally for apex pentagons. A proof must control the
bottom cycle through a stronger induction hypothesis, use bottom edges outside
the cycle, or restore a larger configuration.

## 4. Pentagonal flowers have no locked state

Call `F` a *flower* at a vertex `v` of degree `d>=3` if its neighbours
`a_0,...,a_{d-1}` (cyclically) have degree three and, for every `i`, there is a
5-face `v a_i p_i q_i a_{i+1}` with `p_i,q_i` of degree three. All faces of PI
and PH at an apex form such a flower (13 or 16 vertices, each with at most one
neighbour outside the flower).

**Claim.** No proper 4-colouring makes every vertex of a flower locked (seeing
all three other colours), whatever the outside colours.

*Proof.* A locked degree-3 vertex has three distinctly coloured neighbours. In
the pentagon `v a_i p_i q_i a_{i+1}` this makes the pairs `(v,p_i)`,
`(a_i,q_i)`, `(p_i,a_{i+1})` and `(q_i,v)` distinct, in addition to the cycle
edges. Only `(a_i,a_{i+1})` remains, so four colours on these five vertices
force `a_i=a_{i+1}`. Thus all `a_i` share one colour and `v` is not locked. ∎

The reproducer checks the five-vertex step exhaustively. This removes only
the isolated-state failure in Section 3. Component Hamiltonicity, protected
edges and overlaps for flower fibres have not been checked. An apex pentagon
need not lie in a flower, so no unavoidable set of reducible configurations is
established.

## 5. Exploratory evidence (not a proof premise)

An `R_4(G)` state of degree one would give `h(P_5)=5`. In a temporary
python-sat environment, which is not part of the reproducer:

- No 4-colouring of the dodecahedron, PI or PH has at most six legal moves;
  the dodecahedron minimum is exactly ten.
- No 4-colouring with at most two moves exists in any of 48 random planar
  girth-five graphs (20–42 vertices, up to five degree-4 vertices). These were
  built as duals of 5-edge-connected planar graphs with minimum degree five.

## 6. Status

`h(P_5)` and `hc(P_5)` remain in `[4,5]`. Concrete next targets are:

1. Find an induction invariant on bottom Hamilton cycles that is preserved by
   every existing reduction and excludes the killing pattern in Section 3.
2. Alternatively, find a discharging argument giving an unavoidable set of
   configurations, such as degree-3 pentagons, flowers and degree-two hubs.
   Each would need full local certificates in the style of Appendices C–D.

## Reproduction

```sh
python3 output/research/girth5-apex-pentagon-20261014/apex_pentagon_scan.py
```

This uses only the standard library and finishes in under a second. It
rewrites `apex-pentagon-report.json` beside the script.
