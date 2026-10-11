# Girth-five planar recolouring: Hamiltonian-threshold checkpoint (2026-10-12)

## Current mathematical boundary

For a finite simple graph `G`, `R_k(G)` has the proper labelled `[k]`-colourings as vertices, and two states are adjacent when exactly one vertex changes colour. The uniform threshold is

```text
h(C) = min { q : R_k(G) is Hamiltonian for every G in C and every k >= q }.
```

The current manuscript establishes

```text
4 <= h(P_5) <= 5,    4 <= hc(P_5) <= 5,
```

where `P_5` is the class of planar graphs of girth at least five. The lower bound is the frozen three-colouring obstruction on a cycle whose length is a multiple of three. The upper bound in the manuscript is the five-colour Hamilton-connected theorem for triangle-free planar graphs. The four-colour Hamiltonian result is proved for the two subclasses recorded in `main.tex`: at most seven 5-cycles, and blocks of internal maximum degree at most three. The complete class remains open.

The public-literature check found no later result that changes this boundary. Bartier--Bousquet--Feghali--Heinrich--Moore--Pierron prove only that `R_4(G)` is connected for every planar girth-five `G`, not that it contains a spanning cycle. See <https://arxiv.org/abs/2112.00631>, especially Problem 1.2 and Theorem 1.3. General `d`-degenerate Hamiltonicity at `k >= d+3` is a large-palette result and does not settle the missing case.

## Exact bounded checks

The Jacobian operation `graph.cycle.fixed_length.decide` was run on complete recolouring graphs generated directly from their definitions:

| graph | order of `R_k(G)` | edges | requested cycle length | exact result |
|---|---:|---:|---:|---|
| `R_3(P_3)` | 12 | 15 | 12 | `DOES_NOT_EXIST` |
| `R_3(C_5)` | 30 | 30 | 30 | `DOES_NOT_EXIST` |
| `R_4(K_2)` | 12 | 24 | 12 | `EXISTS` |

The first result independently reproduces the forced-four-cycle obstruction used for the forest lower bound. The second reproduces the two 15-cycle components of the three-colour pentagon. The positive result is a small sanity check for the labelled-state convention. An attempted direct Jacobian search on `R_4(P_3)`, of order 36, was refused by the operation's 10,000,000-path admission bound; that is an operational refusal, not a negative Hamiltonicity result.

The repository verifier was also rerun without source changes:

```text
adjacent-pairs: PASS
path232: PASS
protected-pentagons: PASS
status: PASS
evidence_level: exact-check
scope: finite local certificates and 23x23 product/reserve replay;
       arbitrary-order component-graph and tree-splicing arguments remain analytic
```

These checks validate the finite certificates only; they do not decide the general `P_5` question.

## Finite exploratory signal and the local obstruction

A temporary exhaustive search of connected minimum-degree-at-least-two girth-five cores through order seven found the only cores `C_5`, `C_6`, and five order-seven types. Their four-colour recolouring graphs have orders 240, 732, and respectively 1764, 1716, 1608, 2184, 1680; an exact SAT Hamilton-cycle check found a spanning cycle in each case. All seven cores passed an independent rotation-system planarity check. This is small-order evidence only; the graph list and SAT witnesses were not used as a proof premise for the manuscript.

The more useful negative signal concerns a pentagon fibre with a fixed colouring of its exterior. If `A_i` is the allowed set at the `i`-th pentagon vertex, the local fibre consists of proper cyclic words `x_i in A_i`, with one-coordinate changes as edges. The standard subcubic certificate only needs `|A_i| >= 3`. Once a pentagon vertex has internal degree at least four, a two-colour allowed set can occur. For

```text
(A1,A2,A3,A4,A5) = ({0,1},{0,1},{0,1},{0,1},{0,2}),
```

the fibre has exactly the two states

```text
(0,1,0,1,2) and (1,0,1,0,2),
```

and no edge between them. The standard-library reproducer is `local_fibre_scan.py` in this directory. Exhaustively scanning all five-tuples of allowed masks of size at least two found 48,784 disconnected nonempty local fibres and 58,200 with minimum local degree below two (among 161,051 mask patterns). These are local interface obstructions, not complete-graph counterexamples: the exterior recolouring can change the lists and connect the states globally.

## Research consequence

The existing protected-pentagon induction cannot simply be promoted from subcubic blocks to arbitrary internal degree. A successful proof of `h(P_5)=4` needs either a new global splice invariant that tolerates two-colour or singleton local lists, or a structural theorem guaranteeing a restorable configuration whose pentagon boundary lists stay in the certified three-colour regime. Conversely, a genuine `h(P_5)=5` result requires a complete planar girth-five graph whose full `R_4(G)` is not Hamiltonian; no such graph has been verified in this checkpoint.

The Hamilton-connected question is strictly harder: even the two manuscript subclasses have only `4 <= hc <= 5`. Therefore the defensible status after this checkpoint is still "threshold approximately 4, exact value unresolved," with the finite evidence biased toward 4 but no theorem-level upgrade.
