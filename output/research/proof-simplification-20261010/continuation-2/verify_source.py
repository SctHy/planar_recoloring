from pathlib import Path
import difflib, hashlib, json, re

root = Path('/Users/huahua815/Downloads/planar_recoloring')
base = root / 'output/research/proof-simplification-20261010'
work = base / 'continuation-2'
path = root / 'planar_recoloring_hamilton_thresholds.tex'
before = (work / 'original' / path.name).read_text()
after = path.read_text()
statements = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
assert statements(before) == statements(after)
assert re.findall(r'\\label\{([^}]+)\}', before) == re.findall(r'\\label\{([^}]+)\}', after)
labels = set(re.findall(r'\\label\{([^}]+)\}', after))
assert set(re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', after)) <= labels
blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$', s, re.S | re.M)}
assert blocks(before) == blocks(after)
arrays = re.findall(r'\\begin\{array\}.*?\\end\{array\}', (base/'path232/compact12-candidate.tex').read_text(), re.S)
cycles = re.search(r'\\begin\{array\}.*?\\end\{array\}', after[after.index(r'\label{eq:path232-cycles}'):], re.S).group(0)
table = re.search(r'\\begin\{array\}.*?\\end\{array\}', after[after.index(r'\label{tab:path232-safe-edges}'):], re.S).group(0)
expected = arrays[1].replace(r'\!\text{--}\!', r'\text{--}')
row = r'010&020&301\text{--}302,\ 132\text{--}232&103\text{--}303,\ 302\text{--}303\\' + '\n'
assert expected.count(row) == 1
assert table == expected.replace(row, '')
assert cycles == arrays[0]
manifest = json.loads((work/'original-manifest.json').read_text())
for name, metadata in manifest['files'].items():
    original = work/'original'/name
    assert hashlib.sha256(original.read_bytes()).hexdigest() == metadata['sha256']
    assert original.stat().st_size == metadata['bytes']
log = (root/'.latex-build/planar_recoloring_hamilton_thresholds.log').read_text()
warnings = re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$', log, re.M)
assert not warnings, warnings
result = {
    'all_theorem_lemma_proposition_corollary_statements_identical': True,
    'all_labels_identical': True, 'no_dangling_refs': True,
    'all_pentagon_finite_blocks_byte_identical': len(blocks(after)),
    'symmetric_cycle_words_byte_identical': True,
    'ten_entry_table_exactly_reviewed_twelve_entry_table_minus_MM': True,
    'mathematical_replacement': 'M--M common square, two sets of three of four edges',
    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'pdf_sha256': hashlib.sha256(path.with_suffix('.pdf').read_bytes()).hexdigest(),
    'pdf_pages': int(re.search(r'Output written on .*?\((\d+) pa\s*ges,', log, re.S).group(1)),
    'latex_warnings_overfull_underfull': warnings,
    'evidence_boundary':'source/build identity plus reviewed analytic proof; not formal verification'
}
(work/'source-verification.json').write_text(json.dumps(result,indent=2)+'\n')
(work/'final.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='twelve-entry.tex',tofile='analytic-MM-plus-ten-entry.tex')))
print(json.dumps(result,indent=2))
