#!/usr/bin/env python3
"""Verify the seven adjacent-pair cycles and all 53 endpoint paths."""
from itertools import combinations, permutations
import re
import sys

from finite_graphs import (adjacent, check_path, edge, marked, need_block,
                              require, run_cli, words)

TYPES = ("331", "332", "333", "342", "343", "443", "444")
EXPECTED_WORDS = (6, 7, 1, 16, 8, 11, 4)
EXPECTED_PAIRS = (28, 19, 6, 45, 36, 78, 66)
PALETTE = "01234"


def vertices(a, b):
    return {x + y for x in a for y in b if x != y}


def automorphisms(a, b):
    result = []
    for image in permutations(PALETTE):
        p = dict(zip(PALETTE, image))
        pa, pb = {p[x] for x in a}, {p[x] for x in b}
        if pa == a and pb == b:
            result.append(lambda w, p=p: p[w[0]] + p[w[1]])
        if pa == b and pb == a:
            result.append(lambda w, p=p: p[w[1]] + p[w[0]])
    return result


def feasible_endpoints(v):
    """Independent subset dynamic program: possible ends for every start."""
    v = sorted(v)
    n = len(v)
    neighbours = [sum(1 << j for j, y in enumerate(v) if adjacent(x, y)) for x in v]
    result = set()
    for start in range(n):
        dp = [0] * (1 << n)
        dp[1 << start] = 1 << start
        for mask in range(1 << n):
            ends = dp[mask]
            while ends:
                bit = ends & -ends
                ends -= bit
                at = bit.bit_length() - 1
                new = neighbours[at] & ~mask
                while new:
                    nxt = new & -new
                    new -= nxt
                    dp[mask | nxt] |= nxt
        for end in range(n):
            if end != start and dp[-1] & (1 << end):
                result.add(edge(v[start], v[end]))
    return result


def one_list_change(a, b):
    return (len(a) == len(b) == 3 and len(a ^ b) == 2) or (
        {len(a), len(b)} == {3, 4} and (a <= b or b <= a))


def allowed_interface(a, b, ap, bp):
    return ((a == ap and b == bp) or
            (b == bp and one_list_change(a, ap)) or
            (a == ap and one_list_change(b, bp)))


def check_adjacent_pairs(text):
    blocks = marked(text)
    rows = re.findall(r"(\d{3})\s*&\s*([0-4]+)/([0-4]+)\s*&\s*(.*?)(?=\\\\|\n\\end)",
                      need_block(blocks, "PAIR-CYCLES"), re.S)
    require([r[0] for r in rows] == list(TYPES), "missing or reordered pair cycle types")
    endpoint_rows = re.findall(r"For \$(\d{3})\$.*?\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}",
                               text, re.S)
    require([r[0] for r in endpoint_rows] == list(TYPES), "missing endpoint section")
    endpoints = dict(endpoint_rows)
    summaries = {}
    for typ, aa, bb, body in rows:
        a, b = set(aa), set(bb)
        require(typ == f"{len(a)}{len(b)}{len(a & b)}", f"{typ}: wrong lists")
        v = vertices(a, b)
        e = {edge(x, y) for x, y in combinations(v, 2) if adjacent(x, y)}
        cycle = words(body, 2)
        ce = check_path(cycle, v, typ, cyclic=True)
        autos = automorphisms(a, b)
        orbit = {edge(f(x), f(y)) for f in autos for x, y in ce}
        require(orbit == e, f"{typ}: cycle orbit misses an edge")
        paths = [line.split() for line in endpoints[typ].splitlines() if line.strip()]
        i = TYPES.index(typ)
        require(len(paths) == EXPECTED_WORDS[i], f"{typ}: missing endpoint words")
        covered = set()
        for path in paths:
            check_path(path, v, f"{typ} endpoint word")
            covered.update(edge(f(path[0]), f(path[-1])) for f in autos)
        exact = feasible_endpoints(v)
        require(covered == exact and len(exact) == EXPECTED_PAIRS[i],
                f"{typ}: endpoint coverage differs from exact subset DP")
        summaries[typ] = {"states": len(v), "edges": len(e),
                          "endpoint_words": len(paths), "feasible_pairs": len(exact)}
    lists = [set(c) for size in (3, 4) for c in combinations(PALETTE, size)]
    count = entries = contractions = reset_interfaces = 0
    for a in lists:
        for b in lists:
            source = vertices(a, b)
            for ap in lists:
                for bp in lists:
                    if not allowed_interface(a, b, ap, bp):
                        continue
                    count += 1
                    entries += len(source)
                    common = source & vertices(ap, bp)
                    require(len(common) >= 4, "pair transition has too few common states")
                    for x in source:
                        require(any(adjacent(x, y) for y in common),
                                f"pair transition exit failure: {a},{b},{ap},{bp},{x}")
                    if (len(a) != len(ap)) or (len(b) != len(bp)):
                        contractions += 1
                    if len(a) == len(b) == 4:
                        reset_interfaces += 1
                        require(len(common) >= 9 and (len(ap) == 4 or len(bp) == 4),
                                "44 reset transition does not lead to a Hamilton-connected type")
    require(count == 3225 and contractions == 1200, "incomplete boundary transition coverage")
    return {"types": summaries, "endpoint_words": sum(EXPECTED_WORDS),
            "labelled_list_pairs": len(lists) ** 2, "interfaces": count,
            "entry_states_checked": entries, "three_four_list_changes": contractions,
            "reset_interfaces": reset_interfaces,
            "endpoint_cross_check": "exact subset dynamic programming"}


if __name__ == "__main__":
    sys.exit(run_cli(check_adjacent_pairs, __doc__))
