"""Check a direction-of-use limitation, without searching for more paths."""
from pathlib import Path
import json,re

p=Path(__file__).resolve().parent
t=(p/'literal-input.tex').read_text()
w=json.loads((p/'path-results.json').read_text())['path']
path_edges={tuple(sorted(e)) for e in zip(w,w[1:])}
def edges(tag):
    b=re.search('% BEGIN '+tag+r'\n(.*?)% END '+tag,t,re.S).group(1)
    return {tuple(sorted(e)) for e in re.findall(r'([0-3]{5})-([0-3]{5})',b)}
ports=edges('PORTS-00112');pool=edges('POOL-00112-0');K=ports-pool
result={'ports_count':len(ports),'pool_count':len(pool),'K_count':len(K),
    'K_retained_on_discovered_path':len(K&path_edges),
    'missing_K_edges':sorted(K-path_edges),
    'ports_retained_on_discovered_path':len(ports&path_edges),
    'limitation':'not a first-factor K-preserving path; this does not obstruct use as the traceable second factor B'}
(p/'protected-edges.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
