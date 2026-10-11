#!/usr/bin/env python3
"""Separate supporting identities into the appendix without changing v1."""
from pathlib import Path
import hashlib

WORK = Path(__file__).resolve().parent
first = WORK / 'simplification-candidate-v1.tex'
assert hashlib.sha256(first.read_bytes()).hexdigest() == '054e8162ebfd8f15e536e82a22e548c71906b8ea9735b62c983cd2d500d4bdc0'
text = first.read_text()
start = text.index('Let $a,b,c,d$ be distinct colours.', text.index('\\begin{lemma}[Safe common edges]'))
end = text.index('For six families take $H$', start)
text = text[:start] + r'''Let $a,b,c,d$ be distinct colours. Write $E,M,A$ for the end-change,
middle-change, and all-distinct types, ordered $E<M<A$, and allow reversal.
Appendix~\ref{app:path232-certificates} defines the two middle-cycle
edge sets $M_0,M_1$ and verifies that the good target families,
excluding smaller types, are
\[
E(aab):aac,abb,acb,bab,cab;\qquad
M(aba):aca,cba;\qquad A(abc):abd,adc.
\]
''' + text[end:]
start = text.index('The outside-path bounds in the displayed array', text.index('\\begin{lemma}[Safe common edges]'))
end = text.index('\\end{proof}', start)
text = text[:start] + r'''The selected-cycle deletion profiles in
Appendix~\ref{app:path232-certificates} give the stated bounds on
$q_C+q_D$. The same cyclic words verify all the grid-retention and
omission identities above. Colour permutations and reversal preserve
special edges and transport every argument, proving the assertion
for all allowed cycles at every labelled interface.
''' + text[end:]
start = text.index('\\end{equation}', text.index('\\label{eq:path232-cycles}')) + len('\\end{equation}')
support = r'''

\subsection{Selected-cycle identities}
Let $a,b,c,d$ be distinct colours. Write $E(aab)$ and $A(abc)$ for
the images of $D_E,D_A$ under $(0,1,2,3)\mapsto(a,b,c,d)$.
Write $M_0(aba)$ for the corresponding image of $D_M$, and $M_1$
for its reversal. Unused-colour interchange fixes $E,M_0,M_1$;
reversal followed by endpoint-colour interchange fixes $A$.
Thus $E,A$ have unique allowed edge sets, and $M$ has the two stated sets.

The nine families in the proof of Lemma~\ref{lem:pathsafe} exhaust
one-coordinate changes up to these symmetries. For $aab$, changing
the last, middle, or first coordinate gives respectively $aac$,
$abb,acb$, or $bab,cab$. For $aba$, changing the middle or an end
gives $aca$ or $cba$; for $abc$, changing an end or the middle
gives $abd$ or $adc$. Changes to bad boundaries or smaller types
are excluded; unused colours and the two end positions are identified
by colour permutations and reversal.

The following coordinate classes induce the stated paths in the
respective selected cycles, not in the full fibre graphs.
In $E(aab)$, classes $w=c,v=c,u=c,u=b$ induce respectively
$P_4,P_4,P_3\cup P_2,2P_2$.
In $A(abc)$, classes $v=a,u=b,w=d,u=c$ induce respectively
$P_6,P_4\cup P_3,P_3\cup P_2,P_3\cup P_1$.
In $M_0(aba)$, classes $u=b,w=b,u=c,w=c$ induce respectively
$P_3\cup2P_2,P_5\cup P_2,P_3\cup P_2,P_4\cup P_1$;
reversal gives the profiles for $M_1$. Each identity is obtained
by retaining the stated coordinate class in \eqref{eq:path232-cycles}.
'''
text = text[:start] + support + text[start:]
target = WORK / 'simplification-candidate-v2.tex'
assert not target.exists(), 'Frozen v2 already exists'
target.write_text(text)
print(hashlib.sha256(target.read_bytes()).hexdigest())
