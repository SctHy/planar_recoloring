#!/usr/bin/env python3
"""Replay all adopted certificates and fail-closed regression cases."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from certificate_core import CertificateError, require
from verify_adjacent_pairs import check_adjacent_pairs
from verify_path232 import check_path232
from verify_protected_pentagons import check_pentagons


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
              ("path232", check_path232), ("protected-pentagons", check_pentagons))
    for name, check in checks:
        result = {**common, "check": name, **check(text), "status": "PASS"}
        (args.report_dir / (name + ".json")).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(name + ": PASS")
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
    (args.report_dir / "negative-cases.json").write_text(json.dumps(
        {**common, "status": "PASS", "rejected_cases": negative}, indent=2, sort_keys=True) + "\n")
    report = {**common, "status": "PASS", "positive_checks": len(checks),
              "negative_cases_rejected": len(negative),
              "evidence_level": "exact-check",
              "scope": "finite local certificates and 23x23 product/reserve replay; arbitrary-order component-graph and tree-splicing arguments remain analytic"}
    (args.report_dir / "summary.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CertificateError as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
