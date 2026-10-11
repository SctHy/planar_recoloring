from pathlib import Path
import re

root = Path.cwd()
work = Path(".latex-build/proof-layout-review-directory.txt").read_text().strip()
work = Path(work)
article = root / "planar_recoloring_hamilton_thresholds.tex"
supplement = root / "supplement/article_certificates.tex"
main = article.read_text()
old = r"Hamilton-connected lower bound, the subgraph $\R_3(K_2)=C_6$"
assert main.count(old) == 1
main = main.replace(old, r"Hamilton-connected lower bound, $\R_3(K_2)=C_6$")
assert main.count(r"\Needspace{24\baselineskip}") == 1
main = main.replace(r"\Needspace{24\baselineskip}", r"\Needspace{20\baselineskip}")

text = supplement.read_text()
original = text


def replace_region(start, stop, replacement):
    global text
    assert text.count(start) == text.count(stop) == 1
    a = text.index(start)
    b = text.index(stop, a)
    text = text[:a] + replacement + text[b:]


replace_region("The files ", r"\appendix", r"""Run \texttt{python3 verify\_all.py} to check the certificates and rejection
of corrupted data. The exact verifiers require only the Python standard
library; \texttt{README.md} gives their input contract and build commands.
""")
a = text.index("These certificates use ")
b = text.index(r"\begin{table}", a)
text = text[:a] + r"""For the article's fibre $F(A,B)$, write $ab$ for $(a,b)$ and use type
$(|A|,|B|,|A\cap B|)$. Each endpoint word visits every state once;
successive states differ in one coordinate. Table~\ref{tab:pair-five-counts}
includes list-preserving colour permutations, allowable coordinate
exchange and path reversal. Exact subset dynamic programming checks
all feasible and excluded endpoint pairs.

""" + text[b:]
replace_region("The three-digit type records ", "% BEGIN PAIR-CYCLES", r"""The columns give the type, lists separated by a slash, and one cyclic
word. Its list-preserving symmetry orbit, including allowable coordinate
exchange, covers every edge.
""")
text = text.replace(r"\paragraph{The 53 endpoint words.}",
                    r"\Needspace{10\baselineskip}" + "\n"
                    + r"\paragraph{The 53 endpoint words.}", 1)
pattern = re.compile(r"(\\noindent For \$\d{3}\$:.*?\\end\{verbatim\})", re.S)
text, n = pattern.subn(lambda m: r"\begin{minipage}{\linewidth}" + "\n"
                      + m[0] + "\n" + r"\end{minipage}\par\medskip", text)
assert n == 7
text = text.replace("% END POOL-00000-1\n", r"""% END POOL-00000-1
\begingroup
\setlength{\columnsep}{14pt}
\renewcommand{\paragraph}[1]{\par\addvspace{1ex}\noindent
  {\normalfont\small\bfseries #1}\par\nobreak}
\renewenvironment{flushleft}{\par\raggedright}{\par}
\begin{multicols}{2}
""", 1)
text = text.replace("% END POOL-01234-0\n", r"""% END POOL-01234-0
\end{multicols}
\endgroup
""", 1)
blocks = re.compile(r"^% BEGIN ([^\n]+)\n(.*?)^% END \1\s*$", re.M | re.S)
assert dict(blocks.findall(original)) == dict(blocks.findall(text))
words = re.compile(r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", re.S)
assert words.findall(original) == words.findall(text)
article.write_text(main)
supplement.write_text(text)

script_path = work / "simplify_manuscript.py"
script = script_path.read_text()
a = script.index('replace_between(\n    r"\\begin{theorem}\\label{thm:main-planar}"')
b = script.index("# The end marker", a)
script_path.write_text(script[:a] + script[b:])
print("Refined bibliography flow, grouped endpoint types and two-column pools.")
