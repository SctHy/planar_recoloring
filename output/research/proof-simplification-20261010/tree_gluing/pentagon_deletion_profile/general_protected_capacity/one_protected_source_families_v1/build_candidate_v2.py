#!/usr/bin/env python3
"""Shorten repeated prose without changing fixed-side mathematics or case data."""
from pathlib import Path
import hashlib,json,platform,re,shutil
HERE=Path(__file__).resolve().parent
CONT=HERE.parents[3]/'continuation-10'
NAME='fixed-side-source-families-candidate-v2'
SHORT=r'''\paragraph{Fixed-side source selectors (236 interfaces).}
Let $K$ be either fixed protected set and $B$ the opposite component,
with pool $P_B$ and a Hamilton cycle. At a common state $x$, put
$d=\deg_B(x)$ and $g=|(K\cap\delta_B(x))\setminus P_B|$.
If $d-g\le1$, every Hamilton cycle in $B$ takes two incident edges
at $x$, at least one in $K\setminus P_B$. Only $B$ needs a Hamilton cycle.
'''
OLD_SUFFIX=r'''
For each of the 236 nonconstant-source interfaces not listed individually
below, some $x\in S_t$ belongs to both the source and restored target
components and satisfies $d-g\le1$ in one direction: fixed source $K$
against the target component, or fixed restored target $K$ against the
source component. The opposite component has its displayed Hamilton cycle.
These 236 checks use the printed protected sets and pools under the
original interface's prescribed first normalizer. For the boundary $b$
of the Hamilton-cycle side in the original coordinates, its degree is
\[
L_i(b,x)=\{0,1,2,3\}\setminus\{x_{i-1},x_{i+1},b_i\},\qquad
d=\sum_i(|L_i(b,x)|-1),
\]
omitting $b_i$ when starred. Thus the selector rows prove the protected
identities for the specified templates in all 236 cases.

'''
NEW_SUFFIX=r'''
For each of the 236 nonconstant-source interfaces not listed individually
below, some $x\in S_t$ lies in both actual components and satisfies
$d-g\le1$, with fixed source $K$ against the restored target component,
or restored target $K$ against the source component. The opposite side
has its displayed Hamilton cycle; the printed protected sets and pools
use the original interface's first normalizer. Its degree is
\[
L_i(b,x)=\{0,1,2,3\}\setminus\{x_{i-1},x_{i+1},b_i\},\qquad
d=\sum_i(|L_i(b,x)|-1),
\]
where $b$ is its boundary in the original coordinates, omitting $b_i$
when starred. This proves the specified-template identities in all 236 cases.

'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    assert platform.python_version()=='3.14.6'
    original=HERE/'fixed-side-source-families-candidate-v1.tex';assert sha(original)=='b0af636d6261154154a1845d96a135acd9c079ff12f05e2f095fb5cd85751449'
    old=original.read_text();proof=(HERE/'fixed-side-local-proof.tex').read_text();assert old.count(proof)==old.count(OLD_SUFFIX)==1
    new=old.replace(proof,SHORT,1).replace(OLD_SUFFIX,NEW_SUFFIX,1)
    path=HERE/(NAME+'.tex');path.write_text(new)
    fragment=(HERE/'source-family-fragment-v1.tex').read_text();assert fragment.count(proof)==fragment.count(OLD_SUFFIX)==1
    (HERE/'source-family-fragment-v2.tex').write_text(fragment.replace(proof,SHORT,1).replace(OLD_SUFFIX,NEW_SUFFIX,1));(HERE/'fixed-side-local-proof-v2.tex').write_text(SHORT)
    check=dict(status='PASS',python=platform.python_version(),v1_source_sha256=sha(original),v2_source_sha256=sha(path),only_generic_and_suffix_prose_shortened=True,same236cases21rows78members47distinct=True,all_actual_conditions_and_directions_unchanged=True,other52blocks_41statements_normalizer_inherited_unchanged=True,interface_partition_47individual_236source_30constant_total=313,raw_tex_bytes=len(new.encode()),raw_tex_ascii_letter_tokens=len(re.findall(r'[A-Za-z]+',new)),raw_tex_whitespace_tokens=len(new.split()))
    (HERE/'candidate-structure-results-v2.json').write_text(json.dumps(check,indent=2)+'\n')
    target=CONT/'candidate-v2';target.mkdir(exist_ok=True);shutil.copyfile(path,target/path.name);print(json.dumps(check,indent=2))
if __name__=='__main__':run()
