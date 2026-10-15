#!/usr/bin/env python3
"""Standard-library checks for the 2026-10-15 girth-five checkpoint.

Scope: finite local facts and small exhaustive checks.  Nothing here proves or
refutes h(P_5)=4.

1. Pinch facts used in the analytic move bound: every proper 4-colouring of C_5
   has a vertex whose two cycle neighbours agree; a cyclic sequence of length d
   with s>=2 distinct values has at most d-s equal consecutive pairs; the
   resulting per-vertex defect table; exact minimum move counts for C_5..C_9.
2. The unavoidable configurations C1/C2/C3 in the dodecahedron, PI and PH.
3. Exact fibre classification over all boundary words (canonical under colour
   permutation) for the subcubic pentagon, the apex 5-cycle, the bowtie and the
   bowtie with one heavy vertex on the opposite face.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from itertools import product
from pathlib import Path

sys.dont_write_bytecode = True  # the PI/PH import must not leave a __pycache__
HERE = Path(__file__).resolve().parent
COLOURS = range(4)


# ---------------------------------------------------------------- 1. pinches
def every_c5_colouring_has_pinch():
    count = 0
    for c in product(COLOURS, repeat=5):
        if any(c[i] == c[(i + 1) % 5] for i in range(5)):
            continue
        count += 1
        if not any(c[i - 1] == c[(i + 1) % 5] for i in range(5)):
            return False, count
    return True, count


def cyclic_equal_pairs_bound(max_d=8):
    for d in range(2, max_d + 1):
        for seq in product(COLOURS, repeat=d):
            s = len(set(seq))
            eq = sum(seq[i] == seq[(i + 1) % d] for i in range(d))
            if s >= 2 and eq > d - s:
                return False, d
    return True, max_d


def defect_table(max_d=8):
    """Largest possible defect 6-2d+p(v) against the move count m=3-s."""
    rows = []
    ok2 = ok15 = True
    for d in range(1, max_d + 1):
        for s in range(1, min(d, 3) + 1):
            m = 3 - s
            if d == 1:
                p = 0  # a leaf lies on no 5-cycle
            elif s == 1:
                p = d
            else:
                p = d - s
            defect = 6 - 2 * d + p
            ok2 &= defect <= 2 * m
            if d >= 3:
                ok15 &= 2 * defect <= 3 * m
            rows.append({"degree": d, "colours_seen": s, "moves": m, "max_defect": defect})
    return rows, ok2, ok15


def cycle_min_moves(n):
    best = None
    for c in product(COLOURS, repeat=n - 1):
        c = (0,) + c
        if any(c[i] == c[(i + 1) % n] for i in range(n)):
            continue
        moves = sum(3 - len({c[i - 1], c[(i + 1) % n]}) for i in range(n))
        best = moves if best is None else min(best, moves)
    return best


# ------------------------------------------------- 2. unavoidable C1/C2/C3
def dodecahedron():
    """Plane dodecahedron: outer pentagon, 10-ring, inner pentagon."""
    adj = {v: set() for v in range(20)}

    def edge(a, b):
        adj[a].add(b)
        adj[b].add(a)

    for i in range(5):
        edge(i, (i + 1) % 5)
        edge(i, 5 + 2 * i)
        edge(5 + 2 * i + 1, 15 + i)
        edge(15 + i, 15 + (i + 1) % 5)
    for j in range(10):
        edge(5 + j, 5 + (j + 1) % 10)
    faces = []
    for a in range(20):
        for b in adj[a]:
            for c in adj[b] - {a}:
                for d in adj[c] - {a, b}:
                    for e in adj[d] - {a, b, c}:
                        if a in adj[e] and a == min((a, b, c, d, e)):
                            faces.append(frozenset((a, b, c, d, e)))
    faces = sorted(set(faces), key=sorted)
    assert len(faces) == 12 and all(len(adj[v]) == 3 for v in adj)
    return adj, [sorted(f) for f in faces]


def load_snub():
    path = HERE.parent / "girth5-apex-pentagon-20261014" / "apex_pentagon_scan.py"
    spec = importlib.util.spec_from_file_location("apex_pentagon_scan", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.snub_dual


def configurations(adj, faces):
    deg = {v: len(adj[v]) for v in adj}
    faces = [frozenset(f) for f in faces if len(f) == 5]
    c1 = sum(all(deg[v] == 3 for v in f) for f in faces)
    c2 = c3 = 0
    for u in adj:
        at_u = [f for f in faces if u in f]
        light = [f for f in at_u if all(deg[v] == 3 for v in f - {u})]
        if deg[u] == 4:
            c2 += sum(any(F & g == {u} for F in at_u) for g in light)
        if deg[u] == 5 and len(light) >= 4:
            c3 += 1
    return {"C1_faces": c1, "C2_apex_faces": c2, "C3_vertices": c3}


# ---------------------------------------------------------- 3. fibres
def canonical_words(P):
    for w in product(COLOURS, repeat=P):
        top, ok = -1, True
        for x in w:
            if x > top + 1:
                ok = False
                break
            top = max(top, x)
        if ok:
            yield w


def classify(n, edges, ports, witness=False):
    """ports[p] = tuple of X-vertices adjacent to outside vertex p."""
    nbrs = [[] for _ in range(n)]
    for a, b in edges:
        nbrs[a].append(b)
        nbrs[b].append(a)
    rows = {"canonical_words": 0, "empty": 0, "disconnected": 0, "with_isolated_state": 0,
            "components_killable_twice": 0, "components_killable_once": 0,
            "min_component": None, "max_fibre": 0}
    example = None
    for w in canonical_words(len(ports)):
        rows["canonical_words"] += 1
        allowed = [set(COLOURS) for _ in range(n)]
        for p, xs in enumerate(ports):
            for x in xs:
                allowed[x].discard(w[p])
        states = [()]
        for v in range(n):
            states = [s + (c,) for s in states for c in allowed[v]
                      if all(s[u] != c for u in nbrs[v] if u < v)]
        if not states:
            rows["empty"] += 1
            continue
        rows["max_fibre"] = max(rows["max_fibre"], len(states))
        index = set(states)
        seen = set()
        comps = 0
        for root in states:
            if root in seen:
                continue
            comps += 1
            seen.add(root)
            stack, size, isolated = [root], 0, False
            colours = [set() for _ in range(n)]
            kill = [set(COLOURS) - {w[p]} for p in range(len(ports))]
            while stack:
                s = stack.pop()
                size += 1
                for v in range(n):
                    colours[v].add(s[v])
                for p, xs in enumerate(ports):
                    kill[p] &= {s[x] for x in xs}
                degree = 0
                for v in range(n):
                    for c in allowed[v]:
                        if c != s[v] and all(s[u] != c for u in nbrs[v]):
                            degree += 1
                            t = s[:v] + (c,) + s[v + 1:]
                            if t in index and t not in seen:
                                seen.add(t)
                                stack.append(t)
                isolated |= degree == 0
            kills = sum(len(k) for k in kill)
            if kills >= 2:
                rows["components_killable_twice"] += 1
                if witness and example is None:
                    example = {"word": list(w), "component_size": size, "killing_moves": kills,
                               "state": list(root) if size == 1 else None}
            elif kills == 1:
                rows["components_killable_once"] += 1
            if rows["min_component"] is None or size < rows["min_component"]:
                rows["min_component"] = size
            if isolated:
                rows["with_isolated_state"] += 1
        rows["disconnected"] += comps > 1
    if witness:
        rows["first_doubly_killable_component"] = example
    return rows


def face_union(faces, heavy=()):
    """Vertices of the listed 5-cycles; each vertex of G-degree d gets d-deg_X ports."""
    verts = sorted({v for f in faces for v in f})
    idx = {v: i for i, v in enumerate(verts)}
    edges = sorted({tuple(sorted((idx[f[i]], idx[f[(i + 1) % 5]]))) for f in faces for i in range(5)})
    deg_x = [0] * len(verts)
    for a, b in edges:
        deg_x[a] += 1
        deg_x[b] += 1
    degree = {v: 3 for v in verts}
    for v, d in heavy:
        degree[v] = d
    ports = [(idx[v],) for v in verts for _ in range(degree[v] - deg_x[idx[v]])]
    return len(verts), edges, ports


def main():
    report = {"status": "PASS",
              "scope": "finite local checks; no claim about Hamiltonicity of any full R_4(G)"}
    ok, count = every_c5_colouring_has_pinch()
    bound_ok, dmax = cyclic_equal_pairs_bound()
    rows, ok2, ok15 = defect_table()
    report["pinch"] = {
        "every_proper_C5_4colouring_has_pinch": ok, "C5_colourings": count,
        "equal_pairs_at_most_d_minus_s": bound_ok, "checked_up_to_degree": dmax,
        "defect_at_most_2m": ok2, "defect_at_most_1.5m_for_degree_ge_3": ok15,
        "defect_table": rows,
        "cycle_min_moves": {str(n): cycle_min_moves(n) for n in range(5, 10)},
    }
    snub_dual = load_snub()
    dod_adj, dod_faces = dodecahedron()
    report["unavoidable"] = {"dodecahedron": configurations(dod_adj, dod_faces)}
    for name, k in (("PI", 4), ("PH", 5)):
        adj, faces = snub_dual(k)
        report["unavoidable"][name] = configurations(adj, faces)
    g = [0, 1, 2, 3, 4]
    F = [0, 5, 6, 7, 8]
    report["fibres"] = {
        "subcubic_pentagon": classify(5, [(i, (i + 1) % 5) for i in range(5)], [(i,) for i in range(5)]),
        "apex_5cycle_degree4": classify(5, [(i, (i + 1) % 5) for i in range(5)],
                                        [(1,), (2,), (3,), (4,), (0,), (0,)], witness=True),
        "bowtie": classify(*face_union([g, F], heavy=[(0, 4)])),
        "bowtie_heavy_neighbour_on_F": classify(*face_union([g, F], heavy=[(0, 4), (5, 4)]), witness=True),
        "bowtie_heavy_far_vertex_on_F": classify(*face_union([g, F], heavy=[(0, 4), (6, 4)]), witness=True),
    }
    f = report["fibres"]
    checks = [ok, bound_ok, ok2, ok15, report["pinch"]["cycle_min_moves"]["5"] == 6,
              report["unavoidable"]["dodecahedron"]["C1_faces"] == 12,
              report["unavoidable"]["PI"]["C2_apex_faces"] == 24,
              report["unavoidable"]["PH"]["C3_vertices"] == 12,
              f["subcubic_pentagon"]["disconnected"] == 1 and f["subcubic_pentagon"]["components_killable_once"] == 0,
              f["apex_5cycle_degree4"]["components_killable_twice"] > 0,
              f["bowtie"]["disconnected"] == 0 and f["bowtie"]["components_killable_once"] == 0
              and f["bowtie"]["components_killable_twice"] == 0 and f["bowtie"]["empty"] == 0,
              f["bowtie_heavy_neighbour_on_F"]["components_killable_twice"] > 0,
              f["bowtie_heavy_far_vertex_on_F"]["components_killable_twice"] > 0]
    if not all(checks):
        report["status"] = "FAIL"
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    (HERE / "pinch-tree-report.json").write_text(text)
    print(text)
    assert report["status"] == "PASS"


if __name__ == "__main__":
    main()
