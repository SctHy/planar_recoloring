#!/usr/bin/env python3
"""Check shared-hub path cycles and every labelled physical interface."""
from __future__ import annotations

import hashlib
from itertools import product
import json
from pathlib import Path
import re
import sys

from certificate_core import (CertificateError, check_path, marked, need_block,
                              require, run_cli)

Q = range(4)
DATA = Path(__file__).with_name("data")


def canonical(boundary):
    """Return the first-appearance boundary and its physical inverse map."""
    order = list(dict.fromkeys(boundary))
    order.extend(c for c in Q if c not in order)
    forward = {c: i for i, c in enumerate(order)}
    return tuple(forward[c] for c in boundary), tuple(order)


def load_family(order, data_dir=DATA):
    path = Path(data_dir) / f"path{order}-family.json"
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CertificateError(f"cannot read {path.name}: {error}") from error


def palette_word(word, length):
    return (isinstance(word, list) and len(word) == length
            and all(type(c) is int and c in Q for c in word))


def check_path_family(order, data):
    require(order in (4, 5), "unsupported shared-hub path order")
    require(isinstance(data, dict), "path family must be an object")
    require(type(data.get("path_order")) is int and data["path_order"] == order,
            "wrong shared-hub path order")
    require(data.get("normalization") ==
            "first appearance, then unused colours in ascending order",
            "wrong shared-hub normalization convention")
    records = data.get("records")
    require(isinstance(records, list) and records, "missing shared-hub path templates")
    templates = {}
    for record in records:
        require(isinstance(record, dict), "path template must be an object")
        boundary, cycle = record.get("boundary"), record.get("cycle")
        require(palette_word(boundary, order - 1), "invalid template boundary")
        # Validate the raw digits before using them as palette-map indices:
        # in particular, Python's negative indices are not colour labels.
        require(isinstance(cycle, list) and len(cycle) >= 3
                and all(palette_word(state, order) for state in cycle),
                "invalid template state or out-of-palette colour")
        boundary = tuple(boundary)
        require(boundary not in templates, "duplicate shared-hub path template")
        templates[boundary] = [tuple(state) for state in cycle]

    boundaries = list(product(Q, repeat=order - 1))
    expected = {canonical(t)[0] for t in boundaries}
    require(set(templates) == expected, "incomplete normalized path template coverage")
    path_words = [s for s in product(Q, repeat=order)
                  if all(s[i] != s[i + 1] for i in range(order - 1))]
    physical, legal_sets = {}, {}
    for boundary in boundaries:
        normalized, inverse = canonical(boundary)
        cycle = [tuple(inverse[c] for c in state) for state in templates[normalized]]
        forbidden = boundary + boundary[:1]
        legal = {s for s in path_words
                 if all(c != a for c, a in zip(s, forbidden))}
        physical[boundary] = check_path(cycle, legal, str(boundary), cyclic=True)
        legal_sets[boundary] = legal

    interfaces, minimum = 0, None
    for boundary in boundaries:
        for port in range(order - 1):
            for colour in range(boundary[port] + 1, 4):
                other = boundary[:port] + (colour,) + boundary[port + 1:]
                common = physical[boundary] & physical[other]
                require(len(common) >= 2,
                        f"insufficient shared cycle edges: {boundary}->{other}")
                require(all(a in legal_sets[boundary] & legal_sets[other]
                            and b in legal_sets[boundary] & legal_sets[other]
                            for a, b in common), "illegal physical cross-edge endpoint")
                minimum = len(common) if minimum is None else min(minimum, len(common))
                interfaces += 1
    directed = 2 * interfaces
    require(len(boundaries) == 4 ** (order - 1)
            and directed == len(boundaries) * (order - 1) * 3,
            "incomplete labelled physical interface coverage")
    return {"path_order": order, "normalized_templates": len(templates),
            "template_states": sum(map(len, templates.values())),
            "labelled_boundaries": len(boundaries),
            "directed_physical_interfaces": directed,
            "minimum_shared_cycle_edges": minimum,
            "shared_hub_interfaces": len(boundaries) * 3}


def check_shared_hub_paths(text, data_dir=DATA):
    body = need_block(marked(text), "SHARED-HUB-PATH-COUNTS")
    rows = re.findall(r"^\s*([45])&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)\\\\\s*$",
                      body, re.M)
    require(len(rows) == 2 and [int(row[0]) for row in rows] == [4, 5],
            "missing or duplicate shared-hub coverage row")
    families, inputs = [], []
    for row in rows:
        order = int(row[0])
        result = check_path_family(order, load_family(order, data_dir))
        actual = [result[key] for key in (
            "path_order", "normalized_templates", "template_states", "labelled_boundaries",
            "directed_physical_interfaces", "minimum_shared_cycle_edges")]
        require(actual == list(map(int, row)), "shared-hub coverage table mismatch")
        families.append(result)
        path = Path(data_dir) / f"path{order}-family.json"
        raw = path.read_bytes()
        inputs.append({"path": "data/" + path.name, "bytes": len(raw),
                       "sha256": hashlib.sha256(raw).hexdigest()})
    return {"path_families": families, "certificate_files": inputs,
            "scope": "exact path cycles and all labelled one-port interfaces, including simultaneous endpoint-list changes at the shared hub; arbitrary-order restoration and structural induction remain analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_shared_hub_paths, __doc__))
