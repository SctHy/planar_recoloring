from pathlib import Path
import hashlib,json,re,shutil,difflib
root=Path('/Users/huahua815/Downloads/planar_recoloring')
base=root/'output/research/proof-simplification-20261010';work=base/'continuation-4'
source=root/'planar_recoloring_hamilton_thresholds.tex';before=source.read_text()
assert hashlib.sha256(source.read_bytes()).hexdigest()=='8a8d683dfafb5c09c3b7d3357eaaaba8c44958393f958c94fa7d9d296f583cc3'
(work/'original').mkdir(exist_ok=True);manifest={}
for ext in ('tex','pdf'):
    p=source.with_suffix('.'+ext);shutil.copy2(p,work/'original'/p.name)
    manifest[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
(work/'original-manifest.json').write_text(json.dumps({'files':manifest},indent=2)+'\n')
after=before
def replace(old,new):
    global after
    assert after.count(old)==1,(old,after.count(old))
    after=after.replace(old,new)
replace('The new literal words, pools and all 313 interface records appear in','The literal words, pools and all 313 interface cases appear in')
replace(r'''For a Hamilton component $A$ with specified cycle $C_A$, designate an
ordered pool of eight edges of $C_A$, and let $K_A$ be the other cycle
edges. The first two pool edges join copies of $C_A$ in a two- or
three-row path product; the last six supply splice reserves.''',r'''For a Hamilton component $A$ with specified cycle $C_A$, designate an
ordered pool of five edges for either constant component, and eight
edges otherwise. Let $K_A$ be the other cycle edges. The first two
pool edges join copies of $C_A$ in a two- or three-row path product;
the remaining edges supply at least two splice reserves.''')
replace(r'''Its last six edges supply splice reserves. All pool
edges are distinct.''',r'''Any two pool edges supply splice reserves. All pool edges are distinct.''')
replace(r'''Every initial cycle retains $K_A$ and the same last six pool edges
in every physical row.''',r'''Every initial cycle retains $K_A$ and at least two common reserve
edges in every physical row.''')
replace('path rows; any two of the last six pool edges supply block-chain reserves.','path rows; any two remaining pool edges supply block-chain reserves.')
replace(r'''For each standard source component, each non-star position, each
different new excluded colour and each overlapping normalized target
component, the appendix gives an actual edge in both protected sets.
There are 313 records. Checking membership of the two five-digit
endpoints in the specified cycles and outside their pools proves
each record directly. Applying the inverse coordinate and colour maps
gives every labelled case.''',r'''For the 313 standard-source interfaces, the appendix gives 283
individual common edges and six constant-source parameter families
covering the other 30 cases. Checking the five-digit endpoints in
the specified cycles and outside their pools proves each individual
record. The six families follow from two possible normalizing
directions and four protected target edges, as shown there. Applying
the inverse coordinate and colour maps gives every labelled case.''')

pool0='12123-13123 12312-12313 21231-31231 23121-23131 31212-31312'
pool1='12132-13132 13212-13213 21213-21313 21321-31321 32121-32131'
for i, words in enumerate((pool0,pool1)):
    pattern=rf'(% BEGIN POOL-00000-{i}\n)(.*?)(% END POOL-00000-{i})'
    body=r'\begingroup\footnotesize\ttfamily\begin{flushleft}'+'\n'+words+r'\\'+'\n'+r'\end{flushleft}\endgroup'+'\n'
    after,n=re.subn(pattern,lambda m:m.group(1)+body+m.group(3),after,flags=re.S);assert n==1

pattern=r'% BEGIN INTERFACES-ALL\n(.*?)% END INTERFACES-ALL'
oldbody=re.search(pattern,after,re.S).group(1)
records=re.findall(r'([0-4]{5}:\d) ([0-4]) ([0-3]) ([0-4]{5}:\d) ([0-3]{5}-[0-3]{5})',oldbody)
assert len(records)==313
nonconstant=[x for x in records if not x[0].startswith('00000:')];assert len(nonconstant)==283
replacement=('00001:0','4','0','00000:1')
assert sum(x[:4]==replacement for x in nonconstant)==1
nonconstant=[(*x[:4],'12132-32132') if x[:4]==replacement else x for x in nonconstant]
lines=[r'\begingroup\scriptsize\ttfamily\begin{flushleft}']
for i in range(0,len(nonconstant),2):
    lines.append(' ; '.join(' '.join(x) for x in nonconstant[i:i+2])+r'\\')
lines.append(r'\end{flushleft}\endgroup')
after=re.sub(pattern,lambda m:'% BEGIN INTERFACES-ALL\n'+'\n'.join(lines)+'\n% END INTERFACES-ALL',after,flags=re.S)
replace(r'\paragraph{All 313 single-pentagon interfaces.}',r'\paragraph{The 283 nonconstant-source interfaces.}')
excerpt=(base/'tree_gluing/constant_pool_review/two_orientation_appendix_v2.tex').read_text()
start=excerpt.index(r'\paragraph{The thirty constant-source interfaces.}')
end=excerpt.index(' The other 283 records remain individual;',start)
excerpt=excerpt[start:end]+'\n'
excerpt=excerpt.replace(r'''Each five-edge pool $O_i$ is a rotation orbit, so $K_i$ is invariant''',r'''Coordinate rotation fixes both components, since its order is five.
Each five-edge pool $O_i$ is a rotation orbit, so $K_i$ is invariant''')
extra='% BEGIN CONSTANT-INTERFACE-FAMILIES\n'+excerpt+'% END CONSTANT-INTERFACE-FAMILIES\n\n'
after=after.replace(r'\paragraph{The 283 nonconstant-source interfaces.}',extra+r'\paragraph{The 283 nonconstant-source interfaces.}')
replace('and 313 interfaces, with at least ten common states per interface.', 'and 313 interface cases, with at least ten common states per interface. The constant-source cases are supplied by six parameter families; the other 283 retain individual edge records.')

stmt=lambda s:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)
assert stmt(before)==stmt(after)
assert re.findall(r'\\label\{([^}]+)\}',before)==re.findall(r'\\label\{([^}]+)\}',after)
blocks=lambda s:{m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$',s,re.S|re.M)}
old,new=blocks(before),blocks(after);changed={k for k,v in old.items() if new[k]!=v}
assert changed=={'POOL-00000-0','POOL-00000-1','INTERFACES-ALL'}
assert set(new)-set(old)=={'CONSTANT-INTERFACE-FAMILIES'}
(work/'constant-family-candidate.tex').write_text(after)
(work/'candidate.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='ordered-blocks.tex',tofile='constant-families.tex')))
(work/'candidate-integrity.json').write_text(json.dumps({'all_statements_identical':True,'all_labels_identical':True,'unchanged_old_finite_blocks':len(old)-len(changed),'changed_old_blocks':sorted(changed),'new_block':'CONSTANT-INTERFACE-FAMILIES','individual_records':283,'constant_parameter_families':6,'expanded_standard_source_interfaces':313,'candidate_sha256':hashlib.sha256(after.encode()).hexdigest()},indent=2)+'\n')
print('Candidate written; main source untouched.')
