# Fifteen source-selector rows: separate complete manuscript candidate

The final v2 candidate compiles to 42 pages, equal to the untouched frozen main.
It replaces exactly 125 of the 283 individual nonconstant-source interface
records by fifteen source-selector rows. The partition remains
158 individual + 125 source-selector + 30 constant-source = 313 interfaces.
The other 52 marked C5 blocks, all 41 theorem statements, and the prescribed
first-normalizer paragraph remain byte exact. No font, spacing, pagebreak,
theorem, component-state, selected-cycle, or pool changes were made.

The parent-produced exact mask input is retained without rerunning it:
`union-source-cover-results.json` has SHA256
`a4285d3b846b152ac1d6ac7c34f4c25a3e57a031e73401ab8f47c15347ac9c37`.
Its input is the frozen arbitrary-two-Hamilton-cycle local result with SHA256
`36ee26c64c667dbb7bea0bc88eed3b3162c85cbae16038da3a01cd59eeca68b1`.
Each source has at most 15 interface bits and at most 20 useful word masks.
The root's exact mask DP took 0.044 seconds. Its fifteen independent minima sum
to 48 printed row members, containing 27 distinct five-digit words. This is a
sum of exact per-row minima; 27 is not asserted to be a joint global minimum.

## Mathematical compression and its scope

For a common legal state x under a non-star boundary edit j:a -> q, let d be
its full source degree and alpha indicate that a is absent from the two state
neighbour colours at j. The full source and target incident-star union has
exactly d+alpha edges: only the mutation at j to the old forbidden colour a can
be a new target edge. If d+alpha <= 3, any component Hamilton cycle on either
side takes two incident edges at x, so the two cycles must share an edge.
If no common incident edge lies in either fixed pool, that edge survives both
pool deletions. The argument applies to any two component Hamilton cycles;
it does not require those cycles to contain every pool edge.

The candidate table gives S_t and the one-coordinate allowed-list formula.
For each of the 125 nonconstant-source interfaces absent from the remaining
individual list, an S_t state is in the actual restored target component,
has d+alpha <= 3, and has no common pool incidence under the actual first
normalizer. These are specified finite cases with fixed printed pools and
components, not a classification of all C5 edits or a new uniform family.
Several rows cover only part of their source type; only 01023 and 01124 cover
every originally allowed source interface. No pool equivariance follows from
the selected states, a source stabilizer, or a shared profile.

`removed125-individual-records.json` retains every removed original tuple and
the selected frozen condition observations. Both the complete original
interface block in `frozen-main.tex` and the unchanged input results remain.
No new neighbour generation, whole graph-state enumeration, or Hamilton-cycle
search was used to create or measure this manuscript candidate.

## Literal manuscript comparison

| Metric | Frozen main | Final v2 |
|---|---:|---:|
| PDF pages | 42 | 42 |
| Individual interface records | 283 | 158 |
| Endpoint plus printed selector words | 566 | 364 |
| Endpoint plus distinct selector words | 566 | 343 |
| Raw TeX bytes | 140978 | 138466 |
| Raw TeX ASCII letter tokens | 19206 | 19419 |
| Raw TeX whitespace tokens | 20039 | 19571 |
| PDF ASCII letter tokens | 16176 | 16359 |
| PDF whitespace tokens | 22017 | 21605 |
| PDF characters | 120476 | 117911 |

Thus the explicit word payload and total text size decrease while the prose
letter-token count increases by 183 in the rendered PDF. This is a premise
compression, not a claim that every text metric is smaller.

Final v2 TeX SHA256:
`ecea0571029a8527630442b2242bc21ec76f67bc44b2f768b9228c5f494203a9`.
Final v2 PDF SHA256:
`2ffabb849349d9e17a6dce740e1f22716b04d2167dd87fa742f5c8d2736ad6f5`.
The main remains SHA256
`3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58`.

The final source differs from v1 only by defining the 125-case complement
explicitly and stating the non-star edit scope. The intermediate v2 before
the non-star wording is preserved with its PDF, log, script, and result in
`v2-pre-nonstar/`, bound by its manifest. V1 remains byte exact.

## Verification and delivery boundary

Both full candidates compiled with latexmk without overfull, underfull,
undefined-reference, or LaTeX/package warning matches. Final v2 pages 40-42
were rendered at 110 dpi and visually inspected: the entire selector table
and its argument occupy page 40, the remaining records span pages 41-42,
and references follow without clipping, overlap, or a blank spill page.
`manuscript-pdf-comparison-v2.json` records literal pdfinfo/pdftotext metrics.

The computation record binds exact inputs, code, results, candidates and QA
on actual Python 3.14.6. Schema/hash validation establishes record integrity,
not mathematical sufficiency. The generic local argument was separately
reviewed by the root. An independent actual-source reader is checking all
125 component, normalizer and pool cases; its own report is separate and is
not supplied by this author's PASS output. At this record's creation the
candidate remains reviewable and unadopted; the live main has not been edited.
