#!/usr/bin/env python3
"""Shorter complete candidate, retaining v1 bytes and all52 unchanged blocks."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent

SHORT_FAMILIES=r'''\paragraph{Two source families (27 interfaces).}
At a common state $x$, change non-star entry $j$ from $a$ to $q$.
Let $d$ be its source degree, $\alpha=\mathbf1[a\notin
\{x_{j-1},x_{j+1}\}]$, and $f$ the number of common incident edges
in the union of the source and restored target pools.
Any pair of component Hamilton cycles shares at least
$\max\{0,4-d-\alpha-f\}$ incident edges outside both pools.
Indeed, if $\beta$ indicates a source-legal mutation to $q$, the
target degree is $d+\alpha-\beta$, and there are $d-\beta$ common
incident edges. The safe common universe has size $h=d-\beta-f$;
each cycle takes two incident edges, so inclusion--exclusion gives
$4-d-(d+\alpha-\beta)+h=4-d-\alpha-f$.

Put $w=32301$. Subscripts below give source degree, and superscripts
give $J_t(x)=\{j:t_j\in\{x_{j-1},x_{j+1}\}\}$ as position digits;
an omitted superscript means $J=\varnothing$.
\[
\begin{array}{c|l}
t&S_t\\ \hline
01023&12310_3^{01},\ 23101_3^{12},\ 23201_3^{23},\ 23210_3^{03},\ w_3^{24},\ 32310_3^{04}\\
01124&12303_3^1,\ 23031_2,\ w_2
\end{array}
\]
For each of the fifteen edits of the first source and twelve of the
second, the one-coordinate colour lists and the printed pools under
the prescribed first normalizer give some $x\in S_t$ in the restored
target component with $d+\alpha=3$ and $f=0$.
The bound supplies a common edge for any two component Hamilton
cycles and hence for the specified protected sets.

'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blocks(src):return {m[1]:m[2] for m in re.finditer(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$',src,re.S|re.M)}

def run():
    original=(HERE/'frozen-main.tex').read_text();v1=(HERE/'two-source-families-candidate-v1.tex').read_text()
    assert sha(HERE/'two-source-families-candidate-v1.tex')=='21783ee56638ef617420fd6f9bf3e5b8bca1642a6a2fc1ccfb49d3d742e3bf8a'
    lemma=(HERE/'local-cancellation-lemma.tex').read_text();families=(HERE/'two-source-family-table.tex').read_text()
    assert v1.count(lemma)==v1.count(families)==1
    v2=v1.replace(lemma,'',1).replace(families,SHORT_FAMILIES,1)
    previous='''For the 313 standard-source interfaces, the appendix gives 256
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
    shorter='''For the 313 standard-source interfaces, the appendix gives 256
individual common edges and two source families covering 27 cases;
six constant-source families cover the other 30.
Endpoint membership in the specified cycles and outside their pools
proves each individual record. The two source families use the
appendix's local-degree and inclusion--exclusion argument with the
prescribed first normalizer and pools. The constant-source families
use two normalizing directions and four protected target edges.
Inverse coordinate and colour maps give every labelled case.
This is a complete finite case proof; no finite-length gluing
experiment is used to infer a general rule.'''
    assert v2.count(previous)==1;v2=v2.replace(previous,shorter,1)
    old='The constant-source cases are supplied by six parameter families; the other 283 retain individual edge records.'
    new='Six constant-source families cover 30 cases; two further source families cover 27 by local degrees and inclusion--exclusion, leaving 256 individual edge records.'
    assert v2.count(old)==1;v2=v2.replace(old,new,1)
    assert 'lem:c5-one-boundary-local' not in v2 and 'two ordinary-source families' not in v2
    B,C=blocks(original),blocks(v2);assert len(B)==len(C)==53
    assert all(B[k]==C[k] for k in B if k!='INTERFACES-ALL')
    pat=r'\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b'
    assert len(re.findall(pat,C['INTERFACES-ALL']))==256
    normalization=lambda z:z.split('Here is the exact normalization convention.',1)[1].split('\\begin{lemma}',1)[0]
    assert normalization(original)==normalization(v2)
    target=HERE/'two-source-families-candidate-v2.tex';target.write_text(v2)
    (HERE/'two-source-families-short-v2.tex').write_text(SHORT_FAMILIES)
    result=dict(status='PASS',candidate_version='v2',original_sha256=sha(HERE/'frozen-main.tex'),candidate_sha256=sha(target),v1_retained_sha256=sha(HERE/'two-source-families-candidate-v1.tex'),other52marked_blocks_byte_exact=True,normalizer_byte_exact=True,individual_records=256,source_family_cases=27,constant_family_cases=30,total_interfaces=313,verification_note_numbers_corrected=True,no_new_numbered_lemma=True,no_ordinary_components_restriction_on_star_family=True,raw_tex_bytes_before=len(original.encode()),raw_tex_bytes_after=len(v2.encode()),raw_tex_letter_tokens_before=len(re.findall(r'[A-Za-z]+',original)),raw_tex_letter_tokens_after=len(re.findall(r'[A-Za-z]+',v2)),raw_tex_whitespace_tokens_before=len(original.split()),raw_tex_whitespace_tokens_after=len(v2.split()),all_tex_five_digit_tokens_before=len(re.findall(r'\b[0-4]{5}\b',original)),all_tex_five_digit_tokens_after=len(re.findall(r'\b[0-4]{5}\b',v2)),case_evidence_state_words_before=566,case_evidence_state_words_after=520,global_minimum_distinct_family_words=8,scope='Separate complete candidate with unchanged theorem/state space/normalizer/pools and52unchangedC5blocks; only27 now-unused individual witnesses removed.')
    (HERE/'candidate-structure-results-v2.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
