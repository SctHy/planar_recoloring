#!/usr/bin/env python3
"""Verify hinged-pair product cycles, protected edges and trees of clique blocks."""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
import hashlib
from itertools import product
from pathlib import Path
import re
import sys

from finite_graphs import marked, need_block, require, run_cli
from hinged_pair_core import (DATA, KINDS, MINIMUM, SEEDS, alias_contract, cycle_edges,
                              edge, filename, input_hash, legal_states, load_data,
                              load_records, model, normalize, one_change, parse_records,
                              spatial_maps, validate_record, word)


def check_seed_template(kind, boundary, record):
    validate_record(kind, "cycles", record)
    require(tuple(map(int, record["boundary"])) == tuple(boundary), "hinged-pair record/boundary mismatch")
    states = legal_states(kind, boundary)
    pairs = [(word(a, 8), word(b, 8)) for a, b in record["matching"]]
    require(len({v for pair in pairs for v in pair}) == 2 * len(pairs), "hinged-pair protected edges are not a matching")
    require(all(a in states and b in states and one_change(a, b) for a, b in pairs), "illegal hinged-pair matching edge")
    require(len(pairs[2:]) >= MINIMUM[kind][1], "insufficient unchanged-boundary hinged-pair core")
    skips = 0
    for key, rows, path in SEEDS:
        cycle = [word(s, 9) for s in record[key]]
        expected = {(row << 16) | state for row in range(rows) for state in states}
        require(len(cycle) == len(set(cycle)) and set(cycle) == expected, "hinged-pair product cycle misses or repeats states")
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            ar, ax, br, bx = a >> 16, a & 65535, b >> 16, b & 65535
            require((ar == br and one_change(ax, bx))
                    or (ax == bx and ar != br and (not path or abs(ar - br) == 1)),
                    "illegal hinged-pair product cycle step")
            if key == "clique3":
                skips += abs(ar - br) == 2
        selected = cycle_edges(cycle, 18)
        require(all(edge((row << 16) | a, (row << 16) | b, 18) in selected
                    for row in range(rows) for a, b in pairs), "hinged-pair matching or reserve missing from row")
    return {"states": states, "full_pairs": pairs, "core_pairs": pairs[2:],
            "full_edges": {edge(a, b) for a, b in pairs}, "core_edges": {edge(a, b) for a, b in pairs[2:]},
            "clique_seed_states": 5 * len(states), "path_seed_states": 3 * len(states),
            "total_seed_states": 8 * len(states), "K3_nonpath_row_edges": skips}


def check_clique_tree(kind, boundary, record):
    validate_record(kind, "trees", record)
    require(tuple(map(int, record["boundary"])) == tuple(boundary), "hinged-pair tree/boundary mismatch")
    states = sorted(legal_states(kind, boundary))
    n, blocks, connectors = len(states), record["blocks"], record["connectors"]
    require(sorted(v for block in blocks for v in block) == list(range(n)),
            "hinged-pair clique blocks do not partition the complete fibre")
    owner = [-1] * n
    for i, block in enumerate(blocks):
        for j, a in enumerate(block):
            owner[a] = i
            require(all(one_change(states[a], states[b]) for b in block[j + 1:]), "hinged-pair block is not a clique")
    require(len(connectors) == len(blocks) - 1, "wrong hinged-pair quotient-tree edge count")
    parent, physical_parent = list(range(len(blocks))), list(range(n))
    used, incident = [0] * n, [[] for _ in range(n)]
    def root(parents, vertex):
        while parents[vertex] != vertex:
            parents[vertex] = parents[parents[vertex]]
            vertex = parents[vertex]
        return vertex
    for i, (a, b) in enumerate(connectors):
        require(0 <= a < n and 0 <= b < n and one_change(states[a], states[b]), "invalid hinged-pair tree connector")
        x, y = root(parent, owner[a]), root(parent, owner[b])
        require(x != y, "cyclic or intrablock hinged-pair quotient connector")
        parent[x] = y
        x, y = root(physical_parent, a), root(physical_parent, b)
        require(x != y, "cycle in physical hinged-pair connector graph")
        physical_parent[x] = y
        used[a] += 1
        used[b] += 1
        incident[a].append(i)
        incident[b].append(i)
    require(max(used) <= 2 and len({root(parent, v) for v in range(len(blocks))}) == 1,
            "disconnected hinged-pair quotient or excessive connector degree bound")
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
            require(colours[i] == -1, "physical hinged-pair connector colouring repeats an edge")
            colours[i] = colour
            a, b = connectors[i]
            vertex, previous, colour = (b if vertex == a else a), i, 1 - colour
    require(all(c in (0, 1) for c in colours), "uncoloured hinged-pair connector")
    require(all(len({colours[i] for i in row}) == len(row) for row in incident),
            "two hinged-pair connectors consume the same reserve at a row")
    return {"states": n, "blocks": len(blocks), "triangle_blocks": sum(len(b) == 3 for b in blocks),
            "connectors": len(connectors), "maximum_physical_capacity": max(used)}


def transform_tables(positions, palette):
    def table(start):
        output = []
        for value in range(256):
            target = 0
            for i, j in enumerate(positions):
                if start <= j < start + 4:
                    target |= palette[(value >> (2 * (start + 3 - j))) & 3] << (2 * (7 - i))
            output.append(target)
        return output
    return table(0), table(4)


def check_family(kind, seed_data=None, tree_data=None, data_dir=DATA):
    seeds = parse_records(kind, "cycles", load_data("cycles", data_dir) if seed_data is None else seed_data)
    trees = parse_records(kind, "trees", load_data("trees", data_dir) if tree_data is None else tree_data)
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
    tables = lru_cache(128)(transform_tables)
    @lru_cache(800)
    def mapped(boundary, positions, palette):
        high, low = tables(positions, palette)
        transformed = [(high[a >> 8] | low[a & 255], high[b >> 8] | low[b & 255]) for a, b in pairs[boundary]]
        return {edge(a, b) for a, b in transformed}, {edge(a, b) for a, b in transformed[2:]}
    @lru_cache(100000)
    def overlap(source, target, positions, palette):
        full, core = mapped(target, positions, palette)
        return len(base[source][0] & full), len(base[source][1] & core)
    histograms, digests = [Counter(), Counter()], [hashlib.sha256(), hashlib.sha256()]
    moves_by_size, directed = Counter(), 0
    for boundary in product(range(4), repeat=q):
        source, sm, sp = normal(boundary)
        inverse_palette = tuple(sp.index(c) for c in range(4))
        for group in tuple((i,) for i in range(q)) + aliases:
            if any(boundary[i] != boundary[group[0]] for i in group):
                continue
            for colour in range(4):
                if colour == boundary[group[0]]:
                    continue
                target = tuple(colour if i in group else boundary[i] for i in range(q))
                canonical, tm, tp = normal(target)
                positions = tuple(tm.index(sm[i]) for i in range(8))
                palette = tuple(inverse_palette[tp[i]] for i in range(4))
                counts = overlap(source, canonical, positions, palette)
                require(all(count >= minimum for count, minimum in zip(counts, MINIMUM[kind])),
                        "insufficient hinged-pair full/core boundary transition overlap")
                for i, count in enumerate(counts):
                    histograms[i][count] += 1
                    digests[i].update(count.to_bytes(4, "little"))
                directed += 1
                moves_by_size[len(group)] += 1
    require(directed == q * 4 ** q * 3 + len(aliases) * 4 ** (q - 1) * 3, "incomplete hinged-pair boundary transitions")
    summaries = [{"minimum_overlap": min(hist), "histogram": dict(sorted(hist.items())), "digest": digest.hexdigest()}
                 for hist, digest in zip(histograms, digests)]
    return {"family": kind, "templates": len(seeds), "template_fibre_states": sum(orders),
            "smallest_fibre": min(orders), "largest_fibre": max(orders),
            "clique_seed_states": 5 * sum(orders), "path_seed_states": 3 * sum(orders), "total_seed_states": 8 * sum(orders),
            "seed_cycles": 3 * len(seeds), "minimum_matching_edges": min(matching_sizes), "minimum_core_edges": min(core_sizes),
            "K3_nonpath_row_edges": skips, "automorphisms": len(spatial_maps(kind)), "labelled_boundaries": 4 ** q,
            "alias_groups": aliases, "alias_partitions": partitions, "directed_interfaces": directed,
            "move_sizes": dict(sorted(moves_by_size.items())), "full_matching": summaries[0], "protected_core": summaries[1],
            "clique_trees": {**tree_totals, "maximum_physical_capacity": capacity}}


def check_hinged_pairs(text, data_dir=DATA):
    body = need_block(marked(text), "HINGED-PAIR-COUNTS")
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    parsed = [re.fullmatch(r"(bare|chord)((?:&\d+){6})\\\\", line) for line in lines]
    require(len(parsed) == 2 and all(parsed), "invalid hinged-pair coverage table syntax")
    rows = [match.groups() for match in parsed]
    require([row[0] for row in rows] == list(KINDS), "missing or duplicate hinged-pair coverage row")
    seeds, trees = load_data("cycles", data_dir), load_data("trees", data_dir)
    families = []
    for kind, counts in rows:
        result = check_family(kind, seeds, trees, data_dir)
        actual = [result["templates"], result["template_fibre_states"], result["total_seed_states"],
                  result["directed_interfaces"], result["full_matching"]["minimum_overlap"], result["protected_core"]["minimum_overlap"]]
        require(actual == list(map(int, counts[1:].split("&"))), "hinged-pair coverage table mismatch")
        families.append(result)
    return {"families": families, "inputs": [input_hash(Path(data_dir) / filename(suffix)) for suffix in ("cycles", "trees")],
            "scope": "exact complete hinged-pentagon K2/K3/P3 product cycles, rowwise full/core matching retention, every labelled physical single/shared-role transition, complete clique partitions and quotient trees with maximum connector degree two; P3 product cycles are additional finite witnesses, while generalized products and arbitrary-order restoration remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_hinged_pairs, __doc__))
