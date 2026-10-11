#!/usr/bin/env python3
"""Global word reuse for the two frozen-mask source families; no graph work."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent


def run():
    p=HERE/"set-cover-results.json"
    raw=p.read_bytes()
    r=json.loads(raw)
    families=r["source_families"]
    masks={}
    offset=0
    for t in ("01023","01124"):
        for x,data in families[t]["state_masks"].items():
            masks[x]=masks.get(x,0)|(data["mask_decimal"]<<offset)
        offset+=families[t]["interface_count"]
    assert offset==27
    words=sorted(masks)
    assert len(words)<=16
    full=(1<<27)-1
    counts=Counter()
    minimum=len(words)+1
    optimal=[]
    for subset in range(1<<len(words)):
        chosen=[words[i] for i in range(len(words)) if subset&(1<<i)]
        union=0
        for x in chosen:
            union|=masks[x]
        if union==full:
            counts[len(chosen)]+=1
            if len(chosen)<minimum:
                minimum=len(chosen);optimal=[chosen]
            elif len(chosen)==minimum:
                optimal.append(chosen)
    preferred=sorted({x for f in families.values() for x in f["selected_words"]})
    assert len(preferred)==minimum==8
    assert preferred in optimal
    out=dict(status="PASS",python=platform.python_version(),input_sha256=hashlib.sha256(raw).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),interface_count=27,candidate_distinct_words=words,candidate_count=len(words),total_subsets_checked=1<<len(words),minimum_distinct_words=minimum,preferred_selected_distinct_words=preferred,preferred_source_family_words={t:families[t]["selected_words"] for t in families},number_of_minimum_global_covers=len(optimal),all_minimum_global_covers=sorted(optimal),cover_count_by_cardinality={str(i):counts[i] for i in range(len(words)+1)},shared_word_between_preferred_family_rows="32301",scope="Exact global set cover of27frozen interface masks with the saved candidate source words; no neighbour or Hamilton computation.")
    (HERE/"global-cover-results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","minimum_distinct_words","preferred_selected_distinct_words","number_of_minimum_global_covers","total_subsets_checked")},indent=2))


if __name__=="__main__":
    run()
