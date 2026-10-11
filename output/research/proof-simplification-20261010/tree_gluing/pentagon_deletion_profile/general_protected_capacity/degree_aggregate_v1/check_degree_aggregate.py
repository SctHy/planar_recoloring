from pathlib import Path
from collections import Counter
import hashlib,json,re,sys,time
from root_set_functions import edge,restore,endpoints

here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(here/'phase6-source.tex')=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
text=(here/'phase6-source.tex').read_text();blocks=dict(re.findall(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$',text,re.S|re.M))
words=lambda name:re.findall(r'\b[0-3]{5}\b',blocks[name])
pairs=lambda name:{edge(x,y) for x,y in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[name])}
states={}
for name in blocks:
    if name.startswith(('C1-','FHC-')):
        t=name.split('-')[1];ws=words(name);assert len(ws)==len(set(ws));states[t+':0']=set(ws)
pools={key:pairs('POOL-'+key.replace(':','-')) for key in states}
data=json.loads((here/'verified-interface-input.json').read_text())
local_count=0
def neighbours(w,t):
    global local_count
    out=set()
    for j in range(5):
        for a in '0123':
            local_count+=1
            if a!=w[j] and a!=w[(j-1)%5] and a!=w[(j+1)%5] and (t[j]=='4' or a!=t[j]):
                out.add(w[:j]+a+w[j+1:])
    return out
tic=time.perf_counter();records=[]
for case in data['cases']:
    if case['group']!='HH-230':continue
    source,target=case['source'],case['target'];j,q=case['changed_position'],case['new_colour'];g=case['normalizer']
    Vs=states[source];Vt={restore(v,g) for v in states[target]};U=Vs&Vt;O=Vs-U
    s=source[:5];t=s[:j]+str(q)+s[j+1:]
    Q={edge(restore(x,g),restore(y,g)) for x,y in pools[target]}
    F={e for e in pools[source]|Q if endpoints({e})<=U}
    nt={v:neighbours(v,t) for v in U}
    assert all(n<=Vt for n in nt.values())
    S={v for v in U if len(nt[v])<=3}
    assert all(len(nt[v])>=2 for v in S)
    weights={v:4-len(nt[v]) for v in S}
    ns={v:neighbours(v,s) for v in S}
    assert all(n<=Vs for n in ns.values())
    cut=sum(len(ns[v]&O) for v in S)
    cut_bound=min(2*len(O),cut)
    pool_inc=sum(sum(v in e for e in F) for v in S)
    demand=sum(weights.values());B=cut_bound+pool_inc
    bound=max(0,(demand-B+1)//2)
    # The graph-only pointwise upper bound on lost incidences can be tighter.
    # It is an optional independent conditional variant, never a cycle search.
    point_losses={v:min(2,len(ns[v]&O)+sum(v in e for e in F)) for v in S}
    point_B=sum(point_losses.values())
    point_bound=max(0,(demand-point_B+1)//2)
    records.append({'case':[source,j,q,target],'outside_states':len(O),'common_states':len(U),
       'low_degree_states':len(S),'weights':demand,'graph_cut_edges_from_S':cut,
       'cycle_cut_bound':cut_bound,'pool_incidences':pool_inc,'loss_bound':B,
       'aggregate_bound':bound,'pointwise_loss_bound':point_B,'pointwise_bound':point_bound,
       'low_degree_words':sorted(S)})
assert len(records)==230
summary={'cases':len(records),'aggregate_positive':sum(r['aggregate_bound']>0 for r in records),
         'pointwise_positive':sum(r['pointwise_bound']>0 for r in records),
         'low_degree_state_count_distribution':dict(sorted(Counter(r['low_degree_states'] for r in records).items())),
         'largest_aggregate_margin':max(r['weights']-r['loss_bound'] for r in records),
         'local_colour_checks':local_count}
result={'status':'EXACT_CONDITIONAL_BOUND_FEASIBILITY','source_sha256':sha(here/'phase6-source.tex'),
        'python':sys.version.split()[0],'summary':summary,'records':records,
        'HC_search':False,'selected_cycle_edges_used':False,'whole_state_graph_constructed':False,
        'scope':'230 fixed full ordinary component vertex sets and pools; conditional aggregate theorem, not universal positive coverage.',
        'elapsed_seconds':time.perf_counter()-tic}
(here/'aggregate-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
