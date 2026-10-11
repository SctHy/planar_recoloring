"""Root literal/partition audit for236 fixed-K/opposite-HC replacements."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

p=argparse.ArgumentParser()
p.add_argument('--source', required=True)
p.add_argument('--pdf', required=True)
p.add_argument('--output', required=True)
a=p.parse_args()
stage=Path(__file__).resolve().parent
research=stage.parent
root=research.parents[2]
oldpath=stage/'original/planar_recoloring_hamilton_thresholds.tex'
phase8=research/'continuation-8/final/planar_recoloring_hamilton_thresholds.tex'
original46=research/'original/planar_recoloring_hamilton_thresholds.tex'
source,pdf=Path(a.source).resolve(),Path(a.pdf).resolve()
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
assert sha(oldpath)=='ecea0571029a8527630442b2242bc21ec76f67bc44b2f768b9228c5f494203a9'
assert sha(phase8)=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
old,new,original=oldpath.read_text(),source.read_text(),original46.read_text()
stmts=lambda s:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
primary=lambda s:re.findall(r'\\begin\{(theorem|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
assert stmts(old)==stmts(new) and len(stmts(new))==41
assert primary(original)==primary(new) and len(primary(new))==14
blocklemma=lambda s:next(x for _,x in stmts(s) if '\\label{lem:block-subcubic}' in x)
assert blocklemma(original)==blocklemma(new)
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.M|re.S)}
bo,bn,b8=blocks(old),blocks(new),blocks(phase8.read_text())
assert bo.keys()==bn.keys() and len(bn)==53
assert all(bo[k]==bn[k] for k in bo if k!='INTERFACES-ALL')
pattern=r'([0-4]{5}):(\d) ([0-4]) ([0-3]) ([0-4]{5}):(\d) ([0-3]{5})-([0-3]{5})'
ro,rn,r8=(re.findall(pattern,z['INTERFACES-ALL']) for z in (bo,bn,b8))
assert len(ro)==158 and len(rn)==47 and len(r8)==283
assert len(set(rn))==47 and set(rn)<=set(ro)<=set(r8)
ref=research/'tree_gluing/pentagon_deletion_profile/general_protected_capacity/one_protected_selector_feasibility_v1/saved-one-protected-selector-results.json'
assert sha(ref)=='af2beada94b56cebc1ac100cbb751a10a7124c7d161601c897bba83f4cc5520b'
data=json.loads(ref.read_text())['all236']
keys=set()
for f in data['families'].values():
    for q in f['coverage']:
        z=q['interface']
        keys.add((z['source'],str(z['source_component']),str(z['position']),str(z['colour']),z['target_type'],str(z['target_component'])))
assert len(keys)==236
removed=set(r8)-set(rn)
assert {q[:6] for q in removed}==keys
previous={q[:6] for q in set(r8)-set(ro)}
assert len(previous)==125 and previous<=keys
table=re.search(r'\\paragraph\{Fixed-side source selectors \(236 interfaces\)\.\}.*?\\begin\{array\}\{c\|l\}(.*?)\\end\{array\}',new,re.S)
assert table
actual={t:re.findall(r'(?<!\d)[0-3]{5}(?!\d)',row) for t,row in re.findall(r'([0-4]{5})&([^\n]+)',table.group(1))}
expected={t:f['usable_words'] for t,f in data['families'].items()}
assert actual==expected and len(actual)==21
assert sum(map(len,actual.values()))==78
assert len({w for v in actual.values() for w in v})==47
hard={'00001','00112'}
hardhard={q[:6] for q in r8 if q[0] in hard and q[4] in hard}
assert len(hardhard)==5 and hardhard<={q[:6] for q in rn}
normal=lambda s:re.search(r'Here is the exact normalization convention\..*?In particular a standard boundary first normalizes by the identity\.',s,re.S).group(0)
assert normal(old)==normal(new)
eq=lambda s:re.search(r'\\begin\{equation\}\n\\label\{eq:path232-cycles\}.*?\\end\{equation\}',s,re.S).group(0)
assert eq(old)==eq(new)
labels=lambda s:re.findall(r'\\label\{([^}]+)\}',s)
assert labels(old)==labels(new) and len(set(labels(new)))==len(labels(new))
refs=re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',new)
assert set(refs)<=set(labels(new))
cites={x.strip() for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',new) for x in g.split(',')}
assert cites<=set(re.findall(r'\\bibitem\{([^}]+)\}',new))
pages=int(re.search(r'^Pages:\s*(\d+)',subprocess.check_output(['/opt/homebrew/bin/pdfinfo',str(pdf)],text=True),re.M).group(1))
r={'verdict':'PASS','stage':'continuation-10','source_sha256':sha(source),'pdf_sha256':sha(pdf),
   'phase9_statements_byte_exact':41,'original46_primary_statements_byte_exact':14,
   'original46_block_subcubic_statement_byte_exact':True,'unchanged_literal_blocks':52,
   'changed_literal_blocks':['INTERFACES-ALL'],'individual_interfaces':47,
   'additional_individual_witnesses_removed_since_phase9':111,'fixedK_HC_cases':236,
   'constant_family_cases':30,'complete_partition':313,'previous125_replacement_cases_all_retained':True,
   'actual21_rows_match_frozen_selectors':True,'selector_row_memberships':78,'distinct_selector_words':47,
   'all5_hardhard_interfaces_remain_individual':True,'normalization_byte_exact':True,
   'path232_cycle_equation_byte_exact':True,'labels_unchanged':len(labels(new)),
   'refs':len(refs),'all_references_and_citations_resolve':True,'pages':pages,
   'scope':'Root actual-source invariant/partition audit. Independentactual236g/d/neighbour/K/pool review supplies mathematical local checks; globalclassification andremainingcertificates inherited. No main mutation by checker.'}
Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
