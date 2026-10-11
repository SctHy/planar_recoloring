from pathlib import Path
import hashlib,json,re,difflib,shutil
root=Path('/Users/huahua815/Downloads/planar_recoloring')
base=root/'output/research/proof-simplification-20261010';work=base/'continuation-3'
source=root/'planar_recoloring_hamilton_thresholds.tex'
before=(work/'original'/source.name).read_text();after=source.read_text()
stmt=lambda s,k:re.findall(r'\\begin\{('+k+r')\}(.*?)\\end\{\1\}',s,re.S)
assert stmt(before,'theorem|proposition|corollary')==stmt(after,'theorem|proposition|corollary')
removed=('lem:pentagon-list-factor','lem:listed-pentagon-degree')
assert [x for x in stmt(before,'lemma') if not any(k in x[1] for k in removed)]==[x for x in stmt(after,'lemma') if 'lem:pentagon-path-blocks' not in x[1]]
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
old,new=blocks(before),blocks(after)
assert all(new[k]==v for k,v in old.items())
assert set(new)-set(old)=={'MATCHING-CHAIN-00001','HP-00112'}
table=new['MATCHING-CHAIN-00001'];rows=[]
for m in re.finditer(r'^(\d+) & ([0-3]{5}) & ([0-3]{5}) & ([01-]+) & (\d+) & ([0-3]{5}) & ([0-3]{5}) & ([01-]+)\\\\$',table,re.M):
    x=m.groups();rows += [(int(x[0]),x[1],x[2],x[3]),(int(x[4]),x[5],x[6],x[7])]
rows.sort();chain=json.loads((base/'tree_gluing/constant_pool_review/matching-chain-00001-literal.json').read_text())
assert [(a,b) for _,a,b,_ in rows]==[tuple(x) for x in chain['pairs']]
assert [int(x[3]) for x in rows[:-1]]==chain['outgoing_endpoint'] and rows[-1][3]=='--'
hpbody=re.search(r'\\begin\{flushleft\}(.*?)\\end\{flushleft\}',new['HP-00112'],re.S).group(1)
hp=re.findall(r'\b[0-3]{5}\b',hpbody)
assert hp==json.loads((base/'protected_products/traceability_00112/path-results.json').read_text())['path']
labels=set(re.findall(r'\\label\{([^}]+)\}',after))
assert set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',after))<=labels
assert not any(k in after for k in (*removed,'AAE80'))
log=(root/'.latex-build/planar_recoloring_hamilton_thresholds.log').read_text()
warnings=re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$',log,re.M);assert not warnings,warnings
final=work/'final';final.mkdir(exist_ok=True)
files={}
for ext in ('tex','pdf'):
    p=source.with_suffix('.'+ext);shutil.copy2(p,final/p.name)
    files[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
result={'main_result_statements_identical':True,'retained_lemma_statements_identical':True,'removed_auxiliary_lemmas':list(removed),'new_auxiliary_lemma':'lem:pentagon-path-blocks','old_finite_blocks_byte_identical':len(old),'new_certificates_exactly_match_independently_reviewed_literals':True,'all_labels_resolve':True,'AAE_dependency_removed':True,'latex_warnings_overfull_underfull':warnings,'pages':int(re.search(r'Output written on .*?\((\d+) pa\s*ges,',log,re.S).group(1)),'files':files,'evidence_boundary':'literal/source/build verification plus independent analytic and finite-certificate review; not formal verification'}
(work/'source-verification.json').write_text(json.dumps(result,indent=2)+'\n')
(work/'final.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='ten-entry.tex',tofile='ordered-blocks.tex')))
(work/'pdf-visual-qa.json').write_text(json.dumps({'pdf_sha256':files[source.with_suffix('.pdf').name]['sha256'],'pages':result['pages'],'rendered_and_visually_inspected_pages':[21,22,23,32,33],'result':'no clipping, overlap, broken formula or table alignment observed'},indent=2)+'\n')
print(json.dumps(result,indent=2))
