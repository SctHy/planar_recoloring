# Either fixed protected side versus an arbitrary opposite Hamilton cycle

The symmetric local test covers **266 of the 308 interfaces having at least one
ordinary side**. Five hard/hard interfaces have no whole-component
Hamilton-cycle side and are excluded. The original narrow forward result remains
unchanged at 200/256. The new reverse test covers 228/282. Their ordinary/ordinary
directional union is 202/230. All thirty constant-source/hard-target cases are
covered in the reverse direction. These exact finite results are retained in a
new directory; none of the earlier records, source bytes or manuscript is changed.

## General local implication and the permitted swap

Let J be any fixed edge set, let G be a graph with a Hamilton cycle H, and let P
be a fixed pool on the Hamilton-cycle side. At v∈V(G), let d=d_G(v) and let g
count incident edges belonging to J that are edges of G and avoid P. Every
Hamilton cycle uses two incident edges at v, at most d−g of which can avoid the
safe fixed set. Therefore

`|E(H) ∩ (J \ P) ∩ δ(v)| ≥ max(0,2+g−d)`.

Only G needs a whole-component Hamilton cycle. The component supplying J may be
hard, with J its prescribed protected K. Consequently a hard **original target**
is not permanently excluded: its restored K can be the fixed edge side, while
the ordinary original source supplies the Hamilton-cycle premise.

For each original interface, forward means fixed K_source against **any target
Hamilton cycle**, avoiding the restored target pool. Reverse means fixed
restored K_target against **any source Hamilton cycle**, avoiding the original
source pool. K already excludes its own fixed-side pool. The target K and target
pool are restored using the **original interface's first normalizer**. The
program never renormalizes a swapped source/target pair; that would risk choosing
a different fixed K or pool.

A positive forward or reverse certificate implies the desired intersection for
the specified protected bases, by specializing the arbitrary Hamilton-cycle side
to its supplied ordinary component cycle. The directional union does not imply
an intersection for every pair of arbitrary source and target Hamilton cycles:
the fixed-K side remains fixed. The separate graph-only arbitrary-both-cycle
branch covers 125/230 under that stronger quantifier and remains distinct.

## Actual-source exact computation

`check_symmetric.py` independently parses the fifty-three marked phase6 blocks,
the component cycles, hard D13 bases and fixed pools. It reconstructs all 283
nonconstant rows directly from `INTERFACES-ALL`, adds the thirty constant-source
interfaces, and reconstructs the prescribed first normalizer. States are integer
tuples. At fixed-K endpoint candidates in the ordinary Hamilton-cycle-side
component, it generates only one-coordinate list mutations. It does not import
peer helpers, enumerate a complete legal-state graph, search Hamilton cycles,
or compute actual K_source/K_target common-edge sets.

The frozen source SHA-256 is
`7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3`.
The preserved original forward-result SHA-256 is
`fb21db194e918b1dc05c2d7a0a3a5826ced3f187f8fcb5bea66d747f9fdf21c9`.
The actual execution uses CPython **3.14.6**.

The computation compares all 10,706 forward observations with the original
result, including every local neighbour list, safe fixed-K edge list, d, g and
lower bound. They agree exactly. It additionally evaluates 10,808 reverse
observations under the unchanged original mappings. Every observed local
neighbour lies in the specified ordinary component word set.

| Group | Total | Forward covered | Reverse covered | Directional union |
| --- | ---: | ---: | ---: | ---: |
| Ordinary source / ordinary target | 230 | 181 | 183 | 202 |
| Hard source / ordinary target | 26 | 19 | ineligible | 19 |
| Ordinary nonconstant source / hard target | 22 | ineligible | 15 | 15 |
| Constant source / hard target | 30 | ineligible | 30 | 30 |
| Hard source / hard target | 5 | ineligible | ineligible | excluded |
| All specified interfaces | 313 | 200 | 228 | 266 |

Both directions are eligible on 230 cases and both are positive on 162 of them.
The HH directional union gains 21 beyond forward181 and 19 beyond reverse183.
Across the original 53 nonconstant interfaces with at least one hard side,
the new directional criterion covers 34/53: nineteen forward plus fifteen
reverse; fourteen eligible cases and five hard/hard cases remain unresolved
by this criterion. The constants contribute thirty further reverse cases.

The original57 hard-target exclusions consist of22 ordinary nonconstant sources,
30 constant sources, and5 hard sources. The first52 can now be evaluated with
their original restored hard K as the fixed edge side. They yield45 positive
reverse cases. Thus retaining the narrow forward exclusions does not impose
those exclusions on the symmetric generic criterion.

## Evidence boundaries

The incident counting implication and the legitimacy of exchanging the fixed
edge side are analytic arguments. The counts266/308 and202/230 are exact checks
on the supplied313 interface set. A finite directional union does not prove
a uniform symbolic C5-family statement. Completeness of the component word lists
is supplied by the frozen manuscript context and is not re-enumerated here.

For ordinary components, an arbitrary Hamilton-cycle intersection after deleting
a fixed pool does not establish that every chosen cycle contains all pool edges
needed in a splice construction. Hard fixed sets come from the prescribed D13
bases and do not acquire a whole-component Hamilton cycle through this swap.
No claim is made on the5 hard/hard cases.

The independently written script and its result, this report and the task are
bound by a validated standard computation record. The validator checks schema
and SHA-256 hashes only; it does not verify the mathematical lemma. The broader
graph recolouring research remains open wherever its current proof has open
requirements.
