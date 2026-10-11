"""Four local interfaces and a common canonical target edge; no full-kernel replay."""
from pathlib import Path
import hashlib,json,re
from base_check import edge,word_tuple,word_text,cycle_edges,transform,normalize

HERE=Path(__file__).resolve().parent


def main():
    raw=(HERE/'literal-input.tex').read_bytes()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',raw.decode(),re.S))
    def words(tag,width=5):return [word_tuple(w) for w in re.findall(r'\b[0-3]{'+str(width)+r'}\b',blocks[tag])]
    def elist(tag):return [edge(word_tuple(a),word_tuple(b)) for a,b in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[tag])]
    CA=cycle_edges(words('C1-00011'));DB=set(elist('PORTS-00112'))
    oldA=elist('POOL-00011-0');oldB=elist('POOL-00112-0')
    PA=[oldA[0],oldA[1],oldA[-2],oldA[-1]]
    # Any two old hard pool edges work; avoid the bad leaf-neighbor reserve
    # 12320--12323 so this choice also leaves later seed-insertion research open.
    PB=[oldB[0],oldB[2]]
    assert len(set(PA))==4 and set(PA)<=set(oldA)
    assert len(set(PB))==2 and set(PB)<=set(oldB)
    KA=CA-set(PA);KB=DB-set(PB)
    assert CA-set(oldA)<=KA and DB-set(oldB)<=KB
    for tag,rows in (('C2-00112',2),('C3-00112',3)):
        seed=cycle_edges(words(tag,6))
        for r in range(rows):
            internal={edge(a[1:],b[1:]) for a,b in seed if a[0]==b[0]==r}
            assert set(PB)<=internal
    e=edge(word_tuple('13202'),word_tuple('13203'))
    f=edge(word_tuple('32021'),word_tuple('32031'))
    cases=[]
    for j in (0,2):
        for q in (2,3):
            p=(0,1,2,3) if q==2 else (0,1,3,2)
            action=(0,1,p) if j==0 else (2,-1,p)
            image=edge(*(transform(w,action) for w in e))
            t=list(map(int,'00011'));t[j]=q
            target,N=normalize(tuple(t))
            assert target=='00112' and N==(1,1 if j==0 else -1,p)
            normalized=edge(*(transform(w,N) for w in image))
            assert normalized==f and image in KA and f in KB
            cases.append({'position':j,'new_excluded':q,'source_edge':[word_text(w) for w in image],
                'canonical_normalizer':N,'normalized_target_edge':[word_text(w) for w in normalized]})
    result={'scope':'four fixed interfaces only; no full-kernel run or Hamilton search',
        'input_sha256':hashlib.sha256(raw).hexdigest(),
        'candidate_source_pool':[[word_text(w) for w in z] for z in PA],
        'candidate_target_pool':[[word_text(w) for w in z] for z in PB],
        'old_source_pool_size':len(oldA),'old_target_pool_size':len(oldB),
        'candidate_pools_are_subsets_of_old':True,'both_hard_reserves_present_in_all_five_seed_rows':True,
        'seed':[word_text(w) for w in e],'common_canonical_target_edge':[word_text(w) for w in f],
        'cases':cases,'claim':'four interfaces share the proved normalization family; all other already-valid interfaces survive by K monotonicity'}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
