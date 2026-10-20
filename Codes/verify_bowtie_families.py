#!/usr/bin/env python3
"""Verify bowtie product cycles, protected edges and trees of clique blocks."""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
import hashlib
import json
from itertools import product
from pathlib import Path
import re
import sys

from finite_graphs import (VerificationError, cycle_edges as literal_cycle_edges,
                              edge as literal_edge, marked, need_block, require, run_cli, words)
from bowtie_core import (DATA, KINDS, alias_contract, cycle_edges,
                         edge, filename, input_hash, legal_states, load_data,
                         load_records, model, normalize, one_change, parse_records,
                         spatial_maps, unique_object, validate_record, word)
from verify_protected_pentagons import (HARD, ORDINARY, check_seed, components_from_source)


def check_seed_template(kind, boundary, record):
    validate_record(kind, "seeds", record)
    require(tuple(record["boundary"]) == tuple(boundary), "bowtie record/boundary mismatch")
    states = legal_states(kind, boundary)
    require(len(states) >= 18, "bowtie fibre is too small for the product overlap bound")
    pairs = [(word(a, 9), word(b, 9)) for a, b in record["matching"]]
    require(len({v for pair in pairs for v in pair}) == 2 * len(pairs), "protected bowtie edges are not a matching")
    require(all(a in states and b in states and one_change(a, b) for a, b in pairs),
            "illegal bowtie protected edge")
    require(len(pairs[2:]) >= 9, "insufficient unchanged-boundary bowtie core")
    row_skips = 0
    for rows in (2, 3):
        cycle = [word(s, 10) for s in record["cycles"][str(rows)]]
        expected = {(row << 18) | state for row in range(rows) for state in states}
        require(len(cycle) == len(set(cycle)) and set(cycle) == expected,
                "bowtie clique product cycle misses or repeats states")
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            ar, ax, br, bx = a >> 18, a & ((1 << 18) - 1), b >> 18, b & ((1 << 18) - 1)
            require((ar == br and one_change(ax, bx)) or (ax == bx and ar != br),
                    "illegal bowtie clique-product step")
            row_skips += abs(ar - br) == 2
        selected = cycle_edges(cycle, 20)
        for row in range(rows):
            require(all(edge((row << 18) | a, (row << 18) | b, 20) in selected for a, b in pairs),
                    "bowtie protected edge or reserve missing from row")
    return {"states": states, "full_pairs": pairs, "core_pairs": pairs[2:],
            "full_edges": {edge(a, b) for a, b in pairs},
            "core_edges": {edge(a, b) for a, b in pairs[2:]},
            "seed_states": 5 * len(states), "K3_nonpath_row_edges": row_skips}


def check_clique_tree(kind, boundary, record):
    validate_record(kind, "clique-trees", record)
    require(tuple(record["boundary"]) == tuple(boundary), "bowtie tree/boundary mismatch")
    states = sorted(legal_states(kind, boundary))
    n, blocks, connectors = len(states), record["blocks"], record["connectors"]
    flat = [v for block in blocks for v in block]
    require(sorted(flat) == list(range(n)), "bowtie clique blocks do not partition the complete fibre")
    owner = [-1] * n
    for i, block in enumerate(blocks):
        for j, a in enumerate(block):
            owner[a] = i
            require(all(one_change(states[a], states[b]) for b in block[j + 1:]), "bowtie block is not a clique")
    require(len(connectors) == len(blocks) - 1, "wrong bowtie quotient-tree edge count")
    parent, physical_parent, used = list(range(len(blocks))), list(range(n)), [0] * n
    incident = [[] for _ in range(n)]

    def root(parents, vertex):
        while parents[vertex] != vertex:
            parents[vertex] = parents[parents[vertex]]
            vertex = parents[vertex]
        return vertex

    for i, (a, b) in enumerate(connectors):
        require(0 <= a < n and 0 <= b < n and one_change(states[a], states[b]), "invalid bowtie tree connector")
        x, y = root(parent, owner[a]), root(parent, owner[b])
        require(x != y, "cyclic or intrablock bowtie quotient connector")
        parent[x] = y
        x, y = root(physical_parent, a), root(physical_parent, b)
        require(x != y, "cycle in physical bowtie connector graph")
        physical_parent[x] = y
        used[a] += 1
        used[b] += 1
        incident[a].append(i)
        incident[b].append(i)
    require(max(used) <= 2 and len({root(parent, v) for v in range(len(blocks))}) == 1,
            "disconnected bowtie quotient or excessive connector degree bound")
    colours = [-1] * len(connectors)
    for start in range(n):
        if used[start] != 1 or colours[incident[start][0]] != -1:
            continue
        vertex, previous, colour = start, -1, 0
        while True:
            options = [i for i in incident[vertex] if i != previous]
            if not options:
                break
            i = options[0]
            require(colours[i] == -1, "physical bowtie connector colouring repeats an edge")
            colours[i] = colour
            a, b = connectors[i]
            vertex, previous, colour = (b if vertex == a else a), i, 1 - colour
    require(all(c in (0, 1) for c in colours), "uncoloured bowtie connector")
    require(all(len({colours[i] for i in row}) == len(row) for row in incident),
            "two bowtie connectors consume the same reserve at a row")
    return {"states": n, "blocks": len(blocks), "triangle_blocks": sum(len(b) == 3 for b in blocks),
            "connectors": len(connectors), "maximum_physical_capacity": max(used)}


def transform_tables(positions, palette):
    def table(start, length):
        output = []
        for value in range(4 ** length):
            target = 0
            for i, j in enumerate(positions):
                if start <= j < start + length:
                    target |= palette[(value >> (2 * (start + length - 1 - j))) & 3] << (2 * (8 - i))
            output.append(target)
        return output
    return table(0, 5), table(5, 4)


def check_family(kind, seed_data=None, tree_data=None, data_dir=DATA):
    seeds = parse_records(kind, "seeds", load_data(kind, "seeds", data_dir) if seed_data is None else seed_data)
    trees = parse_records(kind, "clique-trees", load_data(kind, "clique-trees", data_dir) if tree_data is None else tree_data)
    base, pairs, orders, matching_sizes, core_sizes = {}, {}, [], [], []
    tree_totals, capacity, skips = Counter(), 0, 0
    for boundary, record in seeds.items():
        checked = check_seed_template(kind, boundary, record)
        base[boundary] = checked["full_edges"], checked["core_edges"]
        pairs[boundary] = checked["full_pairs"]
        orders.append(len(checked["states"]))
        matching_sizes.append(len(checked["full_pairs"]))
        core_sizes.append(len(checked["core_pairs"]))
        skips += checked["K3_nonpath_row_edges"]
        tree = check_clique_tree(kind, boundary, trees[boundary])
        capacity = max(capacity, tree.pop("maximum_physical_capacity"))
        tree_totals.update(tree)
    aliases, partitions = alias_contract(kind)
    q = len(model(kind)[1])
    normal = lru_cache(None)(lambda t: normalize(kind, t))

    @lru_cache(512)
    def tables(positions, palette):
        return transform_tables(positions, palette)

    @lru_cache(800)
    def mapped(boundary, positions, palette):
        high, low = tables(positions, palette)
        transformed = [(high[a >> 8] | low[a & 255], high[b >> 8] | low[b & 255]) for a, b in pairs[boundary]]
        return ({edge(a, b) for a, b in transformed}, {edge(a, b) for a, b in transformed[2:]})

    @lru_cache(200000)
    def overlap(source, target, positions, palette):
        full, core = mapped(target, positions, palette)
        return len(base[source][0] & full), len(base[source][1] & core)

    histograms, digests, moves_by_size = [Counter(), Counter()], [hashlib.sha256(), hashlib.sha256()], Counter()
    directed = 0
    for boundary in product(range(4), repeat=q):
        source, sm, sp = normal(boundary)
        inverse_palette = tuple(sp.index(c) for c in range(4))
        for group in tuple((i,) for i in range(q)) + aliases:
            if any(boundary[i] != boundary[group[0]] for i in group):
                continue
            for colour in range(4):
                if colour == boundary[group[0]]:
                    continue
                target = list(boundary)
                for i in group:
                    target[i] = colour
                canonical, tm, tp = normal(tuple(target))
                positions = tuple(tm.index(sm[i]) for i in range(9))
                palette = tuple(inverse_palette[tp[i]] for i in range(4))
                counts = overlap(source, canonical, positions, palette)
                require(min(counts) >= 9, "insufficient bowtie full/core transition overlap")
                for i, count in enumerate(counts):
                    histograms[i][count] += 1
                    digests[i].update(count.to_bytes(4, "little"))
                directed += 1
                moves_by_size[len(group)] += 1
    require(directed == q * 4 ** q * 3 + len(aliases) * 4 ** (q - 1) * 3, "incomplete bowtie boundary transitions")
    summaries = [{"minimum_overlap": min(hist), "histogram": dict(sorted(hist.items())), "digest": digest.hexdigest()}
                 for hist, digest in zip(histograms, digests)]
    return {"family": kind, "templates": len(seeds), "template_fibre_states": sum(orders),
            "smallest_fibre": min(orders), "largest_fibre": max(orders), "clique_seed_states": 5 * sum(orders),
            "seed_cycles": 2 * len(seeds), "minimum_matching_edges": min(matching_sizes),
            "minimum_core_edges": min(core_sizes), "K3_nonpath_row_edges": skips,
            "automorphisms": len(spatial_maps(kind)), "labelled_boundaries": 4 ** q,
            "alias_groups": aliases, "alias_partitions": partitions, "directed_interfaces": directed,
            "move_sizes": dict(sorted(moves_by_size.items())), "full_matching": summaries[0],
            "protected_core": summaries[1], "clique_trees": {**tree_totals, "maximum_physical_capacity": capacity}}


def load_ordinary(data_dir=DATA):
    path = Path(data_dir) / "ordinary-pentagon-seeds.json"
    try:
        return json.loads(path.read_text(), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError) as error:
        raise VerificationError(f"cannot read ordinary pentagon extract: {error}") from error


def validate_ordinary_pentagons(text, data):
    require(isinstance(data, dict) and set(data) == {"cycles", "hard_cores", "hard_ports", "hard_seeds", "pools", "provenance"},
            "ordinary pentagon extract data format mismatch")
    require(all(isinstance(data[k], dict) for k in data), "invalid ordinary pentagon extract section")
    blocks = marked(text)
    source, _, hard_edges = components_from_source(blocks)
    catalog = {key: value for key, value in source.items() if key[:5] in ORDINARY}
    require(set(data["pools"]) == set(catalog), "ordinary pentagon type/component identity mismatch")
    require(set(data["cycles"]) == {key for key in catalog if key[:5] not in HARD}, "ordinary cycle ID mismatch")
    require(all(set(data[key]) == HARD for key in ("hard_cores", "hard_ports", "hard_seeds")), "ordinary exceptional-type ID mismatch")
    seed_states, protected_edges = 0, 0
    for key, component in catalog.items():
        boundary = key[:5]
        raw_pool = data["pools"][key]
        require(isinstance(raw_pool, list) and all(isinstance(e, list) and len(e) == 2 for e in raw_pool), "invalid ordinary auxiliary edge set")
        for pair in raw_pool:
            for state in pair:
                word(state, 5)
        pool = [literal_edge(*e) for e in raw_pool]
        require(pool == sorted(component["pool"]), "ordinary auxiliary edge set/reserve IDs differ from current marked source")
        vertices, protected = component["vertices"], component["protected"]
        if boundary not in HARD:
            cycle = data["cycles"][key]
            require(isinstance(cycle, list), "invalid ordinary cycle")
            for state in cycle:
                word(state, 5)
            require(tuple(cycle) == component["order"], "ordinary cycle differs from current marked source")
            basis, reserves, seeds = literal_cycle_edges(cycle), pool[2:4], {}
            for rows in (2, 3):
                edges = {literal_edge(str(row) + a, str(row) + b) for row in range(rows) for a, b in basis}
                for row in range(rows - 1):
                    a, b = pool[row]
                    edges.remove(literal_edge(str(row) + a, str(row) + b))
                    edges.remove(literal_edge(str(row + 1) + a, str(row + 1) + b))
                    edges |= {literal_edge(str(row) + s, str(row + 1) + s) for s in (a, b)}
                seeds[rows] = edges
        else:
            ports = data["hard_ports"][boundary]
            require(isinstance(ports, list) and all(isinstance(e, list) and len(e) == 2 for e in ports), "invalid ordinary exceptional ports")
            for pair in ports:
                for state in pair:
                    word(state, 5)
            require([literal_edge(*e) for e in ports] == sorted(protected | component["pool"]),
                    "ordinary exceptional protected set differs from current marked source")
            seed_key = "PC2-00001" if boundary == "00001" else "C2-00112"
            require(data["hard_seeds"][boundary] == words(need_block(blocks, seed_key), 6)
                    and data["hard_cores"][boundary] == words(need_block(blocks, "COREPATH-" + boundary), 5),
                    "ordinary exceptional product cycle/core differs from current marked source")
            two = literal_cycle_edges(data["hard_seeds"][boundary])
            three = set(two)
            short = [["12312", "12313"], ["13212", "13213"]] if boundary == "00001" else [["12303", "12323"], ["13203", "23203"]]
            for path in short + [data["hard_cores"][boundary]]:
                three.remove(literal_edge("1" + path[0], "1" + path[-1]))
                three |= {literal_edge("2" + a, "2" + b) for a, b in zip(path, path[1:])}
                three |= {literal_edge("1" + s, "2" + s) for s in (path[0], path[-1])}
            seeds, reserves = {2: two, 3: three}, pool
            require(seeds == hard_edges[boundary], "ordinary exceptional row product cycles do not match current source")
        require(protected and len(reserves) == 2 and len(set(reserves)) == 2 and set(reserves).isdisjoint(protected),
                "ordinary protected set/reserves invalid")
        for rows, edges in seeds.items():
            check_seed(vertices, edges, rows, key + " corresponding product cycle")
            for row in range(rows):
                require({literal_edge(str(row) + a, str(row) + b) for a, b in protected | set(reserves)} <= edges,
                        "ordinary protected edge/reserve missing from row")
            seed_states += rows * len(vertices)
        protected_edges += len(protected)
    states = sum(len(c["vertices"]) for c in catalog.values())
    require(len(catalog) == 12 and states == 590 and seed_states == 2950, "ordinary product cycle coverage mismatch")
    return {"boundary_types": len(ORDINARY), "component_types": len(catalog), "component_states": states,
            "seed_cycles": 24, "seed_states": seed_states, "protected_edges": protected_edges,
            "reserves_per_component": 2, "component_ids": sorted(catalog),
            "source_binding": "explicit cycles, auxiliary edge sets, protected K, reserves, exceptional P2 product cycles and insertion cores agree with the current marked supplement; existing protected-edge condition under relative normalization applies",
            "row_graph": "P2/P3 product cycle edges are also valid in K2/K3; protected K need not be a matching"}


def check_bowtie_families(text, data_dir=DATA):
    body = need_block(marked(text), "BOWTIE-FAMILY-COUNTS")
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    parsed = [re.fullmatch(r"(bowseed|bowchord)((?:&\d+){6})\\\\", line) for line in lines]
    require(len(parsed) == 2 and all(parsed), "invalid bowtie coverage table syntax")
    rows = [match.groups() for match in parsed]
    require([r[0] for r in rows] == list(KINDS), "missing or duplicate bowtie coverage row")
    ordinary = validate_ordinary_pentagons(text, load_ordinary(data_dir))
    families, inputs = [], [input_hash(Path(data_dir) / "ordinary-pentagon-seeds.json")]
    for kind, counts in rows:
        result = check_family(kind, data_dir=data_dir)
        actual = [result["templates"], result["template_fibre_states"], result["clique_seed_states"],
                  result["directed_interfaces"], result["full_matching"]["minimum_overlap"], result["protected_core"]["minimum_overlap"]]
        require(actual == list(map(int, counts[1:].split("&"))), "bowtie coverage table mismatch")
        families.append(result)
        inputs.extend(input_hash(Path(data_dir) / filename(kind, suffix)) for suffix in ("seeds", "clique-trees"))
    return {"families": families, "ordinary_pentagon_seeds": ordinary, "inputs": inputs,
            "scope": "exact bowtie K2/K3 product cycles and rowwise full/core protection, both complete matching intersections at boundary transitions, clique partitions/quotient trees and maximum connector degree two, and ordinary pentagon product cycles bound to current marked K/reserves; generalized products and unbounded lifting remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_bowtie_families, __doc__))
