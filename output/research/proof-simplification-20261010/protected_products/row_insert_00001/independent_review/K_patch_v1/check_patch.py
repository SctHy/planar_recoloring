"""Affected-witness monotonicity and tiny necessary-forest audit, no seed search."""
from pathlib import Path
from itertools import permutations,product,combinations
from collections import Counter
import re,json,hashlib

HERE=Path(__file__).resolve().parent
STANDARD=('00000','00001','00011','00012','00101','00102','00112','00121','00123','01012','01023','00004','00014','00104','00114','00124','01014','01024','01104','01124','01204','01234')


def main():
    text=(HERE/'interface-literal-input-v1.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    claims=json.loads((HERE/'K-patch-results-v1.json').read_text())
    edge=lambda u,v:tuple(sorted((u,v)))
    pairs=lambda tag:{edge(u,v) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[tag])}
    K=pairs('COMMON-00001')-pairs('POOL-00001-0');h=edge('12313','12323')
    assert len(K)==12 and h in K
    def norm(boundary):
        for s in range(5):
            for eps in (1,-1):
                for p in permutations(range(4)):
                    w=''.join(str(p[int(boundary[(s+eps*i)%5])]) for i in range(5))
                    if w in STANDARD:return w,(s,eps,p)
        raise AssertionError(boundary)
    def transform(w,g):
        s,eps,p=g;return ''.join(str(p[int(w[(s+eps*i)%5])]) for i in range(5))
    def restore(w,g):
        s,eps,p=g;inv={str(p[c]):str(c) for c in range(4)};z=['']*5
        for i,c in enumerate(w):z[(s+eps*i)%5]=inv[c]
        return ''.join(z)
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',blocks['INTERFACES-ALL'])
    assert len(records)==283
    damaged=[];affected=0
    for source,pos,new,target,u,v in records:
        if source!='00001:0' and target!='00001:0':continue
        affected+=1;pos=int(pos);boundary=list(source[:5]);boundary[pos]=new
        nt,g=norm(''.join(boundary));assert nt==target[:5]
        if (source=='00001:0' and edge(u,v)==h) or (target=='00001:0' and edge(transform(u,g),transform(v,g))==h):
            damaged.append((source,pos,int(new),target,g))
    assert [(s,p,n,t) for s,p,n,t,g in damaged]==[
        ('00001:0',1,3,'00102:0'),('00001:0',4,2,'00001:0'),('00001:0',4,3,'00001:0')]
    c1=re.findall(r'\b[0-3]{5}\b',blocks['C1-00102'])
    Kother={edge(u,v) for u,v in zip(c1,c1[1:]+c1[:1])}-pairs('POOL-00102-0')
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    BAD={'12312','12313','13212','13213'};core=states-BAD
    raw={edge(u,v) for u,v in combinations(core,2) if sum(a!=b for a,b in zip(u,v))==1}
    reserves={e for e in pairs('POOL-00001-0') if not set(e)&BAD}
    assert len(core)==40 and len(reserves)==6
    def forest(es):
        parent={u:u for u in core}
        def find(u):
            while u!=parent[u]:u=parent[u]
            return u
        for u,v in es:
            a,b=find(u),find(v)
            if a==b:return False
            parent[a]=b
        return True
    def propagate(required):
        available=set(raw);required=set(required);rounds=0
        while True:
            rounds+=1;rd=Counter(u for e in required for u in e);ad=Counter(u for e in available for u in e)
            if any(rd[u]>2 or ad[u]<1 for u in core) or not forest(required):return None
            new_available={e for e in available if e in required or all(rd[u]<2 for u in e)}
            nd=Counter(u for e in new_available for u in e)
            new_required=required|{e for e in new_available if any(nd[u]==1 for u in e)}
            if new_available==available and new_required==required:
                return required,available,dict(sorted(Counter(ad[u] for u in core).items())),rounds
            available,required=new_available,new_required
    reports=[]
    critical={edge('31212','31232'),edge('12132','32132'),edge('21313','21323'),edge('13123','23123')}
    for claim in claims['patches']:
        patch=edge(*claim['added_K_edge']);patched=(K-{h})|{patch}
        assert len(patched)==12 and patched<raw
        assert patched=={edge(*e) for e in claim['patched_K']} and critical<=patched
        selected=[]
        for source,pos,new,target,g in damaged:
            target_K=patched if target=='00001:0' else Kother
            common=patched&{edge(restore(u,g),restore(v,g)) for u,v in target_K}
            assert common
            selected.append({'position':pos,'new_excluded':new,'target':target,'common_edges':[list(e) for e in sorted(common)]})
        screens=[]
        for screen in claim['two_old_reserve_necessary_forests']:
            R={edge(*e) for e in screen['two_reserves']};assert len(R)==2 and R<=reserves and not R&patched
            result=propagate(patched|R);assert result is not None
            required,available,degrees,rounds=result
            assert required=={edge(*e) for e in screen['forced_edges']}
            assert (len(required),len(available),rounds)==(screen['forced_edge_count'],screen['available_edge_count'],screen['rounds'])
            assert {str(k):v for k,v in degrees.items()}==screen['available_degree_distribution']
            screens.append({'reserves':[list(e) for e in sorted(R)],'forced_count':len(required),'available_count':len(available),'acyclic_forced_edges':True})
        assert len(screens)==15
        reports.append({'patch':list(patch),'three_damaged_interfaces_repaired':selected,
            'all_other_individual_witnesses_inherited_by_monotonicity':280,
            'six_constant_families_inherited_from_four_critical_target_memberships':True,
            'necessary_forest_screens_verified':screens,'constructed_seeds':False})
    result={'status':'PASS','individual_literal_records':283,'affected00001_records_checked':affected,
        'exactly_three_old_witnesses_damaged':True,'patches':reports,
        'all313_interfaces_supported_by_old_valid_certificates_plus_three_repairs_and_six_family_identity':True,
        'necessary_degree_propagation_is_not_seed_or_forest_existence':True,
        'input_sha256':hashlib.sha256((HERE/'interface-literal-input-v1.tex').read_bytes()).hexdigest(),
        'claim_sha256':hashlib.sha256((HERE/'K-patch-results-v1.json').read_bytes()).hexdigest(),
        'scope':'No full graph or interface kernel replay. Unaffected witnesses are inherited from existing valid certificates; only00001-affected witness deletion tests andthree repairs are checked.'}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='patches'}))
    for p in reports:print(json.dumps({k:v for k,v in p.items() if k!='necessary_forest_screens_verified'}))


if __name__=='__main__':main()
