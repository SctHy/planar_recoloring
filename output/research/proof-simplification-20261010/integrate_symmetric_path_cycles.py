from pathlib import Path
import difflib, hashlib, json, re

root = Path('/Users/huahua815/Downloads/planar_recoloring')
work = root / 'output/research/proof-simplification-20261010'
path = root / 'planar_recoloring_hamilton_thresholds.tex'
candidate_path = work / 'path232' / 'compact12-candidate.tex'
candidate = candidate_path.read_text()
old = path.read_text()
text = old

arrays = re.findall(r'\\begin\{array\}.*?\\end\{array\}', candidate, re.S)
assert len(arrays) == 2
cycle_start = text.index(r'\begin{array}', text.index(r'\label{eq:path232-cycles}'))
cycle_end = text.index(r'\end{array}', cycle_start) + len(r'\end{array}')
text = text[:cycle_start] + arrays[0] + text[cycle_end:]

a = r'''For $t=010$, the retained three-edge paths are
$323,123,121,321$ and $231,232,132,131$.'''
b = r'''For $t=010$, the retained three-edge paths are
$121,321,323,123$ and $132,232,231,131$.'''
assert text.count(a) == 1
text = text.replace(a, b, 1)

start = text.index(r'\begin{proof}', text.index(r'\label{lem:pathsafe}'))
end = text.index(r'\end{proof}', start) + len(r'\end{proof}')
proof = r'''\begin{proof}
Order the types as $E<M<A$ and orient the transition so its source
has no larger type. Normalize its selected source cycle to
\eqref{eq:path232-cycles} by a colour permutation and possibly
reversal. There are eight eligible targets from $001$, six from
$010$, and three from $012$.

The source stabilizers displayed in
Appendix~\ref{app:path232-certificates} reduce these to five, three,
and two target orbits, respectively. The target conventions there
exhaust every allowed edge set. Table~\ref{tab:path232-safe-edges}
gives two actual safe common edges for each of the resulting twelve
source--target cycle pairs. Each entry is checked by the displayed
colour map and optional reversal in \eqref{eq:path232-cycles}.
All normalization and stabilizer maps preserve special edges, so
the witnesses prove the assertion for every labelled pair.
\end{proof}'''
text = text[:start] + proof + text[end:]

start = text.index('Number source edges', text.index(r'\label{app:path232-certificates}'))
end = text.index(r'\clearpage', start)
conventions_start = candidate.index(r'\paragraph{Target conventions.}') + len(r'\paragraph{Target conventions.}')
conventions_end = candidate.index(r'\paragraph{Source stabilizers and completeness.}')
conventions = candidate[conventions_start:conventions_end].strip()
stabilizers = r'''The unused-colour interchange $(2\ 3)$ preserves $D_E,D_M$
and their special edges. Path reversal followed by $(0\ 2)$
preserves $D_A$. The corresponding target orbits are
\[
\begin{array}{c|l}
001&\{002,003\},\ \{011\},\ \{021,031\},\ \{101\},\ \{201,301\}\\
010&\{012,013\},\ \{020,030\},\ \{210,310\}\\
012&\{013,312\},\ \{032\}.
\end{array}
\]
These actions preserve the target families. Middle-change targets have
two edge sets, giving twelve entries in ten rows. Every printed edge
is safe and has a fixed middle coordinate.
'''
table = r'''\begin{table}[!htbp]
\centering\small
\renewcommand{\arraystretch}{1.15}
\caption{Two safe common edges for each representative good-boundary interface.}
\label{tab:path232-safe-edges}
$''' + arrays[1].replace(r'\!\text{--}\!', r'\text{--}') + r'''$
\end{table}
'''
replacement = ('Table~\\ref{tab:path232-safe-edges} prints actual edge endpoints.\n'
               'Target columns use the following conventions.\n\n' + conventions
               + '\n\n' + stabilizers + '\n' + table)
text = text[:start] + replacement + text[end:]

statements = lambda s: re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}(.*?)\\end\{\1\}', s, re.S)
assert statements(old) == statements(text)
assert re.findall(r'\\label\{([^}]+)\}', old) == re.findall(r'\\label\{([^}]+)\}', text)
blocks = lambda s: {m.group(1):m.group(0) for m in re.finditer(r'^% BEGIN ([^\n]+)\n.*?^% END \1$', s, re.S | re.M)}
assert blocks(old) == blocks(text)
assert 'thirty-seven' not in text
assert 'Number source edges' not in text
assert 'Source-edge indices' not in text
path.write_text(text)
(work / 'symmetric-path-integration.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True), text.splitlines(True), fromfile='before.tex', tofile='after.tex')))
(work / 'symmetric-path-integration-verification.json').write_text(json.dumps({
    'all_statements_identical': True, 'all_labels_identical': True,
    'all_pentagon_finite_blocks_identical': True,
    'candidate_sha256': hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
    'source_before_sha256': hashlib.sha256(old.encode()).hexdigest(),
    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'source_cycle_edge_symmetries': ['E and M: unused-colour swap', 'A: endpoint reversal with 0/2 swap'],
    'safe_witness_entries_before': 37,
    'safe_witness_entries_after': 12,
    'safe_witness_rows_after': 10
}, indent=2) + '\n')
print('Integrated reviewed symmetric path cycles and the twelve-entry literal safe-edge certificate.')
