# Two complete source families: exact masks and separate manuscript candidates

The exact minimum covers have six source words for01023 and three for01124.
Their common word32301 is printed once as w, leaving **eight distinct words**.
The global frozen-mask problem also has a unique eight-word optimum. These words
replace27 individual interface witnesses in the separate candidate, giving
256 individual records +27 cases in two source families +30 cases in the existing
six constant-source families =313 cases. The live main is untouched.

| Source | Cases | Candidate words | Minimum row members | Selected words |
| --- | ---: | ---: | ---: | --- |
| 01023 | 15 | 8 | 6 | 12310,23101,23201,23210,32301,32310 |
| 01124 | 12 | 7 | 3 | 12303,23031,32301 |

`find_cover.py` reads only the frozen positive local certificates, whose input
SHA-256 is36ee26c64c667dbb7bea0bc88eed3b3162c85cbae16038da3a01cd59eeca68b1.
It retains each word's interface bitmask and checks all256 and128 word subsets.
The cardinality tables have zero covers below6 and3 respectively, with one
minimum cover each. `find_global_cover.py` checks all4096 subsets of the twelve
distinct candidate words and finds one global minimum cover of size8. The first
global invocation had an incorrect fourteen-word input-count estimate; its
diagnostic is retained. This did not change the per-family results. No neighbour
generation, graph-state enumeration or Hamilton search is performed in this branch.

## General cancellation and specialized short mechanism

For a common legal state x under a single non-star boundary edit j:a→q, set
alpha=1 when a is absent from the two state-neighbour colours, and beta=1 when
changing x_j to q is a source-legal mutation. The target incident star loses that
mutation if beta=1 and gains the mutation to a if alpha=1. All other mutations
are unchanged. Consequently

`d_target=d_source+alpha-beta`, `d_common=d_source-beta`.

The shared safe incident universe excludes the source/target pool union and has
size `d_common-f`. The arbitrary-two-cycle incident inclusion-exclusion bound
therefore simplifies exactly to `max(0,4-d_source-alpha-f)`. Independently written
`check_cancellation.py` compares these identities with all10379 frozen original
candidate observations, without reconstructing neighbour sets. They all agree.

Every chosen one of the27 selectors satisfies d_source+alpha=3 and f=0. Thus the
candidate uses a shorter specialized argument: the union of the two full incident
stars has exactly three edges, since a mutation to the old forbidden colour is
the only possible target-new mutation. Each Hamilton cycle chooses two incident
edges, so two two-element subsets of that three-edge union meet. The intersection
edge lies in the common incident star, whose pool incidence f is zero, and is
therefore outside both fixed pools. The argument does **not** require the full
incident union to avoid the pools or require either arbitrary cycle to contain
every pool edge. The selected27 union identities are separately extracted from
the frozen actual neighbour lists in `selected27-union-results.json`.

For01023 all six selected words have degree3. Their useful coordinate sets
J={j:t_j is one of the two state-neighbour colours} are respectively01,12,23,03,
24,04 in the selected-word order above. For01124,12303 has degree3 and J={1};
23031 and32301 have degree2 and J=empty. These are source degrees. Pool incidence
is still checked with each original interface's actual first-normalized target
pool; equal profiles or source symmetries are not used to infer pool transport.

The saved mask coverage map binds all27 original interface identities, components
and prescribed restoration maps. The minimum claim applies to the frozen mask
problem and these two complete normalized source cases, not to arbitrary C5
families, arbitrary pools or another proof method.

## Candidate history, scope and actual length

The original main TeX SHA-256 is
3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58 and its PDF has42pages.
V1 adds a numbered general lemma and long source-family discussion; it compiles
to44pages. Its prose retains an obsolete283-record verification sentence and
uses an ambiguous ordinary-component restriction that conflicts with the starred
source01124 terminology. It is preserved as a method/prose tradeoff, not accepted.
V2 removes the numbered main lemma, fixes those two prose issues, and puts the
closed bound in the appendix; it compiles to43pages. V3 uses the specialized
three-edge union argument and also compiles to43pages. No fonts, spacing or
explicit page breaks were changed to force a page count.

| Artifact | Pages | PDF ASCII-letter tokens | PDF whitespace tokens |
| --- | ---: | ---: | ---: |
| Original main | 42 | 16176 | 22017 |
| V1 | 44 | 16534 | 22325 |
| V2 | 43 | 16394 | 22161 |
| V3 | 43 | 16363 | 22102 |

PDF token counts use pdftotext and the exact definition in `measure_pdf.py`.
V3 raw TeX is141446bytes versus140978, with19418 versus19206 ASCII-letter tokens
and20079 versus20039 whitespace tokens. The entire TeX's five-digit-token count
falls from3211 to3106. Counting the individual-interface endpoint words plus the
new eight shared anchor words gives566→520, a reduction of46 case-evidence words;
all unchanged component-cycle and pool input is omitted equally from that count.
Thus this branch reduces explicit finite witness input and adds a short analytic
mechanism, while total prose and page count grow. It is a separate43-page
candidate and is **not adopted into the42-page main**.

V3 TeX SHA-256:
505c432f4a18a36056f50f5ba1a56ac4513ca02aa64520580d4de64b3dfff62f.
V3 PDF SHA-256:
34241fb470e6ea3d13b5db3c0e7fd5f4d38b159abd1606d02fd4f3ab29fb80f6.

All candidates keep the other52 marked C5 blocks byte exact. Only the candidate
INTERFACES-ALL block loses exactly27 now-unused records; the original283-record
block remains in frozen-main.tex. The theorem/state space, source bases, pools,
component coverage, normalizer paragraph and arbitrary-vertex/endpoint conventions
are unchanged. V2/V3 synchronize the protected proof and verification note to
256+27+30. The rendered changed pages and end pages are retained; visual inspection
found no clipping, overlapping text, unreadable tables or missing symbols.
All three final compile logs have no overfull, underfull, reference or package warnings.

## Evidence limits

The cancellation and three-edge intersection implications are analytic proofs.
Mask minima, selector legality/pool observations and token counts are exact finite
checks on frozen evidence. They do not complete the global girth-five recolouring
program or create a new uniform C5 classification. Actual source/pool independent
review is performed separately; this branch's schema/hash validator cannot confer
independent mathematical review. Only the specified cycles and seeds are used
by the original protected-product pipeline, where the retained pools have their
original splicing role. The stronger local arbitrary-two-cycle statement is used
solely to prove the protected intersection identities for these source families.
