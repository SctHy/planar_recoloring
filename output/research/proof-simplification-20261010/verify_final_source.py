from pathlib import Path
import difflib, hashlib, json, re

root = Path('/Users/huahua815/Downloads/planar_recoloring')
work = root / 'output/research/proof-simplification-20261010'
path = root / 'planar_recoloring_hamilton_thresholds.tex'
baseline = (work / 'original' / path.name).read_text()
current = path.read_text()
statements = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
before, after = statements(baseline), statements(current)
assert len(before) == len(after)
changed_statements = []
for old, new in zip(before, after):
    if old != new:
        assert r'\label{lem:pentagon-list-factor}' in old[1]
        assert r'\label{lem:pentagon-list-factor}' in new[1]
        changed_statements.append('lem:pentagon-list-factor')
assert changed_statements == ['lem:pentagon-list-factor']
labels = lambda s: set(re.findall(r'\\label\{([^}]+)\}', s))
old_labels, new_labels = labels(baseline), labels(current)
assert old_labels - new_labels == {'tab:pentagon-factors'}
assert not new_labels - old_labels
refs = set(re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', current))
assert refs <= new_labels
cites = {key.strip() for block in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', current) for key in block.split(',')}
bibs = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', current))
assert cites <= bibs
blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$', s, re.S | re.M)}
old_blocks, new_blocks = blocks(baseline), blocks(current)
removed = {key for key in old_blocks if key.startswith('FACTOR-') and key != 'FACTOR-00000'}
removed |= {'C2-00001', 'C3-00001', 'PORTS-00001'}
assert set(old_blocks) - set(new_blocks) == removed
assert not set(new_blocks) - set(old_blocks)
assert all(value == old_blocks[key] for key, value in new_blocks.items())
candidate_path = work / 'path232' / 'compact12-candidate.tex'
candidate_arrays = re.findall(r'\\begin\{array\}.*?\\end\{array\}', candidate_path.read_text(), re.S)
cycle_part = current[current.index(r'\label{eq:path232-cycles}'):]
table_part = current[current.index(r'\label{tab:path232-safe-edges}'):]
assert re.search(r'\\begin\{array\}.*?\\end\{array\}', cycle_part, re.S).group(0) == candidate_arrays[0]
assert re.search(r'\\begin\{array\}.*?\\end\{array\}', table_part, re.S).group(0) == candidate_arrays[1].replace(r'\!\text{--}\!', r'\text{--}')
manifest = json.loads((work / 'original-manifest.json').read_text())
for name, metadata in manifest['files'].items():
    original = work / 'original' / name
    assert hashlib.sha256(original.read_bytes()).hexdigest() == metadata['sha256']
    assert original.stat().st_size == metadata['bytes']
log = root / '.latex-build' / 'planar_recoloring_hamilton_thresholds.log'
bad = re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$', log.read_text(), re.M)
assert not bad, bad
result = {
    'all_main_theorem_corollary_proposition_statements_identical': True,
    'other_lemma_statements_identical': True,
    'replacement_auxiliary_lemma': changed_statements,
    'lemma_and_theorem_counts_unchanged': True,
    'no_dangling_references_or_citations': True,
    'retained_pentagon_finite_blocks_byte_identical': len(new_blocks),
    'protected_interfaces_byte_identical': 'INTERFACES-ALL' in new_blocks,
    'path_cycles_and_twelve_entry_table_match_reviewed_candidate': True,
    'path_candidate_sha256': hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
    'retained_block_sha256': {key:hashlib.sha256(value.encode()).hexdigest() for key,value in new_blocks.items()},
    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'pdf_sha256': hashlib.sha256(path.with_suffix('.pdf').read_bytes()).hexdigest(),
    'source_bytes_before': len(baseline.encode()),
    'source_bytes_after': path.stat().st_size,
    'latex_warnings_overfull_underfull': bad,
    'pdf_pages': int(re.search(r'Output written on .*?\((\d+) pa\s*ges,', log.read_text(), re.S).group(1)),
    'source_artifact': str(path),
    'original_manifest': 'original-manifest.json',
    'original_source_and_pdf_verified_unchanged': True,
    'evidence_boundary': 'source and build integrity, not formal mathematical verification or external peer review'
}
(work / 'final-source-verification.json').write_text(json.dumps(result, indent=2) + '\n')
(work / 'final-proof-simplification.diff').write_text(''.join(difflib.unified_diff(baseline.splitlines(True), current.splitlines(True), fromfile='before-research.tex', tofile='after-research.tex')))
print(json.dumps({key:value for key,value in result.items() if key not in {'retained_block_sha256'}}, indent=2))
