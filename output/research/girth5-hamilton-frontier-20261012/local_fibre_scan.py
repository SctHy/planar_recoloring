#!/usr/bin/env python3
"""Small standard-library scan for C5 list fibres at four colours.

The scan is exploratory: a local fibre obstruction is not a counterexample
to the complete recolouring graph.  A mask records the colours allowed at a
pentagon vertex.  The script reports the explicit two-state obstruction used
in the accompanying research note and counts list patterns with a disconnected
or subdegree-two local fibre among masks of size at least two.
"""

from itertools import product


COLORS = range(4)
ALL_STATES = tuple(
    state
    for state in product(COLORS, repeat=5)
    if all(state[i] != state[(i + 1) % 5] for i in range(5))
)


def fibre(mask_tuple):
    states = tuple(
        state
        for state in ALL_STATES
        if all(mask_tuple[i] & (1 << state[i]) for i in range(5))
    )
    index = {state: i for i, state in enumerate(states)}
    adjacency = [[] for _ in states]
    for i, state in enumerate(states):
        for position in range(5):
            for colour in COLORS:
                if colour == state[position] or not (
                    mask_tuple[position] & (1 << colour)
                ):
                    continue
                neighbour = list(state)
                neighbour[position] = colour
                j = index.get(tuple(neighbour))
                if j is not None:
                    adjacency[i].append(j)
    return states, adjacency


def component_count(adjacency):
    seen = set()
    components = 0
    for start in range(len(adjacency)):
        if start in seen:
            continue
        components += 1
        seen.add(start)
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
    return components


def main():
    obstruction = (0b0011, 0b0011, 0b0011, 0b0011, 0b0101)
    states, adjacency = fibre(obstruction)
    print("obstruction_masks", obstruction)
    print("obstruction_states", states)
    print("obstruction_degrees", [len(row) for row in adjacency])
    print("obstruction_components", component_count(adjacency))

    masks = tuple(mask for mask in range(1, 16) if mask.bit_count() >= 2)
    disconnected = 0
    minimum_degree_below_two = 0
    nonempty = 0
    for mask_tuple in product(masks, repeat=5):
        states, adjacency = fibre(mask_tuple)
        if not states:
            continue
        nonempty += 1
        if component_count(adjacency) > 1:
            disconnected += 1
        if min(map(len, adjacency)) < 2:
            minimum_degree_below_two += 1
    print("mask_patterns_nonempty", nonempty)
    print("mask_patterns_disconnected", disconnected)
    print("mask_patterns_min_degree_below_two", minimum_degree_below_two)


if __name__ == "__main__":
    main()
