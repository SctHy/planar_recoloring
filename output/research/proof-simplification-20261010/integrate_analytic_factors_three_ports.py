from pathlib import Path
import hashlib, json, re, difflib

ROOT = Path('/Users/huahua815/Downloads/planar_recoloring')
WORK = ROOT / 'output/research/proof-simplification-20261010'
PATH = ROOT / 'planar_recoloring_hamilton_thresholds.tex'
old = PATH.read_text()
assert hashlib.sha256(PATH.read_bytes()).hexdigest() == '66bb40fddf3602256bc509de917e39608e657e2f773513d9d9f5037fe1e9199b'
text = old


def replace_once(a, b):
    global text
    assert text.count(a) == 1, a[:90]
    text = text.replace(a, b, 1)


def replace_span(a, b, new):
    global text
    assert text.count(a) == 1, a
    i = text.index(a)
    j = text.index(b, i)
    text = text[:i] + new + text[j:]


replacement = r'''\begin{lemma}[Analytic path factors]\label{lem:pentagon-list-factor}
Let $X$ be the complete fixed-list recolouring graph of a finite
triangle-free graph with a finite palette. Every nontrivial component
$Y$ has a $\{P_2,P_3\}$-factor. Given any such factor $F$, its
components can be joined by $c(F)-1$ edges of $Y$, with each vertex
incident with at most three added edges. Here $c$ counts components.
In particular, this applies to every component of a listed pentagon
with lists of size at least three in a four-colour palette.
\end{lemma}
\begin{proof}
We show $c(Y-S)\le2|S|$ for every nonempty $S\subseteq V(Y)$.
For a component $D$ of $Y-S$ put
$b(D)=|N_Y(D)\cap S|>0$. At each $s\in S$, choose one neighbour
$i_D\in D$ for every component adjacent to $s$. These moves change
different original vertices: two moves at the same vertex yield
adjacent states and cannot lead to different components of $Y-S$.

Join two representatives in a graph $C_s$ if their moves can be
performed simultaneously. Distinct-coordinate legal moves fail to
commute precisely when their original vertices are adjacent and
their target colours agree. Thus $\alpha(C_s)\le2$, since three
pairwise noncommuting moves would create an original triangle.
Each commuting partner of $D$ produces a distinct double-move state
adjacent to $i_D$. Completeness of the fixed-list graph puts this
state in $Y$, and it must belong to $S$; otherwise it joins different
components of $Y-S$. It differs from $s$, so
$d_{C_s}(D)+1\le b(D)$.

For any finite graph $C$, selecting the vertices earliest in their
closed neighbourhoods in a uniform random ordering gives an
independent set, and hence
$\sum_v1/(d_C(v)+1)\le\alpha(C)$. Consequently
\[
\sum_{D:s\in N_Y(D)}\frac1{b(D)}
\le\sum_{D\in V(C_s)}\frac1{d_{C_s}(D)+1}\le2.
\]
Summing over $s\in S$ counts each component once, proving the bound.
It gives $i(Y-S)\le2|S|$ for all $S$, where $i$ counts isolated
vertices; the empty-set case holds because $Y$ is nontrivial and
connected. The Akiyama--Avis--Era path-factor criterion~\cite{AAE80}
gives a $\{P_2,P_3\}$-factor. Also $c(Y-S)<2|S|+3$ for every $S$,
including the empty set. Ellingham--Zha~\cite[Theorem~3.5, $g=2$,
$k=3$]{EZ00}, applied to the specified factor $F$, gives the asserted
connections. Contracting the factor paths makes these edges a tree.

Finally, every proper four-colouring of $C_5$ repeats a colour at
two nonadjacent vertices, which have a common neighbour on the cycle.
Only one colour is forbidden there by its two neighbours; a list of
size at least three therefore permits a different colour. Thus no
pentagon state is isolated, and every component is nontrivial.
\end{proof}

'''
replace_span(r'\begin{lemma}\label{lem:pentagon-list-factor}',
             r'\subsection{The finite protected-edge identities}', replacement)

replace_once(r'''The first two pool edges will join consecutive copies of $C_A$;
the last six will join factor blocks.''', r'''The first two pool edges join copies of $C_A$ in a two- or
three-row path product; the last six supply splice reserves.''')
replace_once(r'''Designate a seven-edge pool in $D_A$, and put $K_A=D_A\setminus
\text{pool}$. Its first edge joins successive seed blocks and its last
six join factor blocks. All pool edges are distinct.''', r'''Designate a seven-edge pool in $D_A$, and put $K_A=D_A\setminus
\text{pool}$. Its last six edges supply splice reserves. All pool
edges are distinct; only three reserves will be needed at each row.''')

start = text.index(r'\begin{lemma}\label{lem:protected-product}')
proof_start = text.index(r'\begin{proof}', start)
proof_end = text.index(r'\end{proof}', proof_start) + len(r'\end{proof}')
new_proof = r'''\begin{proof}
By Lemma~\ref{lem:pentagon-list-factor}, choose a $\{P_2,P_3\}$-factor
of $B$ and join its paths by a tree of actual $B$ edges, with at most
three joining edges incident at any physical vertex of $B$.

For each factor path construct its product cycle with $A$.
If $A$ has its specified cycle $C_A$, join its two copies using the
first pool edge; for a three-vertex path use the first and second
pool edges at its two interfaces. These cuts are distinct in the
middle row. If $A$ is hard, use its specified two- or three-row seed
directly. Every initial cycle retains $K_A$ and the last six pool
edges in every row.

Fix three of these six reserves. Process the factor-path tree in
parent-before-child order. At the parent row at most two of the three
reserve edges have already been consumed, since its total joining
load is at most three; the fresh child row retains all three.
Choose an unused common reserve edge, delete its two copies, and add
the two cross edges supplied by the actual joining edge of $B$.
This joins two disjoint cycles into one and never cuts $K_A$.
Induction over the tree covers all factor paths and gives the required
protected Hamilton cycle of $A\square B$.
\end{proof}'''
text = text[:proof_start] + new_proof + text[proof_end:]

# Remove only obsolete factor words. The constant factor contains the
# two C15 component cycles used by the protected identities and stays.
table_start = text.index(r'\begin{table}', text.index(r'\section{Literal pentagon factors'))
table_end = text.index(r'\paragraph{Factor 00000', table_start)
text = text[:table_start] + text[table_end:]
factor_start = text.index(r'\paragraph{Factor 00001')
factor_end = text.index(r'\paragraph{Cycle 00011', factor_start)
text = text[:factor_start] + text[factor_end:]

# The new protected 00001 seeds PC2/PC3 are printed in the next appendix.
# Keep the ordinary cycles and 00112 seeds, which it explicitly reuses.
seed_start = text.index(r'\paragraph{C2 for 00001')
seed_end = text.index(r'\paragraph{C2 for 00112', seed_start)
text = text[:seed_start] + text[seed_end:]

replace_once(r'''words the first digit is the path layer. Semicolons separate factor blocks;
without a semicolon the entire factor line is one block.
All Hamilton words are cyclic. A port is a pair of five-digit words.''',
             r'''words the first digit is the path layer. Semicolons separate the two
constant-type component cycles. All Hamilton words are cyclic.
A port is a pair of five-digit words. Path factors are supplied
analytically by Lemma~\ref{lem:pentagon-list-factor}; their eleven-type
word enumeration is not needed.''')
replace_once(r'''The first two pool edges (or the first one for a hard component) join
path layers or seed blocks; the last six join the factor tree.''',
             r'''The first two pool edges for a Hamilton component join two or three
path rows; the last six pool edges supply factor-tree reserves.
Three reserves suffice by Lemma~\ref{lem:pentagon-list-factor}.''')

replace_once('For the protected pentagon lift, the fresh readers covered 590 ordinary factor words, 465 factor cycles, 475 seeds, 1024 boundary records, and 245,760 labelled states; the protected reader covered 23 component types, 2304 labelled boundaries, and 313 interfaces, with at least ten common states per interface.',
             'For the protected pentagon lift, the protected reader covered 23 component types, 2304 labelled boundaries, and 313 interfaces, with at least ten common states per interface. The path factors and the load-three factor connections now follow analytically from Lemma~\\ref{lem:pentagon-list-factor}; the eleven-type factor-word enumeration is no longer a proof premise.')

bibliography = r'''\bibitem{AAE80}
J.~Akiyama, D.~Avis, and H.~Era,
\newblock On a $[1,2]$-factor of a graph,
\newblock \emph{TRU Mathematics} 16 (1980), no.~2, 97--102.
\newblock The path-factor criterion is also reproduced as Theorem~A
in \href{https://tgt.ynu.ac.jp/ozeki/2015EFO.pdf}{Egawa--Furuya--Ozeki's author manuscript}.

\bibitem{EZ00}
M.~N.~Ellingham and X.~Zha,
\newblock Toughness, trees, and walks,
\newblock \emph{Journal of Graph Theory} 33 (2000), no.~3, 125--137.
\newblock \href{https://math.vanderbilt.edu/ellingmn/paper/ttw/b-eps.pdf}{Authors' manuscript}, Theorem~3.5.

'''
replace_once(r'\bibitem{DFFV06}', bibliography + r'\bibitem{DFFV06}')

# Reconcile exact retained finite-evidence blocks before writing.
def paragraphs(source):
    starts = list(re.finditer(r'\\paragraph\{([^\n]+)\}', source))
    return {m.group(1):source[m.end():starts[i+1].start() if i+1<len(starts) else len(source)]
            for i,m in enumerate(starts)}
old_p = paragraphs(old)
new_p = paragraphs(text)
retained = ['Factor 00000 (30 words).'] + [key for key in old_p if
    key.startswith(('Cycle ', 'C2 for 00112', 'C3 for 00112', 'Common ports 00112',
                    'PC2 ', 'PC3 ', 'Balanced common', 'Cycle for ', 'Pool for ', 'All 313'))]
certificates = {}
for key in retained:
    # A block ends at the next paragraph; final section separators may change
    # only for Factor 00000 because obsolete following paragraphs were removed.
    a = old_p[key].strip()
    b = new_p[key].strip()
    assert a == b, key
    certificates[key] = hashlib.sha256(a.encode()).hexdigest()

thresholds = lambda s: re.findall(r'\\begin\{(theorem|corollary)\}(.*?)\\end\{\1\}', s, re.S)
assert thresholds(old) == thresholds(text), 'threshold statement changed'
old_labels = set(re.findall(r'\\label\{([^}]+)\}',old))
new_labels = set(re.findall(r'\\label\{([^}]+)\}',text))
assert old_labels-new_labels == {'tab:pentagon-factors'}
assert not (new_labels-old_labels)
refs = set(re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text))
assert refs <= new_labels

PATH.write_text(text)
(WORK/'analytic-factor-integration.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),text.splitlines(True),fromfile='before.tex',tofile='after.tex')))
(WORK/'integration-verification.json').write_text(json.dumps({'threshold_statements_identical':True,'retained_certificate_blocks_identical':True,'retained_certificate_blocks':certificates,'removed_label':'tab:pentagon-factors','removed_material':'560 obsolete nonconstant factor words and old 00001 seeds/ports; original bytes preserved in original/','factor_connections':'AAE path factors plus Ellingham-Zha load three','source_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest()},indent=2)+'\n')
print('Integrated analytic factors, bounded-load connections and direct two/three-row seeds.')
print(f'Retained {len(certificates)} finite-evidence blocks byte-for-byte.')
