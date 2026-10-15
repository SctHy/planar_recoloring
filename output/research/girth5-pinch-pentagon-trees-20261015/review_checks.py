#!/usr/bin/env python3
"""Independent small checks of the scope corrections in review.md.

Standard library only. No original classifier is imported. These finite checks
do not establish Hamiltonicity or resolve h(P_5).
"""
from collections import Counter, deque
from itertools import product
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
COLOURS = range(4)


def components(states):
    """BFS in the single-coordinate recolouring graph."""
    unseen = set(states)
    result = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue, component = deque([start]), []
        while queue:
            state = queue.popleft()
            component.append(state)
            for v in range(len(state)):
                for colour in COLOURS:
                    other = state[:v] + (colour,) + state[v + 1:]
                    if other in unseen:
                        unseen.remove(other)
                        queue.append(other)
        result.append(component)
    return result


def small_fibres():
    cycle = [s for s in product(range(1, 4), repeat=5)
             if all(s[i] != s[(i + 1) % 5] for i in range(5))]
    sizes = sorted(map(len, components(cycle)))
    assert sizes == [15, 15]
    boundary, leaves = (3, 0, 0, 2), []
    for junction in COLOURS:
        states = [s for s in product(COLOURS, repeat=4)
                  if all(s[i] != boundary[i] for i in range(4))
                  and s[0] != junction and s[3] != junction
                  and all(s[i] != s[i + 1] for i in range(3))]
        parts = components(states)
        leaves.append({"junction_colour": junction, "states": len(states),
                       "component_sizes": sorted(map(len, parts)),
                       "isolated_states": sorted(c[0] for c in parts if len(c) == 1)})
    assert [row["states"] for row in leaves] == [11, 17, 23, 23]
    assert leaves[0]["isolated_states"] == [(1, 2, 3, 1)]
    return {"constant_C1": {"boundary": [0] * 5, "states": len(cycle),
                             "component_sizes": sizes},
            "leaf_path": {"outside_colours": boundary, "fibres": leaves}}


def adjacency(faces):
    graph = {}
    for face in faces:
        for a, b in zip(face, face[1:] + face[:1]):
            assert a != b
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)
    return graph


def girth(graph):
    best = len(graph) + 1
    for root in graph:
        distance, parent, queue = {root: 0}, {root: None}, deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbour in graph[vertex]:
                if neighbour not in distance:
                    distance[neighbour] = distance[vertex] + 1
                    parent[neighbour] = vertex
                    queue.append(neighbour)
                elif parent[vertex] != neighbour:
                    best = min(best, distance[vertex] + distance[neighbour] + 1)
    return best if best <= len(graph) else None


def plane_map(faces):
    """Check a connected orientable map with one rotation at every vertex."""
    graph, darts, rotations = adjacency(faces), set(), {}
    for face in faces:
        for i, vertex in enumerate(face):
            before, after = face[i - 1], face[(i + 1) % len(face)]
            assert (vertex, after) not in darts
            darts.add((vertex, after))
            rotation = rotations.setdefault(vertex, {})
            assert before not in rotation
            rotation[before] = after
    assert all((b, a) in darts for a, b in darts)
    for vertex, neighbours in graph.items():
        rotation = rotations[vertex]
        assert set(rotation) == set(rotation.values()) == neighbours
        current, visited = min(neighbours), set()
        while current not in visited:
            visited.add(current)
            current = rotation[current]
        assert visited == neighbours
    visited, queue = set(), deque([next(iter(graph))])
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    assert len(visited) == len(graph)
    edges = len(darts) // 2
    assert len(graph) - edges + len(faces) == 2
    assert girth(graph) == 5
    return {"vertices": len(graph), "edges": edges, "faces": len(faces),
            "face_lengths": sorted(map(len, faces)), "euler_characteristic": 2,
            "girth": 5, "connected": True, "unique_reversed_darts": True,
            "single_vertex_rotations": True,
            "degree_counts": dict(sorted(Counter(map(len, graph.values())).items()))}


def opposite_corners(faces, first, second, junction):
    graph = adjacency(faces)
    pairs = []
    for index in (first, second):
        face = faces[index]
        assert face.count(junction) == 1
        position = face.index(junction)
        pairs.append((face[position - 1], face[(position + 1) % len(face)]))
    assert len(graph[junction]) == 4
    assert set(pairs[0]).isdisjoint(pairs[1])
    assert set(pairs[0] + pairs[1]) == graph[junction]
    return {"junction": junction, "face_indices": [first, second],
            "corner_pairs": pairs, "opposite": True}


def subdivided_dodecahedron(prefix):
    """An explicit plane G(10,2), with one outer edge subdivided."""
    outer = [f"{prefix}o{i}" for i in range(10)]
    inner = [f"{prefix}i{i}" for i in range(10)]
    faces = []
    for i in range(10):
        face = (outer[i], outer[(i + 1) % 10], outer[(i + 2) % 10],
                inner[(i + 2) % 10], inner[i])
        faces.append(face if i % 2 == 0 else face[::-1])
    faces += [tuple(inner[i] for i in range(0, 10, 2)),
              tuple(inner[i] for i in range(9, 0, -2))]
    plane_map(faces)
    subdivider = f"{prefix}s"
    result = []
    for face in faces:
        walk = []
        for a, b in zip(face, face[1:] + face[:1]):
            walk.append(a)
            if {a, b} == {outer[0], outer[1]}:
                walk.append(subdivider)
        result.append(tuple(walk))
    plane_map(result)
    return result, subdivider


def rotate(face, vertex):
    index = face.index(vertex)
    return face[index:] + face[:index]


def minimum_three_completion(faces, selected):
    """Join each original degree-two vertex to a fresh subdivided dodecahedron."""
    graph = adjacency(faces)
    deficient = sorted(v for v in graph if len(graph[v]) == 2)
    protected = {faces[i] for i in selected}
    completed = list(faces)
    for index, vertex in enumerate(deficient):
        gadget, attachment = subdivided_dodecahedron(f"copy{index}:")
        base_index = next(i for i, face in enumerate(completed)
                          if vertex in face and face not in protected)
        gadget_index = next(i for i, face in enumerate(gadget) if attachment in face)
        base = rotate(completed.pop(base_index), vertex)
        side = rotate(gadget.pop(gadget_index), attachment)
        # The bridge occurs in both directions on the merged facial walk.
        completed.append((vertex,) + side + (attachment,) + base)
        completed.extend(gadget)
    result = plane_map(completed)
    assert protected <= set(completed)
    assert min(map(len, adjacency(completed).values())) == 3
    result.update({"minimum_degree": 3, "gadgets_added": len(deficient),
                   "selected_faces_preserved": True,
                   "attachment_vertices": deficient,
                   "construction": "One fresh 21-vertex subdivided dodecahedron per original degree-two vertex, joined by a bridge."})
    return result


def geometric_examples():
    bowtie = [("0", "1", "2", "3", "4"),
              ("0", "5", "6", "7", "8"),
              ("2", "1", "0", "8", "7"),
              ("2", "7", "6", "5", "0", "4", "3")]
    overlap = [("u", "a", "b", "c", "d"),
               ("u", "g", "f", "v", "e"),
               ("v", "j", "b", "a", "h"),
               ("u", "e", "v", "h", "a"),
               ("u", "d", "c", "b", "j", "v", "f", "g")]
    result = {}
    for name, faces, selected, junctions in [
            ("bowtie_extraedge", bowtie, [0, 1], [(0, 1, "0")]),
            ("overlapping_U1", overlap, [0, 1, 2], [(0, 1, "u"), (1, 2, "v")])]:
        row = plane_map(faces)
        row.update({"oriented_face_boundaries": faces, "selected_faces": selected,
                    "opposite_corners": [opposite_corners(faces, *j) for j in junctions],
                    "minimum_three_completion": minimum_three_completion(faces, selected)})
        result[name] = row
    selected_edges = {frozenset((a, b)) for index in (0, 1)
                      for a, b in zip(bowtie[index], bowtie[index][1:] + bowtie[index][:1])}
    assert frozenset(("2", "7")) not in selected_edges
    assert "7" in adjacency(bowtie)["2"]
    result["bowtie_extraedge"]["extra_induced_edge"] = ["2", "7"]
    edge0 = {frozenset((a, b)) for a, b in zip(overlap[0], overlap[0][1:] + overlap[0][:1])}
    edge2 = {frozenset((a, b)) for a, b in zip(overlap[2], overlap[2][1:] + overlap[2][:1])}
    assert edge0 & edge2 == {frozenset(("a", "b"))}
    assert len(set().union(*(set(overlap[i]) for i in (0, 1, 2)))) == 11
    result["overlapping_U1"].update({"shared_edge_of_faces_0_and_2": ["a", "b"],
                                    "selected_union_vertices": 11,
                                    "abstract_three_face_tree_vertices": 13})
    return result


def c_replay_evidence():
    """Check saved full-range coverage and aggregation, without rerunning C."""
    saved = json.loads((HERE / "review-c-replay.json").read_text())
    assert saved["aggregates"]["status"] == "PASS"
    for name in ("fibre_classifier.c", "fibre_configs.py"):
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == \
            saved["replay_metadata"]["sources"][name]["sha256"]

    def checked_text(item):
        text = item["text"]
        assert hashlib.sha256(text.encode()).hexdigest() == item["sha256"]
        return text

    def summary(text):
        fields = text.split()
        assert fields[0] == "part"
        residue, shards = map(int, fields[1].split("/"))
        parsed = {}
        for field in fields[2:]:
            key, value = field.rsplit("=", 1)
            parsed[key] = float(value) if key == "avgfibre" else int(value)
        return residue, shards, parsed

    expected_min = {"chain3_distance2": 14148, "chain3_adjacent": 12840,
                    "PI_flower": 37168, "C3": 46976}
    counts = ("processed", "empty", "disconnected", "iso", "comps>=2kills", "comps1kill")
    result = {}
    assert len(saved["shards"]) == 32
    for name, minimum in expected_min.items():
        input_text = checked_text(saved["input_files"][name])
        ports = int(input_text.splitlines()[0].split()[2])
        # Burnside: identity, six transpositions and eight 3-cycles can fix words.
        words = (4 ** ports + 6 * 2 ** ports + 8) // 24
        rows, residues = [], set()
        for shard in saved["shards"]:
            if shard["configuration"] != name:
                continue
            residue, shards, row = summary(checked_text(shard["raw_stdout"]))
            assert checked_text(shard["raw_stderr"]) == ""
            assert shards == 8 and residue not in residues
            assert residue == shard["residue"] and row == shard["parsed"]
            assert shard["input_sha256"] == saved["input_files"][name]["sha256"]
            assert row["words"] == words and row["processed"] == (words + 7 - residue) // 8
            residues.add(residue)
            rows.append(row)
        assert residues == set(range(8))
        actual = saved["aggregates"]["rows"][name]["actual"]
        for field in counts:
            assert actual[field] == sum(row[field] for row in rows)
        for field in ("mincomp", "minfibre"):
            assert actual[field] == min(row[field] for row in rows) == minimum
        for field in ("maxcomps", "maxfibre"):
            assert actual[field] == max(row[field] for row in rows)
        assert actual["words"] == actual["processed"] == words
        assert all(actual[field] == 0 for field in counts[1:])
        assert actual["maxcomps"] == 1
        result[name] = {"words": words, "min_component": minimum,
                        "all_eight_residues_checked": True}
    extra = saved["bowtie_extra_edge"]
    checked_text(extra["input"])
    residue, shards, row = summary(checked_text(extra["raw_stdout"]))
    assert (residue, shards, row["words"], row["processed"], row["mincomp"]) == (0, 1, 187, 187, 1396)
    assert all(row[field] == 0 for field in counts[1:])
    return {"scope": "Saved-output integrity, exact coverage and aggregation; not a fresh classification.",
            "full_table_rows": result, "extraedge_words": 187}


def main():
    report = {"scope": "Small independent finite checks for the 2026-10-15 review; no Hamiltonicity claim.",
              "fibres": small_fibres(), "plane_examples": geometric_examples(),
              "c_replay_evidence": c_replay_evidence(),
              "all_checks_passed": True}
    path = HERE / "review-checks.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"All review checks passed; wrote {path.name}.")


if __name__ == "__main__":
    main()
