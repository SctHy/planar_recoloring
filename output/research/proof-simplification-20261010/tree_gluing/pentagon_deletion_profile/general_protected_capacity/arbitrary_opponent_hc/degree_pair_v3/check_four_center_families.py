"""Only two new centers; merge frozen earlier30 local cases, no fullgraph."""
from pathlib import Path
from itertools import permutations
import re,json,hashlib
HERE=Path(__file__).resolve().parent
def parse(w):return tuple(map(int,w))
def text(w):return ''.join(map(str,w))
def edge(u,v):return tuple(sorted((u,v)))
def main():
    source=HERE/'phase6-source.tex';s=source.read_text();assert hashlib.sha256(source.read_bytes()).hexdigest()=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',s,re.S));standard=set(re.findall(r'% BEGIN (?:C1|FHC)-([0-4]{5})',s))|{'00000','00001','00112'}
    def edges(n):return {edge(parse(u),parse(v)) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[n])}
    K={'00001':edges('COMMON-00001')-edges('POOL-00001-0'),'00112':edges('PORTS-00112')-edges('POOL-00112-0')};assert all(len(k)==11 for k in K.values())
    def normalizer(t):
        for shift in range(5):
            for eps in (1,-1):
                for p in permutations(range(4)):
                    n=tuple(p[t[(shift+eps*i)%5]] for i in range(5))
                    if text(n) in standard:return text(n),(shift,eps,p)
        raise AssertionError(t)
    def restore(w,g):
        shift,eps,p=g;out=[0]*5
        for i in range(5):out[(shift+eps*i)%5]=p.index(w[i])
        return tuple(out)
    previous=json.loads((HERE/'previous-two-center-results.json').read_text());assert previous['case_count']==30
    vertices={'00001':'12132','00112':'13230'};rows=[];templates={}
    for hard,vs in vertices.items():
        base=parse(hard);v=parse(vs);B=[set(range(4))-{v[(i-1)%5],v[i],v[(i+1)%5]} for i in range(5)]
        templates[hard]={'vertex':vs,'coordinate_alternative_sets':[sorted(b) for b in B],'source_degree':sum(len(B[i]-{base[i]}) for i in range(5)),'source_incident_K':['-'.join(map(text,e)) for e in sorted(K[hard]) if v in e]}
        for j in range(5):
            for q in range(4):
                if q==base[j]:continue
                u=base[:j]+(q,)+base[j+1:];nt,g=normalizer(u)
                row={'hard':hard,'position':j,'new_colour':q,'actual_target':text(u),'target_type':nt,'prescribed_normalizer':[g[0],g[1],list(g[2])],'vertex':vs,'vertex_legal':all(v[i]!=u[i] for i in range(5))}
                if not row['vertex_legal']:
                    row.update({'status':'INAPPLICABLE_WITNESS_VERTEX_ILLEGAL','raw_local_criterion':False,'safe_local_criterion':False});rows.append(row);continue
                N={v[:i]+(c,)+v[i+1:] for i in range(5) for c in B[i]-{u[i]}}
                inc={edge(v,w) for w in N};protected=inc&K[hard];degree=sum(len(B[i]-{u[i]}) for i in range(5));assert degree==len(N)
                if nt=='00000':
                    words=[parse(w) for w in re.findall(r'\b[0-3]{5}\b',blocks['FACTOR-00000'])];assert len(words)==30
                    components=[{restore(w,g) for w in words[:15]},{restore(w,g) for w in words[15:]}];indices=[i for i,W in enumerate(components) if v in W];assert len(indices)==1;component=indices[0];scope='constant_component_containing_vertex'
                else:component=0;scope='hard_target_no_nonvacuous_HC_claim' if nt in K else 'ordinary_single_component'
                Q={edge(restore(a,g),restore(b,g)) for a,b in edges(f'POOL-{nt}-{component}')};safe=protected-Q
                raw_lower=max(0,2-degree+len(protected));safe_lower=max(0,2-degree+len(safe))
                row.update({'target_component':component,'scope':scope,'degree':degree,'neighbours':sorted(map(text,N)),'incident_hardK':['-'.join(map(text,e)) for e in sorted(protected)],'incident_target_pool_overlap':['-'.join(map(text,e)) for e in sorted(protected&Q)],'raw_local_lower_bound':raw_lower,'safe_local_lower_bound':safe_lower,'raw_local_criterion':degree>=2 and raw_lower>0,'safe_local_criterion':degree>=2 and safe_lower>0,'status':'NONVACUOUS_LOCAL_SAFE_PROOF' if degree>=2 and safe_lower>0 and scope!='hard_target_no_nonvacuous_HC_claim' else 'LOCAL_RAW_ONLY' if degree>=2 and raw_lower>0 else 'LOCAL_DEGREE_CRITERION_INCONCLUSIVE'})
                rows.append(row)
    assert len(rows)==30
    new_rows=rows;rows=previous['cases']+new_rows
    merged_templates={f'{hard}:'+template['vertex']:template for hard,template in previous['templates'].items()}
    merged_templates.update({f'{hard}:'+template['vertex']:template for hard,template in templates.items()});templates=merged_templates
    summaries={}
    for hard in vertices:
        subset=[r for r in rows if r['hard']==hard]
        ordinary_safe=sorted({(r['position'],r['new_colour']) for r in subset if r['vertex_legal'] and r['scope']=='ordinary_single_component' and r['safe_local_criterion']})
        ordinary_raw=sorted({(r['position'],r['new_colour']) for r in subset if r['vertex_legal'] and r['scope']=='ordinary_single_component' and r['raw_local_criterion']})
        summaries[hard]={'ordinary_arbitrary_HC_safe_family':ordinary_safe,'ordinary_raw_only_family':sorted(set(ordinary_raw)-set(ordinary_safe)),'constant_component_safe':sorted({(r['position'],r['new_colour'],r['target_component']) for r in subset if r['vertex_legal'] and r['scope']=='constant_component_containing_vertex' and r['safe_local_criterion']}),'witnesses_per_safe_case':{f'{j}:{q}':sorted({r['vertex'] for r in subset if r['position']==j and r['new_colour']==q and r['vertex_legal'] and r['scope']=='ordinary_single_component' and r['safe_local_criterion']}) for j,q in ordinary_safe}}
    result={'status':'FOUR_FIXED_VERTEX_ANALYTIC_ONE_CHANGE_FAMILIES','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'templates':templates,'summaries':summaries,'case_count':60,'new_local_cases_computed':30,'frozen_previous_cases_inherited':30,'cases':rows,'state_graph_enumeration':False,'Hamilton_search':False,'selected_opponent_cycle_edges_or_retention_used':False,'scope':'four protected-degree2 centers, exact local color formulas; earlier30 cases inherited without rerun; no general53-interface assertion'}
    (HERE/'one-change-family-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
if __name__=='__main__':main()
