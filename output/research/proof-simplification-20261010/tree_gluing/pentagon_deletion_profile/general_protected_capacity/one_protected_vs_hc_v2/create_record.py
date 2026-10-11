#!/usr/bin/env python3
"""Freeze metadata for the executed symmetric one-sided v2; no computation rerun."""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import sys

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    assert platform.python_version() == "3.14.6"
    path = HERE / "computation-record.json"
    r = json.loads(path.read_text())
    result = json.loads((HERE / "symmetric-one-sided-results-v2.json").read_text())
    assert result["status"] == "PASS" and result["python"] == "3.14.6"
    assert r["task"]["sha256"] == sha(HERE / "task.md")
    inventory = HERE / "backend-inventory-snapshot.json"
    assert not inventory.exists()
    shutil.copyfile(HERE.parent / "one_sided_degree_v1/independent_local_review/backend-inventory-snapshot.json", inventory)
    r["task"].update(object="Generic fixed protected set versus any Hamilton cycle on the opposite original interface side, evaluated in both directions without renormalizing", deliverables=["reproducible independently written local-only checker", "complete two-direction finite result and scope groups", "analytic local implication and validated metadata"])
    r["mathematical_context"].update(assumptions=["Actual frozen phase6 bases and pools; original first target normalizer retained for reversal.", "A whole-component Hamilton cycle is needed only on the opposite side of the fixed K.", "Hard fixed sides are allowed; both-hard5 cases excluded.", "Fixed K has its own pool removed; the HC-side pool is excluded from safe incidences."],domain="313 specified interfaces:230HH,26hard-source/HC-target,22HC-source/hard-target,30constant-source/hard-target,5hard/hard;10706forward and10808reverse local candidate observations")
    r["implementation_discovery"] = {
        "mathematica": dict(candidate_implementations=["exact finite graph-set arithmetic and local degree formula"], existence_evidence="The operations are finite exact set arithmetic; no CAS implementation selected.", local_availability="unavailable", availability_evidence="Retained local backend inventory has no Mathematica executable."),
        "sagemath": dict(candidate_implementations=["exact finite graph-set arithmetic and local degree formula"], existence_evidence="The operations are finite exact graph-set arithmetic; no Sage implementation selected.", local_availability="unavailable", availability_evidence="Retained local backend inventory has no native Sage executable."),
        "python": dict(candidate_implementations=["stdlib tuples, parsing, prescribed permutations, local allowed-list mutations and exact incidence counts"], existence_evidence="check_symmetric.py ran to PASS and produced the exact retained result.", local_availability="available", availability_evidence=f"Current material execution recordsPython3.14.6; live interpreter is{sys.executable}.")
    }
    r["decision"] = dict(selected_backend="python",backend_version="3.14.6",selection_reason="The frozen evidence is Python-native and the required independent stdlib implementation handles roughly21000 local vertices without complete graph construction.",fallback_reason="No recorded local CAS is callable, and no CAS or numerical approximation is required for these exact finite set operations.")
    r["execution"] = dict(status="complete",interface="local-cli",command_or_input="python3 -B check_symmetric.py",code_artifact="check_symmetric.py")
    names = [("task.md","input"),("phase6-source.tex","input"),("original-forward-results.json","input"),("backend-inventory-snapshot.json","input"),("check_symmetric.py","code"),("symmetric-one-sided-results-v2.json","result"),("report.md","report"),("create_record.py","code")]
    r["artifacts"] = [dict(path=name,role=role,sha256=sha(HERE / name)) for name,role in names]
    r["result"] = dict(status="complete",summary="Forward200/256exactly agrees with all10706 original observations. Reverse228/282; either-direction266/308after excludingonly5hard/hard. HHunion202/230with162overlap; mixed nonconstant hard34/53; constantreverse30/30.",result_artifact="symmetric-one-sided-results-v2.json")
    r["verification"] = dict(methods=["Independent actual-source parsing of cycles, hard D13 bases, fixed pools and313 interface identities.","First-normalizer reconstruction and explicit equality with the original actual mapping; reverse never renormalizes.","Exact agreement with every originalforward neighbour/safe-edge list and scalar observation.","Exact local one-coordinate neighbour generation on both original HC-side scopes.","Analytic2+g-d incident-edge lower bound and correct fixed-K/any-opposite-HC quantifiers."],evidence_level="exact-check",residual_or_error="not-applicable: exact finite integer counts",limitations=["Finite266/308and202/230coverage is not a uniform symbolic C5-family theorem or global theorem completion.","Either-direction fixed-K/any-opposite-HC union is not an arbitrary-both-Hamilton-cycle guarantee.","No result is claimed on5hard/hard interfaces.","No complete legal-state graph enumeration, Hamilton search, or actual K/K common-edge enumeration.","Supplied component completeness comes from frozen manuscript context and is not re-enumerated here.","Record validation checks schema/hashes only; manuscript and old results are unchanged."])
    path.write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps(dict(record_sha256=sha(path),result_sha256=sha(HERE / "symmetric-one-sided-results-v2.json"))))


if __name__ == "__main__":
    run()
