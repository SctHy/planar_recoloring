#!/usr/bin/env python3
"""Independently verify bowtie product cycles and matching intersections.

The local graphs, contacts, symmetries and permissible identifications are
specified separately. Chosen edges are compared in the original colour labels."""
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

DATA = Path(__file__).with_name("data") / "bowties"
KINDS = ("bowseed", "bowchord")
CONTRACTS = {
    "bowseed": {
        "edges": ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                  (0, 5), (5, 6), (6, 7), (7, 8), (8, 0)),
        "ports": (1, 2, 3, 4, 5, 6, 7, 8),
        "maps": (
            ((0, 1, 2, 3, 4, 5, 6, 7, 8), (0, 1, 2, 3, 4, 5, 6, 7)),
            ((0, 1, 2, 3, 4, 8, 7, 6, 5), (0, 1, 2, 3, 7, 6, 5, 4)),
            ((0, 4, 3, 2, 1, 5, 6, 7, 8), (3, 2, 1, 0, 4, 5, 6, 7)),
            ((0, 4, 3, 2, 1, 8, 7, 6, 5), (3, 2, 1, 0, 7, 6, 5, 4)),
            ((0, 5, 6, 7, 8, 1, 2, 3, 4), (4, 5, 6, 7, 0, 1, 2, 3)),
            ((0, 5, 6, 7, 8, 4, 3, 2, 1), (4, 5, 6, 7, 3, 2, 1, 0)),
            ((0, 8, 7, 6, 5, 1, 2, 3, 4), (7, 6, 5, 4, 0, 1, 2, 3)),
            ((0, 8, 7, 6, 5, 4, 3, 2, 1), (7, 6, 5, 4, 3, 2, 1, 0))),
        "aliases": ((0, 5), (0, 6), (1, 4), (1, 5), (1, 6), (1, 7),
                    (2, 4), (2, 5), (2, 6), (2, 7), (3, 5), (3, 6)),
        "partitions": 87},
    "bowchord": {
        "edges": ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                  (0, 5), (5, 6), (6, 7), (7, 8), (8, 0), (2, 6)),
        "ports": (1, 3, 4, 5, 7, 8),
        "maps": (
            ((0, 1, 2, 3, 4, 5, 6, 7, 8), (0, 1, 2, 3, 4, 5)),
            ((0, 5, 6, 7, 8, 1, 2, 3, 4), (3, 4, 5, 0, 1, 2))),
        "aliases": ((0, 4), (1, 3), (1, 4), (1, 5), (2, 4)),
        "partitions": 10}}


def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, "duplicate direct bowtie JSON field")
        result[key] = value
    return result


def load_family(kind, data_dir=DATA):
    require(kind in KINDS, "unknown direct bowtie file")
    path = Path(data_dir) / (kind + "-seeds.json.gz")
    try:
        return json.loads(gzip.decompress(path.read_bytes()), object_pairs_hook=unique_object)
    except (OSError, EOFError, zlib.error, UnicodeError, ValueError) as error:
        raise VerificationError(f"cannot read {path.name}: {error}") from error


def parse_family(kind, data):
    require(kind in KINDS, "unknown direct bowtie model")
    require(isinstance(data, dict) and set(data) == {"family", "templates"}
            and data["family"] == kind, "direct bowtie identity or data format mismatch")
    require(isinstance(data["templates"], list) and data["templates"], "missing direct bowtie representatives")
    q, records = len(CONTRACTS[kind]["ports"]), {}
    for record in data["templates"]:
        require(isinstance(record, dict) and set(record) == {"boundary", "matching", "cycles"},
                "invalid direct bowtie representative data format")
        boundary, matching, cycles = record["boundary"], record["matching"], record["cycles"]
        require(isinstance(boundary, list) and len(boundary) == q
                and all(type(c) is int and 0 <= c < 4 for c in boundary), "invalid direct bowtie boundary")
        require(isinstance(matching, list) and len(matching) >= 4
                and all(isinstance(e, list) and len(e) == 2 for e in matching), "invalid direct bowtie matching")
        require(all(type(s) is str and len(s) == 9 and all(c in "0123" for c in s)
                    for e in matching for s in e), "invalid direct bowtie raw matching word")
        require(isinstance(cycles, dict) and set(cycles) == {"2", "3"}, "missing direct bowtie clique product cycle")
        for rows in (2, 3):
            cycle = cycles[str(rows)]
            require(isinstance(cycle, list) and len(cycle) >= 3
                    and all(type(s) is str and len(s) == 10 and all(c in "0123" for c in s)
                            and s[0] in "012"[:rows] for s in cycle), "invalid direct bowtie raw clique product cycle")
        boundary = tuple(boundary)
        require(boundary not in records, "duplicate direct bowtie representative")
        records[boundary] = record
    return records


def check_contract(kind):
    require(kind in KINDS, "unknown direct bowtie condition")
    spec = CONTRACTS[kind]
    edges, ports, maps, aliases = spec["edges"], spec["ports"], spec["maps"], spec["aliases"]
    require(len(edges) == (10 if kind == "bowseed" else 11)
            and len(ports) == (8 if kind == "bowseed" else 6), "direct bowtie geometry mismatch")
    # Closing the complete group independently also rules out a missing map.
    graph = {frozenset(e) for e in edges}
    spatial = {m for m, _ in maps}
    require(len(spatial) == (8 if kind == "bowseed" else 2) and tuple(range(9)) in spatial,
            "direct bowtie spatial coverage mismatch")
    for m, roles in maps:
        require(set(m) == set(range(9)) and {frozenset((m[a], m[b])) for a, b in edges} == graph,
                "invalid direct bowtie spatial graph map")
        require(tuple(ports.index(m[v]) for v in ports) == roles, "invalid direct bowtie role map")
        require(all(tuple(m[p[i]] for i in range(9)) in spatial for p in spatial), "incomplete direct bowtie spatial group")
    expected = []
    for i, j in combinations(range(len(ports)), 2):
        frontier, seen = {ports[i]}, {ports[i]}
        for _ in range(2):
            frontier = {b if a in frontier else a for a, b in edges if a in frontier or b in frontier} - seen
            seen |= frontier
        if ports[j] not in seen:
            expected.append((i, j))
    require(tuple(expected) == aliases, "direct bowtie identification coverage mismatch")
    require(not any(all(pair in aliases for pair in combinations(group, 2))
                    for group in combinations(range(len(ports)), 3)), "unhandled direct bowtie triple identification")
    partitions = 0
    for mask in range(1 << len(aliases)):
        pairs = [pair for i, pair in enumerate(aliases) if mask & (1 << i)]
        partitions += len({v for pair in pairs for v in pair}) == 2 * len(pairs)
    require(partitions == spec["partitions"], "direct bowtie identification-partition mismatch")
    return spec


@lru_cache(None)
def normalize(kind, boundary):
    possibilities = []
    for order, (m, roles) in enumerate(CONTRACTS[kind]["maps"]):
        values = tuple(boundary[j] for j in roles)
        appearing = list(dict.fromkeys(values))
        key = tuple(appearing.index(c) for c in values)
        palette = tuple(appearing + [c for c in range(4) if c not in appearing])
        possibilities.append((key, order, m, palette))
    key, _, m, palette = min(possibilities)
    return key, m, palette


@lru_cache(None)
def unrestricted_words(kind):
    # Generate paths on both arms independently, then close their two cycles.
    output = []
    def arm(centre, prefix=""):
        if len(prefix) == 4:
            if prefix[-1] != centre:
                yield prefix
            return
        for colour in "0123":
            if colour != (prefix[-1] if prefix else centre):
                yield from arm(centre, prefix + colour)
    for centre in "0123":
        paths = list(arm(centre))
        for left, right in product(paths, repeat=2):
            state = centre + left + right
            if kind == "bowseed" or state[2] != state[6]:
                output.append(state)
    return tuple(output)


def literal_edge(a, b):
    return tuple(sorted((a, b)))


def differs_once(a, b):
    return len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1


def check_seed_template(kind, boundary, record):
    # Parse a one-record wrapper first, so direct calls have the same raw guard.
    parsed = parse_family(kind, {"family": kind, "templates": [record]})
    require(tuple(boundary) in parsed, "direct bowtie boundary/representative mismatch")
    ports = CONTRACTS[kind]["ports"]
    states = {s for s in unrestricted_words(kind) if all(int(s[v]) != boundary[i] for i, v in enumerate(ports))}
    pairs = [tuple(pair) for pair in record["matching"]]
    require(len(states) >= 18 and len(pairs[2:]) >= 9, "insufficient direct bowtie unchanged-boundary margin")
    require(len({s for pair in pairs for s in pair}) == 2 * len(pairs), "direct bowtie protected edges are not a matching")
    require(all(a in states and b in states and differs_once(a, b) for a, b in pairs), "illegal direct bowtie matching")
    skips = 0
    for rows in (2, 3):
        cycle = record["cycles"][str(rows)]
        require(len(cycle) == len(set(cycle)) and set(cycle) == {str(row) + s for row in range(rows) for s in states},
                "direct bowtie clique product cycle omits or repeats a state")
        edges = set()
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            require(differs_once(a, b), "illegal direct bowtie clique-product step")
            edges.add(literal_edge(a, b))
            skips += {a[0], b[0]} == {"0", "2"}
        require(all(literal_edge(str(row) + a, str(row) + b) in edges
                    for row in range(rows) for a, b in pairs), "direct bowtie matching/reserve missing in row")
    return {"states": len(states), "pairs": pairs, "seed_states": 5 * len(states), "K3_nonpath_row_edges": skips}


def check_family(kind, data=None, data_dir=DATA):
    spec = check_contract(kind)
    records = parse_family(kind, load_family(kind, data_dir) if data is None else data)
    q = len(spec["ports"])
    expected = {normalize(kind, t)[0] for t in product(range(4), repeat=q)}
    require(set(records) == expected, "missing or extra direct bowtie boundary representative")
    pairs, orders, matching_sizes, core_sizes, skips = {}, [], [], [], 0
    for boundary, record in records.items():
        checked = check_seed_template(kind, boundary, record)
        pairs[boundary] = checked["pairs"]
        orders.append(checked["states"])
        matching_sizes.append(len(checked["pairs"]))
        core_sizes.append(len(checked["pairs"][2:]))
        skips += checked["K3_nonpath_row_edges"]

    @lru_cache(900)
    def transported(boundary, m, palette):
        translation = str.maketrans("0123", "".join(str(c) for c in palette))
        inverse = [m.index(i) for i in range(9)]
        def physical(state):
            translated = state.translate(translation)
            return int("".join(translated[i] for i in inverse), 4)
        values = {s: physical(s) for pair in pairs[boundary] for s in pair}
        physical_edges = [(min(values[a], values[b]) << 18) | max(values[a], values[b]) for a, b in pairs[boundary]]
        return set(physical_edges), set(physical_edges[2:])

    identity, identity_palette = tuple(range(9)), tuple(range(4))
    @lru_cache(200000)
    def overlap(source, target, target_positions, target_palette):
        a = transported(source, identity, identity_palette)
        b = transported(target, target_positions, target_palette)
        return tuple(len(x & y) for x, y in zip(a, b))

    histograms, digests, moves_by_size = [Counter(), Counter()], [hashlib.sha256(), hashlib.sha256()], Counter()
    total, physical_checks = 0, 0
    moves = tuple((i,) for i in range(q)) + spec["aliases"]
    for boundary in product(range(4), repeat=q):
        source, sm, sp = normalize(kind, boundary)
        for group in moves:
            if len({boundary[j] for j in group}) != 1:
                continue
            for colour in range(4):
                if colour == boundary[group[0]]:
                    continue
                target_boundary = tuple(colour if j in group else boundary[j] for j in range(q))
                target, tm, tp = normalize(kind, target_boundary)
                palette = tuple(sp.index(c) for c in tp)
                positions = tuple(sm.index(j) for j in tm)
                counts = overlap(source, target, positions, palette)
                if total % 4093 == 0:
                    physical_counts = tuple(len(a & b) for a, b in zip(transported(source, sm, sp), transported(target, tm, tp)))
                    require(physical_counts == counts, "explicit physical bowtie overlap differs from source-frame transport")
                    physical_checks += 1
                require(min(counts) >= 9, "insufficient direct bowtie full/core transition overlap")
                for i, count in enumerate(counts):
                    histograms[i][count] += 1
                    digests[i].update(count.to_bytes(4, "little"))
                total += 1
                moves_by_size[len(group)] += 1
    require(total == q * 4 ** q * 3 + len(spec["aliases"]) * 4 ** (q - 1) * 3,
            "incomplete direct bowtie boundary transitions")
    summaries = [{"minimum_overlap": min(hist), "histogram": dict(sorted(hist.items())), "digest": digest.hexdigest()}
                 for hist, digest in zip(histograms, digests)]
    return {"family": kind, "templates": len(records), "template_fibre_states": sum(orders),
            "smallest_fibre": min(orders), "largest_fibre": max(orders), "clique_seed_states": 5 * sum(orders),
            "seed_cycles": 2 * len(records), "minimum_matching_edges": min(matching_sizes), "minimum_core_edges": min(core_sizes),
            "K3_nonpath_row_edges": skips, "automorphisms": len(spec["maps"]), "labelled_boundaries": 4 ** q,
            "alias_groups": spec["aliases"], "alias_partitions": spec["partitions"], "directed_interfaces": total,
            "move_sizes": dict(sorted(moves_by_size.items())), "full_matching": summaries[0], "protected_core": summaries[1],
            "physical_spot_checks": physical_checks}


def check_bowtie_interfaces(text, data_dir=DATA):
    body = need_block(marked(text), "BOWTIE-FAMILY-COUNTS")
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    parsed = [re.fullmatch(r"(bowseed|bowchord)((?:&\d+){6})\\\\", line) for line in lines]
    require(len(parsed) == 2 and all(parsed), "invalid direct bowtie coverage table syntax")
    rows = [match.groups() for match in parsed]
    require([r[0] for r in rows] == list(KINDS), "missing or duplicate direct bowtie coverage row")
    families, inputs = [], []
    for kind, counts in rows:
        result = check_family(kind, data_dir=data_dir)
        actual = [result["templates"], result["template_fibre_states"], result["clique_seed_states"],
                  result["directed_interfaces"], result["full_matching"]["minimum_overlap"], result["protected_core"]["minimum_overlap"]]
        require(actual == list(map(int, counts[1:].split("&"))), "direct bowtie coverage table mismatch")
        families.append(result)
        path = Path(data_dir) / (kind + "-seeds.json.gz")
        raw = path.read_bytes()
        inputs.append({"file": "data/bowties/" + path.name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"families": families, "inputs": inputs,
            "scope": "independent complete bowtie K2/K3 product cycle coverage and rowwise matching/core retention; every labelled single/shared-role factor transition via explicit string transport, with additional original-coordinate checks; no product or unbounded lifting claim"}


if __name__ == "__main__":
    sys.exit(run_cli(check_bowtie_interfaces, __doc__))
