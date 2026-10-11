"""Two explicit g switches and two prescribed YY switches; no graph search."""
from pathlib import Path
from collections import Counter
import hashlib,json,re

HERE=Path(__file__).resolve().parent

def edge(u,v):return tuple(sorted((u,v)))

def analyze(es):
    adj={}
    for u,v in es:adj.setdefault(u,[]).append(v);adj.setdefault(v,[]).append(u)
    assert all(len(ns)==2 for ns in adj.values())
    cycles=[];unseen=set(adj)
    while unseen:
        start=min(unseen);prev=None;u=start;words=[]
        while not words or u!=start:
            words.append(u);unseen.remove(u)
            v=next(v for v in sorted(adj[u]) if v!=prev)
            prev,u=u,v
        cycles.append(words)
    return cycles

def main():
    inp=HERE/'original-literal-input.tex';text=inp.read_text()
    def block(name):return re.search('% BEGIN '+name+'\n(.*?)% END '+name,text,re.S).group(1)
    ws=re.findall(r'\b[01][0-3]{5}\b',block('PC2-00001'))
    original={edge(a,b) for a,b in zip(ws,ws[1:]+ws[:1])}
    K={edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block('COMMON-00001'))}-{edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block('POOL-00001-0'))}
    K.remove(('12313','12323'));K.add(('13120','23120'))
    reports=[]
    for terminal in ('23123','23130'):
        changes=[{'name':'add g in both rows',
                  'remove':{edge(r+'23120',r+terminal) for r in '01'}|{edge('013120','113120')},
                  'add':{edge(r+'13120',r+'23120') for r in '01'}|{edge('0'+terminal,'1'+terminal)}},
                 {'name':'insert first YY in both rows',
                  'remove':{edge(r+'12310',r+'12313') for r in '01'}|{edge('012312','112312')},
                  'add':{edge(r+'12312',r+'12313') for r in '01'}|{edge('012310','112310')}},
                 {'name':'insert second YY in both rows',
                  'remove':{edge(r+'13212',r+'13232') for r in '01'}|{edge('013213','113213')},
                  'add':{edge(r+'13212',r+'13213') for r in '01'}|{edge('013232','113232')}}]
        result=set(original);stages=[]
        for ch in changes:
            assert ch['remove']<=result and not ch['add']&result
            result-=ch['remove'];result|=ch['add']
            cs=analyze(result)
            stages.append({'switch':ch['name'],'cycle_lengths':list(map(len,cs))})
        cs=analyze(result)
        rows={r:{edge(a[1:],b[1:]) for a,b in result if a[0]==b[0]==r} for r in '01'}
        assert all(K<=es for es in rows.values())
        pools={edge(a,b) for a,b in re.findall(r'([0-3]{5})-([0-3]{5})',block('POOL-00001-0'))}
        kept=sorted(e for e in pools if all(e in row for row in rows.values()))
        reports.append({'g_terminal':terminal,'stage_cycles':stages,'final_cycle_lengths':list(map(len,cs)),
                        'K12_retained_in_both_rows':True,'old_pool_edges_retained_in_both_rows':kept,
                        'changes':[{k:sorted(v) if isinstance(v,set) else v for k,v in ch.items()} for ch in changes],
                        'result_cycles':cs,'row_internal_edges':{r:sorted(es) for r,es in rows.items()}})
    out={'explicit_variants':reports,'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
         'scope':'Only two explicitly specified local three-edge rewires; no general seed/Hamilton search.'}
    (HERE/'local-switch-results-v1.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{'g_terminal':r['g_terminal'],'stage_cycles':r['stage_cycles'],'final_cycle_lengths':r['final_cycle_lengths'],'retained_old_pool_count':len(r['old_pool_edges_retained_in_both_rows'])} for r in reports]))

if __name__=='__main__':main()
