"""Four fixed local degree3 witnesses; no state graph or HC enumeration."""
from pathlib import Path
from itertools import permutations
import re,json,hashlib
HERE=Path(__file__).resolve().parent
def parse(w):return tuple(map(int,w))
def text(w):return ''.join(map(str,w))
def edge(u,v):return tuple(sorted((u,v)))
def legal(w,t):return all(w[i]!=w[(i+1)%5] and w[i]!=t[i] for i in range(5))
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
    cases=[('00001','01001','32132'),('00001','03001','32132'),('00112','01112','13023'),('00112','00111','13023')];rows=[]
    for hard,target,vertex in cases:
        t=parse(target);v=parse(vertex);assert legal(v,t)
        neighbours={w for i in range(5) for c in range(4) if c!=v[i] and legal(w:=v[:i]+(c,)+v[i+1:],t)}
        incident={edge(v,w) for w in neighbours};protected={e for e in incident if e in K[hard]};assert len(neighbours)==3 and len(protected)==2
        nt,g=normalizer(t);assert nt not in {'00000','00001','00112'} and f'C1-{nt}' in blocks
        Q={edge(restore(u,g),restore(w,g)) for u,w in edges(f'POOL-{nt}-0')}
        rows.append({'hard':hard,'actual_target':target,'witness_vertex':vertex,'neighbours':sorted(map(text,neighbours)),'target_degree':3,'hard_incident_edges':['-'.join(map(text,e)) for e in sorted(protected)],'neighbours_after_hardK_deleted':sorted(text(w) for w in neighbours if edge(v,w) not in protected),'target_standard_type':nt,'prescribed_normalizer':[g[0],g[1],list(g[2])],'hard_pair_target_pool_overlap':['-'.join(map(text,e)) for e in sorted(protected&Q)],'arbitrary_HC_must_meet_hardK':True,'arbitrary_HC_must_meet_hardK_outside_target_pool':not bool(protected&Q)})
    result={'status':'FOUR_FIXED_DEGREE3_PAIR_CERTIFICATES','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':rows,'state_graph_enumeration':False,'Hamilton_search':False,'selected_opponent_cycle_retention_count_used':False,'scope':'two symbolic boundary-change families, four nonhard target instances and all their simultaneous relabelings; not all53 interfaces'}
    (HERE/'degree-pair-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
