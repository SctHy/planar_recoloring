#!/usr/bin/env python3
"""Finalize metadata for retained executions; never rerun computation or old code."""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import sys

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def save_record(path, object_text, domain, assumptions, code, command, result, summary, artifacts, methods, limits):
    data = json.loads(path.read_text())
    root = path.parent
    assert data["task"]["sha256"] == digest(root / data["task"]["file"])
    data["task"]["object"] = object_text
    data["task"]["deliverables"] = ["reproducible exact code and result", "mathematical report and stated finite scope", "validated metadata and artifact hashes"]
    data["mathematical_context"].update(assumptions=assumptions, domain=domain)
    data["implementation_discovery"] = {
        "mathematica": dict(candidate_implementations=["exact finite set operations and local list degrees"], existence_evidence="The object is finite exact edge-set arithmetic; a CAS implementation was not selected.", local_availability="unavailable", availability_evidence="Local backend inventory reports no Mathematica executable; the frozen snapshot is retained in the independent review directory."),
        "sagemath": dict(candidate_implementations=["exact finite set operations and local list degrees"], existence_evidence="The object is finite exact graph/set arithmetic; no Sage implementation was selected.", local_availability="unavailable", availability_evidence="Local backend inventory reports no native Sage executable; the frozen snapshot is retained in the independent review directory."),
        "python": dict(candidate_implementations=["stdlib integer tuples, source parsing, local allowed-list neighbour generation and exact set counts"], existence_evidence="Retained executed Python code and PASS results.", local_availability="available", availability_evidence=f"Live interpreter {sys.executable}; material results record CPython {platform.python_version()}; stale inventory 3.14.3 was refreshed to3.14.6 before this independent run.")
    }
    data["decision"] = dict(selected_backend="python", backend_version="3.14.6", selection_reason="Python-native frozen evidence and an independent auditable stdlib checker fit this exact local-neighbour task; 313 interfaces and about10,000 supplied candidate vertices are comfortably feasible.", fallback_reason="No callable local CAS is recorded; no CAS or numerical approximation is required for these local exact set operations.")
    data["execution"] = dict(status="complete", interface="local-cli", command_or_input=command, code_artifact=code)
    data["artifacts"] = [dict(path=name, role=role, sha256=digest(root / name)) for name, role in artifacts]
    data["result"] = dict(status="complete", summary=summary, result_artifact=result)
    data["verification"] = dict(methods=methods, evidence_level="exact-check", residual_or_error="not-applicable: exact finite integer counts", limitations=limits)
    path.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(dict(record=str(path), sha256=digest(path), artifact_count=len(data["artifacts"]))))


def run():
    assert platform.python_version() == "3.14.6"
    inventory = Path("/private/var/folders/60/c_yt4kyd5mv8gr_wfcbmq96c0000gn/T/Codex/math-science-computation/backend-inventory.json")
    snapshot = HERE / "backend-inventory-snapshot.json"
    assert not snapshot.exists()
    shutil.copyfile(inventory, snapshot)
    original = load("author-results.json")
    reviewed = load("review-results.json")
    both = load("both-hc-local-results.json")
    omitted = load("omitted-vertices-results.json")
    family = load("local-family-extract.json")
    assert all(r["status"] == "PASS" and r["python"] == "3.14.6" for r in (original, reviewed, both, omitted, family))
    assert digest(AUTHOR / "one-sided-degree-results-v1.json") == digest(HERE / "author-results.json") == "fb21db194e918b1dc05c2d7a0a3a5826ced3f187f8fcb5bea66d747f9fdf21c9"
    assert digest(AUTHOR / "phase6-source.tex") == digest(HERE / "phase6-source.tex") == "7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3"
    common_limits = ["Finite specified-interface counts are not uniform C5-family coverage theorems or global mathematical completion.", "No complete legal-state graph enumeration or Hamilton-cycle search.", "Completeness of supplied fibre-component word lists is inherited from frozen manuscript context, not re-enumerated here.", "Schema and hash validation does not prove mathematical correctness.", "The manuscript and previously retained author result/code are unchanged."]
    save_record(HERE / "computation-record.json", "Independent complete one-sided-degree scalar readback and arbitrary-source-Hamilton-cycle degree-two subfamily", "313 prescribed interfaces, 256 ordinary target cases and10,706 target candidate observations;230 ordinary/ordinary interfaces for the66 arbitrary-two-cycle subfamily", ["Actual frozen phase6 templates, fixed pools and first standard normalizer.", "Hard targets excluded from whole-component Hamilton-cycle premise.", "Source degree-two edges are forced in every Hamilton cycle only on ordinary source components."], "check_local.py", "python3 -B check_local.py", "review-results.json", "All313 original records and10,706 local observation vectors exactly agree; one-sided criterion covers200/256 with85 degree-two,181 degree-three-pair and66 overlap. The source-degree-two arbitrary-two-cycle extension covers66/230.", [("task.md", "input"), ("phase6-source.tex", "input"), ("author-results.json", "input"), ("backend-inventory-snapshot.json", "input"), ("check_local.py", "code"), ("review-results.json", "result"), ("report.md", "report"), ("create_records.py", "code")], ["Independent source/pool parsing and first-normalizer construction with no peer imports.", "Exact complete313-record comparison, including all local neighbour and safe-edge lists.", "Analytic proof of one-sided incident capacity and source-degree-two forced-edge implication.", "Local-only source and target list-degree evaluation at already specified candidate vertices.", "Byte equality of all53 marked C5 blocks and normalization paragraph with observed live manuscript."], common_limits+["The live manuscript byte-equality guard requires the actual workspace manuscript path when rerunning this checker."])
    save_record(HERE / "both-hc-computation-record.json", "Graph-only conditional local intersection for arbitrary Hamilton cycles on both sides", "230 ordinary-source/ordinary-target interfaces,10,379 original candidates and51 separately checked omitted printed common vertices;27 selectors in two complete finite source groups", ["Both whole-component Hamilton cycles are assumed; all hard-source or hard-target cases excluded.", "Fixed source and restored target pools; forbidden common incidence is their edge union.", "Local source and target neighbourhoods generated only from the one-coordinate allowed-list formula.", "Every omitted original candidate is incident with two pool edges of the known selected source cycle."], "extract_both_hc.py", "python3 -B extract_both_hc.py\npython3 -B check_omitted.py\npython3 -B extract_families.py", "both-hc-local-results.json", "The local bound max(0,4-ds-dt+dc-f) covers125/230, includes the previous66 and adds59. All51 omitted printed common vertices have nonpositive bound. Complete finite groups are01023:15/15 and01124:12/12; cubic stars alone cover60 interfaces and either-side degree-two witnesses98.", [("both-hc-task.md", "input"), ("phase6-source.tex", "input"), ("author-results.json", "input"), ("review-results.json", "input"), ("backend-inventory-snapshot.json", "input"), ("extract_both_hc.py", "code"), ("check_omitted.py", "code"), ("extract_families.py", "code"), ("both-hc-local-results.json", "result"), ("omitted-vertices-results.json", "result"), ("local-family-extract.json", "result"), ("both-hc-attempt-1-failure.txt", "report"), ("both-hc-report.md", "report"), ("create_records.py", "code")], ["Analytic inclusion-exclusion in the shared safe incident-edge universe of size dc-f.", "Independent graph-only local list evaluation and fixed-pool union counts at10,379 existing candidates.", "Separate local verification of all51 omitted vertices and their two selected source-cycle incident pool edges.", "Exact inclusion of all66 previous source-degree-two interfaces.", "Readback of source-type coverage and neighbour-colour cubic-star selector conditions for every certificate.", "Preserved diagnosis of the false candidate-set equality assumption."], common_limits+["Primary candidates are not the full printed common-vertex set; the two checked scopes remain separately retained.", "No whole-source-type pool-equivariance or uniform symbolic family conclusion is claimed.", "The first extract invocation failed on a false candidate=full-common assertion; the corrected full primary run and separate51-vertex check are retained.", "Arbitrary Hamilton-cycle intersection after deleting fixed pools does not imply all pool edges belong to each arbitrary cycle."])
    save_record(AUTHOR / "computation-record-final-v1.json", "Final metadata for the already executed one-sided degree criterion on existing313 interfaces", "313 specified interfaces,57 hard targets excluded,256 ordinary-target eligible cases; one-sided local-neighbour criterion", ["Actual frozen phase6 K and pools with prescribed first normalizer.", "Fixed source protected sets allowed on hard sources.", "Target whole-component Hamilton-cycle premise only on ordinary target components."], "check_one_sided_degree.py", "python3 check_one_sided_degree.py", "one-sided-degree-results-v1.json", "The preserved original execution records200/256 one-sided-degree coverage,85 degree-two and181 degree-three-pair, overlap66, additional115; independent local review matches all313 rows and10,706 observation vectors. This metadata finalization did not rerun the author computation.", [("task.md", "input"), ("phase6-source.tex", "input"), ("check_one_sided_degree.py", "code"), ("one-sided-degree-results-v1.json", "result"), ("independent_local_review/review-results.json", "result"), ("independent_local_review/check_local.py", "code"), ("independent_local_review/report.md", "report"), ("independent_local_review/backend-inventory-snapshot.json", "input"), ("independent_local_review/create_records.py", "code")], ["Original retained exact local-neighbour result and actualPython3.14.6 banner.", "Separately executed independently written checker agrees on every original row, scalar and local-list observation.", "Analytic one-sided incident counting argument in the retained independent report."], common_limits+["This is retrospective final metadata for an existing retained execution, not a newly repeated author run."])


if __name__ == "__main__":
    run()
