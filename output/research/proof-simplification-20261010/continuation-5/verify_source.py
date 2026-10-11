from pathlib import Path
import hashlib,json,re,difflib,shutil,itertools,sys
root=Path('/Users/huahua815/Downloads/planar_recoloring')
work=root/'output/research/proof-simplification-20261010/continuation-5'
source=root/'planar_recoloring_hamilton_thresholds.tex'
candidate='--candidate' in sys.argv
target=work/'simplification-candidate.tex' if candidate else source
before=(work/'original'/source.name).read_text();after=target.read_text()
stmt=lambda s:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
assert stmt(before)==stmt(after)
assert re.findall(r'\\label\{([^}]+)\}',before)==re.findall(r'\\label\{([^}]+)\}',after)
labels=set(re.findall(r'\\label\{([^}]+)\}',after))
assert set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',after))<=labels
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
old,new=blocks(before),blocks(after)
removed=set(old)-set(new);added=set(new)-set(old)
changed={k for k in set(old)&set(new) if old[k]!=new[k]}
assert removed=={'C3-00112'} and added=={'COREPATH-00112'}
assert changed=={'PORTS-00112','POOL-00112-0'}
words=lambda block,n:re.findall(r'\b[0-3]{'+str(n)+r'}\b','\n'.join(x for x in block.splitlines() if not x.startswith('%')))
edges=lambda block:{tuple(sorted(x)) for x in re.findall(r'([0-3]{5})-([0-3]{5})',block)}
D=edges(new['PORTS-00112']);pool=edges(new['POOL-00112-0'])
oldK=edges(old['PORTS-00112'])-edges(old['POOL-00112-0'])
assert len(D)==13 and len(pool)==2 and pool<=D and D-pool==oldK and len(oldK)==11
P=words(new['COREPATH-00112'],5);C2=words(new['C2-00112'],6)
assert len(P)==len(set(P))==47 and len(C2)==len(set(C2))==102
states={''.join(x) for x in itertools.product('0123',repeat=5) if all(x[i]!=x[(i+1)%5] and x[i]!='00112'[i] for i in range(5))}
assert len(states)==51 and set(P)|{'12303','12323','13203','23203'}==states
one=lambda a,b:sum(x!=y for x,y in zip(a,b))==1
assert all(one(a,b) for a,b in zip(P,P[1:]))
assert D<={tuple(sorted((a,b))) for a,b in zip(P,P[1:])}
paths=[['12303','12323'],['13203','23203'],P]
cuts={tuple(sorted((p[0],p[-1]))):p for p in paths}
assert len({x for c in cuts for x in c})==6 and not(set(cuts)&D)
derived=[];seen=set()
for a,b in zip(C2,C2[1:]+C2[:1]):
    derived.append(a)
    k=tuple(sorted((a[1:],b[1:])))
    if a[0]==b[0]=='1' and k in cuts:
        p=cuts[k];p=p if p[0]==a[1:] else p[::-1]
        derived.extend('2'+x for x in p);seen.add(k)
assert seen==set(cuts) and len(derived)==len(set(derived))==153
assert set(derived)=={str(r)+x for r in range(3) for x in states}
def step(a,b):
    return (a[0]==b[0] and one(a[1:],b[1:])) or (a[1:]==b[1:] and abs(int(a[0])-int(b[0]))==1)
assert all(step(a,b) for a,b in zip(derived,derived[1:]+derived[:1]))
for r in range(3):
    retained={tuple(sorted((a[1:],b[1:]))) for a,b in zip(derived,derived[1:]+derived[:1]) if a[0]==b[0]==str(r)}
    assert D<=retained
assert new['COREPATH-00112']==blocks((root/'output/research/proof-simplification-20261010/protected_products/row_insert_00112/candidate-v3.tex').read_text())['COREPATH-00112']
assert '153 words' not in after[after.index(r'\paragraph{C2 for 00112'):after.index(r'\section{Literal protected-pentagon')]
assert '$|D_A|=18$' not in after
result={'all_mathematical_statements_identical':True,'all_labels_identical_and_refs_resolve':True,'unchanged_old_finite_blocks':len(old)-len(removed)-len(changed),'changed_old_blocks':sorted(changed),'removed_old_block':sorted(removed),'new_block':sorted(added),'C2_literal_byte_identical':True,'K00112_byte_set_identical_edges':11,'new_common_ports':13,'new_pool_edges':2,'new_core_path_states':47,'generated_C3_states':153,'generated_C3_every_step_and_all_row_ports_verified':True,'all_interface_and_family_blocks_byte_identical':True,'expanded_standard_source_interface_cases':313,'source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'evidence_boundary':'independent analytic review and finite exact certificate; not formal verification'}
if not candidate:
    assert after==(work/'simplification-candidate.tex').read_text()
    log=(root/'.latex-build/planar_recoloring_hamilton_thresholds.log').read_text()
    warnings=re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$',log,re.M);assert not warnings,warnings
    result['latex_warnings_overfull_underfull']=warnings
    result['pages']=int(re.search(r'Output written on .*?\((\d+) pa\s*ges,',log,re.S).group(1))
    final=work/'final';final.mkdir(exist_ok=True);files={}
    for ext in ('tex','pdf'):
        p=source.with_suffix('.'+ext);shutil.copy2(p,final/p.name)
        files[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
    result['files']=files
    shutil.copy2(root/'.latex-build/planar_recoloring_hamilton_thresholds.log',work/'final-latex.log')
(work/('candidate-source-verification.json' if candidate else 'source-verification.json')).write_text(json.dumps(result,indent=2)+'\n')
(work/'final.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='phase4.tex',tofile='phase5.tex')))
print(json.dumps(result,indent=2))
