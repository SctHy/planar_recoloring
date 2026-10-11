#!/usr/bin/env python3
"""Read-only scalar/selector extraction from the frozen graph-local result."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent


def cubic(o):
    return o["source_degree"] == o["target_degree"] == o["common_incident_count"] == 3 and o["forbidden_common_count"] == 0


def run():
    raw = (HERE / "both-hc-local-results.json").read_bytes()
    result = json.loads(raw)
    statistics = {}
    selections = []
    for row in result["records"]:
        a = row["interface"]
        typ = a["source"]
        stats = statistics.setdefault(typ, dict(eligible=0, covered=0, cubic_star=0, either_centre_degree_two=0))
        stats["eligible"] += 1
        stats["covered"] += row["covered"]
        cs = [o for o in row["certificates"] if cubic(o)]
        dg = [o for o in row["certificates"] if min(o["source_degree"], o["target_degree"]) == 2]
        stats["cubic_star"] += bool(cs)
        stats["either_centre_degree_two"] += bool(dg)
        for o in cs:
            x = o["state"]
            j = a["position"]
            assert {x[(j-1) % 5], x[(j+1) % 5]} == {typ[j], a["colour"]}
            assert o["source_neighbours"] == o["target_neighbours"]
        if typ in {"01023", "01124"}:
            assert row["covered"]
            choices = cs if cs else dg
            assert choices
            chosen = min(choices, key=lambda o: o["state"])
            selections.append(dict(interface=a, selector_rule="common-cubic-star" if cs else "one-side-degree-two", state=chosen["state"], source_degree=chosen["source_degree"], target_degree=chosen["target_degree"], common_degree=chosen["common_incident_count"], forbidden_common=chosen["forbidden_common_count"], safe_neighbours=chosen["safe_common_neighbours"], degree_terms_source=chosen["source_degree_terms"], degree_terms_target=chosen["target_degree_terms"]))
    all_covered_types = [t for t, d in statistics.items() if d["eligible"] == d["covered"]]
    cubic_all_types = [t for t, d in statistics.items() if d["eligible"] == d["cubic_star"]]
    assert sorted(all_covered_types) == ["01023", "01124"]
    assert cubic_all_types == []
    assert len(selections) == 27
    out = dict(status="PASS", python=platform.python_version(), input_sha256=hashlib.sha256(raw).hexdigest(), code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), source_type_statistics=dict(sorted(statistics.items())), entirely_covered_source_types=sorted(all_covered_types), entirely_cubic_star_covered_source_types=cubic_all_types, total_cubic_star_interfaces=sum(d["cubic_star"] for d in statistics.values()), total_either_centre_degree_two_interfaces=sum(d["either_centre_degree_two"] for d in statistics.values()), selectors=selections, selected_family_selector_rule_counts=dict(Counter(z["selector_rule"] for z in selections)), limits="Two selected-template source types have complete finite coverage; no uniform symbolic source-type-family theorem or pool-equivariant transport is claimed.")
    (HERE / "local-family-extract.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k: out[k] for k in ("status", "entirely_covered_source_types", "entirely_cubic_star_covered_source_types", "total_cubic_star_interfaces", "total_either_centre_degree_two_interfaces", "selected_family_selector_rule_counts")}, indent=2))


if __name__ == "__main__":
    run()
