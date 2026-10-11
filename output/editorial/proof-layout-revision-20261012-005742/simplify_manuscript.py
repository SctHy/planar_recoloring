from pathlib import Path
import difflib
import re

root = Path.cwd()
work = root / "output/editorial/proof-layout-revision-20261012-005742"
article = root / "planar_recoloring_hamilton_thresholds.tex"
supplement = root / "supplement/article_certificates.tex"
text = article.read_text()
original = text


def replace_once(old, new):
    global text
    assert text.count(old) == 1, old[:100]
    text = text.replace(old, new, 1)


def replace_between(start, stop, new):
    global text
    assert text.count(start) == text.count(stop) == 1
    a = text.index(start)
    b = text.index(stop, a)
    text = text[:a] + new + text[b:]


# The end marker occurs elsewhere too: isolate this theorem explicitly.
a = text.index(r"\begin{theorem}\label{thm:main-planar}")
b = text.index(r"\end{theorem}", a)
text = text[:a] + r"""\begin{theorem}\label{thm:main-planar}
The common thresholds $h=\hc$ are $7$ for $\mathcal P$,
$5$ for $\mathcal T$ and $\mathcal B$, and $4$ for
$\mathcal P_6$ and $\mathcal F$.
""" + text[b:]
replace_once(
    "what the accompanying verifiers check. The finite data supply local\n"
    "lemmas; the inductions and restoration arguments in the article give\n"
    "the conclusions for graphs of arbitrary order.",
    "what the accompanying verifiers check. The data certify local lemmas;\n"
    "the article supplies the arbitrary-order restoration arguments and\n"
    "inductions.",
)
replace_once(
    r"""Set $x_{-1}=a$ and $x_t=b$. Choose $x_0,\ldots,x_{j-1}$ in this
order, each time avoiding the preceding colour. Then choose
$x_{t-1},\ldots,x_{j+1}$ in this order, each time avoiding the following
colour. Each of these choices excludes at most one colour from a list of
size at least two. Finally choose
\[
x_j\in S_j\setminus\{x_{j-1},x_{j+1}\}.
\]
At most two colours are excluded, so this choice is possible. The
boundary assignments $x_{-1}=a$ and $x_t=b$ also cover $j=0$,
$j=t-1$, and $t=1$.""",
    r"""Set $x_{-1}=a$ and $x_t=b$. Choose $x_0,\ldots,x_{j-1}$ forwards,
avoiding the preceding colour, and $x_{t-1},\ldots,x_{j+1}$
backwards, avoiding the following colour. Each choice excludes only
one colour. Finally choose $x_j\in S_j\setminus\{x_{j-1},x_{j+1}\}$,
which is possible since $|S_j|\ge3$. The boundary assignments also
cover $j=0$, $j=t-1$, and $t=1$.""",
)
replace_once(
    r"""The sets $F_f$ partition $V(\Rk(G))$ into cliques. If
$f,g$ are adjacent base colourings, then""",
    r"""The sets $F_f$ partition $V(\Rk(G))$ into cliques. Whenever
$k\ge d+3$, adjacent base colourings $f,g$ satisfy""",
)
replace_once(
    "We use this notation in both following proofs.",
    "We use these fibres throughout the single-vertex lifts.",
)
replace_between(
    r"\begin{theorem}[Degenerate Hamilton-connectedness]",
    r"\begin{theorem}[Degenerate vertex-pancyclicity]",
    r"""\begin{lemma}[Single-vertex endpoint lift]\label{lem:clique-endpoints}
Let $H=G-v\ne\varnothing$ and $k\ge d_G(v)+3$.
Suppose $Y=\Rk(H)$ is nonempty and Hamilton-connected, and $v$ has
a nonneighbour in $H$. If for every $f\in V(Y)$ and $c\in L(f)$
there is a neighbour $g$ of $f$ with $c\in L(g)$, then
$\Rk(G)$ is Hamilton-connected.
\end{lemma}
\begin{proof}
Fix a nonneighbour $w$ of $v$. Colour permutations give all $k$
colours at $w$ among the states of $Y$; deleting at most one state
leaves at least $k-1\ge2$ colours. Thus every base path missing at
most one state contains a move at $w$. Its consecutive intersections
$S_i=L(f_i)\cap L(f_{i+1})$ have size at least two, and the move at
$w$ supplies one of size at least three.
Lemma~\ref{lem:bridge-colours} now gives bridge colours avoiding any
prescribed first and last colours, with distinct entrance and exit
colours in every clique. Hamilton paths inside the cliques concatenate
to a spanning path through those fibres with the prescribed endpoints.

Now prescribe distinct endpoints $\alpha(a)$ and $\beta(b)$ in
$\Rk(G)$. If $\alpha\ne\beta$, lift a Hamilton path in $Y$ between
their restrictions.

If $\alpha=\beta$, choose $c\in L(\alpha)\setminus\{a,b\}$ and
a neighbour $g$ preserving $c$. Since $|V(Y)|\ge k\ge3$, closing
a Hamilton path between the ends of $\alpha g$ gives a Hamilton
cycle through that edge. Let $h$ be its other neighbour of $\alpha$
and choose $q\in(L(\alpha)\cap L(h))\setminus\{c\}$.
If $q=a$, exchange $a,b$ and reverse the final path; thus assume
$q\ne a$.

Partition $F_\alpha$ into paths
$P:\alpha(a)\leadsto\alpha(c)$ and
$P':\alpha(q)\leadsto\alpha(b)$.
Use a singleton for $P'$ if $q=b$, and its endpoint edge otherwise;
put all remaining vertices in $P$. Deleting $\alpha$ from the chosen
base cycle leaves a path missing only that state. Lift it from $g(c)$
to $h(q)$ through all other fibres. The cross edges at $c,q$ join
this lifted path to $P,P'$, giving the prescribed spanning path.
\end{proof}

\begin{theorem}[Degenerate Hamilton-connectedness]\label{thm:degenerate-hc}
Let $G$ be a nonempty $d$-degenerate graph and $k\ge d+3$.
Then $\Rk(G)$ is Hamilton-connected.
\end{theorem}
\begin{proof}
Induct on $n=|V(G)|$, starting with $\Rk(K_1)=K_k$.
If $G=K_n$, then $\Rk(G)$ is the arrangement graph $A_{k,n}$.
Since $k\ge n+2$, it is Hamilton-connected
by~\cite[Theorem~1]{HLTH04}.

Otherwise a minimum-degree vertex $v$ has degree at most $d$ and
a nonneighbour. Put $H=G-v$; induction makes $\Rk(H)$
Hamilton-connected. For each base colouring $f$ and $c\in L(f)$,
choose a vertex of degree at most $d$ in $H$. It has at least three
available colours, so can be recoloured avoiding its present colour
and $c$. This base move preserves $c$ at $v$.
Lemma~\ref{lem:clique-endpoints} applies.
\end{proof}

""",
)
replace_once(
    r"""\begin{corollary}
\label{cor:degenerate-hamiltonian}
Every nonempty $d$-degenerate graph has a Hamiltonian $\Rk(G)$ for $k\ge d+3$; it is Hamilton-connected and vertex-pancyclic in the same range.
\end{corollary}""",
    "",
)
replace_between(
    r"\begin{lemma}[Single-vertex Hamilton-connected lift]",
    "A Hamilton-connected graph of order at least four",
    r"""\begin{lemma}[State-degree criterion]\label{lem:single-hc}
Let $H=G-v\ne\varnothing$ and $k\ge\max\{4,d_G(v)+3\}$.
If $v$ has a nonneighbour, $\Rk(H)$ is Hamilton-connected, and
$\delta(\Rk(H))>d_G(v)$, then $\Rk(G)$ is Hamilton-connected.
\end{lemma}
\begin{proof}
For each base colouring $f$ and $c\in L(f)$, at most $d_G(v)$
moves make $c$ unavailable at $v$: only a neighbour of $v$
recoloured to $c$ can do so. The state-degree bound therefore
supplies a neighbour preserving $c$.
Apply Lemma~\ref{lem:clique-endpoints}.
\end{proof}

""",
)
replace_once(
    r"""It remains to check the interface exit.  If neither list changes,
take a row or column neighbour of $p$. If a $3$-list $A$ changes to
another $3$-list $A'$ and $A_0=A\cap A'$, then $|A_0|=2$: for $p=(a,b)$ choose
$(a,d)$ with $d\in B\setminus\{a,b\}$ when $a\in A_0$, and choose
$(c,b)$ with $c\in A_0\setminus\{b\}$ otherwise.  The other
one-list change is symmetric. If $A$ and $A'$ have sizes three and
four, one containing the other, put $A_0=A\cap A'$. Then $|A_0|=3$.
When $a\in A_0$, choose $(a,d)$ with $d\in B\setminus\{a,b\}$;
otherwise choose $(c,b)$ with $c\in A_0\setminus\{b\}$. The change
in $B$ is symmetric. In every case the selected edge lies
on a Hamilton cycle, so deleting it gives the required Hamilton path.""",
    r"""For the interface exit, exchange coordinates if needed so that
$B$ is unchanged, and put $A_0=A\cap A'$. All allowed transitions,
including the unchanged case, give $|A_0|\ge2$ and $|B|\ge3$.
For $p=(a,b)$ with $a\in A_0$, choose $(a,d)$ with
$d\in B\setminus\{a,b\}$; otherwise choose $(c,b)$ with
$c\in A_0\setminus\{b\}$. Either choice is a neighbour in $J$.
Deleting this edge from a Hamilton cycle gives the required
$p$--$q$ Hamilton path.""",
)
replace_once(
    "six antipodal vertex pairs of the icosahedron with six different\ncolours.",
    "six antipodal vertex pairs of the icosahedron with six different\n"
    "colours~\\cite{BP16}.",
)
replace_between(
    "The results in this section are Hamiltonian results.",
    r"\begin{lemma}[Subdivided-star lift]",
    r"""The reductions below splice Hamilton cycles and establish
Hamiltonicity at four colours. They do not prescribe arbitrary
endpoints, so the Hamilton-connected thresholds of these subclasses
remain in $[4,5]$. Supplementary Appendices~B--D supply their local
certificates.

\subsection{Graphs with few five-cycles}
""",
)
replace_once(
    r"\begin{lemma}[Adjacent degree-two restoration]",
    r"\subsection{Local degree-two reductions}" + "\n"
    + r"\begin{lemma}[Adjacent degree-two restoration]",
)
replace_once(r"\subsection{Two degree-two reductions}" + "\n", "")
headings = {
    r"\subsection{Good cycles with safe connecting edges}":
        r"\paragraph{Good fibres and safe edges.}",
    r"\subsection{A bad block with prescribed safe edges left intact}":
        r"\paragraph{Bad blocks.}",
    r"\subsection{The complete path-lifting induction}":
        r"\paragraph{Restoration over a base cycle.}",
    r"\subsection{The finite protected-edge identities}":
        r"\paragraph{Local certificates.}",
    r"\subsection{Products retaining protection in every row}":
        r"\paragraph{Products and overlaps.}",
    r"\subsection{An arbitrary bottom cycle}":
        r"\paragraph{Restoration over a base cycle.}",
    r"\subsection{The planar structural reduction}":
        r"\subsection{Two separated five-faces}",
    r"\subsection{Induction, checks and the remaining frontier}":
        r"\paragraph{Completing the subcubic induction.}",
}
for old, new in headings.items():
    replace_once(old, new)
replace_once(
    r"\begin{theorem}\label{thm:subcubic}",
    r"\subsection{Protected pentagon restoration}" + "\n"
    + r"\begin{theorem}\label{thm:subcubic}",
)
replace_once(
    "The frozen $012012$ colouring of $C_6$ gives the Hamiltonian\n"
    "threshold lower bound four. No monotonicity in $k$ is presumed.",
    "The frozen $012012$ colouring of $C_6$ gives the Hamiltonian\n"
    "threshold lower bound four.",
)
replace_once(
    "four. No monotonicity in the number of colours has been assumed.",
    "four.",
)
replace_between(
    r"\section{Sharpness and the unresolved frontier}",
    r"\section{Finite certificates and reproducibility}",
    r"""\section{The girth-five frontier}\label{sec:sharpness}

The threshold intervals in Table~\ref{tab:thresholds} leave two
questions: does every $G\in\mathcal P_5$ have a Hamiltonian
$\R_4(G)$, and is every such recolouring graph Hamilton-connected?
The latter question also remains open for the four-colour subclasses
of Theorem~\ref{thm:main-four}. Known connectivity~\cite{BBFHMP23}
does not settle either question. Theorem~\ref{lem:block-subcubic}
shows that a minimum Hamiltonian counterexample must contain a block
with internal maximum degree at least four.

""",
)
replace_once(
    r"\clearpage" + "\n" + r"\begin{thebibliography}",
    r"\Needspace{24\baselineskip}" + "\n" + r"\begin{thebibliography}",
)
replace_once(
    "109--120.\\bibitem{HLTH04}",
    "109--120.\n\n\\bibitem{HLTH04}",
)
text = re.sub(r"\n{4,}", "\n\n\n", text)
article.write_text(text)
(work / "manuscript.diff").write_text(
    "".join(difflib.unified_diff(original.splitlines(True), text.splitlines(True),
                                fromfile="before/article.tex", tofile="after/article.tex"))
)

text = supplement.read_text()
original = text
replace_once(
    r"\usepackage{microtype,booktabs,needspace}",
    r"\usepackage{microtype,booktabs,needspace,multicol}",
)
replace_once(
    r"\paragraph{The 53 endpoint words.}",
    r"""\paragraph{The 53 endpoint words.}
The list pairs are given in the preceding cycle table.
\begin{multicols}{2}
\small""",
)
text, count = re.subn(
    r"For \$(\d{3})\$, use [^\n]+:",
    lambda match: r"\noindent For $" + match[1] + "$:",
    text,
)
assert count == 7, count
replace_once(
    r"\clearpage" + "\n"
    + r"\section{Certificates for the \texorpdfstring{$(2,3,2)$}{(2,3,2)}-path restoration}",
    r"\end{multicols}" + "\n\n"
    + r"\Needspace{8\baselineskip}" + "\n"
    + r"\section{Certificates for the \texorpdfstring{$(2,3,2)$}{(2,3,2)}-path restoration}",
)
replace_once(
    r"\clearpage" + "\n"
    + r"\section{Literal pentagon cycles, path blocks and common-port seeds}",
    r"\Needspace{8\baselineskip}" + "\n"
    + r"\section{Literal pentagon cycles, path blocks and common-port seeds}",
)
replace_once(
    r"\section{Literal protected-pentagon certificates}",
    r"\Needspace{8\baselineskip}" + "\n"
    + r"\section{Literal protected-pentagon certificates}",
)
# Layout may change around the markers; all literal marked data stay identical.
pattern = re.compile(r"^% BEGIN ([^\n]+)\n(.*?)^% END \1\s*$", re.M | re.S)
before_blocks = dict(pattern.findall(original))
after_blocks = dict(pattern.findall(text))
assert len(before_blocks) == len(after_blocks) == 55
assert before_blocks == after_blocks
before_words = re.findall(r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", original, re.S)
after_words = re.findall(r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", text, re.S)
assert before_words == after_words
supplement.write_text(text)
(work / "supplement.diff").write_text(
    "".join(difflib.unified_diff(original.splitlines(True), text.splitlines(True),
                                fromfile="before/certificates.tex",
                                tofile="after/certificates.tex"))
)
print("Shared endpoint construction extracted; duplicate exposition removed.")
print("55 marked data blocks and all 53 endpoint words preserved exactly.")
