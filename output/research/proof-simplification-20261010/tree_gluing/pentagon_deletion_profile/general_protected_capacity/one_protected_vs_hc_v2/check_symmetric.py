#!/usr/bin/env python3
"""One fixed protected set vs any opposite HC; original-map two-direction scope."""
from pathlib import Path
from itertools import permutations
from collections import Counter
import hashlib
import json
import platform
import re
import time

HERE = Path(__file__).resolve().parent
COL = frozenset(range(4))
HARD = {"00001", "00112"}


def word(s):
    return tuple(map(int, s))


def text(w):
    return "".join(map(str, w))


def edge(a, b):
    return tuple(sorted((a, b)))


def local(x, t):
    out = set()
    terms = []
    for i in range(5):
        forbidden = {x[(i-1) % 5], x[(i+1) % 5]}
        if t[i] != 4:
            forbidden.add(t[i])
        allowed = COL-forbidden
        assert x[i] in allowed
        terms.append(len(allowed)-1)
        for c in allowed-{x[i]}:
            z = list(x)
            z[i] = c
            out.add(tuple(z))
    assert len(out) == sum(terms)
    return out, terms


def analyze(fixed_k, ordinary_states, hc_boundary, hc_pool):
    incident = {}
    for a, b in fixed_k:
        incident.setdefault(a, set()).add(b)
        incident.setdefault(b, set()).add(a)
    candidates = sorted(set(incident) & ordinary_states)
    observations = []
    for x in candidates:
        neighbours, terms = local(x, hc_boundary)
        assert neighbours <= ordinary_states
        safe = {z for z in neighbours if z in incident[x] and edge(x, z) not in hc_pool}
        d, g = len(neighbours), len(safe)
        assert d >= 2 and g <= 2
        observations.append(dict(state=text(x), HC_side_degree=d, safe_incident_count=g, protected_edge_lower_bound=max(0,2+g-d), HC_side_degree_terms=terms, HC_side_neighbours=sorted(map(text, neighbours)), safe_fixed_K_neighbours=sorted(map(text, safe))))
    return dict(covered=any(o["protected_edge_lower_bound"] for o in observations), candidate_vertices=len(candidates), certificates=[o for o in observations if o["protected_edge_lower_bound"]], all_local_observations=observations)


def run():
    begin = time.perf_counter()
    source_path = HERE / "phase6-source.tex"
    original_path = HERE / "original-forward-results.json"
    original = json.loads(original_path.read_text())
    source = source_path.read_text()
    blocks = {}
    name = None
    for line in source.splitlines(keepends=True):
        if line.startswith("% BEGIN "):
            name = line[8:].strip()
            assert name not in blocks
            blocks[name] = ""
        elif line.startswith("% END "):
            assert line[6:].strip() == name
            name = None
        elif name is not None:
            blocks[name] += line
    assert len(blocks) == 53
    pools = {}
    for key, content in blocks.items():
        if key.startswith("POOL-"):
            _, t, c = key.split("-")
            pools[t, int(c)] = {edge(word(a), word(b)) for a, b in re.findall(r"\b([0-3]{5})-([0-3]{5})\b", content)}
    types = {t for t, c in pools}
    ordinary = {}
    for key, content in blocks.items():
        if key.startswith(("C1-", "FHC-")):
            ordinary[key.split("-")[1], 0] = [word(w) for w in re.findall(r"\b[0-3]{5}\b", content)]
    const = [word(w) for w in re.findall(r"\b[0-3]{5}\b", blocks["FACTOR-00000"])]
    ordinary["00000",0], ordinary["00000",1] = const[:15], const[15:]
    K = {}
    for key, pool in pools.items():
        t, c = key
        if t in HARD:
            basis = {edge(word(a),word(b)) for a,b in re.findall(r"\b([0-3]{5})-([0-3]{5})\b", blocks["COMMON-00001" if t == "00001" else "PORTS-00112"])}
            assert len(basis) == 13 and len(pool) == 2
        else:
            cyc = ordinary[key]
            basis = {edge(cyc[i],cyc[(i+1) % len(cyc)]) for i in range(len(cyc))}
        assert pool <= basis
        K[key] = basis-pool
    colour_maps = list(permutations(range(4)))

    def first(actual):
        for start in range(5):
            for direction in (1,-1):
                for perm in colour_maps:
                    n = text(tuple(4 if actual[(start+direction*i)%5] == 4 else perm[actual[(start+direction*i)%5]] for i in range(5)))
                    if n in types:
                        return n,(start,direction,perm)
        raise AssertionError(actual)

    def restore(w,mapping):
        start,direction,perm = mapping
        inverse = {perm[i]:i for i in range(4)}
        out = [None]*5
        for i in range(5):
            out[(start+direction*i)%5] = inverse[w[i]]
        return tuple(out)

    identity_rows = []
    pattern = r"\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b"
    parsed = re.findall(pattern,blocks["INTERFACES-ALL"])
    assert len(parsed) == 283
    for t,sc,pos,colour,nt,tc,a,b in parsed:
        identity_rows.append((t,int(sc),int(pos),int(colour),nt,int(tc),"existing283"))
    for sc in range(2):
        for pos in range(5):
            for colour in range(1,4):
                identity_rows.append(("00000",sc,pos,colour,"00001",0,"constant_families30"))
    assert len(identity_rows) == len(set(identity_rows)) == len(original["records"]) == 313
    rows = []
    forward_observations = 0
    reverse_observations = 0
    for identity, preceding in zip(identity_rows,original["records"]):
        t,sc,pos,colour,nt,tc,origin = identity
        actual = list(word(t))
        actual[pos] = colour
        actual = tuple(actual)
        normalized,mapping = first(actual)
        assert normalized == nt
        assert [mapping[0],mapping[1],text(mapping[2])] == preceding["mapping"]
        assert all(preceding[k] == val for k,val in dict(source=t,source_component=sc,position=pos,colour=str(colour),target_type=nt,target_component=tc,actual_target=text(actual),origin=origin).items())
        source_k = K[t,sc]
        target_k = {edge(restore(a,mapping),restore(b,mapping)) for a,b in K[nt,tc]}
        source_pool = pools[t,sc]
        target_pool = {edge(restore(a,mapping),restore(b,mapping)) for a,b in pools[nt,tc]}
        forward = None
        reverse = None
        if nt not in HARD:
            target_states = {restore(w,mapping) for w in ordinary[nt,tc]}
            forward = analyze(source_k,target_states,actual,target_pool)
            assert forward["covered"] == (preceding["status"] == "covered")
            assert forward["candidate_vertices"] == preceding["candidate_vertices_checked"]
            for a,b in zip(forward["all_local_observations"],preceding["all_vertex_observations"]):
                assert (a["state"],a["HC_side_degree"],a["safe_incident_count"],a["protected_edge_lower_bound"],a["HC_side_neighbours"],a["safe_fixed_K_neighbours"]) == (b["state"],b["target_degree_d"],b["safe_incident_count_g"],b["protected_edge_lower_bound"],b["target_neighbours"],b["safe_source_K_neighbours"])
            forward_observations += forward["candidate_vertices"]
        else:
            assert preceding["status"] == "excluded-hard-target"
        if t not in HARD:
            reverse = analyze(target_k,set(ordinary[t,sc]),word(t),source_pool)
            reverse_observations += reverse["candidate_vertices"]
        if t == "00000":
            group = "constant-source-hard-target30"
        elif t in HARD and nt in HARD:
            group = "hard-hard5"
        elif t in HARD:
            group = "hard-source-HC-target26"
        elif nt in HARD:
            group = "HC-source-hard-target22"
        else:
            group = "ordinary-HH230"
        rows.append(dict(interface={k: preceding[k] for k in ("source","source_component","position","colour","actual_target","target_type","target_component","mapping","origin")},group=group,forward_fixed_source_K=forward,reverse_fixed_restored_target_K=reverse,covered=bool((forward and forward["covered"]) or (reverse and reverse["covered"]))))
    def summary(selected):
        return dict(total=len(selected),forward_eligible=sum(r["forward_fixed_source_K"] is not None for r in selected),reverse_eligible=sum(r["reverse_fixed_restored_target_K"] is not None for r in selected),forward_covered=sum(bool(r["forward_fixed_source_K"] and r["forward_fixed_source_K"]["covered"]) for r in selected),reverse_covered=sum(bool(r["reverse_fixed_restored_target_K"] and r["reverse_fixed_restored_target_K"]["covered"]) for r in selected),either_direction_covered=sum(r["covered"] for r in selected),both_directions_covered=sum(bool(r["forward_fixed_source_K"] and r["forward_fixed_source_K"]["covered"] and r["reverse_fixed_restored_target_K"] and r["reverse_fixed_restored_target_K"]["covered"]) for r in selected))
    groups = {g:summary([r for r in rows if r["group"] == g]) for g in sorted({r["group"] for r in rows})}
    assert {g:d["total"] for g,d in groups.items()} == {"HC-source-hard-target22":22,"constant-source-hard-target30":30,"hard-hard5":5,"hard-source-HC-target26":26,"ordinary-HH230":230}
    allsummary = summary(rows)
    assert allsummary["forward_eligible"] == 256 and allsummary["forward_covered"] == 200
    out = dict(status="PASS",python=platform.python_version(),source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),original_forward_result_sha256=hashlib.sha256(original_path.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),original_mapping_preserved_on_reverse=True,original_forward_full_scalar_readback_exact=True,summary=allsummary,groups=groups,forward_local_observations=forward_observations,reverse_local_observations=reverse_observations,covered_by_source=dict(sorted(Counter(r["interface"]["source"] for r in rows if r["covered"]).items())),certificate_types_by_direction={direction:dict(sorted(Counter(f"d{o['HC_side_degree']}/g{o['safe_incident_count']}" for r in rows if r[direction] for o in r[direction]["certificates"]).items())) for direction in ("forward_fixed_source_K","reverse_fixed_restored_target_K")},records=rows,elapsed_seconds=time.perf_counter()-begin,scope="Either original side can serve as the fixed protected-K side; only the opposite side requires a whole-component HC. Original normalization is retained on swapping. No full-state graph, HC search, or actual K/K edge-intersection enumeration.")
    (HERE / "symmetric-one-sided-results-v2.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","python","summary","groups","forward_local_observations","reverse_local_observations","covered_by_source","elapsed_seconds")},indent=2))


if __name__ == "__main__":
    run()
