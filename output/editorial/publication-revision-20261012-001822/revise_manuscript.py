from pathlib import Path
import hashlib

p=Path('planar_recoloring_hamilton_thresholds.tex')
s=p.read_text()
backup=Path('output/editorial/publication-revision-20261012-001822/original/planar_recoloring_hamilton_thresholds.tex')
assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(backup.read_bytes()).digest()
s=s.replace('Hamiltonian Thresholds for Planar Recolouring Graphs', 'Hamiltonian and Hamilton-connected thresholds for planar recolouring graphs')
s=s.replace(r'\date{October 2026}', r'\date{}')
s=s.replace(r'\usepackage{microtype,enumitem,needspace,booktabs}', r'\usepackage{microtype,enumitem,needspace,booktabs,tabularx}')
a=s.index(r'\begin{abstract}')
b=s.index(r'\section{The degenerate theorem}',a)
s=s[:a]+r'''\begin{abstract}
For a graph $G$, let $\Rk(G)$ have the proper colourings of $G$ with a
labelled $k$-colour palette as vertices, with one-vertex recolourings as
edges. We prove that $\Rk(G)$ is Hamilton-connected and vertex-pancyclic
whenever $G$ is nonempty and $d$-degenerate and $k\ge d+3$; this uniform
palette bound is sharp for both properties. We determine the common
Hamiltonian and Hamilton-connected thresholds as $7$ for planar graphs,
$5$ for triangle-free and bipartite planar graphs, and $4$ for planar
graphs of girth at least six and for forests. At four colours we also
prove Hamiltonicity for planar graphs of girth at least five with at
most seven distinct $5$-cycles, and for those whose every block has
maximum degree at most three. The latter condition allows unbounded
degree at cutvertices. These four-colour proofs combine structural
reductions with local restoration certificates supplied in a separate,
reproducible supplement. For unrestricted planar graphs of girth at
least five, both thresholds remain between $4$ and $5$.
\end{abstract}

\section{Introduction}

A cyclic listing of all proper colourings in which successive colourings
differ at one vertex is a colouring Gray code, or equivalently a Hamilton
cycle in the recolouring graph. Prescribing the first and last
colourings asks for Hamilton-connectedness. Requiring a cycle of every
length through each colouring asks for vertex-pancyclicity. We study
these stronger spanning and cyclic properties for sparse graphs, with
particular emphasis on sharp palette thresholds for planar classes.

All graphs are finite, simple and undirected, and may be disconnected.
A graph is nonempty when it has at least one vertex. Put $[k]=\{1,\ldots,k\}$.
The vertices of $\Rk(G)$ are the proper maps $\sigma:V(G)\to[k]$;
two are adjacent when they differ on exactly one vertex of $G$.
Colours are labelled, and a colouring need not use every colour.
A cycle has at least three vertices. A graph is Hamilton-connected if
every two distinct vertices are joined by a spanning path, and
vertex-pancyclic if every vertex lies on a cycle of every length from
three to the order of the graph.

For a class $\mathcal C$ of nonempty graphs, define
\begin{align*}
 h(\mathcal C)&=\min\{q:\Rk(G)\text{ is Hamiltonian for every }G\in\mathcal C
                      \text{ and every }k\ge q\},\\
 \hc(\mathcal C)&=\min\{q:\Rk(G)\text{ is Hamilton-connected for every }G\in\mathcal C
                      \text{ and every }k\ge q\},
\end{align*}
when these sets are nonempty. These are uniform thresholds in the
palette size; the proofs establish every larger palette separately.
A graph is $d$-degenerate if each nonempty subgraph has a vertex of
degree at most $d$. Write $\mathcal D_d$ for this class.

Choo and MacGillivray~\cite[Theorem~3.4]{ChMa11} proved that
$\Rk(G)$ is Hamiltonian for $k\ge d+3$ when $G$ is $d$-degenerate.
They also determined the uniform forest threshold and several
individual tree and cycle cases~\cite[Sections~5--6]{ChMa11}.
Our first result strengthens their general Hamiltonian conclusion
while keeping the same palette bound.

\begin{theorem}\label{thm:main-degenerate}
Let $G$ be a nonempty $d$-degenerate graph. For every $k\ge d+3$,
$\Rk(G)$ is Hamilton-connected and vertex-pancyclic. Moreover,
$\hc(\mathcal D_d)=d+3$, and $d+3$ is also the least uniform palette
bound for vertex-pancyclicity on $\mathcal D_d$.
\end{theorem}

Write $\mathcal P$ for the planar graphs, $\mathcal T$ for the
triangle-free planar graphs, $\mathcal B$ for the bipartite planar
graphs, $\mathcal P_g$ for the planar graphs of girth at least $g$,
and $\mathcal F$ for the forests. All these classes contain only
nonempty graphs; forests have infinite girth.

\begin{theorem}\label{thm:main-planar}
The following uniform thresholds are exact:
\[
\begin{aligned}
 h(\mathcal P)=\hc(\mathcal P)&=7,\\
 h(\mathcal T)=\hc(\mathcal T)=h(\mathcal B)=\hc(\mathcal B)&=5,\\
 h(\mathcal P_6)=\hc(\mathcal P_6)=h(\mathcal F)=\hc(\mathcal F)&=4.
\end{aligned}
\]
\end{theorem}

The large-palette cases follow from degeneracy. The critical palettes
require endpoint-preserving restoration of separated low-degree
vertices, and, in the triangle-free case, of an adjacent degree-three
pair. The lower bounds use frozen colourings and the three-colour
recolouring graph of a short path. The equality $h(\mathcal F)=4$
already follows from~\cite{ChMa11}; here it accompanies the
Hamilton-connected forest result.

At four colours the girth-five case requires different local
configurations. Let $\mathcal P_5^{\le7}$ consist of the graphs in
$\mathcal P_5$ with at most seven distinct $5$-cycles. Let
$\mathcal S_5$ consist of those in $\mathcal P_5$ whose every block
has maximum degree at most three. Here blocks include bridges and
isolated vertices as well as maximal two-connected subgraphs.

\begin{theorem}\label{thm:main-four}
For every $G\in\mathcal P_5^{\le7}\cup\mathcal S_5$ and every $k\ge4$,
$\Rk(G)$ is Hamiltonian. Both classes have uniform Hamiltonian
threshold four, and their Hamilton-connected thresholds lie between
four and five.
\end{theorem}

In particular, Theorem~\ref{thm:main-four} includes all subcubic planar
graphs of girth at least five, while allowing vertices of arbitrarily
large total degree when that degree is distributed among blocks.
Bartier et al.~\cite{BBFHMP23} proved that $\R_4(G)$ is connected for
every $G\in\mathcal P_5$. The spanning-cycle and prescribed-endpoint
questions remain stronger: for the full class we obtain
\[
4\le h(\mathcal P_5)\le5,\qquad 4\le\hc(\mathcal P_5)\le5.
\]
Table~\ref{tab:thresholds} records the results and these open cases.

\begin{table}[htbp]
\centering\small
\caption{Uniform thresholds. An interval records an unresolved value.}
\label{tab:thresholds}
\begin{tabularx}{\linewidth}{@{}Xcc@{}}
\toprule
Graph class & $h$ & $\hc$\\
\midrule
Planar & $7$ & $7$\\
Triangle-free planar & $5$ & $5$\\
Bipartite planar & $5$ & $5$\\
Planar, girth at least six & $4$ & $4$\\
Forests & $4$ & $4$\\
Planar, girth at least five, at most seven $5$-cycles & $4$ & $[4,5]$\\
Planar, girth at least five, every block subcubic & $4$ & $[4,5]$\\
Planar, girth at least five & $[4,5]$ & $[4,5]$\\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Proof strategy and organization}
Deleting vertices partitions the larger recolouring graph into fibres
above colourings of the smaller graph. At the degenerate bound these
fibres are cliques of order at least three. We choose bridge colours
between consecutive fibres to prescribe endpoints or cycle lengths.
Section~\ref{sec:degenerate} proves Theorem~\ref{thm:main-degenerate},
including the parity obstruction that makes its bound sharp.
Section~\ref{sec:restoration} develops the product and independent-set
lifts used in the planar proofs.

Section~\ref{sec:hc-planar} proves Theorem~\ref{thm:main-planar} by
combining these lifts with planar degree counts. Section~\ref{sec:four-colour-subclasses}
proves Theorem~\ref{thm:main-four}. The few-cycle argument restores
low-degree configurations. For the subcubic and block-subcubic classes,
we restore two separated pentagons. Their product fibres have at most
four components. Local cycles retain protected edges at each interface;
a bounded-degree spanning tree then joins all component cycles into
one spanning cycle, for a bottom recolouring cycle of arbitrary length.

The supplement \emph{Finite certificates for Hamiltonian thresholds in
planar recolouring graphs} contains the literal paths, cycles, pools
and interface records. Its Appendices~A--D correspond to the adjacent-pair,
path and pentagon steps. Section~\ref{sec:verification} specifies exactly
what the accompanying verifiers check. The finite data supply local
lemmas; the inductions and restoration arguments in the article give
the conclusions for graphs of arbitrary order.

\subsection{Notation}
For a graph $G$, write $N_G(v)$ for the open neighbourhood,
$N_G[v]=N_G(v)\cup\{v\}$, and $G-S$ for deletion of a vertex set $S$.
The Cartesian product $X\square Y$ joins $(x,y)$ to $(x',y')$ when
exactly one coordinate changes along an edge of its factor.
A spanning path may be a singleton when its ends coincide in an
intermediate construction. Local certificates use zero-based palettes
$\{0,\ldots,k-1\}$, obtained by relabelling $[k]$.
Face lengths count edge-side incidences, so a bridge is counted twice.

''' +s[b:]
# Shared fibre notation, followed by the complete endpoint argument.
a=s.index(r'\begin{theorem}[Degenerate Hamilton-connectedness]')
s=s[:a]+r'''\subsection{Clique fibres}
For a vertex $v$ of degree at most $d$ with $H=G-v\ne\varnothing$, put
\[
 L(f)=[k]\setminus f(N_G(v)),\qquad
 F_f=\{f(c):c\in L(f)\},
\]
where $f(c)$ extends a proper colouring $f$ of $H$ by assigning colour
$c$ to $v$. The sets $F_f$ partition $V(\Rk(G))$ into cliques. If
$f,g$ are adjacent base colourings, then
\begin{equation}\label{eq:clique-fibres}
 |L(f)|\ge3,\qquad |L(f)\cap L(g)|\ge |L(f)|-1\ge2.
\end{equation}
The cross edges are exactly $f(c)g(c)$ for $c\in L(f)\cap L(g)$.
If the base move changes a nonneighbour of $v$, then $L(f)=L(g)$.
We use this notation in both following proofs.

''' +s[a:]
a=s.index(r'\begin{proof}',s.index(r'\begin{theorem}[Degenerate Hamilton-connectedness]'))
b=s.index(r'\end{proof}',a)+len(r'\end{proof}')
s=s[:a]+r'''\begin{proof}
Induct on $n=|V(G)|$. The case $n=1$ is $K_k$. If $G=K_n$,
then $\Rk(G)$ is the arrangement graph $A_{k,n}$, whose vertices
are ordered $n$-tuples of distinct colours. Since $k\ge n+2$,
it is Hamilton-connected by~\cite[Theorem~1]{HLTH04}.

Otherwise choose a minimum-degree vertex $v$ and a nonneighbour
$w\in V(H)$, where $H=G-v$. Both exist because $G$ is not complete,
and $d_G(v)\le d$. By induction, $Y=\Rk(H)$ is Hamilton-connected.
Use the clique fibres just defined.

\emph{Path-lifting claim.} Let $f_0,\ldots,f_t$ be a base path,
$t\ge1$, and set $S_i=L(f_i)\cap L(f_{i+1})$. If some $S_j$ has
size at least three, then the union of its fibres has a spanning
path from $f_0(a)$ to $f_t(b)$ for arbitrary
$a\in L(f_0)$ and $b\in L(f_t)$. Indeed,
Lemma~\ref{lem:bridge-colours} chooses $x_i\in S_i$ with
$x_0\ne a$, consecutive $x_i$ distinct, and $x_{t-1}\ne b$.
Traverse each clique between its prescribed entrance and exit,
and join consecutive traversals by $f_i(x_i)f_{i+1}(x_i)$.

This claim applies to every base path missing at most one vertex of
$Y$. To see this, colour permutations give all $k$ colours at $w$
among the states of $Y$. After removing at most one state, at least
$k-1\ge2$ colours still occur at $w$. A path through those states
therefore contains a move at $w$. This move leaves $L(f)$ unchanged,
so its intersection has size at least three.

Now prescribe distinct endpoints $\alpha(a)$ and $\beta(b)$ in
$\Rk(G)$. If $\alpha\ne\beta$, lift a Hamilton path in $Y$ from
$\alpha$ to $\beta$ by the claim. This covers every fibre.

If $\alpha=\beta$, then $a\ne b$. Choose
$c\in L(\alpha)\setminus\{a,b\}$. A vertex of degree at most $d$
in $H$ has at least three available colours. Recolour it to a colour
different from its present colour and from $c$, obtaining a neighbour
$g$ of $\alpha$ with $c\in L(g)$.
Every edge of a Hamilton-connected graph of order at least three lies
on a Hamilton cycle, by closing a spanning path between its ends.
Choose such a cycle through $\alpha g$, and let $h$ be its other
neighbour of $\alpha$. Take
$q\in(L(\alpha)\cap L(h))\setminus\{c\}$.
If $q=a$, exchange $a,b$ and reverse the path constructed below.
We may thus assume $q\ne a$.

Partition $F_\alpha$ into paths
$P:\alpha(a)\leadsto\alpha(c)$ and
$P':\alpha(q)\leadsto\alpha(b)$.
Use a singleton for $P'$ if $q=b$, and its endpoint edge otherwise;
put all remaining vertices in $P$. The base path obtained by deleting
$\alpha$ from the chosen cycle misses only that state. The claim lifts
it to a spanning path $Q$ through the other fibres, from $g(c)$ to
$h(q)$. The two cross edges $\alpha(c)g(c)$ and $h(q)\alpha(q)$
join $P,Q,P'$ into the required spanning path.
\end{proof}''' +s[b:]
a=s.index(r'\begin{proof}',s.index(r'\begin{theorem}[Degenerate vertex-pancyclicity]'))
b=s.index(r'\end{proof}',a)+len(r'\end{proof}')
s=s[:a]+r'''\begin{proof}
Induct on $|V(G)|$, starting with $\Rk(K_1)=K_k$. For larger $G$,
choose $v$ with $d_G(v)\le d$ and put $H=G-v$.
Use the clique fibres above, and write
$Y=\Rk(H)$, $M=|V(Y)|$, and $N=|V(\Rk(G))|$.
Colour permutations give $M\ge k\ge3$.
Fix a state $x=\alpha(a)$ of $\Rk(G)$.

\emph{Closed-lifting claim.} A base cycle
$f_0,f_1,\ldots,f_{s-1},f_0$ through $f_0=\alpha$ lifts to a cycle
through $x$ of every length in
\begin{equation}\label{eq:closed-lift-lengths}
 [2s+1,\ \textstyle\sum_i|F_{f_i}|].
\end{equation}
Put $S_i=L(f_i)\cap L(f_{i+1})$, with cyclic indices.
Lemma~\ref{lem:list-cycle} selects bridge colours $y_i\in S_i$
with $y_{i-1}\ne y_i$, unless $s$ is odd and all $S_i$ equal
one binary set $\{p,q\}$.

We exclude this exception. By~\eqref{eq:clique-fibres}, each
$L(f_i)$ then has size three, and
\[
 k-3=|f_i(N_G(v))|\le d_G(v)\le d\le k-3.
\]
Thus $d_G(v)=d=k-3$, its neighbours have distinct colours, and
none uses $p$ or $q$. Every base move changes a neighbour of $v$;
a nonneighbour move would leave an intersection of size three.
Order the neighbours $u_1,\ldots,u_d$. In the $(d+1)$-element
palette $[k]\setminus\{p,q\}$, append the unique unused colour
$r_i$ to the tuple $(f_i(u_1),\ldots,f_i(u_d))$.
A base move exchanges one neighbour colour with $r_i$, reversing
permutation parity. An odd number of such exchanges cannot return
to the initial tuple. Hence the bridge colours exist.

Choose an $m_0$-vertex path in $F_{f_0}$ between its bridge states
and containing $x$, with $3\le m_0\le|F_{f_0}|$.
In every other clique choose a bridge-to-bridge path on
$2\le m_i\le|F_{f_i}|$ vertices. The sums of these integer intervals
are exactly~\eqref{eq:closed-lift-lengths}. The cross edges with $v$
fixed at $y_i$ close these paths into the desired cycle.

The clique $F_\alpha$ already supplies a triangle through $x$.
For lengths four, five and six, recolour a vertex of degree at most
$d$ in $H$ to a colour avoiding its present colour, its neighbours,
and $a$. At most $d+2$ colours are excluded, so this gives a neighbour
$\beta$ of $\alpha$ with $a\in L(\beta)$.
Choose $p\in(L(\alpha)\cap L(\beta))\setminus\{a\}$,
$q\in L(\alpha)\setminus\{a,p\}$, and
$r\in L(\beta)\setminus\{a,p\}$.
The following cyclic sequences have the required lengths:
\[
\begin{array}{ll}
4:&\alpha(a),\alpha(p),\beta(p),\beta(a),\\
5:&\alpha(a),\alpha(q),\alpha(p),\beta(p),\beta(a),\\
6:&\alpha(a),\alpha(q),\alpha(p),\beta(p),\beta(r),\beta(a).
\end{array}
\]

For each $3\le s\le M$, induction supplies a base $s$-cycle $C_s$
through $\alpha$. Put $T_s=\sum_{f\in V(C_s)}|F_f|$.
The closed-lifting claim gives every length in $[2s+1,T_s]$.
These intervals overlap successively, since $T_s\ge3s\ge2s+3$
for $s\ge3$. Also $T_M=N$. They therefore cover every length
from seven to $N$, completing the proof.
\end{proof}''' +s[b:]
a=s.index(r'\section{Endpoint lifting and restoration}')
s=s[:a]+r'''\begin{proposition}[Optimal uniform palette bound]\label{prop:degenerate-sharp}
For every $d\ge0$, $\hc(\mathcal D_d)=d+3$. The same uniform palette
bound for vertex-pancyclicity cannot be reduced.
\end{proposition}
\begin{proof}
The upper bounds are the preceding theorems. For $d\ge1$, take
$G=K_{d+1}$ and $k=d+2$. Append the unique unused colour to each
ordered colouring of $G$. The resulting permutation of $d+2$ colours
changes by a transposition at every recolouring. Thus $\R_{d+2}(G)$
is bipartite by permutation parity, with equal parts and even order
$(d+2)!\ge6$. A spanning path must have endpoints in opposite parts,
so the graph is not Hamilton-connected. It has no triangle, so it is
not vertex-pancyclic. For $d=0$, the two-isolated-vertex graph has
$\R_2(G)=C_4$, which fails both properties.
\end{proof}

''' +s[a:]
# State the actual one-list 3/4 interfaces and their exit argument.
s=s.replace('The preserved endpoint words prove the four\nHamilton-connected types (indeed, the stronger original endpoint\nclassification).  These are finite local checks; no arbitrary-size\nclaim is being inferred from them.', 'The 53 endpoint words in supplementary Appendix~A prove the four\nHamilton-connected types. Their symmetry coverage and an exact subset\ndynamic program verify the complete endpoint classification.')
s=s.replace('one-list change is symmetric.  When a $3$-list and a containing\n$4$-list are interchanged, change the other coordinate to the other\ncolour in the common $3$-list.  In every case the selected edge lies', 'one-list change is symmetric. If $A$ and $A\'$ have sizes three and\nfour, one containing the other, put $A_0=A\cap A\'$. Then $|A_0|=3$.\nWhen $a\in A_0$, choose $(a,d)$ with $d\in B\setminus\{a,b\}$;\notherwise choose $(c,b)$ with $c\in A_0\setminus\{b\}$. The change\nin $B$ is symmetric. In every case the selected edge lies')
s=s.replace('both lists stay unchanged, or one stays unchanged and the other is\nreplaced by a three-element list differing in one colour, or a\nthree-element list and a containing four-element list are interchanged.', 'both lists stay unchanged, or exactly one changes. A changed list\nis either replaced by another three-element list differing in one\ncolour, or changes between a three-element list and a containing\nfour-element list.')
s=s.replace(r'\subsection{Block-subcubic lemma}', r'\subsection{Graphs with subcubic blocks}')
s=s.replace(r'\begin{lemma}\label{lem:block-subcubic}', r'\begin{theorem}[Subcubic blocks]\label{lem:block-subcubic}')
a=s.index(r'\begin{theorem}[Subcubic blocks]')
b=s.index(r'\end{lemma}',a)
s=s[:b]+s[b:].replace(r'\end{lemma}',r'\end{theorem}',1)
s=s.replace('Four-colour Hamilton-connectedness is not asserted.\n\\end{theorem}', 'Its Hamilton-connected threshold lies between four and five.\n\\end{theorem}')
# Replace retrospective material with the final mathematical scope and contract.
a=s.index('The general planar girth-five problem is deliberately left')
b=s.index(r'\begin{thebibliography}',a)
s=s[:a]+r'''For the full girth-five class, Theorem~\ref{thm:trianglefree-hc} and
the frozen three-colouring of $C_6$ give
\[
 4\le h(\mathcal P_5)\le5,\qquad
 4\le\hc(\mathcal P_5)\le5.
\]
The same Hamilton-connected interval applies to both four-colour
classes in Theorem~\ref{thm:main-four}. The unresolved question is
whether every $G\in\mathcal P_5$ has a Hamiltonian $\R_4(G)$, and,
more strongly, whether every such recolouring graph is
Hamilton-connected. Connectivity~\cite{BBFHMP23} supplies neither
conclusion. The structural argument above shows that a remaining
minimum four-colour Hamiltonian counterexample must contain a block
with internal maximum degree at least four.

\section{Finite certificates and reproducibility}
\label{sec:verification}

The supplementary source \texttt{article\_certificates.tex} is the input
for all three exact verifiers. The words, pools and selectors are read
from that source. Missing blocks, duplicate records, illegal transitions,
incomplete state coverage and failed protection conditions cause the
check to fail. No solver output or earlier computation report is an
input to these checks.

\begin{table}[htbp]
\centering\small
\caption{Finite checks supporting the local restoration lemmas.}
\label{tab:verification}
\begin{tabularx}{\linewidth}{@{}lX@{}}
\toprule
Supplement & Checked objects and coverage\\
\midrule
Appendix A & Seven edge-covering cycle orbits; 53 endpoint words with
exact subset-DP cross-check; 225 labelled list pairs and 3,225 interfaces.\\
Appendix B & Three normalized path cycles; 60 good boundaries and all
504 directed adjacent good-boundary changes; safe edges for every
allowed cycle pair and support at bad neighbours.\\
Appendices C--D & 23 complete pentagon components; 2,304 labelled
boundaries; ordered path blocks; both hard two- and three-row seeds;
pool membership and protection in every row; all 313 interfaces,
partitioned as $47+236+30$.\\
\bottomrule
\end{tabularx}
\end{table}

Run \texttt{python3 supplement/verify\_all.py} from the article directory.
The scripts require only the Python standard library and use exact
integer and finite-set operations. The runner also checks rejection
of corrupted cycles, missing certificate blocks, invalid interface
edges and altered selector data. Its JSON reports record input hashes,
coverage and the Python version; the distribution includes commands
for rebuilding both PDFs and a file manifest.

The finite verification establishes the local certificate claims in
Table~\ref{tab:verification}. The path lifting, arbitrary bad-run
construction, protected products, spanning-tree splicing and structural
inductions are analytic arguments in the article. Thus the finite checks
have no bound on the order of $G$ as an input premise, and the general
girth-five questions stated above remain open.

''' +s[b:]
# Make appendix references and template statements locatable without an old full draft.
s=s.replace('The companion certificate gives one short Hamilton cycle for each of', 'Supplementary Appendix~A gives one short Hamilton cycle for each of')
s=s.replace('are specified by literal cycles and capacity checks in the companion\ncertificate;', 'are specified by literal cycles and capacity checks in supplementary\nAppendix~B;')
s=s.replace('in the supplementary pentagon-kernel certificate.', 'in supplementary Appendix~C.')
s=s.replace('For $00001$, the supplementary certificate supplies the ordered path blocks', 'For $00001$, supplementary Appendix~C supplies the ordered path blocks')
s=s.replace('the companion certificate specifies a two-row cycle and derives its three-row', 'supplementary Appendices~C--D specify a two-row cycle and derive its three-row')
s=s.replace('the companion certificate gives 47', 'supplementary Appendix~D gives 47')
s=s.replace("Both three-row seeds follow from the companion certificate's", "Both three-row seeds follow from the supplement's")
s=s.replace('The $00112$ protected set is unchanged;', 'The $00112$ protected set')
s=s.replace('The two circles become two paths joined into one circle.', 'The two cycles become two paths joined into one cycle.')
s=s.replace('Induction over the tree preserves one circle, disjoint coverage and', 'Induction over the tree preserves one cycle, disjoint coverage and')
s=s.replace('There is no additional unproved closing step.', 'The final cycle spans the complete recolouring graph.')
# Drop the unused mixing reference; keep the primary mathematical inputs.
a=s.index(r'\bibitem{DFFV06}')
b=s.index(r'\bibitem{ChMa11}',a)
s=s[:a]+s[b:]
p.write_text(s)
print('Revised main manuscript:',len(s.splitlines()),'lines')
