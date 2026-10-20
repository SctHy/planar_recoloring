#!/usr/bin/env python3
"""Verify the finite constructions and check the rejection of invalid examples."""
import argparse
from copy import deepcopy
import hashlib
import json
import re
import sys
from pathlib import Path

from finite_graphs import VerificationError, require
from verify_adjacent_pairs import check_adjacent_pairs
from verify_degree_two_families import (check_degree_two_families,
                                       check_family as check_degree_two_family,
                                       load_family as load_degree_two_family)
from verify_degree_two_interfaces import (check_degree_two_interfaces,
                                         check_family as check_degree_two_interface_family)
from verify_path232 import check_path232
from verify_pentagonal_reservoirs import (check_pentagonal_reservoirs,
                                        check_family as check_pentagonal_family,
                                        load_family as load_pentagonal_family)
from verify_pentagonal_reservoir_interfaces import (check_pentagonal_reservoir_interfaces,
                                                   check_family as check_pentagonal_interface_family)
from verify_protected_pentagons import check_pentagons
from verify_shared_hub_paths import check_path_family, check_shared_hub_paths, load_family
from verify_extended_cycles import (check_extended_cycles,
                                    check_family as check_extended_family,
                                    load_family as load_extended_family)
from verify_extended_cycle_interfaces import (check_extended_cycle_interfaces,
                                              check_family as check_extended_interface_family)
from verify_bowtie_families import check_bowtie_families
from verify_bowtie_interfaces import check_bowtie_interfaces
from verify_hinged_pairs import check_hinged_pairs
from verify_hinged_pair_interfaces import check_hinged_pair_interfaces


def remove_block(text, name):
    return re.sub(rf"^% BEGIN {name}\n.*?^% END {name}\n", "", text, count=1, flags=re.M | re.S)


def change_block(text, name, before, after):
    pattern = rf"(^% BEGIN {name}\n)(.*?)(^% END {name}$)"
    found = re.search(pattern, text, re.M | re.S)
    require(found is not None and before in found[2], f"negative-test anchor absent: {name}")
    return text[:found.start(2)] + found[2].replace(before, after, 1) + text[found.end(2):]


def append_extended_negative_cases(text, negative):
    for suite, check in (("families", check_extended_cycles),
                         ("interfaces", check_extended_cycle_interfaces)):
        cases = (("missing", remove_block(text, "EXTENDED-CYCLE-COUNTS")),
                 ("altered", change_block(text, "EXTENDED-CYCLE-COUNTS",
                                           "sharededge&187&158054&4096&95232&56",
                                           "sharededge&187&158054&4096&95232&55")))
        for mutation, corrupted in cases:
            try:
                check(corrupted)
            except VerificationError as error:
                negative.append({"case": mutation + "_extended_counts_" + suite,
                                 "status": "REJECTED", "reason": str(error)})
            else:
                raise VerificationError("corrupted extended-cycle counts accepted")
    mutations = ("missing_boundary", "duplicate_boundary", "wrong_family", "extra_field",
                 "boolean_boundary", "negative_boundary", "invalid_palette",
                 "missing_state", "illegal_step")
    original = load_extended_family("sharededgechord")
    for mutation in mutations:
        corrupted = deepcopy(original)
        records = corrupted["records"]
        if mutation == "missing_boundary":
            records.pop()
        elif mutation == "duplicate_boundary":
            records.append(deepcopy(records[0]))
        elif mutation == "wrong_family":
            corrupted["family"] = "bare"
        elif mutation == "extra_field":
            corrupted["extra"] = 0
        elif mutation == "boolean_boundary":
            records[0]["boundary"][0] = False
        elif mutation == "negative_boundary":
            records[0]["boundary"][0] = -1
        elif mutation == "invalid_palette":
            records[0]["cycle"][0] = "4" + records[0]["cycle"][0][1:]
        elif mutation == "missing_state":
            records[0]["cycle"].pop()
        else:
            cycle = records[0]["cycle"]
            cycle[0], cycle[2] = cycle[2], cycle[0]
        require(corrupted != original or mutation == "boolean_boundary",
                "extended-cycle mutation did not change the input")
        for suite, check in (("families", check_extended_family),
                             ("interfaces", check_extended_interface_family)):
            try:
                check("sharededgechord", corrupted)
            except VerificationError as error:
                negative.append({"case": mutation + "_extended_" + suite,
                                 "status": "REJECTED", "reason": str(error)})
            else:
                raise VerificationError("corrupted extended-cycle family accepted: " + mutation)


def append_bowtie_negative_cases(text, negative):
    from copy import deepcopy
    from finite_graphs import VerificationError, require
    import verify_bowtie_families as primary
    import verify_bowtie_interfaces as direct

    def rejected(name, check, expected):
        try:
            check()
        except VerificationError as error:
            require(expected in str(error), "bowtie mutation rejected for an unintended reason: " + str(error))
            negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
        else:
            require(False, "corrupted bowtie construction was accepted: " + name)

    original = primary.load_data("bowseed")
    record = original["templates"][0]
    boundary = tuple(record["boundary"])
    require(boundary == (0,) * 8, "bowtie product cycle-negative anchor changed")
    cases = []

    bad = deepcopy(record)
    bad["boundary"][0] = 4
    cases.append(("boundary_palette", bad, "boundary", "boundary"))
    bad = deepcopy(record)
    bad["matching"][0][0] = "9" + bad["matching"][0][0][1:]
    cases.append(("matching_palette", bad, "colour word", "raw matching word"))
    bad = deepcopy(record)
    bad["cycles"]["3"][0] = "3" + bad["cycles"]["3"][0][1:]
    cases.append(("row_palette", bad, "product cycle row", "raw clique product cycle"))
    bad = deepcopy(record)
    bad["cycles"]["2"][0] = bad["cycles"]["2"][1]
    cases.append(("duplicate_seed_state", bad, "misses or repeats", "omits or repeats"))
    bad = deepcopy(record)
    bad["cycles"]["2"][0], bad["cycles"]["2"][2] = bad["cycles"]["2"][2], bad["cycles"]["2"][0]
    cases.append(("illegal_seed_step", bad, "product step", "product step"))
    bad = deepcopy(record)
    bad["matching"][0] = bad["matching"][1][:]
    cases.append(("nonmatching_protected_edges", bad, "not a matching", "not a matching"))
    bad = deepcopy(record)
    bad["cycles"].pop("3")
    cases.append(("missing_K3_seed", bad, "clique product cycle", "clique product cycle"))
    bad = deepcopy(record)
    require(bad["matching"][0] == ["012121212", "312121212"], "bowtie retention-negative anchor changed")
    # This remains a legal matching edge, disjoint from the other entries;
    # it is absent from row zero of the unchanged complete K2 product cycle.
    bad["matching"][0] = ["012121212", "032121212"]
    cases.append(("legal_matching_edge_missing_from_row", bad, "missing from row", "missing in row"))
    for name, bad, primary_reason, direct_reason in cases:
        rejected("bowtie_primary_" + name,
                 lambda bad=bad: primary.check_seed_template("bowseed", boundary, bad), primary_reason)
        rejected("bowtie_direct_" + name,
                 lambda bad=bad: direct.check_seed_template("bowseed", boundary, bad), direct_reason)

    trees = primary.load_records("bowseed", "clique-trees")
    bad = deepcopy(trees[boundary])
    bad["blocks"][0][0] = bad["blocks"][0][1]
    rejected("bowtie_tree_duplicate_partition_state",
             lambda: primary.check_clique_tree("bowseed", boundary, bad), "partition")

    t = (0, 0, 0, 0, 0, 1, 2, 0)
    bad = deepcopy(trees[t])
    require(bad["blocks"][258][2] == 434 and bad["blocks"][95][1] == 171,
            "bowtie path-not-K3 negative anchor changed")
    # Exchange two indices, preserving the complete partition; the changed
    # triangle is a three-vertex path, so a P3 check would be insufficient.
    bad["blocks"][258][2], bad["blocks"][95][1] = bad["blocks"][95][1], bad["blocks"][258][2]
    rejected("bowtie_tree_P3_substituted_for_K3_with_valid_partition",
             lambda: primary.check_clique_tree("bowseed", t, bad), "not a clique")

    t = (0, 0, 0, 0, 0, 0, 1, 0)
    bad = deepcopy(trees[t])
    require(bad["connectors"][37][1] == 804, "bowtie capacity-negative anchor changed")
    # The new endpoint is in the same block and gives a legal factor edge.
    # The exact quotient tree survives, but one vertex has degree 3.
    bad["connectors"][37][1] = 806
    rejected("bowtie_tree_legal_quotient_with_physical_capacity_three",
             lambda: primary.check_clique_tree("bowseed", t, bad), "excessive connector degree bound")

    ordinary = deepcopy(primary.load_ordinary())
    ordinary["pools"]["00000:0"].reverse()
    rejected("bowtie_ordinary_reserve_ids_differ_from_marked_source",
             lambda: primary.validate_ordinary_pentagons(text, ordinary), "differ from current marked source")

    altered = deepcopy(original)
    bad = altered["templates"][133]
    require(tuple(bad["boundary"]) == (0, 0, 1, 0, 1, 0, 1, 1), "bowtie transition-negative anchor changed")
    for a, b in ((0, 15), (1, 67)):
        bad["matching"][a], bad["matching"][b] = bad["matching"][b], bad["matching"][a]
    # All matching edges and K2/K3 product cycles are unchanged. Both local product cycle
    # verification programs accept, while the designated core loses two critical common
    # edges at physical 01001011 -> 01101111: nine becomes seven.
    primary.check_seed_template("bowseed", bad["boundary"], bad)
    direct.check_seed_template("bowseed", bad["boundary"], bad)
    rejected("bowtie_primary_valid_seeds_with_incompatible_reserve_core",
             lambda: primary.check_family("bowseed", seed_data=altered), "transition overlap")
    rejected("bowtie_direct_valid_seeds_with_incompatible_reserve_core",
             lambda: direct.check_family("bowseed", data=altered), "transition overlap")


def append_hinged_negative_cases(text, negative):
    from copy import deepcopy
    from finite_graphs import VerificationError, require
    import verify_hinged_pairs as primary
    import verify_hinged_pair_interfaces as direct

    def rejected(name, check, expected):
        try:
            check()
        except VerificationError as error:
            require(expected in str(error), "hinged mutation rejected for an unintended reason: " + str(error))
            negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
        else:
            require(False, "corrupted hinged-pair construction was accepted: " + name)

    count_before = len(negative)
    original = primary.load_data("cycles")
    record = original["models"]["bare"][0]
    boundary = record["boundary"]
    require(boundary == "0000000", "hinged product cycle-negative anchor changed")
    tuple_boundary = tuple(map(int, boundary))
    cases = []
    bad = deepcopy(record)
    bad["boundary"] = "4" + bad["boundary"][1:]
    cases.append(("boundary_palette", bad, "raw colour word", "boundary"))
    bad = deepcopy(record)
    bad["matching"][0][0] = "4" + bad["matching"][0][0][1:]
    cases.append(("matching_palette", bad, "raw colour word", "raw matching word"))
    bad = deepcopy(record)
    bad["clique2"][0] = "2" + bad["clique2"][0][1:]
    cases.append(("physical_row_palette", bad, "physical product cycle row", "raw product cycle row or word"))
    bad = deepcopy(record)
    bad["clique2"][0] = bad["clique2"][1]
    cases.append(("duplicate_seed_state", bad, "misses or repeats", "omits or repeats"))
    bad = deepcopy(record)
    bad["clique2"].pop()
    cases.append(("missing_seed_state", bad, "misses or repeats", "omits or repeats"))
    bad = deepcopy(record)
    bad["clique2"][0], bad["clique2"][2] = bad["clique2"][2], bad["clique2"][0]
    cases.append(("illegal_seed_step", bad, "product cycle step", "product step"))
    bad = deepcopy(record)
    bad["matching"][0] = bad["matching"][1][:]
    cases.append(("nonmatching_protected_edges", bad, "not a matching", "not a matching"))
    bad = deepcopy(record)
    bad["path3"] = bad["clique3"][:]
    cases.append(("K3_seed_substituted_for_P3", bad, "product cycle step", "nonpath row edge"))
    bad = deepcopy(record)
    require(bad["matching"][0] == ["10212212", "13212212"], "hinged row-retention negative anchor changed")
    # This replacement is a legal factor edge disjoint from all other matching
    # entries, but it is absent from row zero of the unchanged product cycle.
    bad["matching"][0] = ["10212212", "30212212"]
    cases.append(("legal_matching_edge_missing_from_row", bad, "missing from row", "missing in row"))
    for name, bad, primary_reason, direct_reason in cases:
        rejected("hinged_primary_" + name,
                 lambda bad=bad: primary.check_seed_template("bare", tuple_boundary, bad), primary_reason)
        rejected("hinged_direct_" + name,
                 lambda bad=bad: direct.check_seed_template("bare", boundary, bad), direct_reason)

    for mutation in ("missing_boundary", "duplicate_boundary", "extra_field", "Boolean_format"):
        bad = deepcopy(original)
        if mutation == "missing_boundary":
            bad["models"]["bare"].pop()
            reasons = ("boundary representative", "boundary representative")
        elif mutation == "duplicate_boundary":
            bad["models"]["bare"].append(deepcopy(bad["models"]["bare"][0]))
            reasons = ("duplicate", "duplicate")
        elif mutation == "extra_field":
            bad["unrecognized"] = True
            reasons = ("data format", "data format mismatch")
        else:
            bad["format"] = True
            reasons = ("data format", "data format mismatch")
        rejected("hinged_primary_" + mutation,
                 lambda bad=bad: primary.check_family("bare", seed_data=bad), reasons[0])
        rejected("hinged_direct_" + mutation,
                 lambda bad=bad: direct.check_family("bare", data=bad), reasons[1])

    marker = "HINGED-PAIR-COUNTS"
    require(text.count("% BEGIN " + marker) == text.count("% END " + marker) == 1,
            "hinged coverage-marker negative anchor changed")
    missing = text.replace("% BEGIN " + marker, "% BEGIN OMITTED-" + marker).replace(
        "% END " + marker, "% END OMITTED-" + marker)
    count_row = "bare&379&241774&1934192&430080&6&6"
    require(text.count(count_row) == 1, "hinged coverage-count negative anchor changed")
    changed = text.replace(count_row, "bare&380&241774&1934192&430080&6&6", 1)
    for suffix, corrupted, reason in (("missing_coverage_marker", missing, "missing construction block"),
                                      ("altered_coverage_count", changed, "coverage")):
        rejected("hinged_primary_" + suffix,
                 lambda corrupted=corrupted: primary.check_hinged_pairs(corrupted), reason)
        rejected("hinged_direct_" + suffix,
                 lambda corrupted=corrupted: direct.check_hinged_pair_interfaces(corrupted), reason)

    trees = primary.load_records("bare", "trees")
    bad = deepcopy(trees[tuple_boundary])
    bad["blocks"][0][0] = bad["blocks"][0][1]
    rejected("hinged_tree_duplicate_partition_state",
             lambda: primary.check_clique_tree("bare", tuple_boundary, bad), "partition")
    t = (0, 0, 0, 0, 0, 1, 2)
    bad = deepcopy(trees[t])
    require(bad["blocks"][149][2] == 288 and bad["blocks"][77][1] == 144,
            "hinged path-not-K3 negative anchor changed")
    # Swapping two indices preserves the full state partition. The modified
    # triangle is a path of order three, so a path-only check would miss it.
    bad["blocks"][149][2], bad["blocks"][77][1] = bad["blocks"][77][1], bad["blocks"][149][2]
    rejected("hinged_tree_P3_substituted_for_K3_with_valid_partition",
             lambda: primary.check_clique_tree("bare", t, bad), "not a clique")
    t = (0, 0, 0, 0, 0, 1, 0)
    bad = deepcopy(trees[t])
    require(bad["connectors"][93][0] == 175, "hinged capacity-negative anchor changed")
    # The endpoint remains in its original block and the edge stays legal;
    # the same quotient tree now overloads one vertex to degree 3.
    bad["connectors"][93][0] = 174
    rejected("hinged_tree_legal_quotient_with_physical_capacity_three",
             lambda: primary.check_clique_tree("bare", t, bad), "excessive connector degree bound")

    altered = deepcopy(original)
    bad = altered["models"]["bare"][89]
    require(bad["boundary"] == "0011101", "hinged transition-negative anchor changed")
    for a, b in ((0, 13), (1, 15)):
        bad["matching"][a], bad["matching"][b] = bad["matching"][b], bad["matching"][a]
    # Every matching edge and all three complete product cycles survive. At the actual
    # interface 0101011 -> 0111111, full overlap is six while the new designated
    # core has only four common edges instead of the required six.
    primary.check_seed_template("bare", tuple(map(int, bad["boundary"])), bad)
    direct.check_seed_template("bare", bad["boundary"], bad)
    rejected("hinged_primary_valid_seeds_with_incompatible_reserve_core",
             lambda: primary.check_family("bare", seed_data=altered), "transition overlap")
    rejected("hinged_direct_valid_seeds_with_incompatible_reserve_core",
             lambda: direct.check_family("bare", data=altered), "transition overlap")
    require(len(negative) - count_before == 35, "unexpected hinged-pair negative-case count")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path,
                        default=Path(__file__).with_name("local_constructions.tex"))
    parser.add_argument("--report-dir", type=Path,
                        default=Path(__file__).with_name("reports"))
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write-reports", action="store_true",
                       help="run all finite checks and write the JSON reports")
    args = parser.parse_args()

    text = args.source.read_text()
    digest = hashlib.sha256(args.source.read_bytes()).hexdigest()
    args.report_dir.mkdir(parents=True, exist_ok=True)
    common = {"source": args.source.name, "source_sha256": digest,
              "arithmetic": "exact finite sets and integers"}
    checks = (("adjacent-pairs", check_adjacent_pairs),
              ("path232", check_path232), ("protected-pentagons", check_pentagons),
              ("shared-hub-paths", check_shared_hub_paths),
              ("degree-two-families", check_degree_two_families),
              ("degree-two-interfaces", check_degree_two_interfaces),
              ("pentagonal-reservoirs", check_pentagonal_reservoirs),
              ("pentagonal-reservoir-interfaces", check_pentagonal_reservoir_interfaces),
              ("extended-cycles", check_extended_cycles),
              ("extended-cycle-interfaces", check_extended_cycle_interfaces),
              ("bowtie-families", check_bowtie_families),
              ("bowtie-interfaces", check_bowtie_interfaces),
              ("hinged-pairs", check_hinged_pairs),
              ("hinged-pair-interfaces", check_hinged_pair_interfaces))
    degree_results, pentagonal_results, extended_results, bowtie_results = {}, {}, {}, {}
    hinged_results = {}
    for name, check in checks:
        result = {**common, "check": name, **check(text), "status": "PASS"}
        (args.report_dir / (name + ".json")).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(name + ": PASS")
        if name.startswith("degree-two-"):
            degree_results[name] = {r["kind"]: r for r in result["families"]}
        if name.startswith("pentagonal-reservoir"):
            pentagonal_results[name] = {r["kind"]: r for r in result["families"]}
        if name.startswith("extended-cycle"):
            extended_results[name] = {r["kind"]: r for r in result["families"]}
        if name.startswith("bowtie-"):
            bowtie_results[name] = result
        if name.startswith("hinged-pair"):
            hinged_results[name] = result
    primary, direct = degree_results["degree-two-families"], degree_results["degree-two-interfaces"]
    require(primary.keys() == direct.keys(), "degree-two verification program family disagreement")
    for kind in primary:
        for field in ("file", "bytes", "sha256", "templates", "template_states", "boundaries",
                      "directed_interfaces", "minimum_common_cycle_edges", "margins_by_changed_indices"):
            require(primary[kind][field] == direct[kind][field],
                    f"degree-two computation disagreement: {kind} {field}")
    primary = pentagonal_results["pentagonal-reservoirs"]
    direct = pentagonal_results["pentagonal-reservoir-interfaces"]
    require(primary.keys() == direct.keys(), "pentagonal verification program family disagreement")
    for kind in primary:
        for field in primary[kind]:
            if field != "relative_signatures":
                require(primary[kind][field] == direct[kind].get(field),
                        f"pentagonal computation disagreement: {kind} {field}")
    primary = extended_results["extended-cycles"]
    direct = extended_results["extended-cycle-interfaces"]
    require(primary.keys() == direct.keys(), "extended-cycle verification program family disagreement")
    for kind in primary:
        for field, value in primary[kind].items():
            require(value == direct[kind].get(field),
                    f"extended-cycle computation disagreement: {kind} {field}")
    primary_report, direct_report = (bowtie_results["bowtie-families"],
                                     bowtie_results["bowtie-interfaces"])
    primary = {r["family"]: r for r in primary_report["families"]}
    direct = {r["family"]: r for r in direct_report["families"]}
    require(primary.keys() == direct.keys(), "bowtie verification program family disagreement")
    for kind in primary:
        for field, value in primary[kind].items():
            if field != "clique_trees":
                require(value == direct[kind].get(field),
                        f"bowtie computation disagreement: {kind} {field}")
    primary_inputs = {row["file"]: row for row in primary_report["inputs"]}
    for row in direct_report["inputs"]:
        require(primary_inputs.get(row["file"]) == row, "bowtie verification program input hash disagreement")
    primary_report, direct_report = (hinged_results["hinged-pairs"],
                                     hinged_results["hinged-pair-interfaces"])
    primary = {r["family"]: r for r in primary_report["families"]}
    direct = {r["family"]: r for r in direct_report["families"]}
    require(primary.keys() == direct.keys(), "hinged-pair verification program family disagreement")
    for kind in primary:
        for field, value in primary[kind].items():
            if field != "clique_trees":
                require(value == direct[kind].get(field),
                        f"hinged-pair computation disagreement: {kind} {field}")
    primary_inputs = {row["file"]: row for row in primary_report["inputs"]}
    for row in direct_report["inputs"]:
        require(primary_inputs.get(row["file"]) == row, "hinged-pair verification program input hash disagreement")
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
        except VerificationError as error:
            negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
        else:
            raise VerificationError(f"invalid construction accepted: {name}")
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
        except VerificationError as error:
            negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
        else:
            raise VerificationError(f"invalid construction accepted: {name}")
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
            except VerificationError as error:
                negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
            else:
                raise VerificationError(f"invalid construction accepted: {name}")
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
            except VerificationError as error:
                negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
            else:
                raise VerificationError(f"invalid construction accepted: {name}")
    for suite, check in (("families", check_pentagonal_reservoirs),
                         ("interfaces", check_pentagonal_reservoir_interfaces)):
        count_cases = (("missing", remove_block(text, "PENTAGONAL-RESERVOIR-COUNTS")),
                       ("altered", change_block(text, "PENTAGONAL-RESERVOIR-COUNTS",
                                                 "reservoir&715&720&91410&16384&466944&470208&4",
                                                 "reservoir&715&720&91410&16384&466944&470208&3")))
        for mutation, corrupted in count_cases:
            name = mutation + "_pentagonal_counts_" + suite
            require(corrupted != text, "negative case failed to alter pentagonal counts")
            try:
                check(corrupted)
            except VerificationError as error:
                negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
            else:
                raise VerificationError(f"invalid construction accepted: {name}")
    pentagonal_cases = ("missing_boundary", "duplicate_boundary", "missing_component",
                        "missing_state", "duplicate_state", "negative_palette_digit",
                        "short_cycle_word", "illegal_step", "wrong_kind")
    for mutation in pentagonal_cases:
        original = load_pentagonal_family("reservoir")
        corrupted = deepcopy(original)
        if mutation == "missing_boundary":
            corrupted["records"].pop()
        elif mutation == "duplicate_boundary":
            corrupted["records"].append(deepcopy(corrupted["records"][0]))
        elif mutation == "missing_component":
            corrupted["records"][0]["cycles"].pop()
        elif mutation == "missing_state":
            corrupted["records"][0]["cycles"][0].pop()
        elif mutation == "duplicate_state":
            cycle = corrupted["records"][0]["cycles"][0]
            cycle[0] = cycle[1][:]
        elif mutation == "negative_palette_digit":
            corrupted["records"][0]["cycles"][0][0][0] = -1
        elif mutation == "short_cycle_word":
            corrupted["records"][0]["cycles"][0][0].pop()
        elif mutation == "illegal_step":
            cycle = corrupted["records"][0]["cycles"][0]
            cycle[0], cycle[2] = cycle[2], cycle[0]
        else:
            corrupted["kind"] = "pentagon_one_full"
        require(corrupted != original, "negative case failed to alter pentagonal family")
        for suite, check in (("families", check_pentagonal_family),
                             ("interfaces", check_pentagonal_interface_family)):
            name = mutation + "_pentagonal_" + suite
            try:
                check("reservoir", corrupted)
            except VerificationError as error:
                negative.append({"case": name, "status": "REJECTED", "reason": str(error)})
            else:
                raise VerificationError(f"invalid construction accepted: {name}")
    append_extended_negative_cases(text, negative)
    append_bowtie_negative_cases(text, negative)
    append_hinged_negative_cases(text, negative)
    (args.report_dir / "negative-cases.json").write_text(json.dumps(
        {**common, "status": "PASS", "rejected_cases": negative}, indent=2, sort_keys=True) + "\n")
    report = {**common, "status": "PASS", "positive_checks": len(checks),
              "negative_cases_rejected": len(negative),
              "evidence_level": "exact-check",
              "scope": "finite local constructions, shared-hub paths, seven degree-two families, three pentagonal component families, five extended cycle families, bowtie and hinged-pair product cycles and trees of clique blocks, agreement of the ordinary-pentagon product cycles with the listed constructions, and the fixed hinged three-leaf obstruction; independent boundary transitions and 23x23 product/reserve verification are exact checks; arbitrary-order restoration, protected products, degree and face bounds and structural inductions remain analytic"}
    (args.report_dir / "summary.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except VerificationError as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
