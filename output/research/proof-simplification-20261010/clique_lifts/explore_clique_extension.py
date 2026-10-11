"""Exact bounded exploration; universal conclusions require separate proofs."""
from itertools import combinations, combinations_with_replacement
from functools import lru_cache
import json
from pathlib import Path
import time


def graph_for(lists, base_edges):
    vertices = [(i, c) for i, colors in enumerate(lists) for c in sorted(colors)]
    adj = [0] * len(vertices)
    edges = {frozenset(e) for e in base_edges}
    for i, (f, c) in enumerate(vertices):
        for j in range(i):
            g, d = vertices[j]
            if f == g or (c == d and frozenset((f, g)) in edges):
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    return vertices, adj


def hamilton_endpoints(adj, start):
    """Memoized exact suffix search, collecting all possible terminal vertices."""
    all_mask = (1 << len(adj)) - 1
    @lru_cache(None)
    def go(last, remaining):
        if not remaining:
            return 1 << last
        out = 0
        candidates = adj[last] & remaining
        while candidates:
            bit = candidates & -candidates
            candidates -= bit
            out |= go(bit.bit_length() - 1, remaining ^ bit)
        return out
    return go(start, all_mask ^ (1 << start))


def hc_failure(adj):
    all_mask = (1 << len(adj)) - 1
    for start in range(len(adj)):
        ends = hamilton_endpoints(adj, start)
        missing = (all_mask ^ (1 << start)) & ~ends
        if missing:
            return start, (missing & -missing).bit_length() - 1
    return None


def triangle_obstruction(lists):
    s = [lists[i] & lists[(i + 1) % 3] for i in range(3)]
    return len(s[0]) == 2 and s[0] == s[1] == s[2]


def external_condition(lists, edges):
    return all(any(c in lists[j] for edge in edges if i in edge
                   for j in edge if j != i)
               for i, colors in enumerate(lists) for c in colors)


def check_k3():
    palette = range(5)
    options = [frozenset(x) for x in combinations(palette, 3)]
    edges = [(0, 1), (1, 2), (2, 0)]
    tested = 0
    for lists in combinations_with_replacement(options, 3):
        if any(len(lists[a] & lists[b]) < 2 for a, b in edges):
            continue
        if triangle_obstruction(lists) or not external_condition(lists, edges):
            continue
        vertices, adj = graph_for(lists, edges)
        fail = hc_failure(adj)
        tested += 1
        if fail:
            return {"tested": tested, "counterexample": {
                "base": "K3", "lists": [sorted(x) for x in lists],
                "endpoints": [vertices[i] for i in fail]}}
    return {"tested": tested, "counterexample": None}


def main():
    t0 = time.perf_counter()
    # Independent elementary boundary cases for the exact search.
    assert hc_failure([0b110, 0b101, 0b011]) is None  # K3
    assert hc_failure([0b1010, 0b0101, 0b1010, 0b0101]) is not None  # C4
    lists = [frozenset((0, 1, i)) for i in (2, 3, 4)]
    vertices, adj = graph_for(lists, [(0, 1), (1, 2), (2, 0)])
    assert triangle_obstruction(lists)
    assert hc_failure(adj) is not None
    result = {"evidence": "bounded-check", "python_standard_library": True,
              "k3_three_element_lists_palette5": check_k3(),
              "elapsed_seconds": time.perf_counter() - t0}
    out = Path(__file__).with_name("explore-results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
