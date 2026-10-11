#!/usr/bin/env python3
"""Complete exact replay of the protected-pentagon certificates."""
from functools import lru_cache
from itertools import permutations, product
import re
import sys

from certificate_core import (adjacent, check_path, cycle_edges, edge, marked,
                              need_block, path_edges, read_edges, require, run_cli, words)

Q = "0123"
PERMS = tuple(permutations(Q))
ORDINARY = ("00000", "00001", "00011", "00012", "00101", "00102",
            "00112", "00121", "00123", "01012", "01023")
STARRED = ("00004", "00014", "00104", "00114", "00124", "01014",
           "01024", "01104", "01124", "01204", "01234")
TYPES = set(ORDINARY + STARRED)
HARD = {"00001", "00112"}


def legal(x, t):
    return (all(x[i] != x[(i + 1) % 5] for i in range(5)) and
            all(t[i] == "4" or x[i] != t[i] for i in range(5)))


@lru_cache(None)
def states(t):
    return frozenset("".join(x) for x in product(Q, repeat=5) if legal(x, t))


def neighbours(x, t):
    result = set()
    for i in range(5):
        for q in Q:
            y = x[:i] + q + x[i + 1:]
            if y != x and legal(y, t):
                result.add(y)
    return result


def transform(x, mapping):
    start, sign, image = mapping
    p = dict(zip(Q, image))
    return "".join("4" if x[(start + sign * i) % 5] == "4" else
                   p[x[(start + sign * i) % 5]] for i in range(5))


def restore(x, mapping):
    start, sign, image = mapping
    inv = dict(zip(image, Q))
    out = [""] * 5
    for i in range(5):
        out[(start + sign * i) % 5] = "4" if x[i] == "4" else inv[x[i]]
    return "".join(out)


@lru_cache(None)
def first_normalizer(t):
    for start in range(5):
        for sign in (1, -1):
            for image in PERMS:
                mapping = start, sign, image
                target = transform(t, mapping)
                if target in TYPES:
                    return target, mapping
    raise ValueError(f"unclassified boundary: {t}")


def restored_edges(edges, mapping):
    return {edge(restore(a, mapping), restore(b, mapping)) for a, b in edges}


def connected(vertices, edges):
    require(vertices, "empty component")
    adj = {x: set() for x in vertices}
    for a, b in edges:
        require(a in adj and b in adj, "edge leaves the component")
        adj[a].add(b)
        adj[b].add(a)
    reached = {next(iter(vertices))}
    stack = list(reached)
    while stack:
        for y in adj[stack.pop()] - reached:
            reached.add(y)
            stack.append(y)
    return reached == set(vertices), adj


def check_seed(vertices, edges, rows, context):
    expected = {str(r) + x for r in range(rows) for x in vertices}
    conn, adj = connected(expected, edges)
    require(conn and len(edges) == len(expected) and all(len(n) == 2 for n in adj.values()),
            f"{context}: seed is not one spanning cycle")
    for a, b in edges:
        require((a[0] == b[0] and adjacent(a[1:], b[1:])) or
                (a[1:] == b[1:] and abs(int(a[0]) - int(b[0])) == 1),
                f"{context}: edge is not in the path product")


def hard_seeds(blocks, t, v, ports, capture=None):
    seed_key = "PC2-00001" if t == "00001" else "C2-00112"
    cycle = words(need_block(blocks, seed_key), 6)
    e2 = check_path(cycle, {"0" + x for x in v} | {"1" + x for x in v},
                    seed_key, cyclic=True)
    check_seed(v, e2, 2, seed_key)
    core = words(need_block(blocks, "COREPATH-" + t), 5)
    if t == "00001":
        short = [["12312", "12313"], ["13212", "13213"]]
        ends = ["13210", "13230"]
        expected_core = 40
    else:
        short = [["12303", "12323"], ["13203", "23203"]]
        ends = ["21201", "23201"]
        expected_core = 47
    require(len(core) == expected_core and [core[0], core[-1]] == ends,
            f"{t}: wrong three-row core path")
    new_paths = short + [core]
    covered = [x for path in new_paths for x in path]
    require(len(covered) == len(set(covered)) and set(covered) == v,
            f"{t}: insertion paths do not partition the new row")
    for path in new_paths:
        require(all(adjacent(a, b) for a, b in zip(path, path[1:])),
                f"{t}: insertion path contains an illegal edge")
    cuts = {edge(path[0], path[-1]) for path in new_paths}
    require(ports.isdisjoint(cuts) and ports <= path_edges(core),
            f"{t}: insertion cuts or paths lose a common port")
    e3 = set(e2)
    for path in new_paths:
        cut = edge("1" + path[0], "1" + path[-1])
        require(cut in e3, f"{t}: insertion cut missing from row 1")
        e3.remove(cut)
        e3 |= {edge("2" + a, "2" + b) for a, b in zip(path, path[1:])}
        e3 |= {edge("1" + x, "2" + x) for x in (path[0], path[-1])}
    check_seed(v, e3, 3, t + " derived three-row seed")
    for rows, edges in ((2, e2), (3, e3)):
        for row in range(rows):
            require({edge(str(row) + a, str(row) + b) for a, b in ports} <= edges,
                    f"{t}: port not retained in every seed row")
    if capture is not None:
        # Keep the literal seed edges available to the product-level replay.
        # They are not included in the JSON report; the report retains only
        # the finite counts below.
        capture[t] = {2: e2, 3: e3}
    return {"two_row_states": 2 * len(v), "three_row_states": 3 * len(v),
            "common_ports_per_row": len(ports), "core_path_states": len(core)}


def components_from_source(blocks):
    result = {}
    seed_reports = {}
    hard_seed_edges = {}
    for t in ORDINARY + STARRED:
        for c in range(2 if t == "00000" else 1):
            key = f"{t}:{c}"
            component_blocks = None
            if t == "00000":
                all_words = words(need_block(blocks, "FACTOR-00000"), 5)
                require(len(all_words) == len(set(all_words)) == 30, "bad constant factor")
                path = all_words[15*c:15*(c+1)]
            elif t == "00001":
                body = need_block(blocks, "MATCHING-CHAIN-00001")
                rows = sorted((int(i), a, b, e) for i, a, b, e in re.findall(
                    r"(\d+)\s*&\s*([0-3]{5})\s*&\s*([0-3]{5})\s*&\s*(--|[01])", body))
                require([i for i, _, _, _ in rows] == list(range(1, 23)), "missing matching-chain row")
                require(all(e in ("0", "1") for _, _, _, e in rows[:-1]) and rows[-1][3] == "--",
                        "bad matching-chain connector index")
                require(all(adjacent(a, b) for _, a, b, _ in rows), "bad matching-chain pair")
                for (_, a, b, e), (_, next_a, _, _) in zip(rows, rows[1:]):
                    require(adjacent(a if e == "0" else b, next_a), "bad matching-chain connector")
                path = [x for _, a, b, _ in rows for x in (a, b)]
                component_blocks = [(a, b) for _, a, b, _ in rows]
            else:
                name = "HP-" + t if t in HARD else ("FHC-" if "4" in t else "C1-") + t
                path = words(need_block(blocks, name), 5)
            v = set(path)
            require(len(v) == len(path) and v <= states(t), f"{key}: repeated or illegal states")
            if t != "00000":
                require(v == states(t), f"{key}: words miss a legal state")
            all_edges = {edge(x, y) for x in v for y in neighbours(x, t)}
            conn, _ = connected(v, all_edges)
            require(conn and all(neighbours(x, t) <= v for x in v), f"{key}: not a complete component")
            pool = read_edges(need_block(blocks, f"POOL-{t}-{c}"), key,
                              2 if t in HARD else 5 if t == "00000" else 8)
            if t in HARD:
                if t == "00112":
                    check_path(path, v, "HP-00112")
                ports = read_edges(need_block(blocks, "COMMON-00001" if t == "00001" else "PORTS-00112"),
                                   key + " ports", 13)
                require(pool <= ports <= all_edges, f"{key}: pool or port not in component")
                seed_reports[t] = hard_seeds(blocks, t, v, ports, hard_seed_edges)
                basis = ports
            else:
                basis = check_path(path, v, key, cyclic=True)
                require(pool <= basis and len(pool) - 2 >= 2, f"{key}: missing reserve edges")
            if component_blocks is None:
                lengths = [2] * (len(path) // 2)
                if len(path) % 2:
                    lengths = [3] + [2] * ((len(path) - 3) // 2)
                component_blocks = []
                offset = 0
                for length in lengths:
                    component_blocks.append(tuple(path[offset:offset + length]))
                    offset += length
            result[key] = {"vertices": v, "order": tuple(path),
                           "blocks": tuple(tuple(x) for x in component_blocks),
                           "cycle": basis if t not in HARD else set(),
                           "pool": pool, "protected": basis - pool, "has_cycle": t not in HARD}
    require(len(result) == 23, "wrong component catalog size")
    require(result["00000:0"]["vertices"].isdisjoint(result["00000:1"]["vertices"]) and
            result["00000:0"]["vertices"] | result["00000:1"]["vertices"] == states("00000"),
            "constant components fail to partition legal states")
    return result, seed_reports, hard_seed_edges


def selectors_from_source(text):
    heading = r"\paragraph{Fixed-side source selectors (236 interfaces).}"
    require(text.count(heading) == 1, "missing or duplicated source-selector table")
    section = text.split(heading, 1)[1].split(r"\end{array}", 1)[0]
    rows = re.findall(r"([0-4]{5})&(.*?)(?=\\\\|$)", section, re.S)
    require(len(rows) == 21 and len({t for t, _ in rows}) == 21, "missing selector row")
    result = {t: words(row, 5) for t, row in rows}
    require(set(result) == TYPES - {"00000"} and sum(map(len, result.values())) == 78 and
            len({x for row in result.values() for x in row}) == 47, "wrong selector coverage")
    for t, row in result.items():
        require(len(row) == len(set(row)) and set(row) <= states(t), f"{t}: bad selector")
    return result


def constant_families(blocks, components):
    body = need_block(blocks, "CONSTANT-INTERFACE-FAMILIES")
    aliases = dict((name, edge(a, b)) for name, a, b in re.findall(
        r"([abcd])=([0-3]{5})\\!-([0-3]{5})", body))
    rows = re.findall(r"([01])&([123])&([0-3]{5})\\!-([0-3]{5})&([abcd])&([abcd])", body)
    require(len(aliases) == 4 and len(rows) == 6 and
            {(i, q) for i, q, *_ in rows} == set(product("01", "123")),
            "missing constant-source family")
    kh = components["00001:0"]["protected"]
    require(set(aliases.values()) <= kh, "constant-family image is not protected")
    witnesses = {}
    for i, q, a, b, positive, negative in rows:
        source = "00000:" + i
        e = edge(a, b)
        k = components[source]["protected"]
        require(e in k, "constant-family edge is not source-protected")
        for r in range(5):
            rotated = {edge(x[r:] + x[:r], y[r:] + y[:r]) for x, y in k}
            require(rotated == k, "constant protected set is not rotation invariant")
        p = next(image for image in PERMS if image[0] == "0" and image[int(q)] == "1")
        for sign, alias in ((1, positive), (-1, negative)):
            mapping = ((-4 * sign) % 5, sign, p)
            require(edge(transform(a, mapping), transform(b, mapping)) == aliases[alias],
                    "constant-family normalized image differs from printed table")
        for j in range(5):
            r = (-j) % 5
            actual = edge(a[r:] + a[:r], b[r:] + b[:r])
            target_boundary = "0" * j + q + "0" * (4 - j)
            target, mapping = first_normalizer(target_boundary)
            require(target == "00001" and actual in k and
                    actual in restored_edges(kh, mapping), "constant-family physical edge fails")
            witnesses[(source, j, q, "00001:0")] = actual
    require(len(witnesses) == 30, "incomplete constant families")
    return witnesses


def product_edge(a, b):
    """An unordered edge whose vertices are pairs of pentagon states."""
    return tuple(sorted((a, b)))


def product_blocks(data):
    """Return ordered 2/3-vertex blocks from a certificate word order.

    The source words are ordered paths (a cycle with its closing edge
    omitted for ordinary components); the matching-chain certificate for
    00001 supplies its blocks explicitly.  Odd orders use one initial
    3-block and then 2-blocks.  Every boundary between consecutive blocks
    is checked for an actual one-coordinate edge below.
    """
    result = [tuple(block) for block in data["blocks"]]
    require(result, "empty component order")
    require({x for block in result for x in block} == data["vertices"],
            "product blocks do not cover component")
    connectors = []
    for left, right in zip(result, result[1:]):
        choices = [(x, y) for x in left for y in right if adjacent(x, y)]
        require(choices, "product block connector is not an edge")
        connectors.append(choices[0])
    return result, connectors


def product_cycle_for_block(data, block, hard_edges=None):
    """Build and replay the literal A square P_m seed for m=2 or 3."""
    m = len(block)
    require(m in (2, 3), "product block has the wrong length")
    vertices = {(a, b) for a in data["vertices"] for b in block}
    if data["has_cycle"]:
        order = list(data["order"])
        base = set()
        for b in block:
            for i, a in enumerate(order):
                base.add(product_edge((a, b),
                                       (order[(i + 1) % len(order)], b)))
        pool = sorted(data["pool"])
        require(len(pool) >= m - 1, "component pool is too small for this block")
        for row, e in ((0, pool[0]), (1, pool[0])):
            base.remove(product_edge((e[0], block[row]), (e[1], block[row])))
        base.update((product_edge((pool[0][0], block[0]),
                                  (pool[0][0], block[1])),
                     product_edge((pool[0][1], block[0]),
                                  (pool[0][1], block[1]))))
        if m == 3:
            e = pool[1]
            base.remove(product_edge((e[0], block[1]), (e[1], block[1])))
            base.remove(product_edge((e[0], block[2]), (e[1], block[2])))
            base.update((product_edge((e[0], block[1]), (e[0], block[2])),
                        product_edge((e[1], block[1]), (e[1], block[2]))))
        return vertices, base

    require(hard_edges is not None, "missing hard product seed")
    seed = hard_edges[m]

    def lift(word):
        row, state = int(word[0]), word[1:]
        require(row < m and state in data["vertices"],
                "hard seed leaves its component")
        return (state, block[row])

    base = {product_edge(lift(a), lift(b)) for a, b in seed}
    return vertices, base


def check_product_cycle(vertices, edges, context):
    require(len(edges) == len(vertices), f"{context}: wrong cycle edge count")
    adj = {x: set() for x in vertices}
    for a, b in edges:
        require(a in adj and b in adj and a != b,
                f"{context}: edge leaves product")
        adj[a].add(b)
        adj[b].add(a)
    require(all(len(n) == 2 for n in adj.values()),
            f"{context}: product is not 2-regular")
    reached = {next(iter(vertices))}
    stack = list(reached)
    while stack:
        x = stack.pop()
        for y in adj[x] - reached:
            reached.add(y)
            stack.append(y)
    require(reached == vertices, f"{context}: product is disconnected")


def product_level_replay(components, hard_seed_edges):
    """Replay all 23^2 products and the block-chain splicing invariant.

    This is deliberately a finite check of the construction scheme, not a
    search over arbitrary bottom cycles.  It verifies every component pair,
    both hard seeds, all 2/3-row blocks, protected-edge retention, and the
    alternating reserve rule used when block cycles are joined.
    """
    products = 0
    spliced = 0
    for a_key, a in sorted(components.items()):
        a_type = a_key[:5]
        for b_key, b in sorted(components.items()):
            blocks, connectors = product_blocks(b)
            block_cycles = []
            pool = sorted(a["pool"])
            reserves = pool[2:] if a["has_cycle"] else pool
            require(len(reserves) >= 2,
                    f"{a_key}: fewer than two unused pool reserves")
            for block in blocks:
                if a["has_cycle"]:
                    vertices, cycle = product_cycle_for_block(a, block)
                else:
                    vertices, cycle = product_cycle_for_block(
                        a, block, hard_seed_edges[a_type])
                context = f"{a_key} square {b_key} block {len(block)}"
                check_product_cycle(vertices, cycle, context)
                for b_state in block:
                    for x, y in a["protected"]:
                        require(product_edge((x, b_state), (y, b_state)) in cycle,
                                f"{context}: protected edge cut")
                block_cycles.append((block, cycle))
            all_vertices = {(x, y) for x in a["vertices"]
                            for y in b["vertices"]}
            all_edges = set().union(*(cycle for _, cycle in block_cycles))
            # Alternating reserves ensure that an internal block never loses
            # the same protected edge at both of its two interfaces.
            for i, ((left_block, _), (right_block, _)) in enumerate(
                    zip(block_cycles, block_cycles[1:])):
                reserve = reserves[i % 2]
                left_state, right_state = connectors[i]
                left_row = left_block.index(left_state)
                right_row = right_block.index(right_state)
                left_edge = product_edge((reserve[0], left_block[left_row]),
                                         (reserve[1], left_block[left_row]))
                right_edge = product_edge((reserve[0], right_block[right_row]),
                                          (reserve[1], right_block[right_row]))
                require(left_edge in all_edges and right_edge in all_edges,
                        f"{a_key} square {b_key}: reserve unavailable at interface {i}")
                all_edges.remove(left_edge)
                all_edges.remove(right_edge)
                all_edges.add(product_edge((reserve[0], left_block[left_row]),
                                            (reserve[0], right_block[right_row])))
                all_edges.add(product_edge((reserve[1], left_block[left_row]),
                                            (reserve[1], right_block[right_row])))
                # The inserted edges are precisely synchronous bottom
                # recolourings; consecutive block endpoints differ in one B
                # coordinate and the A state is held fixed.
                require(adjacent(left_state, right_state),
                        f"{a_key} square {b_key}: illegal block splice")
            check_product_cycle(all_vertices, all_edges,
                                f"{a_key} square {b_key} after block splicing")
            for b_state in b["vertices"]:
                for x, y in a["protected"]:
                    require(product_edge((x, b_state), (y, b_state)) in all_edges,
                            f"{a_key} square {b_key}: protected edge lost in splice")
            products += 1
            spliced += len(block_cycles)
    return {"product_pairs": products, "product_block_cycles": spliced,
            "product_scope": "23 by 23 component pairs; finite replay of local product and reserve splice"}


def check_pentagons(text):
    blocks = marked(text)
    components, seeds, hard_seed_edges = components_from_source(blocks)
    selectors = selectors_from_source(text)
    const = constant_families(blocks, components)
    pattern = r"([0-4]{5}:[01]) ([0-4]) ([0-3]) ([0-4]{5}:[01]) ([0-3]{5})-([0-3]{5})"
    raw = re.findall(pattern, need_block(blocks, "INTERFACES-ALL"))
    records = {(s, int(j), q, t): edge(a, b) for s, j, q, t, a, b in raw}
    require(len(records) == len(raw) == 47, "missing or duplicate individual interface")
    for t in TYPES:
        require(first_normalizer(t) == (t, (0, 1, tuple(Q))), f"{t}: nonidentity standard map")
    labelled = ["".join(t) for t in product(Q, repeat=5)]
    for j in range(5):
        for t in product(Q, repeat=4):
            labelled.append("".join(t[:j]) + "4" + "".join(t[j:]))
    require(len(set(labelled)) == len(labelled) == 2304, "bad labelled boundary enumeration")
    for t in labelled:
        target, mapping = first_normalizer(t)
        require(transform(t, mapping) == target, "normalizer fails on boundary")
        restored = {restore(x, mapping) for x in states(target)}
        require(restored == states(t), f"{t}: restoration is not a legal-state bijection")
    checked = set()
    case_rows = []
    family_count = 0
    minimum_overlap = 1024
    for source, data in sorted(components.items()):
        t = source[:5]
        for j in range(5):
            if t[j] == "4":
                continue
            for q in Q:
                if q == t[j]:
                    continue
                boundary = t[:j] + q + t[j + 1:]
                target, mapping = first_normalizer(boundary)
                for c in range(2 if target == "00000" else 1):
                    target_key = f"{target}:{c}"
                    other = components[target_key]
                    v = {restore(x, mapping) for x in other["vertices"]}
                    common = data["vertices"] & v
                    if not common:
                        continue
                    key = source, j, q, target_key
                    checked.add(key)
                    minimum_overlap = min(minimum_overlap, len(common))
                    require(len(common) >= 10, f"{key}: fewer than ten common states")
                    pk = restored_edges(other["protected"], mapping)
                    pp = restored_edges(other["pool"], mapping)
                    shared = data["protected"] & pk
                    require(shared, f"{key}: protected sets have no common edge")
                    if key in records:
                        require(records[key] in shared, f"{key}: printed edge is not jointly protected")
                        method, witness = "individual", records[key]
                    elif key in const:
                        require(const[key] in shared, f"{key}: constant family is not jointly protected")
                        method, witness = "constant family", const[key]
                    else:
                        require(t != "00000", f"{key}: constant interface omitted")
                        candidates = []
                        for x in selectors[t]:
                            if x not in common:
                                continue
                            for direction, eligible, ns, fixed, pool in (
                                ("forward", other["has_cycle"], neighbours(x, boundary), data["protected"], pp),
                                ("reverse", data["has_cycle"], neighbours(x, t), pk, data["pool"])):
                                if not eligible:
                                    continue
                                star = {edge(x, y) for y in ns}
                                good = (star & fixed) - pool
                                if len(star) >= 2 and len(star - good) <= 1:
                                    candidates.append((x, direction, len(star), len(good)))
                        require(candidates, f"{key}: selector has no valid fixed-side degree witness")
                        method, witness = "selector", candidates[0]
                        family_count += 1
                    case_rows.append({"source": source, "position": j, "new_colour": q,
                                      "target": target_key, "method": method, "witness": witness,
                                      "common_states": len(common), "common_protected_edges": len(shared)})
    require(set(records) <= checked and set(const) <= checked and set(records).isdisjoint(const),
            "spurious or overlapping interface records")
    require(len(checked) == len(case_rows) == 313 and family_count == 236 and
            len(checked) == len(records) + len(const) + family_count, "incomplete interface partition")
    product_report = product_level_replay(components, hard_seed_edges)
    return {"component_types": len(components), "labelled_boundaries": len(labelled),
            "ordinary_representative_states": sum(len(states(t)) for t in ORDINARY),
            "starred_representative_states": sum(len(states(t)) for t in STARRED),
            "hard_seeds": seeds, "standard_source_interfaces": len(checked),
            "individual_records": len(records), "selector_cases": family_count,
            "constant_family_cases": len(const), "minimum_common_states": minimum_overlap,
            "components": {key: {"states": len(v["vertices"]), "pool_edges": len(v["pool"]),
                                  "protected_edges": len(v["protected"])}
                           for key, v in sorted(components.items())},
            "interfaces": case_rows,
            **product_report,
            "scope": "all literal local certificates and 23x23 product/reserve replay; arbitrary-order component-graph and tree splicing remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_pentagons, __doc__))
