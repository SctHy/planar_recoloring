#!/usr/bin/env python3
"""Graph-only incident inclusion-exclusion, separately retained from v1 readback."""
from collections import Counter
from itertools import permutations
from pathlib import Path
import hashlib
import json
import platform
import re
import time

HERE = Path(__file__).resolve().parent
HARD = {"00001", "00112"}
COL = frozenset(range(4))


def w(s):
    return tuple(map(int, s))


def s(x):
    return "".join(map(str, x))


def e(x, y):
    return tuple(sorted((x, y)))


def neigh(x, t):
    result = set()
    terms = []
    for i in range(5):
        excluded = {x[(i-1) % 5], x[(i+1) % 5]}
        if t[i] != 4:
            excluded.add(t[i])
        allowed = COL - excluded
        assert x[i] in allowed
        terms.append(len(allowed)-1)
        for c in allowed - {x[i]}:
            z = list(x)
            z[i] = c
            result.add(tuple(z))
    assert len(result) == sum(terms)
    return result, terms


def run():
    begin = time.perf_counter()
    text = (HERE / "phase6-source.tex").read_text()
    blocks = {}
    current = None
    for line in text.splitlines(keepends=True):
        if line.startswith("% BEGIN "):
            current = line[8:].strip()
            assert current not in blocks
            blocks[current] = ""
        elif line.startswith("% END "):
            assert line[6:].strip() == current
            current = None
        elif current is not None:
            blocks[current] += line
    assert len(blocks) == 53
    pools = {}
    for name in blocks:
        if name.startswith("POOL-"):
            _, t, c = name.split("-")
            pools[t, int(c)] = {e(w(a), w(b)) for a, b in re.findall(r"\b([0-3]{5})-([0-3]{5})\b", blocks[name])}
    types = {t for t, c in pools}
    cycles = {}
    for name in blocks:
        if name.startswith(("C1-", "FHC-")):
            cycles[name.split("-")[1], 0] = [w(x) for x in re.findall(r"\b[0-3]{5}\b", blocks[name])]
    constant = [w(x) for x in re.findall(r"\b[0-3]{5}\b", blocks["FACTOR-00000"])]
    cycles["00000", 0], cycles["00000", 1] = constant[:15], constant[15:]
    colmaps = list(permutations(range(4)))

    def first(t):
        for offset in range(5):
            for direction in (1, -1):
                for p in colmaps:
                    n = s(tuple(4 if t[(offset+direction*i) % 5] == 4 else p[t[(offset+direction*i) % 5]] for i in range(5)))
                    if n in types:
                        return n, (offset, direction, p)
        raise AssertionError(t)

    def restore(x, mapping):
        offset, direction, p = mapping
        inv = {p[i]: i for i in range(4)}
        z = [None] * 5
        for i in range(5):
            z[(offset+direction*i) % 5] = inv[x[i]]
        return tuple(z)

    author = json.loads((HERE / "author-results.json").read_text())
    preceding = json.loads((HERE / "review-results.json").read_text())
    assert preceding["status"] == "PASS" and preceding["all_313_records_exactly_equal"]
    assert preceding["author_result_sha256"] == hashlib.sha256((HERE / "author-results.json").read_bytes()).hexdigest()
    rows = []
    full_common_count = 0
    omitted_common_count = 0
    interfaces_with_omitted_common = 0
    inspected = 0
    for row in author["records"]:
        t, sc = row["source"], row["source_component"]
        nt, tc = row["target_type"], row["target_component"]
        if t in HARD or nt in HARD:
            continue
        actual = list(w(t))
        actual[row["position"]] = int(row["colour"])
        actual = tuple(actual)
        found, mapping = first(actual)
        assert found == nt
        assert [mapping[0], mapping[1], s(mapping[2])] == row["mapping"]
        target_states = {restore(x, mapping) for x in cycles[nt, tc]}
        source_states = set(cycles[t, sc])
        full_common = source_states & target_states
        full_common_count += len(full_common)
        # Candidate list was independently verified in preceding one-sided readback.
        candidates = {w(o["state"]) for o in row["all_vertex_observations"]}
        source_basis = {e(cycles[t, sc][i], cycles[t, sc][(i+1) % len(cycles[t, sc])]) for i in range(len(cycles[t, sc]))}
        K_endpoints = {x for pair in source_basis-pools[t, sc] for x in pair}
        assert candidates == K_endpoints & target_states
        assert candidates <= full_common
        omitted = full_common - candidates
        omitted_common_count += len(omitted)
        interfaces_with_omitted_common += bool(omitted)
        source_pool = pools[t, sc]
        target_pool = {e(restore(a, mapping), restore(b, mapping)) for a, b in pools[nt, tc]}
        union_pool = source_pool | target_pool
        observations = []
        for x in sorted(candidates):
            Ns, source_terms = neigh(x, w(t))
            Nt, target_terms = neigh(x, actual)
            assert Ns <= source_states and Nt <= target_states
            # One changed boundary entry changes just one degree summand by at most one.
            assert all(source_terms[i] == target_terms[i] for i in range(5) if i != row["position"])
            assert abs(source_terms[row["position"]]-target_terms[row["position"]]) <= 1
            common = Ns & Nt
            forbidden = {z for z in common if e(x, z) in union_pool}
            safe = common - forbidden
            ds, dt, dc, f = len(Ns), len(Nt), len(common), len(forbidden)
            h = dc-f
            source_retention = max(0, 2-ds+h)
            target_retention = max(0, 2-dt+h)
            bound = max(0, 4-ds-dt+h)
            assert bound == max(0, source_retention+target_retention-h)
            observations.append(dict(state=s(x), source_degree=ds, target_degree=dt, common_incident_count=dc, forbidden_common_count=f, safe_common_count=h, source_degree_terms=source_terms, target_degree_terms=target_terms, source_neighbours=sorted(map(s, Ns)), target_neighbours=sorted(map(s, Nt)), common_neighbours=sorted(map(s, common)), forbidden_common_neighbours=sorted(map(s, forbidden)), safe_common_neighbours=sorted(map(s, safe)), safe_source_retention=source_retention, safe_target_retention=target_retention, safe_common_edge_lower_bound=bound))
            inspected += 1
        positive = [o for o in observations if o["safe_common_edge_lower_bound"] > 0]
        rows.append(dict(interface={k: row[k] for k in ("source", "source_component", "position", "colour", "actual_target", "target_type", "target_component", "mapping")}, covered=bool(positive), positive_vertices=len(positive), omitted_printed_common_vertices=sorted(map(s, omitted)), certificates=positive, all_local_observations=observations))
    assert len(rows) == 230
    selected = [r for r in rows if r["covered"]]
    # The map field is a list, so use the first seven scalar interface fields as identity.
    def identity(r):
        a = r["interface"]
        return tuple(a[k] for k in ("source", "source_component", "position", "colour", "actual_target", "target_type", "target_component"))
    old_covered = {identity(r) for r in preceding["forced_source_records"] if r["covered"]}
    new_covered = {identity(r) for r in selected}
    assert old_covered <= new_covered
    summary = dict(ordinary_HH_interfaces=230, hard_source_or_target_excluded=83, covered_interfaces=len(selected), uncovered_interfaces=230-len(selected), covered_source_degree_two_previous=len(old_covered), additional_beyond_source_degree_two=len(new_covered-old_covered), common_vertices_inspected=inspected, full_common_vertices_from_printed_components=full_common_count, candidates_equal_full_common_at_all_interfaces=(omitted_common_count == 0), omitted_printed_common_vertices=omitted_common_count, interfaces_with_omitted_printed_common=interfaces_with_omitted_common, covered_by_source=dict(sorted(Counter(r["interface"]["source"] for r in selected).items())), certificate_degree_data=dict(sorted(Counter(f"ds{o['source_degree']}/dt{o['target_degree']}/dc{o['common_incident_count']}/f{o['forbidden_common_count']}" for r in selected for o in r["certificates"]).items())))
    result = dict(status="PASS", python=platform.python_version(), source_sha256=hashlib.sha256((HERE / "phase6-source.tex").read_bytes()).hexdigest(), preceding_readback_sha256=hashlib.sha256((HERE / "review-results.json").read_bytes()).hexdigest(), code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), rule="max(0,4-ds-dt+dc-f)", summary=summary, records=rows, elapsed_seconds=time.perf_counter()-begin, scope="Graph-only local neighbours and fixed pool union at existing candidate vertices. No HC search, full state enumeration or selected-cycle edge overlap used for the bound.")
    (HERE / "both-hc-local-results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "python", "rule", "summary", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    run()
