"""Bounded exact Hamilton-path discovery on the frozen 44-state 00001 kernel."""
from pathlib import Path
from itertools import product, combinations
import hashlib, json, re, time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'clique_lifts' / 'protected_interfaces' / 'literal-input.tex'
MAX_NODES = 2_000_000
MAX_SECONDS = 10.0


def main():
    inp = HERE / 'literal-input.tex'
    if not inp.exists():
        inp.write_bytes(SOURCE.read_bytes())
    literal = inp.read_text()
    block = re.search(r'% BEGIN PC2-00001\n(.*?)% END PC2-00001', literal, re.S).group(1)
    listed = {w[1:] for w in re.findall(r'\b[01][0-3]{5}\b', block)}
    boundary = '00001'
    states = sorted(''.join(map(str, w)) for w in product(range(4), repeat=5)
                    if all(w[i] != w[(i+1) % 5] and str(w[i]) != boundary[i]
                           for i in range(5)))
    assert set(states) == listed and len(states) == 44
    adj = [sum(1 << j for j, z in enumerate(states)
               if sum(x != y for x, y in zip(w, z)) == 1) for w in states]
    full = (1 << len(states)) - 1
    frozen = {'boundary': boundary, 'states': states,
              'edges': [[states[i], states[j]] for i in range(len(states))
                        for j in range(i+1, len(states)) if adj[i] >> j & 1],
              'literal_input_sha256': hashlib.sha256(inp.read_bytes()).hexdigest()}
    (HERE / 'graph-input.json').write_text(json.dumps(frozen, indent=2) + '\n')

    def components(mask):
        left = mask
        parts = []
        while left:
            reached = left & -left
            todo = reached
            while todo:
                bit = todo & -todo
                todo -= bit
                new = adj[bit.bit_length()-1] & left & ~reached
                reached |= new
                todo |= new
            parts.append(reached)
            left &= ~reached
        return parts

    start = time.perf_counter()
    cuts = []
    obstruction = None
    for size in range(5):
        count = 0
        max_components = 0
        for cut in combinations(range(len(states)), size):
            cc = components(full & ~sum(1 << i for i in cut))
            count += 1
            max_components = max(max_components, len(cc))
            if len(cc) > size + 1:
                obstruction = {'cut': [states[i] for i in cut],
                               'component_count': len(cc),
                               'components': [[states[i] for i in range(len(states))
                                               if mask >> i & 1] for mask in cc]}
                break
        cuts.append({'cut_size': size, 'checked': count,
                     'maximum_components': max_components,
                     'complete_layer': obstruction is None})
        if obstruction:
            break
    cut_seconds = time.perf_counter() - start

    nodes = 0
    dead = set()
    search_start = time.perf_counter()
    path = []
    solution = None
    starts_tried = []
    budget_exhausted = False

    class Budget(Exception):
        pass

    def dfs(current, remaining):
        nonlocal nodes, solution
        nodes += 1
        if nodes > MAX_NODES or (nodes % 1024 == 0 and
                                time.perf_counter() - search_start > MAX_SECONDS):
            raise Budget
        if remaining == 0:
            solution = path.copy()
            return True
        key = (current, remaining)
        if key in dead:
            return False
        choices = adj[current] & remaining
        if not choices or len(components(remaining)) != 1:
            return False
        # In the residual graph, only its final endpoint may be an
        # unvisited vertex of degree one.
        required_endpoint = None
        left = remaining
        while left:
            bit = left & -left
            left -= bit
            vertex = bit.bit_length()-1
            degree = (adj[vertex] & remaining).bit_count() + bool(adj[vertex] >> current & 1)
            if degree == 0:
                return False
            if degree == 1:
                if required_endpoint is not None:
                    return False
                required_endpoint = vertex
        ordered = []
        while choices:
            bit = choices & -choices
            choices -= bit
            vertex = bit.bit_length()-1
            if vertex == required_endpoint and remaining != bit:
                continue
            ordered.append(vertex)
        ordered.sort(key=lambda v: ((adj[v] & remaining).bit_count(), v))
        for vertex in ordered:
            path.append(vertex)
            if dfs(vertex, remaining & ~(1 << vertex)):
                return True
            path.pop()
        if len(dead) < 200_000:
            dead.add(key)
        return False

    if obstruction is None:
        try:
            for vertex in sorted(range(len(states)), key=lambda i: (adj[i].bit_count(), i)):
                starts_tried.append(states[vertex])
                path[:] = [vertex]
                if dfs(vertex, full & ~(1 << vertex)):
                    break
        except Budget:
            budget_exhausted = True
    literal_path = None if solution is None else [states[i] for i in solution]
    if literal_path is not None:
        assert len(literal_path) == len(states) and set(literal_path) == set(states)
        assert all(sum(x != y for x, y in zip(a, b)) == 1
                   for a, b in zip(literal_path, literal_path[1:]))
    result = {'boundary': boundary, 'vertices': len(states), 'edges': len(frozen['edges']),
              'degree_distribution': {str(d): sum(a.bit_count() == d for a in adj)
                                      for d in sorted({a.bit_count() for a in adj})},
              'cut_search': cuts, 'cut_seconds': cut_seconds,
              'nontraceability_certificate': obstruction,
              'Hamilton_path': literal_path,
              'search': {'maximum_nodes': MAX_NODES, 'maximum_seconds': MAX_SECONDS,
                         'nodes': nodes, 'seconds': time.perf_counter() - search_start,
                         'budget_exhausted': budget_exhausted, 'starts_tried': starts_tried},
              'status': 'traceable' if literal_path else ('nontraceable-cut' if obstruction else 'UNKNOWN'),
              'input_sha256': frozen['literal_input_sha256']}
    (HERE / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
