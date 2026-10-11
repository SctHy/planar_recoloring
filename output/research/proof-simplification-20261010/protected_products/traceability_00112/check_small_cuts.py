"""Exact local cut obstructions for the fixed listed C5 with boundary 00112."""
from pathlib import Path
from itertools import product, combinations
import hashlib, json, re, time, sys

HERE=Path(__file__).resolve().parent
BOUNDARY=(0,0,1,1,2)


def main():
    start=time.perf_counter()
    inp=HERE/'literal-input.tex'
    literal=inp.read_text()
    block=re.search(r'% BEGIN C2-00112\n(.*?)% END C2-00112',literal,re.S).group(1)
    listed={w[1:] for w in re.findall(r'\b[01][0-3]{5}\b',block)}
    states=sorted(''.join(map(str,w)) for w in product(range(4),repeat=5)
                  if all(w[i]!=w[(i+1)%5] and w[i]!=BOUNDARY[i] for i in range(5)))
    assert set(states)==listed and len(states)==51
    neighbors=[]
    for w in states:
        neighbors.append(sum(1<<j for j,z in enumerate(states)
                             if sum(x!=y for x,y in zip(w,z))==1))
    allmask=(1<<len(states))-1
    def components(removed):
        left=allmask & ~removed; cc=[]
        while left:
            seed=left & -left; reached=0; frontier=seed
            while frontier:
                reached |= frontier; expansion=0; ff=frontier
                while ff:
                    bit=ff & -ff; ff-=bit
                    expansion |= neighbors[bit.bit_length()-1]
                frontier=expansion & left & ~reached
            left &= ~reached
            cc.append([states[j] for j in range(len(states)) if reached>>j&1])
        return cc
    assert len(components(0))==1
    leaves=[i for i,n in enumerate(neighbors) if n.bit_count()==1]
    assert [states[i] for i in leaves]==['12303','13203']
    degs={str(d):sum(n.bit_count()==d for n in neighbors)
          for d in sorted({n.bit_count() for n in neighbors})}
    checked=[]; certificate=None
    max_size=int(sys.argv[1]) if len(sys.argv)>1 else 3
    for size in range(max_size+1):
        count=0; max_excess=-100; extremal=None
        for cut in combinations(range(len(states)),size):
            mask=sum(1<<i for i in cut); cc=components(mask); count+=1
            removed_endpoints=sum(i in cut for i in leaves)
            bound=size+1-removed_endpoints
            excess=len(cc)-bound
            if excess>max_excess: max_excess=excess; extremal=[states[i] for i in cut]
            if excess>0:
                certificate={'cut':[states[i] for i in cut],
                    'component_count':len(cc),'component_sizes':[len(c) for c in cc],
                    'components':cc,'ordinary_Hamilton_path_bound':size+1,
                    'forced_endpoint_bound':bound,
                    'removed_forced_endpoints':removed_endpoints,
                    'ordinary_cut_condition_fails':len(cc)>size+1}
                break
        checked.append({'cut_size':size,'checked':count,'maximum_endpoint_bound_excess':max_excess,
                        'extremal_cut':extremal,'complete_layer':certificate is None})
        if certificate: break
    result={'boundary':'00112','vertices':len(states),'edges':sum(n.bit_count() for n in neighbors)//2,
        'degree_distribution':degs,
        'leaves_and_neighbors':{states[i]:states[(neighbors[i]&-neighbors[i]).bit_length()-1] for i in leaves},
        'cut_search':checked,'maximum_requested_cut_size':max_size,
        'nontraceability_certificate':certificate,
        'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
        'elapsed_seconds':time.perf_counter()-start}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__': main()
