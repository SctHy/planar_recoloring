#!/usr/bin/env python3
"""Separate full candidate; exact27 record deletion, old52 blocks retained."""
from pathlib import Path
import hashlib,json,re

HERE=Path(__file__).resolve().parent

LOCAL_LEMMA=r'''\begin{lemma}[One-boundary local cycle intersection]\label{lem:c5-one-boundary-local}
Let ordinary components $A\subseteq F_t$ and $B\subseteq F_{t'}$
meet at $x$, where $t'$ changes entry $j$ from $a$ to $q$.
Use the prescribed restoration for $B$ and its pool $Q$, and let $P$
be the source pool. Put $d=d_A(x)$,
$\alpha=\mathbf1[a\notin\{x_{j-1},x_{j+1}\}]$, and let $f$ count
common incident edges lying in $P\cup Q$.
Every pair of Hamilton cycles of $A,B$ shares at least
$\max\{0,4-d-\alpha-f\}$ incident edges outside both pools.
\end{lemma}
\begin{proof}
Let $\beta$ indicate that recolouring $x_j$ to $q$ is source-legal.
At coordinate $j$, the target loses that mutation and gains the
mutation to $a$ exactly when $\alpha=1$. Thus its degree is
$d+\alpha-\beta$, and the common incident universe has size $d-\beta$.
After deleting $P\cup Q$ its size is $h=d-\beta-f$.
Each cycle uses two incident edges; at most $d-h$ on the source side
and $d+\alpha-\beta-h$ on the target side lie outside this universe.
Inclusion--exclusion gives $4-d-(d+\alpha-\beta)+h=4-d-\alpha-f$.
\end{proof}

'''

SOURCE_FAMILIES=r'''\paragraph{Two ordinary-source families (27 interfaces).}
Put $w=32301$. The two sets below replace all individual records
with these sources. Superscripts list
$J_t(x)=\{j:t_j\in\{x_{j-1},x_{j+1}\}\}$; all six words in the
first row have source degree three. In the second row $12303$ has
degree three and $J=\{1\}$, while $23031,w$ have degree two and
$J=\varnothing$.
\[
\begin{array}{c|l}
t&S_t\\ \hline
01023&12310^{01},\ 23101^{12},\ 23201^{23},\ 23210^{03},\ w^{24},\ 32310^{04}\\
01124&12303^{1},\ 23031,\ w
\end{array}
\]
For every allowed edit of each source, some $x\in S_t$ is legal
in its restored target component and satisfies $d_A(x)+\alpha=3$
and $f=0$. These checks use precisely the first normalizer above
and the printed pools; no pool-equivariance is assumed.
They follow directly from the one-coordinate lists
\[
L_i(t,x)=\{0,1,2,3\}\setminus\{x_{i-1},x_{i+1},t_i\},\qquad
d_A(x)=\sum_i(|L_i(t,x)|-1),
\]
omitting $t_i$ when starred. Lemma~\ref{lem:c5-one-boundary-local}
then supplies a common edge outside both pools for any pair of
component Hamilton cycles. In particular it proves the protected
identity for their specified cycles. The first row covers all fifteen
edits and the second all twelve; these are two complete normalized
source cases, rather than a symmetry claim about their pools.

'''

def blocks(src):
    return {m[1]:m[2] for m in re.finditer(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$',src,re.S|re.M)}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def run():
    original=HERE/'frozen-main.tex';old=original.read_text()
    assert sha(original)=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
    cover=json.loads((HERE/'set-cover-results.json').read_text());glob=json.loads((HERE/'global-cover-results.json').read_text())
    cancellation=json.loads((HERE/'cancellation-results.json').read_text())
    assert glob['minimum_distinct_words']==8 and cancellation['selected27_all_ds_plus_alpha_equals3_and_f0']
    B=blocks(old);assert len(B)==53
    rowpattern=r'\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b'
    rows=list(re.finditer(rowpattern,B['INTERFACES-ALL']));assert len(rows)==283
    removed=[m.group(0) for m in rows if m.group(1) in cover['source_families']]
    remaining=[m.group(0) for m in rows if m.group(1) not in cover['source_families']]
    assert len(removed)==27 and len(remaining)==256
    identity=lambda m:(m.group(1),int(m.group(2)),int(m.group(3)),m.group(4),m.group(5),int(m.group(6)))
    expected={tuple(a[k] for k in ('source','source_component','position','colour','target_type','target_component')) for f in cover['source_families'].values() for z in f['coverage_map'] for a in [z['interface']]}
    assert {identity(m) for m in rows if m.group(1) in cover['source_families']}==expected
    body='\\begingroup\\scriptsize\\ttfamily\\begin{flushleft}\n'+'\n'.join(' ; '.join(remaining[i:i+2])+r'\\' for i in range(0,len(remaining),2))+'\n\\end{flushleft}\\endgroup\n'
    candidate=old.replace(B['INTERFACES-ALL'],body,1)
    start='\\begin{lemma}[Protected-edge identities]'
    assert candidate.count(start)==1
    candidate=candidate.replace(start,LOCAL_LEMMA+start,1)
    oldproof='''For the 313 standard-source interfaces, the appendix gives 283
individual common edges and six constant-source parameter families
covering the other 30 cases. Checking the five-digit endpoints in
the specified cycles and outside their pools proves each individual
record. The six families follow from two possible normalizing
directions and four protected target edges, as shown there. Applying
the inverse coordinate and colour maps gives every labelled case. This is a complete finite case proof;
no finite-length gluing experiment is used to infer a general rule.'''
    newproof='''For the 313 standard-source interfaces, the appendix gives 256
individual common edges, two ordinary-source families covering 27
cases, and six constant-source families covering 30 cases.
Checking the five-digit endpoints in the specified cycles and outside
their pools proves each individual record. The two ordinary-source
families use Lemma~\\ref{lem:c5-one-boundary-local}, the local colour
lists and the same prescribed pools. The constant-source families
follow from two possible normalizing directions and four protected
target edges. Applying the inverse coordinate and colour maps gives
every labelled case. This is a complete finite case proof;
no finite-length gluing experiment is used to infer a general rule.'''
    assert candidate.count(oldproof)==1
    candidate=candidate.replace(oldproof,newproof,1)
    oldheading='\\paragraph{The 283 nonconstant-source interfaces.}'
    assert candidate.count(oldheading)==1
    candidate=candidate.replace(oldheading,SOURCE_FAMILIES+'\\paragraph{The 256 remaining individual nonconstant-source interfaces.}',1)
    C=blocks(candidate);assert len(C)==53 and all(B[k]==C[k] for k in B if k!='INTERFACES-ALL')
    assert len(re.findall(rowpattern,C['INTERFACES-ALL']))==256
    normalization=lambda z:z.split('Here is the exact normalization convention.',1)[1].split('\\begin{lemma}',1)[0]
    assert normalization(old)==normalization(candidate)
    target=HERE/'two-source-families-candidate-v1.tex';target.write_text(candidate)
    (HERE/'removed-individual-records.json').write_text(json.dumps(dict(removed_count=27,records=removed,retained_individual_count=256,source_family_case_count=27,constant_source_family_case_count=30,total=313),indent=2)+'\n')
    (HERE/'local-cancellation-lemma.tex').write_text(LOCAL_LEMMA)
    (HERE/'two-source-family-table.tex').write_text(SOURCE_FAMILIES)
    metrics=dict(status='PASS',original_source_sha256=sha(original),candidate_source_sha256=sha(target),other52marked_blocks_byte_exact=True,normalization_paragraph_byte_exact=True,interface_records_before=283,interface_records_after=256,removed_interface_records=27,two_source_family_members=27,constant_six_family_members=30,scope_total=313,per_family_minimum_words={t:f['minimum_word_count'] for t,f in cover['source_families'].items()},global_minimum_distinct_state_words=8,explicit_interface_witness_endpoint_words_before=566,explicit_interface_witness_endpoint_words_after=512,added_distinct_family_state_words=8,replacement_case_evidence_word_count_before=566,replacement_case_evidence_word_count_after=520,case_evidence_state_word_reduction=46,raw_tex_bytes_before=len(old.encode()),raw_tex_bytes_after=len(candidate.encode()),raw_tex_characters_before=len(old),raw_tex_characters_after=len(candidate),whitespace_tokens_before=len(old.split()),whitespace_tokens_after=len(candidate.split()),all_tex_five_digit_tokens_before=len(re.findall(r'\b[0-4]{5}\b',old)),all_tex_five_digit_tokens_after=len(re.findall(r'\b[0-4]{5}\b',candidate)),limits=['Case-evidence word count counts two state endpoints per retained individual interface and the eight new distinct shared family state words; unchanged cycle/pool premises are omitted from both sides equally.','Raw TeX size includes added analytic proof, so reduced witness input does not imply reduced prose length.','No live main edit; the candidate alone removes27unused individual witness records.'])
    (HERE/'candidate-structure-results.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps(metrics,indent=2))

if __name__=='__main__':run()
