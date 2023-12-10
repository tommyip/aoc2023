import sys
sys.setrecursionlimit(10000)

with open('inputs/day10.txt') as f:
    m = f.read().splitlines()

w, h = len(m[0]), len(m)

last_loc = None
S = None
loc = None
for j, tiles in enumerate(m):
    i = tiles.find('S')
    if i != -1:
        last_loc = S = complex(i, j)
        break


def lookup(c):
    return m[int(c.imag)][int(c.real)]


neighbors = (-1j, 1+0j, 1j, -1+0j)
pipes = {
    '|': (-1j, 1j),
    '-': (1+0j, -1+0j),
    'L': (-1j, 1+0j),
    'J': (-1+0j, -1j),
    '7': (1j, -1+0j),
    'F': (1+0j, 1j)
}
dir = None
perp = None
for nb in neighbors:
    nb_loc = S + nb
    nb_pipe = lookup(nb_loc)
    if nb_pipe == '.':
        continue
    start, end = pipes[nb_pipe]
    if nb == -start or nb == -end:
        loc = nb_loc
        dir = nb
        perp = nb * 1j ** 3
        break

loop = [[] for _ in range(h)]
loop[int(S.imag)].append(int(S.real))
if lookup(loc) != '-':
    loop[int(loc.imag)].append(int(loc.real))
trail = [S]
while loc != S:
    trail.append(loc)
    pipe = lookup(loc)
    if pipe != '-':
        loop[int(loc.imag)].append(int(loc.real))
    start, end = pipes[pipe]
    if loc + start == last_loc:
        loc, last_loc = loc + end, loc
    else:
        loc, last_loc = loc + start, loc
trail_set = set(trail)

part2 = 0
to_visit = set()
for step in trail:
    pipe = lookup(step)
    if pipe == 'S':
        continue
    start, end = pipes[pipe]
    if pipe in '-|':
        nb = step + perp
        if 0 <= nb.real < w and 0 <= nb.imag < h and nb not in trail_set:
            to_visit.add(nb)
    elif pipe in 'LJ7F':
        nb = step + perp
        if 0 <= nb.real < w and 0 <= nb.imag < h and nb not in trail_set:
            to_visit.add(nb)
        if dir == -start:
            dir = end
            perp *= 1j ** 3
        else:
            dir = start
            perp *= 1j
        nb = step + perp
        if 0 <= nb.real < w and 0 <= nb.imag < h and nb not in trail_set:
            to_visit.add(nb)

m = [list(l) for l in m]
visited = set()
is_outside = False


def visit(loc):
    m[int(loc.imag)][int(loc.real)] = '#'
    visited.add(loc)
    for nb in neighbors:
        nb_loc = loc + nb
        if 0 <= nb_loc.real < w and 0 <= nb_loc.imag < h:
            if nb_loc not in trail_set and m[int(nb_loc.imag)][int(nb_loc.real)] != '#':
                visit(nb_loc)
        else:
            global is_outside
            is_outside = True


for loc in to_visit:
    visit(loc)

print(len(trail) // 2)
if is_outside:
    print((w * h) - len(visited) - len(trail))
else:
    print(len(visited))
