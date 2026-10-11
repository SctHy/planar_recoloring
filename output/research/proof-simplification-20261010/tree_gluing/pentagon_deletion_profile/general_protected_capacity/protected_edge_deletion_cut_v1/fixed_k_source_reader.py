#!/usr/bin/env python3
"""Own literal-source fixedK and complete-component reader.

This imports only this reviewer's copied independent parser, not any
author helper. HardK common-to-product-seeds status remains a frozen
premise; actual port graph legality, pool exclusion and state membership
are checked here.
"""
from itertools import permutations
import hashlib
import re
import independent_source_reader as R

HARD={'00001','00112'}


class ActualSource:
    def __init__(self,current,reference,prior_component_checks):
        self.current=current
        self.reference=reference
        self.prior=prior_component_checks
        self.cache={}
        self.component_checks={}
        self.standard_types={'00000','00001','00112'}|{name.split('-')[1] for name in current if name.startswith(('C1-','FHC-'))}
        assert len(self.standard_types)==22

    def first_normalizer(self,boundary):
        for start in range(5):
            for sign in (1,-1):
                for perm in permutations(R.COLOURS):
                    mapping=(start,sign,perm);target=R.transform(boundary,mapping)
                    if target in self.standard_types:return target,mapping
        raise AssertionError('no normalizer: '+boundary)

    def component(self,t,c):
        key=t+':'+str(c)
        if key in self.cache:return self.cache[key]
        if t=='00000':
            assert c in (0,1)
            name='FACTOR-00000'
            all_words=re.findall(r'\b[0-3]{5}\b',R.body(self.current[name]))
            assert len(all_words)==30 and len(set(all_words))==30
            words=all_words[15*c:15*(c+1)]
            has_hc=True
        elif t in HARD:
            assert c==0
            name='MATCHING-CHAIN-00001' if t=='00001' else 'HP-00112'
            words=re.findall(r'\b[0-3]{5}\b',R.body(self.current[name]))
            assert len(words)==(44 if t=='00001' else 51)
            has_hc=False
        else:
            assert c==0
            name=('FHC-' if '4' in t else 'C1-')+t
            words=re.findall(r'\b[0-3]{5}\b',R.body(self.current[name]))
            has_hc=True
        pool_name='POOL-'+t+'-'+str(c)
        assert self.current[name]==self.reference[name]
        assert self.current[pool_name]==self.reference[pool_name]
        V=set(words)
        assert len(V)==len(words)>2 and all(R.is_legal(w,t) for w in words)
        P={R.edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',R.body(self.current[pool_name]))}
        assert len(P)==(2 if t in HARD else 5 if t=='00000' else 8)
        E=set()
        if has_hc:
            E={R.edge(a,b) for a,b in zip(words,words[1:]+words[:1])}
            assert len(E)==len(V) and all(sum(a!=b for a,b in zip(*e))==1 for e in E)
            assert P<=E
            K=E-P
            if key in self.prior:
                old=self.prior[key]
                assert old['state_count']==len(V) and old['cycle_block']==name
                assert old['cycle_block_sha256']==hashlib.sha256(self.current[name].encode()).hexdigest()
                assert old['pool_block_sha256']==hashlib.sha256(self.current[pool_name].encode()).hexdigest()
                assert old['all_legal_mutation_neighbours_inside_cycle_vertices'] is True
                count=old['local_neighbour_memberships_checked']
                mode='inherited-own-frozen-phase9-complete-component-closure'
            else:
                N={w:R.neighbours(w,t) for w in V}
                assert all(neighbours<=V for neighbours in N.values())
                count=sum(map(len,N.values()));mode='fresh-complete-HC-component-neighbour-closure'
            protected_basis=name+' cycle edges minus '+pool_name
        else:
            port_name='COMMON-00001' if t=='00001' else 'PORTS-00112'
            assert self.current[port_name]==self.reference[port_name]
            D={R.edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',R.body(self.current[port_name]))}
            assert len(D)==13 and P<=D
            assert all(a in V and b in V and sum(x!=y for x,y in zip(a,b))==1 for a,b in D)
            K=D-P
            assert len(K)==11 and K.isdisjoint(P)
            N={w:R.neighbours(w,t) for w in V}
            assert all(neighbours<=V for neighbours in N.values())
            reached={words[0]};frontier=[words[0]]
            while frontier:
                for neighbor in N[frontier.pop()]:
                    if neighbor not in reached:reached.add(neighbor);frontier.append(neighbor)
            assert reached==V
            assert all(b in N[a] for a,b in D)
            count=sum(map(len,N.values()));mode='fresh-hard-whole-component-neighbour-closure-and-connectivity'
            protected_basis=port_name+' designated common ports minus '+pool_name
        assert all(a in V and b in V for a,b in K)
        assert K.isdisjoint(P)
        self.cache[key]=(V,E,P,K,has_hc)
        self.component_checks[key]={'word_block':name,'state_count':len(V),
            'word_block_sha256':hashlib.sha256(self.current[name].encode()).hexdigest(),
            'pool_block_sha256':hashlib.sha256(self.current[pool_name].encode()).hexdigest(),
            'has_printed_whole_component_HC':has_hc,'printed_HC_edge_count':len(E),
            'pool_edge_count':len(P),'fixed_K_edge_count':len(K),'actual_pool':sorted(P),'actual_fixed_K':sorted(K),
            'fixed_K_basis':protected_basis,'fixed_K_disjoint_own_pool':True,
            'all_vertices_legal':True,'component_connected':True,
            'all_legal_mutation_neighbours_inside_vertex_set':True,'local_neighbour_memberships_checked':count,
            'closure_mode':mode,'hard_seed_common_port_property_inherited':not has_hc,
            'complete_component_reason':'A legal connected vertex set closed under every legal one-coordinate mutation is an entire connected component.'}
        return self.cache[key]
