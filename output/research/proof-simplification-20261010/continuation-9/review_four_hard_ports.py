from pathlib import Path
from itertools import permutations
import json, re, hashlib

b = Path(__file__).resolve().parent
root = b.parents[3]
source = root/'planar_recoloring_hamilton_thresholds.tex'
s = source.read_text()
blocks = dict(re.findall(r'% BEGIN ([^\n]+)\n(.*?)% END \1', s, re.S))
types = {k.split('-')[1] for k in blocks if k.startswith('POOL-')}
edge = lambda a,c:tuple(sorted((a,c)))
def edges(block):
    return {edge(a,c) for a,c in re.findall(r'(?<!\d)([0-3]{5})-([0-3]{5})(?!\d)', blocks[block])}
K = {'00001':edges('COMMON-00001')-edges('POOL-00001-0'),
     '00112':edges('PORTS-00112')-edges('POOL-00112-0')}
assert all(len(x)==11 for x in K.values())
def first(t):
    for off in range(5):
        for eps in (1,-1):
            for p in permutations('0123'):
                n=''.join('4' if t[(off+eps*i)%5]=='4' else p[int(t[(off+eps*i)%5])] for i in range(5))
                if n in types:return n,off,eps,p
    raise AssertionError(t)
def forward(w,m):
    _,off,eps,p=m
    return ''.join(p[int(w[(off+eps*i)%5])] for i in range(5))
cases=[('00001',4,'2',('13210','23210'),('13120','23120')),
       ('00001',4,'3',('12310','32310'),('13120','23120')),
       ('00112',0,'2',('12023','13023'),('13020','13023')),
       ('00112',3,'2',('13030','13230'),('32030','32031'))]
records=[]
members=set()
for t,j,q,e,f in cases:
    actual=t[:j]+q+t[j+1:]
    m=first(actual)
    assert m[0]==t and edge(*e) in K[t] and edge(*f) in K[t]
    assert edge(*(forward(w,m) for w in e))==edge(*f)
    for w in e:
        assert all(w[i]!=actual[i] and w[i]!=w[(i+1)%5] for i in range(5))
    assert sum(a!=c for a,c in zip(*e))==1
    assert sum(a!=c for a,c in zip(*f))==1
    involution = all(forward(forward(w,m),m)==w for w in (*e,*f))
    if t=='00112':assert involution
    records.append({'source':t,'position':j,'new_colour':q,
                    'first_map':[m[1],m[2],''.join(m[3])],
                    'source_K_edge':e,'target_K_edge':f,'pair_involution':involution})
    members.update((t,edge(*z)) for z in (e,f))
assert len(members)==7
result={'verdict':'PASS','actual_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'actual_first_normalizers_independently_recomputed':4,
        'distinct_current_K_memberships':7,'records':records,
        'math_review':'Designated e in K_s and firstmap(e) in K_t gives e in restored protected intersection; no HC premise or whole-K equivariance.',
        'scope':'Four named actual cases only. Hardseed port validity inherited; prior49union and arbitrary graph conclusions not re-reviewed.'}
(b/'four-hard-port-root-review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
