import itertools

with open('inputs/day11.txt') as f:
    m = [list(l) for l in f.read().splitlines()]


w, h = len(m[0]), len(m)
tm = [list(i) for i in zip(*m)]


def manhatten(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve(er):
    rows = [er if all(c == '.' for c in row) else 1
            for j, row in enumerate(m)]
    cols = [er if all(c == '.' for c in col) else 1
            for i, col in enumerate(tm)]
    mapped_cols = list(itertools.accumulate(cols))

    galaxies = []
    for j, j_ in enumerate(itertools.accumulate(rows)):
        for i, i_ in enumerate(mapped_cols):
            if m[j][i] == '#':
                galaxies.append((j_, i_))

    return sum(manhatten(*pair)
               for pair in itertools.combinations(galaxies, 2))


print(solve(2))
print(solve(1_000_000))
