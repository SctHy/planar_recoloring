#!/usr/bin/env python3
"""Exact small readback of2hard supports and5existing named self transports."""
from pathlib import Path
import hashlib,itertools,json,platform
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edge(a,b):return tuple(sorted((a,b)))
def coordinate(e):
    d=[i for i,(a,b) in enumerate(zip(*e)) if a!=b];assert len(d)==1;return d[0]
def casekey(r):return (r['source']+':'+str(r['source_component']),r['position'],int(r['colour']),r['target_type']+':'+str(r['target_component']))
def image(v,m):
    s,eps,p=m;return ''.join(p[int(v[(s+eps*i)%5])] for i in range(5))
def run():
    assert platform.python_version()=='3.14.6'
    old=json.loads((HERE/'conditional-stars-results.json').read_text());root=json.loads((HERE/'frozen-root-cut-results.json').read_text());support=json.loads((HERE/'frozen-hard-support-results-v3.json').read_text());review=json.loads((HERE/'frozen-four-port-root-review.json').read_text())
    supports={}
    for t in ('00001:0','00112:0'):
        meta=root['component_checks'][t];K={tuple(e) for e in meta['actual_fixed_K']};P={tuple(e) for e in meta['actual_pool']};V=sorted(set().union(*(set(e) for e in K)))
        assert len(K)==11 and len(P)==2 and K.isdisjoint(P) and len(V)==20
        J={edge(x,y) for x,y in itertools.combinations(V,2) if sum(a!=b for a,b in zip(x,y))==1};M=J-K
        expected=support['fixed_hard_templates'][t];assert len(J)==17 and len(M)==6 and M=={tuple(e) for e in expected['missing_edges']}
        budgets=[sum(coordinate(e)==j for e in M) for j in range(5)];assert budgets==expected['missing_coordinate_counts']
        supports[t]=dict(K=[list(e) for e in sorted(K)],pool=[list(e) for e in sorted(P)],endpoint_vertices=V,induced_support_edges=[list(e) for e in sorted(J)],missing_edges=[list(e) for e in sorted(M)],missing_coordinate_counts=budgets,full_hard_component_states=meta['state_count'])
    identities={casekey(r['row']) for r in old['records']};profiles=[p for p in support['hard_side_profiles_all53'] if tuple(p['case']) in identities]
    hits={tuple(p['case']) for p in profiles if max(p['one_sided_legal_support_bounds'])>0};exceptions=[s for s in support['two_hard_self_supports'] if tuple(s['case']) in identities]
    assert len(hits)==17 and len(exceptions)==2 and hits|{tuple(s['case']) for s in exceptions}==identities
    originalmaps={casekey(r['row']):r['interface']['mapping'] for r in old['records']};ports=[]
    for r in review['records']:
        t=r['source'];case=(t+':0',r['position'],int(r['new_colour']),t+':0');m=r['first_map'];e=tuple(r['source_K_edge']);f=tuple(r['target_K_edge']);assert m==originalmaps[case]
        assert edge(*(image(v,m) for v in e))==f and list(e) in supports[t+':0']['K'] and list(f) in supports[t+':0']['K']
        ports.append(dict(case=case,original_first_map=m,source_port=e,target_port=f,inherited_review='frozen-four-port-root-review.json'))
    fifth=('00112:0',4,3,'00112:0');m=originalmaps[fifth];e=('13230','23230');f=('12320','32320')
    assert m==[0,1,'0132'] and edge(*(image(v,m) for v in e))==f and list(e) in supports['00112:0']['K'] and list(f) in supports['00112:0']['K']
    ports.append(dict(case=fifth,original_first_map=m,source_port=e,target_port=f,inherited_review='frozen-weak-transport-results-v5.json; named00112port'))
    assert len(ports)==5 and {tuple(p['case']) for p in ports}=={casekey(r['row']) for r in old['records'] if not r['eligible']}
    named_members={(p['case'][0],tuple(e)) for p in ports for e in (p['source_port'],p['target_port'])}
    old_members=set()
    for r in old['records']:
        if r['eligible']:continue
        t=r['row']['source']+':0';e=tuple(r['row']['old_edge']);f=edge(*(image(v,r['interface']['mapping']) for v in e))
        assert list(e) in supports[t]['K'] and list(f) in supports[t]['K']
        old_members.update(((t,e),(t,f)))
    assert named_members==old_members and len(named_members)==9
    A=('13120','23120');sigma=[0,1,'0231'];bad=edge(*(image(v,sigma) for v in A))
    assert list(A) in supports['00001:0']['K'] and list(bad) in supports['00001:0']['pool']
    out=dict(status='PASS',python=platform.python_version(),hard_supports=supports,remaining_hard_cases=19,inherited_missing_budget_positive_cases=17,inherited_two_support_exceptions=exceptions,hard_self_existing_ports=ports,distinct_standard_K_memberships_named_ports=9,distinct_standard_K_memberships_original_rows=9,standard_K_membership_sets_identical=True,whole_K_transport_counterexample=dict(source_port=A,actual_map=sigma,image_in_target_pool=bad),scope='Small2support/5namedportmetadatareadback;frozen17retentionprofilesareinheritednumericinputs,notanewuniformproof.')
    (HERE/'support-port-extract-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('hard_supports','hard_self_existing_ports','inherited_two_support_exceptions')},indent=2))
if __name__=='__main__':run()
