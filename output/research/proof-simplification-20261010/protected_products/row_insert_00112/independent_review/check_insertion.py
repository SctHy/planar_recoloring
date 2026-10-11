"""Independent literal verification of the 47-word single-row insertion certificate."""
from pathlib import Path
from itertools import product
import hashlib,json,re

HERE=Path(__file__).resolve().parent


def main():
    data=json.loads((HERE/'core-path-results-v1.json').read_text());answer=data['answer']
    literal=(HERE/'literal-input.tex').read_text()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',literal,re.S))
    edge=lambda a,b:tuple(sorted((a,b)))
    def edges(words):return {edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
    def pairs(tag):return {edge(a,b) for a,b in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[tag])}
    states={''.join(map(str,w)) for w in product(range(4),repeat=5)
        if all(w[i]!=w[(i+1)%5] and w[i]!=(0,0,1,1,2)[i] for i in range(5))}
    assert len(states)==51
    old2=re.findall(r'\b[01][0-3]{5}\b',blocks['C2-00112'])
    assert len(old2)==102 and len(set(old2))==102
    assert set(old2)=={str(r)+w for r in (0,1) for w in states}
    def legal_product_step(a,b):
        return (a[0]==b[0] and sum(x!=y for x,y in zip(a[1:],b[1:]))==1) or (
                abs(int(a[0])-int(b[0]))==1 and a[1:]==b[1:])
    assert all(legal_product_step(a,b) for a,b in edges(old2))
    oldD=pairs('PORTS-00112');oldpool=pairs('POOL-00112-0');oldK=oldD-oldpool
    assert len(oldD)==18 and len(oldpool)==7 and len(oldK)==11
    reserves={edge(*e) for e in answer['reserves']}
    assert reserves=={edge('21020','23020'),edge('21030','31030')}
    assert reserves<=oldpool and edge('12320','12323') not in reserves
    protected=oldK|reserves
    assert protected=={edge(*e) for e in answer['protected_edges']} and len(protected)==13
    path=answer['core_path']
    candidate=(HERE/'candidate-v2.tex').read_text()
    cb=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',candidate,re.S))
    assert re.findall(r'\b[0-3]{5}\b',cb['COREPATH-00112'])==path
    assert {edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',cb['PORTS-00112-INSERTION'])}==protected
    assert {edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',cb['POOL-00112-INSERTION'])}==reserves
    removed={'12303','12323','13203','23203'}
    assert len(path)==47 and len(set(path))==47 and set(path)==states-removed
    assert (path[0],path[-1])==('21201','23201')
    assert all(sum(a!=b for a,b in zip(w,z))==1 for w,z in zip(path,path[1:]))
    assert protected<={edge(a,b) for a,b in zip(path,path[1:])}
    paths=[['12303','12323'],['13203','23203'],path]
    M={edge(w[0],w[-1]) for w in paths}
    assert M=={edge(*e) for e in answer['matching_cuts']}
    assert len(M)==3 and len(set().union(*map(set,M)))==6
    oldedges=edges(old2)
    assert {edge('1'+a,'1'+b) for a,b in M}<=oldedges
    assert not M&protected
    by_pair={edge(w[0],w[-1]):w for w in paths}
    derived=[];cut_count=0
    for a,b in zip(old2,old2[1:]+old2[:1]):
        derived.append(a)
        if a[0]==b[0]=='1' and edge(a[1:],b[1:]) in M:
            sub=by_pair[edge(a[1:],b[1:])]
            if sub[0]!=a[1:]:sub=list(reversed(sub))
            assert sub[0]==a[1:] and sub[-1]==b[1:]
            derived.extend('2'+w for w in sub);cut_count+=1
    assert cut_count==3 and derived==answer['derived_C3']
    assert len(derived)==153 and len(set(derived))==153
    assert set(derived)=={str(r)+w for r in (0,1,2) for w in states}
    ee=edges(derived)
    assert all(legal_product_step(a,b) for a,b in ee)
    row_edges={r:{edge(a[1:],b[1:]) for a,b in ee if a[0]==b[0]==str(r)} for r in (0,1,2)}
    assert all(protected<=row_edges[r] for r in (0,1,2))
    assert protected-reserves==oldK
    extra=edge('32021','32031')
    result={'status':'PASS','independent_generated_states':51,'old_seed_words':102,
        'core_words':47,'matching_row_digit':1,'matching_edges':[list(e) for e in sorted(M)],
        'derived_words':153,'derived_literal_equal_supplied':True,
        'all_153_states_exactly_once':True,'all_cyclic_product_steps_legal':True,
        'old_K_11_exactly_retained':True,'protected_D_prime_13': [list(e) for e in sorted(protected)],
        'two_reserves':[list(e) for e in sorted(reserves)],
        'all_13_edges_retained_in_every_row':True,
        'additional_32021_32031_retained_in_every_row':all(extra in row_edges[r] for r in (0,1,2)),
        'candidate_v2_literal_path_ports_pool_verified':True,
        'candidate_v2_sha256':hashlib.sha256((HERE/'candidate-v2.tex').read_bytes()).hexdigest(),
        'literal_input_sha256':hashlib.sha256((HERE/'literal-input.tex').read_bytes()).hexdigest(),
        'discovery_input_sha256':hashlib.sha256((HERE/'core-path-results-v1.json').read_bytes()).hexdigest(),
        'scope':'independent exact certificate replay only; no path discovery/search'}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
