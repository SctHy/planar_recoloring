#!/usr/bin/env python3
"""Write a deleted configuration X for fibre_classifier.c.

Format: "n m P", then m edges of G[X], then P port lines "k x_1 .. x_k" (the
X-neighbours of one outside vertex).  Every listed vertex has G-degree 3 unless
stated; a vertex of G-degree d gets d - deg_X(v) private ports.
Usage: python3 fibre_configs.py NAME
"""
import sys


def faces_config(faces, degree):
    verts = sorted({v for f in faces for v in f}, key=str)
    idx = {v: i for i, v in enumerate(verts)}
    edges = sorted({tuple(sorted((idx[f[i]], idx[f[(i + 1) % len(f)]]))) for f in faces for i in range(len(f))})
    deg_x = [0] * len(verts)
    for a, b in edges:
        deg_x[a] += 1
        deg_x[b] += 1
    ports = [[idx[v]] for v in verts for _ in range(degree.get(v, 3) - deg_x[idx[v]])]
    lines = [f"{len(verts)} {len(edges)} {len(ports)}"] + [f"{a} {b}" for a, b in edges]
    lines += [" ".join(map(str, [len(p)] + p)) for p in ports]
    return "\n".join(lines) + "\n"


def petals(centre, k, closed):
    last = k if closed else k - 1
    return [[centre, f"u{i}", f"z{i}", f"y{i}", f"u{i % k + 1 if closed else i + 1}"] for i in range(1, last + 1)]


CONFIGS = {
    "pentagon": ([[0, 1, 2, 3, 4]], {}),
    "bowtie": ([[0, 1, 2, 3, 4], [0, 5, 6, 7, 8]], {0: 4}),
    "bowtie_heavy_neighbour": ([[0, 1, 2, 3, 4], [0, 5, 6, 7, 8]], {0: 4, 5: 4}),
    "bowtie_heavy_far": ([[0, 1, 2, 3, 4], [0, 5, 6, 7, 8]], {0: 4, 6: 4}),
    # three faces in a chain; on the middle face the junctions are at distance two / adjacent
    "chain3_distance2": ([["j1", "a1", "a2", "a3", "a4"], ["j1", "b1", "j2", "b3", "b4"],
                          ["j2", "c1", "c2", "c3", "c4"]], {"j1": 4, "j2": 4}),
    "chain3_adjacent": ([["j1", "a1", "a2", "a3", "a4"], ["j1", "j2", "b2", "b3", "b4"],
                         ["j2", "c1", "c2", "c3", "c4"]], {"j1": 4, "j2": 4}),
    "PI_flower": (petals("v", 4, True), {"v": 4}),
    "C3": (petals("v", 5, False)[:4], {"v": 5}),
}

if __name__ == "__main__":
    faces, degree = CONFIGS[sys.argv[1]]
    sys.stdout.write(faces_config(faces, degree))
