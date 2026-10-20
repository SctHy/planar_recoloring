#!/usr/bin/env python3
"""Verify the path cycles, their symmetry images and the safe-edge counts."""
from itertools import product, permutations, combinations
import re
import sys

from finite_graphs import (adjacent, check_path, cycle_edges, edge, marked,
                              need_block, require, run_cli, words)

Q = "0123"


def states(t):
    return {"".join(x) for x in product(Q, repeat=3)
            if x[0] != x[1] != x[2] and all(x[i] != t[i] for i in range(3))}


def special(t):
    """The unique square edges at an end change from an all-equal boundary."""
    if t[0] == t[1] != t[2]:
        a, b = t[0], t[2]
    elif t[0] != t[1] == t[2]:
        a, b = t[1], t[0]
    else:
        return set()
    result = set()
    for c in set(Q) - {a, b}:
        v = [w for w in states(t) & states(a * 3) if w[1] == c]
        es = {edge(x, y) for x, y in combinations(v, 2) if adjacent(x, y)}
        require(len(es) == 1, f"{t}: end-change special edge is not unique")
        result |= es
    return result


def check_path232(text):
    body = need_block(marked(text), "PATH232-CYCLES")
    matches = re.findall(r"(001|010|012)&(.*?)(?=001&|010&|012&|\\end\{array\})", body, re.S)
    require([t for t, _ in matches] == ["001", "010", "012"], "missing path cycle")
    base = {t: words(row, 3) for t, row in matches}
    expected = {"001": 14, "010": 17, "012": 16}
    allowed = {}
    for t, cycle in base.items():
        check_path(cycle, states(t), t, cyclic=True)
        require(len(cycle) == expected[t], f"{t}: wrong state count")
        for image in permutations(Q):
            p = dict(zip(Q, image))
            for reverse in (False, True):
                u = t[::-1] if reverse else t
                boundary = "".join(p[c] for c in u)
                transformed = ["".join(p[c] for c in (w[::-1] if reverse else w))
                               for w in cycle]
                check_path(transformed, states(boundary), boundary, cyclic=True)
                allowed.setdefault(boundary, set()).add(frozenset(cycle_edges(transformed)))
    good = {"".join(t) for t in product(Q, repeat=3) if len(set(t)) > 1}
    require(set(allowed) == good and len(good) == 60, "incomplete good boundary coverage")
    support_checks = 0
    for t, cycles in allowed.items():
        pt = special(t)
        for ce in cycles:
            require(pt <= ce, f"{t}: selected cycle misses a special edge")
        for a in Q:
            if not adjacent(t, a * 3):
                continue
            for ce in cycles:
                for c in set(Q) - {a}:
                    square = {x for x in states(a * 3) if x[1] == c}
                    square_edges = {edge(x, y) for x, y in combinations(square, 2)
                                    if adjacent(x, y)}
                    retained = len(ce & square_edges)
                    if t[1] == a:
                        b = next(x for x in t if x != a)
                        require(retained == (2 if c == b else 1),
                                f"{t}: end-change square support mismatch")
                        if c == b:
                            es = list(ce & square_edges)
                            require(set(es[0]).isdisjoint(es[1]), "end-change edges not opposite")
                    else:
                        require(retained == (0 if c == t[1] else 3),
                                f"{t}: middle-change square support mismatch")
                        if c == t[1]:
                            require(not (states(t) & square), "forbidden middle square meets fibre")
                    support_checks += 1
    transitions = cycle_pairs = 0
    minima = []
    for t in sorted(good):
        for s in sorted(good):
            if not adjacent(t, s):
                continue
            transitions += 1
            forbidden = special(t) | special(s)
            for a in allowed[t]:
                for b in allowed[s]:
                    safe = (a & b) - forbidden
                    require(len(safe) >= 2, f"safe-common-edge failure: {t}->{s}")
                    minima.append(len(safe))
                    cycle_pairs += 1
    require(transitions == 504, "incomplete adjacent good boundary coverage")
    return {"normalized_states": expected, "good_boundaries": len(good),
            "allowed_cycles": sum(map(len, allowed.values())),
            "directed_good_transitions": transitions,
            "selected_cycle_pairs": cycle_pairs, "minimum_safe_common_edges": min(minima),
            "bad_neighbour_square_support_checks": support_checks,
            "scope": "explicit cycles, symmetry images, and safe-edge hypotheses; arbitrary bad-run lifting is analytic"}


if __name__ == "__main__":
    sys.exit(run_cli(check_path232, __doc__))
