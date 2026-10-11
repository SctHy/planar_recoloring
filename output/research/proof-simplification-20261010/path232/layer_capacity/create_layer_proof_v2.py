#!/usr/bin/env python3
"""Only the authorized separation: preserve frozen mathematical v1."""
from pathlib import Path
import hashlib
BASE=Path(__file__).resolve().parent
first=BASE/'layer-proof-candidate-v1.tex';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(first)=='7d8db274e8529a31261988b92e2908852a3422952f0c77f5cdda4a5151800d08'
s=first.read_text()
oldproof=s.split('% BEGIN SAFE-PROOF\n',1)[1].split('% END SAFE-PROOF',1)[0].rstrip()
exceptions=oldproof[oldproof.index('For $aab\\to bab$'):oldproof.index('\\end{proof}')]
proof=r'''\begin{proof}
Partition the common fibre graph into its fixed-middle layers $H_v$
and the edge set $H_*$ changing the middle coordinate. In any block,
if $m$ edges remain outside $P_t\cup P_s$ and the two cycles retain
$x,y$ of them, they share at least $\max(0,x+y-m)$ safe edges.
These bounds add over disjoint blocks. Appendix~\ref{app:path232-certificates}
classifies all allowed transitions and gives sufficient block counts
for seven families, each yielding at least two.

Let $a,b,c,d$ be distinct and use the selected cycles defined there.
''' + exceptions + '\\end{proof}'
counts=oldproof[oldproof.index('\\[\n\\begin{array}{c|c|c}'):oldproof.index('Thus each gives at least two.')]
cross=s[s.index('Each cycle has four middle-changing edges.'):s.index('% END SELECTED-SUPPORT')].rstrip()
support=r'''\subsection{Selected-layer identities and capacities}
Order the end-, middle-, and all-distinct types as $E<M<A$.
For distinct $a,b,c,d$, let $E(aab),M_0(aba),A(abc)$ be the images of
$D_E,D_M,D_A$ under $(0,1,2,3)\mapsto(a,b,c,d)$, and let $M_1$ be
the reversal of $M_0$. Unused-colour interchange fixes $E,M_0,M_1$;
reversal followed by endpoint-colour interchange fixes $A$. Thus
$E,A$ each have one allowed edge set and $M$ has the two stated sets.
Up to these symmetries, the good transitions to a type no smaller are
\[
E(aab):aac,abb,acb,bab,cab;\quad
M(aba):aca,cba;\quad A(abc):abd,adc.
\]
These exhaust one-coordinate changes; bad targets and smaller types
are excluded, and unused colours and the two ends are identified
by the stated symmetries.

In $E(aab)$, the middle-$b$ layer is $2P_3$ and the middle-$c,d$
squares are $P_4$. In $M_0(aba)$, the middle-$a$ layer is $P_8$
with isolated $bab$, and the middle-$c,d$ squares are $P_4$;
reverse for $M_1$. In $A(abc)$, the middle-$a,c$ layers are $P_6$
and the middle-$d$ square is $P_3$ with isolated $bdb$.
These are subgraphs of the respective selected cycles.

''' + cross + r'''

For common endpoint lists $L,R$, the layer $H_v$ is
$K_{|L\setminus\{v\}|}\square K_{|R\setminus\{v\}|}$, and there are
$|L\setminus\{v,w\}|\,|R\setminus\{v,w\}|$ edges between middle
colours $v,w$. Removing the special edges gives the safe universe
size $m$; the original cyclic words give the retained counts $x,y$.
The following seven families supply the capacities used in the proof:
''' + counts.rstrip()
new='% Separated candidate v2; frozen v1 and main are unchanged.\n% BEGIN SAFE-PROOF\n'+proof+'\n% END SAFE-PROOF\n\n% BEGIN SELECTED-SUPPORT\n'+support+'\n% END SELECTED-SUPPORT\n'
target=BASE/'layer-proof-candidate-v2.tex';assert not target.exists();target.write_text(new)
print(sha(target))
