"""Independent exact readback of the two protected-capacity scopes.

The only external data are a frozen full manuscript and frozen result JSONs.
No peer code is imported. No intersection of the two edge bases is taken.
"""
from pathlib import Path
from itertools import product, permutations, combinations
from collections import Counter
import hashlib
import json
import re
import sys
import time

HERE = Path(__file__).resolve().parent
STANDARD = ('00000', '00001', '00011', '00012', '00101', '00102',
            '00112', '00121', '00123', '01012', '01023', '00004',
            '00014', '00104', '00114', '00124', '01014', '01024',
            '01104', '01124', '01204', '01234')
HARD = {'00001', '00112'}
EXPECTED_SOURCE = '7a90f79db489447b0bad3019217fd369a5cc25986288247981cbe7f3462acba3'
PERMS = tuple(permutations(range(4)))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def edge(x, y):
    return tuple(sorted((x, y)))

def coordinate(e):
    changes = [j for j in range(5) if e[0][j] != e[1][j]]
    assert len(changes) == 1
    return changes[0]

def raw_edges(vertices):
    return {edge(x, y) for x, y in combinations(sorted(vertices), 2)
            if sum(a != b for a, b in zip(x, y)) == 1}

def counts(edges):
    c = Counter(coordinate(e) for e in edges)
    return [c[j] for j in range(5)]

def endpoints(edges):
    return {v for e in edges for v in e}

def legal(t):
    return {''.join(map(str, x)) for x in product(range(4), repeat=5)
            if all(x[j] != x[(j+1) % 5] for j in range(5))
            and all(t[j] == '4' or x[j] != int(t[j]) for j in range(5))}

def normalize(t):
    for start in range(5):
        for sign in (1, -1):
            for p in PERMS:
                out = ''.join('4' if t[(start+sign*j) % 5] == '4'
                              else str(p[int(t[(start+sign*j) % 5])])
                              for j in range(5))
                if out in STANDARD:
                    return out, [start, sign, list(p)]
    raise AssertionError(t)

def restore(word, g):
    start, sign, p = g
    out = [''] * 5
    for j in range(5):
        out[(start+sign*j) % 5] = str(p.index(int(word[j])))
    return ''.join(out)

def move_edges(edges, g):
    return {edge(restore(x, g), restore(y, g)) for x, y in edges}

def case_key(c):
    return (c['source'], c['changed_position'], c['new_colour'], c['target'])

def main():
    begin = time.monotonic()
    source_path = HERE / 'phase6-source.tex'
    assert sha(source_path) == EXPECTED_SOURCE
    text = source_path.read_text()
    blocks = dict(re.findall(r'^% BEGIN ([^\n]+)\n(.*?)^% END \1$', text, re.S | re.M))
    def words(name):
        return re.findall(r'\b[0-3]{5}\b', blocks[name])
    def pairs(name):
        return {edge(x, y) for x, y in re.findall(r'\b([0-3]{5})-([0-3]{5})\b', blocks[name])}
    def cycle(ws):
        assert len(ws) == len(set(ws))
        result = {edge(x, ws[(j+1) % len(ws)]) for j, x in enumerate(ws)}
        assert len(result) == len(ws)
        for e in result:
            coordinate(e)
        return result
    components = {}
    support_shapes = {}
    for t in STANDARD:
        if t == '00000':
            ws = words('FACTOR-00000')
            partitions = [set(ws[:15]), set(ws[15:])]
            bases = [cycle(ws[:15]), cycle(ws[15:])]
        elif t in HARD:
            partitions = [legal(t)]
            bases = [pairs('COMMON-00001' if t == '00001' else 'PORTS-00112')]
        else:
            ws = words(('FHC-' if '4' in t else 'C1-') + t)
            partitions = [set(ws)]
            bases = [cycle(ws)]
        assert set().union(*partitions) == legal(t)
        for index, (vertices, base) in enumerate(zip(partitions, bases)):
            p = pairs(f'POOL-{t}-{index}')
            assert p <= base and endpoints(base) <= vertices
            k = base - p
            components[f'{t}:{index}'] = (vertices, base, p, k)
            if t in HARD:
                v = endpoints(k); h = raw_edges(v)
                support_shapes[t] = {
                    'full_fibre_vertices': len(vertices), 'protected_vertices': len(v),
                    'protected_edges': len(k), 'support_edges': len(h),
                    'K_counts': counts(k), 'H_counts': counts(h),
                    'extra_edges': sorted(h-k)}
    assert len(components) == 23
    assert support_shapes['00001']['K_counts'] == [5,2,0,2,2]
    assert support_shapes['00001']['H_counts'] == [6,2,1,4,4]
    assert support_shapes['00112']['K_counts'] == [3,1,3,2,2]
    assert support_shapes['00112']['H_counts'] == [4,3,3,4,3]
    for shape in support_shapes.values():
        assert (shape['protected_vertices'], shape['protected_edges'], shape['support_edges']) == (20,11,17)

    expected_base = json.loads((HERE/'expected-baseline.json').read_text())
    expected_support = json.loads((HERE/'expected-port-support.json').read_text())
    base_by_key = {case_key(c):c for c in expected_base['cases']}
    port_by_key = {case_key(c):c for c in expected_support['cases']}
    seen = set()
    totals = {}
    for source, (va, a, p, k) in components.items():
        t = source[:5]
        for j in range(5):
            if t[j] == '4':
                continue
            for q in range(4):
                if str(q) == t[j]:
                    continue
                nt, g = normalize(t[:j]+str(q)+t[j+1:])
                for target, (vb0, b0, q0, l0) in components.items():
                    if target[:5] != nt:
                        continue
                    vb = {restore(v, g) for v in vb0}
                    u = va & vb
                    if not u:
                        continue
                    b, qq, l = move_edges(b0,g), move_edges(q0,g), move_edges(l0,g)
                    h = raw_edges(u); fset = (p|qq) & h
                    aa,bb,mm,ff,ra,rb = map(counts,(a&h,b&h,h,fset,a&fset,b&fset))
                    coarse = [aa[z]+bb[z]-mm[z]-ff[z] for z in range(5)]
                    refined = [aa[z]+bb[z]-mm[z]-ra[z]-rb[z]+ff[z] for z in range(5)]
                    key = (source,j,q,target)
                    assert key not in seen
                    seen.add(key)
                    e = base_by_key[key]
                    for field, actual in [('normalizer',g),('a',aa),('b',bb),('m',mm),('f',ff),('rA',ra),('rB',rb),('coarse_bounds',coarse),('refined_bounds',refined)]:
                        assert e[field] == actual, (key,field)
                    w = endpoints(k) & endpoints(l)
                    assert w <= u
                    hh = raw_edges(w); fp = (p|qq) & hh
                    x,y,m,f,rk,rl = map(counts,(k&hh,l&hh,hh,fp,k&fp,l&fp))
                    plain = [x[z]+y[z]-m[z] for z in range(5)]
                    strong = [plain[z]-rk[z]-rl[z]+f[z] for z in range(5)]
                    assert all(strong[z] >= refined[z] for z in range(5))
                    e = port_by_key[key]
                    for field, actual in [('normalizer',g),('joint_port_support_states',len(w)),('x',x),('y',y),('m_prime',m),('f_prime',f),('rK',rk),('rL',rl),('plain_support_bounds',plain),('refined_support_bounds',strong)]:
                        assert e[field] == actual, (key,field)
                    group = 'constant-source-30' if source.startswith('00000') else (
                        'nonconstant-source-hard-53' if source[:5] in HARD or nt in HARD else 'HH-230')
                    assert e['group'] == group
                    r = totals.setdefault(group, Counter())
                    r.update(total=1, baseline_coarse=max(coarse)>0, baseline_refined=max(refined)>0,
                             support_plain=max(plain)>0, support_refined=max(strong)>0)
    assert seen == set(base_by_key) == set(port_by_key) and len(seen) == 313
    assert totals['HH-230']['support_refined'] == 222
    assert totals['nonconstant-source-hard-53']['support_plain'] == 53
    assert totals['constant-source-30']['support_plain'] == 30
    result = {'status':'PASS_BOUNDED_TWO_SCOPE_READBACK','source_sha256':sha(source_path),
              'backend_version':sys.version.split()[0],'cases':len(seen),
              'all_case_fields_match':True,'coverage_by_group':totals,
              'hard_support_shapes':support_shapes,
              'actual_basis_edge_intersection_computed':False,'HC_search':False,
              'scope':'313 fixed standard interfaces. Inequalities are general; coverage is finite supporting evidence.',
              'expected_baseline_sha256':sha(HERE/'expected-baseline.json'),
              'expected_support_sha256':sha(HERE/'expected-port-support.json'),
              'code_sha256':sha(Path(__file__)),'elapsed_seconds':time.monotonic()-begin}
    (HERE/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='hard_support_shapes'},indent=2))

if __name__ == '__main__':
    main()
