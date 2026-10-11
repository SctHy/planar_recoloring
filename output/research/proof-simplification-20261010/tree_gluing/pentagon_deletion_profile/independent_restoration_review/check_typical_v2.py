"""Literal correction readback for frozen typical note-v2; no peer helpers."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json,re

HERE=Path(__file__).resolve().parent
def edge(u,v):return tuple(sorted((u,v)))
def parse(w):return tuple(map(int,w))

def main():
    source=HERE/'phase6-source-v1.tex';note=HERE/'coordinate-note-v2.tex';src=source.read_text();text=note.read_text()
    def block(n):return re.search('% BEGIN '+n+'\n(.*?)% END '+n,src,re.S).group(1)
    words=[parse(w) for w in re.findall(r'\b[0-3]{5}\b',block('C1-00101'))]
    C={edge(u,v) for u,v in zip(words,words[1:]+words[:1])}
    pool={edge(parse(u),parse(v)) for u,v in re.findall(r'([0-3]{5})-([0-3]{5})',block('POOL-00101-0'))}
    def legal(t):return {w for w in product(range(4),repeat=5) if all(w[i]!=w[(i+1)%5] and w[i]!=t[i] for i in range(5))}
    def g(w):return tuple((1,0,2,3)[w[-j%5]] for j in range(5))
    U=legal(parse('00101'))&legal(parse('10101'))
    H={edge(u,v) for u,v in combinations(U,2) if sum(a!=b for a,b in zip(u,v))==1}
    J={e for e in H if e[0][0]!=e[1][0]};D={edge(g(u),g(v)) for u,v in C};Q={edge(g(u),g(v)) for u,v in pool}
    listed_block=text.split('(x,y)=')[1].split('\\]')[0]
    listed=[tuple(map(int,p)) for p in re.findall(r'\(([0-3]),([0-3])\)',listed_block)]
    listed_edges={edge((2,1,x,y,0),(3,1,x,y,0)) for x,y in listed}
    assert len(listed)==6 and listed_edges==C&J
    assert len(C&J)==len(D&J)==6 and len(J)==7
    assert (pool|Q)&J=={edge(parse('21010'),parse('31010'))}
    assert {edge(g(u),g(v)) for u,v in J}==J
    assert {edge(g(u),g(v)) for u,v in C&J}!=C&J
    assert edge(parse('21310'),parse('31310')) in C&J and edge(parse('21030'),parse('31030')) not in C&J
    assert edge(g(parse('21310')),g(parse('31310')))==edge(parse('21030'),parse('31030'))
    assert re.search(r'5\+5-6=4',text) and 'six of these seven' in text
    assert 'entire six-edge selected subset is not invariant' in text
    safe=(C-pool)&(D-Q)&J;assert len(safe)==4
    result={'status':'PASS','note_v2_sha256':hashlib.sha256(note.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'printed_six_pairs_match_actual_source_cycle':True,
            'source_and_target_retention_counts':[6,6],'common_coordinate_universe':7,'pool_union_count':1,
            'printed_corrected_bound':4,'noninvariance_statement_and_extra_edge_image_verified':True,
            'old_note_v1_and_correction_verdict_left_unchanged':True,
            'scope':'Literal corrected note for this selected pair only; no general-Hamilton-cycle claim.'}
    (HERE/'typical-v2-review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
