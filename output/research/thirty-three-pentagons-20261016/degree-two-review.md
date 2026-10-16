# Degree-two review of the thirty-three-pentagon continuation

Reviewed sources: `research_note.md`, Sections 6--7, and
`thirty_three_pentagons.tex`, lines 153--224. This is an analytic dependency
review, not a consequence of the archive's program verdicts.

## Verdict and adoption boundary

The four-attachment-chain argument is valid. The proposed bounds
`p >= 38` and `D >= 16` are also valid conditional on the inherited
three-face fan restoration through a retained hub. That restoration uses an
induced ten-vertex path with the hub adjacent at positions `0,3,6,9`.
Its certificate and interface contract are not adopted in the current
repository. I have no complete derivation of that restoration from the
currently adopted local lemmas.

The missing premise is explicit at note lines 321--325 and TeX lines 168--169:
a Z-run of length two must cost two units rather than the one supplied by
the current P7 Z-run lemma. This gives `b >= 2` for `t >= 2`, and cost at
least three for two runs of lengths one and two. These stronger costs are
used at note lines 367, 378, 392, 396--399 and in the corresponding TeX
case extraction. The bounded algebra checker assumes this improvement at
`check_algebra.py:64,83,118`; its PASS cannot establish it.

Adopting only the new `D <= 10` and full `<=33 distinct 5-cycles` results
does not require this missing premise. The existing degree-two exclusions
`p >= 34`, `D >= 14`, and unique-vertex `p >= 42`, `D >= 16` suffice for
both new full-class inductions. The existing two-degenerate `D <= 13`
result remains valid. The old two-degenerate `<=33 cycles` assertion is
now subsumed by the full-class result. The stronger two-degenerate
`<=37 cycles` and `D <= 15` claims should not be adopted on the present
certificate set. Unrestricted four-colour Hamiltonicity and
Hamilton-connectedness remain open.

## Checked chain and small-hub arguments

Put `H = delta + W`. Under `Q=e=0`, all faces are simple pentagons or
hexagons and all other heavy degrees are four or five. An SS hexagon
is a current regular/one-degree-four P5 reduction unless it contributes
at least two to `W`. Thus under `H <= 1` every SS face is a pentagon.
The only possible successive attachment degrees are
`44,45,54,55,53,35`.

For four consecutive S-neighbours, an internal light attachment has two
distinct degree-five attachment-neighbours; its third face costs at least
two in `W`. Otherwise the two internal attachments are heavy. Each
degree-four one has no clean angle and contributes one to `delta`.
Their shared SS face contributes zero, one or two to `W` according
as the internal pair is `44`, `45` or `55`. In each case `H >= 2`.
These charges do not double-count: the two degree-four losses occur at
distinct vertices, and the mixed-degree contribution is a face term in
`W`. The proof applies to any four consecutive S-neighbours; `t=1`
is only used to guarantee such a run.

For `s=2,t=2`, any mixed p0-pentagon gives the already adopted tailed5
configuration. Its hub has original degree four, its cycle contains one
degree-two neighbour, and the other degree-two neighbour has no second
contact with that cycle: another contact would create a triangle or
4-cycle. There is at most one ZZ angle. Thus `b <= 2`, equivalently
`p0 >= 2`, gives a mixed p0-face directly, without P10. The remaining
`kappa=1,b=3` case under `D <= 15` has light attachments and
`Q=e=H=0`; current P4/P5 reductions exclude an SS angle, so the order
alternates and its p0-face is again mixed. The archive's use of tailed5
is valid, but its preliminary stronger run bound is unnecessary here.

## Two residues left without the P10 premise

The current P7 lemma gives each isolated Z-run cost one and each run of
length `l >= 2` cost `l-1`. A total cost of one with `t >= 2` is
possible only for one run of length two. Applying these current costs,
the existing master inequality, the chain argument and the current
tailed/star reductions leaves the following uneliminated numerical cases.
They are not constructions or counterexamples.

| Quantity | Residue A | Residue B |
| --- | --- | --- |
| `s,t,b,kappa` | `3,2,1,0` | `2,3,2,1` |
| `Q,e,delta,W` | all zero | all zero |
| `D'`, hub excess, `D` | `13,2,15` | `13,2,15` |
| `p = 6+2t+2D'+Q` | `36` | `38` |
| Cyclic runs | one S-run of length three, one Z-run of length two | two S singletons and Z-runs of lengths one and two |

In A, the two SS faces are pentagons. Their three attachment degrees
must be `3,5,3`: an internal degree-four attachment would lose its
clean face, an internal light one would cost two in `W`, and a heavy
neighbour of the internal degree-five vertex would contribute to `W`.
The hub has degree five, so neither star3 nor the degree-four tailed5
model applies. There are only three consecutive S-neighbours, so the
four-attachment lemma does not apply. Here `p0=3`; all three faces
beside the length-two Z-run are p0-faces. This is exactly the missing
three-face fan. A prevents deriving `p >= 38` and also `D >= 16`
from the listed reductions.

In B, the exceptional clean centre makes both attachments light.
With `Q=W=0`, current P4/P5 reductions exclude an SS angle. The
two Z-runs therefore have lengths one and two. Current P7 costs
only `1+1=2`, consistent with `b=2`; the archive needs `1+2=3`.
Here `p0=4`, so the length-two run again has all three incident
p0-faces. B concerns the claimed `D >= 16` bound, not the
`p >= 38` bound. Additional angular restrictions might further
constrain these residues, but no such complete exclusion is supplied.

## Exact three-face fan classification

Write its faces as
`(w,u,x,a,z1,w)`, `(w,z1,b,c,z2,w)`,
`(w,z2,d,y,v,w)`. Their path order is
`p0,...,p9 = u,x,a,z1,b,c,z2,d,y,v`.
The hub contacts are `p0,p3,p6,p9`; the endpoints have original
degree two and all other path vertices have original degree three.

These ten vertices are distinct. At a common light vertex, two distinct
facial pentagons share an incident edge, and shared edges cannot be
consecutive at a degree-three vertex. For two consecutive faces, if
`r` edges were shared, their union would have `10-2r` vertices and
`10-r` edges. The planar girth-five bound forces `r=1`. The first
and third faces share the hub but no hub edge; `r` further common
edges would give `9-2r` vertices and `10-r` edges, forcing `r=0`.

Only indices `1,2,4,5,7,8` have an unused degree. Girth excludes
every possible chord except the following six. Original degree three
allows at most one chord at each such vertex.

| Chord | Induced retained-hub reduction already adopted |
| --- | --- |
| `1--5` | P7 on `0,1,5,6,7,8,9`, hub contacts at its positions `0,3,6` |
| `4--8` | P7 on `0,1,2,3,4,8,9`, hub contacts at its positions `0,3,6` |
| `1--7` | regular P5 on `0,1,7,8,9` |
| `2--8` | regular P5 on `0,1,2,8,9` |
| `1--8` | regular P4 on `0,1,8,9` |
| `2--7` | regular P6 on `0,1,2,7,8,9`, unless `1--8` already gives P4 |

The degree restrictions make the selected paths induced, with the
explicitly handled possible `1--8` chord in the P6 case. Therefore
the only genuinely missing local case is a chordless four-contact
P10. Its restoration is not established merely by this geometric
classification. Any future certificate adoption must also include
all compatible shared outside-role moves: contacts at path positions
`1,4,7`, for example, permit a triple alias. Pair-only interface
checking would be insufficient.
