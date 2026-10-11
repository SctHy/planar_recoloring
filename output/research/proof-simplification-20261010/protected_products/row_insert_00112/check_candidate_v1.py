"""Direct readback of the proposed 47-word certificate and subdivision seed."""
from pathlib import Path
from itertools import product
import hashlib,json,re

HERE=Path(__file__).resolve().parent

def main():
    source=HERE/'literal-input.tex';text=source.read_text()
    proposal=HERE/'candidate-v1.tex';candidate=proposal.read_text()
    def block(name):return re.search('% BEGIN '+name+'\n(.*?)% END '+name,text,re.S).group(1)
    def read_edges(name):return {tuple(sorted(e)) for e in re.findall(r'([0-3]{5})-([0-3]{5})',block(name))}
    D=read_edges('PORTS-00112');pool=read_edges('POOL-00112-0');K=D-pool
    R={('21020','23020'),('21030','31030')};Dnew=K|R
    assert len(K)==11 and len(Dnew)==13 and R<=pool and Dnew-R==K
    pblock=re.search('% BEGIN COREPATH-00112\n(.*?)% END COREPATH-00112',candidate,re.S).group(1)
    P=re.findall(r'\b[0-3]{5}\b',pblock)
    states={''.join(map(str,x)) for x in product(range(4),repeat=5)
            if all(x[i]!=x[(i+1)%5] and str(x[i])!='00112'[i] for i in range(5))}
    assert len(states)==51 and len(P)==47 and len(set(P))==47
    leafpairs=[('12303','12323'),('13203','23203')]
    assert set(P)|{v for e in leafpairs for v in e}==states
    assert not set(P)&{v for e in leafpairs for v in e}
    assert P[0]=='21201' and P[-1]=='23201'
    assert all(sum(a!=b for a,b in zip(x,y))==1 for x,y in zip(P,P[1:]))
    pedges={tuple(sorted(e)) for e in zip(P,P[1:])}
    assert Dnew<=pedges
    paths={tuple(sorted(e)):list(e) for e in leafpairs}
    paths[('21201','23201')]=P
    assert len({v for e in paths for v in e})==6
    old=re.findall(r'\b[01][0-3]{5}\b',block('C2-00112'));assert len(old)==102
    old_edges={tuple(sorted(e)) for e in zip(old,old[1:]+old[:1])}
    assert all(tuple('1'+v for v in e) in old_edges for e in paths)
    assert not set(paths)&Dnew
    derived=[]
    for a,b in zip(old,old[1:]+old[:1]):
        derived.append(a);key=tuple(sorted((a[1:],b[1:])))
        if a[0]==b[0]=='1' and key in paths:
            path=paths[key]
            if path[0]!=a[1:]:path=path[::-1]
            assert path[0]==a[1:] and path[-1]==b[1:]
            derived.extend('2'+v for v in path)
    assert len(derived)==153 and len(set(derived))==153
    assert set(derived)=={str(row)+v for row in range(3) for v in states}
    new_edges={tuple(sorted(e)) for e in zip(derived,derived[1:]+derived[:1])}
    for a,b in new_edges:
        if a[0]==b[0]:assert sum(x!=y for x,y in zip(a[1:],b[1:]))==1
        else:assert abs(int(a[0])-int(b[0]))==1 and a[1:]==b[1:]
    for row in range(3):assert all(tuple(str(row)+v for v in e) in new_edges for e in Dnew)
    lost_old=old_edges-new_edges
    assert lost_old=={tuple('1'+v for v in e) for e in paths}
    result={'status':'PASS','candidate_sha256':hashlib.sha256(proposal.read_bytes()).hexdigest(),
            'literal_input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'K_unchanged':True,'new_D_size':13,'new_pool':sorted(R),
            'all_47_words_legal_unique':True,'covers_exact_complement_of_two_leaf_pairs':True,
            'all_13_protected_edges_in_path':True,'three_disjoint_old_row1_cuts':sorted(paths),
            'derived_C3_states':len(derived),'all_153_states_once':True,
            'all_cartesian_cycle_edges_legal':True,'all_D_edges_retained_in_all_three_rows':True,
            'old_cycle_edges_lost_only_the_three_designated_cuts':True,'derived_C3':derived}
    (HERE/'candidate-readback-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='derived_C3'}))

if __name__=='__main__':main()
