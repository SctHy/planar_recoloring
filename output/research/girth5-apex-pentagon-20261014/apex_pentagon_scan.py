#!/usr/bin/env python3
"""Exploratory standard-library checks for the girth-five four-colour frontier.

Scope: finite local facts only.  Nothing here proves or refutes h(P_5)=4.

1. Builds the pentagonal icositetrahedron (PI) and pentagonal hexecontahedron
   (PH) as duals of the snub cube / snub dodecahedron, given as Cayley maps of
   the rotation groups S_4 and A_5.  Checks the sphere map, degrees, girth five,
   and that every face has four degree-3 vertices and one apex of degree 4 / 5.
2. For an apex pentagon x_1..x_4 (degree three) with apex v, classifies the
   local fibres for deleting {x_1..x_4} (path lists) and the whole 5-cycle
   (apex list of size two), over all labelled boundary words.
3. In PI, finds a colouring of the deleted graph whose fibre has an isolated
   local state and two legal bottom recolourings that each delete that state.
4. Checks the K_5-minus-an-edge fact used for the no-locked-flower remark.
"""
from __future__ import annotations

from itertools import permutations, product
import json
from pathlib import Path

COLOURS = range(4)


def mul(p, q):
    return tuple(p[i] for i in q)


def inv(p):
    r = [0] * len(p)
    for i, x in enumerate(p):
        r[x] = i
    return tuple(r)


def order(p):
    e = tuple(range(len(p)))
    q, k = p, 1
    while q != e:
        q, k = mul(q, p), k + 1
    return k


def even(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2 == 0


def snub_dual(n):
    """Dual of the snub map Cay(G; a, b, ab), a of order n, b of order 3."""
    m = 4 if n == 4 else 5
    elems = [p for p in permutations(range(m)) if m == 4 or even(p)]
    a = tuple(list(range(1, m)) + [0]) if n == m else None
    assert a is not None and order(a) == n
    b = next(b for b in elems if order(b) == 3 and order(mul(a, b)) == 2)
    ab = mul(a, b)
    gens = {a, inv(a), b, inv(b), ab}
    group = {tuple(range(m))}
    frontier = list(group)
    while frontier:
        nxt = []
        for g in frontier:
            for s in gens:
                h = mul(g, s)
                if h not in group:
                    group.add(h)
                    nxt.append(h)
        frontier = nxt
    group = sorted(group)
    assert len(group) == (24 if n == 4 else 60)
    edges = {frozenset((g, mul(g, s))) for g in group for s in gens}
    faces = set()
    for g in group:
        faces.add(frozenset(mul(g, x) for x in (tuple(range(m)), a, mul(a, a), mul(mul(a, a), a), mul(mul(mul(a, a), a), a))[:n]))
        faces.add(frozenset((g, mul(g, b), mul(g, inv(b)))))
        faces.add(frozenset((g, mul(g, a), mul(g, ab))))
    faces = sorted(faces, key=lambda f: sorted(f))
    # Sphere-map checks: every edge in two faces, every vertex link one cycle, Euler 2.
    for e in edges:
        assert sum(e <= f for f in faces) == 2
    for g in group:
        around = [i for i, f in enumerate(faces) if g in f]
        adj = {i: [j for j in around if j != i and len(faces[i] & faces[j] - {g}) == 1
                   and frozenset(faces[i] & faces[j]) in edges] for i in around}
        assert all(len(v) == 2 for v in adj.values())
        seen, cur, prev = [around[0]], around[0], None
        while True:
            nxt = [j for j in adj[cur] if j != prev][0]
            if nxt == around[0]:
                break
            seen.append(nxt)
            prev, cur = cur, nxt
        assert len(seen) == len(around) == 5
    assert len(group) - len(edges) + len(faces) == 2
    dual = {i: set() for i in range(len(faces))}
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            if frozenset(faces[i] & faces[j]) in edges and len(faces[i] & faces[j]) == 2:
                dual[i].add(j)
                dual[j].add(i)
    # Dual faces: the five snub faces around each group element, in cyclic order.
    dual_faces = []
    for g in group:
        around = [i for i, f in enumerate(faces) if g in f]
        cyc, prev = [around[0]], None
        while len(cyc) < 5:
            cur = cyc[-1]
            nxt = [j for j in around if j in dual[cur] and j != prev and j not in cyc][0]
            prev = cur
            cyc.append(nxt)
        dual_faces.append(cyc)
    return dual, dual_faces


def girth(adj):
    best = 10**9
    for r in adj:
        dist, par, queue = {r: 0}, {r: None}, [r]
        for x in queue:
            for y in adj[x]:
                if y not in dist:
                    dist[y], par[y] = dist[x] + 1, x
                    queue.append(y)
                elif par[x] != y:
                    best = min(best, dist[x] + dist[y] + 1)
    return best


def fibre(lists, cyclic):
    n = len(lists)
    pairs = [(i, (i + 1) % n) for i in range(n if cyclic else n - 1)]
    states = [s for s in product(*[sorted(x) for x in lists]) if all(s[i] != s[j] for i, j in pairs)]
    index = {s: i for i, s in enumerate(states)}
    adj = [[] for _ in states]
    for i, s in enumerate(states):
        for p in range(n):
            for c in lists[p]:
                if c != s[p]:
                    t = s[:p] + (c,) + s[p + 1:]
                    if t in index:
                        adj[i].append(index[t])
    return states, adj


def components(adj):
    seen, out = set(), []
    for r in range(len(adj)):
        if r in seen:
            continue
        seen.add(r)
        stack, comp = [r], 0
        while stack:
            v = stack.pop()
            comp += 1
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        out.append(comp)
    return out


def apex_lists(word, whole):
    """word = (v, y1, y2, y3, y4) for the path; (z1, z2, y1, ..., y4) for the 5-cycle."""
    if whole:
        z1, z2, y1, y2, y3, y4 = word
        return [set(COLOURS) - {z1, z2}] + [set(COLOURS) - {y} for y in (y1, y2, y3, y4)]
    v, y1, y2, y3, y4 = word
    return [set(COLOURS) - {v, y1}, set(COLOURS) - {y2}, set(COLOURS) - {y3}, set(COLOURS) - {v, y4}]


def classify(whole):
    rows = {"boundary_words": 0, "disconnected": 0, "isolated_state": 0, "local_degree_at_most_one": 0}
    for word in product(COLOURS, repeat=6 if whole else 5):
        states, adj = fibre(apex_lists(word, whole), whole)
        if not states:
            continue
        rows["boundary_words"] += 1
        rows["disconnected"] += len(components(adj)) > 1
        rows["isolated_state"] += any(not a for a in adj)
        rows["local_degree_at_most_one"] += min(map(len, adj)) <= 1
    return rows


def colour_extension(adj, fixed):
    order_ = sorted(adj, key=lambda v: (v not in fixed, -len(adj[v])))
    col = dict(fixed)

    def rec(i):
        if i == len(order_):
            return True
        v = order_[i]
        if v in fixed:
            return all(col.get(w) != col[v] for w in adj[v]) and rec(i + 1)
        for c in COLOURS:
            if all(col.get(w) != c for w in adj[v]):
                col[v] = c
                if rec(i + 1):
                    return True
                del col[v]
        return False

    return dict(col) if rec(0) else None


def isolated_witness(adj, face, whole):
    apex = next(i for i, x in enumerate(face) if len(adj[x]) >= 4)
    face = face[apex:] + face[:apex]
    X = face if whole else face[1:]
    H = {v: adj[v] - set(X) for v in adj if v not in X}
    boundary = sorted({w for x in X for w in adj[x] if w not in X})
    for word in product(COLOURS, repeat=len(boundary)):
        fixed = dict(zip(boundary, word))
        if any(fixed[a] == fixed[b] for a in boundary for b in H[a] if b in fixed):
            continue
        lists = [set(COLOURS) - {fixed[w] for w in adj[x] if w not in X} for x in X]
        states, fadj = fibre(lists, whole)
        isolated = [states[i] for i, a in enumerate(fadj) if not a]
        if not isolated:
            continue
        col = colour_extension(H, fixed)
        if col is None:
            continue
        for s in isolated:
            killers = sorted({(w, col[w], c) for x, c in zip(X, s) for w in adj[x] if w not in X
                              and c != col[w] and all(col[z] != c for z in H[w])})
            if len(killers) >= 2:
                return {"deleted": X, "apex_position": 0 if whole else None,
                        "boundary_colours": {str(b): fixed[b] for b in boundary},
                        "lists": ["".join(map(str, sorted(x))) for x in lists],
                        "isolated_local_state": list(s),
                        "killing_bottom_moves": [list(k) for k in killers],
                        "bottom_colouring_is_proper": all(col[a] != col[b] for a in H for b in H[a])}
    return None


def k5_minus_edge_fact():
    """Proper 4-colourings of v,a,p,q,a' with all pentagram pairs distinct except (a,a')."""
    count = 0
    for v, a, p, q, a2 in product(COLOURS, repeat=5):
        cyc = [v, a, p, q, a2]
        if any(cyc[i] == cyc[(i + 1) % 5] for i in range(5)):
            continue
        if v == p or a == q or p == a2 or q == v:
            continue
        count += 1
        if a != a2:
            return False, count
    return True, count


def main():
    report = {"status": "PASS", "scope": "finite local exploration; no claim about Hamiltonicity of any full R_4(G)"}
    for name, n in (("PI", 4), ("PH", 5)):
        adj, faces = snub_dual(n)
        degrees = {}
        for v in adj:
            degrees[len(adj[v])] = degrees.get(len(adj[v]), 0) + 1
        face_types = {tuple(sorted(len(adj[x]) for x in f)) for f in faces}
        report[name] = {"vertices": len(adj), "edges": sum(map(len, adj.values())) // 2,
                        "degree_counts": {str(k): v for k, v in sorted(degrees.items())},
                        "girth": girth(adj), "five_faces": len(faces),
                        "face_degree_types": [list(t) for t in sorted(face_types)],
                        "has_all_degree_three_five_face": any(all(len(adj[x]) == 3 for x in f) for f in faces)}
        if name == "PI":
            report["PI_witness_path_deletion"] = isolated_witness(adj, faces[0], False)
            report["PI_witness_cycle_deletion"] = isolated_witness(adj, faces[0], True)
    report["apex_path_fibres"] = classify(False)
    report["apex_cycle_fibres_degree_four_apex"] = classify(True)
    ok, count = k5_minus_edge_fact()
    report["flower_lock_fact"] = {"forced_equal_spokes": ok, "colourings_checked": count}
    assert report["PI"]["girth"] == report["PH"]["girth"] == 5
    assert not report["PI"]["has_all_degree_three_five_face"]
    assert not report["PH"]["has_all_degree_three_five_face"]
    assert report["PI_witness_path_deletion"] and report["PI_witness_cycle_deletion"] and ok
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    Path(__file__).with_name("apex-pentagon-report.json").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
