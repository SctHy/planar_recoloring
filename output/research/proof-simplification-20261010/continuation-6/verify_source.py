from pathlib import Path
import hashlib,json,re,difflib,shutil,itertools,sys
root=Path('/Users/huahua815/Downloads/planar_recoloring');base=root/'output/research/proof-simplification-20261010';work=base/'continuation-6'
source=root/'planar_recoloring_hamilton_thresholds.tex';candidate='--candidate' in sys.argv
target=work/'shared-insertion-candidate.tex' if candidate else source
before=(work/'original'/source.name).read_text();after=target.read_text()
stmt=lambda s:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
assert stmt(before)==stmt(after)
assert re.findall(r'\\label\{([^}]+)\}',before)==re.findall(r'\\label\{([^}]+)\}',after)
labels=set(re.findall(r'\\label\{([^}]+)\}',after));assert set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',after))<=labels
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
old,new=blocks(before),blocks(after)
removed=set(old)-set(new);added=set(new)-set(old);changed={k for k in set(old)&set(new) if old[k]!=new[k]}
assert removed=={'PC3-00001'} and added=={'COREPATH-00001'}
assert changed=={'PC2-00001','COMMON-00001','POOL-00001-0','INTERFACES-ALL'}
words=lambda block,n:re.findall(r'\b[0-3]{'+str(n)+r'}\b','\n'.join(x for x in block.splitlines() if not x.startswith('%')))
edge=lambda a,b:tuple(sorted((a,b)))
edges=lambda block:{edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block)}
one=lambda a,b:sum(x!=y for x,y in zip(a,b))==1
def step(a,b):
    return (a[0]==b[0] and one(a[1:],b[1:])) or (a[1:]==b[1:] and abs(int(a[0])-int(b[0]))==1)
seed_results={}
for typ,c2tag,dtag,leafpaths in [('00001','PC2-00001','COMMON-00001',[['12312','12313'],['13212','13213']]),('00112','C2-00112','PORTS-00112',[['12303','12323'],['13203','23203']])]:
    D=edges(new[dtag]);pool=edges(new[f'POOL-{typ}-0']);P=words(new[f'COREPATH-{typ}'],5);C2=words(new[c2tag],6)
    n=44 if typ=='00001' else 51
    states={''.join(x) for x in itertools.product('0123',repeat=5) if all(x[i]!=x[(i+1)%5] and x[i]!=typ[i] for i in range(5))}
    assert len(states)==n and len(C2)==len(set(C2))==2*n and len(P)==len(set(P))==n-4
    assert set(C2)=={str(r)+x for r in range(2) for x in states}
    assert all(step(a,b) for a,b in zip(C2,C2[1:]+C2[:1]))
    assert len(D)==13 and len(pool)==2 and pool<=D
    assert set(P)|{x for p in leafpaths for x in p}==states
    assert all(one(a,b) for a,b in zip(P,P[1:])) and D<={edge(a,b) for a,b in zip(P,P[1:])}
    paths=leafpaths+[P];cuts={edge(p[0],p[-1]):p for p in paths};assert len({x for c in cuts for x in c})==6 and not(set(cuts)&D)
    for r in range(2):
        retained={edge(a[1:],b[1:]) for a,b in zip(C2,C2[1:]+C2[:1]) if a[0]==b[0]==str(r)};assert D<=retained
    derived=[];seen=set()
    for a,b in zip(C2,C2[1:]+C2[:1]):
        derived.append(a);k=edge(a[1:],b[1:])
        if a[0]==b[0]=='1' and k in cuts:
            p=cuts[k];p=p if p[0]==a[1:] else p[::-1];derived.extend('2'+x for x in p);seen.add(k)
    assert seen==set(cuts) and len(derived)==len(set(derived))==3*n
    assert set(derived)=={str(r)+x for r in range(3) for x in states}
    assert all(step(a,b) for a,b in zip(derived,derived[1:]+derived[:1]))
    for r in range(3):
        retained={edge(a[1:],b[1:]) for a,b in zip(derived,derived[1:]+derived[:1]) if a[0]==b[0]==str(r)};assert D<=retained
    if typ=='00001':
        peer=(base/'protected_products/row_insert_00001/candidate-v2.tex').read_text();cw,pw=re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}',peer,re.S)
        assert C2==cw.split() and P==pw.split()
        Kold=edges(old[dtag])-edges(old['POOL-00001-0']);Knew=D-pool
        assert len(Knew)==11 and Knew==(Kold-{edge('12313','12323'),edge('13230','23230')})|{edge('13120','23120')}
    seed_results[typ]={'states':n,'C2_words':2*n,'core_path_words':n-4,'generated_C3_words':3*n,'common_ports':13,'pool_edges':2,'K_edges':11,'all_row_protection_and_every_step_verified':True}

records=lambda s:re.findall(r'([0-4]{5}:[01]) ([0-4]) ([0-3]) ([0-4]{5}:[01]) ([0-3]{5}-[0-3]{5})',s)
orig=records(old['INTERFACES-ALL']);curr=records(new['INTERFACES-ALL']);assert len(orig)==len(curr)==283
patches={('00001:0','1','3','00102:0'):'21313-21323',('00001:0','4','2','00001:0'):'13120-23120',('00001:0','4','3','00001:0'):'12310-32310'}
assert curr==[(*x[:4],patches.get(x[:4],x[4])) for x in orig]
standard=['00000','00001','00011','00012','00101','00102','00112','00121','00123','01012','01023','00004','00014','00104','00114','00124','01014','01024','01104','01124','01204','01234']
def normalize(t):
    for s in range(5):
        for eps in (1,-1):
            for p in itertools.permutations('0123'):
                n=''.join('4' if t[(s+eps*i)%5]=='4' else p[int(t[(s+eps*i)%5])] for i in range(5))
                if n in standard:return n,(s,eps,p)
    raise AssertionError(t)
def restore(x,g):
    s,eps,p=g;out=['']*5
    for i,c in enumerate(x):out[(s+eps*i)%5]=str(p.index(c))
    return ''.join(out)
constants=words(new['FACTOR-00000'],5);K={}
for typ in standard:
    for comp in range(2 if typ=='00000' else 1):
        if typ=='00000':w=constants[15*comp:15*(comp+1)];support={edge(a,b) for a,b in zip(w,w[1:]+w[:1])}
        elif typ in ('00001','00112'):support=edges(new['COMMON-00001' if typ=='00001' else 'PORTS-00112'])
        else:w=words(new[('FHC-' if '4' in typ else 'C1-')+typ],5);support={edge(a,b) for a,b in zip(w,w[1:]+w[:1])}
        K[f'{typ}:{comp}']=support-edges(new[f'POOL-{typ}-{comp}'])
affected=[x for x in curr if x[0]=='00001:0' or x[3]=='00001:0'];assert len(affected)==24
for source_id,j,q,target_id,witness in affected:
    t=list(source_id[:5]);t[int(j)]=q;n,g=normalize(''.join(t));assert n==target_id[:5]
    restored={edge(restore(a,g),restore(b,g)) for a,b in K[target_id]}
    assert tuple(witness.split('-')) in K[source_id]&restored,(source_id,j,q,target_id,witness)
critical={edge('31212','31232'),edge('12132','32132'),edge('21313','21323'),edge('13123','23123')}
assert critical<=K['00001:0'] and new['CONSTANT-INTERFACE-FAMILIES']==old['CONSTANT-INTERFACE-FAMILIES']
assert '$|D_A|=19$' not in after and 'seven-edge pool' not in after
result={'all_mathematical_statements_identical':True,'all_labels_identical_and_refs_resolve':True,'unchanged_old_finite_blocks':len(old)-len(removed)-len(changed),'changed_old_blocks':sorted(changed),'removed_old_block':sorted(removed),'new_block':sorted(added),'shared_three_path_insertion_rule':True,'seeds':seed_results,'individual_interface_records':283,'changed_individual_witnesses':3,'affected00001_records_verified':24,'unaffected_literal_records_inherited':259,'six_constant_families_four_target_memberships_verified':True,'expanded_standard_source_interface_cases':313,'source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'evidence_boundary':'reviewed analytic construction and exact source-certificate readback; not formal verification'}
if not candidate:
    assert after==(work/'shared-insertion-candidate.tex').read_text()
    log=(root/'.latex-build/planar_recoloring_hamilton_thresholds.log').read_text();warnings=re.findall(r'^.*(?:Warning:|Overfull|Underfull|^!).*$',log,re.M);assert not warnings,warnings
    result['latex_warnings_overfull_underfull']=warnings;result['pages']=int(re.search(r'Output written on .*?\((\d+) pa\s*ges,',log,re.S).group(1))
    final=work/'final';final.mkdir(exist_ok=True);files={}
    for ext in ('tex','pdf'):
        p=source.with_suffix('.'+ext);shutil.copy2(p,final/p.name);files[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
    result['files']=files;shutil.copy2(root/'.latex-build/planar_recoloring_hamilton_thresholds.log',work/'final-latex.log')
(work/('candidate-source-verification.json' if candidate else 'source-verification.json')).write_text(json.dumps(result,indent=2)+'\n')
(work/'final.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='phase5.tex',tofile='phase6.tex')))
print(json.dumps(result,indent=2))
