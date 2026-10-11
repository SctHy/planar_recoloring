from pathlib import Path
import difflib, hashlib, json, re

root = Path('/Users/huahua815/Downloads/planar_recoloring')
work = root / 'output/research/proof-simplification-20261010/continuation-2'
path = root / 'planar_recoloring_hamilton_thresholds.tex'
old = path.read_text()
assert hashlib.sha256(path.read_bytes()).hexdigest() == '9c457bc09ef8db4c8e8bd1ae1ea2cb4d33dfebeb89357f972b91f1dd8f25f332'
text = old

start = text.index(r'\begin{proof}', text.index(r'\label{lem:pathsafe}'))
end = text.index(r'\end{proof}', start) + len(r'\end{proof}')
proof = r'''\begin{proof}
If both boundaries are middle-change types, adjacency gives
$t=(a,b,a)$ and $s=(a,c,a)$ with $a,b,c$ distinct. Let $d$ be the
fourth colour. Each allowed cycle retains three of the four edges
of $Q_d\subset B_{aaa}$ by the preceding square-support property.
Their intersection has at least two edges, and both special-edge
sets are empty. Thus these common edges are safe.

For every other transition, order the types as $E<M<A$ and orient
it so its source has no larger type. Normalize the selected source
cycle to \eqref{eq:path232-cycles} by a colour permutation and
possibly reversal. There are eight remaining eligible targets from
$001$, four from $010$, and three from $012$.

The source stabilizers displayed in
Appendix~\ref{app:path232-certificates} reduce these to five, two,
and two target orbits, respectively. The target conventions there
exhaust every allowed edge set. Table~\ref{tab:path232-safe-edges}
gives two actual safe common edges for each of the resulting ten
source--target cycle pairs. Each entry is checked by the displayed
colour map and optional reversal in \eqref{eq:path232-cycles}.
All normalization and stabilizer maps preserve special edges, so
the witnesses prove the assertion for every labelled pair.
\end{proof}'''
text = text[:start] + proof + text[end:]

old_orbits = r'010&\{012,013\},\ \{020,030\},\ \{210,310\}\\'
new_orbits = r'010&\{012,013\},\ \{210,310\}\\'
assert text.count(old_orbits) == 1
text = text.replace(old_orbits, new_orbits, 1)
text = text.replace('preserves $D_A$. The corresponding target orbits are',
                    'preserves $D_A$. After the middle--middle case in the proof\n'
                    'of Lemma~\\ref{lem:pathsafe}, the remaining target orbits are', 1)
old_count = ('These actions preserve the target families. Middle-change targets have\n'
             'two edge sets, giving twelve entries in ten rows. Every printed edge\n'
             'is safe and has a fixed middle coordinate.')
new_count = ('These actions preserve the target families. The end-to-middle target\n'
             'has two edge sets, giving ten entries in nine rows. Every printed\n'
             'edge is safe and has a fixed middle coordinate.')
assert text.count(old_count) == 1
text = text.replace(old_count, new_count, 1)
row = r'010&020&301\text{--}302,\ 132\text{--}232&103\text{--}303,\ 302\text{--}303\\' + '\n'
assert text.count(row) == 1
text = text.replace(row, '', 1)

statements = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
assert statements(old) == statements(text)
assert re.findall(r'\\label\{([^}]+)\}', old) == re.findall(r'\\label\{([^}]+)\}', text)
blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$', s, re.S | re.M)}
assert blocks(old) == blocks(text)
path.write_text(text)
(work / 'middle-interface-integration.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True), text.splitlines(True), fromfile='twelve-entry.tex', tofile='analytic-MM-plus-ten-entry.tex')))
(work / 'integration-verification.json').write_text(json.dumps({
    'all_statements_and_labels_identical': True,
    'all_finite_pentagon_blocks_identical': True,
    'source_before_sha256': hashlib.sha256(old.encode()).hexdigest(),
    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'replacement': 'M--M handled by two three-edge subsets of a four-edge square',
    'remaining_safe_witness_entries': 10,
    'remaining_safe_witness_rows': 9
}, indent=2)+'\n')
print('Integrated analytic M--M square proof; remaining safe-edge table has ten entries.')
