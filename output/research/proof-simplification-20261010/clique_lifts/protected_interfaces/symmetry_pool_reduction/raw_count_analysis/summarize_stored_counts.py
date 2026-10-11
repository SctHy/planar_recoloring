"""Summarize already-stored raw-edge counts; do not regenerate a graph or kernel."""
from pathlib import Path
from collections import Counter
import hashlib,json,re

HERE=Path(__file__).resolve().parent


def main():
    raw=(HERE/'stored-witness-orbit-results.json').read_bytes();stored=json.loads(raw)
    variant=next(v for v in stored['variants'] if v['name']=='nonconstant-four-two-pools')
    text=(HERE/'literal-input.tex').read_text()
    block=re.search(r'% BEGIN INTERFACES-ALL\n(.*?)% END INTERFACES-ALL',text,re.S).group(1)
    records=re.findall(r'([0-4]{5}:[01])\s+([0-4])\s+([0-3])\s+([0-4]{5}:[01])\s+([0-3]{5})-([0-3]{5})',block)
    assert len(records)==313
    def kind(key):
        t=key[:5]
        if t=='00000':return 'constant-cycle'
        if t in {'00001','00112'}:return 'hard'
        return 'starred-cycle' if '4' in t else 'ordinary-cycle'
    def category(d):
        a,b=kind(d['source']),kind(d['target'])
        if b=='constant-cycle':return a+'-constant'
        return 'hard-hard' if a==b=='hard' else 'one-hard' if 'hard' in (a,b) else 'cycle-cycle'
    counts=variant['raw_count_bounds'];assert len(counts)==283
    def stats(ds):
        return {'cases':len(ds),'minimum_raw_edges':min(d['raw_common_edges'] for d in ds),
            'pool_sum_thresholds':sorted({d['removed_pool_sum']+1 for d in ds}),
            'qualified':sum(d['pigeonhole_guarantee'] for d in ds),
            'unqualified':sum(not d['pigeonhole_guarantee'] for d in ds),
            'minimum_raw_among_qualified':min((d['raw_common_edges'] for d in ds if d['pigeonhole_guarantee']),default=None)}
    coarse={c:stats([d for d in counts if category(d)==c]) for c in sorted({category(d) for d in counts})}
    fine={c:stats([d for d in counts if kind(d['source'])+'->'+kind(d['target'])==c])
          for c in sorted({kind(d['source'])+'->'+kind(d['target']) for d in counts})}
    sources={c:stats([d for d in counts if d['source']==c]) for c in sorted({d['source'] for d in counts})}
    residual=[]
    for d in counts:
        if d['pigeonhole_guarantee']:continue
        source,pos,new,target,a,b=records[d['id']]
        assert source==d['source'] and target==d['target']
        residual.append({**d,'position':int(pos),'new_excluded':int(new),'category':category(d),
            'needed_raw_edges':d['removed_pool_sum']+1,
            'meaning':'count bound is insufficient; a valid protected witness still exists'})
    assert len(residual)==29 and sum(d['pigeonhole_guarantee'] for d in counts)==254
    result={'scope':'read-only summary of previously stored counts; no graph generation or kernel replay',
        'stored_input_sha256':hashlib.sha256(raw).hexdigest(),
        'variant':variant['name'],'cases':283,'qualified':254,'residual':29,
        'coarse_categories':coarse,'fine_categories':fine,'by_source_type':sources,
        'residual_interfaces':residual,
        'limitations':['counts use the old fixed hard common sets19 and18 and the four/two-pool candidate',
            'new00112 derived Dprime13 is not substituted into these stored counts',
            'a finite observed minimum is not an analytic template lower bound']}
    (HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('scope','qualified','residual','coarse_categories','fine_categories')}))


if __name__=='__main__':main()
