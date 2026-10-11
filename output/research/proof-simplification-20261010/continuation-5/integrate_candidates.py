from pathlib import Path
import hashlib,re,shutil,json

root=Path('/Users/huahua815/Downloads/planar_recoloring')
work=root/'output/research/proof-simplification-20261010/continuation-5'
source=root/'planar_recoloring_hamilton_thresholds.tex'
before=source.read_text()
assert hashlib.sha256(source.read_bytes()).hexdigest()=='6ae559d6418dd963f5093ab700deb5f36b2385f130d657b20916096a55b24227'
original=work/'original'; original.mkdir(exist_ok=True)
for ext in ('tex','pdf'):
    p=source.with_suffix('.'+ext); assert not (original/p.name).exists(); shutil.copy2(p,original/p.name)
s=before
def replace(old,new):
    global s
    assert s.count(old)==1,old[:100]
    s=s.replace(old,new)

start=s.index(r'\begin{proof}',s.index(r'\label{lem:adjacent-two-four}'))
end=s.index(r'\end{proof}',start)+len(r'\end{proof}')
s=s[:start]+r'''\begin{proof}
For a base colouring $f$, the extension fibre is $F(A,B)$, where
$A=[4]\setminus\{f(x)\}$ and $B=[4]\setminus\{f(y)\}$.
For $A=B=\{a,b,c\}$ use the cycle $(ab,ac,bc,ba,ca,cb)$;
for $A=\{a,b,c\}$, $B=\{a,b,d\}$ use
$(ab,ad,bd,ba,ca,cd,cb)$.

In fact, any two fibre Hamilton cycles have at least two common
edges when at most one list changes. For an unchanged fibre, equal
lists give $C_6$, while unequal lists give four distinct forced
edges at the two degree-two states using the common colours.
By exchanging coordinates suppose only $A$ changes. If one value
equals $B=\{a,b,c\}$, the common fibre is the path
$(ab,ac,bc,ba)$; its two end edges are forced in both cycles.
Otherwise let $a,b$ be the old and new excluded colours, $c$ the
fixed excluded colour and $d$ the fourth colour. The common fibre
has five vertices $ca,cb,cd,da,db$ and six edges. The old outside
states $ba,bd$ occur consecutively because $bd$ has degree two
with neighbours $ba,cd$. Thus the old cycle uses exactly four
common-fibre edges; the new cycle does likewise with $ab,ad,cd$.
The cycles share at least $4+4-6=2$ edges.

Since $x\ne y$, a base step changes at most one list. Cut an edge
of a base Hamilton cycle and process its fibres in path order.
At each splice the current fibre has lost at most one edge and the
next is fresh, so a common edge remains. Cutting its two copies
and adding the two actual base-step edges merges the circles.
The fibres partition all states, giving a spanning cycle.
\end{proof}'''+s[end:]

replace(r'''For a hard component, specify cycles of $A\square P_2$ and
$A\square P_3$, and a set $D_A$ of internal edges occurring in
\emph{every} row of both seeds. We use new seeds for $00001$ with
$|D_A|=19$ and the earlier seeds for $00112$ with $|D_A|=18$.
Designate a seven-edge pool in $D_A$, and put $K_A=D_A\setminus
\text{pool}$. Any two pool edges supply splice reserves. All pool edges are distinct.''',r'''For a hard component, specify cycles of $A\square P_2$ and
$A\square P_3$, and a set $D_A$ of internal edges occurring in
\emph{every} row of both seeds. For $00001$ use the printed seeds
with $|D_A|=19$ and a seven-edge pool. For $00112$ use the printed
two-row cycle and the three-row construction below, with
$|D_A|=13$ and a two-edge pool. Put $K_A=D_A\setminus\text{pool}$.
Any two pool edges supply splice reserves. All pool edges are distinct.''')
replace(r'''give their specified component cycles and the two hard seeds: their
entries are precisely the legal words, without repetition, and
successive entries, including last and first, differ in one coordinate.
Every listed common edge occurs in all five seed rows.''',r'''give their specified component cycles and the printed hard seeds:
their entries are precisely the legal words, without repetition,
and successive entries, including last and first, differ in one
coordinate. The three-row seed for $00112$ instead follows by
inserting two edges and the displayed 47-state path into its
two-row cycle, as proved in the appendix. Every listed common
edge occurs in every row of both corresponding seeds.''')
replace(r'''cycles are printed separately. Cycle words are cyclic; the
$00112$ path below is linear. A port is a pair of five-digit words.''',r'''cycles are printed separately. Cycle words are cyclic; the
51-state and 47-state paths for $00112$ are linear.
A port is a pair of five-digit words.''')

a=s.index(r'\paragraph{C3 for 00112 (153 words).}')
b=s.index('% END PORTS-00112',a)+len('% END PORTS-00112')
insertion=(root/'output/research/proof-simplification-20261010/protected_products/row_insert_00112/candidate-v3.tex').read_text()
block=re.search(r'^% BEGIN COREPATH-00112\n.*?^% END COREPATH-00112$',insertion,re.S|re.M).group(0)
ports=re.search(r'^% BEGIN PORTS-00112-INSERTION\n.*?^% END PORTS-00112-INSERTION$',insertion,re.S|re.M).group(0).replace('PORTS-00112-INSERTION','PORTS-00112')
replacement=r'''\paragraph{Common ports 00112 (13 edges).}
'''+ports+r'''
\paragraph{Generating the three-row seed for 00112.}
Let $D_A$ be the thirteen ports above, with pool
$\{e,f\}=\{21020\text{--}23020,21030\text{--}31030\}$, and set
$K_A=D_A\setminus\{e,f\}$. All thirteen edges occur in both rows
of the printed $C_2$.
The following path $P$ contains forty-seven distinct states and
all edges of $D_A$. Together with $12303,12323,13203,23203$,
its vertices are precisely the legal states of $00112$.
'''+block+r'''
In the second old row (leading digit $1$), cut the three edges
\[
12303\text{--}12323,\qquad13203\text{--}23203,\qquad
21201\text{--}23201.
\]
In the new row (leading digit $2$), use the first two displayed
edges and $P$. Replace each cut edge $(1,u)(1,v)$ by the corresponding
new-row path and its two cross edges $(1,u)(2,u)$, $(1,v)(2,v)$.
These replacement paths have the same old endpoints, are internally
disjoint and partition the new row. Thus they subdivide three edges
of $C_2$ and give a single Hamilton cycle of $A\square P_3$.
No cut edge belongs to $D_A$, and the new row contains every edge
of $D_A$, so all thirteen ports survive in every row.'''
s=s[:a]+replacement+s[b:]
replace(r'''12020-12030 12320-12323 13020-13030 21020-23020\\
21021-21031 21030-31030 32021-32031\\''',r'''21020-23020 21030-31030\\''')
replace(r'''The ordered path blocks in Lemma~\ref{lem:pentagon-path-blocks} use the existing component cycles, the 51-state path for $00112$, and the 22-edge chain for $00001$.''',r'''The ordered path blocks in Lemma~\ref{lem:pentagon-path-blocks} use the existing component cycles, the 51-state path for $00112$, and the 22-edge chain for $00001$. The separate 47-state path generates the $00112$ three-row seed by three edge substitutions, retaining its thirteen common ports; its eleven-edge protected set is unchanged.''')
(work/'simplification-candidate.tex').write_text(s)
print(json.dumps({'candidate_sha256':hashlib.sha256(s.encode()).hexdigest(),'bytes':len(s.encode()),'removed_C3_words':153,'new_core_path_words':47,'unchanged_K00112_edges':11},indent=2))
