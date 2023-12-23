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
    def aux(pos, visited, length):
        if pos == dest:
            return length
        longest_hikes = 0
        for npos, dist in G[pos].items():
            if npos not in visited:
                longest_hikes = max(longest_hikes, aux(
                    npos, visited.union({pos}), length + dist))

        return longest_hikes
    return aux(source, set(), 0)


def prune_useless_edges(G):
    g = defaultdict(lambda: defaultdict(int))
    visited = set()

    def aux(pos, prev_pos, prev_vert, dist):
        visited.add(pos)
        is_vert = len(G[pos]) >= 3
        if is_vert or pos == dest:
            g[prev_vert][pos] = max(g[prev_vert][pos], dist)
            g[pos][prev_vert] = max(g[pos][prev_vert], dist)
            dist = 0
        for npos in G[pos]:
            if npos != prev_pos:
                if npos not in visited:
                    aux(npos, pos, pos if is_vert else prev_vert, dist + 1)
                elif len(G[npos]) >= 3:
                    g[prev_vert][npos] = max(g[prev_vert][npos], dist + 1)
                    g[npos][prev_vert] = max(g[npos][prev_vert], dist + 1)

    aux(source, None, source, 0)
    return g


print(longest_path(G1))
print(longest_path(prune_useless_edges(G2)))
