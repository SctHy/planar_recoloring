#!/usr/bin/env python3
"""Local-only check of the 51 omitted printed common vertices; no rerun of v2."""
from pathlib import Path
import hashlib
import json
import platform
import re

HERE = Path(__file__).resolve().parent


def w(x):
    return tuple(map(int, x))


def s(x):
    return "".join(map(str, x))


def edge(a, b):
    return tuple(sorted((a, b)))


def local(x, t):
    out = set()
    for i in range(5):
        excluded = {x[(i-1) % 5], x[(i+1) % 5]}
        if t[i] != 4:
            excluded.add(t[i])
        for c in set(range(4))-excluded-{x[i]}:
            z = list(x)
            z[i] = c
            out.add(tuple(z))
    return out


def run():
    raw = (HERE / "both-hc-local-results.json").read_bytes()
    input_result = json.loads(raw)
    text = (HERE / "phase6-source.tex").read_text()
    blocks = {m[1]: m[2] for m in re.finditer(r"^% BEGIN ([^\n]+)\n(.*?)^% END \1$", text, re.M | re.S)}
    pools = {}
    for key, b in blocks.items():
        if key.startswith("POOL-"):
            _, t, c = key.split("-")
            pools[t, int(c)] = {edge(w(a), w(z)) for a, z in re.findall(r"\b([0-3]{5})-([0-3]{5})\b", b)}
    cycles = {}
    for key, b in blocks.items():
        if key.startswith(("C1-", "FHC-")):
            cycles[key.split("-")[1], 0] = [w(a) for a in re.findall(r"\b[0-3]{5}\b", b)]
    constant = [w(a) for a in re.findall(r"\b[0-3]{5}\b", blocks["FACTOR-00000"])]
    cycles["00000", 0], cycles["00000", 1] = constant[:15], constant[15:]
    checks = []
    for row in input_result["records"]:
        a = row["interface"]
        t, sc, nt, tc = a["source"], a["source_component"], a["target_type"], a["target_component"]
        shift, direction, perm = a["mapping"]
        inv = {int(perm[i]): i for i in range(4)}

        def restored(x):
            z = [None] * 5
            for i in range(5):
                z[(shift+direction*i) % 5] = inv[x[i]]
            return tuple(z)

        target_pool = {edge(restored(x), restored(z)) for x, z in pools[nt, tc]}
        union_pool = target_pool | pools[t, sc]
        cyc = cycles[t, sc]
        source_basis = {edge(cyc[i], cyc[(i+1) % len(cyc)]) for i in range(len(cyc))}
        for raw_x in row["omitted_printed_common_vertices"]:
            x = w(raw_x)
            incident_basis = {e for e in source_basis if x in e}
            assert len(incident_basis) == 2 and incident_basis <= pools[t, sc]
            Ns, Nt = local(x, w(t)), local(x, w(a["actual_target"]))
            assert {z for e in incident_basis for z in e if z != x} <= Ns
            common = Ns & Nt
            f = sum(edge(x, z) in union_pool for z in common)
            ds, dt, dc = len(Ns), len(Nt), len(common)
            assert dt >= 2 and ds-dc+f >= 2
            raw_bound = 4-ds-dt+dc-f
            assert raw_bound <= 0
            checks.append(dict(interface={k: a[k] for k in ("source", "source_component", "position", "colour", "actual_target", "target_type", "target_component")}, state=raw_x, source_degree=ds, target_degree=dt, common_count=dc, forbidden_common_count=f, source_nonsafe_count=ds-dc+f, raw_local_lower_bound=raw_bound, source_cycle_incident_pool_edges=[sorted(map(s, e)) for e in sorted(incident_basis)]))
    assert len(checks) == input_result["summary"]["omitted_printed_common_vertices"] == 51
    result = dict(status="PASS", python=platform.python_version(), primary_result_sha256=hashlib.sha256(raw).hexdigest(), code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), omitted_vertices_checked=len(checks), positive_omitted_vertices=0, all_omitted_source_nonsafe_count_at_least_two=True, primary_coverage=125, all_printed_common_scope_coverage=125, observations=checks, scope="Only the 51 previously omitted printed common vertices; local neighbour formula and prescribed pools, no state enumeration or Hamilton search.")
    (HERE / "omitted-vertices-results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "python", "omitted_vertices_checked", "positive_omitted_vertices", "primary_coverage", "all_printed_common_scope_coverage")}, indent=2))


if __name__ == "__main__":
    run()
