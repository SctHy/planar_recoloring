from pathlib import Path
import hashlib, json, re, shutil, subprocess, difflib

base = Path(__file__).resolve().parent
research = base.parent
root = research.parents[2]
main = root/'planar_recoloring_hamilton_thresholds.tex'
pdf = root/'planar_recoloring_hamilton_thresholds.pdf'
oldpath = base/'original'/main.name
candidate = base/'path232-candidate/layer-capacity-manuscript-candidate-v3.tex'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
old,new,original46 = oldpath.read_text(),main.read_text(),(research/'original'/main.name).read_text()
assert sha(oldpath)=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
assert sha(main)==sha(candidate)=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
statements = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
primary = lambda s: re.findall(r'\\begin\{(theorem|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
blocks = lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.M|re.S)}
assert statements(old)==statements(new) and len(statements(new))==41
assert primary(original46)==primary(new) and len(primary(new))==14
blocklemma = lambda s:next(x for k,x in statements(s) if '\\label{lem:block-subcubic}' in x)
assert blocklemma(original46)==blocklemma(new)
assert blocks(old)==blocks(new) and len(blocks(new))==53
eq = lambda s:re.search(r'\\begin\{equation\}\n\\label\{eq:path232-cycles\}.*?\\end\{equation\}',s,re.S).group(0)
assert eq(old)==eq(new)
labels = lambda s:re.findall(r'\\label\{([^}]+)\}',s)
assert labels(new)==[x for x in labels(old) if x!='tab:path232-safe-edges']
refs = re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',new)
assert set(refs)<=set(labels(new)) and len(set(labels(new)))==len(labels(new))
cites = set(x.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',new) for x in group.split(','))
bib = set(re.findall(r'\\bibitem\{([^}]+)\}',new))
assert cites<=bib
log = (root/'.latex-build/planar_recoloring_hamilton_thresholds.log').read_text()
warnings = re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$',log,re.M)
assert not warnings,warnings
pages = int(re.search(r'^Pages:\s*(\d+)',subprocess.check_output(['/opt/homebrew/bin/pdfinfo',str(pdf)],text=True),re.M).group(1))
assert pages==42
result={'verdict':'PASS','stage':'continuation-8','adopted_candidate_version':'v3',
 'main_equals_reviewed_candidate_byte_exact':True,'primary_math_statements_vs_phase6_exact':41,
 'original46_theorems_propositions_corollaries_exact':14,'original46_block_subcubic_statement_exact':True,
 'phase6_literal_marked_blocks_exact':53,'three_path232_cycles_equation_exact':True,
 'only_removed_phase6_label':'tab:path232-safe-edges','labels':len(labels(new)),
 'refs':len(refs),'all_refs_resolve':True,'all_citations_resolve':True,
 'latex_warnings_overfull_underfull':warnings,'pages':pages,
 'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in (main,pdf)},
 'evidence_boundary':'Actual adopted-source readback and clean compilation. Selected-cycle symbolic proof separately reviewed; unchanged finite C5 input inherited. No formal verification or general C5 four-colour theorem.'}
(base/'source-verification.json').write_text(json.dumps(result,indent=2)+'\n')
(base/'adopted.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='phase6.tex',tofile='phase8.tex')))
shutil.copy2(root/'.latex-build/planar_recoloring_hamilton_thresholds.log',base/'final-latex.log')
(base/'final').mkdir(exist_ok=True)
for p in (main,pdf):shutil.copy2(p,base/'final'/p.name)
print(json.dumps(result,indent=2))
