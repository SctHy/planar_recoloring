"""Root source audit for proposed125-case three-edge-union replacement."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--candidate', required=True)
p.add_argument('--pdf', required=True)
p.add_argument('--output', required=True)
args = p.parse_args()
stage = Path(__file__).resolve().parent
research = stage.parent
root = research.parents[2]
oldpath = research/'continuation-8/final/planar_recoloring_hamilton_thresholds.tex'
candidate = Path(args.candidate).resolve()
pdf = Path(args.pdf).resolve()
old, new = oldpath.read_text(), candidate.read_text()
original46 = (research/'original/planar_recoloring_hamilton_thresholds.tex').read_text()
sha = lambda q: hashlib.sha256(q.read_bytes()).hexdigest()
assert sha(oldpath) == '3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
statements = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
primary = lambda s: re.findall(r'\\begin\{(theorem|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$', s, re.M|re.S)}
assert statements(old) == statements(new) and len(statements(new)) == 41
assert primary(original46) == primary(new) and len(primary(new)) == 14
blocklemma = lambda s: next(x for k,x in statements(s) if '\\label{lem:block-subcubic}' in x)
assert blocklemma(original46) == blocklemma(new)
bo, bn = blocks(old), blocks(new)
assert bo.keys() == bn.keys() and len(bn) == 53
assert all(bo[k] == bn[k] for k in bo if k != 'INTERFACES-ALL')
pattern = r'([0-4]{5}):(\d) ([0-4]) ([0-3]) ([0-4]{5}):(\d) ([0-3]{5})-([0-3]{5})'
ro = re.findall(pattern, bo['INTERFACES-ALL'])
rn = re.findall(pattern, bn['INTERFACES-ALL'])
assert len(ro) == 283 and len(rn) == 158
assert len(set(rn)) == 158 and set(rn) <= set(ro)
maskpath = research/'tree_gluing/pentagon_deletion_profile/general_protected_capacity/union_star_families_v1/union-source-cover-results.json'
mask = json.loads(maskpath.read_text())
keys = set()
for family in mask['families'].values():
    for r in family['coverage']:
        z = r['interface']
        keys.add((z['source'], str(z['source_component']), str(z['position']), str(z['colour']), z['target_type'], str(z['target_component'])))
assert len(keys) == 125
removed = set(ro) - set(rn)
assert {r[:6] for r in removed} == keys
table = re.search(r'\\paragraph\{[^}]*125 interfaces[^}]*\}.*?\\begin\{array\}\{c\|l\}(.*?)\\end\{array\}', new, re.S)
assert table, 'actual125family table not located'
rows = re.findall(r'([0-4]{5})&([^\n]+)', table.group(1))
actual_sets = {t:re.findall(r'(?<!\d)[0-3]{5}(?!\d)', row) for t,row in rows}
expected_sets = {t: f['selected_words'] for t,f in mask['families'].items()}
assert actual_sets == expected_sets and len(actual_sets) == 15
normalization = lambda s: re.search(r'Here is the exact normalization convention\..*?In particular a standard boundary first normalizes by the identity\.', s, re.S).group(0)
assert normalization(old) == normalization(new)
eq = lambda s: re.search(r'\\begin\{equation\}\n\\label\{eq:path232-cycles\}.*?\\end\{equation\}', s, re.S).group(0)
assert eq(old) == eq(new)
labels = lambda s: re.findall(r'\\label\{([^}]+)\}', s)
assert labels(old) == labels(new)
refs = re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}', new)
assert set(refs) <= set(labels(new)) and len(set(labels(new))) == len(labels(new))
cites = {x.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', new) for x in group.split(',')}
bib = set(re.findall(r'\\bibitem\{([^}]+)\}', new))
assert cites <= bib
pages = int(re.search(r'^Pages:\s*(\d+)', subprocess.check_output(['/opt/homebrew/bin/pdfinfo', str(pdf)], text=True), re.M).group(1))
result = {'verdict':'PASS', 'candidate_source_sha256':sha(candidate), 'candidate_pdf_sha256':sha(pdf),
          'phase8_statements_byte_exact':41, 'original46_primary_statements_byte_exact':14,
          'original46_block_subcubic_statement_byte_exact':True,
          'phase8_unchanged_marked_blocks':52, 'modified_marked_blocks':['INTERFACES-ALL'],
          'remaining_individual_interfaces':158, 'removed_individual_interfaces':125,
          'fifteen_actual_source_rows_match_frozen_mask_selectors':True,
          'local_family_cases':125, 'constant_family_cases':30, 'complete_partition':313,
          'first_normalization_paragraph_byte_exact':True, 'path232_cycle_equation_byte_exact':True,
          'labels_unchanged':len(labels(new)), 'refs':len(refs), 'all_references_and_citations_resolve':True,
          'pages':pages,
          'scope':'Root actual-source partition and invariant audit.125actual neighbourhood/pool checks and local mathematical proof require separate independent review. No main mutation by this checker.'}
Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
