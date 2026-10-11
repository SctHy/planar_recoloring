from pathlib import Path
import hashlib,json,re,difflib,shutil
root=Path('/Users/huahua815/Downloads/planar_recoloring')
base=root/'output/research/proof-simplification-20261010';work=base/'continuation-4'
source=root/'planar_recoloring_hamilton_thresholds.tex'
before=(work/'original'/source.name).read_text();after=source.read_text();candidate=(work/'constant-family-candidate.tex').read_text()
assert after.replace('\\par\\needspace{16\\baselineskip}\n','')==candidate
stmt=lambda s:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
assert stmt(before)==stmt(after)
assert re.findall(r'\\label\{([^}]+)\}',before)==re.findall(r'\\label\{([^}]+)\}',after)
labels=set(re.findall(r'\\label\{([^}]+)\}',after))
assert set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',after))<=labels
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
old,new=blocks(before),blocks(after);changed={k for k,v in old.items() if new[k]!=v}
assert changed=={'POOL-00000-0','POOL-00000-1','INTERFACES-ALL'}
assert set(new)-set(old)=={'CONSTANT-INTERFACE-FAMILIES'}
records=lambda s:re.findall(r'([0-4]{5}:\d) ([0-4]) ([0-3]) ([0-4]{5}:\d) ([0-3]{5}-[0-3]{5})',s)
orig=records(old['INTERFACES-ALL']);curr=records(new['INTERFACES-ALL']);assert len(orig)==313 and len(curr)==283
expected=[x for x in orig if not x[0].startswith('00000:')]
expected=[(*x[:4],'12132-32132') if x[:4]==('00001:0','4','0','00000:1') else x for x in expected]
assert curr==expected
log=(root/'.latex-build/planar_recoloring_hamilton_thresholds.log').read_text()
warnings=re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$',log,re.M);assert not warnings,warnings
final=work/'final';final.mkdir(exist_ok=True);files={}
for ext in ('tex','pdf'):
    p=source.with_suffix('.'+ext);shutil.copy2(p,final/p.name)
    files[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
result={'all_mathematical_statements_identical':True,'all_labels_identical_and_refs_resolve':True,'unchanged_old_finite_blocks':len(old)-len(changed),'changed_old_blocks':sorted(changed),'new_block':'CONSTANT-INTERFACE-FAMILIES','individual_records':283,'parameter_families':6,'representative_entries':289,'expanded_standard_source_interface_cases':313,'reviewed_candidate_sha256':hashlib.sha256(candidate.encode()).hexdigest(),'final_differs_from_reviewed_candidate_only_in_table_keep_space_command':True,'latex_warnings_overfull_underfull':warnings,'pages':int(re.search(r'Output written on .*?\((\d+) pa\s*ges,',log,re.S).group(1)),'files':files,'evidence_boundary':'source/build and reviewed finite/analytic identity; not formal verification'}
(work/'source-verification.json').write_text(json.dumps(result,indent=2)+'\n')
(work/'final.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='ordered-blocks.tex',tofile='constant-families.tex')))
(work/'pdf-visual-qa.json').write_text(json.dumps({'pdf_sha256':files[source.with_suffix('.pdf').name]['sha256'],'pages':result['pages'],'final_layout_rendered_and_visually_inspected_pages':[37,39,40,42],'main_proof_pages_21_22_also_inspected_before_appendix_only_layout_adjustment':True,'result':'no clipping, overlap, broken formula or table alignment observed'},indent=2)+'\n')
shutil.copy2(root/'.latex-build/planar_recoloring_hamilton_thresholds.log',work/'final-latex.log')
print(json.dumps(result,indent=2))
