#!/usr/bin/env python3
"""Adapt the frozen layer mechanism into a separate complete manuscript."""
from pathlib import Path
import hashlib,shutil
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[4]
MAIN=ROOT/'planar_recoloring_hamilton_thresholds.tex'
EXPECTED='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(MAIN)==EXPECTED
original=BASE/'original';original.mkdir(exist_ok=True)
for p in (MAIN,MAIN.with_suffix('.pdf'),ROOT/'.latexmkrc'):
    q=original/p.name
    if q.exists():assert q.read_bytes()==p.read_bytes()
    else:shutil.copy2(p,q)
shutil.copy2(ROOT/'.latexmkrc',BASE/'.latexmkrc')
local=ROOT/'output/research/proof-simplification-20261010/path232/layer_capacity/layer-proof-candidate-v2.tex'
shutil.copy2(local,BASE/'layer-proof-input-v2.tex')
data=local.read_text()
segment=lambda name:data.split('% BEGIN '+name+'\n',1)[1].split('% END '+name,1)[0].rstrip()
before=MAIN.read_text();after=before
start=after.index('\\begin{proof}',after.index('\\begin{lemma}[Safe common edges]'));end=after.index('\\end{proof}',start)+len('\\end{proof}')
after=after[:start]+segment('SAFE-PROOF')+after[end:]
old=('The fibres $B_t$, allowed colour images and path reversals, and special\n'
     'edge sets $P_t$ are defined in the main text. The following literal\n'
     'cycles and interface witnesses supply the finite input to\n'
     'Lemma~\\ref{lem:pathsafe}.')
new=('The fibres $B_t$, allowed colour images and path reversals, and special\n'
     'edge sets $P_t$ are defined in the main text. The following literal\n'
     'cycles supply the selected-layer identities used in\n'
     'Lemma~\\ref{lem:pathsafe}.')
assert after.count(old)==1;after=after.replace(old,new)
start=after.index('\\subsection{Safe common-edge witnesses}');end=after.index('\\clearpage',start)
after=after[:start]+segment('SELECTED-SUPPORT')+'\n'+after[end:]
verification=('For $(2,3,2)$-path restoration, the three displayed cycles are used\n'
              'through fixed-middle-layer and middle-change-edge capacity bounds\n'
              'rather than an interface witness table.\n\n')
anchor='All arbitrary-order assertions in this paper are supplied by the analytic inductions:'
assert after.count(anchor)==1;after=after.replace(anchor,verification+anchor)
target=BASE/'layer-capacity-manuscript-candidate-v2.tex';assert not target.exists()
target.write_text(after);assert sha(MAIN)==EXPECTED
print(sha(target))
