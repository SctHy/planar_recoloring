#!/usr/bin/env python3
"""Independent exhaustive subset check for two small saved-word-mask families."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'saved-one-protected-selector-results.json'


def run():
    saved = json.loads(INPUT.read_text())
    checked = []
    for source in ('00001', '00112'):
        family = saved['all236']['families'][source]
        masks = family['candidate_masks']
        full = (1 << family['covered_cases']) - 1
        selected = tuple(family['selected_new_words'])
        checked_subsets = 0
        first = None
        for cardinality in range(len(selected)+1):
            for words in combinations(sorted(masks), cardinality):
                checked_subsets += 1
                union = 0
                for word in words:
                    union |= masks[word]
                if union == full:
                    first = words
                    break
            if first is not None:
                break
        assert first == selected
        checked.append({'source': source, 'candidate_words': len(masks),
                        'covered_interfaces': family['covered_cases'],
                        'minimum_members': len(first), 'first_minimum_words': list(first),
                        'subsets_checked': checked_subsets})
    # Boundary: an old selector word can cover every extra interface for a
    # source, so an exact minimum of zero additional words must be permitted.
    zero_additional = []
    for source in ('00121', '00124'):
        family = saved['extra111_with_retained_union48']['families'][source]
        full = (1 << family['covered_cases']) - 1
        union = 0
        for word in family['retained_words']:
            union |= family['candidate_masks'].get(word, 0)
        assert union == full and family['minimum_new_members'] == 0
        zero_additional.append(source)
    result = {'status': 'PASS', 'python': platform.python_version(),
              'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'independent_exhaustive_subset_checks': checked,
              'zero_additional_word_boundary_sources': zero_additional,
              'scope': 'Two small frozen mask families and two zero-addition boundaries only; no graph, normalization or HC operations.'}
    (HERE / 'small-mask-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
