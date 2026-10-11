from pathlib import Path
import difflib, hashlib, json, re

root = Path('/Users/huahua815/Downloads/planar_recoloring')
work = root / 'output/research/proof-simplification-20261010'
path = root / 'planar_recoloring_hamilton_thresholds.tex'
old = path.read_text()
expected = json.loads((work / 'integration-verification.json').read_text())['source_sha256']
assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
text = old

start = text.index(r'First suppose $\ell=1$.', text.index(r'\label{lem:badblock}'))
end = text.index(r'Now let $\ell\ge2$.', start)
single = r'''First suppose $\ell=1$. Let $S_L,S_R$ be the sets of square
colours supported by available edges of the two chosen good cycles.
Then $|S_L|,|S_R|\ge2$ and $S_L\cup S_R=[4]\setminus\{a\}$:
the only exception could be two middle changes to the same colour,
which would give $t=s$.

Choose a common square with different available edges on the two
sides. If either change is at the middle, any $c\in S_L\cap S_R$
works, since that side offers at least two edges. If both changes
are at ends, choose $c\notin\{a,b_L,b_R\}$, where $b_L,b_R$ are
their changed colours. Its two singleton edges are different:
different ends give different coordinate directions, while changes
at the same end have $b_L\ne b_R$ and give opposite square edges.

Start with the two good cycles and three bad squares. Attach the
chosen square to both good cycles using these different edges, and
attach each other square to a supporting good cycle. These four
incidences form a tree. Cuts at a good cycle lie in different
middle-colour squares, and the two bridge-square cuts are distinct.
Along each tree edge delete the two selected internal edges and add
the two matching edges. Each splice joins disjoint cycles into one;
all reserved edges survive.

'''
text = text[:start] + single + text[end:]

start = text.index(r'Let $q$ count the degree-two vertices', text.index(r'\label{lem:block-subcubic}'))
end = text.index('Choose these pentagons in two distinct endblocks.', start)
endblock = r'''Let $q$ count the degree-two vertices of $B-x$ and put
$\varepsilon=[d_B(x)=2]$. If $q\ge2$, any pair of these vertices
has a common neighbour of $G$-degree at least four by the excluded
reductions. Their neighbours all lie in $B$, so only $x$ can be
this common neighbour. Every one of the $q$ vertices is therefore
adjacent to $x$, giving $q\le d_B(x)=3-\varepsilon$. Together with
the immediate $q\le1$ case, this proves $q+\varepsilon\le3$.

Euler's identity in the two-connected block $B$ now gives
\[
 f_5(B)=12-2(q+\varepsilon)+\sum_{|F|\ge7}(|F|-6)\ge6.
\]
Each five-face is a simple pentagon, while at most $d_B(x)\le3$
faces meet $x$, so choose one avoiding $x$. If $q\le1$, it contains
at most one degree-two vertex of $G$. If $q\ge2$, a cycle through
any of the $q$ vertices must use its edge to $x$, so the chosen
pentagon contains none. All its other vertices have $G$-degree three.

'''
text = text[:start] + endblock + text[end:]

statements = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
assert statements(old) == statements(text)
labels = lambda s: re.findall(r'\\label\{([^}]+)\}', s)
assert labels(old) == labels(text)
blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$', s, re.M | re.S)}
assert blocks(old) == blocks(text)
path.write_text(text)
(work / 'structural-short-proofs.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True), text.splitlines(True), fromfile='before.tex', tofile='after.tex')))
(work / 'structural-integration-verification.json').write_text(json.dumps({
    'all_statements_identical': True, 'all_labels_identical': True,
    'all_finite_blocks_identical': True,
    'source_before_sha256': expected,
    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'changes': ['support-set proof for a single bad layer', 'unified endblock degree bound']
}, indent=2) + '\n')
print('Integrated two reviewed structural short proofs; statements, labels and finite blocks unchanged.')
