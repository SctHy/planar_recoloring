#!/usr/bin/env python3
"""Independently replay degree-two interfaces in physical colour labels.

No primary-reader import, relative-normalization cache, or state-set
enumerator is used. Complete legal-state coverage and alias-distance
completeness are separate obligations of verify_degree_two_families.py.
"""
from __future__ import annotations

import hashlib
from itertools import product
import json
from pathlib import Path
import re
import sys

from certificate_core import CertificateError, marked, need_block, require, run_cli

DATA = Path(__file__).with_name("data") / "degree-two"
# Deliberately separate from the primary reader's model definitions.
CONTRACTS = {
    "star3": (4, ((0, 1), (0, 2), (0, 3)), ((0,), (1,), (2,), (3,)), ()),
    "path4heavy": (4, ((0, 1), (1, 2), (2, 3)), ((0,), (1, 2), (3,), (0,)), ()),
    "path5heavynear": (5, ((0, 1), (1, 2), (2, 3), (3, 4)),
                       ((0,), (1, 2), (3,), (4,), (0,)), ()),
    "path5heavycenter": (5, ((0, 1), (1, 2), (2, 3), (3, 4)),
                         ((0,), (1,), (2, 3), (4,), (0,)), ()),
    "path6": (5, ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5)),
              ((0,), (1,), (2,), (3,), (4,), (0,)), ((1, 4),)),
    "tailed5": (5, ((0, 1), (0, 4), (0, 5), (1, 2), (2, 3), (3, 4)),
                ((0,), (), (1,), (2,), (3,), (4,)), ((1, 4), (2, 4))),
    "tailed6": (6, ((0, 1), (0, 5), (0, 6), (1, 2), (2, 3), (3, 4), (4, 5)),
                ((0,), (), (1,), (2,), (3,), (4,), (5,)),
                ((0, 2), (1, 4), (1, 5), (2, 5), (3, 5))),
}


def load_family(kind, data_dir=DATA):
    require(kind in CONTRACTS, "unknown direct degree-two input identity")
    path = Path(data_dir) / (kind + "-family.json")
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CertificateError(f"cannot read {path.name}: {error}") from error


def valid_word(value, length, bound):
    return (isinstance(value, list) and len(value) == length
            and all(type(c) is int and 0 <= c < bound for c in value))


def check_family(kind, data):
    require(kind in CONTRACTS and isinstance(data, dict), "invalid direct degree-two object")
    q, graph, exclusions, pairs = CONTRACTS[kind]
    n = len(exclusions)
    require(data.get("kind") == kind, "direct degree-two file/kind identity mismatch")
    require(type(data.get("vertex_count")) is int and data["vertex_count"] == n
            and type(data.get("boundary_length")) is int and data["boundary_length"] == q,
            "direct degree-two model dimensions mismatch")
    raw_edges = data.get("graph_edges")
    require(isinstance(raw_edges, list)
            and all(valid_word(e, 2, n) and e[0] != e[1] for e in raw_edges),
            "invalid direct degree-two internal edge")
    actual_edges = [tuple(sorted(e)) for e in raw_edges]
    require(len(actual_edges) == len(set(actual_edges))
            and set(actual_edges) == {tuple(sorted(e)) for e in graph},
            "direct degree-two internal graph mismatch")
    raw_exclusions = data.get("forbidden_indices")
    require(isinstance(raw_exclusions, list) and len(raw_exclusions) == n,
            "invalid direct degree-two exclusion shape")
    lists = [p if isinstance(p, list) else [p] for p in raw_exclusions]
    require(all(valid_word(p, len(p), q) and len(p) == len(set(p)) for p in lists)
            and tuple(tuple(p) for p in lists) == exclusions,
            "direct degree-two exclusions mismatch")
    groups = data.get("transition_groups")
    expected_groups = tuple((i,) for i in range(q)) + pairs
    require(isinstance(groups, list)
            and all(isinstance(g, list) and len(g) in (1, 2)
                    and valid_word(g, len(g), q) and len(g) == len(set(g)) for g in groups)
            and tuple(tuple(g) for g in groups) == expected_groups,
            "direct degree-two transition/alias groups mismatch")
    require(data.get("normalization") == "first appearance, then unused colours in ascending order",
            "direct degree-two normalization convention mismatch")
    rows = data.get("records")
    require(isinstance(rows, list) and rows, "missing direct degree-two cycle records")
    records = {}
    for row in rows:
        require(isinstance(row, dict) and valid_word(row.get("boundary"), q, 4),
                "invalid direct degree-two template boundary")
        cycle = row.get("cycle")
        require(isinstance(cycle, list) and len(cycle) >= 3
                and all(valid_word(s, n, 4) for s in cycle),
                "invalid direct degree-two cycle word or palette digit")
        boundary = tuple(row["boundary"])
        require(boundary not in records, "duplicate direct degree-two cycle record")
        records[boundary] = cycle

    cycles, used_templates = {}, set()
    width = 2 * n
    for boundary in product(range(4), repeat=q):
        palette = list(dict.fromkeys(boundary))
        palette.extend(c for c in range(4) if c not in palette)
        source = tuple(palette.index(c) for c in boundary)
        require(source in records, "missing direct degree-two cycle template")
        used_templates.add(source)
        words = [tuple(palette[c] for c in s) for s in records[source]]
        require(len(words) == len(set(words)), "repeated direct degree-two cycle state")
        for word in words:
            require(all(word[a] != word[b] for a, b in graph)
                    and all(word[v] != boundary[p] for v, ps in enumerate(exclusions) for p in ps),
                    "illegal direct degree-two local state")
        codes = [sum(c << (2 * i) for i, c in enumerate(word)) for word in words]
        edges = set()
        for i, a in enumerate(codes):
            b = codes[(i + 1) % len(codes)]
            difference = a ^ b
            require(sum(bool(difference & (3 << (2 * j))) for j in range(n)) == 1,
                    "illegal direct degree-two cycle step")
            edges.add((min(a, b) << width) | max(a, b))
        require(len(edges) == len(words), "repeated direct degree-two cycle edge")
        cycles[boundary] = edges
    require(set(records) == used_templates, "extra direct degree-two cycle template")
    margins = {",".join(map(str, g)): None for g in expected_groups}
    interfaces = 0
    for boundary, edges in cycles.items():
        for group in expected_groups:
            old = boundary[group[0]]
            if any(boundary[i] != old for i in group):
                continue
            for colour in range(4):
                if colour == old:
                    continue
                target = list(boundary)
                for i in group:
                    target[i] = colour
                common = len(edges & cycles[tuple(target)])
                require(common >= 2, f"direct degree-two interface failure: {kind} {boundary}->{target}")
                label = ",".join(map(str, group))
                margins[label] = common if margins[label] is None else min(margins[label], common)
                interfaces += 1
    require(interfaces == q * 4 ** q * 3 + len(pairs) * 4 ** (q - 1) * 3
            and all(v is not None for v in margins.values()), "incomplete direct degree-two interfaces")
    return {"kind": kind, "templates": len(records),
            "template_states": sum(map(len, records.values())), "boundaries": len(cycles),
            "directed_interfaces": interfaces, "minimum_common_cycle_edges": min(margins.values()),
            "margins_by_changed_indices": margins}


def check_degree_two_interfaces(text, data_dir=DATA):
    body = need_block(marked(text), "DEGREE-TWO-FAMILY-COUNTS")
    rows = re.findall(r"^\s*([a-z0-9]+)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)\\\\\s*$", body, re.M)
    require([row[0] for row in rows] == list(CONTRACTS), "missing or duplicate direct degree-two coverage row")
    results = []
    for row in rows:
        kind = row[0]
        result = check_family(kind, load_family(kind, data_dir))
        values = [result[k] for k in ("templates", "template_states", "boundaries",
                                      "directed_interfaces", "minimum_common_cycle_edges")]
        require(values == list(map(int, row[1:])), "direct degree-two coverage table mismatch")
        path = Path(data_dir) / (kind + "-family.json")
        raw = path.read_bytes()
        results.append({**result, "file": "data/degree-two/" + path.name,
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"families": results,
            "scope": "independent physical-label cycle legality and all labelled interfaces, with no primary-reader import or relative-normalization cache; full local-state coverage, alias completeness and analytic restoration are separate obligations"}


if __name__ == "__main__":
    sys.exit(run_cli(check_degree_two_interfaces, __doc__))
