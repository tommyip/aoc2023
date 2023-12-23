import sys
from collections import defaultdict

sys.setrecursionlimit(10000)

with open('inputs/day23.txt') as f:
    m = f.read().splitlines()

w, h = len(m[0]), len(m)
source, dest = (1, 0), (w - 2, h - 1)

NEIGHBORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
slopes = '>v<^'


# Create adjacency list for part 1 & 2
G1 = defaultdict(dict)
G2 = defaultdict(dict)
for j in range(h):
    for i in range(w):
        tile = m[j][i]
        if tile != '#':
            for di, dj in NEIGHBORS:
                ni, nj = i + di, j + dj
                if 0 <= ni < w and 0 <= nj < h and m[nj][ni] != '#':
                    if tile not in slopes or (di, dj) == NEIGHBORS[slopes.index(tile)]:
                        G1[i, j][ni, nj] = 1
                    G2[i, j][ni, nj] = 1


def longest_path(G):
    def aux(pos, visited, path_length):
        if pos == dest:
            return path_length
        new_visited = visited.union({pos})
        return max((aux(npos, new_visited, path_length + edge_length)
                    for npos, edge_length in G[pos].items()
                    if npos not in new_visited),
                   default=0)

    return aux(source, set(), 0)


def prune_useless_edges(G):
    g = defaultdict(lambda: defaultdict(int))
    visited = set()
    def is_hub(pos): return len(G[pos]) >= 3

    def aux(pos, prev_pos, prev_hub, dist):
        visited.add(pos)
        if is_hub(pos) or pos == dest:
            g[prev_hub][pos] = max(g[prev_hub][pos], dist)
            g[pos][prev_hub] = max(g[pos][prev_hub], dist)
            dist = 0
            prev_hub = pos
        for npos in G[pos]:
            if npos != prev_pos:
                if npos not in visited:
                    aux(npos, pos, prev_hub, dist + 1)
                elif is_hub(npos):
                    g[prev_hub][npos] = max(g[prev_hub][npos], dist + 1)
                    g[npos][prev_hub] = max(g[npos][prev_hub], dist + 1)

    aux(source, None, source, 0)
    return g


print(longest_path(G1))
print(longest_path(prune_useless_edges(G2)))
