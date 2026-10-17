#!/usr/bin/env python3
"""Independently replay hinged-pair seeds and all physical matching interfaces.

Graph, contact, spatial and alias contracts are frozen here. Literal strings
are restored at every labelled boundary; no primary reader or report is used.
"""
from __future__ import annotations

from collections import Counter
import gzip
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys
import zlib

from certificate_core import CertificateError, marked, need_block, require, run_cli

DATA = Path(__file__).with_name("data") / "hinged-pairs"
KINDS = ("bare", "chord")
CONTRACTS = {
    "bare": {
        "edges": ((0, 1), (0, 2), (2, 3), (3, 4), (4, 1),
                  (0, 5), (5, 6), (6, 7), (7, 1)),
        "ports": (0, 2, 3, 4, 5, 6, 7),
        "maps": ((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 5, 6, 7, 2, 3, 4)),
        "aliases": ((1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5)),
        "partitions": 22, "floors": (6, 6)},
    "chord": {
        "edges": ((0, 1), (0, 2), (2, 3), (3, 4), (4, 1),
                  (0, 5), (5, 6), (6, 7), (7, 1), (3, 6)),
        "ports": (0, 2, 4, 5, 7),
        "maps": ((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 5, 6, 7, 2, 3, 4)),
        "aliases": ((1, 4), (2, 3)), "partitions": 4, "floors": (21, 20)}}


def unique_object(items):
    out = {}
    for key, value in items:
        require(key not in out, "duplicate direct hinged-pair JSON field")
        out[key] = value
    return out


def load_family(data_dir=DATA):
    path = Path(data_dir) / "cycles.json.gz"
    try:
        return json.loads(gzip.decompress(path.read_bytes()), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError, EOFError, zlib.error) as error:
        raise CertificateError(f"cannot read {path.name}: {error}") from error


def raw_word(word, length):
    return type(word) is str and len(word) == length and all(c in "0123" for c in word)


def validate_record(kind, record):
    require(kind in KINDS, "unknown direct hinged-pair kind")
    require(isinstance(record, dict)
            and set(record) == {"boundary", "matching", "clique2", "clique3", "path3"},
            "invalid direct hinged-pair record schema")
    require(raw_word(record["boundary"], len(CONTRACTS[kind]["ports"])),
            "invalid direct hinged-pair boundary")
    matching = record["matching"]
    require(isinstance(matching, list) and len(matching) >= 4
            and all(isinstance(e, list) and len(e) == 2
                    and all(raw_word(s, 8) for s in e) for e in matching),
            "invalid direct hinged-pair raw matching word")
    for name, rows in (("clique2", 2), ("clique3", 3), ("path3", 3)):
        cycle = record[name]
        require(isinstance(cycle, list) and len(cycle) >= 3
                and all(raw_word(s, 9) and int(s[0]) < rows for s in cycle),
                "invalid direct hinged-pair raw seed row or word")


def parse_family(kind, data):
    require(kind in KINDS, "unknown direct hinged-pair family")
    require(isinstance(data, dict) and set(data) == {"format", "models"}
            and type(data["format"]) is int and data["format"] == 1
            and isinstance(data["models"], dict) and set(data["models"]) == set(KINDS),
            "direct hinged-pair input identity or schema mismatch")
    rows = data["models"][kind]
    require(isinstance(rows, list) and rows, "missing direct hinged-pair records")
    out = {}
    for record in rows:
        validate_record(kind, record)
        boundary = record["boundary"]
        require(boundary not in out, "duplicate direct hinged-pair boundary")
        out[boundary] = record
    return out


def check_contract(kind):
    require(kind in KINDS, "unknown direct hinged-pair contract")
    spec = CONTRACTS[kind]
    edges, ports = spec["edges"], spec["ports"]
    distance = [[0 if a == b else 99 for b in range(8)] for a in range(8)]
    for a, b in edges:
        distance[a][b] = distance[b][a] = 1
    for c in range(8):
        for a in range(8):
            for b in range(8):
                distance[a][b] = min(distance[a][b], distance[a][c] + distance[c][b])
    aliases = tuple((a, b) for a, b in combinations(range(len(ports)), 2)
                    if distance[ports[a]][ports[b]] >= 3)
    require(aliases == spec["aliases"], "incomplete direct hinged-pair aliases")
    require(not any(all(p in aliases for p in combinations(t, 2))
                    for t in combinations(range(len(ports)), 3)),
            "unhandled direct hinged-pair triple alias")
    partitions = sum(len({v for e in subset for v in e}) == 2 * len(subset)
                     for size in range(len(aliases) + 1) for subset in combinations(aliases, size))
    require(partitions == spec["partitions"], "direct hinged-pair alias partition mismatch")
    edge_set = {frozenset(e) for e in edges}
    for spatial in spec["maps"]:
        require(set(spatial) == set(range(8))
                and {frozenset((spatial[a], spatial[b])) for a, b in edges} == edge_set
                and {spatial[v] for v in ports} == set(ports),
                "invalid direct hinged-pair spatial contract")
    return spec


def normalize(kind, boundary):
    ports = CONTRACTS[kind]["ports"]
    choices = []
    for spatial in CONTRACTS[kind]["maps"]:
        roles = tuple(ports.index(spatial[v]) for v in ports)
        palette, word = [], ""
        for role in roles:
            colour = boundary[role]
            if colour not in palette:
                palette.append(colour)
            word += str(palette.index(colour))
        palette.extend(c for c in "0123" if c not in palette)
        choices.append((word, spatial, roles, tuple(palette)))
    return min(choices)


def legal_words(kind, boundary):
    edges, ports = CONTRACTS[kind]["edges"], CONTRACTS[kind]["ports"]
    forbidden = dict(zip(ports, boundary))
    previous = [tuple(a if b == v else b for a, b in edges if max(a, b) == v)
                for v in range(8)]
    out = set()

    def extend(word):
        v = len(word)
        if v == 8:
            out.add(word)
            return
        for colour in "0123":
            if colour != forbidden.get(v) and all(colour != word[u] for u in previous[v]):
                extend(word + colour)

    extend("")
    return out


def literal_edge(a, b):
    return tuple(sorted((a, b)))


def check_seed_template(kind, boundary, record):
    validate_record(kind, record)
    require(record["boundary"] == boundary, "direct hinged-pair boundary/record mismatch")
    states = legal_words(kind, boundary)
    pairs = [tuple(e) for e in record["matching"]]
    require(len({s for pair in pairs for s in pair}) == 2 * len(pairs),
            "direct hinged-pair protected edges are not a matching")
    require(all(a in states and b in states and sum(x != y for x, y in zip(a, b)) == 1
                for a, b in pairs), "illegal direct hinged-pair matching edge")
    skips = 0
    for name, rows in (("clique2", 2), ("clique3", 3), ("path3", 3)):
        cycle = record[name]
        require(len(cycle) == len(set(cycle)) == rows * len(states)
                and set(cycle) == {str(r) + s for r in range(rows) for s in states},
                "direct hinged-pair seed omits or repeats a state")
        edges = set()
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            require(sum(x != y for x, y in zip(a, b)) == 1,
                    "illegal direct hinged-pair product step")
            require(name != "path3" or abs(int(a[0]) - int(b[0])) <= 1,
                    "direct hinged-pair path seed has a nonpath row edge")
            skips += name == "clique3" and {a[0], b[0]} == {"0", "2"}
            edges.add(literal_edge(a, b))
        require(all(literal_edge(str(row) + a, str(row) + b) in edges
                    for row in range(rows) for a, b in pairs),
                "direct hinged-pair matching/reserve missing in physical row")
    return {"states": len(states), "pairs": pairs, "K3_nonpath_row_edges": skips}


def check_family(kind, data=None, data_dir=DATA):
    spec = check_contract(kind)
    records = parse_family(kind, load_family(data_dir) if data is None else data)
    q = len(spec["ports"])
    boundaries = list(product("0123", repeat=q))
    maps = {t: normalize(kind, t) for t in boundaries}
    require(set(records) == {m[0] for m in maps.values()},
            "missing or extra direct hinged-pair boundary template")
    matchings, orders, sizes, skips = {}, [], [], 0
    for boundary, record in records.items():
        checked = check_seed_template(kind, boundary, record)
        matchings[boundary] = checked["pairs"]
        orders.append(checked["states"])
        sizes.append(len(checked["pairs"]))
        skips += checked["K3_nonpath_row_edges"]
    require(min(sizes) >= spec["floors"][0] and min(sizes) - 2 >= spec["floors"][1],
            "insufficient direct unchanged-boundary hinged-pair core")
    physical = {}
    for boundary in boundaries:
        key, spatial, _, palette = maps[boundary]
        inverse = tuple(spatial.index(v) for v in range(8))
        translation = str.maketrans("0123", "".join(palette))

        def restore(word):
            translated = word.translate(translation)
            return int("".join(translated[v] for v in inverse), 4)

        endpoint_values = {s: restore(s) for pair in matchings[key] for s in pair}
        values = [(min(endpoint_values[a], endpoint_values[b]) << 16)
                  | max(endpoint_values[a], endpoint_values[b]) for a, b in matchings[key]]
        physical[boundary] = (set(values), set(values[2:]))
    histograms, digests, move_sizes = [Counter(), Counter()], [hashlib.sha256(), hashlib.sha256()], Counter()
    total = 0
    for boundary in boundaries:
        for group in tuple((i,) for i in range(q)) + spec["aliases"]:
            if len({boundary[j] for j in group}) != 1:
                continue
            for colour in "0123":
                if colour == boundary[group[0]]:
                    continue
                target = tuple(colour if j in group else boundary[j] for j in range(q))
                counts = tuple(len(a & b) for a, b in zip(physical[boundary], physical[target]))
                require(all(n >= floor for n, floor in zip(counts, spec["floors"])),
                        "insufficient direct hinged-pair full/core interface overlap")
                for i, count in enumerate(counts):
                    histograms[i][count] += 1
                    digests[i].update(count.to_bytes(4, "little"))
                total += 1
                move_sizes[len(group)] += 1
    require(total == 3 * q * 4 ** q + 3 * len(spec["aliases"]) * 4 ** (q - 1),
            "incomplete direct hinged-pair physical interface coverage")
    summaries = [{"minimum_overlap": min(h), "histogram": dict(sorted(h.items())), "digest": d.hexdigest()}
                 for h, d in zip(histograms, digests)]
    return {"family": kind, "templates": len(records), "template_fibre_states": sum(orders),
            "smallest_fibre": min(orders), "largest_fibre": max(orders),
            "clique_seed_states": 5 * sum(orders), "path_seed_states": 3 * sum(orders),
            "total_seed_states": 8 * sum(orders), "seed_cycles": 3 * len(records),
            "minimum_matching_edges": min(sizes), "minimum_core_edges": min(sizes) - 2,
            "K3_nonpath_row_edges": skips, "automorphisms": len(spec["maps"]),
            "labelled_boundaries": len(boundaries), "alias_groups": spec["aliases"],
            "alias_partitions": spec["partitions"], "directed_interfaces": total,
            "move_sizes": dict(sorted(move_sizes.items())),
            "full_matching": summaries[0], "protected_core": summaries[1],
            "physical_boundaries_restored": len(physical)}


def coverage_rows(text):
    body = need_block(marked(text), "HINGED-PAIR-COUNTS")
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    parsed = [re.fullmatch(r"(bare|chord)((?:&\d+){6})\\\\", line) for line in lines]
    require(len(parsed) == 2 and all(parsed), "invalid direct hinged-pair coverage table")
    rows = [m.groups() for m in parsed]
    require([r[0] for r in rows] == list(KINDS), "direct hinged-pair coverage order mismatch")
    return {kind: tuple(map(int, counts[1:].split("&"))) for kind, counts in rows}


def check_local_obstruction():
    boundary = "2211311"
    states = legal_words("bare", boundary)
    degrees = {s: sum(s[:i] + c + s[i + 1:] in states
                      for i in range(8) for c in "0123" if c != s[i]) for s in states}
    leaves = sorted(s for s, degree in degrees.items() if degree == 1)
    require(len(states) == 526 and sum(degrees.values()) == 3156
            and leaves == ["10032023", "10302023", "13302020"],
            "hinged-pair local obstruction differs from exact reconstruction")
    return {"family": "bare", "boundary": list(map(int, boundary)),
            "states": len(states), "edges": sum(degrees.values()) // 2,
            "leaves": leaves,
            "scope": "three leaves preclude a Hamilton path in this fixed fibre; no complete-graph obstruction is claimed"}


def check_hinged_pair_interfaces(text, data_dir=DATA):
    rows, data = coverage_rows(text), load_family(data_dir)
    families = []
    for kind in KINDS:
        checked = check_family(kind, data=data)
        actual = (checked["templates"], checked["template_fibre_states"], checked["total_seed_states"],
                  checked["directed_interfaces"], checked["full_matching"]["minimum_overlap"],
                  checked["protected_core"]["minimum_overlap"])
        require(actual == rows[kind], "direct hinged-pair coverage count mismatch")
        families.append(checked)
    raw = (Path(data_dir) / "cycles.json.gz").read_bytes()
    return {"families": families,
            "local_obstruction": check_local_obstruction(),
            "inputs": [{"file": "data/hinged-pairs/cycles.json.gz", "bytes": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()}],
            "scope": "independent complete K2/K3/P3 seed and row-retention checks, frozen graph/contact/spatial/alias contracts, literal physical restoration at every labelled boundary and all full/core interface histograms, plus the fixed three-leaf fibre obstruction; clique trees and arbitrary-order products remain separate"}


if __name__ == "__main__":
    sys.exit(run_cli(check_hinged_pair_interfaces, __doc__))
