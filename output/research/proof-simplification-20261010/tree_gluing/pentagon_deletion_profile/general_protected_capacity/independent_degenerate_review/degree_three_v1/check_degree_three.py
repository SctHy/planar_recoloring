#!/usr/bin/env python3
"""Independent four fixed degree-three certificate checks; no peer imports."""
from pathlib import Path
from itertools import permutations, combinations
import hashlib
import json
import platform
import re
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "main-source.tex"
TEXT = SOURCE.read_text()
COLOURS = "0123"


def block(name):
    found = re.findall(r"% BEGIN " + re.escape(name) + r"\n(.*?)% END " + re.escape(name), TEXT, re.S)
    assert len(found) == 1, (name, len(found))
    return found[0]


def edge(u, v):
    return tuple(sorted((u, v)))


def edges(name):
    return {edge(u, v) for u, v in re.findall(r"(?<!\d)([0-3]{5})-([0-3]{5})(?!\d)", block(name))}


def legal(word, boundary):
    return len(word) == 5 and all(word[i] in COLOURS and word[i] != boundary[i]
                                and word[i] != word[(i + 1) % 5] for i in range(5))


def neighbours(word, boundary):
    found = []
    for i in range(5):
        for colour in COLOURS:
            if colour != word[i]:
                changed = word[:i] + colour + word[i + 1:]
                if legal(changed, boundary):
                    found.append({"word": changed, "coordinate": i, "from": word[i], "to": colour})
    return sorted(found, key=lambda x: x["word"])


types = set(re.findall(r"% BEGIN POOL-([0-4]{5})-0\n", TEXT))
assert len(types) == 22
normalizer_text = TEXT[TEXT.index("Here is the exact normalization convention."):TEXT.index("\\begin{lemma}[Protected-edge identities]")]
for token in ("s=0,\\ldots,4", "\\epsilon=+1,-1", "lexicographic", "p^{-1}(x_i)"):
    assert token in normalizer_text, token


def normalize(boundary):
    for start in range(5):
        for direction in (1, -1):
            for perm in permutations(COLOURS):
                candidate = "".join(perm[int(boundary[(start + direction * i) % 5])]
                                    if boundary[(start + direction * i) % 5] != "4" else "4"
                                    for i in range(5))
                if candidate in types:
                    return candidate, start, direction, "".join(perm)
    raise AssertionError(boundary)


def restore(word, start, direction, perm):
    result = [None] * 5
    for i, colour in enumerate(word):
        result[(start + direction * i) % 5] = COLOURS[perm.index(colour)]
    return "".join(result)


def cycle_words(boundary_type):
    name = "C1-" + boundary_type if "% BEGIN C1-" + boundary_type + "\n" in TEXT else "FHC-" + boundary_type
    words = re.findall(r"(?<!\d)([0-3]{5})(?!\d)", block(name))
    assert len(set(words)) == len(words)
    assert all(legal(w, boundary_type) for w in words)
    cycle = {edge(words[i], words[(i + 1) % len(words)]) for i in range(len(words))}
    assert all(sum(a != b for a, b in zip(u, v)) == 1 for u, v in cycle)
    assert edges("POOL-" + boundary_type + "-0") <= cycle
    return words, cycle


start_time = time.perf_counter()
specs = [
    ("00001", "01001", "32132", ["12132", "30132", "32130"], ["12132", "32130"], True),
    ("00001", "03001", "32132", ["12132", "30132", "32130"], ["12132", "32130"], False),
    ("00112", "01112", "13023", ["12023", "13020", "23023"], ["12023", "13020"], True),
    ("00112", "00111", "13023", ["12023", "13020", "23023"], ["12023", "13020"], True),
]
rows = []
for source, target, state, expected_n, expected_k_n, protected in specs:
    assert legal(state, source) and legal(state, target)
    ports = edges("COMMON-00001" if source == "00001" else "PORTS-00112")
    source_pool = edges("POOL-" + source + "-0")
    assert len(ports) == 13 and len(source_pool) == 2 and source_pool <= ports
    hard_k = ports - source_pool
    assert len(hard_k) == 11
    local_n = neighbours(state, target)
    assert [x["word"] for x in local_n] == expected_n
    assert len(local_n) == 3
    incident = {edge(state, x["word"]) for x in local_n}
    hard_incident = incident & hard_k
    assert hard_incident == {edge(state, x) for x in expected_k_n}
    normalized, shift, direction, perm = normalize(target)
    for standard in types:
        assert normalize(standard) == (standard, 0, 1, "0123")
    std_pool = edges("POOL-" + normalized + "-0")
    restored_pool = {edge(restore(u, shift, direction, perm), restore(v, shift, direction, perm))
                     for u, v in std_pool}
    assert all(legal(u, target) and legal(v, target) for u, v in restored_pool)
    words, cycle = cycle_words(normalized)
    assert state in {restore(w, shift, direction, perm) for w in words}
    safe_hard = hard_incident - restored_pool
    # All degree-two incident selections: sufficient local inference only.
    selections = [set(pair) for pair in combinations(sorted(incident), 2)]
    every_pair_meets_hard = all(pair & hard_incident for pair in selections)
    every_pair_meets_safe = all(pair & safe_hard for pair in selections)
    assert every_pair_meets_hard
    assert every_pair_meets_safe == protected
    assert (len(safe_hard) == 2) == protected
    rows.append({
        "source": source, "target": target, "state": state,
        "target_neighbours": local_n, "degree": len(local_n),
        "hard_K_incident_edges": sorted(hard_incident),
        "first_normalizer": {"type": normalized, "start": shift, "direction": direction, "permutation": perm},
        "restored_target_pool": sorted(restored_pool),
        "hard_K_incident_in_target_pool": sorted(hard_incident & restored_pool),
        "safe_hard_K_incident_edges": sorted(safe_hard),
        "every_degree_two_selection_meets_hard_K": every_pair_meets_hard,
        "every_degree_two_selection_meets_safe_hard_K": every_pair_meets_safe,
        "local_degree_two_selections_avoiding_safe_hard_K": [sorted(pair) for pair in selections if not pair & safe_hard],
        "protected_common_edge_guaranteed_by_local_argument": protected,
        "boundary_of_claim": "No conclusion that the global protected-intersection statement fails" if not protected else "Any Hamilton cycle of the target component containing this state"
    })

result = {
    "status": "PASS", "python": platform.python_version(),
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "elapsed_seconds": time.perf_counter() - start_time,
    "interface_count": len(rows), "rows": rows,
    "method": "Independent stdlib parser, first-normalizer, all one-coordinate mutations at four specified states and all three local degree-two incident selections",
    "scope": "Four fixed interfaces, no HC search/full313 replay/peer-helper import/main edit",
    "mathematical_rule": "A cycle through a degree-three vertex uses two incident edges and therefore intersects every specified pair of its three incident edges."
}
(ROOT / "degree-three-review-results-v1.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "interfaces": len(rows), "protected_guarantees": sum(r["protected_common_edge_guaranteed_by_local_argument"] for r in rows), "first_normalizers": [r["first_normalizer"] for r in rows], "seconds": result["elapsed_seconds"]}))
