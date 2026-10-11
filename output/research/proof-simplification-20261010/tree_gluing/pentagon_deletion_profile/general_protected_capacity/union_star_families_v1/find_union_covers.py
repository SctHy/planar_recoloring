"""Exact finite mask compression; no neighbour-generation or cycle operations."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import platform
import time

BASE = Path(__file__).resolve().parent
INPUT = BASE/'frozen-both-hc-local-results.json'
start = time.perf_counter()
data = json.loads(INPUT.read_text())
groups = defaultdict(list)
for r in data['records']:
    if r['covered']:
        good = [c for c in r['certificates'] if c['forbidden_common_count'] == 0
                and c['source_degree'] + c['target_degree'] - c['common_incident_count'] <= 3]
        assert good, r['interface']
        groups[r['interface']['source']].append((r['interface'], good))
assert sum(map(len, groups.values())) == 125
families = {}
for t, rs in sorted(groups.items()):
    masks = defaultdict(int)
    for i, (_, cs) in enumerate(rs):
        for c in cs:
            masks[c['state']] |= 1 << i
    full = (1 << len(rs))-1
    # After processing each word, store the shortest, lexicographically first
    # subset for each achieved mask. Losing longer subsets cannot improve an
    # extension, since all future words have the same marginal mask effect.
    dp = {0: ()}
    transitions = 0
    for w, mask in sorted(masks.items()):
        updated = dict(dp)
        for oldmask, selected in dp.items():
            transitions += 1
            newmask = oldmask | mask
            new = selected + (w,)
            old = updated.get(newmask)
            if old is None or (len(new), new) < (len(old), old):
                updated[newmask] = new
        dp = updated
    selected = dp[full]
    coverage = []
    for i, (interface, cs) in enumerate(rs):
        witnesses = sorted(c['state'] for c in cs if c['state'] in selected)
        assert witnesses
        c = next(c for c in cs if c['state'] == witnesses[0])
        coverage.append({'interface_index': i, 'interface': interface,
                         'selected_state': witnesses[0],
                         'all_selected_covering_states': witnesses,
                         'certificate': c})
    families[t] = {'covered_cases': len(rs), 'candidate_words': len(masks),
                   'candidate_masks': dict(sorted(masks.items())),
                   'minimum_members': len(selected), 'selected_words': list(selected),
                   'mask_states_reached': len(dp), 'dp_transitions': transitions,
                   'coverage': coverage}
members = sum(x['minimum_members'] for x in families.values())
distinct = len({w for x in families.values() for w in x['selected_words']})
rows = [r'\paragraph{Three-edge-union source selectors (125 interfaces).}',
        r'\[\begin{array}{c|l}t&S_t\\\hline']
for t, f in families.items():
    rows.append(t+'&'+r',\ '.join(f['selected_words'])+r'\\')
rows.append(r'\end{array}\]')
(BASE/'source-selector-table.tex').write_text('\n'.join(rows)+'\n')
result = {'status':'PASS', 'python':platform.python_version(),
          'input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),
          'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'source_families':len(families), 'covered_interfaces':125,
          'minimum_members_per_family_sum':members, 'selected_distinct_words':distinct,
          'original_individual_records':283, 'remaining_individual_records_proposed':158,
          'old_individual_endpoint_words':566,
          'new_endpoint_plus_family_word_memberships':316+members,
          'new_endpoint_plus_distinct_family_words':316+distinct,
          'elapsed_seconds':time.perf_counter()-start, 'families':families,
          'limits':['Exact minimum for each source among frozen pool-free local certificates.',
                    'No joint global distinct-word optimization, changed pools, alternative mechanism or main edit.',
                    'Full actual-source independent pool/normalizer/component review still required.']}
(BASE/'union-source-cover-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'families'}))
print(json.dumps({t:{k:v for k,v in f.items() if k not in ('coverage','candidate_masks')} for t,f in families.items()},indent=2))
