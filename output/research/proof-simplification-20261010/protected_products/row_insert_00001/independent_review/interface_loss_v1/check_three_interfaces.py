"""Recompute three selected loss interfaces directly; no full kernel replay."""
from pathlib import Path
from itertools import permutations
import re,json,hashlib

HERE=Path(__file__).resolve().parent
STANDARD=('00000','00001','00011','00012','00101','00102','00112','00121','00123','01012','01023','00004','00014','00104','00114','00124','01014','01024','01104','01124','01204','01234')


def main():
    text=(HERE/'interface-literal-input-v1.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    claim=json.loads((HERE/'interface-feasibility-results-v1.json').read_text())
    edge=lambda a,b:tuple(sorted((a,b)))
    pairs=lambda tag:{edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[tag])}
    oldK=pairs('COMMON-00001')-pairs('POOL-00001-0');removed=edge('12313','12323')
    assert len(oldK)==12 and removed in oldK
    reduced=oldK-{removed}
    c1=re.findall(r'\b[0-3]{5}\b',blocks['C1-00102'])
    Kother={edge(u,v) for u,v in zip(c1,c1[1:]+c1[:1])}-pairs('POOL-00102-0')
    def normalizer(boundary):
        for s in range(5):
            for eps in (1,-1):
                for p in permutations(range(4)):
                    word=''.join(str(p[int(boundary[(s+eps*i)%5])]) for i in range(5))
                    if word in STANDARD:return word,(s,eps,p)
        raise AssertionError(boundary)
    def restore(w,g):
        s,eps,p=g;pinv={str(p[c]):str(c) for c in range(4)};z=['']*5
        for i,c in enumerate(w):z[(s+eps*i)%5]=pinv[c]
        return ''.join(z)
    details=[]
    for claimed in claim['lost_old_witness_records']:
        pos,new=claimed['position'],claimed['new_excluded']
        assert (pos,new) in ((1,3),(4,2),(4,3))
        boundary=list('00001');boundary[pos]=str(new)
        target,g=normalizer(''.join(boundary));assert target+':0'==claimed['target']
        target_old=oldK if target=='00001' else Kother
        target_new=reduced if target=='00001' else Kother
        restored_old={edge(restore(u,g),restore(v,g)) for u,v in target_old}
        restored_new={edge(restore(u,g),restore(v,g)) for u,v in target_new}
        common_old=oldK&restored_old;common_new=reduced&restored_new
        assert len(common_old)==claimed['old_common_K_count']
        assert len(common_new)==claimed['reduced_common_K_count']
        assert edge(*claimed['old_witness']) in common_old-common_new
        if claimed['replacement_witness'] is not None:assert edge(*claimed['replacement_witness']) in common_new
        details.append({'position':pos,'new_excluded':new,'target':target,
            'normalizer':{'shift':g[0],'orientation':g[1],'permutation':g[2]},
            'old_common_edges':[list(e) for e in sorted(common_old)],
            'reduced_common_edges':[list(e) for e in sorted(common_new)],
            'restored_deleted_target_edge':list(edge(*(restore(w,g) for w in removed))) if target=='00001' else None})
    assert len(details)==3
    critical={edge('31212','31232'),edge('12132','32132'),edge('21313','21323'),edge('13123','23123')}
    assert critical<=reduced and critical=={edge(*e) for e in claim['four_critical_target_edges_survive']}
    result={'status':'PASS','old_K_count':12,'reduced_K_count':11,'removed_edge':list(removed),
        'selected_interfaces_checked':3,'details':details,
        'all_four_constant_family_critical_edges_retained':True,
        'constant_family_preservation_reason':'The four canonical target edges remain and the unchanged six-family normalization proof uses only those four target memberships; constant source sets are unchanged.',
        'input_sha256':hashlib.sha256((HERE/'interface-literal-input-v1.tex').read_bytes()).hexdigest(),
        'claim_sha256':hashlib.sha256((HERE/'interface-feasibility-results-v1.json').read_bytes()).hexdigest(),
        'scope':'Three specified interfaces only; not an independent completeness check over all283records. No graph or Hamilton search.'}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
