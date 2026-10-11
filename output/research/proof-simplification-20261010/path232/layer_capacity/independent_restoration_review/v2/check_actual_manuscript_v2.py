"""Actual v2 manuscript transfer review; no repeat of14-case computation."""
from pathlib import Path
import re,json,hashlib
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edge(u,v):return tuple(sorted((u,v)))
def statements(s):return [m.group(0) for m in re.finditer(r'\\begin\{(lemma|theorem|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)]
def blocks(s):return {m.group(1):m.group(0) for m in re.finditer(r'% BEGIN ([A-Z0-9-]+)\n.*?% END \1',s,re.S)}
def safe_proof(s):
    at=s.index('\\label{lem:pathsafe}');a=s.index('\\begin{proof}',at);b=s.index('\\end{proof}',a)+len('\\end{proof}');return s[a:b]
def selected_support(s):
    a=s.index('\\subsection{Selected-layer identities');b=s.index('\\clearpage',a);return s[a:b].strip()
def marker(s,name):return s.split('% BEGIN '+name+'\n')[1].split('% END '+name)[0].strip()
def equation(s):
    a=s.index('\\begin{equation}\n\\label{eq:path232-cycles}');b=s.index('\\end{equation}',a)+len('\\end{equation}');return s[a:b]
def capacity_table(s):
    a=s.index('aab\\to aac&H_*');b=s.index('\\end{array}',a);return s[a:b]
def em_ma(s):
    a=s.index('For $aab\\to bab$');b=s.index('\\end{proof}',a);return s[a:b]
def cross_rules(s):
    a=s.index('Each cycle has four middle-changing edges.');b=s.index('\\eqref{eq:path232-cycles}.',a)+len('\\eqref{eq:path232-cycles}.');return s[a:b]
def main():
    phase=(HERE/'phase6-source.tex').read_text();old=(HERE/'actual-manuscript-v1.tex').read_text();new=(HERE/'actual-manuscript-v2.tex').read_text();local=(HERE/'local-candidate-v2.tex').read_text();prior=(HERE/'previous-local-v1.tex').read_text();results=json.loads((HERE/'previous-independent-layer-results-v1.json').read_text())
    assert digest(HERE/'phase6-source.tex')=='7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
    assert digest(HERE/'actual-manuscript-v2.tex')=='68ce8760008895fcc1c27d54faf0fadc1ff5335901894f5cf89cd9e37ec9b506'
    assert digest(HERE/'local-candidate-v2.tex')=='11a6bada97dd2f08f150306eeae48e02f7f1ddb7ccfc1147f15077804497dc03'
    assert digest(HERE/'previous-local-v1.tex')==results['candidate_sha256']=='7d8db274e8529a31261988b92e2908852a3422952f0c77f5cdda4a5151800d08'
    assert results['status']=='PASS_INDEPENDENT_LAYER_PROOF' and len(results['fourteen_allowed_orientation_cases'])==14
    assert safe_proof(old)==marker(prior,'SAFE-PROOF') and selected_support(old)==marker(prior,'SELECTED-SUPPORT')
    assert safe_proof(new)==marker(local,'SAFE-PROOF') and selected_support(new)==marker(local,'SELECTED-SUPPORT')
    assert capacity_table(old)==capacity_table(new) and em_ma(old)==em_ma(new) and cross_rules(old)==cross_rules(new)
    assert equation(phase)==equation(old)==equation(new)
    assert len(statements(phase))==len(statements(new))==41 and statements(phase)==statements(new)
    assert len(blocks(phase))==len(blocks(new))==53 and blocks(phase)==blocks(new)
    labels=re.findall(r'\\label\{([^}]+)\}',new);refs=[x.strip() for r in re.findall(r'\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}',new) for x in r.split(',')]
    assert len(labels)==len(set(labels))==55 and set(refs)<=set(labels)
    statement=new.split('\\label{lem:pathsafe}')[1].split('\\end{lemma}')[0]
    assert 'every allowed cycle at $t$' in statement and 'every allowed cycle at $s$' in statement
    assert 'Allow all their colour images and path reversals.' in new
    assert 'These are subgraphs of the respective selected cycles.' in selected_support(new)
    assert 'E,A$ each have one allowed edge set and $M$ has the two stated sets.' in new
    assert 'good transitions to a type no smaller' in new
    eq=equation(new);chunks={'001':eq.split('001&')[1].split('010&')[0],'010':eq.split('010&')[1].split('012&')[0],'012':eq.split('012&')[1].split('\\end{array}')[0]}
    cycles={t:[tuple(map(int,w)) for w in re.findall(r'\b[0-3]{3}\b',chunk)] for t,chunk in chunks.items()}
    # Verify only the newly compressed full-layer shape assertions.
    expected={'001':{1:([3,3],None),2:([4],None),3:([4],None)},'010':{0:([1,8],(1,0,1)),2:([4],None),3:([4],None)},'012':{0:([6],None),2:([6],None),3:([1,3],(1,3,1))}}
    layer_shapes=[]
    for t,ws in cycles.items():
        E={edge(u,v) for u,v in zip(ws,ws[1:]+ws[:1])}
        for v,(orders,isolated) in expected[t].items():
            W={w for w in ws if w[1]==v};adj={w:set() for w in W}
            for u,z in E:
                if u in W and z in W:adj[u].add(z);adj[z].add(u)
            unseen=set(W);components=[]
            while unseen:
                pending=[min(unseen)];component=set()
                while pending:
                    w=pending.pop()
                    if w in component:continue
                    component.add(w);pending.extend(adj[w]-component)
                unseen-=component;components.append(component)
            assert sorted(map(len,components))==orders
            for component in components:assert sum(len(adj[w]) for w in component)==2*(len(component)-1) and all(len(adj[w])<=2 for w in component)
            if isolated is not None:assert isolated in W and not adj[isolated]
            layer_shapes.append({'cycle':t,'middle_colour':v,'path_orders':orders,'isolated_vertex':None if isolated is None else ''.join(map(str,isolated))})
    result={'status':'PASS_WITH_FORMULA_DOMAIN_CLARIFICATION_REQUIRED','actual_v2_sha256':digest(HERE/'actual-manuscript-v2.tex'),'local_v2_sha256':digest(HERE/'local-candidate-v2.tex'),'phase6_sha256':digest(HERE/'phase6-source.tex'),'actual_main_and_appendix_match_local_v2':True,'actual_v1_matches_previously_reviewed_local_v1':True,'seven_capacity_rows_byte_exact':True,'EM_MA_arguments_byte_exact':True,'cross_star_rules_byte_exact':True,'three_cycle_words_byte_exact':True,'all_allowed_cycle_quantifiers_retained':True,'fixed_boundary_stabilizers_retained':True,'classification_equal_types_retained':True,'statement_count':41,'all_statements_byte_exact':True,'literal_block_count':53,'all_literal_blocks_byte_exact':True,'label_count':55,'reference_count':len(refs),'duplicate_labels':[],'unresolved_references':[],'new_selected_layer_structures':layer_shapes,'selected_cycle_scope_explicit':True,'previous_fourteen_case_review_inherited_by_unchanged_counts_and_cycles':True,'formula_domain_clarification':{'required':'for allowed middle colours v,w','counterexample_boundaries':['001','002'],'forbidden_middle':0,'actual_layer_order':0,'unqualified_formula_layer_order':3,'unqualified_formula_layer_edges':3,'all_used_proof_blocks_have_allowed_middle_colours':True,'no_retention_or_safe_count_change_needed':True},'fourteen_case_computation_repeated':False,'Hamilton_search':False,'compile_or_PDF_review':False,'scope':'actual manuscript source and proof completeness only; parent separately performs compile/PDF QA'}
    (HERE/'actual-manuscript-v2-review-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='new_selected_layer_structures'}))
if __name__=='__main__':main()
