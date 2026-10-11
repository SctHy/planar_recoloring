"""Independent direct-state verification of the 20-vertex nontraceability cut."""
from pathlib import Path
from itertools import product
import hashlib,json

HERE=Path(__file__).resolve().parent

def orientation(a,b):
    assert a!=b and a in '123' and b in '123'
    return 1 if (int(b)-int(a))%3==1 else -1

def sigma(w):return orientation(w[0],w[1])*orientation(w[2],w[3])
def chi(w):return sigma(w)*(1 if w[4]=='0' else -1)

def main():
    inp=HERE/'graph-input.json';g=json.loads(inp.read_text())
    boundary='00001'
    states=sorted(''.join(map(str,x)) for x in product(range(4),repeat=5)
                  if all(x[i]!=x[(i+1)%5] and str(x[i])!=boundary[i] for i in range(5)))
    edges=[(a,b) for i,a in enumerate(states) for b in states[i+1:]
           if sum(x!=y for x,y in zip(a,b))==1]
    assert states==g['states'] and set(edges)==set(map(tuple,g['edges']))
    small={w for w in states if chi(w)==1};large=set(states)-small
    small_edges=[e for e in edges if set(e)<=small]
    large_edges=[e for e in edges if set(e)<=large]
    assert len(small)==20 and len(large)==24 and small_edges==[]
    assert large_edges==[('12312','12313'),('13212','13213')]
    assert all(chi(a)!=chi(b) for a,b in edges if a[:4]!=b[:4])
    noncrossing=[e for e in edges if chi(e[0])==chi(e[1])]
    assert noncrossing==large_edges
    paired=set().union(*(set(e) for e in large_edges))
    components=[list(e) for e in large_edges]+[[w] for w in sorted(large-paired)]
    assert len(components)==22>len(small)+1
    result={'boundary':boundary,'vertices':len(states),'edges':len(edges),
            'orientation_definition':'o(a,b)=+1 iff (b-a) mod 3 is 1 on colors 1,2,3',
            'sigma_definition':'o(x0,x1)*o(x2,x3)',
            'chi_definition':'sigma for x4=0; -sigma for x4=2 or 3',
            'counts_by_last_coordinate':{c:{str(s):sum(w[4]==c and sigma(w)==s for w in states)
                                            for s in (1,-1)} for c in '023'},
            'cut_S':sorted(small),'remaining_vertices':sorted(large),
            'remaining_edges':large_edges,'components_of_B_minus_S':components,
            'component_count':len(components),'Hamilton_path_cut_bound':len(small)+1,
            'strict_cut_obstruction':True,'conclusion':'B_00001 is not traceable',
            'independent_state_and_edge_enumeration':True,
            'graph_input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest()}
    (HERE/'independent-nontraceability-cut-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('components_of_B_minus_S','remaining_vertices')}))

if __name__=='__main__':main()
