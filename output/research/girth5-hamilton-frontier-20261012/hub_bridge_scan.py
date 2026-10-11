#!/usr/bin/env python3
"""Exact local bridge scan for high-degree hub-fan fibres.

The graph construction is only used to certify that the list pattern comes
from a planar girth-five branch graph.  The Hamilton obstruction below is for
the *fibre with the exterior colouring frozen*: it is not a statement about
R_4 of the whole branch graph.
"""
from __future__ import annotations

from itertools import product
import json
from pathlib import Path

COLORS = range(4)


def fibre(s: int):
    """States (x,u_1,...,u_s) after deleting the independent u_i."""
    states = []
    for x in (0, 1):
        # a_i is fixed to 2.  u_i avoids x and 2.
        allowed = tuple(c for c in COLORS if c not in (x, 2))
        states.extend((x,) + us for us in product(allowed, repeat=s))
    index = {state: i for i, state in enumerate(states)}
    edges = set()
    for i, state in enumerate(states):
        x, *us = state
        # Recolour one u_i inside its binary list.
        for j, colour in enumerate(us, start=1):
            other = ({1: 3, 3: 1} if x == 0 else {0: 3, 3: 0}).get(colour)
            if other is None:
                raise AssertionError("unexpected binary list")
            nxt = list(state)
            nxt[j] = other
            edges.add(tuple(sorted((i, index[tuple(nxt)]))))
        # Recolour x.  The only legal transition is all u_i=3.
        other_x = 1 - x
        if all(colour == 3 for colour in us):
            nxt = (other_x,) + tuple(us)
            edges.add(tuple(sorted((i, index[nxt]))))
    return states, edges


def components(vertex_count, edges):
    adj = [[] for _ in range(vertex_count)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = set()
    out = []
    for root in range(vertex_count):
        if root in seen:
            continue
        seen.add(root)
        stack = [root]
        block = []
        while stack:
            v = stack.pop()
            block.append(v)
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        out.append(sorted(block))
    return out


def branch_graph(s: int):
    """Return vertices/edges of a planar girth-five branch witness.

    x has neighbours y,z,u_i; each u_i-a_i path ends in a private C5
    sharing a_i.  y,z are leaves.  This is a planar graph with cycles only
    the private pentagons, hence girth five.
    """
    vertices = ["x", "y", "z"]
    edges = [("x", "y"), ("x", "z")]
    for i in range(s):
        u, a = f"u{i+1}", f"a{i+1}"
        vertices += [u, a]
        edges += [("x", u), (u, a)]
        cycle = [a] + [f"b{i+1}", f"c{i+1}", f"d{i+1}", f"e{i+1}"]
        vertices += cycle[1:]
        edges += list(zip(cycle, cycle[1:] + cycle[:1]))
    return vertices, edges


def witness_colouring(s: int):
    """A proper colouring of H=G-{u_i} realizing the binary lists."""
    colour = {"x": 0, "y": 2, "z": 3}
    for i in range(s):
        colour[f"a{i+1}"] = 2
        for name, value in zip("bcde", (0, 1, 0, 1)):
            colour[f"{name}{i+1}"] = value
    vertices, edges = branch_graph(s)
    assert all(colour[a] != colour[b] for a, b in edges if a not in {f"u{i+1}" for i in range(s)} and b not in {f"u{i+1}" for i in range(s)})
    available_x = sorted(set(COLORS) - {colour["y"], colour["z"]})
    available_u = {x: sorted(set(COLORS) - {x, 2}) for x in (0, 1)}
    return available_x, available_u


def main():
    rows = []
    for s in range(2, 7):
        states, edges = fibre(s)
        # Remove the unique x-change edge; the two Q_s blocks remain.
        bridge = [edge for edge in edges if states[edge[0]][0] != states[edge[1]][0]]
        remainder = edges.difference(bridge)
        comps = components(len(states), remainder)
        available_x, available_u = witness_colouring(s)
        rows.append({
            "s": s,
            "states": len(states),
            "edges": len(edges),
            "bridge_edges": len(bridge),
            "bridge": [[states[a], states[b]] for a, b in bridge],
            "components_after_bridge_removal": [len(c) for c in comps],
            "component_count_after_bridge_removal": len(comps),
            "hamilton_cycle_impossible_by_bridge_cut": len(comps) == 2 and len(bridge) == 1,
            "branch_vertices": len(branch_graph(s)[0]),
            "branch_edges": len(branch_graph(s)[1]),
            "witness_available_at_x": available_x,
            "witness_available_at_u_by_x": {str(x): values for x, values in available_u.items()},
        })
    report = {
        "status": "PASS",
        "scope": "frozen local fibre only; no claim about full R4 of branch_graph",
        "construction": "x-u_i-a_i, x-y, x-z, and a private C5 through each a_i",
        "rows": rows,
    }
    print(json.dumps(report, indent=2))
    out = Path(__file__).with_name("hub-bridge-report.json")
    out.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
