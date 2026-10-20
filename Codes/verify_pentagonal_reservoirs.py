#!/usr/bin/env python3
"""Verify pentagon component cycles and all labelled boundary transitions."""
from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import re
import sys

from finite_graphs import VerificationError, check_path, marked, need_block, require, run_cli

Q = tuple(range(4))
DATA = Path(__file__).with_name("data") / "pentagonal-reservoirs"
KINDS = ("reservoir", "full", "pendant")
FILES = {"reservoir": "reservoir-family.json", "full": "pentagon-full-family.json",
         "pendant": "pentagon-pendant-family.json"}
TAGS = {"reservoir": "pentagon_reservoir", "full": "pentagon_one_full",
        "pendant": "pentagon_pendant"}


def specification(kind):
    require(kind in KINDS, "unknown pentagonal family")
    graph = [(i, (i + 1) % 5) for i in range(5)]
    if kind == "reservoir":
        n, q, forbidden, capacity = 6, 7, [[i] for i in range(5)] + [[5, 6]], 4
        pairs = [(i, j) for i in range(5) for j in (5, 6)]
    elif kind == "full":
        n, q, forbidden, capacity = 5, 4, [[]] + [[i] for i in range(4)], 2
        pairs = []
    else:
        graph.append((0, 5))
        n, q, forbidden, capacity = 6, 5, [[]] + [[i] for i in range(5)], 2
        pairs = [(1, 4), (2, 4)]
    return n, q, graph, forbidden, [(i,) for i in range(q)] + pairs, capacity


def load_family(kind, data_dir=DATA):
    require(kind in KINDS, "unknown pentagonal input identity")
    path = Path(data_dir) / FILES[kind]
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"cannot read {path.name}: {error}") from error


def word_valid(word, length):
    return (isinstance(word, list) and len(word) == length
            and all(type(c) is int and c in Q for c in word))


def normalize(boundary):
    inverse = list(dict.fromkeys(boundary))
    inverse.extend(c for c in Q if c not in inverse)
    forward = tuple(inverse.index(c) for c in Q)
    return tuple(forward[c] for c in boundary), tuple(inverse), forward


def parse_family(kind, data):
    n, q, _, _, _, capacity = specification(kind)
    require(isinstance(data, dict) and set(data) == {"kind", "records"}
            and data["kind"] == TAGS[kind], "pentagonal file/kind or data format mismatch")
    rows = data["records"]
    require(isinstance(rows, list) and rows, "missing pentagonal boundary records")
    records = {}
    cycle_key = "cycles" if kind == "reservoir" else "cycle"
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"boundary", cycle_key}
                and word_valid(row["boundary"], q), "invalid pentagonal boundary record")
        boundary = tuple(row["boundary"])
        require(boundary not in records, "duplicate pentagonal boundary record")
        cycles = row[cycle_key] if kind == "reservoir" else [row[cycle_key]]
        expected_count = 2 if kind == "reservoir" and len(set(boundary[:5])) == 1 else 1
        require(isinstance(cycles, list) and len(cycles) == expected_count,
                "wrong pentagonal component-cycle count")
        require(all(isinstance(cycle, list) and len(cycle) >= max(3, capacity)
                    and all(word_valid(word, n) for word in cycle) for cycle in cycles),
                "invalid pentagonal cycle word, palette digit or cycle length")
        records[boundary] = [[tuple(word) for word in cycle] for cycle in cycles]
    expected = {normalize(t)[0] for t in product(Q, repeat=q)}
    require(set(records) == expected, "incomplete normalized pentagonal boundary coverage")
    return records


def components(states):
    unseen, result = set(states), []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        component, todo = {seed}, [seed]
        while todo:
            state = todo.pop()
            for i in range(len(state)):
                for colour in Q:
                    target = state[:i] + (colour,) + state[i + 1:]
                    if target in unseen:
                        unseen.remove(target)
                        component.add(target)
                        todo.append(target)
        result.append(component)
    return result


def check_aliases(n, q, graph, forbidden, groups):
    adjacency = [set() for _ in range(n)]
    for a, b in graph:
        adjacency[a].add(b)
        adjacency[b].add(a)
    distance = []
    for root in range(n):
        row, todo = [n + 1] * n, deque([root])
        row[root] = 0
        while todo:
            a = todo.popleft()
            for b in adjacency[a]:
                if row[b] > row[a] + 1:
                    row[b] = row[a] + 1
                    todo.append(b)
        distance.append(row)
    incident = [{v for v, ports in enumerate(forbidden) if p in ports} for p in range(q)]
    require(all(incident), "unused pentagonal port")
    pairs = {(a, b) for a, b in combinations(range(q), 2)
             if all(distance[x][y] >= 3 for x in incident[a] for y in incident[b])}
    require(pairs == {g for g in groups if len(g) == 2}, "incomplete pentagonal shared-vertex moves")
    require(not any(set(combinations(t, 2)) <= pairs for t in combinations(range(q), 3)),
            "unhandled pentagonal triple identification")
    ordered = sorted(pairs)

    def matchings(position, used):
        if position == len(ordered):
            return 1
        a, b = ordered[position]
        return matchings(position + 1, used) + (
            0 if a in used or b in used else matchings(position + 1, used | {a, b}))

    return {"possible_identified_pairs": [list(p) for p in ordered],
            "possible_alias_matchings": matchings(0, set())}


def encode(state):
    value = 0
    for colour in state:
        value = 4 * value + colour
    return value


def check_family(kind, data):
    n, q, graph, forbidden, groups, capacity = specification(kind)
    records = parse_family(kind, data)
    alias = check_aliases(n, q, graph, forbidden, groups)
    require(alias["possible_alias_matchings"] == {"reservoir": 31, "full": 1, "pendant": 3}[kind],
            "pentagonal identification matching count mismatch")
    boundaries = list(records)
    lookup = {boundary: i for i, boundary in enumerate(boundaries)}
    size = 4 ** n

    def ecode(a, b):
        return min(a, b) * size + max(a, b)

    component_states, cycle_edges, orders, component_orders = [], [], [], []
    for boundary, cycles in records.items():
        states = {s for s in product(Q, repeat=n) if all(s[a] != s[b] for a, b in graph)
                  and all(s[v] != boundary[p] for v, ports in enumerate(forbidden) for p in ports)}
        expected = {frozenset(c) for c in components(states)}
        require(len(expected) == len(cycles), "pentagonal component classification mismatch")
        state_sets, edge_sets = [], []
        for cycle in cycles:
            component = frozenset(cycle)
            require(component in expected, "wrong or incomplete pentagonal component cycle")
            expected.remove(component)
            edges = check_path(cycle, component, kind + str(boundary), cyclic=True)
            state_sets.append({encode(s) for s in component})
            edge_sets.append({ecode(encode(a), encode(b)) for a, b in edges})
            component_orders.append(len(component))
        require(not expected, "missing pentagonal component cycle")
        component_states.append(state_sets)
        cycle_edges.append(edge_sets)
        orders.append(len(states))
    palettes = list(permutations(Q))
    palette_ids = {p: i for i, p in enumerate(palettes)}
    words = list(product(Q, repeat=n))
    colour_maps = [[encode(tuple(p[c] for c in s)) for s in words] for p in palettes]

    @lru_cache(maxsize=None)
    def transport(index, palette):
        mapping = colour_maps[palette]
        return ([{mapping[s] for s in component} for component in component_states[index]],
                [{ecode(mapping[e // size], mapping[e % size]) for e in edges}
                 for edges in cycle_edges[index]])

    @lru_cache(maxsize=None)
    def interface(source, target, palette):
        target_states, target_edges = transport(target, palette)
        counts, left, right = [], [False] * len(component_states[source]), [False] * len(target_states)
        for a, source_states in enumerate(component_states[source]):
            for b, other_states in enumerate(target_states):
                if source_states.isdisjoint(other_states):
                    continue
                left[a] = right[b] = True
                common = len(cycle_edges[source][a] & target_edges[b])
                require(common >= capacity, "insufficient pentagonal component-transition edges")
                counts.append(common)
        require(all(left) and all(right), "killable pentagonal component")
        return tuple(counts)

    directed, overlaps, histogram = 0, 0, Counter()
    for boundary in product(Q, repeat=q):
        source, _, forward = normalize(boundary)
        for group in groups:
            if len({boundary[p] for p in group}) != 1:
                continue
            for colour in Q:
                if colour == boundary[group[0]]:
                    continue
                target = list(boundary)
                for p in group:
                    target[p] = colour
                normalized, inverse, _ = normalize(tuple(target))
                relative = palette_ids[tuple(forward[inverse[c]] for c in Q)]
                counts = interface(lookup[source], lookup[normalized], relative)
                directed += 1
                overlaps += len(counts)
                histogram.update(counts)
    pairs = len(alias["possible_identified_pairs"])
    require(directed == q * 4 ** q * 3 + pairs * 4 ** (q - 1) * 3,
            "incomplete pentagonal directed transitions")
    return {"kind": kind, "canonical_boundaries": len(records),
            "canonical_disconnected_boundaries": sum(len(c) > 1 for c in records.values()),
            "component_cycle_templates": len(component_orders), "template_states": sum(orders),
            "minimum_fibre_order": min(orders), "maximum_fibre_order": max(orders),
            "minimum_component_order": min(component_orders), "labelled_boundaries": 4 ** q,
            "directed_interfaces": directed, "overlapping_component_interfaces": overlaps,
            "relative_signatures": interface.cache_info().currsize,
            "minimum_common_cycle_edges": min(histogram),
            "common_edge_histogram": dict(sorted(histogram.items())), **alias}


def check_pentagonal_reservoirs(text, data_dir=DATA):
    body = need_block(marked(text), "PENTAGONAL-RESERVOIR-COUNTS")
    rows = re.findall(r"^\s*([a-z]+)((?:&\d+){7})\\\\\s*$", body, re.M)
    require([r[0] for r in rows] == list(KINDS), "missing or duplicate pentagonal coverage row")
    results = []
    for kind, counts in rows:
        result = check_family(kind, load_family(kind, data_dir))
        fields = ("canonical_boundaries", "component_cycle_templates", "template_states",
                  "labelled_boundaries", "directed_interfaces", "overlapping_component_interfaces",
                  "minimum_common_cycle_edges")
        require([result[f] for f in fields] == list(map(int, counts[1:].split("&"))),
                "pentagonal coverage table mismatch")
        raw = (Path(data_dir) / FILES[kind]).read_bytes()
        results.append({**result, "file": "data/pentagonal-reservoirs/" + FILES[kind],
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"families": results,
            "scope": "exact fixed pentagonal fibres and components, component Hamilton cycles, all port identifications and labelled component transitions, bilateral non-killability and margins four/two; unbounded restoration and structural proofs remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_pentagonal_reservoirs, __doc__))
