import sys
from collections import defaultdict

sys.setrecursionlimit(10000)

with open('inputs/day23.txt') as f:
    m = f.read().splitlines()

NEIGHBORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
w, h = len(m[0]), len(m)
source, dest = (1, 0), (w - 2, h - 1)
slopes = '>v<^'


# Create weighted adjacency list for part 1 & 2
G1 = defaultdict(dict)
G2 = defaultdict(dict)
for j in range(h):
    for i in range(w):
        tile = m[j][i]
        if tile == '#':
            continue
        for di, dj in NEIGHBORS:
            ni, nj = i + di, j + dj
            if 0 <= ni < w and 0 <= nj < h and m[nj][ni] != '#':
                if (tile not in slopes or
                        (di, dj) == NEIGHBORS[slopes.index(tile)]):
                    G1[i, j][ni, nj] = 1
                G2[i, j][ni, nj] = 1


def longest_path(G):
    last_hub = next(iter(G[dest]))

    def aux(pos, visited, length):
        if pos == dest:
            return length
        elif pos == last_hub:
            # Perf optimization: once we reached the last hub we must proceed
            # to the destination, otherwise we block ourselves when we
            # eventually cycle back. (-10 secs)
            return length + G[last_hub][dest]
        new_visited = visited.union({pos})
        return max((aux(npos, new_visited, length + edge_length)
                    for npos, edge_length in G[pos].items()
                    if npos not in new_visited),
                   default=0)

    return aux(source, set(), 0)


def prune_useless_edges(G):
    """
    Let hubs be vertices with 3+ neighbors. All vertices between hubs are
    useless for our longest path algorithm, so we create a new graph with
    only hubs and set the edge weights as the number of edges between them
    in the original graph.
    """
    g = defaultdict(lambda: defaultdict(int))
    visited = set()
    def is_hub(pos): return len(G[pos]) >= 3

    def aux(pos, prev_pos, prev_hub, length):
        visited.add(pos)
        if is_hub(pos) or pos == dest:
            g[prev_hub][pos] = g[pos][prev_hub] = max(g[prev_hub][pos], length)
            length = 0
            prev_hub = pos
        for npos in G[pos]:
            if npos != prev_pos:
                if npos not in visited:
                    aux(npos, pos, prev_hub, length + 1)
                elif is_hub(npos):
                    g[prev_hub][npos] = g[npos][prev_hub] = max(
                        g[prev_hub][npos], length + 1)

    aux(source, None, source, 0)
    return g


print(longest_path(G1))
print(longest_path(prune_useless_edges(G2)))
