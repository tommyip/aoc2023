import sys
sys.setrecursionlimit(10000)

with open('inputs/day16.txt') as f:
    m = f.read().splitlines()

w, h = len(m[0]), len(m)

reflect = {
    '/': {
        (1, 0): [(0, -1)],
        (0, 1): [(-1, 0)],
        (-1, 0): [(0, 1)],
        (0, -1): [(1, 0)]
    },
    '\\': {
        (1, 0): [(0, 1)],
        (0, 1): [(1, 0)],
        (-1, 0): [(0, -1)],
        (0, -1): [(-1, 0)]
    },
    '|': {
        (1, 0): [(0, 1), (0, -1)],
        (-1, 0): [(0, 1), (0, -1)]
    },
    '-': {
        (0, 1): [(1, 0), (-1, 0)],
        (0, -1): [(1, 0), (-1, 0)]
    },
}


def solve(start, dir):
    visited = set()
    energized = [[False] * w for _ in range(h)]

    def beam(coord, dir):
        if not (0 <= coord[0] < w) or not (0 <= coord[1] < h) or coord+dir in visited:
            return

        energized[coord[1]][coord[0]] = True
        cell = m[coord[1]][coord[0]]
        visited.add(coord + dir)
        if cell in reflect and dir in reflect[cell]:
            for r in reflect[cell][dir]:
                beam((coord[0] + r[0], coord[1] + r[1]), r)
        else:
            beam((coord[0] + dir[0], coord[1] + dir[1]),
                 dir)

    beam(start, dir)
    return sum(sum(row) for row in energized)


print(solve((0, 0), (1, 0)))

part2 = 0
for i in range(w):
    part2 = max(part2, solve((i, 0), (0, 1)), solve((i, h-1), (0, -1)))
for j in range(h):
    part2 = max(part2, solve((0, j), (1, 0)), solve((w-1, j), (-1, 0)))

print(part2)
