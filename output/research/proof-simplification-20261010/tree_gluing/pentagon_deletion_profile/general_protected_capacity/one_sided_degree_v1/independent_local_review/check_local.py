#!/usr/bin/env python3
"""Independent actual-source readback; no peer imports or graph construction."""
from collections import Counter
from itertools import permutations
from pathlib import Path
import hashlib
import json
import platform
import re
import sys
import time

HERE = Path(__file__).resolve().parent
COLOURS = frozenset(range(4))
HARD = {"00001", "00112"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def marked_blocks(text):
    result = {}
    name = None
    content = []
    for line in text.splitlines(keepends=True):
        if line.startswith("% BEGIN "):
            assert name is None
            name = line[len("% BEGIN "):].rstrip("\r\n")
            assert name not in result
            content = []
        elif line.startswith("% END "):
            assert line[len("% END "):].rstrip("\r\n") == name
            result[name] = "".join(content)
            name = None
        elif name is not None:
            content.append(line)
    assert name is None
    return result


def word(token):
    return tuple(int(ch) for ch in token)


def token(w):
    return "".join(map(str, w))


def undirected(a, b):
    return (a, b) if a < b else (b, a)


def printed_words(block):
    return [word(m) for m in re.findall(r"\b[0-3]{5}\b", block)]


def printed_edges(block):
    return {undirected(word(a), word(b)) for a, b in re.findall(r"\b([0-3]{5})-([0-3]{5})\b", block)}


def local(w, boundary):
    """Allowed lists L_i minus current colour; never enumerate legal words."""
    found = []
    terms = []
    for i in range(5):
        excluded = {w[(i + 4) % 5], w[(i + 1) % 5]}
        if boundary[i] != 4:
            excluded.add(boundary[i])
        allowed = COLOURS - excluded
        assert w[i] in allowed
        terms.append(len(allowed) - 1)
        for colour in sorted(allowed - {w[i]}):
            changed = list(w)
            changed[i] = colour
            found.append(tuple(changed))
    assert sum(terms) == len(found)
    return sorted(found), terms


def legal(w, t):
    return all(w[i] != w[(i + 1) % 5] and (t[i] == 4 or w[i] != t[i]) for i in range(5))


def normalization_text(text):
    return text.split("Here is the exact normalization convention.", 1)[1].split("\\begin{lemma}", 1)[0]


def run():
    start = time.perf_counter()
    source = HERE / "phase6-source.tex"
    baseline_path = HERE / "author-results.json"
    baseline = json.loads(baseline_path.read_text())
    frozen = source.read_text()
    B = marked_blocks(frozen)
    main_path = HERE.parents[7] / "planar_recoloring_hamilton_thresholds.tex"
    # Work from the actual workspace path, whose source identity is also reported.
    while not main_path.exists() and main_path.parent != main_path:
        main_path = main_path.parent.parent / "planar_recoloring_hamilton_thresholds.tex"
    if not main_path.exists():
        main_path = Path("/Users/huahua815/Downloads/planar_recoloring/planar_recoloring_hamilton_thresholds.tex")
    live = main_path.read_text()
    LB = marked_blocks(live)
    assert len(B) == 53 and all(LB[k] == v for k, v in B.items())
    assert normalization_text(frozen) == normalization_text(live)
    convention = normalization_text(frozen)
    assert "then $\\epsilon=+1,-1$" in convention and "lexicographic" in convention
    assert sha(source) == baseline["source_sha256"] == "7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3"

    pools = {}
    for name, content in B.items():
        if name.startswith("POOL-"):
            _, t, c = name.split("-")
            pools[t, int(c)] = printed_edges(content)
    types = {t for t, c in pools}
    assert len(types) == 22 and len(pools) == 23
    cycles = {}
    for name, content in B.items():
        if name.startswith("C1-") or name.startswith("FHC-"):
            cycles[name.split("-")[1], 0] = printed_words(content)
    constant = printed_words(B["FACTOR-00000"])
    assert len(constant) == 30
    cycles["00000", 0] = constant[:15]
    cycles["00000", 1] = constant[15:]
    K = {}
    for key, pool in pools.items():
        t, c = key
        if t in HARD:
            basis = printed_edges(B["COMMON-00001" if t == "00001" else "PORTS-00112"])
            assert len(basis) == 13 and len(pool) == 2
        else:
            states = cycles[key]
            assert len(states) == len(set(states))
            assert all(legal(w, word(t)) for w in states)
            basis = {undirected(states[i], states[(i + 1) % len(states)]) for i in range(len(states))}
        assert pool <= basis
        K[key] = basis - pool
        assert all(legal(a, word(t)) and legal(b, word(t)) and sum(x != y for x, y in zip(a, b)) == 1 for a, b in basis)

    colour_maps = list(permutations(range(4)))

    def first_normalizer(actual):
        for s in range(5):
            for eps in (1, -1):
                positions = [(s + eps * i) % 5 for i in range(5)]
                for p in colour_maps:
                    standard = tuple(4 if actual[j] == 4 else p[actual[j]] for j in positions)
                    if token(standard) in types:
                        return token(standard), (s, eps, p)
        raise AssertionError(actual)

    def inverse(w, mapping):
        s, eps, p = mapping
        inverse_colours = {p[j]: j for j in range(4)}
        restored = [None] * 5
        for i, colour in enumerate(w):
            restored[(s + eps * i) % 5] = inverse_colours[colour]
        return tuple(restored)

    assert all(first_normalizer(word(t)) == (t, (0, 1, (0, 1, 2, 3))) for t in types)
    rows = []
    pattern = r"\b([0-4]{5}):(\d)\s+([0-4])\s+([0-3])\s+([0-4]{5}):(\d)\s+([0-3]{5})-([0-3]{5})\b"
    parsed = re.findall(pattern, B["INTERFACES-ALL"])
    assert len(parsed) == 283
    for t, sc, pos, colour, nt, tc, a, b in parsed:
        rows.append((t, int(sc), int(pos), int(colour), nt, int(tc), "existing283"))
    assert "The thirty constant-source interfaces" in B["CONSTANT-INTERFACE-FAMILIES"]
    for sc in range(2):
        for pos in range(5):
            for colour in range(1, 4):
                rows.append(("00000", sc, pos, colour, "00001", 0, "constant_families30"))
    assert len(rows) == len(set(rows)) == len(baseline["records"]) == 313
    recomputed = []
    forced_rows = []
    scalar_count = 0
    source_formula_vertices = 0
    for row, expected in zip(rows, baseline["records"]):
        t, sc, pos, colour, nt, tc, origin = row
        actual = list(word(t))
        assert actual[pos] != 4 and actual[pos] != colour
        actual[pos] = colour
        actual = tuple(actual)
        normal, mapping = first_normalizer(actual)
        assert normal == nt
        s, eps, p = mapping
        got = dict(source=t, source_component=sc, position=pos, colour=str(colour), actual_target=token(actual), target_type=nt, target_component=tc, mapping=[s, eps, token(p)], origin=origin)
        if nt in HARD:
            got.update(status="excluded-hard-target", reason="No whole-graph target Hamilton cycle premise; no seed-row claim examined.")
            assert got == expected
            recomputed.append(got)
            continue
        target_words = {inverse(w, mapping) for w in cycles[nt, tc]}
        target_pool = {undirected(inverse(a, mapping), inverse(b, mapping)) for a, b in pools[nt, tc]}
        incident = {}
        for a, b in K[t, sc]:
            incident.setdefault(a, set()).add(b)
            incident.setdefault(b, set()).add(a)
        candidates = sorted(target_words.intersection(incident))
        observations = []
        certs = []
        source_local = {}
        if t not in HARD:
            for w in candidates:
                source_local[w] = local(w, word(t))
                assert set(source_local[w][0]) <= set(cycles[t, sc])
                source_formula_vertices += 1
        forced_observations = []
        for w in candidates:
            neighbours, degree_terms = local(w, actual)
            assert set(neighbours) <= target_words
            safe = [z for z in neighbours if z in incident[w] and undirected(w, z) not in target_pool]
            d, g = len(neighbours), len(safe)
            assert d >= 2 and g <= 2
            lower = max(0, 2 + g - d)
            obs = dict(state=token(w), target_neighbours=list(map(token, neighbours)), safe_source_K_neighbours=list(map(token, safe)), target_degree_d=d, safe_incident_count_g=g, protected_edge_lower_bound=lower)
            observations.append(obs)
            scalar_count += 1
            if lower:
                certs.append(obs)
            if t not in HARD:
                ds = len(source_local[w][0])
                forced_safe = [z for z in safe if ds == 2 or len(source_local[z][0]) == 2]
                f = len(forced_safe)
                forced_lower = max(0, 2 + f - d)
                centre_lower = lower if ds == 2 else 0
                if forced_lower:
                    forced_observations.append(dict(state=token(w), source_degree=ds, source_degree_terms=source_local[w][1], target_degree=d, target_degree_terms=degree_terms, forced_safe_neighbours=list(map(token, forced_safe)), source_degrees_of_forced_neighbours=[len(source_local[z][0]) for z in forced_safe], forced_edge_lower_bound=forced_lower, centre_degree_two_lower_bound=centre_lower))
        got.update(status="covered" if certs else "not-covered", candidate_vertices_checked=len(candidates), certificates=certs, all_vertex_observations=observations, degree2_subcriterion_covered=any(z["target_degree_d"] == 2 for z in certs), degree3_pair_covered=any(z["target_degree_d"] == 3 and z["safe_incident_count_g"] == 2 for z in certs))
        got["new_beyond_degree2"] = got["degree3_pair_covered"] and not got["degree2_subcriterion_covered"]
        assert got == expected, (row, "scalar or local observation mismatch")
        recomputed.append(got)
        if t not in HARD:
            forced_rows.append(dict(interface={k: got[k] for k in ("source", "source_component", "position", "colour", "actual_target", "target_type", "target_component", "mapping")}, covered=bool(forced_observations), centre_degree_two_covered=any(o["centre_degree_two_lower_bound"] for o in forced_observations), target_degree_two_covered=any(o["target_degree"] == 2 for o in forced_observations), target_degree_three_pair_covered=any(o["target_degree"] == 3 for o in forced_observations), certificates=forced_observations))

    eligible = [r for r in recomputed if r["status"] != "excluded-hard-target"]
    covered = [r for r in eligible if r["status"] == "covered"]
    new = [r for r in covered if r["new_beyond_degree2"]]
    old_summary = dict(all_interfaces=313, excluded_hard_targets=313-len(eligible), eligible_HC_targets=len(eligible), covered_interfaces=len(covered), uncovered_eligible=len(eligible)-len(covered), degree2_subcriterion_covered=sum(r["degree2_subcriterion_covered"] for r in eligible), degree3_pair_covered=sum(r["degree3_pair_covered"] for r in eligible), new_beyond_degree2=len(new), covered_source_kind=dict(Counter("hard" if r["source"] in HARD else "Hamilton" for r in covered)), new_source_kind=dict(Counter("hard" if r["source"] in HARD else "Hamilton" for r in new)), covered_by_source=dict(sorted(Counter(r["source"] for r in covered).items())), new_by_source=dict(sorted(Counter(r["source"] for r in new).items())), certificate_degree_pairs=dict(Counter(f"d{c['target_degree_d']}/g{c['safe_incident_count_g']}" for r in covered for c in r["certificates"])), local_mutation_alternatives_counted=15*scalar_count)
    assert old_summary == baseline["summary"]
    selected = [r for r in forced_rows if r["covered"]]
    centre = [r for r in forced_rows if r["centre_degree_two_covered"]]
    forced_summary = dict(ordinary_source_and_target_interfaces=len(forced_rows), excluded_hard_source_eligible=len(eligible)-len(forced_rows), endpoint_forced_covered=len(selected), centre_degree_two_covered=len(centre), endpoint_only_additional=len(selected)-len(centre), target_degree_two_covered=sum(r["target_degree_two_covered"] for r in selected), target_degree_three_pair_covered=sum(r["target_degree_three_pair_covered"] for r in selected), source_formula_vertices=source_formula_vertices, covered_by_source=dict(sorted(Counter(r["interface"]["source"] for r in selected).items())), centre_by_source=dict(sorted(Counter(r["interface"]["source"] for r in centre).items())), certificate_degree_pairs=dict(Counter(f"s{o['source_degree']}/t{o['target_degree']}/f{len(o['forced_safe_neighbours'])}" for r in selected for o in r["certificates"])))
    result = dict(status="PASS", python=platform.python_version(), executable=sys.executable, source_sha256=sha(source), author_result_sha256=sha(baseline_path), checker_sha256=sha(Path(__file__)), all_53_marked_blocks_byte_equal=True, normalizer_byte_equal=True, observed_live_main_sha256=sha(main_path), all_313_records_exactly_equal=True, local_observation_scalar_vectors_compared=scalar_count, degree2_degree3_overlap=old_summary["degree2_subcriterion_covered"]+old_summary["degree3_pair_covered"]-old_summary["covered_interfaces"], original_summary=old_summary, forced_source_summary=forced_summary, forced_source_records=forced_rows, elapsed_seconds=time.perf_counter()-start, boundaries=["No whole-graph state enumeration or Hamilton search.", "Hard sources are excluded only from the any-source-Hamilton-cycle extension.", "Finite selected-interface coverage is not a uniform interface-family theorem.", "All original result bytes and author code are preserved; no manuscript edit."])
    (HERE / "review-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "python", "all_313_records_exactly_equal", "local_observation_scalar_vectors_compared", "degree2_degree3_overlap", "original_summary", "forced_source_summary", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    run()
