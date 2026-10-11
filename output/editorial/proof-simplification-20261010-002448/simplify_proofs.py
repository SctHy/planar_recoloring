from pathlib import Path
import hashlib

ROOT = Path('/Users/huahua815/Downloads/planar_recoloring')
SOURCE = ROOT / 'planar_recoloring_hamilton_thresholds.tex'
EXPECTED = '8bf2bc9e60c356c6f3f0daad2674fc712d8c123f36c13f35927ce4be9351c91d'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
text = SOURCE.read_text()


def replace_once(old, new):
    global text
    assert text.count(old) == 1, old[:100]
    text = text.replace(old, new, 1)


def replace_between(start, end, new):
    global text
    assert text.count(start) == 1, start
    i = text.index(start)
    j = text.index(end, i)
    text = text[:i] + new + text[j:]


replace_once(r'''If $n=2$, the edgeless graph gives $K_k\square K_k$, which is
Hamilton-connected by Lemma~\ref{lem:product}.  For $G=K_2$, we have
$d\ge1$ and hence $k\ge4$, so the arrangement-graph result below applies.
We may therefore assume that $n\ge3$.
''', '')

replace_between(
    r'\noindent\textit{Case 2: $\alpha=\beta$.}',
    '\nIn both cases there is a Hamilton path from $x$ to $y$.',
    r'''\noindent\textit{Case 2: $\alpha=\beta$.}
Here $a\ne b$. Choose $c\in L(\alpha)\setminus\{a,b\}$.
Since $H$ is nonempty and $d$-degenerate, it has a vertex $u$ with
$\deg_H(u)\le d$. At least $k-d\ge3$ colours are available at $u$,
so recolour $u$ to one different from both $\alpha(u)$ and $c$.
This gives a base colouring $g$ adjacent to $\alpha$ with
$c\in L(g)$: no neighbour of $v_1$ has acquired colour $c$.

Every edge of a Hamilton-connected graph of order at least three lies
on a Hamilton cycle, obtained by closing a Hamilton path between its
ends. Take such a cycle $C$ through $\alpha g$, and let $h$ be the
other neighbour of $\alpha$ on $C$. Since
$|L(\alpha)\cap L(h)|\ge2$, choose
\[
q\in (L(\alpha)\cap L(h))\setminus\{c\}.
\]
If $q=a$, interchange $a,b$ and reverse the final path. Thus we may
assume $q\ne a$. Partition $F_\alpha$ into two disjoint paths
$P:\alpha(a)\leadsto\alpha(c)$ and
$P':\alpha(q)\leadsto\alpha(b)$: take $P'$ to be a singleton if
$q=b$, and otherwise the edge $\alpha(q)\alpha(b)$; place all
remaining vertices in $P$. The distinct ends of $P$ belong to this
remaining clique, so this partition exists for every $|L(\alpha)|\ge3$.

The path $C-\alpha$ contains all but one base state, so the lifting
claim gives a spanning path $Q$ through all other fibres from $g(c)$
to $h(q)$. The two cross edges
$\alpha(c)g(c)$ and $h(q)\alpha(q)$ concatenate $P,Q,P'$ into the
required Hamilton path.
''')

replace_between(
    'We use an elementary fact about lists on a cycle.',
    '\nIt remains to exclude the exceptional odd-cycle configuration',
    r'''By Lemma~\ref{lem:list-cycle}, such bridge colours exist unless $s$
is odd and all the $S_i$ are the same two-element set.
''')

replace_once(r'''M:=|V(Y)|,\qquad N:=|V(X)|.
\]
''', r'''M:=|V(Y)|,\qquad N:=|V(X)|.
\]
Since $H$ is nonempty, colour permutations give $M\ge k\ge3$.
''')

replace_between(
    'It remains to construct cycles of all lengths $\\ell\\ge 7$.',
    '\nSince $x$ was arbitrary,',
    r'''It remains to construct cycles of all lengths $\ell\ge7$.
By induction, for each $3\le s\le M$ choose a cycle $C_s$ of length
$s$ in $Y$ through $\alpha$, and put
\[
T_s:=\sum_{f\in V(C_s)}|F_f|.
\]
The closed lifting claim gives every length in $[2s+1,T_s]$ through
$x$. These intervals overlap consecutively, since $T_s\ge3s$ and
the next lower endpoint satisfies $2s+3\le3s$ for $s\ge3$.
Moreover, $T_M=N$, because $C_M$ is spanning. Hence the intervals
cover every length from $7$ to $N$. Together with the cycles of
lengths $3,4,5,6$ constructed above, this proves the claim.
''')

replace_once(r'''To see this, choose bridge colours in the successive intersections,
requiring consecutive bridge colours to differ and avoiding the
prescribed endpoint colour at either end.  All intersection lists have
size at least two and one has size at least three.  Greedily choose from
the two ends towards a three-element list, and choose at that list last
while avoiding its at most two forbidden colours.  Then traverse each
clique between its distinct entrance and exit colours.
''', r'''Indeed, Lemma~\ref{lem:bridge-colours} supplies bridge colours in the
successive intersections, with distinct entrance and exit colours in
each clique and with the prescribed endpoint colours avoided at the
two ends. Traverse each clique between these colours and join the
paths by the corresponding cross edges.
''')

replace_between(
    'If $|A_f|\\ge4$, choose a base Hamilton cycle through $f$',
    '\n\\end{proof}',
    r'''Choose any $c\in A_f\setminus\{a,b\}$. At most $d_G(v)$ base
moves from $f$ make $c$ unavailable: for each neighbour of $v$,
only its move to colour $c$ can do so. The state-degree assumption
therefore gives a base edge $fg$ preserving $c$. Take a base Hamilton
cycle $C$ containing $fg$, and let $h$ be the other neighbour of $f$
on $C$. Choose $q\in(A_f\cap A_h)\setminus\{c\}$, which is possible
because the intersection has size at least two. If $q=a$, interchange
the endpoints and reverse the final path, so we may assume $q\ne a$.

As in the same-fibre case of Theorem~\ref{thm:degenerate-hc}, split
the root clique into disjoint paths $a\leadsto c$ and $q\leadsto b$
covering it; the second is a singleton when $q=b$, and otherwise is
the edge $qb$. Lift $C-f$ through all other fibres with endpoint
colours $c,q$. Joining this lifted path to the two root paths by the
cross edges at $c,q$ gives the prescribed spanning path.
''')

SOURCE.write_text(text)
print(f'Updated {SOURCE.name}: {len(text.splitlines())} lines')
