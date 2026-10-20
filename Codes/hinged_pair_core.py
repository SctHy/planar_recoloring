"""Hinged-pair graphs, boundary colourings, symmetries and product cycles."""
from __future__ import annotations

from functools import lru_cache
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import zlib

from finite_graphs import VerificationError, require

DATA = Path(__file__).with_name("data") / "hinged-pairs"
KINDS = ("bare", "chord")
BASE = ((0, 1), (0, 2), (2, 3), (3, 4), (4, 1),
        (0, 5), (5, 6), (6, 7), (7, 1))
MINIMUM = {"bare": (6, 6), "chord": (21, 20)}
SEEDS = (("clique2", 2, False), ("clique3", 3, False), ("path3", 3, True))


def model(kind):
    require(kind in KINDS, "unknown hinged-pair model")
    return (BASE + (((3, 6),) if kind == "chord" else ()),
            (0, 2, 3, 4, 5, 6, 7) if kind == "bare" else (0, 2, 4, 5, 7))


@lru_cache(None)
def spatial_maps(kind):
    edges, roles = model(kind)
    maps = (tuple(range(8)), (0, 1, 5, 6, 7, 2, 3, 4))
    output = []
    for vertices in maps:
        require(set(vertices) == set(range(8))
                and {frozenset((vertices[a], vertices[b])) for a, b in edges} == {frozenset(e) for e in edges},
                "invalid hinged-pair spatial graph map")
        require({vertices[v] for v in roles} == set(roles), "hinged-pair spatial map changes contacts")
        output.append((vertices, tuple(roles.index(vertices[v]) for v in roles)))
    return tuple(output)


def normalize(kind, boundary):
    choices = []
    for vertices, roles in spatial_maps(kind):
        palette, renamed = [], []
        for role in roles:
            colour = boundary[role]
            if colour not in palette:
                palette.append(colour)
            renamed.append(palette.index(colour))
        palette.extend(c for c in range(4) if c not in palette)
        choices.append((tuple(renamed), vertices, tuple(palette)))
    return min(choices)


@lru_cache(None)
def canonical_boundaries(kind):
    q = len(model(kind)[1])
    def extend(prefix):
        if len(prefix) == q:
            yield prefix
        else:
            for colour in range(min(4, max(prefix, default=-1) + 2)):
                yield from extend(prefix + (colour,))
    result = tuple(t for t in extend(()) if normalize(kind, t)[0] == t)
    require(len(result) == (379 if kind == "bare" else 31), "hinged-pair canonical coverage mismatch")
    return result


def word(raw, length):
    require(type(raw) is str and len(raw) == length and set(raw) <= set("0123"),
            "invalid hinged-pair raw colour word")
    return int(raw, 4)


def one_change(a, b):
    difference = a ^ b
    while difference and not (difference & 3):
        difference >>= 2
    return 0 < difference < 4


def edge(a, b, bits=16):
    return (min(a, b) << bits) | max(a, b)


def cycle_edges(cycle, bits=16):
    return {edge(a, b, bits) for a, b in zip(cycle, cycle[1:] + cycle[:1])}


def legal_states(kind, boundary):
    edges, roles = model(kind)
    exclusions = dict(zip(roles, boundary))
    previous = [[] for _ in range(8)]
    for a, b in edges:
        previous[max(a, b)].append(min(a, b))
    state, output = [0] * 8, set()
    def extend(i, code):
        if i == 8:
            output.add(code)
            return
        for colour in range(4):
            if colour != exclusions.get(i) and all(colour != state[j] for j in previous[i]):
                state[i] = colour
                extend(i + 1, (code << 2) | colour)
    extend(0, 0)
    return output


def alias_contract(kind):
    edges, roles = model(kind)
    distances = [[0 if i == j else 99 for j in range(8)] for i in range(8)]
    for a, b in edges:
        distances[a][b] = distances[b][a] = 1
    for k in range(8):
        for i in range(8):
            for j in range(8):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
    pairs = tuple((i, j) for i, j in combinations(range(len(roles)), 2) if distances[roles[i]][roles[j]] >= 3)
    require(not any(set(combinations(group, 2)) <= set(pairs) for group in combinations(range(len(roles)), 3)),
            "unhandled hinged-pair triple identification")
    partitions = sum(len({v for pair in subset for v in pair}) == 2 * len(subset)
                     for size in range(len(pairs) + 1) for subset in combinations(pairs, size))
    require((len(pairs), partitions) == ((7, 22) if kind == "bare" else (2, 4)),
            "incomplete hinged-pair identification condition")
    return pairs, partitions


def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, "duplicate hinged-pair JSON field")
        result[key] = value
    return result


def filename(suffix):
    require(suffix in ("cycles", "trees"), "unknown hinged-pair input identity")
    return suffix + ".json.gz"


def load_data(suffix="cycles", data_dir=DATA):
    path = Path(data_dir) / filename(suffix)
    try:
        return json.loads(gzip.decompress(path.read_bytes()), object_pairs_hook=unique_object)
    except (OSError, EOFError, zlib.error, UnicodeError, ValueError) as error:
        raise VerificationError(f"cannot read {path.name}: {error}") from error


def validate_record(kind, suffix, record):
    require(suffix in ("cycles", "trees"), "unknown hinged-pair record kind")
    fields = {"boundary", "matching", "clique2", "clique3", "path3"} if suffix == "cycles" else {"boundary", "blocks", "connectors"}
    require(isinstance(record, dict) and set(record) == fields, "invalid hinged-pair record data format")
    word(record["boundary"], len(model(kind)[1]))
    if suffix == "cycles":
        matching = record["matching"]
        require(isinstance(matching, list) and len(matching) >= 4
                and all(isinstance(pair, list) and len(pair) == 2 for pair in matching), "invalid hinged-pair matching shape")
        for pair in matching:
            for state in pair:
                word(state, 8)
        for key, rows, _ in SEEDS:
            cycle = record[key]
            require(isinstance(cycle, list) and len(cycle) >= 3, "missing hinged-pair product cycle")
            for state in cycle:
                word(state, 9)
                require(int(state[0]) < rows, "invalid hinged-pair physical product cycle row")
    else:
        blocks, connectors = record["blocks"], record["connectors"]
        require(isinstance(blocks, list) and blocks
                and all(isinstance(block, list) and len(block) in (2, 3)
                        and all(type(v) is int and v >= 0 for v in block) for block in blocks), "invalid hinged-pair block indices")
        require(isinstance(connectors, list)
                and all(isinstance(pair, list) and len(pair) == 2
                        and all(type(v) is int and v >= 0 for v in pair) for pair in connectors), "invalid hinged-pair connector indices")


def parse_records(kind, suffix, data):
    require(kind in KINDS and suffix in ("cycles", "trees"), "unknown hinged-pair record identity")
    require(isinstance(data, dict) and set(data) == {"format", "models"}
            and type(data["format"]) is int and data["format"] == 1, "invalid hinged-pair file data format")
    require(isinstance(data["models"], dict) and set(data["models"]) == set(KINDS), "hinged-pair file model set mismatch")
    rows = data["models"][kind]
    require(isinstance(rows, list) and rows, "missing hinged-pair representative records")
    records = {}
    for record in rows:
        validate_record(kind, suffix, record)
        boundary = tuple(map(int, record["boundary"]))
        require(boundary not in records, "duplicate hinged-pair boundary representative")
        records[boundary] = record
    require(set(records) == set(canonical_boundaries(kind)), "missing or extra hinged-pair boundary representative")
    return records


def load_records(kind, suffix="cycles", data_dir=DATA):
    return parse_records(kind, suffix, load_data(suffix, data_dir))


def input_hash(path):
    raw = Path(path).read_bytes()
    return {"file": "data/hinged-pairs/" + Path(path).name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
