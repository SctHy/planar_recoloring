from pathlib import Path
import hashlib, json, re, shutil, difflib

root = Path('/Users/huahua815/Downloads/planar_recoloring')
base = root / 'output/research/proof-simplification-20261010'
work = base / 'continuation-3'
review = base / 'tree_gluing/constant_pool_review'
source = root / 'planar_recoloring_hamilton_thresholds.tex'
before = source.read_text()
assert hashlib.sha256(source.read_bytes()).hexdigest() == '9badcff3587c8d0832790259d3a190f8e88d91dc0052300b5fd142ec196f9610'
(work/'original').mkdir(exist_ok=True)
manifest = {}
for ext in ('tex', 'pdf'):
    p = source.with_suffix('.'+ext)
    shutil.copy2(p, work/'original'/p.name)
    manifest[p.name] = {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes':p.stat().st_size}
(work/'original-manifest.json').write_text(json.dumps({'files':manifest},indent=2)+'\n')

start = before.index(r'\subsection{Listed pentagon factors}')
end = before.index(r'\subsection{The finite protected-edge identities}', start)
after = before[:start] + before[end:]
start = after.index(r'\begin{lemma}\label{lem:listed-pentagon-degree}')
end = after.index(r'\begin{lemma}\label{lem:protected-product}', start)
after = after[:start] + after[end:]

local = r'''
\begin{lemma}[Ordered path blocks]\label{lem:pentagon-path-blocks}
Every one of the 23 component types $B$ has a partition into paths
$P_1,\ldots,P_r$ of order two or three, with an actual $B$ edge
joining $P_i$ to $P_{i+1}$ for each $i<r$.
\end{lemma}
\begin{proof}
Twenty-one types have the printed Hamilton cycles, and $00112$ has
the 51-state Hamilton path in Appendix~\ref{app:pentagon-factor-words}.
Delete a cycle edge where necessary, and divide the resulting path
into consecutive two-vertex blocks, with one three-vertex block if
its order is odd. For $00001$, the 22 ordered edges in
Table~\ref{tab:pentagon-matching-chain} cover all 44 states, and the
indicated consecutive connectors are actual $B$ edges. Coverage and
every edge follow by checking the displayed words and one-coordinate
differences.
\end{proof}
'''
needle = 'Thus there are 23 component types, including the two constant components.\n'
assert after.count(needle)==1
after = after.replace(needle, needle+local)

start = after.index(r'\begin{proof}', after.index(r'\label{lem:protected-product}'))
end = after.index(r'\end{proof}', start)+len(r'\end{proof}')
product = r'''\begin{proof}
Use the ordered path blocks of Lemma~\ref{lem:pentagon-path-blocks}
for $B$. On each block construct its product cycle with $A$.
If $A$ has its specified cycle $C_A$, join two copies using the
first pool edge; for a three-row block use the first and second
pool edges at its two interfaces. These cuts are distinct in the
middle row. If $A$ is hard, use its specified two- or three-row seed.
Every initial cycle retains $K_A$ and the same last six pool edges
in every physical row.

Choose two distinct reserve edges $e,f$. Join consecutive block
cycles by cutting their two copies of $e$ or $f$, alternating along
the block chain, and adding the two cross edges supplied by the
indicated actual edge of $B$. Each block participates in at most two
joins. If both use the same physical row, they cut different edges;
thus every required copy is still present. Processing the blocks in
order merges their disjoint cycles into one, covers every row, and
never cuts $K_A$.
\end{proof}'''
after = after[:start]+product+after[end:]

old = r'The path factors now follow analytically from Lemma~\ref{lem:pentagon-list-factor}; the eleven-type factor-word enumeration is no longer a proof premise.'
new = r'The ordered path blocks in Lemma~\ref{lem:pentagon-path-blocks} use the existing component cycles, the 51-state path for $00112$, and the 22-edge chain for $00001$. The eleven-type factor-word enumeration is no longer a proof premise.'
assert after.count(old)==1
after = after.replace(old,new)
after = after.replace(r'\section{Literal pentagon factors and common-port seeds}', r'\section{Literal pentagon cycles, path blocks and common-port seeds}')
old = r'''constant-type component cycles. All Hamilton words are cyclic.
A port is a pair of five-digit words. Path factors are supplied
analytically by Lemma~\ref{lem:pentagon-list-factor}; their eleven-type
word enumeration is not needed.
These literal identities are part of the proof, not solver verdicts.
'''
new = r'''constant-type component cycles. Cycle words are cyclic; the
$00112$ path below is linear. A port is a pair of five-digit words.
The ordered path blocks use the specified cycles and the two
additional identities below; no eleven-type factor-word list is needed.
These literal identities are part of the proof, not solver verdicts.
'''
assert after.count(old)==1
after = after.replace(old,new)

chain = json.loads((review/'matching-chain-00001-literal.json').read_text())
pairs = chain['pairs']; bits=chain['outgoing_endpoint']
assert len(pairs)==22 and len(bits)==21
table = [r'''\begin{table}[!htbp]
\centering\footnotesize\ttfamily
\caption{Ordered pairs for $00001$. Each pair $a_i b_i$ is a block;
the connector to the next block is $a_i a_{i+1}$ when $\epsilon_i=0$
and $b_i a_{i+1}$ when $\epsilon_i=1$.}
\label{tab:pentagon-matching-chain}
% BEGIN MATCHING-CHAIN-00001
\begin{tabular}{rllc@{\qquad}rllc}
$i$ & $a_i$ & $b_i$ & $\epsilon_i$ & $i$ & $a_i$ & $b_i$ & $\epsilon_i$\\
\hline''']
for i in range(11):
    cells=[]
    for j in (i,i+11):
        cells += [str(j+1),*pairs[j],str(bits[j]) if j<21 else '--']
    table.append(' & '.join(cells)+r'\\')
table += [r'\end{tabular}',r'% END MATCHING-CHAIN-00001',r'\end{table}']
path = json.loads((base/'protected_products/traceability_00112/path-results.json').read_text())['path']
assert len(path)==51
hp = [r'\paragraph{Path for 00112 (51 words).}',r'% BEGIN HP-00112',r'\begingroup\footnotesize\ttfamily\begin{flushleft}']
for i in range(0,len(path),10):
    hp.append(' '.join(path[i:i+10])+r'\\')
hp += [r'\end{flushleft}\endgroup',r'% END HP-00112']
extra='\n'.join(table)+'\n\n'+'\n'.join(hp)+'\n\n'
needle = r'\paragraph{Factor 00000 (30 words).}'
assert after.count(needle)==1
after=after.replace(needle,extra+r'\paragraph{Constant-boundary cycles (30 words).}')
after=after.replace('path rows; the last six pool edges supply factor-tree reserves.', 'path rows; any two of the last six pool edges supply block-chain reserves.')
after,n=re.subn(r'\\bibitem\{AAE80\}.*?(?=\\bibitem\{DFFV06\})','',after,flags=re.S)
assert n==1
assert 'pentagon-list-factor' not in after and 'listed-pentagon-degree' not in after and 'AAE80' not in after

blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
oldblocks,newblocks=blocks(before),blocks(after)
assert all(newblocks[k]==v for k,v in oldblocks.items())
assert set(newblocks)-set(oldblocks)=={'MATCHING-CHAIN-00001','HP-00112'}
statements = lambda s, kinds: re.findall(r'\\begin\{('+kinds+r')\}(.*?)\\end\{\1\}',s,re.S)
assert statements(before,'theorem|proposition|corollary')==statements(after,'theorem|proposition|corollary')
oldlem=statements(before,'lemma'); newlem=statements(after,'lemma')
removed=('lem:pentagon-list-factor','lem:listed-pentagon-degree')
assert [x for x in oldlem if not any(k in x[1] for k in removed)]==[x for x in newlem if 'lem:pentagon-path-blocks' not in x[1]]
(work/'ordered-block-candidate.tex').write_text(after)
(work/'ordered-block-candidate.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='ten-entry.tex',tofile='ordered-blocks.tex')))
(work/'candidate-integrity.json').write_text(json.dumps({'main_result_statements_identical':True,'other_lemma_statements_identical':True,'old_finite_blocks_byte_identical':len(oldblocks),'new_finite_blocks':['MATCHING-CHAIN-00001','HP-00112'],'candidate_sha256':hashlib.sha256(after.encode()).hexdigest()},indent=2)+'\n')
print('Candidate written; main source untouched.')
