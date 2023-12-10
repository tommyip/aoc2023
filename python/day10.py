with open('inputs/day10.txt') as f:
    m = f.read().splitlines()

w, h = len(m[0]), len(m)

# Initialize starting point
last_loc = None
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
# Initialize starting direction, perpendicular direction
# of starting direction (for part 2) and first step of trail.
for nb in neighbors:
    nb_loc = S + nb
    nb_pipe = lookup(nb_loc)
    if nb_pipe == '.':
        continue
    start, end = pipes[nb_pipe]
    if nb == -start or nb == -end:
        loc = nb_loc
        dir = nb
        # Multiplying a complex number by i rotates it 90
        # degrees counter-clockwise.
        # NOTE: our y axis is flipped, so the behaviour
        # is slightly weird.
        perp = nb * 1j
        break

# Navigate trail until we reach back to S
trail = [S]
while loc != S:
    trail.append(loc)
    pipe = lookup(loc)
    start, end = pipes[pipe]
    if loc + start == last_loc:
        loc, last_loc = loc + end, loc
    else:
        loc, last_loc = loc + start, loc

# Part 1
print(len(trail) // 2)

# Solve part 2 by flood filling one side of the trail. First
# record all the points touching one side.
trail_set = set(trail)
flood_fill_starts = set()
filled = set()
is_outside = False

for step in trail:
    pipe = lookup(step)
    if pipe == 'S':
        continue
    start, end = pipes[pipe]
    nb = step + perp
    if 0 <= nb.real < w and 0 <= nb.imag < h and nb not in trail_set:
        flood_fill_starts.add(nb)
    if pipe in 'LJ7F':
        if dir == -start:
            dir = end
            perp *= 1j ** 3
        else:
            dir = start
            perp *= 1j
        nb = step + perp
        if 0 <= nb.real < w and 0 <= nb.imag < h and nb not in trail_set:
            flood_fill_starts.add(nb)


def flood_fill(loc):
    filled.add(loc)
    for nb in neighbors:
        nb_loc = loc + nb
        if 0 <= nb_loc.real < w and 0 <= nb_loc.imag < h:
            if nb_loc not in trail_set and nb_loc not in filled:
                flood_fill(nb_loc)
        else:
            global is_outside
            # We touched the edge, must be filling the outside.
            is_outside = True


for loc in flood_fill_starts:
    flood_fill(loc)

# Part 2
if is_outside:
    print((w * h) - len(filled) - len(trail))
else:
    print(len(filled))
