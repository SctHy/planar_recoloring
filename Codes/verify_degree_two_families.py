#!/usr/bin/env python3
"""Check the seven degree-two restoration families and complete port aliases."""
from __future__ import annotations

import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

from certificate_core import (CertificateError, check_path, edge, marked,
                              need_block, require, run_cli)

Q = range(4)
DATA = Path(__file__).with_name("data") / "degree-two"
KINDS = ("star3", "path4heavy", "path5heavynear", "path5heavycenter",
         "path6", "tailed5", "tailed6")


def expected_model(kind):
    if kind == "star3":
        return 4, 4, [(0, 1), (0, 2), (0, 3)], [[0], [1], [2], [3]], []
    if kind == "path4heavy":
        return 4, 4, [(i, i + 1) for i in range(3)], [[0], [1, 2], [3], [0]], []
    if kind == "path5heavynear":
        return 5, 5, [(i, i + 1) for i in range(4)], [[0], [1, 2], [3], [4], [0]], []
    if kind == "path5heavycenter":
        return 5, 5, [(i, i + 1) for i in range(4)], [[0], [1], [2, 3], [4], [0]], []
    if kind == "path6":
        return 6, 5, [(i, i + 1) for i in range(5)], [[0], [1], [2], [3], [4], [0]], [(1, 4)]
    require(kind in ("tailed5", "tailed6"), "unknown degree-two family")
    m = int(kind[-1])
    graph = [(i, (i + 1) % m) for i in range(m)] + [(0, m)]
    exclusions = [[0], []] + [[i - 1] for i in range(2, m)] + [[m - 1]]
    pairs = [(1, 4), (2, 4)] if m == 5 else [(0, 2), (1, 4), (1, 5), (2, 5), (3, 5)]
    return m + 1, m, graph, exclusions, pairs


def load_family(kind, data_dir=DATA):
    require(kind in KINDS, "unknown degree-two input identity")
    path = Path(data_dir) / (kind + "-family.json")
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CertificateError(f"cannot read {path.name}: {error}") from error


def integer_word(word, length, bound):
    return (isinstance(word, list) and len(word) == length
            and all(type(c) is int and 0 <= c < bound for c in word))


def parse_family(kind, data):
    require(kind in KINDS and isinstance(data, dict), "invalid degree-two family object")
    require(data.get("kind") == kind, "degree-two file/kind identity mismatch")
    n, q, graph, exclusions, pairs = expected_model(kind)
    require(type(data.get("vertex_count")) is int and data["vertex_count"] == n
            and type(data.get("boundary_length")) is int and data["boundary_length"] == q,
            "degree-two model dimensions mismatch")
    raw_edges = data.get("graph_edges")
    require(isinstance(raw_edges, list)
            and all(integer_word(e, 2, n) and e[0] != e[1] for e in raw_edges),
            "invalid degree-two internal edge")
    actual_edges = [edge(a, b) for a, b in raw_edges]
    require(len(actual_edges) == len(set(actual_edges))
            and set(actual_edges) == {edge(a, b) for a, b in graph},
            "degree-two internal graph mismatch")
    raw_exclusions = data.get("forbidden_indices")
    require(isinstance(raw_exclusions, list) and len(raw_exclusions) == n,
            "invalid degree-two exclusion shape")
    actual_exclusions = [p if isinstance(p, list) else [p] for p in raw_exclusions]
    require(all(integer_word(p, len(p), q) and len(p) == len(set(p))
                for p in actual_exclusions) and actual_exclusions == exclusions,
            "degree-two exclusions mismatch")
    groups = data.get("transition_groups")
    expected_groups = [[i] for i in range(q)] + [list(p) for p in pairs]
    require(isinstance(groups, list)
            and all(isinstance(g, list) and len(g) in (1, 2)
                    and integer_word(g, len(g), q) and len(g) == len(set(g)) for g in groups)
            and groups == expected_groups, "degree-two transition/alias groups mismatch")
    require(data.get("normalization") == "first appearance, then unused colours in ascending order",
            "degree-two normalization convention mismatch")
    rows = data.get("records")
    require(isinstance(rows, list) and rows, "missing degree-two cycle records")
    records = {}
    for row in rows:
        require(isinstance(row, dict) and integer_word(row.get("boundary"), q, 4),
                "invalid degree-two template boundary")
        cycle = row.get("cycle")
        # Raw palette and word lengths are checked before any palette indexing.
        require(isinstance(cycle, list) and len(cycle) >= 3
                and all(integer_word(s, n, 4) for s in cycle),
                "invalid degree-two cycle word or palette digit")
        boundary = tuple(row["boundary"])
        require(boundary not in records, "duplicate degree-two cycle record")
        records[boundary] = [tuple(s) for s in cycle]
    return n, q, graph, exclusions, [tuple(g) for g in groups], records


def normalize(boundary):
    order = list(dict.fromkeys(boundary))
    order.extend(c for c in Q if c not in order)
    forward = {c: i for i, c in enumerate(order)}
    return tuple(forward[c] for c in boundary), tuple(order)


def verify_port_aliases(n, q, graph, exclusions, groups):
    adjacency = [set() for _ in range(n)]
    for a, b in graph:
        adjacency[a].add(b)
        adjacency[b].add(a)
    distances = []
    for root in range(n):
        distance, todo = {root: 0}, [root]
        for vertex in todo:
            for other in adjacency[vertex]:
                if other not in distance:
                    distance[other] = distance[vertex] + 1
                    todo.append(other)
        require(len(distance) == n, "disconnected degree-two internal model")
        distances.append(distance)
    incident = [{v for v, ports in enumerate(exclusions) if i in ports} for i in range(q)]
    require(all(incident), "unused degree-two port role")
    pairs = {(a, b) for a, b in combinations(range(q), 2)
             if all(distances[v][w] >= 3 for v in incident[a] for w in incident[b])}
    require(pairs == {g for g in groups if len(g) == 2}, "incomplete degree-two port aliases")
    require(not any(set(combinations(triple, 2)) <= pairs
                    for triple in combinations(range(q), 3)), "uncovered triple port alias")
    return [list(pair) for pair in sorted(pairs)]


def check_family(kind, data):
    n, q, graph, exclusions, groups, records = parse_family(kind, data)
    aliases = verify_port_aliases(n, q, graph, exclusions, groups)
    normal = {t: normalize(t) for t in product(Q, repeat=q)}
    require(set(records) == {t for t, _ in normal.values()},
            "incomplete normalized degree-two template coverage")
    edges = {}
    for boundary, cycle in records.items():
        lists = [[c for c in Q if all(c != boundary[i] for i in ports)] for ports in exclusions]
        actual = {s for s in product(*lists) if all(s[a] != s[b] for a, b in graph)}
        edges[boundary] = check_path(cycle, actual, kind + str(boundary), cyclic=True)
    cache, interfaces = {}, 0
    margins = {",".join(map(str, group)): None for group in groups}
    for boundary, (source, inverse) in normal.items():
        for group in groups:
            if len({boundary[i] for i in group}) != 1:
                continue
            for colour in Q:
                if colour == boundary[group[0]]:
                    continue
                target = list(boundary)
                for i in group:
                    target[i] = colour
                normalized, target_inverse = normal[tuple(target)]
                target_forward = {c: i for i, c in enumerate(target_inverse)}
                relative = tuple(target_forward[inverse[i]] for i in Q)
                key = source, normalized, relative
                if key not in cache:
                    mapped = {edge(tuple(relative[c] for c in a), tuple(relative[c] for c in b))
                              for a, b in edges[source]}
                    cache[key] = len(mapped & edges[normalized])
                common = cache[key]
                require(common >= 2, f"degree-two interface failure: {kind} {boundary}->{target}")
                label = ",".join(map(str, group))
                margins[label] = common if margins[label] is None else min(margins[label], common)
                interfaces += 1
    expected_interfaces = q * 4 ** q * 3 + len(aliases) * 4 ** (q - 1) * 3
    require(interfaces == expected_interfaces and all(v is not None for v in margins.values()),
            "incomplete degree-two directed interfaces")
    return {"kind": kind, "templates": len(records),
            "template_states": sum(map(len, records.values())), "boundaries": len(normal),
            "directed_interfaces": interfaces, "minimum_common_cycle_edges": min(margins.values()),
            "margins_by_changed_indices": margins, "complete_possible_alias_pairs": aliases,
            "distinct_normalized_interface_checks": len(cache)}


def check_degree_two_families(text, data_dir=DATA):
    body = need_block(marked(text), "DEGREE-TWO-FAMILY-COUNTS")
    rows = re.findall(r"^\s*([a-z0-9]+)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)\\\\\s*$", body, re.M)
    require([row[0] for row in rows] == list(KINDS), "missing or duplicate degree-two coverage row")
    results = []
    for row in rows:
        kind = row[0]
        result = check_family(kind, load_family(kind, data_dir))
        values = [result[k] for k in ("templates", "template_states", "boundaries",
                                      "directed_interfaces", "minimum_common_cycle_edges")]
        require(values == list(map(int, row[1:])), "degree-two coverage table mismatch")
        path = Path(data_dir) / (kind + "-family.json")
        raw = path.read_bytes()
        results.append({**result, "file": "data/degree-two/" + path.name,
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"families": results,
            "scope": "exact fixed local models, complete short-cycle port-alias coverage, literal Hamilton cycles and all labelled interfaces; arbitrary-order restoration and structural induction remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_degree_two_families, __doc__))
