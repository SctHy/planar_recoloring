#!/usr/bin/env python3
"""Replay all adopted certificates and fail-closed regression cases."""
import argparse
from copy import deepcopy
import hashlib
import json
import re
import sys
from pathlib import Path

from certificate_core import CertificateError, require
from verify_adjacent_pairs import check_adjacent_pairs
from verify_degree_two_families import (check_degree_two_families,
                                       check_family as check_degree_two_family,
                                       load_family as load_degree_two_family)
from verify_degree_two_interfaces import (check_degree_two_interfaces,
                                         check_family as check_degree_two_interface_family)
from verify_path232 import check_path232
from verify_protected_pentagons import check_pentagons
from verify_shared_hub_paths import check_path_family, check_shared_hub_paths, load_family


def remove_block(text, name):
    return re.sub(rf"^% BEGIN {name}\n.*?^% END {name}\n", "", text, count=1, flags=re.M | re.S)


def change_block(text, name, before, after):
    pattern = rf"(^% BEGIN {name}\n)(.*?)(^% END {name}$)"
    found = re.search(pattern, text, re.M | re.S)
    require(found is not None and before in found[2], f"negative-test anchor absent: {name}")
    return text[:found.start(2)] + found[2].replace(before, after, 1) + text[found.end(2):]


def check_manifest(manifest_path):
    """Check every delivered byte named by a publication manifest.

    The manifest is deliberately checked independently of the certificate
    readers: a passing local replay must not be confused with a hash check of
    the files that will actually be delivered.
    """
    manifest_path = manifest_path.resolve()
    require(manifest_path.is_file(), f"manifest not found: {manifest_path}")
    data = json.loads(manifest_path.read_text())
    require(data.get("format") == "sha256 file manifest", "unsupported manifest format")
    rows = data.get("files")
    require(isinstance(rows, list) and rows, "manifest has no file rows")
    listed = set()
    root = manifest_path.parent
    for row in rows:
        rel = row.get("path")
        require(isinstance(rel, str) and rel and not Path(rel).is_absolute(),
                "manifest contains an invalid relative path")
        require(rel not in listed and rel != "manifest.json", "manifest path is duplicated or self-listed")
        listed.add(rel)
        target = root / rel
        require(target.is_file(), f"manifest file missing: {rel}")
        raw = target.read_bytes()
        require(row.get("bytes") == len(raw), f"manifest byte count mismatch: {rel}")
        require(row.get("sha256") == hashlib.sha256(raw).hexdigest(),
                f"manifest hash mismatch: {rel}")
    def is_build_artifact(path):
        return (
            ".latex-build" in path.parts
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
            or path.suffix in {".aux", ".log", ".out", ".fdb_latexmk", ".fls"}
            or path.name.endswith(".synctex.gz")
            or path.name == ".DS_Store"
            or path.name.startswith("._")
        )

    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file()
        and not is_build_artifact(p)
        and p.name != "manifest.json"
    }
    require(actual == listed,
            "manifest coverage mismatch: "
            f"missing={sorted(actual - listed)} extra={sorted(listed - actual)}")
    return {"files": len(listed), "status": "PASS"}


def default_manifest_path():
    """Locate the manifest both in the repository and in its standalone package."""
    package_manifest = Path(__file__).parents[1] / "manifest.json"
    repository_manifest = Path(__file__).parents[1] / "output" / "publication" / "manifest.json"
    return package_manifest if package_manifest.exists() else repository_manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path,
                        default=Path(__file__).with_name("article_certificates.tex"))
    parser.add_argument("--report-dir", type=Path,
                        default=Path(__file__).with_name("reports"))
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write-reports", action="store_true",
                       help="run all finite checks and write the JSON reports")
    modes.add_argument("--check-manifest", action="store_true",
                       help="read-only verification of the manifest and every delivered file")
    parser.add_argument("--manifest", type=Path,
                        default=default_manifest_path())
    args = parser.parse_args()

    # Keep the historical no-argument command useful while making the two
    # operations explicit.  In particular, --check-manifest must not create
    # directories or rewrite any report in the delivered package.
    if args.check_manifest:
        result = check_manifest(args.manifest)
        print("manifest: PASS")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    text = args.source.read_text()
    digest = hashlib.sha256(args.source.read_bytes()).hexdigest()
    args.report_dir.mkdir(parents=True, exist_ok=True)
    common = {"source": args.source.name, "source_sha256": digest,
              "arithmetic": "exact finite sets and integers"}
    checks = (("adjacent-pairs", check_adjacent_pairs),
              ("path232", check_path232), ("protected-pentagons", check_pentagons),
              ("shared-hub-paths", check_shared_hub_paths),
              ("degree-two-families", check_degree_two_families),
              ("degree-two-interfaces", check_degree_two_interfaces))
    degree_results = {}
    for name, check in checks:
        result = {**common, "check": name, **check(text), "status": "PASS"}
        (args.report_dir / (name + ".json")).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(name + ": PASS")
        if name.startswith("degree-two-"):
            degree_results[name] = {r["kind"]: r for r in result["families"]}
    primary, direct = degree_results["degree-two-families"], degree_results["degree-two-interfaces"]
    require(primary.keys() == direct.keys(), "degree-two reader family disagreement")
    for kind in primary:
        for field in ("file", "bytes", "sha256", "templates", "template_states", "boundaries",
                      "directed_interfaces", "minimum_common_cycle_edges", "margins_by_changed_indices"):
            require(primary[kind][field] == direct[kind][field],
                    f"degree-two reader disagreement: {kind} {field}")
    cases = [
        ("missing_pair_cycles", check_adjacent_pairs, remove_block(text, "PAIR-CYCLES")),
        ("illegal_pair_cycle", check_adjacent_pairs,
         change_block(text, "PAIR-CYCLES", "03 04 14", "03 03 14")),
        ("missing_path_cycle", check_path232, remove_block(text, "PATH232-CYCLES")),
        ("illegal_path_cycle", check_path232,
         change_block(text, "PATH232-CYCLES", "001&120", "001&110")),
        ("missing_pentagon_pool", check_pentagons, remove_block(text, "POOL-00112-0")),
        ("illegal_pentagon_seed", check_pentagons,
         change_block(text, "C2-00112", "012020 012030", "012020 012020")),
        ("invalid_individual_edge", check_pentagons,
         change_block(text, "INTERFACES-ALL", "21313-21323", "21313-31313")),
        ("witness_cut_by_pool", check_pentagons,
         change_block(text, "POOL-00112-0", "21020-23020", "12023-13023")),
        ("altered_selector_data", check_pentagons,
         text.replace("00001&13123,", "00001&12123,", 1)),
        ("missing_shared_hub_counts", check_shared_hub_paths,
         remove_block(text, "SHARED-HUB-PATH-COUNTS")),
        ("altered_shared_hub_counts", check_shared_hub_paths,
         change_block(text, "SHARED-HUB-PATH-COUNTS", "4&5&160&64&576&3",
                      "4&5&160&64&576&2")),
    ]
    negative = []
    for name, check, corrupted in cases:
        require(corrupted != text, "negative case failed to alter the input")
        try:
            check(corrupted)
        except CertificateError as error:
            negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
        else:
            raise CertificateError(f"corrupted certificate accepted: {name}")
    family_cases = (("missing_shared_hub_template", 5),
                    ("duplicate_shared_hub_template", 4),
                    ("repeated_shared_hub_state", 4),
                    ("negative_shared_hub_palette_digit", 5))
    for name, order in family_cases:
        original = load_family(order)
        corrupted = deepcopy(original)
        if name == "missing_shared_hub_template":
            corrupted["records"].pop()
        elif name == "duplicate_shared_hub_template":
            corrupted["records"].append(deepcopy(corrupted["records"][0]))
        elif name == "repeated_shared_hub_state":
            corrupted["records"][0]["cycle"][0] = corrupted["records"][0]["cycle"][1][:]
        else:
            corrupted["records"][0]["cycle"][0][0] = -1
        require(corrupted != original, "negative case failed to alter the path family")
        try:
            check_path_family(order, corrupted)
        except CertificateError as error:
            negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
        else:
            raise CertificateError(f"corrupted certificate accepted: {name}")
    for suite, check in (("families", check_degree_two_families),
                         ("interfaces", check_degree_two_interfaces)):
        count_cases = (("missing", remove_block(text, "DEGREE-TWO-FAMILY-COUNTS")),
                       ("altered", change_block(text, "DEGREE-TWO-FAMILY-COUNTS",
                                                 "star3&15&499&256&3072&4",
                                                 "star3&15&499&256&3072&3")))
        for mutation, corrupted in count_cases:
            name = mutation + "_degree_two_counts_" + suite
            require(corrupted != text, "negative case failed to alter degree-two counts")
            try:
                check(corrupted)
            except CertificateError as error:
                negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
            else:
                raise CertificateError(f"corrupted certificate accepted: {name}")
    degree_cases = ("missing_record", "duplicate_record", "negative_palette_digit",
                    "altered_internal_graph", "omitted_alias_pair", "short_cycle_word")
    for mutation in degree_cases:
        kind = "path6" if mutation == "omitted_alias_pair" else "path4heavy"
        original = load_degree_two_family(kind)
        corrupted = deepcopy(original)
        if mutation == "missing_record":
            corrupted["records"].pop()
        elif mutation == "duplicate_record":
            corrupted["records"].append(deepcopy(corrupted["records"][0]))
        elif mutation == "negative_palette_digit":
            corrupted["records"][0]["cycle"][0][0] = -1
        elif mutation == "altered_internal_graph":
            corrupted["graph_edges"].pop()
        elif mutation == "omitted_alias_pair":
            corrupted["transition_groups"].pop()
        else:
            corrupted["records"][0]["cycle"][0].pop()
        require(corrupted != original, "negative case failed to alter degree-two family")
        for suite, check in (("families", check_degree_two_family),
                             ("interfaces", check_degree_two_interface_family)):
            name = mutation + "_degree_two_" + suite
            try:
                check(kind, corrupted)
            except CertificateError as error:
                negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
            else:
                raise CertificateError(f"corrupted certificate accepted: {name}")
    (args.report_dir / "negative-cases.json").write_text(json.dumps(
        {**common, "status": "PASS", "rejected_cases": negative}, indent=2, sort_keys=True) + "\n")
    report = {**common, "status": "PASS", "positive_checks": len(checks),
              "negative_cases_rejected": len(negative),
              "evidence_level": "exact-check",
              "scope": "finite local certificates, shared-hub paths, seven degree-two families with independent physical interfaces, and 23x23 product/reserve replay; arbitrary-order restoration, component-graph, tree-splicing, and structural inductions remain analytic"}
    (args.report_dir / "summary.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CertificateError as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
