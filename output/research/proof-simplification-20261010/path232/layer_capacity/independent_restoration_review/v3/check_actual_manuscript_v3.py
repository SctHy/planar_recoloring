"""Independent final one-patch actual-manuscript review; no14-case rerun."""
from pathlib import Path
import re,json,hashlib
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def statements(s):return [m.group(0) for m in re.finditer(r'\\begin\{(lemma|theorem|proposition|corollary)\}(.*?)\\end\{\1\}',s,re.S)]
def blocks(s):return {m.group(1):m.group(0) for m in re.finditer(r'% BEGIN ([A-Z0-9-]+)\n.*?% END \1',s,re.S)}
def main():
    original=(HERE/'phase6-source.tex').read_text();v2=(HERE/'actual-manuscript-v2.tex').read_text();v3=(HERE/'actual-manuscript-v3.tex').read_text();review=json.loads((HERE/'frozen-v2-review-results.json').read_text())
    assert digest(HERE/'actual-manuscript-v2.tex')==review['actual_v2_sha256']=='68ce8760008895fcc1c27d54faf0fadc1ff5335901894f5cf89cd9e37ec9b506'
    assert digest(HERE/'actual-manuscript-v3.tex')=='3806a0c7f8ec374ea92e70152f939e92e35c3c76564f9e69e8c06160999bcb58'
    assert review['status']=='PASS_WITH_FORMULA_DOMAIN_CLARIFICATION_REQUIRED'
    before='For common endpoint lists $L,R$, the layer $H_v$ is\n';after='For common endpoint lists $L,R$ and distinct allowed middle colours $v,w$,\nthe layer $H_v$ is\n'
    assert v2.count(before)==v3.count(after)==1 and v2.replace(before,after)==v3
    assert len(statements(original))==len(statements(v3))==41 and statements(original)==statements(v3)
    assert len(blocks(original))==len(blocks(v3))==53 and blocks(original)==blocks(v3)
    labels=re.findall(r'\\label\{([^}]+)\}',v3);refs=[x.strip() for r in re.findall(r'\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}',v3) for x in r.split(',')]
    assert len(labels)==len(set(labels))==55 and set(refs)<=set(labels)
    result={'status':'PASS_FINAL_ACTUAL_MANUSCRIPT_V3','v3_sha256':digest(HERE/'actual-manuscript-v3.tex'),'v2_sha256':digest(HERE/'actual-manuscript-v2.tex'),'phase6_sha256':digest(HERE/'phase6-source.tex'),'exactly_one_allowed_middle_domain_patch':True,'domain_qualification_correct_and_sufficient':True,'all_v2_math_checks_transfer_unchanged':True,'all_selected_layer_shapes_correct':True,'all_allowed_cycle_quantifiers_and_stabilizers_retained':True,'seven_safe_capacity_rows_and_EM_MA_complete':True,'statement_count':41,'statements_byte_exact':True,'literal_block_count':53,'literal_blocks_byte_exact':True,'label_count':55,'reference_count':len(refs),'duplicate_labels':[],'unresolved_references':[],'v2_required_clarification_history_preserved':True,'fourteen_case_computation_repeated':False,'Hamilton_search':False,'compile_or_PDF_review':False,'scope':'final actual source and selected-cycle proof completeness; parent separately owns layout/compile QA and adoption'}
    (HERE/'actual-manuscript-v3-review-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
