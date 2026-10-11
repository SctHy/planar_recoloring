"""Tiny fixed-matching quotient path; exact final literal certificate checks."""
from pathlib import Path
from itertools import product
import json, re, hashlib, time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
GRAPH=ROOT/'protected_products/traceability_00001/graph-input.json'
ORIGINAL=ROOT/'original/planar_recoloring_hamilton_thresholds.tex'

def main():
    g=json.loads(GRAPH.read_text()); states=g['states']
    legal={''.join(w) for w in product('0123',repeat=5)
           if all(w[i]!=w[(i+1)%5] and w[i]!='00001'[i] for i in range(5))}
    assert len(legal)==44 and legal==set(states)
    actual={tuple(sorted((u,v))) for u,v in g['edges']}
    independent_edges={tuple(sorted((u,v))) for u in states for v in states
                       if sum(a!=b for a,b in zip(u,v))==1}
    assert actual==independent_edges and len(actual)==74
    block=re.search(r'% BEGIN FACTOR-00001\n(.*?)% END FACTOR-00001',ORIGINAL.read_text(),re.S).group(1)
    ws=re.findall(r'\b[0-3]{5}\b',block); old=[ws[i:i+2] for i in range(0,len(ws),2)]
    assert len(ws)==len(set(ws))==44 and set(ws)==legal
    assert all(tuple(sorted(pair)) in actual for pair in old)
    where={w:i for i,p in enumerate(old) for w in p}
    adj={i:set() for i in range(22)}; witnesses={}
    for u,v in sorted(actual):
        i,j=where[u],where[v]
        if i==j: continue
        adj[i].add(j);adj[j].add(i)
        witnesses.setdefault(tuple(sorted((i,j))),[]).append((u,v))
    path=[]; nodes=0
    def dfs(v,remaining):
        nonlocal nodes
        nodes+=1
        if not remaining: return path[:]
        for z in sorted(adj[v]&remaining,key=lambda k:(len(adj[k]&remaining),k)):
            path.append(z)
            answer=dfs(z,remaining-{z})
            if answer: return answer
            path.pop()
        return None
    start=time.perf_counter(); order=None
    for v in sorted(adj,key=lambda k:(len(adj[k]),k)):
        path[:]=[v];order=dfs(v,set(adj)-{v})
        if order: break
    assert order is not None and len(set(order))==22
    joins=[min(witnesses[tuple(sorted((i,j)))]) for i,j in zip(order,order[1:])]
    pairs=[]
    for i,k in enumerate(order):
        pair=old[k]
        incoming=(next(w for w in joins[0] if w in pair) if i==0
                  else next(w for w in joins[i-1] if w in pair))
        pairs.append([incoming,next(w for w in pair if w!=incoming)])
    eps=[]
    for i,e in enumerate(joins):
        outgoing=next(w for w in e if w in pairs[i])
        eps.append(pairs[i].index(outgoing))
        assert tuple(sorted((pairs[i][eps[-1]],pairs[i+1][0]))) in actual
    load={w:0 for w in states}
    for u,v in joins: load[u]+=1;load[v]+=1
    assert max(load.values())==2
    literal={'boundary':'00001','pairs':pairs,'outgoing_endpoint':eps,
             'convention':'rows i=1..22; a_i=pairs[i-1][0], b_i=pairs[i-1][1]; join i to i+1 by (a_i if bit=0 else b_i)--a_(i+1)',
             'actual_joins':[list(e) for e in joins],
             'matching_state_count':44,'block_count':22,'join_count':21}
    (HERE/'matching-chain-00001-literal.json').write_text(json.dumps(literal,indent=2)+'\n')
    source_lines=['% BEGIN MATCHING-CHAIN-00001',r'\begingroup\small\ttfamily',
                  r'\begin{tabular}{rllc@{\qquad}rllc}',
                  r'$i$ & $a_i$ & $b_i$ & $\epsilon_i$ & $i$ & $a_i$ & $b_i$ & $\epsilon_i$ \\ \hline']
    for i in range(11):
        j=i+11; a,b=pairs[i];c,d=pairs[j]
        source_lines.append(f'{i+1} & {a} & {b} & {eps[i]} & {j+1} & {c} & {d} & '
                            +(str(eps[j]) if j<21 else '--')+r' \\')
    source_lines+=[r'\end{tabular}\endgroup','% END MATCHING-CHAIN-00001']
    (HERE/'matching-chain-00001-literal.tex').write_text('\n'.join(source_lines)+'\n')
    record={'graph_sha256':hashlib.sha256(GRAPH.read_bytes()).hexdigest(),
            'original_source_sha256':hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
            'original_factor_sha256':hashlib.sha256(block.encode()).hexdigest(),
            'literal_certificate_sha256':hashlib.sha256((HERE/'matching-chain-00001-literal.json').read_bytes()).hexdigest(),
            'legal_states':44,'actual_edges':74,'matching_edges':22,'matching_quotient_edges':len(witnesses),
            'quotient_path_search_nodes':nodes,'elapsed_seconds':time.perf_counter()-start,
            'old_pair_order_1_based':[i+1 for i in order],
            'connector_maximum_physical_load':max(load.values()),
            'connector_load_distribution':{str(d):sum(x==d for x in load.values()) for d in sorted(set(load.values()))},
            'claim':'a spanning P2-factor with linearly ordered blocks and actual consecutive cross edges; not a Hamilton path of the 44-state graph',
            'checks':'enumerated legal graph independently; factor covers all states once; 22-node quotient path; every actual join Hamming distance one; connector load at most two'}
    (HERE/'matching-chain-00001-record.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2));print('epsilon',eps)

if __name__=='__main__':main()
