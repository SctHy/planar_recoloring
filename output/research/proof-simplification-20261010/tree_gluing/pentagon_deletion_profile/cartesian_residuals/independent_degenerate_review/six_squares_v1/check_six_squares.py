#!/usr/bin/env python3
"""Independent exact reader of six selected square certificates only."""
from pathlib import Path
import hashlib,itertools,json,re,shutil,time

BASE=Path(__file__).resolve().parent
PARENT=BASE.parents[1]
ROOT=Path('/Users/huahua815/Downloads/planar_recoloring')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
edge=lambda x,y:tuple(sorted((x,y)))
cyclic_edges=lambda C:{edge(x,y) for x,y in zip(C,C[1:]+C[:1])}
step=lambda x,y:sum(a!=b for a,b in zip(x,y))==1
def legal(x,t):
    return all(x[i]!=x[(i+1)%5] and (t[i]=='4' or x[i]!=t[i]) for i in range(5))
def blocks(s):
    return {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
def cycle(block):
    text='\n'.join(x for x in block.splitlines() if not x.startswith('%'))
    return re.findall(r'(?<![0-9])[0-3]{5}(?![0-9])',text)
def pool(block):
    return {edge(x,y) for x,y in re.findall(r'([0-3]{5})-([0-3]{5})',block)}
def normalize(t,standard):
    tested=0
    for start in range(5):
        for direction in (1,-1):
            for permutation in itertools.permutations('0123'):
                tested+=1
                z=''.join('4' if t[(start+direction*i)%5]=='4' else permutation[int(t[(start+direction*i)%5])] for i in range(5))
                if z in standard:return z,(start,direction,permutation),tested
    raise AssertionError(('unclassified',t))
def restore(x,g):
    start,direction,p=g;out=['']*5
    for i,c in enumerate(x):out[(start+direction*i)%5]=str(p.index(c))
    return ''.join(out)
def main():
    tic=time.monotonic()
    source=PARENT/'phase6-source.tex';candidate=PARENT/'square-capacity-candidate-v1.tex'
    assert sha(source)=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
    for src,name in [(source,'phase6-source.tex'),(candidate,'square-candidate-input.tex')]:
        dst=BASE/name
        if dst.exists():assert dst.read_bytes()==src.read_bytes()
        else:shutil.copy2(src,dst)
    manuscript=source.read_text();live=(ROOT/'planar_recoloring_hamilton_thresholds.tex').read_text()
    frozen,actual=blocks(manuscript),blocks(live)
    relevant=[t for t in frozen if t.startswith(('C1-','FHC-','POOL-'))]
    assert all(frozen[t]==actual[t] for t in relevant)
    convention=lambda s:s.split('Here is the exact normalization convention.',1)[1].split('\\begin{lemma}',1)[0]
    assert convention(manuscript)==convention(live)
    assert 'then $\\epsilon=+1,-1$, then the permutations $p\\in S_4$ in lexicographic' in convention(manuscript)
    C={t.split('-',1)[1]:cycle(b) for t,b in frozen.items() if t.startswith(('C1-','FHC-'))}
    standard=set(C)|{'00000','00001','00112'};assert len(standard)==22
    text=candidate.read_text();table=text.split('\\text{source}&\\text{change}&\\text{square words}',1)[1].split('\\end{array}',1)[0]
    rows=re.findall(r'([0-4]{5})&([0-4])\\to\s*([0-3q])&([^&]+)&([^&]+)&([^&]+)&([^\n]+)',table)
    assert len(rows)==5
    records=[];used=set()
    for rowid,(src,pos,new,pattern,xs,ys,ret) in enumerate(rows,1):
        for q in ((2,3) if new=='q' else (None,)):
            env={'q':str(q),'r':str(5-q)} if q is not None else {}
            value=lambda z:env.get(z,z)
            a,b=[list(map(value,z.replace(' ','').split(','))) for z in (xs,ys)]
            assert len(a)==len(set(a))==len(b)==len(set(b))==2
            pattern=re.sub(r'\s+','',pattern);assert len(pattern)==5 and pattern.count('x')==pattern.count('y')==1
            V={''.join({'x':x,'y':y,**env}.get(c,c) for c in pattern) for x,y in itertools.product(a,b)}
            assert len(V)==4
            changed=list(src);changed[int(pos)]=value(new);target=''.join(changed)
            assert target!=src and all(legal(x,src) and legal(x,target) for x in V)
            E={edge(x,y) for x,y in itertools.combinations(V,2) if step(x,y)}
            assert len(E)==4 and all(sum(x in e for e in E)==2 for x in V)
            normalized,g,tested=normalize(target,standard);assert normalized in C
            source_cycle=C[src];target_cycle=[restore(x,g) for x in C[normalized]]
            A,B=cyclic_edges(source_cycle),cyclic_edges(target_cycle)
            PA=pool(frozen[f'POOL-{src}-0']);PB={edge(restore(x,g),restore(y,g)) for x,y in pool(frozen[f'POOL-{normalized}-0'])}
            assert len(source_cycle)==len(set(source_cycle)) and len(target_cycle)==len(set(target_cycle))
            assert all(legal(x,src) for x in source_cycle) and all(legal(x,target) for x in target_cycle)
            assert all(step(x,y) for x,y in A|B) and PA<=A and PB<=B
            assert not(E&PA) and not(E&PB)
            claimed=re.findall(r'\((\d+),(\d+)\)(?:\\text\{ if \}q=(\d))?',ret)
            chosen=[(int(x),int(y)) for x,y,condition in claimed if not condition or int(condition)==q]
            assert len(chosen)==1
            count=(len(A&E),len(B&E));assert count==chosen[0]
            capacity=sum(count)-4;assert capacity in (1,2)
            used|={src,normalized}
            records.append({'printed_row':rowid,'source':src,'boundary_change':{'position':int(pos),'new_colour':value(new)},'actual_target_boundary':target,'normalized_target_type':normalized,'first_normalizer':{'start':g[0],'direction':g[1],'permutation_old_to_new':list(g[2]),'candidate_maps_tested':tested},'square_vertices':sorted(V),'four_square_edges':[list(e) for e in sorted(E)],'source_cycle_order':len(source_cycle),'target_cycle_order':len(target_cycle),'source_retained_square_edges':[list(e) for e in sorted(A&E)],'target_retained_square_edges':[list(e) for e in sorted(B&E)],'retention_counts':list(count),'claimed_retention_counts':list(chosen[0]),'source_pool_square_intersection':[],'restored_target_pool_square_intersection':[],'protected_capacity_lower_bound':capacity})
    assert len(records)==6 and sum(r['protected_capacity_lower_bound']==2 for r in records)==2
    result={'verdict':'PASS','scope':'Only the six numeric square interfaces in the first five-row table; reflection case excluded','candidate_sha256':sha(candidate),'frozen_phase6_sha256':sha(source),'live_main_sha256_at_review':sha(ROOT/'planar_recoloring_hamilton_thresholds.tex'),'script_sha256':sha(Path(__file__)),'actual_main_relevant_blocks_equal_phase6':len(relevant),'normalizer_convention_byte_exact_to_main':True,'five_printed_rows':5,'six_expanded_interfaces':6,'all_square_vertices_legal_in_both_fibres':True,'all_squares_have_exactly_four_legal_edges':True,'all_source_and_target_retention_counts_match_table':True,'all_pools_avoid_square_edges':True,'first_normalizers_regenerated_without_peer_helpers':True,'used_cycle_types':sorted(used),'records':records,'new_Hamilton_search':False,'full313_replay':False,'actual_source_target_cycle_intersections_computed':False,'elapsed_seconds':time.monotonic()-tic,'evidence_boundary':'Independent exact bounded selected-certificate readback; inclusion-exclusion is the mathematical argument. No arbitrary-cycle, alternative-normalizer or formal-verification claim.'}
    (BASE/'six-square-review-results-v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'verdict':result['verdict'],'main':result['live_main_sha256_at_review'],'cases':[{k:r[k] for k in ('source','boundary_change','actual_target_boundary','normalized_target_type','retention_counts','protected_capacity_lower_bound')} for r in records],'elapsed_seconds':result['elapsed_seconds']},indent=2))

if __name__=='__main__':main()
