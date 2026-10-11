#!/usr/bin/env python3
"""Check that compact v2 retains the frozen count/profile statements."""
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    candidate = BASE / 'table-free-safe-proof-candidate-v2.tex'
    text = candidate.read_text()
    source = BASE / 'table-free-safe-proof-results-v1.json'
    prior = json.loads(source.read_text())
    assert prior['verdict'] == 'PASS'
    rows = re.findall(r'(aab|abc|aba)\\to (aac|acb|cab|abd|bab|cba)&'
                      r'(\d+)&(\d+)&(\d+)&(\d+)&(\d+)&(\d+)', text)
    expected = [(rec['family'][0], rec['family'][1], *map(str, rec['n_m_f_qcap_Rfloor_bound']))
                for rec in prior['retention_families']]
    assert rows == expected
    prose = re.sub(r'\s+', '', text)
    phrases = [
        '$w=c,v=c,u=c,u=b$inducerespectively$P_4,P_4,P_3\\cupP_2,2P_2$',
        '$v=a,u=b,w=d,u=c$inducerespectively$P_6,P_4\\cupP_3,P_3\\cupP_2,P_3\\cupP_1$',
        '$u=b,w=b,u=c,w=c$inducerespectively$P_3\\cup2P_2,P_5\\cupP_2,P_3\\cupP_2,P_4\\cupP_1$',
    ]
    for phrase in phrases:
        assert phrase in prose, phrase
    for edge in ('$bab$--$cab$', '$bab$--$dab$', '$bab$--$bac$', '$bab$--$bad$', '$dad$--$dcd$'):
        assert edge in text, edge
    result = {
        'verdict': 'PASS', 'scope': 'Compact v2 six count rows and twelve coordinate-class profiles match the frozen full proof v1.',
        'candidate_sha256': sha(candidate), 'script_sha256': sha(Path(__file__)),
        'full_proof_sha256': prior['candidate_sha256'],
        'full_proof_record': {source.name: sha(source)},
        'six_count_rows': rows,
        'profile_compression': 'All literal paths are retained in full proof v1; v2 uses exactly their component sizes.',
        'math_scope': 'Every original allowed cycle is preserved; no arbitrary-Hamilton-cycle claim.',
        'new_cycle_search': False,
    }
    out = BASE / 'table-free-safe-proof-v2-readback.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verdict': result['verdict'], 'candidate_sha256': result['candidate_sha256']}))


if __name__ == '__main__':
    main()
