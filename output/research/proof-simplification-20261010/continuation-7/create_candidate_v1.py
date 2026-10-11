#!/usr/bin/env python3
"""Create a frozen manuscript candidate; never mutate the main manuscript."""
from pathlib import Path
import hashlib
import shutil

ROOT = Path('/Users/huahua815/Downloads/planar_recoloring')
WORK = Path(__file__).resolve().parent
MAIN = ROOT / 'planar_recoloring_hamilton_thresholds.tex'
EXPECTED = '7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(MAIN) == EXPECTED
original = WORK / 'original'
original.mkdir(exist_ok=True)
for source in (MAIN, MAIN.with_suffix('.pdf'), ROOT / '.latexmkrc'):
    assert source.exists(), source
    target = original / source.name
    if target.exists():
        assert target.read_bytes() == source.read_bytes()
    else:
        shutil.copy2(source, target)
source_proof = ROOT / 'output/research/proof-simplification-20261010/path232/deletion_profile/table-free-safe-proof-candidate-v2.tex'
shutil.copy2(source_proof, WORK / 'source-proof-v2.tex')
shutil.copy2(ROOT / '.latexmkrc', WORK / '.latexmkrc')
before = MAIN.read_text()
start = before.index('\\begin{proof}', before.index('\\begin{lemma}[Safe common edges]'))
end = before.index('\\end{proof}', start) + len('\\end{proof}')
proof = r'''\begin{proof}
We first record a cycle-deletion count. Let $C,D$ be cycles with
$U=V(C)\cap V(D)\ne\varnothing$, and let $H$ be a graph on $U$
containing their edges with both endpoints in $U$. Put $n=|U|$,
$m=|E(H)|$, and let $F\subseteq E(H)$ be a forbidden set of size $f$.
In the respective cycles, suppose the vertices outside $U$ induce
$q_C,q_D$ paths, counting isolated vertices and assigning zero to an
empty outside set. If at least $k$ edges of $E(H)\setminus F$ are
used by neither cycle, then their common edges outside $F$ number at least
\[
 2n-q_C-q_D-m-f+k.
\]
Indeed, each cycle retains at least $n-q-f$ edges outside $F$,
in a common universe of at most $m-f-k$ edges; apply inclusion--exclusion.

Let $a,b,c,d$ be distinct colours. Write $E,M,A$ for the end-change,
middle-change, and all-distinct types, ordered $E<M<A$, and allow reversal.
The good target families, excluding targets of smaller type, are
\[
E(aab):aac,abb,acb,bab,cab;\qquad
M(aba):aca,cba;\qquad A(abc):abd,adc.
\]
These exhaust one-coordinate changes up to colour permutations and
reversal. Here $E(aab)$ and $A(abc)$ denote the allowed edge sets at
the indicated boundaries. Write $M_0(aba)$ for the image of $D_M$
under $(0,1,2,3)\mapsto(a,b,c,d)$, and $M_1$ for its reversal.
Unused-colour interchange fixes $E,M_0,M_1$, and reversal followed
by endpoint-colour interchange fixes $A$. Thus $E,A$ have unique
allowed edge sets, and $M$ has the two stated sets.

For six families take $H$ to be the recolouring graph induced by
$U=B_t\cap B_s$ and $F=(P_t\cup P_s)\cap E(H)$.
The following bounds have $q_C+q_D\le r$:
\[
\begin{array}{c|rrrrr|r}
t\to s&n&m&f&r&k&\text{bound}\\\hline
aab\to aac&10&13&2&2&0&3\\
aab\to acb&10&15&1&2&0&2\\
aab\to cab&9&11&1&4&0&2\\
abc\to abd&11&17&0&4&2&3\\
aab\to bab&10&15&0&5&2&2\\
aba\to cba&12&21&0&4&3&2
\end{array}
\]
Their fixed-middle layers are respectively
$(C_4,C_4,K_2)$, $(K_2\square K_3,C_4)$, $(K_3,C_4,K_2)$,
$(K_3,C_4,C_4)$, $(K_2\square K_3,K_2,K_2)$, and
$(K_2\square K_3,C_4,K_2)$, with four, two, three, six, four,
and seven middle-change edges. These give $n,m$.
The two special edges of $E(aab)$ are $bcd$--$dcd$ and $bdc$--$cdc$:
one from each $E$ side survives in the first graph, one source edge
in either following graph, and neither in $aab\to bab$.

For $abc\to abd$, both cycles omit $bab$--$cab$ and $bab$--$dab$:
their middle-$a$ paths start at $bab$ by changing the last coordinate
to the unused colour. For $aab\to bab$, each row triangle of the
common middle-$b$ prism retains one $E$ edge. In either row $M_0$
retains two edges including this edge, and $M_1$ retains one; at
least one edge in each row is unused by both. For $aba\to cba$,
the $M$ middle-$a$ grid isolates $bab$, while the $A$ path begins
$bab,dab$; both omit $bab$--$bac$ and $bab$--$bad$. Every inter-grid
edge of either selected family has endpoint colour $b$, so both
also omit $dad$--$dcd$. These prove the positive values of $k$.

For $aab\to abb$, both cycles retain the two edges at $bca$ of the
common middle-$c$ square; their special edges at its opposite corner
$dcd$ are absent from the other cycle. For $abc\to adc$, both retain
five of the common hexagon
$(bab,bad,cad,dad,dab,cab,bab)$, hence share four. For $aba\to aca$,
each retains three of four edges of $Q_d\subset B_{aaa}$, hence
two common edges. The latter two families have no special edges.

The outside-path bounds in the displayed array follow from these
deletion profiles in the respective selected cycles of
\eqref{eq:path232-cycles}. In $E(aab)$, classes
$w=c,v=c,u=c,u=b$ induce respectively $P_4,P_4,P_3\cup P_2,2P_2$.
In $A(abc)$, classes $v=a,u=b,w=d,u=c$ induce respectively
$P_6,P_4\cup P_3,P_3\cup P_2,P_3\cup P_1$.
In $M_0(aba)$, classes $u=b,w=b,u=c,w=c$ induce respectively
$P_3\cup2P_2,P_5\cup P_2,P_3\cup P_2,P_4\cup P_1$;
reversal gives the profiles for $M_1$. Each is obtained by retaining
the stated coordinate class in the cyclic word. The same words give
all grid-retention and omission properties above. Colour permutations
and reversal preserve special edges and transport every argument,
proving the assertion for all allowed cycles at every labelled interface.
\end{proof}'''
after = before[:start] + proof + before[end:]
old_intro = ('The fibres $B_t$, allowed colour images and path reversals, and special\n'
             'edge sets $P_t$ are defined in the main text. The following literal\n'
             'cycles and interface witnesses supply the finite input to\n'
             'Lemma~\\ref{lem:pathsafe}.')
new_intro = ('The fibres $B_t$, allowed colour images and path reversals, and special\n'
             'edge sets $P_t$ are defined in the main text. The following literal\n'
             'cycles supply the selected-cycle identities used in\n'
             'Lemma~\\ref{lem:pathsafe}.')
assert after.count(old_intro) == 1
after = after.replace(old_intro, new_intro)
start = after.index('\\subsection{Safe common-edge witnesses}')
end = after.index('\\clearpage', start)
after = after[:start] + after[end:]
verification = ('The $(2,3,2)$-path proof uses the three displayed cycles, twelve\n'
                'coordinate-class deletion profiles, and six counting bounds in\n'
                'Lemma~\\ref{lem:pathsafe}, replacing the common-edge witness table.\n\n')
anchor = 'All arbitrary-order assertions in this paper are supplied by the analytic inductions:'
assert after.count(anchor) == 1
after = after.replace(anchor, verification + anchor)
candidate = WORK / 'simplification-candidate-v1.tex'
assert not candidate.exists(), 'Frozen v1 already exists'
candidate.write_text(after)
assert sha(MAIN) == EXPECTED
print(f'original {EXPECTED}\ncandidate {sha(candidate)}')
