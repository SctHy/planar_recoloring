#!/usr/bin/env python3
"""Local C5 list-colouring fibres for pentagons whose vertices may have degree four.

Model.  A boundary t is a 5-tuple of nonempty lists L_0,...,L_4 of colours from
Q = {0,1,2,3}.  The local fibre F(t) consists of the proper colourings x of the
5-cycle with x_i in L_i; two states are adjacent when they differ at exactly one
position.  Lists of size 3 or 4 are what the manuscript's protected-pentagon
certificates use (a cycle vertex of degree three or two).  A cycle vertex of
degree four has two exterior neighbours, so its list has size at least two; this
script measures which new fibre structures appear at that size.

All computations are exact finite-set computations.  Hamiltonicity of a fibre
component is decided by fixed-start subset dynamic programming when it has at
most DP_LIMIT states; larger components are searched with a deterministic
Warnsdorff heuristic and reported as found/unknown, so a positive result is an
explicit certificate while a negative result is only "not found".
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

Q = range(4)
ALL_LISTS = [frozenset(s) for k in range(1, 5) for s in combinations(Q, k)]
PERMS = list(permutations(Q))
DP_LIMIT = 18

GROUP = [(start, sign, perm) for start in range(5) for sign in (1, -1) for perm in PERMS]


def mask(L):
    return sum(1 << c for c in L)


def bits(m):
    return frozenset(c for c in Q if m >> c & 1)


CMAP = [{m: mask(frozenset(p[c] for c in bits(m))) for m in (mask(L) for L in ALL_LISTS)}
        for (_, _, p) in GROUP]
POS = [[(start + sign * i) % 5 for i in range(5)] for (start, sign, _) in GROUP]


def transform(masks, g):
    return tuple(CMAP[g][masks[POS[g][i]]] for i in range(5))


def canon(masks):
    return min(transform(masks, g) for g in range(len(GROUP)))


def states(masks):
    out = []
    for x in product(*[sorted(bits(m)) for m in masks]):
        if all(x[i] != x[(i + 1) % 5] for i in range(5)):
            out.append(x)
    return out


def adjacency(comp):
    S = set(comp)
    adj = {x: set() for x in comp}
    for x in comp:
        for i in range(5):
            for c in Q:
                if c == x[i]:
                    continue
                z = x[:i] + (c,) + x[i + 1:]
                if z in S:
                    adj[x].add(z)
    return adj


def components(st):
    S = set(st)
    seen = set()
    comps = []
    for x in S:
        if x in seen:
            continue
        stack = [x]
        seen.add(x)
        comp = []
        while stack:
            y = stack.pop()
            comp.append(y)
            for i in range(5):
                for c in Q:
                    if c == y[i]:
                        continue
                    z = y[:i] + (c,) + y[i + 1:]
                    if z in S and z not in seen:
                        seen.add(z)
                        stack.append(z)
        comps.append(sorted(comp))
    return comps


def has_hamilton_cycle(comp):
    """Return (True, 'exact'|'search'), (False, 'exact'), or (None, 'unknown')."""
    return find_cycle_or_path(comp, need_cycle=True)


def has_hamilton_path(comp):
    return find_cycle_or_path(comp, need_cycle=False)


def find_cycle_or_path(comp, need_cycle, cap=400000):
    """Exact subset DP for small components, pruned DFS with a step cap otherwise.

    The DFS uses only sound necessary-condition pruning, so a completed search
    returning False is an exact negative for the searched subproblem; a True is
    certified by the printed order of the search, and None means the cap was hit.
    """
    n = len(comp)
    if n == 0:
        return False, "exact"
    if n == 1:
        return (not need_cycle), "exact"
    if n == 2:
        return False, "exact"
    adj = adjacency(comp)
    if n <= DP_LIMIT:
        idx = {x: i for i, x in enumerate(comp)}
        A = [[False] * n for _ in range(n)]
        for x in comp:
            for y in adj[x]:
                A[idx[x]][idx[y]] = True
        full = (1 << n) - 1
        from functools import lru_cache

        @lru_cache(None)
        def path(m, last):
            if m == 1:
                return last == 0
            if not (m >> last & 1) or last == 0:
                return False
            prev = m ^ (1 << last)
            return any(A[last][j] and path(prev, j) for j in range(n) if prev >> j & 1)

        if not need_cycle:
            @lru_cache(None)
            def any_path(m, last):
                if m == (1 << last):
                    return True
                if not (m >> last & 1):
                    return False
                prev = m ^ (1 << last)
                return any(A[last][j] and any_path(prev, j)
                           for j in range(n) if prev >> j & 1)
            return any(any_path(full, last) for last in range(n)), "exact"
        ok = any(A[last][0] and path(full, last) for last in range(1, n))
        return ok, "exact"

    order = sorted(comp)
    # fast positive test: deterministic Warnsdorff tours from several starts
    for start in order:
        tour = [start]
        used = {start}
        while len(tour) < n:
            cur = tour[-1]
            candidates = sorted((y for y in adj[cur] if y not in used),
                                key=lambda y: sum(1 for w in adj[y] if w not in used))
            if not candidates:
                break
            used.add(candidates[0])
            tour.append(candidates[0])
        if len(tour) == n:
            if not need_cycle or start in adj[tour[-1]]:
                return True, "search"

    starts = order if not need_cycle else [min(order, key=lambda x: len(adj[x]))]
    per_start_cap = max(1, cap // len(starts))
    any_unknown = False
    for start in starts:
        steps = [0]
        verdict = [None]

        def dfs(last, used):
            if steps[0] > per_start_cap or verdict[0] is not None:
                return
            steps[0] += 1
            if len(used) == n:
                if (not need_cycle) or start in adj[last]:
                    verdict[0] = True
                return
            for y in order:
                if y not in used and y not in adj[last] and not any(w not in used for w in adj[y]):
                    return
            candidates = sorted((y for y in adj[last] if y not in used),
                                key=lambda y: sum(1 for w in adj[y] if w not in used))
            for y in candidates:
                used.add(y)
                dfs(y, used)
                used.remove(y)
                if verdict[0] is not None:
                    return

        dfs(start, {start})
        if verdict[0] is True:
            return True, "search"
        if steps[0] > per_start_cap:
            any_unknown = True
    if any_unknown:
        return None, "unknown"
    return False, "search"


def cut_vertex_count(comp):
    """Number of components that are not 2-connected; a cut vertex certifies no Hamilton cycle."""
    if len(comp) < 3:
        return len(comp)
    adj = adjacency(comp)
    S = set(comp)
    found = 0
    for v in comp:
        rest = S - {v}
        start = next(iter(rest))
        seen = {start}
        stack = [start]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y != v and y not in seen:
                    seen.add(y)
                    stack.append(y)
        if seen != rest:
            found += 1
    return found


def profile(masks):
    st = states(masks)
    comps = components(st)
    cycles = [has_hamilton_cycle(c) for c in comps]
    paths = [has_hamilton_path(c) for c in comps]
    return {
        "list_sizes": [bin(m).count("1") for m in masks],
        "states": len(st),
        "components": len(comps),
        "component_sizes": [len(c) for c in comps],
        "singleton_components": sum(1 for c in comps if len(c) == 1),
        "two_state_components": sum(1 for c in comps if len(c) == 2),
        "hamiltonian_components": sum(1 for v, _ in cycles if v is True),
        "component_cycle_verdicts": [str(v) for v, _ in cycles],
        "component_cycle_modes": [m for _, m in cycles],
        "component_path_verdicts": [str(v) for v, _ in paths],
        "all_components_hamiltonian": (all(v is True for v, _ in cycles) if comps else None),
        "all_components_traceable": (all(v is True for v, _ in paths) if comps else None),
        "cut_vertex_components": sum(1 for c in comps if cut_vertex_count(c)),
        "covers_empty": len(st) == 0,
    }


def orbit_classes(boundaries):
    orbits = {}
    for t in boundaries:
        orbits.setdefault(canon(t), []).append(t)
    return orbits


def common_states(a, b):
    return sorted(set(states(a)) & set(states(b)))


def component_hits(st, comps):
    """Number of components of `comps` that contain at least one state of st."""
    S = set(st)
    return sum(1 for c in comps if S & set(c))


def report_of(name, boundaries, max_problem=40):
    orbits = orbit_classes(boundaries)
    hist = Counter()
    problems = []
    empty_orbits = single_orbits = many_orbits = 0
    no_cycle_orbits = no_path_orbits = unknown_orbits = 0
    empty_labelled = single_labelled = many_labelled = 0
    no_cycle_labelled = 0
    total_states = 0
    for c, members in orbits.items():
        info = profile(c)
        total_states += info["states"] * len(members)
        hist[(info["components"], info["singleton_components"],
              tuple(info["component_sizes"]))] += len(members)
        no_cycle = any(v == "False" for v in info["component_cycle_verdicts"])
        no_path = any(v == "False" for v in info["component_path_verdicts"])
        unknown = any(v == "None" for v in info["component_cycle_verdicts"])
        if info["covers_empty"]:
            empty_orbits += 1
            empty_labelled += len(members)
        if info["singleton_components"]:
            single_orbits += 1
            single_labelled += len(members)
        if info["components"] > 2:
            many_orbits += 1
            many_labelled += len(members)
        if no_cycle:
            no_cycle_orbits += 1
            no_cycle_labelled += len(members)
        if no_path:
            no_path_orbits += 1
        if unknown:
            unknown_orbits += 1
        if info["covers_empty"] or info["singleton_components"] or info["components"] > 2 \
                or no_cycle or no_path or unknown:
            problems.append({**info, "boundary": [sorted(bits(m)) for m in c],
                             "orbit_size": len(members),
                             "has_no_cycle_component": no_cycle,
                             "has_no_path_component": no_path,
                             "has_unresolved_component": unknown})
    return {
        "name": name,
        "boundaries_labelled": len(boundaries),
        "orbits_under_D5xS4": len(orbits),
        "total_states_labelled": total_states,
        "histogram_components_singletons_sizes": {str(k): v for k, v in sorted(hist.items())},
        "problem_orbit_count": len(problems),
        "empty_fibre_orbits": empty_orbits,
        "empty_fibre_labelled_boundaries": empty_labelled,
        "singleton_orbits": single_orbits,
        "singleton_labelled_boundaries": single_labelled,
        "more_than_two_components_orbits": many_orbits,
        "more_than_two_components_labelled_boundaries": many_labelled,
        "no_cycle_component_orbits": no_cycle_orbits,
        "no_cycle_component_labelled_boundaries": no_cycle_labelled,
        "no_cycle_cutvertex_certified_orbits": sum(
            1 for p in problems if p["has_no_cycle_component"] and p["cut_vertex_components"]),
        "no_cycle_without_cutvertex_orbits": sum(
            1 for p in problems if p["has_no_cycle_component"] and not p["cut_vertex_components"]),
        "no_path_component_orbits": no_path_orbits,
        "unresolved_component_orbits": unknown_orbits,
        "problem_orbits_sample": sorted(problems, key=lambda d: (d["states"], d["boundary"]))[:max_problem],
    }


def main():
    stats = {
        "model": "proper C5 colourings over five colour lists; single-vertex moves",
        "palette": [0, 1, 2, 3],
        "scope": {
            "exact": f"all fibre enumeration and components; Hamiltonianicity exact for components of <= {DP_LIMIT} states",
            "boundary": "large components: deterministic Warnsdorff search; True is a certificate, None means not found",
        },
        "regression_existing_lists_size_ge3": report_of(
            "lists of size 3 or 4",
            [t for t in product([mask(L) for L in ALL_LISTS if len(L) >= 3], repeat=5)]),
    }
    # build class one-2-four-3 explicitly
    two = [mask(L) for L in ALL_LISTS if len(L) == 2]
    three = [mask(L) for L in ALL_LISTS if len(L) == 3]
    classA = []
    for pos in range(5):
        for A in two:
            for rest in product(three, repeat=4):
                it = iter(rest)
                classA.append(tuple(A if i == pos else next(it) for i in range(5)))
    stats["class_one_2_four_3"] = report_of("one list of size 2, four lists of size 3", classA)

    # all patterns of lists of size 2 or 3 (100000 labelled boundaries)
    class23 = list(product(two + three, repeat=5))
    stats["class_lists_size_2_or_3"] = report_of("lists of size 2 or 3", class23, max_problem=100)

    # the face of a degree-four vertex: exactly one list of size 2, others 3 or 4
    four = [mask(L) for L in ALL_LISTS if len(L) == 4]
    class_face4 = []
    for pos in range(5):
        for A in two:
            for rest in product(three + four, repeat=4):
                it = iter(rest)
                class_face4.append(tuple(A if i == pos else next(it) for i in range(5)))
    stats["class_face_of_degree4"] = report_of(
        "one list of size 2, the other four of size 3 or 4", class_face4)

    # every boundary whose lists have size 2, 3 or 4 and at least one of size 2
    ge2 = [mask(L) for L in ALL_LISTS if len(L) >= 2]
    class_all = [t for t in product(ge2, repeat=5) if any(bin(m).count("1") == 2 for m in t)]
    stats["class_ge2_at_least_one_2"] = report_of(
        "lists of size 2, 3 or 4 with at least one 2 (pentagon vertices of degree at most 4)",
        class_all, max_problem=60)
    # secondary: one list of size 1 (a degree-five cycle vertex) and four of size 3
    one = [mask(L) for L in ALL_LISTS if len(L) == 1]
    class_one1 = []
    for pos in range(5):
        for A in one:
            for rest in product(three, repeat=4):
                it = iter(rest)
                class_one1.append(tuple(A if i == pos else next(it) for i in range(5)))
    stats["class_one_1_four_3"] = report_of(
        "one list of size 1 (degree-five cycle vertex) and four of size 3", class_one1, max_problem=20)

    # interface probe on the smallest problem type: a singleton component
    probe = None
    for problem in stats["class_one_2_four_3"]["problem_orbits_sample"]:
        if not problem["singleton_components"]:
            continue
        boundary = tuple(mask(frozenset(s)) for s in problem["boundary"])
        comps = components(states(boundary))
        singleton = next(c[0] for c in comps if len(c) == 1)
        moves = []
        for j in range(5):
            for other in (m for m in (mask(L) for L in ALL_LISTS) if m != boundary[j]):
                changed = list(boundary)
                changed[j] = other
                changed = tuple(changed)
                inter = common_states(boundary, changed)
                moves.append({
                    "position": j,
                    "new_list": sorted(bits(other)),
                    "common_states": len(inter),
                    "singleton_in_common": singleton in inter,
                    "common_hits_components": component_hits(inter, comps),
                })
        probe = {"boundary": problem["boundary"],
                 "states": problem["states"],
                 "component_sizes": problem["component_sizes"],
                 "singleton_state": singleton,
                 "one_list_moves": moves}
        break
    stats["singleton_interface_probe"] = probe

    Path("pentagon-boundary-report.json").write_text(
        json.dumps(stats, indent=1, sort_keys=True) + "\n")
    for key in ("regression_existing_lists_size_ge3", "class_one_2_four_3",
                "class_lists_size_2_or_3", "class_face_of_degree4",
                "class_ge2_at_least_one_2", "class_one_1_four_3"):
        d = stats[key]
        print(key, {k: d[k] for k in ("boundaries_labelled", "orbits_under_D5xS4",
                                      "problem_orbit_count", "empty_fibre_orbits",
                                      "singleton_orbits", "no_cycle_component_orbits",
                                      "no_path_component_orbits",
                                      "unresolved_component_orbits")})
        print("  histogram:", list(d["histogram_components_singletons_sizes"].items())[:8])
    print("probe:", "none" if probe is None else
          (probe["boundary"], probe["component_sizes"], probe["singleton_state"]))
    print("wrote pentagon-boundary-report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
