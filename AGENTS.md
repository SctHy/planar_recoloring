# Agent instructions

These rules apply to the whole repository. Write repository files in English. Finish
every requested edit with its verification and a local Git commit. Keep mathematics
accurate and additions concise.

## Layout

- `main.tex` / `main.pdf`: the article.
- `Codes/`: certificate source, `article_certificates.tex` / `.pdf`, literal data,
  and the `verify_*.py` readers. Reader output is temporary and is not committed.
- The Lean formalization is maintained outside this repository.
- Older manuscripts, editorial backups and superseded research live only in Git history;
  recover them with `git show <commit>:<path>`.

## Git

1. Start with `git status --short` and keep unrelated or untracked work out of commits.
2. After the checks pass, run `git diff --check`, stage explicit paths, and review
   `git diff --cached`.
3. Commit with a short descriptive message: one commit per logical change, never an
   empty commit.
4. In the final reply, give the commit id, the changed files and the checks run.

Commit locally without asking. Push only with authorization for the task or standing
authorization. Never force-push, rewrite history or change global Git configuration. If
a commit fails, keep the edits and report the error.

## Mathematics

- Keep analytic proofs, finite computational evidence, candidate results and open
  problems distinct. Compilation and self-checks are neither proofs nor independent
  review.
- When editing a statement or proof, check hypotheses, quantifiers, definitions and
  dependencies. Put short counterexamples next to the relevant result, preferably as a
  compact remark.
- `4 <= h(P_5) <= 5` and `4 <= hc(P_5) <= 5` stay open unless a complete new proof is
  supplied.
- Remark 2.7 (the star `K_{1,k-2}`, `k >= 4`) shows that vertex-pancyclicity cannot be
  uniformly strengthened to edge-pancyclicity. Do not turn it into a claim that no
  recolouring graph is edge-pancyclic.
- Two-pentagon restoration (Lemma 5.14, Claim 3) propagates restoration maps along a
  bottom Hamilton path; canonical per-boundary maps are insufficient (`00002 -> 00003`).
- Change certificate data only together with a rerun of the readers. Generated reader
  output must state its scope when retained outside the repository.

## Checks

Run from the repository root (Python 3.10+, standard library only; pdfLaTeX directly,
default output location, each document compiled twice):

```sh
python3 Codes/verify_all.py --write-reports \
  --report-dir /tmp/planar-recoloring-reports
pdflatex main.tex
pdflatex main.tex
cd Codes
pdflatex article_certificates.tex
pdflatex article_certificates.tex
```

- Article text or layout: compile twice. The final log must have no warnings, undefined
  references or overfull/underfull boxes. Render and inspect the changed pages.
- Certificates, readers or finite constructions: run `verify_all.py --write-reports`
  with a temporary report directory and explain the scope of the generated output.
- Documentation only: proofread and run `git diff --check`.

## Files

Delete only files the task identifies, after checking references. Generated caches
(`__pycache__`, LaTeX auxiliary files, `.DS_Store`) may be removed at any time.
