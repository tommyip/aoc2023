from queue import SimpleQueue
from collections import defaultdict

with open('inputs/day22.txt') as f:
    lines = f.read().splitlines()


bricks = []
cubes = {}
for brick_id, line in enumerate(lines):
    c, c1 = [tuple(int(x) for x in chunk.split(','))
             for chunk in line.split('~')]
    dx, dy, dz = c1[0] - c[0], c1[1] - c[1], c1[2] - c[2]
    brick_cubes = []
    for i in range(max(dx, dy, dz) + 1):
        brick_cubes.append(c)
        cubes[c] = brick_id
        c = (c[0] + dx // (dx or 1),
             c[1] + dy // (dy or 1),
             c[2] + dz // (dz or 1))
    min_z = min(c[2] for c in brick_cubes)
    bricks.append((min_z, brick_id, brick_cubes))

# Run gravity simulation by z-order to ensure a brick does not settle on a
# mid-air brick.
bricks.sort(key=lambda args: args[0])

for min_z, brick_id, brick_cubes in bricks:
    settled = False
    for cube in brick_cubes:
        del cubes[cube]
    while not settled:
        # Only consider the lowest cubes to avoid falling onto itself
        for x, y, z in brick_cubes:
            if z == min_z and (z == 1 or (x, y, z - 1) in cubes):
                settled = True
                break
        else:
            for i, (x, y, z) in enumerate(brick_cubes):
                brick_cubes[i] = x, y, z - 1
            min_z -= 1
    for cube in brick_cubes:
        cubes[cube] = brick_id

supporting = defaultdict(set)
supported_by = defaultdict(set)

for (x, y, z), brick_id in cubes.items():
    if (x, y, z - 1) in cubes:
        support_id = cubes[x, y, z - 1]
        if support_id != brick_id:
            supporting[support_id].add(brick_id)
            supported_by[brick_id].add(support_id)

part1 = 0
part2 = 0
q = SimpleQueue()
for _, brick_id, _ in bricks:
    # Find how many bricks (including self) would be disintegrated
    # if we disintegrate this brick.
    q.put(brick_id)
    disintegrated = set()
    while not q.empty():
        to_disintegrate = q.get()
        disintegrated.add(to_disintegrate)
        for supporting_id in supporting[to_disintegrate]:
            if all(by in disintegrated for by in supported_by[supporting_id]):
                q.put(supporting_id)
    part1 += len(disintegrated) == 1
    part2 += len(disintegrated) - 1

print(part1)
print(part2)
