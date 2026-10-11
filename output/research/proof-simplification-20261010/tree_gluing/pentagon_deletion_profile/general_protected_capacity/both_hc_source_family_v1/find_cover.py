#!/usr/bin/env python3
"""Exact set cover of frozen positive certificates; no graph computation."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import platform
import time

HERE = Path(__file__).resolve().parent


def solve(rows):
    indexed = sorted(rows, key=lambda r:(r["interface"]["position"],r["interface"]["colour"],r["interface"]["target_type"],r["interface"]["target_component"]))
    masks = {}
    observations = {}
    for i,row in enumerate(indexed):
        for o in row["certificates"]:
            assert o["safe_common_edge_lower_bound"] == max(0,4-o["source_degree"]-o["target_degree"]+o["common_incident_count"]-o["forbidden_common_count"]) > 0
            masks[o["state"]] = masks.get(o["state"],0) | (1<<i)
            observations[o["state"],i] = o
    words = sorted(masks)
    assert len(words) <= 64 and len(indexed) <= 15
    full = (1<<len(indexed))-1
    covers_by_size = Counter()
    all_minimum = []
    minimum = len(words)+1
    for subset in range(1<<len(words)):
        chosen = [words[i] for i in range(len(words)) if subset & (1<<i)]
        union = 0
        for x in chosen:
            union |= masks[x]
        if union == full:
            size = len(chosen)
            covers_by_size[size] += 1
            if size < minimum:
                minimum = size
                all_minimum = [chosen]
            elif size == minimum:
                all_minimum.append(chosen)
    assert minimum <= len(words)
    selected = min(all_minimum)
    mapping = []
    for i,row in enumerate(indexed):
        available = [x for x in selected if masks[x] & (1<<i)]
        assert available
        x = min(available)
        mapping.append(dict(interface_index=i,interface=row["interface"],selected_state=x,all_selected_covering_states=available,certificate=observations[x,i]))
    return dict(interface_count=len(indexed),candidate_state_count=len(words),candidate_states=words,state_masks={x:dict(mask_decimal=masks[x],mask_bits=format(masks[x],f"0{len(indexed)}b"),covered_interface_indices=[i for i in range(len(indexed)) if masks[x]&(1<<i)]) for x in words},full_mask_decimal=full,total_subsets_checked=1<<len(words),minimum_word_count=minimum,selected_words=selected,number_of_minimum_covers=len(all_minimum),all_minimum_covers=sorted(all_minimum),cover_count_by_cardinality={str(i):covers_by_size[i] for i in range(len(words)+1)},coverage_map=mapping)


def run():
    start=time.perf_counter()
    p=HERE/"frozen-both-hc-local-results.json"
    raw=p.read_bytes()
    r=json.loads(raw)
    assert r["status"]=="PASS" and hashlib.sha256(raw).hexdigest()=="36ee26c64c667dbb7bea0bc88eed3b3162c85cbae16038da3a01cd59eeca68b1"
    families={t:solve([row for row in r["records"] if row["interface"]["source"]==t]) for t in ("01023","01124")}
    assert families["01023"]["interface_count"]==15 and families["01124"]["interface_count"]==12
    out=dict(status="PASS",python=platform.python_version(),input_sha256=hashlib.sha256(raw).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),source_families=families,total_original_case_selectors=27,total_minimum_source_words=sum(f["minimum_word_count"] for f in families.values()),total_state_word_subsets_checked=sum(f["total_subsets_checked"] for f in families.values()),elapsed_seconds=time.perf_counter()-start,scope="Minimum set cover of already frozen positive local certificates for two specified normalized source types; no new neighbour generation, graph-state enumeration or Hamilton search.")
    (HERE/"set-cover-results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(status=out["status"],python=out["python"],total_minimum_source_words=out["total_minimum_source_words"],total_state_word_subsets_checked=out["total_state_word_subsets_checked"],families={t:{k:f[k] for k in ("interface_count","candidate_state_count","minimum_word_count","selected_words","number_of_minimum_covers")} for t,f in families.items()}),indent=2))


if __name__=="__main__":
    run()
