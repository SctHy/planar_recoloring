#!/usr/bin/env python3
"""Verify five local-cycle families and every admissible boundary recolouring."""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys
import zlib

from finite_graphs import VerificationError, marked, need_block, require, run_cli

DATA = Path(__file__).with_name("data") / "extended-cycles"
KINDS = ("sharededge", "sharededgechord", "threecontactpath7",
         "onelinkpentagons", "twolinkpentagons")
IDENTITIES = {
    "sharededge": ("bare", "records"),
    "sharededgechord": ("chord", "records"),
    "threecontactpath7": ("path7-three-contact", "records"),
    "onelinkpentagons": ("bridge", "templates"),
    "twolinkpentagons": ("double", "templates"),
}


def expected_model(kind):
    require(kind in KINDS, "unknown extended-cycle model")
    if kind in ("sharededge", "sharededgechord"):
        graph = [(0, 1), (0, 2), (2, 3), (3, 4), (4, 1),
                 (0, 5), (5, 6), (6, 7), (7, 1)]
        if kind == "sharededgechord":
            graph.append((3, 6))
        roles = (2, 3, 4, 5, 6, 7) if kind == "sharededge" else (2, 4, 5, 7)
        exclusions = [((roles.index(i),) if i in roles else ()) for i in range(8)]
        aliases = ((0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4))
        if kind == "sharededgechord":
            aliases = ((0, 3), (1, 2))
        return 8, len(roles), tuple(graph), tuple(exclusions), aliases, ()
    if kind == "threecontactpath7":
        return (7, 5, tuple((i, i + 1) for i in range(6)),
                ((0,), (1,), (2,), (0,), (3,), (4,), (0,)),
                ((1, 3), (1, 4), (2, 4)), ())
    if kind in ("onelinkpentagons", "twolinkpentagons"):
        graph = [(i, (i + 1) % 5) for i in range(5)]
        graph += [(5 + i, 5 + (i + 1) % 5) for i in range(5)] + [(0, 5)]
        internal = {0, 5}
        if kind == "twolinkpentagons":
            graph.append((2, 7))
            internal |= {2, 7}
        roles = tuple(i for i in range(10) if i not in internal)
        exclusions = tuple((roles.index(i),) if i in roles else () for i in range(10))
        half = len(roles) // 2
        aliases = tuple((a, b) for a in range(half) for b in range(half, 2 * half))
        generators = ((0, 4, 3, 2, 1, 5, 6, 7, 8, 9),
                      (0, 1, 2, 3, 4, 5, 9, 8, 7, 6),
                      (5, 6, 7, 8, 9, 0, 1, 2, 3, 4))
        if kind == "twolinkpentagons":
            generators = ((2, 1, 0, 4, 3, 7, 6, 5, 9, 8), generators[-1])
        return 10, len(roles), tuple(graph), exclusions, aliases, generators
    raise VerificationError("unimplemented extended-cycle model")


def unique_object(items):
    require(len(items) == len({key for key, _ in items}), "duplicate JSON field")
    return dict(items)


def load_family(kind, data_dir=DATA):
    require(kind in KINDS, "unknown extended-cycle file identity")
    path = Path(data_dir) / (kind + ".json.gz")
    try:
        return json.loads(gzip.decompress(path.read_bytes()), object_pairs_hook=unique_object)
    except (OSError, EOFError, zlib.error, UnicodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"cannot read {path.name}: {error}") from error


def integer_word(value, length, bound):
    return (isinstance(value, list) and len(value) == length
            and all(type(c) is int and 0 <= c < bound for c in value))


def parse_family(kind, data):
    require(kind in KINDS, "unknown extended-cycle family")
    tag, row_key = IDENTITIES[kind]
    require(isinstance(data, dict) and set(data) == {"family", row_key}
            and data["family"] == tag, "extended-cycle file/kind or raw data format mismatch")
    n, q, _, _, _, _ = expected_model(kind)
    require(isinstance(data[row_key], list) and data[row_key], "missing extended-cycle records")
    records = {}
    for row in data[row_key]:
        require(isinstance(row, dict) and set(row) == {"boundary", "cycle"}
                and integer_word(row["boundary"], q, 4), "invalid extended-cycle boundary")
        raw = row["cycle"]
        require(isinstance(raw, list) and len(raw) >= 3
                and all(isinstance(s, str) and len(s) == n and set(s) <= set("0123") for s in raw),
                "invalid extended-cycle word, palette digit, or length")
        boundary = tuple(row["boundary"])
        require(boundary not in records, "duplicate extended-cycle boundary")
        # Validate all raw digits before integer conversion or palette indexing.
        records[boundary] = tuple(int(s, 4) for s in raw)
    return records


def contracts(kind):
    n, q, graph, exclusions, declared, generators = expected_model(kind)
    require(len(exclusions) == n and all(0 <= v < n for e in graph for v in e), "invalid fixed graph")
    contacts = tuple(frozenset(v for v, ps in enumerate(exclusions) if p in ps) for p in range(q))
    require(all(contacts), "unused extended-cycle port")
    distance = [[0 if a == b else n + 1 for b in range(n)] for a in range(n)]
    for a, b in graph:
        distance[a][b] = distance[b][a] = 1
    for k in range(n):
        for a in range(n):
            for b in range(n):
                distance[a][b] = min(distance[a][b], distance[a][k] + distance[k][b])
    pairs = {(a, b) for a, b in combinations(range(q), 2)
             if all(distance[v][w] >= 3 for v in contacts[a] for w in contacts[b])}
    groups = tuple(g for size in range(2, q + 1) for g in combinations(range(q), size)
                   if all(pair in pairs for pair in combinations(g, 2)))
    require(groups == declared, "incomplete fixed extended-cycle identification classes")
    allowed = set(groups)

    def partitions(left):
        if not left:
            return 1
        first, rest = left[0], left[1:]
        total = 0
        for size in range(len(rest) + 1):
            for others in combinations(rest, size):
                group = (first,) + others
                if others and group not in allowed:
                    continue
                total += partitions(tuple(v for v in rest if v not in others))
        return total

    count = partitions(tuple(range(q)))
    require(count == dict(zip(KINDS, (22, 4, 5, 209, 34)))[kind],
            "extended-cycle identification partition count mismatch")
    group = {tuple(range(n))}
    todo = list(group)
    while todo:
        old = todo.pop()
        for generator in generators:
            new = tuple(generator[old[i]] for i in range(n))
            if new not in group:
                group.add(new)
                todo.append(new)
    edge_set = {tuple(sorted(e)) for e in graph}
    maps = []
    for vertices in sorted(group):
        require(set(vertices) == set(range(n)) and
                {tuple(sorted((vertices[a], vertices[b]))) for a, b in graph} == edge_set,
                "invalid fixed spatial automorphism")
        images = tuple(frozenset(vertices[v] for v in c) for c in contacts)
        require(set(images) == set(contacts), "spatial map changes the physical port model")
        maps.append((vertices, tuple(contacts.index(c) for c in images)))
    require(len(maps) == dict(zip(KINDS, (1, 1, 1, 8, 4)))[kind], "wrong spatial group size")
    return n, q, graph, exclusions, groups, tuple(maps), count, contacts


def normalize(boundary, maps):
    best = None
    for vertices, ports in maps:
        word = tuple(boundary[p] for p in ports)
        palette = list(dict.fromkeys(word))
        normalized = tuple(palette.index(c) for c in word)
        palette.extend(c for c in range(4) if c not in palette)
        if best is None or normalized < best[0]:
            best = normalized, vertices, tuple(palette)
    return best


def legal_states(n, graph, exclusions, boundary):
    previous = [[] for _ in range(n)]
    for a, b in graph:
        previous[max(a, b)].append(min(a, b))
    lists = [tuple(c for c in range(4) if all(c != boundary[p] for p in ps)) for ps in exclusions]
    state, result = [0] * n, set()

    def extend(i, code):
        if i == n:
            result.add(code)
            return
        for c in lists[i]:
            if all(state[j] != c for j in previous[i]):
                state[i] = c
                extend(i + 1, (code << 2) | c)

    extend(0, 0)
    return result


def packed_edge(a, b, width):
    return (min(a, b) << width) | max(a, b)


def one_coordinate(a, b):
    difference = a ^ b
    while difference and difference & 3 == 0:
        difference >>= 2
    return 0 < difference < 4


def check_family(kind, data):
    records = parse_family(kind, data)
    n, q, graph, exclusions, aliases, maps, partitions, contacts = contracts(kind)
    width = 2 * n
    norm = lru_cache(None)(lambda t: normalize(t, maps))
    boundaries = tuple(product(range(4), repeat=q))
    require(set(records) == {norm(t)[0] for t in boundaries}, "incomplete normalized cycle coverage")
    edges, sizes = {}, []
    for boundary, cycle in records.items():
        legal = legal_states(n, graph, exclusions, boundary)
        require(len(cycle) == len(set(cycle)) and set(cycle) == legal,
                f"{kind}: omitted, repeated, or illegal local state")
        require(all(one_coordinate(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1])),
                f"{kind}: illegal cyclic transition or closing edge")
        edges[boundary] = frozenset(packed_edge(a, b, width) for a, b in zip(cycle, cycle[1:] + cycle[:1]))
        require(len(edges[boundary]) == len(cycle), "repeated local cycle edge")
        sizes.append(len(cycle))

    @lru_cache(256)
    def tables(positions, palette):
        split = n // 2
        lengths = (n - split, split)
        output = []
        start = 0
        for length in lengths:
            values = []
            for code in range(4 ** length):
                image = 0
                for i, j in enumerate(positions):
                    if start <= j < start + length:
                        image |= palette[(code >> (2 * (start + length - 1 - j))) & 3] << (2 * (n - 1 - i))
                values.append(image)
            output.append(values)
            start += length
        return output[0], output[1], 2 * split, (1 << (2 * split)) - 1

    @lru_cache(512)
    def transported(boundary, positions, palette):
        upper, lower, shift, mask = tables(positions, palette)
        cycle = records[boundary]
        words = [upper[x >> shift] | lower[x & mask] for x in cycle]
        return frozenset(packed_edge(a, b, width) for a, b in zip(words, words[1:] + words[:1]))

    @lru_cache(300000)
    def common(source, target, positions, palette):
        return len(edges[source] & transported(target, positions, palette))

    moves = tuple((i,) for i in range(q)) + aliases
    histogram, move_sizes, local_lists, margins = Counter(), Counter(), Counter(), {}
    digest = hashlib.sha256()
    for boundary in boundaries:
        source, sm, sp = norm(boundary)
        inverse_palette = tuple(sp.index(c) for c in range(4))
        for move in moves:
            if any(boundary[p] != boundary[move[0]] for p in move):
                continue
            label = ",".join(map(str, move))
            for colour in range(4):
                if colour == boundary[move[0]]:
                    continue
                other = list(boundary)
                for port in move:
                    other[port] = colour
                target, tm, tp = norm(tuple(other))
                positions = tuple(tm.index(sm[i]) for i in range(n))
                palette = tuple(inverse_palette[tp[c]] for c in range(4))
                count = common(source, target, positions, palette)
                require(count >= 2, f"{kind}: insufficient selected-cycle edges at {boundary},{move},{colour}")
                histogram[count] += 1
                move_sizes[str(len(move))] += 1
                local_lists[str(len(set().union(*(contacts[p] for p in move))))] += 1
                margins[label] = min(margins.get(label, count), count)
                digest.update(count.to_bytes(4, "little"))
    total = sum(histogram.values())
    require(total == sum(3 * 4 ** (q - len(g) + 1) for g in moves)
            and len(margins) == len(moves), "incomplete boundary move coverage")
    return {"kind": kind, "vertex_count": n, "boundary_length": q,
            "graph_edges": [list(e) for e in graph],
            "forbidden_indices": [list(ps) for ps in exclusions],
            "physical_contacts": [sorted(c) for c in contacts],
            "possible_alias_groups": [list(g) for g in aliases], "possible_alias_partitions": partitions,
            "spatial_automorphisms": len(maps), "templates": len(records),
            "template_states": sum(sizes), "smallest_fibre": min(sizes), "largest_fibre": max(sizes),
            "labelled_boundaries": len(boundaries), "directed_interfaces": total,
            "move_sizes": dict(sorted(move_sizes.items())), "changed_local_list_counts": dict(sorted(local_lists.items())),
            "minimum_common_cycle_edges": min(histogram), "margins_by_changed_indices": margins,
            "overlap_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "interface_digest": digest.hexdigest()}


def coverage_rows(text):
    body = need_block(marked(text), "EXTENDED-CYCLE-COUNTS")
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    pattern = r"([a-z0-9]+)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)\\\\"
    rows = [re.fullmatch(pattern, line) for line in lines]
    require(len(rows) == len(KINDS) and all(rows), "invalid extended-cycle coverage rows")
    rows = [row.groups() for row in rows]
    require([row[0] for row in rows] == list(KINDS), "missing, extra or reordered extended-cycle kind")
    return {row[0]: tuple(map(int, row[1:])) for row in rows}


def check_extended_cycles(text, data_dir=DATA):
    rows = coverage_rows(text)
    results = []
    for kind in KINDS:
        result = check_family(kind, load_family(kind, data_dir))
        require(tuple(result[key] for key in ("templates", "template_states", "labelled_boundaries",
                                              "directed_interfaces", "minimum_common_cycle_edges")) == rows[kind],
                "extended-cycle coverage table mismatch")
        raw = (Path(data_dir) / (kind + ".json.gz")).read_bytes()
        results.append({**result, "file": "data/extended-cycles/" + kind + ".json.gz",
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"families": results,
            "scope": "complete fixed local states, explicit Hamilton cycles, spatial normalization, every permitted role-identification class and every labelled recolouring move; arbitrary-length restoration and structural results remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_extended_cycles, __doc__))
