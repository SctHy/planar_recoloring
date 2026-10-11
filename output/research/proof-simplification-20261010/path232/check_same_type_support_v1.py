"""Two fixed support cases and their 24 color images/reversals, not the 360 kernel."""
from pathlib import Path
from itertools import permutations,product
import hashlib,json,re

HERE=Path(__file__).resolve().parent

def edges(words,cyclic=True):
    return {frozenset((a,b)) for a,b in zip(words,words[1:]+(words[:1] if cyclic else []))}

def image(words,p,reverse=False):
    return [''.join(str(p[int(c)]) for c in (w[::-1] if reverse else w)) for w in words]

def special(t):
    if t[0]==t[1]!=t[2]:a,b,j=t[0],t[2],2
    elif t[1]==t[2]!=t[0]:a,b,j=t[1],t[0],0
    else:return set()
    all_words=[''.join(map(str,x)) for x in product(range(4),repeat=3)
               if x[0]!=x[1]!=x[2] and all(x[i]!=t[i] for i in range(3))]
    answer=set()
    for c in set(range(4))-{a,b}:
        layer=[w for w in all_words if int(w[1])==c and int(w[0])!=a and int(w[2])!=a]
        es={frozenset((u,v)) for i,u in enumerate(layer) for v in layer[i+1:]
            if sum(x!=y for x,y in zip(u,v))==1}
        assert len(es)==1
        answer|=es
    return answer

def main():
    inp=HERE/'same-type-support-input-v1.tex';s=inp.read_text()
    parts=re.search(r'001&(.*?)010&(.*?)012&(.*?)\\end\{array\}',s,re.S).groups()
    E,M,A=[re.findall(r'\b[0-3]{3}\b',part) for part in parts]
    assert [len(E),len(M),len(A)]==[14,17,16]
    records=[]
    for p in permutations(range(4)):
        for rev in (False,True):
            source=edges(image(E,p,rev))
            target=edges(image(E,(p[1],p[0],p[2],p[3]),not rev))
            t=image(['001'],p,rev)[0];u=image(['011'],p,rev)[0]
            c=p[2];a,b,d=p[0],p[1],p[3]
            square=[f'{b}{c}{a}',f'{b}{c}{d}',f'{d}{c}{d}',f'{d}{c}{a}']
            path=[f'{d}{c}{a}',f'{b}{c}{a}',f'{b}{c}{d}']
            if rev:square=[w[::-1] for w in square];path=[w[::-1] for w in path]
            sq=edges(square);pp=edges(path,False)
            pt=special(tuple(map(int,t)));pu=special(tuple(map(int,u)))
            assert len(source&sq)==len(target&sq)==3
            assert (source&sq)-pt==(target&sq)-pu==pp
            assert len(pp)==2 and pp<=source&target and not pp&(pt|pu)
            records.append({'family':'E middle change','map':p,'reversal':rev,'safe_shared_square_edges':sorted(sorted(e) for e in pp)})

            source=edges(image(A,p,rev))
            target=edges(image(A,(p[0],p[3],p[2],p[1]),rev))
            a,b,c,d=p
            ring=[f'{b}{a}{b}',f'{b}{a}{d}',f'{c}{a}{d}',f'{d}{a}{d}',f'{d}{a}{b}',f'{c}{a}{b}']
            if rev:ring=[w[::-1] for w in ring]
            hh=edges(ring)
            assert len(hh)==6 and len(source&hh)==len(target&hh)==5
            assert len(source&target&hh)==4
            records.append({'family':'A middle change','map':p,'reversal':rev,'common_hexagon_edge_count':4})
    result={'frozen_cycle_input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
            'E_normalized_case':[0,0,1,0,1,1],'A_normalized_case':[0,1,2,0,3,2],
            'scope':'two support cases and their 24 color images and reversals; no full-interface enumeration',
            'checked_case_images':len(records),'all_assertions_pass':True,'records':records,
            'remaining_table_entries':8,'remaining_representative_rows':7}
    (HERE/'same-type-support-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))

if __name__=='__main__':main()
