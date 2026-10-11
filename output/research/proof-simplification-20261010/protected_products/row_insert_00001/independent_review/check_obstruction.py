"""Independently verify the fixed graph and protected-edge inputs; no search."""
from pathlib import Path
from itertools import product,combinations
import re,json,hashlib

HERE=Path(__file__).resolve().parent


def main():
    text=(HERE/'literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',text,re.S))
    edge=lambda a,b:tuple(sorted((a,b)))
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,0,0,1)[i] for i in range(5))}
    edges={edge(u,v) for u,v in combinations(states,2) if sum(a!=b for a,b in zip(u,v))==1}
    def eps(a,b):
        assert a!=b and a in '123' and b in '123'
        return 1 if (int(b)-int(a))%3==1 else -1
    def chi(w):
        sign=eps(w[0],w[1])*eps(w[2],w[3])
        return sign if w[4]=='0' else -sign
    X={w for w in states if chi(w)==1};Y=states-X
    XX={e for e in edges if set(e)<=X};YY={e for e in edges if set(e)<=Y}
    assert len(states)==44 and len(edges)==74 and len(X)==20 and len(Y)==24
    assert not XX and YY=={edge('12312','12313'),edge('13212','13213')}
    pairset=lambda tag:{edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',blocks[tag])}
    D,pool=pairset('COMMON-00001'),pairset('POOL-00001-0')
    K=D-pool
    assert len(D)==19 and len(pool)==7 and len(K)==12
    assert edge('12313','12323') in K
    assert '12313' in Y and '12323' in X
    c2=re.findall(r'\b[01][0-3]{5}\b',blocks['PC2-00001'])
    assert len(c2)==len(set(c2))==88 and set(c2)=={str(r)+w for r in (0,1) for w in states}
    e2={edge(u,v) for u,v in zip(c2,c2[1:]+c2[:1])}
    def product_step(u,v):
        return (u[0]==v[0] and edge(u[1:],v[1:]) in edges) or (
            u[0]!=v[0] and u[1:]==v[1:])
    assert all(product_step(u,v) for u,v in e2)
    rows={r:{edge(u[1:],v[1:]) for u,v in e2 if u[0]==v[0]==str(r)} for r in (0,1)}
    assert all(len(rows[r])==38 and not rows[r]&YY and K<=rows[r] for r in (0,1))
    result={'status':'PASS','legal_states':44,'legal_edges':74,'independent_small_class':20,
        'large_class':24,'small_internal_edges':0,'large_internal_edges':[list(e) for e in sorted(YY)],
        'old_PC2_internal_edges_each_row':[38,38],'all_old_PC2_internal_edges_cross_classes':True,
        'old_K_count':12,'obstructing_protected_edge':['12313','12323'],
        'degree_balance':'M has t cross edges and r large-large edges; endpoints X=t,Y=t+2r. L degree sums X=40-t,Y=48-t-2r. Hence r+q=4.',
        'arbitrary_seed_protected_obstruction':'r,q<=2 forces r=q=2. L contains both large-large edges, whose four endpoints all have degree1. Therefore L cannot retain protected12313-12323.',
        'fixed_seed_unprotected_obstruction':'Every old PC2 internal edge crosses the classes, so r=0; q=4 is impossible even without protection.',
        'scope':'Any one-row insertion that cuts a matching of internal edges in that row and inserts a spanning no-isolate linear forest with exactly those endpoints. Does not prohibit more general rewiring.',
        'input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest()}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
