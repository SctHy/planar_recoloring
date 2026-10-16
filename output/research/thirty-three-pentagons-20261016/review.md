# Thirty-three-pentagon integration review, 2026-10-16

The article adopts Hamiltonicity of R_k(G), for every k >= 4, for nonempty
finite simple planar graphs of girth at least five with D(G) <= 10 or at most
33 distinct 5-cycles. D(G) is the sum of max(deg_G(v)-3,0). This strengthens
the preceding bounds 9 and 31. The seven-heavy and block-subcubic classes
remain; the two-degenerate D(G) <= 13 class is retained. Its former 33-cycle
alternative is now subsumed by the unrestricted 33-cycle theorem.

## Analytic review

The exact hinge loss identity is

    nu_X + sigma_X + omega_X = D - 10 - 3e - 2Q - 3 beta_+.

In a minimum counterexample no hinge has a separated restorable partner, so
all three losses are nonnegative for every hinge. At D=10 they all vanish,
and e=Q=beta_+=0. The local equality proof distinguishes a duplicated new
pentagon (V >= 1) from two unusable angles (U >= 2); equality forces
p_X=9, U=0, V=1 when the special face is pentagonal. All four rotated hinges
exclude the hexagonal exception. Single-heavy faces and their degree-four
centres then propagate across every edge in the connected dual. This would
force D=6, contradicting D=10.

The proof uses only the delivered restoration lemmas and the existing
P10-free degree-two lower bounds of 34 distinct pentagons and excess 14.
Vertex deletion preserves both adopted classes, and the residual graph is
nonempty. The general thresholds h(P5) and hc(P5) remain in [4,5].
The new <=35-cycle frontier is stated only under minimum degree at least
three. Degree-two cases with 34 or 35 cycles remain unexcluded.

## Unadopted claims

The source also proposes two-degenerate graphs with <=37 distinct pentagons
or D<=15. Its stronger degree-two bounds use an induced four-contact P10
restoration, specifically to charge a length-two Z-run by two. Neither the
33 archive nor the current publication contains that literal certificate
or an independent proof of its restoration. Earlier replay logs alone do
not supply this proof input. These conclusions are therefore not adopted;
this review does not assert they are false.

For example, with only the delivered run bound, the scalar residue
s=3, t=2, b=1, Q=e=delta=W=0, D'=13, D=15, p=36 is not excluded.
Its three SS attachments may have degree pattern (3,5,3). This is a residue
of the charging argument, not a constructed counterexample. A second use
of the missing bound concerns Z-runs of lengths one and two at s=2,t=3.
See degree-two-review.md for the induced-fan classification and exact scope.

## Reproduction and limits

The original ZIP is retained byte for byte beside this review. Its SHA-256 is
baf7a1c159cff4623f7fa89681f416e0652c5a47a8785917d412cc9f463920de.
Extract it into a temporary directory and run, from its top-level directory:

    python3 -B verify.py
    python3 -B verify.py --check-manifest

Both original commands passed read-only; all 56 source files, including
reports, remained byte-identical. replay-receipt.json records the actual
commands, exit codes, timings and output hashes. The three source readers
check 129 nonexhaustive spherical fixtures (76 at D=10), 2,482 local and
2,480 global loss ledgers, 513 full centres, six locally saturated centres,
one global-rigidity instance, 18,000 scalar identities, 31 attachment words,
1,703 circular words, and 37 low-p/11 low-D tuples; eight corruptions are
rejected. The tuple extraction uses the P10-dependent run bound, so its PASS
does not close that missing dependency.

The sole global-rigidity fixture is the inherited D=6 PI graph. All 76 D=10
fixtures have separated-partner witnesses; none supplies a saturated D=10
no-partner case. These are finite regressions, not an exhaustive graph
classification or mechanical verification of the universal rigidity proof.
There are no new colouring-cycle certificates or complete recolouring-graph
enumerations in this archive.

Inherited receipts distinguish completed factor/obstruction/manifest checks
from incomplete full-suite attempts in the source continuation. The earlier
repository integration independently completed the 31 archive replay; that
separate evidence is preserved in the existing publication provenance.
The current integration reruns all 14 publication suites and 132 rejection
cases without changing certificate inputs or finite report bytes. This review
is not a Lean verification or independent human peer review.
