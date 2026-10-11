"""Natural stabilizers of the fixed cycles/common seed edges, before pool edits."""
from pathlib import Path
from itertools import product,permutations
import hashlib,json,re,time
from base_check import STANDARD,HARD,edge,word_tuple,word_text,cycle_edges,transform

HERE=Path(__file__).resolve().parent
SOURCE=Path('/Users/huahua815/Downloads/planar_recoloring/planar_recoloring_hamilton_thresholds.tex')


def main():
    started=time.perf_counter()
    raw=(HERE/'literal-input.tex').read_bytes(); literal=raw.decode()
    blocks=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',literal,re.S))
    current=dict(re.findall(r'% BEGIN ([A-Z0-9-]+)\n(.*?)% END \1',SOURCE.read_text(),re.S))
    def words(tag,width=5):return [word_tuple(w) for w in re.findall(r'\b[0-3]{'+str(width)+r'}\b',blocks[tag])]
    def edge_list(tag):return [edge(word_tuple(a),word_tuple(b)) for a,b in re.findall(r'\b([0-3]{5})-([0-3]{5})\b',blocks[tag])]
    def moved(es,g):return {edge(transform(a,g),transform(b,g)) for a,b in es}
    groups=[(s,eps,p) for s in range(5) for eps in (1,-1) for p in permutations(range(4))]
    identity=(0,1,(0,1,2,3))
    details=[]; tags_used=set()
    for t in STANDARD:
        if t=='00000': continue
        states={w for w in product(range(4),repeat=5)
            if all(w[i]!=w[(i+1)%5] for i in range(5))
            and all(t[i]=='4' or w[i]!=int(t[i]) for i in range(5))}
        pooltag='POOL-'+t+'-0'; tags_used.add(pooltag)
        pool=edge_list(pooltag)
        if t in HARD:
            tag='COMMON-00001' if t=='00001' else 'PORTS-00112'
            support=set(edge_list(tag)); tags_used.add(tag)
            seedtags=('PC2-00001','PC3-00001') if t=='00001' else ('C2-00112','C3-00112')
            common=None
            for st,rows in zip(seedtags,(2,3)):
                tags_used.add(st); seed=cycle_edges(words(st,6))
                for r in range(rows):
                    row={edge(a[1:],b[1:]) for a,b in seed if a[0]==b[0]==r}
                    common=row if common is None else common&row
            assert support<=common
        else:
            tag=('FHC-' if '4' in t else 'C1-')+t; tags_used.add(tag)
            support=cycle_edges(words(tag)); common=support
            assert len(support)==len(states)
        assert set(pool)<=support
        boundary_group=[g for g in groups if word_text(transform(word_tuple(t),g))==t]
        assert all({transform(w,g) for w in states}==states for g in boundary_group)
        support_group=[g for g in boundary_group if moved(support,g)==support]
        common_group=[g for g in boundary_group if moved(common,g)==common]
        K=support-set(pool)
        K_group=[g for g in boundary_group if moved(K,g)==K]
        failures=[]
        for g in boundary_group:
            if g in support_group: continue
            lost=min(moved(support,g)-support)
            original=min(e for e in support if edge(transform(e[0],g),transform(e[1],g))==lost)
            failures.append({'action':g,'support_edge':[word_text(w) for w in original],
                'image_not_in_fixed_support':[word_text(w) for w in lost]})
        # Even if the full support breaks g, a smaller invariant subset might
        # survive. Compute the exact maximal cyclic-invariant core, then
        # exclude all orbits of the two already-used ordinary seed edges.
        invariant_bounds=[]
        for g in boundary_group:
            if g==identity: continue
            core=set(support); cur=moved(support,g); period=1
            while cur!=support:
                core &= cur; cur=moved(cur,g); period+=1
                assert period<=60
            if t not in HARD:
                for e in pool[:2]:
                    orbit={e}; cur=next(iter(moved({e},g)))
                    while cur!=e:
                        orbit.add(cur); cur=next(iter(moved({cur},g)))
                        assert len(orbit)<=60
                    core -= orbit
            forced_pool=support-core
            invariant_bounds.append({'action':g,'support_set_period':period,
                'maximal_seed_compatible_invariant_K_size':len(core),
                'minimum_pool_deletions':len(forced_pool),
                'strict_shrink_size_cap':len(pool)-1,
                'strict_shrink_ruled_out_by_lower_bound':len(forced_pool)>len(pool)-1,
                'forced_deleted_edges':[[word_text(w) for w in e] for e in sorted(forced_pool)]})
        details.append({'type':t,'kind':'hard-common' if t in HARD else 'cycle',
            'vertices':len(states),'support_edges':len(support),'actual_seed_common_edges':len(common),
            'boundary_group_size':len(boundary_group),'support_group_size':len(support_group),
            'actual_common_group_size':len(common_group),'current_K_group_size':len(K_group),
            'boundary_group':boundary_group,'support_group':support_group,
            'actual_common_group':common_group,'support_failures':failures,
            'cyclic_invariant_pool_lower_bounds':invariant_bounds,
            'fixed_ordinary_seed_cut_edges':[[word_text(w) for w in e] for e in pool[:2]] if t not in HARD else [],
            'minimum_new_pool_size':2 if t in HARD else 4})
    unchanged=all(current.get(tag)==blocks[tag] for tag in tags_used)
    assert unchanged,'current relevant cycles/seeds/pools/interfaces differ from frozen input'
    result={'scope':'all 21 nonconstant components; no Hamilton search or manuscript edits',
        'input_sha256':hashlib.sha256(raw).hexdigest(),
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'current_relevant_literal_tags_equal_frozen':unchanged,'checked_tags':sorted(tags_used),
        'details':details,'elapsed_seconds':time.perf_counter()-started}
    (HERE/'support-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('details','checked_tags')}|
        {'summary':[{k:d[k] for k in ('type','kind','vertices','support_edges','actual_seed_common_edges','boundary_group_size','support_group_size','actual_common_group_size','current_K_group_size')} for d in details]}))


if __name__=='__main__':main()
