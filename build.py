#!/usr/bin/env python3
"""Build the article and standalone certificates with isolated intermediates."""
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parent
latexmk = shutil.which("latexmk")
if not latexmk:
    raise SystemExit("latexmk is required (with a pdfLaTeX installation).")
build = root / ".latex-build"
build.mkdir(exist_ok=True)
jobs = [
    (root, "planar_recoloring_hamilton_thresholds.tex",
     ["-outdir=.latex-build", "-out2dir=."], "article-build.log"),
    (root / "supplement", "article_certificates.tex",
     ["-outdir=../.latex-build", "-out2dir=."], "certificates-build.log"),
]
for cwd, source, options, log in jobs:
    command = [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", *options, source]
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (build / log).write_text(result.stdout)
    if result.returncode:
        raise SystemExit(f"Build failed; see {build / log}")
    print(f"Built {cwd / Path(source).with_suffix('.pdf')}")
