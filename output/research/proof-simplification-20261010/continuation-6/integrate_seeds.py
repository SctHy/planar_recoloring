from pathlib import Path
import re,json,hashlib,shutil
root=Path('/Users/huahua815/Downloads/planar_recoloring')
base=root/'output/research/proof-simplification-20261010';work=base/'continuation-6'
source=root/'planar_recoloring_hamilton_thresholds.tex'
s=source.read_text()
assert hashlib.sha256(source.read_bytes()).hexdigest()=='85e08613026474c11a5b5a804361070e1a68ca7857ad93f5cc8386bf4549d6f6'
original=work/'original';original.mkdir(exist_ok=True)
for ext in ('tex','pdf'):
    p=source.with_suffix('.'+ext)
    if (original/p.name).exists():assert p.read_bytes()==(original/p.name).read_bytes()
    else:shutil.copy2(p,original/p.name)

candidate=(base/'protected_products/row_insert_00001/candidate-v2.tex').read_text()
assert hashlib.sha256(candidate.encode()).hexdigest()=='94a3d46d7c3c7c65984216924ebd72f315314833a2f9d885679ad1900455d6a4'
c2raw,praw=re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}',candidate,re.S)
C2=c2raw.split();P=praw.split();assert len(C2)==88 and len(P)==40
answer=json.loads((base/'protected_products/row_insert_00001/core40-path-results-v2.json').read_text())['answer']
assert P==answer['core40_path'] and C2==[x for x in answer['derived_C3_words'] if x[0]!='2']
D=answer['D13'];pool=answer['two_reserves'];assert len(D)==13 and len(pool)==2
def replace(old,new):
    global s
    assert s.count(old)==1,old[:100]
    s=s.replace(old,new)
def literal(tag,items,width,size='footnotesize'):
    lines=[' '.join(items[i:i+width])+r'\\' for i in range(0,len(items),width)]
    return f'% BEGIN {tag}\n'+f'\\begingroup\\{size}\\ttfamily\\begin{{flushleft}}\n'+'\n'.join(lines)+'\n'+r'\end{flushleft}\endgroup'+f'\n% END {tag}'

replace(r'''\emph{every} row of both seeds. For $00001$ use the printed seeds
with $|D_A|=19$ and a seven-edge pool. For $00112$ use the printed
two-row cycle and the three-row construction below, with
$|D_A|=13$ and a two-edge pool. Put $K_A=D_A\setminus\text{pool}$.
Any two pool edges supply splice reserves. All pool edges are distinct.''',r'''\emph{every} row of both seeds. For each of $00001$ and $00112$,
the appendix specifies a two-row cycle and derives its three-row
seed by the same three-path insertion rule. Both use $|D_A|=13$
and a two-edge pool. Put $K_A=D_A\setminus\text{pool}$; the two
distinct pool edges supply the splice reserves.''')
replace(r'''give their specified component cycles and the printed hard seeds:
their entries are precisely the legal words, without repetition,
and successive entries, including last and first, differ in one
coordinate. The three-row seed for $00112$ instead follows by
inserting two edges and the displayed 47-state path into its
two-row cycle, as proved in the appendix. Every listed common
edge occurs in every row of both corresponding seeds.''',r'''give their specified component cycles and the two-row hard seeds:
their entries are precisely the legal words, without repetition,
and successive entries, including last and first, differ in one
coordinate. Both three-row seeds follow from the appendix's
three-path insertion rule, using two edges and the displayed
40-state or 47-state path. Every listed common edge occurs in
every row of both corresponding seeds.''')
replace(r'''The separate 47-state path generates the $00112$ three-row seed by three edge substitutions, retaining its thirteen common ports; its eleven-edge protected set is unchanged.''',r'''The separate 40-state and 47-state paths generate both hard three-row seeds by the same three-path insertion rule, retaining thirteen common ports in every row. The $00112$ protected set is unchanged; $00001$ uses eleven protected edges with three repaired individual witnesses.''')

marker='% END C2-00112'
rule=r'''
\paragraph{Three-row insertion rule.}
Let $C_2$ be a Hamilton cycle of $A\square P_2$, with row digits
$0,1$. Suppose its
second row contains three disjoint edges $u_i v_i$, and the states
of $A$ partition into three paths with respective endpoints $u_i,v_i$.
Replace each cut edge $(1,u_i)(1,v_i)$ by its path in row $2$ and
the cross edges at both endpoints. These paths are internally
disjoint and cover the new row, so they subdivide three edges of
$C_2$ into one Hamilton cycle of $A\square P_3$.
If $D_A$ occurs in both old rows and in the new paths, and avoids
the three cut edges, it survives in every row of the derived seed.
'''
replace(marker,marker+rule)
a=s.index(r'\paragraph{Generating the three-row seed for 00112.}')
b=s.index('\n\n\n\\section{Literal protected-pentagon certificates}',a)
core=re.search(r'^% BEGIN COREPATH-00112\n.*?^% END COREPATH-00112$',s[a:b],re.S|re.M).group(0)
s=s[:a]+r'''\paragraph{Generating the three-row seed for 00112.}
The following path $P$ contains forty-seven distinct states and
all thirteen ports above. Together with $12303,12323,13203,23203$,
its vertices are precisely the legal states of $00112$.
'''+core+r'''
In row $1$ of the printed $C_2$, cut
\[
12303\text{--}12323,\qquad13203\text{--}23203,\qquad
21201\text{--}23201.
\]
The new row uses the first two edges as its two-point paths and
$P$ as the third path. All cut edges avoid $D_A$, which occurs
in both rows of $C_2$ and in $P$. The insertion rule therefore
gives the required three-row seed with all thirteen common ports.'''+s[b:]

a=s.index(r'\paragraph{PC2 for 00001 (88 words).}')
b=s.index('% END COMMON-00001',a)+len('% END COMMON-00001')
s=s[:a]+r'''\paragraph{PC2 for 00001 (88 words).}
'''+literal('PC2-00001',C2,9)+r'''
\paragraph{Common ports 00001 (13 edges).}
'''+literal('COMMON-00001',['-'.join(e) for e in D],4)+r'''
\paragraph{Generating the three-row seed for 00001.}
The following path $P$ contains forty distinct states and all
thirteen ports above. Together with $12312,12313,13212,13213$,
its vertices are precisely the legal states of $00001$.
'''+literal('COREPATH-00001',P,10)+r'''
In row $1$ of the printed $C_2$, cut
\[
12312\text{--}12313,\qquad13212\text{--}13213,\qquad
13210\text{--}13230.
\]
The new row uses the first two edges and $P$. All cuts avoid
$D_A$, which occurs in both rows of $C_2$ and in $P$. Apply the
insertion rule in Appendix~\ref{app:pentagon-factor-words} to obtain
the three-row seed, retaining every listed common port.'''+s[b:]
a=s.index('% BEGIN POOL-00001-0');b=s.index('% END POOL-00001-0',a)+len('% END POOL-00001-0')
s=s[:a]+literal('POOL-00001-0',['-'.join(e) for e in pool],2)+s[b:]
for pos,new,target,old,witness in [(1,3,'00102:0','12313-12323','21313-21323'),(4,2,'00001:0','12313-12323','13120-23120'),(4,3,'00001:0','31212-31232','12310-32310')]:
    replace(f'00001:0 {pos} {new} {target} {old}',f'00001:0 {pos} {new} {target} {witness}')

(work/'shared-insertion-candidate.tex').write_text(s)
print(json.dumps({'candidate_sha256':hashlib.sha256(s.encode()).hexdigest(),'bytes':len(s.encode()),'new00001C2_words':88,'new00001core_words':40,'removed00001C3_words':132,'changed_individual_witnesses':3},indent=2))
