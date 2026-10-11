"""Exact exploration of only the manuscript's path232 local kernel."""
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLORS = tuple(range(4))
WORDS = {
    (0,0,1): '120 123 323 313 213 210 230 130 132 232 212 312 310 320',
    (0,1,0): '101 102 103 203 303 323 123 121 321 301 302 202 201 231 232 132 131',
    (0,1,2): '101 121 120 320 321 323 123 103 203 303 301 201 231 230 130 131',
}

def edge(x, y):
    return tuple(sorted((x, y)))

def edges(word):
    return frozenset(edge(x,y) for x,y in zip(word, word[1:]+word[:1]))

def states(t):
    return frozenset((u,v,w) for u,v,w in itertools.product(COLORS, repeat=3)
                     if u != v and v != w and u != t[0] and v != t[1] and w != t[2])

def kind(t):
    if len(set(t)) == 3:
        return 'A'
    if t[0] == t[2]:
        return 'M'
    return 'E'

def bad_squares(a):
    return {c: frozenset((u,c,w) for u,w in itertools.product(COLORS, repeat=2)
                         if u not in (a,c) and w not in (a,c))
            for c in COLORS if c != a}

def square_edges(q):
    return frozenset(edge(x,y) for x,y in itertools.combinations(q,2)
                     if sum(a != b for a,b in zip(x,y)) == 1)

def special(t):
    if kind(t) != 'E':
        return frozenset()
    a = t[1]
    b = t[0] if t[0] != a else t[2]
    result = set()
    for c,q in bad_squares(a).items():
        if c != b:
            result.update(e for e in square_edges(q) if set(e) <= states(t))
    assert len(result) == 2
    return frozenset(result)

def serialize(e):
    return [''.join(map(str,x)) for x in e]

def main():
    both = len(sys.argv)>1 and sys.argv[1]=='--symmetric-both'
    variant = both or (len(sys.argv)>1 and sys.argv[1]=='--symmetric-middle')
    if variant:
        WORDS[(0,1,0)] = '101 121 321 323 123 103 303 302 301 201 203 202 102 132 232 231 131'
    if both:
        WORDS[(0,1,2)] = '131 101 103 203 303 301 201 231 230 130 120 123 323 320 321 121'
    cycles = {}
    for t0, word in WORDS.items():
        w0 = tuple(tuple(map(int,x)) for x in word.split())
        for p in itertools.permutations(COLORS):
            for rev in (False,True):
                t = tuple(p[c] for c in t0)
                w = tuple(tuple(p[c] for c in x) for x in w0)
                if rev:
                    t = t[::-1]
                    w = tuple(x[::-1] for x in w)
                assert len(w) == len(set(w)) and set(w) == states(t)
                ee = edges(w)
                assert all(sum(a != b for a,b in zip(*e)) == 1 for e in ee)
                cycles.setdefault(t,{})[ee] = w
    assert len(cycles) == 60
    assert sum(map(len,cycles.values())) == (72 if both else 96 if variant else 120)
    safe = {t: {ee: ee-special(t) for ee in cc} for t,cc in cycles.items()}
    support_checks = 0
    for t,cc in cycles.items():
        if kind(t)=='A':
            continue
        a = t[0] if kind(t)=='M' else t[1]
        b = t[1] if kind(t)=='M' else (t[0] if t[0]!=a else t[2])
        for ce in cc:
            assert special(t) <= ce
            for c,q in bad_squares(a).items():
                count = len(ce & square_edges(q))
                assert count == ((0 if c==b else 3) if kind(t)=='M' else (2 if c==b else 1))
                support_checks += 1
    forced = {t: frozenset.intersection(*ss.values()) for t,ss in safe.items()}
    minimum = {}
    minimum_internal = {}
    minimum_pivot = {}
    forced_failures = []
    interface_checks = 0
    interface_failures = []
    for t, cc in cycles.items():
        for s, dd in cycles.items():
            differences = [j for j in range(3) if t[j] != s[j]]
            if len(differences) != 1 or t >= s:
                continue
            coordinate = 'middle' if differences[0] == 1 else 'end'
            family = '-'.join(sorted((kind(t),kind(s))))+'/'+coordinate
            count = len(forced[t] & forced[s])
            if count < 2:
                forced_failures.append({'t': t, 's': s, 'count': count,
                                        'edges': [serialize(e) for e in sorted(forced[t]&forced[s])]})
            for ce in cc:
                for de in dd:
                    common = safe[t][ce] & safe[s][de]
                    if len(common) < 2:
                        interface_failures.append({'t':t,'s':s,'common_count':len(common),
                            'source_cycle': [''.join(map(str,x)) for x in cc[ce]],
                            'target_cycle': [''.join(map(str,x)) for x in dd[de]],
                            'common_safe_edges': [serialize(e) for e in sorted(common)]})
                    interface_checks += 1
                    minimum[family] = min(minimum.get(family,100),len(common))
                    internal = {e for e in common if e[0][1] == e[1][1]}
                    minimum_internal[family] = min(minimum_internal.get(family,100),len(internal))
                    if set((kind(t),kind(s))) == {'E','M'}:
                        tm = t if kind(t)=='M' else s
                        pivot = {e for e in internal if e[0][1] == tm[0]}
                        minimum_pivot[family] = min(minimum_pivot.get(family,100),len(pivot))

    reservation_profiles = {}
    for t, cc in cycles.items():
        if kind(t) == 'A':
            continue
        a = t[0] if kind(t) == 'M' else t[1]
        sq = {c: square_edges(q) for c,q in bad_squares(a).items()}
        profiles = {}
        for ce in cc:
            for reserved in [None]+sorted(safe[t][ce]):
                av = {c: ce&ee-({reserved} if reserved is not None else set()) for c,ee in sq.items()}
                signature = tuple((c,tuple(sorted(ee))) for c,ee in sorted(av.items()))
                profiles[signature] = (ce,reserved,av)
        reservation_profiles[t] = profiles
    block_checks = 0
    for a in COLORS:
        bad = (a,a,a)
        neighbours = [t for t in reservation_profiles if sum(x != y for x,y in zip(t,bad)) == 1]
        assert len(neighbours) == 9
        for t,s in itertools.combinations(neighbours,2):
            for _,rl,al in reservation_profiles[t].values():
                for _,rr,ar in reservation_profiles[s].values():
                    sl = {c for c,ee in al.items() if ee}
                    sr = {c for c,ee in ar.items() if ee}
                    assert len(sl) >= 2 and len(sr) >= 2 and sl|sr == set(COLORS)-{a}
                    if kind(t) == kind(s) == 'E':
                        bl = t[0] if t[0] != a else t[2]
                        br = s[0] if s[0] != a else s[2]
                        c = min(set(COLORS)-{a,bl,br})
                    else:
                        c = min(sl&sr)
                    assert any(el != er for el in al[c] for er in ar[c])
                    assert all(d in sl|sr for d in set(COLORS)-{a,c})
                    block_checks += 1

    output = {
        'domain': 'only the four-colour path232 local fibres and the literal cycle images',
        'evidence_level': 'bounded-check',
        'good_boundaries': len(cycles),
        'allowed_cycles': sum(map(len,cycles.values())),
        'cycle_family': 'symmetric-both' if both else 'symmetric-middle' if variant else 'original',
        'safe_interface_cycle_pairs_checked': interface_checks,
        'safe_interface_failures': interface_failures[:5],
        'safe_interface_failure_count':len(interface_failures),
        'minimum_common_safe_edges_by_type_and_coordinate': minimum,
        'minimum_same_middle_common_safe_edges_by_type_and_coordinate': minimum_internal,
        'minimum_E_M_pivot_middle_common_safe_edges': minimum_pivot,
        'forced_safe_edge_sizes_by_kind': {
            k: sorted({len(forced[t]) for t in cycles if kind(t)==k}) for k in ('E','M','A')},
        'forced_safe_edge_proposal_counterexamples': forced_failures[:5],
        'forced_safe_edge_proposal_failed_interfaces': len(forced_failures),
        'bad_singleton_reservation_profiles_checked': block_checks,
        'bad_square_support_counts_checked':support_checks,
        'conclusion': 'The support-set construction always chooses a valid bridge square and covers every remaining square. Forced edges alone do not replace all image-dependent safe-interface cases.',
    }
    filename = 'symmetric-both-results.json' if both else 'symmetric-middle-results.json' if variant else 'results.json'
    (ROOT/filename).write_text(json.dumps(output,indent=2)+'\n')
    if both:
        targets = {
            (0,0,1): [(0,0,2),(0,0,3),(0,1,1),(0,2,1),(0,3,1),(1,0,1),(2,0,1),(3,0,1)],
            (0,1,0): [(0,1,2),(0,1,3),(0,2,0),(0,3,0),(2,1,0),(3,1,0)],
            (0,1,2): [(0,1,3),(0,3,2),(3,1,2)],
        }
        def canonical_cycle(t, rev=False):
            k = kind(t)
            if k=='E':
                a=t[1]; b=t[0] if t[0]!=a else t[2]
                h=sorted(set(COLORS)-{a,b}); p=(a,b,*h)
                base=(0,0,1); rev=t[0]!=a
            elif k=='M':
                a=t[0]; b=t[1]; h=sorted(set(COLORS)-{a,b}); p=(a,b,*h)
                base=(0,1,0)
            else:
                p=(*t,next(iter(set(COLORS)-set(t)))); base=(0,1,2); rev=False
            w=tuple(tuple(p[c] for c in x) for x in tuple(tuple(map(int,x)) for x in WORDS[base].split()))
            if rev:
                w=tuple(x[::-1] for x in w)
            return w
        rows=[]
        for t,ss in targets.items():
            source=tuple(tuple(map(int,x)) for x in WORDS[t].split())
            numbered=[edge(x,y) for x,y in zip(source,source[1:]+source[:1])]
            for s in ss:
                entries=[]
                for rev in ([False,True] if kind(s)=='M' else [False]):
                    target=canonical_cycle(s,rev)
                    common=(edges(source)-special(t))&(edges(target)-special(s))
                    indices=[i+1 for i,e in enumerate(numbered) if e in common][:2]
                    assert len(indices)==2
                    entries.append({'reversal':rev,'source_edge_indices':indices,
                                    'common_edges':[serialize(numbered[i-1]) for i in indices]})
                rows.append({'source':t,'target':s,'entries':entries})
        assert len(rows)==17 and sum(len(r['entries']) for r in rows)==20
        (ROOT/'symmetric-safe-witnesses.json').write_text(json.dumps(rows,indent=2)+'\n')
        print('20-entry witness table:')
        for row in rows:
            print(''.join(map(str,row['source'])), ''.join(map(str,row['target'])),
                  ' | '.join(','.join(map(str,e['source_edge_indices'])) for e in row['entries']))
    print(json.dumps({k:v for k,v in output.items() if k not in ('forced_safe_edge_proposal_counterexamples',)},indent=2))

if __name__ == '__main__':
    main()
