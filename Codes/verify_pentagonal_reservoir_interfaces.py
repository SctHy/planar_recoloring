#!/usr/bin/env python3
"""Independently verify pentagon components and boundary transitions.

Legal colourings and their components are enumerated separately from the first
computation. The selected cycles are expressed in the original colour labels."""
from __future__ import annotations

from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

from finite_graphs import VerificationError, marked, need_block, require, run_cli

DATA = Path(__file__).with_name("data") / "pentagonal-reservoirs"
# Frozen independently of verify_pentagonal_reservoirs.py.
CONTRACTS = {
    "reservoir": ("reservoir-family.json", "pentagon_reservoir", 7,
                  ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
                  ((0,), (1,), (2,), (3,), (4,), (5, 6)),
                  tuple((i, j) for i in range(5) for j in (5, 6)), 4),
    "full": ("pentagon-full-family.json", "pentagon_one_full", 4,
             ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
             ((), (0,), (1,), (2,), (3,)), (), 2),
    "pendant": ("pentagon-pendant-family.json", "pentagon_pendant", 5,
                ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4), (0, 5)),
                ((), (0,), (1,), (2,), (3,), (4,)), ((1, 4), (2, 4)), 2),
}


def load_family(kind, data_dir=DATA):
    require(kind in CONTRACTS, "unknown direct pentagonal input")
    path = Path(data_dir) / CONTRACTS[kind][0]
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"cannot read {path.name}: {error}") from error


def valid_word(value, length):
    return (isinstance(value, list) and len(value) == length
            and all(type(c) is int and 0 <= c < 4 for c in value))


def canonical(boundary):
    palette = list(dict.fromkeys(boundary))
    return tuple(palette.index(c) for c in boundary)


def parse_family(kind, data):
    require(kind in CONTRACTS, "unknown direct pentagonal family")
    _, tag, q, _, exclusions, _, capacity = CONTRACTS[kind]
    n = len(exclusions)
    require(isinstance(data, dict) and set(data) == {"kind", "records"}
            and data["kind"] == tag, "direct pentagonal file/kind or data format mismatch")
    rows = data["records"]
    require(isinstance(rows, list) and rows, "missing direct pentagonal records")
    records, cycle_key = {}, "cycles" if kind == "reservoir" else "cycle"
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"boundary", cycle_key}
                and valid_word(row["boundary"], q), "invalid direct pentagonal boundary")
        boundary = tuple(row["boundary"])
        require(boundary not in records, "duplicate direct pentagonal boundary")
        cycles = row[cycle_key] if kind == "reservoir" else [row[cycle_key]]
        count = 2 if kind == "reservoir" and len(set(boundary[:5])) == 1 else 1
        require(isinstance(cycles, list) and len(cycles) == count,
                "wrong direct pentagonal component-cycle count")
        # In particular, negative Python indices are rejected before decoding.
        require(all(isinstance(cycle, list) and len(cycle) >= max(3, capacity)
                    and all(valid_word(s, n) for s in cycle) for cycle in cycles),
                "invalid direct pentagonal cycle word, palette digit or length")
        records[boundary] = cycles
    expected = {canonical(t) for t in product(range(4), repeat=q)}
    require(set(records) == expected, "incomplete direct pentagonal boundary coverage")
    return records


def pack(word):
    return sum(c << (2 * i) for i, c in enumerate(word))


def canonical_components(boundary, graph, exclusions):
    n = len(exclusions)
    previous = [[] for _ in range(n)]
    for a, b in graph:
        previous[max(a, b)].append(min(a, b))
    states, word = set(), [-1] * n

    def extend(i):
        if i == n:
            states.add(pack(word))
            return
        for c in range(4):
            if all(c != boundary[p] for p in exclusions[i]) and all(c != word[j] for j in previous[i]):
                word[i] = c
                extend(i + 1)

    extend(0)
    unseen, result = set(states), set()
    while unseen:
        seed = unseen.pop()
        todo, component = [seed], {seed}
        for state in todo:
            for i in range(n):
                cleared = state & ~(3 << (2 * i))
                for c in range(4):
                    other = cleared | (c << (2 * i))
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        todo.append(other)
        result.add(frozenset(component))
    return result


def aliases(q, graph, exclusions, declared):
    n = len(exclusions)
    distance = [[0 if a == b else n + 1 for b in range(n)] for a in range(n)]
    for a, b in graph:
        distance[a][b] = distance[b][a] = 1
    for k in range(n):
        for a in range(n):
            for b in range(n):
                distance[a][b] = min(distance[a][b], distance[a][k] + distance[k][b])
    incident = [{v for v, ps in enumerate(exclusions) if i in ps} for i in range(q)]
    require(all(incident), "unused direct pentagonal port")
    pairs = {(a, b) for a, b in combinations(range(q), 2)
             if min(distance[x][y] for x in incident[a] for y in incident[b]) >= 3}
    require(pairs == set(declared), "incomplete direct pentagonal identifications")
    require(not any(set(combinations(t, 2)) <= pairs for t in combinations(range(q), 3)),
            "unhandled direct pentagonal triple identification")
    count = sum(len({v for pair in subset for v in pair}) == 2 * len(subset)
                for size in range(len(pairs) + 1) for subset in combinations(sorted(pairs), size))
    return {"possible_identified_pairs": [list(p) for p in sorted(pairs)],
            "possible_alias_matchings": count}


def check_family(kind, data):
    records = parse_family(kind, data)
    _, _, q, graph, exclusions, pairs, capacity = CONTRACTS[kind]
    n, width = len(exclusions), 2 * len(exclusions)
    alias = aliases(q, graph, exclusions, pairs)
    require(alias["possible_alias_matchings"] == {"reservoir": 31, "full": 1, "pendant": 3}[kind],
            "direct pentagonal matching count mismatch")
    orders, component_orders = [], []
    for boundary, cycles in records.items():
        supplied = [frozenset(pack(s) for s in cycle) for cycle in cycles]
        require(all(len(c) == len(cycle) for c, cycle in zip(supplied, cycles)),
                "repeated direct pentagonal state")
        require(len(set(supplied)) == len(supplied)
                and set(supplied) == canonical_components(boundary, graph, exclusions),
                "wrong or incomplete direct pentagonal components")
        orders.append(sum(map(len, supplied)))
        component_orders.extend(map(len, supplied))
    physical = {}
    for boundary in product(range(4), repeat=q):
        palette = list(dict.fromkeys(boundary))
        palette.extend(c for c in range(4) if c not in palette)
        source = tuple(palette.index(c) for c in boundary)
        states, edges = [], []
        for raw in records[source]:
            words = [tuple(palette[c] for c in word) for word in raw]
            require(all(all(s[a] != s[b] for a, b in graph)
                        and all(s[v] != boundary[p] for v, ps in enumerate(exclusions) for p in ps)
                        for s in words), "illegal direct pentagonal local state")
            codes = [pack(s) for s in words]
            component_edges = set()
            for a, b in zip(codes, codes[1:] + codes[:1]):
                difference = a ^ b
                require(sum(bool(difference & (3 << (2 * i))) for i in range(n)) == 1,
                        "illegal direct pentagonal cycle step")
                component_edges.add((min(a, b) << width) | max(a, b))
            require(len(component_edges) == len(words), "repeated direct pentagonal cycle edge")
            states.append(set(codes))
            edges.append(component_edges)
        physical[boundary] = states, edges
    groups = [(i,) for i in range(q)] + list(pairs)
    histogram, directed, overlaps = Counter(), 0, 0
    for boundary, (source_states, source_edges) in physical.items():
        for group in groups:
            if any(boundary[i] != boundary[group[0]] for i in group):
                continue
            for colour in range(4):
                if colour == boundary[group[0]]:
                    continue
                target = list(boundary)
                for i in group:
                    target[i] = colour
                target_states, target_edges = physical[tuple(target)]
                left, right = [False] * len(source_states), [False] * len(target_states)
                for a, source_component in enumerate(source_states):
                    for b, target_component in enumerate(target_states):
                        if source_component.isdisjoint(target_component):
                            continue
                        left[a] = right[b] = True
                        common = len(source_edges[a] & target_edges[b])
                        require(common >= capacity, "insufficient direct pentagonal component-transition edges")
                        histogram[common] += 1
                        overlaps += 1
                require(all(left) and all(right), "killable direct pentagonal component")
                directed += 1
    require(directed == q * 4 ** q * 3 + len(pairs) * 4 ** (q - 1) * 3,
            "incomplete direct pentagonal transitions")
    return {"kind": kind, "canonical_boundaries": len(records),
            "canonical_disconnected_boundaries": sum(len(c) > 1 for c in records.values()),
            "component_cycle_templates": len(component_orders), "template_states": sum(orders),
            "minimum_fibre_order": min(orders), "maximum_fibre_order": max(orders),
            "minimum_component_order": min(component_orders), "labelled_boundaries": len(physical),
            "directed_interfaces": directed, "overlapping_component_interfaces": overlaps,
            "minimum_common_cycle_edges": min(histogram),
            "common_edge_histogram": dict(sorted(histogram.items())), **alias}


def check_pentagonal_reservoir_interfaces(text, data_dir=DATA):
    body = need_block(marked(text), "PENTAGONAL-RESERVOIR-COUNTS")
    rows = re.findall(r"^\s*([a-z]+)((?:&\d+){7})\\\\\s*$", body, re.M)
    require([r[0] for r in rows] == list(CONTRACTS), "missing or duplicate direct pentagonal coverage row")
    results = []
    for kind, counts in rows:
        result = check_family(kind, load_family(kind, data_dir))
        fields = ("canonical_boundaries", "component_cycle_templates", "template_states",
                  "labelled_boundaries", "directed_interfaces", "overlapping_component_interfaces",
                  "minimum_common_cycle_edges")
        require([result[f] for f in fields] == list(map(int, counts[1:].split("&"))),
                "direct pentagonal coverage table mismatch")
        filename = CONTRACTS[kind][0]
        raw = (Path(data_dir) / filename).read_bytes()
        results.append({**result, "file": "data/pentagonal-reservoirs/" + filename,
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"families": results,
            "scope": "independent recursive state construction, packed-state component coverage, transport to the original colour labels and every labelled component transition with bilateral non-killability; no first verification program import or relative-colour cache; unbounded proofs remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_pentagonal_reservoir_interfaces, __doc__))
