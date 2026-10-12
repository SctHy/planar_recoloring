# Project Collaboration Conventions

This file applies to this repository and all of its subdirectories. Use English by
default, complete requested edits, the corresponding verification, and Git commits;
keep the mathematical statements accurate and keep additions concise.

## File entry points

- Main article: `main.tex` / `.pdf`.
- Standalone finite-certificate supplement: `supplement/article_certificates.tex` /
  `.pdf`; certificate format and reproduction instructions are in
  `supplement/README.md`.
- Submission directory: `output/publication/`; archive: `output/publication.zip`.
  They contain the article, supplement, checkers, reports, and `manifest.json`.
- Research candidates and editorial records: `output/research/`, `output/editorial/`.
- Historical full manuscript: `supplement/planar_recoloring_hamilton_thresholds_full.tex`.
  Preserve the historical manuscript, original certificates, and pre-edit backups;
  do not use them as direct overwrite targets for the current article.
- Project overview: `README.md`; Git instructions: `GIT_GUIDE.md`.

## Automatic Git for every modification

The user requires automatic Git for every modification. After each logical change is
complete and passes its applicable checks, stage the related files and create a local
commit without asking again. This applies to article, PDF, script, report, submission
bundle, and documentation changes; even an `AGENTS.md`-only change must be committed.

1. At the start, run `git status --short` to inspect existing changes and distinguish
   them from the work in this task.
2. After editing and running the necessary checks, run `git diff --check`.
3. Add explicit files or directories, inspect `git diff --cached`, and stage only this
   task's work and existing changes the user explicitly requested to include.
4. Run `git commit -m "Briefly describe the changes"`. Combine continuous edits and
   fixes for one task into one meaningful commit; independent changes may use separate
   commits.
5. Check the status after committing. In the final response, briefly give the commit
   identifier, changed files, and verification results.

Automatic Git means local staging and committing by default. Push to a remote only when
the user has authorized it for the current task or on an ongoing basis; reuse existing
push authorization without asking again. If a commit or push fails, preserve the edits
and report the actual error; do not claim success, change global Git configuration,
force-push, or rewrite history. Do not create an empty commit. If a required check
fails, fix it first; if the task remains incomplete, state the remaining issue rather
than substituting a commit for verification.

## Article and mathematical boundaries

- Keep analytic proofs, finite computational evidence, candidate conclusions, and open
  problems distinct; a successful compilation does not establish mathematical
  correctness, and self-checking is not independent review.
- When editing a theorem or proof, check its assumptions, quantifiers, definitions,
  and dependencies. Put short counterexamples near the relevant theorem or proof,
  preferably as a compact remark, and avoid repetition.
- The four-colour Hamiltonian and Hamilton-connected problems for general planar
  girth-five graphs remain open: `4 <= h(P_5) <= 5` and `4 <= hc(P_5) <= 5`. Changing
  this boundary requires a new complete proof.
- A vertex-pancyclic conclusion for degenerate graphs cannot be uniformly strengthened
  to edge-pancyclicity. Existing Remark 2.7 uses the star `K_{1,k-2}` for `k >= 4`:
  colour the leaves with `3,...,k`, and switch the centre between colours `1,2`.
  The recolouring edge is in no triangle. Do not rewrite this as a claim that no graph
  is edge-pancyclic.
- Preserve certificates and generated results byte for byte. When updating reports,
  retain useful original results and state the scope of the current check; reuse an
  existing verification only when the inputs and checker are unchanged and the scope
  still applies.

## Verification and compilation

Run the following from the repository root:

```sh
python3 supplement/verify_all.py
pdflatex main.tex
pdflatex main.tex
cd supplement
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

The Python checkers use only the standard library and require Python 3.10 or later;
compile directly with pdfLaTeX. Compile each document twice to resolve cross-references,
using the default output location; PDFs and auxiliary files remain beside their sources,
and auxiliary files are ignored by Git. Do not use a custom compilation program.

- For changes only to article text or layout, recompile the article, inspect the final
  log for warnings, undefined references, and overfull/underfull boxes, then render and
  inspect the affected PDF pages.
- For changes to certificates, checkers, or finite constructions, run the corresponding
  verification; if a cross-construction interface is affected, run the complete
  `supplement/verify_all.py`. Do not repeat unchanged checks for a text-only edit.
- For changes only to collaboration documentation, check the content and run
  `git diff --check`; recompiling the article is unnecessary.
- Check new counterexamples and proofs directly; do not use layout inspection as a
  substitute for mathematical checking.

## Synchronizing submission files

After changing the current article, supplement, or their checkers, synchronize the
corresponding files and applicable reports and hash manifest in `output/publication/`,
then update `output/publication.zip`. Changes only to collaboration documentation do
not require rebuilding the article bundle.

- Keep the repository and submission versions of the article and supplement identical;
  independently compile affected documents in the submission directory and inspect the
  resulting PDFs.
- When updating generated reports, state the scope of the current verification and any
  reused evidence, retaining necessary older results.
- Artifact hashes in `computation-record.json` must match the delivered files.
- `manifest.json` lists the size and SHA-256 of every delivered file; it does not list
  itself.
- Put delivered files directly in the ZIP without an extra top-level directory; check
  every ZIP entry against the manifest. Do not include LaTeX auxiliary files,
  `.latex-build/`, Python caches, or temporary renders.
- Update change descriptions, page counts, theorem numbers, and build status from the
  latest artifacts; do not copy them from historical records.

## File protection

Preserve article sources, original certificates, necessary research evidence, and
historical backups. Clean up only explicitly identified temporary or generated files;
inspect references and dependencies first. Do not treat all of `output/` as disposable
cache.
