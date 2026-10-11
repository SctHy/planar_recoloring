from pathlib import Path
import re, json, hashlib
root=Path('/Users/huahua815/Downloads/planar_recoloring')
work=root/'output/editorial/table-relocation-20261009-185213'
path=root/'planar_recoloring_hamilton_thresholds.tex'
old=(work/path.name).read_text()
s=old

def replace(a,b):
 global s
 assert s.count(a)==1, (a[:100],s.count(a))
 s=s.replace(a,b,1)

def segment(start,end):
 a=old.index(start)
 b=old.index(end,a)+len(end)
 return old[a:b]

summary=segment(r'\begin{center}',r'\end{center}')
counts=segment('\\[\n\\begin{array}{c|r|r|r}', '\\end{array}\n\\]')
words=segment(r'\paragraph{The 53 endpoint words.}', '01 21 31 32 30 20 10 13 12 02 03 23\n\\end{verbatim}')
cycles=segment('\\[\n\\begin{array}{c|l}\n001', '\\end{array}                                                     \\tag{8}\n\\]')
witness=segment('Number source edges in (8)', r'\end{center}')
factors=segment('\\[\n\\begin{array}{c|r|l@{\\qquad}c|r|l}', '\\end{array}\n\\]')

replace(r'\usepackage{microtype,enumitem,needspace}',r'\usepackage{microtype,enumitem,needspace,booktabs}')
replace(r'\numberwithin{equation}{section}', '\\numberwithin{equation}{section}\n\\numberwithin{table}{section}')
replace('The principal conclusions are summarized below.', 'The principal conclusions are summarized in Table~\\ref{tab:threshold-summary}\nin Appendix~\\ref{app:threshold-summary}.')
replace(summary,'')
replace('The explicit words below prove every positive assertion:', 'The explicit words in Appendix~\\ref{app:pair-five-certificates}\nprove every positive assertion:')
replace('path reversal.  The resulting endpoint pairs have the counts in the\nfollowing table, covering all claimed positive pairs.', 'path reversal.  The resulting endpoint pairs have the counts in\nTable~\\ref{tab:pair-five-counts}, covering all claimed positive pairs.')
replace(counts,'')
replace(words,'')
replace('In the following cyclic words the coordinates are $uvw$:\n'+cycles, 'The cycles $D_E,D_M,D_A$ for the normalized boundaries $001,010,012$\nare specified in~\\eqref{eq:path232-cycles} in\nAppendix~\\ref{app:path232-certificates}; the coordinates are $uvw$.')
replace('Call these cycles $D_E,D_M,D_A$, and allow all their colour images and\npath reversals.', 'Allow all their colour images and path reversals.')
replace(witness, 'The edge numbering and target-column conventions are specified in\nAppendix~\\ref{app:path232-certificates}.\nTable~\\ref{tab:path232-safe-edges} supplies two safe common source-edge\nindices for every normalized source and allowed target cycle.')
replace('six from $010$, and three from $012$, exactly the seventeen rows above.', 'six from $010$, and three from $012$, exactly the seventeen rows of\nTable~\\ref{tab:path232-safe-edges}.')
replace('Hamilton-connectedness at four colours.  The local finite inputs are recorded below.  Their finite parts classify', 'Hamilton-connectedness at four colours.  The local models are defined\nbelow and their literal certificates are recorded in the appendices.\nTheir finite parts classify')
replace('least three, its list recolouring graph has such a factor.', 'least three, its list recolouring graph has a spanning factor whose\ncomponents are edges, triangles, or $15$-cycles.')
replace('boundary types and factors are as follows.\n'+factors, 'boundary types and factors are listed in\nTable~\\ref{tab:pentagon-factors} in Appendix~\\ref{app:pentagon-factor-words}.')
s=s.replace('(8)',r'\eqref{eq:path232-cycles}')

# Reuse every data row; only table rules, wrappers, and labels change.
summary_table=summary.replace(r'\begin{center}', '\\begin{table}[htbp]\n\\centering\\small\n\\setlength{\\tabcolsep}{4pt}\n\\caption{Hamiltonian and Hamilton-connected thresholds for the graph classes considered.}\n\\label{tab:threshold-summary}')
summary_table=summary_table.replace(r'p{0.32\linewidth}c c p{0.34\linewidth}',r'p{0.30\linewidth}c c p{0.32\linewidth}')
summary_table=summary_table.replace(r'\hline',r'\toprule',1).replace(r'\hline',r'\midrule',1).replace(r'\hline',r'\bottomrule',1)
summary_table=summary_table.replace(r'\end{center}',r'\end{table}')

counts_table=r'''\begin{table}[htbp]
\centering
\caption{Adjacent-pair endpoint certificates and their symmetry coverage.}
\label{tab:pair-five-counts}
\begin{tabular}{crrr}
\toprule
Type & $|V(F)|$ & Words & Feasible unordered pairs\\
\midrule
'''+counts.split('\\\\\\hline\n',1)[1].split('\n\\end{array}',1)[0]+r'''\\
\bottomrule
\end{tabular}
\end{table}'''

cycles_eq=cycles.replace('\\[\n','\\begin{equation}\n\\label{eq:path232-cycles}\n',1)
cycles_eq=cycles_eq.replace('                                                     \\tag{8}', '').replace('\n\\]','\n\\end{equation}')

witness_appendix=witness.replace('Number source edges in (8) cyclically from one. The following explicit\nwitness table supplies two safe common source-edge indices in every\ncase.', 'Number source edges in~\\eqref{eq:path232-cycles} cyclically from one.\nTable~\\ref{tab:path232-safe-edges} supplies two safe common source-edge\nindices in every case.')
witness_appendix=witness_appendix.replace(r'\begin{center}\small', '\\begin{table}[htbp]\n\\centering\\small\n\\renewcommand{\\arraystretch}{1.1}\n\\caption{Safe common source-edge indices for adjacent good boundaries.}\n\\label{tab:path232-safe-edges}')
witness_appendix=witness_appendix.replace(r'\begin{tabular}{cc|cccc}', '\\begin{tabular}{cccccc}\n\\toprule')
witness_appendix=witness_appendix.replace(r'\\\hline', '\\\\\n\\midrule').replace(r'\end{tabular}', '\\bottomrule\n\\end{tabular}').replace(r'\end{center}',r'\end{table}')

factor_table=r'''\begin{table}[htbp]
\centering
\caption{Spanning factors for the eleven normalized pentagon boundary types.}
\label{tab:pentagon-factors}
$\begin{array}{crl@{\qquad}crl}
\toprule
t & |F_t| & \text{Factor} & t & |F_t| & \text{Factor}\\
\midrule
'''+factors.split('\\\\\\hline\n',1)[1].split('\n\\end{array}',1)[0]+r'''\\
\bottomrule
\end{array}$
\end{table}'''

new_appendices=r'''\clearpage
\appendix
\section{Summary of threshold results}
\label{app:threshold-summary}
Table~\ref{tab:threshold-summary} collects the conclusions proved in the
main text. A range records a proved lower and upper bound; the
four-colour statement between them remains unresolved.

'''+summary_table+r'''

\clearpage
\section{Adjacent-pair endpoint certificates}
\label{app:pair-five-certificates}
These certificates use the graph $F(A,B)$ and the type
$(|A|,|B|,|A\cap B|)$ defined before
Lemma~\ref{lem:pair-five-endpoints}. The two-digit word $ab$ denotes
$(a,b)$. Each displayed word lists all states once, with consecutive
states differing in one coordinate; the $333$ word is cyclic.
The counts in Table~\ref{tab:pair-five-counts} include all colour
permutations preserving the listed pair of lists, coordinate exchange
when it preserves the type, and path reversal. The proof of
Lemma~\ref{lem:pair-five-endpoints} gives the negative witnesses for the
excluded endpoint pairs.

'''+counts_table+'\n\n'+words+r'''

\clearpage
\section{Certificates for the \texorpdfstring{$(2,3,2)$}{(2,3,2)}-path restoration}
\label{app:path232-certificates}
The fibres $B_t$, allowed colour images and path reversals, and special
edge sets $P_t$ are defined in the main text. The following literal
cycles and interface witnesses supply the finite input to
Lemma~\ref{lem:pathsafe}.

\subsection{The three normalized cycles}
In the cyclic words below the coordinates are $uvw$. The rows for
$001,010,012$ specify $D_E,D_M,D_A$, respectively.

'''+cycles_eq+r'''

\subsection{Safe common-edge witnesses}
'''+witness_appendix+r'''
\clearpage
'''
replace('\\appendix\n',new_appendices)
replace('These literal identities are part of the proof, not solver verdicts.\n\\paragraph{Factor 00000', 'These literal identities are part of the proof, not solver verdicts.\n\n'+factor_table+'\n\n\\paragraph{Factor 00000')
path.write_text(s)

# Compare literal payloads and all original numerical table rows.
def literal_blocks(text):
 marked=re.findall(r'% BEGIN ([^\n]+)\n(.*?)% END \1',text,re.S)
 verbatim=re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',text,re.S)
 return marked,verbatim
assert literal_blocks(old)==literal_blocks(s),'Literal certificate changed'
for block in (summary,counts,witness,factors):
 rows=[line.strip() for line in block.splitlines() if '&' in line and not ('text{' in line or 'Graph class' in line or '$t$ & $s$' in line or line.startswith('t&'))]
 for row in rows:
  assert row.rstrip('\\') in s, ('Missing numerical row',row)
assert '\\tag{8}' not in s and '(8)' not in s
# All theorem/lemma/etc labels and statements stay, except the ambiguous factor wording.
for kind in ('theorem','lemma','proposition','corollary'):
 before=re.findall(r'\\begin\{'+kind+r'\}(.*?)\\end\{'+kind+r'\}',old,re.S)
 after=re.findall(r'\\begin\{'+kind+r'\}(.*?)\\end\{'+kind+r'\}',s,re.S)
 assert len(before)==len(after),(kind,len(before),len(after))
 for a,b in zip(before,after):
  if a!=b:
   assert 'lem:pentagon-list-factor' in a and 'lem:pentagon-list-factor' in b,(kind,a[:100])
report={
 'source':str(path), 'original_sha256':hashlib.sha256(old.encode()).hexdigest(),
 'edited_sha256':hashlib.sha256(s.encode()).hexdigest(),
 'marked_certificate_blocks_unchanged':len(literal_blocks(s)[0]),
 'verbatim_certificate_blocks_unchanged':len(literal_blocks(s)[1]),
 'original_numerical_table_rows_preserved':True,
 'theorem_and_lemma_statements_preserved_except_factor_definition_clarification':True,
 'appendix_sections':re.findall(r'\\section\{([^\n]+)\}',s.split('\\appendix',1)[1]),
 'mathematical_revalidation_performed':False
}
(work/'integrity-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
