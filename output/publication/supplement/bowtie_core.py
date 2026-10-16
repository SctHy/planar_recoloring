"""Fixed bowtie models, strict literal schemas and primary-reader helpers."""
from __future__ import annotations

from functools import lru_cache
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import zlib

from certificate_core import CertificateError, require

DATA = Path(__file__).with_name("data") / "bowties"
KINDS = ("bowseed", "bowchord")
BASE = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
        (0, 5), (5, 6), (6, 7), (7, 8), (8, 0))


def model(kind):
    require(kind in KINDS, "unknown bowtie model")
    edges = BASE + (((2, 6),) if kind == "bowchord" else ())
    ports = tuple(v for v in range(1, 9) if kind == "bowseed" or v not in (2, 6))
    return edges, ports


@lru_cache(None)
def spatial_maps(kind):
    edges, ports = model(kind)
    generators = [(0, 5, 6, 7, 8, 1, 2, 3, 4)]
    if kind == "bowseed":
        generators += [(0, 4, 3, 2, 1, 5, 6, 7, 8), (0, 1, 2, 3, 4, 8, 7, 6, 5)]
    group, todo = {tuple(range(9))}, [tuple(range(9))]
    for permutation in todo:
        for generator in generators:
            image = tuple(generator[permutation[i]] for i in range(9))
            if image not in group:
                group.add(image)
                todo.append(image)
    output = []
    for permutation in sorted(group):
        require(set(permutation) == set(range(9)), "invalid bowtie spatial permutation")
        require({frozenset((permutation[a], permutation[b])) for a, b in edges}
                == {frozenset(e) for e in edges}, "bowtie spatial map changes graph")
        require({permutation[v] for v in ports} == set(ports), "bowtie spatial map changes contacts")
        roles = tuple(ports.index(permutation[v]) for v in ports)
        require(set(roles) == set(range(len(ports))), "invalid bowtie role permutation")
        output.append((permutation, roles))
    require(len(output) == (8 if kind == "bowseed" else 2), "wrong bowtie symmetry count")
    return tuple(output)


def normalize(kind, boundary):
    best = None
    for vertices, roles in spatial_maps(kind):
        palette, renamed = [], []
        for role in roles:
            colour = boundary[role]
            if colour not in palette:
                palette.append(colour)
            renamed.append(palette.index(colour))
        key = tuple(renamed)
        if best is None or key < best[0]:
            best = key, vertices, tuple(palette + [c for c in range(4) if c not in palette])
    return best


@lru_cache(None)
def canonical_boundaries(kind):
    q = len(model(kind)[1])

    def extend(prefix):
        if len(prefix) == q:
            yield prefix
        else:
            for colour in range(min(4, max(prefix, default=-1) + 2)):
                yield from extend(prefix + (colour,))

    return tuple(t for t in extend(()) if normalize(kind, t)[0] == t)


def word(raw, length):
    require(isinstance(raw, str) and len(raw) == length and set(raw) <= set("0123"),
            "invalid bowtie colour word")
    return int(raw, 4)


def one_change(a, b):
    difference = a ^ b
    while difference and not (difference & 3):
        difference >>= 2
    return 0 < difference < 4


def edge(a, b, bits=18):
    return (min(a, b) << bits) | max(a, b)


def cycle_edges(cycle, bits=18):
    return {edge(a, b, bits) for a, b in zip(cycle, cycle[1:] + cycle[:1])}


def legal_states(kind, boundary):
    edges, ports = model(kind)
    exclusions = dict(zip(ports, boundary))
    previous = [[] for _ in range(9)]
    for a, b in edges:
        previous[max(a, b)].append(min(a, b))
    state, output = [0] * 9, set()

    def extend(i, code):
        if i == 9:
            output.add(code)
            return
        for colour in range(4):
            if colour != exclusions.get(i) and all(colour != state[j] for j in previous[i]):
                state[i] = colour
                extend(i + 1, (code << 2) | colour)

    extend(0, 0)
    return output


def alias_contract(kind):
    edges, ports = model(kind)
    n, q = 9, len(ports)
    distance = [[0 if a == b else 99 for b in range(n)] for a in range(n)]
    for a, b in edges:
        distance[a][b] = distance[b][a] = 1
    for k in range(n):
        for a in range(n):
            for b in range(n):
                distance[a][b] = min(distance[a][b], distance[a][k] + distance[k][b])
    pairs = tuple((i, j) for i, j in combinations(range(q), 2)
                  if distance[ports[i]][ports[j]] >= 3)
    require(not any(set(combinations(t, 2)) <= set(pairs) for t in combinations(range(q), 3)),
            "unhandled bowtie triple alias")
    partitions = sum(len({v for pair in subset for v in pair}) == 2 * len(subset)
                     for size in range(len(pairs) + 1) for subset in combinations(pairs, size))
    require((len(pairs), partitions) == ((12, 87) if kind == "bowseed" else (5, 10)),
            "bowtie alias completeness mismatch")
    return pairs, partitions


def filename(kind, suffix):
    require(kind in KINDS and suffix in ("seeds", "clique-trees"), "unknown bowtie input identity")
    return kind + "-" + suffix + ".json.gz"


def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, "duplicate bowtie JSON field")
        result[key] = value
    return result


def load_data(kind, suffix="seeds", data_dir=DATA):
    path = Path(data_dir) / filename(kind, suffix)
    try:
        return json.loads(gzip.decompress(path.read_bytes()), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError, EOFError, zlib.error) as error:
        raise CertificateError(f"cannot read {path.name}: {error}") from error


def validate_record(kind, suffix, record):
    require(suffix in ("seeds", "clique-trees"), "unknown bowtie record kind")
    q = len(model(kind)[1])
    expected = {"boundary", "matching", "cycles"} if suffix == "seeds" else {"boundary", "blocks", "connectors"}
    require(isinstance(record, dict) and set(record) == expected, "invalid bowtie record schema")
    boundary = record["boundary"]
    require(isinstance(boundary, list) and len(boundary) == q
            and all(type(c) is int and 0 <= c < 4 for c in boundary), "invalid bowtie boundary")
    if suffix == "seeds":
        matching = record["matching"]
        require(isinstance(matching, list) and len(matching) >= 4, "missing bowtie matching or reserves")
        for pair in matching:
            require(isinstance(pair, list) and len(pair) == 2, "invalid bowtie matching edge")
            for state in pair:
                word(state, 9)
        cycles = record["cycles"]
        require(isinstance(cycles, dict) and set(cycles) == {"2", "3"}, "missing bowtie clique seed")
        for rows in (2, 3):
            cycle = cycles[str(rows)]
            require(isinstance(cycle, list) and len(cycle) >= 3, "invalid bowtie clique cycle")
            for state in cycle:
                word(state, 10)
                require(int(state[0]) < rows, "invalid physical bowtie seed row")
    else:
        require(isinstance(record["blocks"], list) and record["blocks"], "missing bowtie clique blocks")
        require(all(isinstance(block, list) and len(block) in (2, 3)
                    and all(type(v) is int and v >= 0 for v in block) for block in record["blocks"]),
                "invalid bowtie clique-block indices")
        require(isinstance(record["connectors"], list)
                and all(isinstance(pair, list) and len(pair) == 2
                        and all(type(v) is int and v >= 0 for v in pair) for pair in record["connectors"]),
                "invalid bowtie connector indices")


def parse_records(kind, suffix, data):
    require(kind in KINDS and suffix in ("seeds", "clique-trees"), "unknown bowtie record identity")
    fields = {"family", "templates"} | ({"indexing"} if suffix == "clique-trees" else set())
    require(isinstance(data, dict) and set(data) == fields and data["family"] == kind,
            "bowtie file/family or schema mismatch")
    if suffix == "clique-trees":
        require(data["indexing"] == "ascending packed big-endian legal local words", "bowtie state-index convention mismatch")
    require(isinstance(data["templates"], list), "invalid bowtie template list")
    records = {}
    for record in data["templates"]:
        validate_record(kind, suffix, record)
        boundary = tuple(record["boundary"])
        require(boundary not in records, "duplicate bowtie boundary template")
        records[boundary] = record
    require(set(records) == set(canonical_boundaries(kind)), "missing or extra bowtie boundary template")
    return records


def load_records(kind, suffix="seeds", data_dir=DATA):
    return parse_records(kind, suffix, load_data(kind, suffix, data_dir))


def input_hash(path):
    raw = Path(path).read_bytes()
    return {"file": "data/bowties/" + Path(path).name, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}
