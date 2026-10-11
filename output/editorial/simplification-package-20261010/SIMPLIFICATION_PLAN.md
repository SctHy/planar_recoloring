# Proof simplification plan

This note accompanies `planar_recoloring_hamilton_thresholds.tex`. It distinguishes
structural simplifications (which shorten the proof itself) from certificate
compression (which changes where finite data are stored).

## Recommended architecture

Keep the arbitrary-order inductions and their fibre-lifting lemmas in the main
paper. Replace the long literal tables by three compact local lemmas:

1. **Adjacent-pair exit lemma.** For
   \[
   F(A,B)=\{(a,b)\in A\times B:a\ne b\},
   \]
   with list sizes 3 or 4, prove only the one-interface property used by
   `Adjacent-pair interfaces and reset`: from every entrance state there is a
   Hamilton path to a state in the common interface. The `44` fibre is retained
   as Hamilton-connected. This is weaker than listing all feasible endpoint
   pairs. A seven-type verifier (or seven short staircase cycles plus a local
   endpoint argument) is enough; the 53 endpoint words and count table are not
   needed in the main text.

2. **(2,3,2) strip lemma.** Build the good-boundary cycles from fixed-middle
   layers (products of paths/complete graphs) and two ordinary square switches.
   The bad constant run is already handled for arbitrary length by the strip
   proposition. The three 14/17/16-state literal cycles and the seven-row
   capacity table can therefore be replaced by a layer construction and a
   small safe-edge lemma. If one transition check remains finite, put it in a
   machine-readable supplement rather than a printed table.

3. **Protected pentagon lemma.** The protected-edge condition is genuinely
   stronger than “each local fibre is Hamiltonian”: the same protected edge
   must survive in every physical row and across every one-coordinate boundary
   change. Do not simply delete this certificate. Compress it into a canonical
   verifier: enumerate the 2304 labelled boundaries, canonicalize by the
   dihedral/color action, construct each local seed, and check the protected
   intersection condition. The main paper states the finite lemma and gives the
   canonicalization/verification algorithm; the words, pools and 47 exceptional
   records live in a supplementary file.

## What cannot be claimed without new mathematics

Moving a table to a script is a presentation change, not a new non-computational
proof. The general protected-pentagon statement and the exceptional `332/333`
interface behavior still need either (a) a proof of the compact local lemmas, or
(b) an explicit, reproducible finite certificate. Deleting both the table and
its verifier would leave a gap.

## Expected effect

The main PDF can lose the three large certificate appendices and the summary of
literal words. The proof becomes a sequence of structural lemmas followed by
one short “finite kernel certificate” paragraph. The supplement remains fully
reproducible and can regenerate every local path/cycle and every exceptional
interface record.
