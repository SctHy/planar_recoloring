"""Small exact helpers shared by the manuscript's certificate readers."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
from pathlib import Path


class CertificateError(ValueError):
    """A missing, malformed, or mathematically invalid certificate."""


def require(condition, message):
    # Deliberately independent of assertions and of Python's -O option.
    if not condition:
        raise CertificateError(str(message))


def marked(text):
    starts = re.findall(r"^% BEGIN ([A-Z0-9_-]+)$", text, re.M)
    ends = re.findall(r"^% END ([A-Z0-9_-]+)$", text, re.M)
    pairs = re.findall(r"^% BEGIN ([A-Z0-9_-]+)\n(.*?)^% END \1$", text, re.M | re.S)
    require(len(starts) == len(set(starts)), "duplicate certificate marker")
    require(starts == ends and len(pairs) == len(starts), "unmatched certificate marker")
    return dict(pairs)


def need_block(blocks, key):
    require(key in blocks and blocks[key].strip(), f"missing certificate block: {key}")
    return blocks[key]


def words(body, length):
    tokens = re.findall(rf"\b[0-9]{{{length}}}\b", body)
    require(all(set(t) <= set("01234") for t in tokens), "word contains an out-of-palette digit")
    return tokens


def edge(a, b):
    return tuple(sorted((a, b)))


def adjacent(a, b):
    return len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1


def path_edges(path):
    return {edge(a, b) for a, b in zip(path, path[1:])}


def cycle_edges(cycle):
    require(len(cycle) >= 3, "cycle has fewer than three vertices")
    return path_edges(cycle + cycle[:1])


def check_path(path, vertices, context, cyclic=False):
    require(len(path) == len(set(path)) == len(vertices) and set(path) == set(vertices),
            f"{context}: incomplete or repeated vertices")
    edges = cycle_edges(path) if cyclic else path_edges(path)
    require(all(adjacent(a, b) for a, b in edges), f"{context}: illegal transition")
    return edges


def read_edges(body, context, expected=None):
    pairs = re.findall(r"\b([0-3]{5})-([0-3]{5})\b", body)
    edges = {edge(a, b) for a, b in pairs}
    require(pairs and len(edges) == len(pairs), f"{context}: missing or repeated edges")
    if expected is not None:
        require(len(edges) == expected, f"{context}: expected {expected} edges")
    require(all(adjacent(a, b) for a, b in edges), f"{context}: illegal edge")
    return edges


def run_cli(check, description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("source", nargs="?", type=Path,
                        default=Path(__file__).with_name("article_certificates.tex"))
    parser.add_argument("--json", type=Path, help="write a machine-readable report")
    args = parser.parse_args()
    report = {
        "check": check.__name__,
        "source": args.source.name,
        "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "arithmetic": "exact finite sets and integers",
    }
    try:
        report.update(check(args.source.read_text()))
        report["status"] = "PASS"
    except (CertificateError, KeyError, IndexError, ValueError) as error:
        report.update(status="FAIL", error=str(error))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1
