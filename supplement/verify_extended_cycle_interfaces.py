#!/usr/bin/env python3
"""Independently check connected cycles by literal physical-string transport.

The fixed contracts and normalizing maps are frozen independently of the
primary reader. Complete local coverage is checked by filtering an unrestricted
proper-word enumeration. Every physical interface is enumerated; a source-frame
quotient caches equal string transports, with additional full physical checks.
"""
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

from certificate_core import CertificateError, marked, need_block, require, run_cli

DATA = Path(__file__).with_name("data") / "extended-cycles"
KINDS = ("sharededge", "sharededgechord", "threecontactpath7",
         "onelinkpentagons", "twolinkpentagons")
# These literal contracts are filled from the independently frozen source
# specification, and do not import or consult the publication's primary reader.
CONTRACTS = {'sharededge': {'n': 8,
                'q': 6,
                'edges': ((0, 1), (0, 2), (2, 3), (3, 4), (4, 1), (0, 5), (5, 6), (6, 7), (7, 1)),
                'forbidden': ((), (), (0,), (1,), (2,), (3,), (4,), (5,)),
                'aliases': ((0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4)),
                'tag': 'bare',
                'row_key': 'records',
                'partitions': 22,
                'maps': (((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 2, 3, 4, 5)),)},
 'sharededgechord': {'n': 8,
                     'q': 4,
                     'edges': ((0, 1),
                               (0, 2),
                               (2, 3),
                               (3, 4),
                               (4, 1),
                               (0, 5),
                               (5, 6),
                               (6, 7),
                               (7, 1),
                               (3, 6)),
                     'forbidden': ((), (), (0,), (), (1,), (2,), (), (3,)),
                     'aliases': ((0, 3), (1, 2)),
                     'tag': 'chord',
                     'row_key': 'records',
                     'partitions': 4,
                     'maps': (((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 2, 3)),)},
 'threecontactpath7': {'n': 7,
                       'q': 5,
                       'edges': ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)),
                       'forbidden': ((0,), (1,), (2,), (0,), (3,), (4,), (0,)),
                       'aliases': ((1, 3), (1, 4), (2, 4)),
                       'tag': 'path7-three-contact',
                       'row_key': 'records',
                       'partitions': 5,
                       'maps': (((0, 1, 2, 3, 4, 5, 6), (0, 1, 2, 3, 4)),)},
 'onelinkpentagons': {'n': 10,
                      'edges': ((0, 1),
                                (1, 2),
                                (2, 3),
                                (3, 4),
                                (4, 0),
                                (5, 6),
                                (6, 7),
                                (7, 8),
                                (8, 9),
                                (9, 5),
                                (0, 5)),
                      'forbidden': ((), (0,), (1,), (2,), (3,), (), (4,), (5,), (6,), (7,)),
                      'q': 8,
                      'maps': (((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), (0, 1, 2, 3, 4, 5, 6, 7)),
                               ((0, 1, 2, 3, 4, 5, 9, 8, 7, 6), (0, 1, 2, 3, 7, 6, 5, 4)),
                               ((0, 4, 3, 2, 1, 5, 6, 7, 8, 9), (3, 2, 1, 0, 4, 5, 6, 7)),
                               ((0, 4, 3, 2, 1, 5, 9, 8, 7, 6), (3, 2, 1, 0, 7, 6, 5, 4)),
                               ((5, 6, 7, 8, 9, 0, 1, 2, 3, 4), (4, 5, 6, 7, 0, 1, 2, 3)),
                               ((5, 6, 7, 8, 9, 0, 4, 3, 2, 1), (4, 5, 6, 7, 3, 2, 1, 0)),
                               ((5, 9, 8, 7, 6, 0, 1, 2, 3, 4), (7, 6, 5, 4, 0, 1, 2, 3)),
                               ((5, 9, 8, 7, 6, 0, 4, 3, 2, 1), (7, 6, 5, 4, 3, 2, 1, 0))),
                      'aliases': ((0, 4),
                                  (0, 5),
                                  (0, 6),
                                  (0, 7),
                                  (1, 4),
                                  (1, 5),
                                  (1, 6),
                                  (1, 7),
                                  (2, 4),
                                  (2, 5),
                                  (2, 6),
                                  (2, 7),
                                  (3, 4),
                                  (3, 5),
                                  (3, 6),
                                  (3, 7)),
                      'tag': 'bridge',
                      'row_key': 'templates',
                      'partitions': 209},
 'twolinkpentagons': {'n': 10,
                      'edges': ((0, 1),
                                (1, 2),
                                (2, 3),
                                (3, 4),
                                (4, 0),
                                (5, 6),
                                (6, 7),
                                (7, 8),
                                (8, 9),
                                (9, 5),
                                (0, 5),
                                (2, 7)),
                      'forbidden': ((), (0,), (), (1,), (2,), (), (3,), (), (4,), (5,)),
                      'q': 6,
                      'maps': (((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), (0, 1, 2, 3, 4, 5)),
                               ((2, 1, 0, 4, 3, 7, 6, 5, 9, 8), (0, 2, 1, 3, 5, 4)),
                               ((5, 6, 7, 8, 9, 0, 1, 2, 3, 4), (3, 4, 5, 0, 1, 2)),
                               ((7, 6, 5, 9, 8, 2, 1, 0, 4, 3), (3, 5, 4, 0, 2, 1))),
                      'aliases': ((0, 3),
                                  (0, 4),
                                  (0, 5),
                                  (1, 3),
                                  (1, 4),
                                  (1, 5),
                                  (2, 3),
                                  (2, 4),
                                  (2, 5)),
                      'tag': 'double',
                      'row_key': 'templates',
                      'partitions': 34}}


def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, "duplicate direct extended-cycle JSON field")
        result[key] = value
    return result


def load_family(kind, data_dir=DATA):
    require(kind in KINDS, "unknown direct extended-cycle file")
    path = Path(data_dir) / (kind + ".json.gz")
    try:
        return json.loads(gzip.decompress(path.read_bytes()), object_pairs_hook=unique_object)
    except (OSError, EOFError, zlib.error, UnicodeError, json.JSONDecodeError) as error:
        raise CertificateError(f"cannot read {path.name}: {error}") from error


def parse_family(kind, data):
    require(kind in KINDS, "unknown direct extended-cycle family")
    spec = CONTRACTS[kind]
    require(isinstance(data, dict) and set(data) == {"family", spec["row_key"]}
            and data["family"] == spec["tag"], "direct extended-cycle identity or schema mismatch")
    rows = data[spec["row_key"]]
    require(isinstance(rows, list) and rows, "missing direct extended-cycle templates")
    result = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"boundary", "cycle"},
                "invalid direct extended-cycle template schema")
        boundary, cycle = row["boundary"], row["cycle"]
        require(isinstance(boundary, list) and len(boundary) == spec["q"]
                and all(type(c) is int and 0 <= c <= 3 for c in boundary),
                "invalid direct extended-cycle boundary")
        require(isinstance(cycle, list) and len(cycle) >= 3
                and all(type(s) is str and len(s) == spec["n"]
                        and all(c in "0123" for c in s) for s in cycle),
                "invalid direct extended-cycle raw colour word")
        boundary = tuple(boundary)
        require(boundary not in result, "repeated direct extended-cycle template")
        result[boundary] = tuple(cycle)
    return result


def check_contract(kind):
    spec = CONTRACTS[kind]
    n, q = spec["n"], spec["q"]
    contacts = tuple(tuple(v for v, ps in enumerate(spec["forbidden"]) if p in ps) for p in range(q))
    require(len(spec["forbidden"]) == n and all(contacts), "invalid direct fixed contact model")
    adjacency = [set() for _ in range(n)]
    for a, b in spec["edges"]:
        require(type(a) is type(b) is int and 0 <= a < n and 0 <= b < n and a != b,
                "invalid direct fixed graph edge")
        adjacency[a].add(b)
        adjacency[b].add(a)
    distances = []
    for start in range(n):
        levels, todo = {start: 0}, [start]
        for vertex in todo:
            for other in adjacency[vertex]:
                if other not in levels:
                    levels[other] = levels[vertex] + 1
                    todo.append(other)
        require(len(levels) == n, "disconnected direct fixed model")
        distances.append(levels)
    pairs = {(i, j) for i in range(q) for j in range(i + 1, q)
             if min(distances[a][b] for a in contacts[i] for b in contacts[j]) >= 3}
    groups = tuple(g for size in range(2, q + 1) for g in combinations(range(q), size)
                   if all(p in pairs for p in combinations(g, 2)))
    require(groups == spec["aliases"], "incomplete direct extended-cycle alias classes")
    blocks = []

    def count_partitions(port):
        if port == q:
            return 1
        total = 0
        for block in blocks:
            if all((old, port) in pairs for old in block):
                block.append(port)
                total += count_partitions(port + 1)
                block.pop()
        blocks.append([port])
        total += count_partitions(port + 1)
        blocks.pop()
        return total

    partitions = count_partitions(0)
    require(partitions == spec["partitions"], "wrong direct extended-cycle alias partition count")
    edge_set = {frozenset(e) for e in spec["edges"]}
    for vertices, ports in spec["maps"]:
        require(set(vertices) == set(range(n)) and set(ports) == set(range(q)),
                "invalid direct spatial permutation")
        require({frozenset((vertices[a], vertices[b])) for a, b in spec["edges"]} == edge_set,
                "direct spatial map changes internal graph")
        require(all({vertices[v] for v in contacts[p]} == set(contacts[ports[p]]) for p in range(q)),
                "direct spatial map changes outside roles")
    return contacts


def check_family(kind, data):
    records = parse_family(kind, data)
    spec = CONTRACTS[kind]
    n, q = spec["n"], spec["q"]
    contacts = check_contract(kind)

    @lru_cache(None)
    def normal(boundary):
        choices = []
        for order, (vertices, ports) in enumerate(spec["maps"]):
            image = tuple(boundary[p] for p in ports)
            appearing = list(dict.fromkeys(image))
            key = tuple(appearing.index(c) for c in image)
            palette = tuple(appearing + [c for c in range(4) if c not in appearing])
            choices.append((key, order, vertices, palette))
        key, _, vertices, palette = min(choices)
        return key, vertices, palette

    boundaries = tuple(product(range(4), repeat=q))
    require(set(records) == {normal(t)[0] for t in boundaries},
            "incomplete direct normalized-template coverage")
    # Enumerate the unrestricted proper cube independently of the certificates.
    proper = tuple("".join(s) for s in product("0123", repeat=n)
                   if all(s[a] != s[b] for a, b in spec["edges"]))
    orders = []
    for boundary, cycle in records.items():
        tests = tuple((v, str(boundary[p])) for v, ps in enumerate(spec["forbidden"]) for p in ps)
        legal = {s for s in proper if all(s[v] != c for v, c in tests)}
        require(len(cycle) == len(set(cycle)) and set(cycle) == legal,
                "direct cycle omits, repeats or adds a local state")
        require(all(sum(a != b for a, b in zip(x, y)) == 1
                    for x, y in zip(cycle, cycle[1:] + cycle[:1])),
                "invalid direct local cycle transition or closure")
        orders.append(len(cycle))
    width = 2 * n

    @lru_cache(512)
    def physical(boundary, vertices, palette):
        translation = str.maketrans("0123", "".join(str(c) for c in palette))
        inverse = tuple(vertices.index(i) for i in range(n))
        words = []
        for raw in records[boundary]:
            renamed = raw.translate(translation)
            word = "".join(renamed[i] for i in inverse)
            words.append(int(word, 4))
        return frozenset((min(a, b) << width) | max(a, b)
                         for a, b in zip(words, words[1:] + words[:1]))

    @lru_cache(300000)
    def overlap(source, target, vertices, palette):
        return len(physical(source, tuple(range(n)), (0, 1, 2, 3))
                   & physical(target, vertices, palette))

    histogram, by_size, local_lists, margins = Counter(), Counter(), Counter(), {}
    digest, count, physical_checks = hashlib.sha256(), 0, 0
    moves = tuple((p,) for p in range(q)) + spec["aliases"]
    for boundary in boundaries:
        source, sm, sp = normal(boundary)
        for move in moves:
            if len({boundary[p] for p in move}) != 1:
                continue
            for colour in range(4):
                if colour == boundary[move[0]]:
                    continue
                other = tuple(colour if p in move else boundary[p] for p in range(q))
                target, tm, tp = normal(other)
                relative_positions = tuple(sm.index(i) for i in tm)
                relative_palette = tuple(sp.index(c) for c in tp)
                common = overlap(source, target, relative_positions, relative_palette)
                if count % 4093 == 0:
                    direct = len(physical(source, sm, sp) & physical(target, tm, tp))
                    require(direct == common, "source-frame and literal physical intersections disagree")
                    physical_checks += 1
                require(common >= 2, f"direct extended interface failure: {kind},{boundary},{move},{colour}")
                histogram[common] += 1
                by_size[str(len(move))] += 1
                local_lists[str(len({v for p in move for v in contacts[p]}))] += 1
                label = ",".join(str(p) for p in move)
                margins[label] = min(margins.get(label, common), common)
                digest.update(common.to_bytes(4, "little"))
                count += 1
    require(count == sum(3 * 4 ** (q + 1 - len(g)) for g in moves)
            and len(margins) == len(moves), "incomplete direct physical moves")
    return {"kind": kind, "vertex_count": n, "boundary_length": q,
            "graph_edges": [list(e) for e in spec["edges"]],
            "forbidden_indices": [list(ps) for ps in spec["forbidden"]],
            "physical_contacts": [list(c) for c in contacts],
            "templates": len(records), "template_states": sum(orders),
            "smallest_fibre": min(orders), "largest_fibre": max(orders),
            "labelled_boundaries": len(boundaries), "directed_interfaces": count,
            "possible_alias_groups": [list(g) for g in spec["aliases"]],
            "possible_alias_partitions": spec["partitions"],
            "spatial_automorphisms": len(spec["maps"]),
            "move_sizes": dict(sorted(by_size.items())), "changed_local_list_counts": dict(sorted(local_lists.items())),
            "minimum_common_cycle_edges": min(histogram), "margins_by_changed_indices": margins,
            "overlap_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "interface_digest": digest.hexdigest(), "additional_physical_coordinate_checks": physical_checks}


def coverage_rows(text):
    body = need_block(marked(text), "EXTENDED-CYCLE-COUNTS")
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    rows = []
    for line in lines:
        match = re.fullmatch(r"([a-z0-9]+)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)\\\\", line)
        require(match is not None, "invalid direct extended-cycle coverage row")
        rows.append(match.groups())
    require([row[0] for row in rows] == list(KINDS), "direct extended-cycle coverage order mismatch")
    return {row[0]: tuple(int(c) for c in row[1:]) for row in rows}


def check_extended_cycle_interfaces(text, data_dir=DATA):
    rows = coverage_rows(text)
    results = []
    for kind in KINDS:
        result = check_family(kind, load_family(kind, data_dir))
        actual = tuple(result[key] for key in ("templates", "template_states", "labelled_boundaries",
                                               "directed_interfaces", "minimum_common_cycle_edges"))
        require(actual == rows[kind], "direct extended-cycle coverage table mismatch")
        raw = (Path(data_dir) / (kind + ".json.gz")).read_bytes()
        results.append({**result, "file": "data/extended-cycles/" + kind + ".json.gz",
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"families": results,
            "scope": "independent unrestricted-state coverage, fixed contracts, literal string transport and all physical interfaces, including every shared-role clique; full histograms and digests are returned for comparison; analytic lifting and structural results remain separate"}


if __name__ == "__main__":
    sys.exit(run_cli(check_extended_cycle_interfaces, __doc__))
