# Stored raw-count summary

The four/two-pool candidate has 254 of the 283 nonconstant-source interfaces satisfying the elementary sufficient condition

\[
|E_A\cap g^{-1}E_B|>|\mathrm{pool}_A|+|\mathrm{pool}_B|.
\]

Here an ordinary component uses its fixed cycle support and a hard component uses its fixed printed common-port support. The conclusion is a protected common edge: deleting the two pools removes at most their summed cardinality. These statistics were read from the existing exact JSON result; no graph, normalization, or interface kernel was regenerated.

| Interface type | Cases | Observed minimum raw edges | Required count | Qualified | Residual |
|---|---:|---:|---:|---:|---:|
| Ordinary cycle to ordinary cycle | 98 | 9 | 9 | 98 | 0 |
| Starred cycle to starred cycle | 132 | 12 | 9 | 132 | 0 |
| Hard to ordinary cycle | 24 | 4 | 7 | 13 | 11 |
| Ordinary cycle to hard | 22 | 3 | 7 | 10 | 12 |
| Hard to hard | 5 | 2 | 5 | 1 | 4 |
| Hard to a constant component | 2 | 3 | 8 | 0 | 2 |

Thus all 230 cycle/cycle interfaces pass, and the 29 residual cases are exactly 23 one-hard, four hard/hard, and two hard/constant cases. Every residual still has a valid individual protected witness; failure of this sufficient count does not mean failure of the interface. The full 29 records, with original zero-based record IDs, source/target types, position, changed colour, raw count, and required count, are in [summary.json](summary.json). The sole qualifying hard/hard case has six raw edges.

This provides a possible next research direction, not a shorter analytic proof. In particular, the fixed observations `ordinary/ordinary >= 9` and `starred/starred >= 12` do not yet follow from a uniform layer or template argument. Replacing 230 edge records by an unproved minimum assertion would merely hide a finite check. A useful replacement would derive a count of nine from the structure of every actual restored cycle pair. The analogous universal seven-edge and five-edge assertions for the hard cases are false for the current fixed supports, as the minima in the table show.

The statistics use the old hard supports of cardinality 19 and 18, ordinary four-edge pools, hard two-edge pools, and the previously validated constant five-edge pools. They do not substitute the proposed 00112 support of cardinality 13. The 230 cycle/cycle observations remain applicable because those supports are unchanged; the 254 total must not be claimed for the new thirteen-port version without a separate check or deduction. Neither this report nor its summary changes the manuscript, pools, seeds, or formal research archive.
