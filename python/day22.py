from collections import defaultdict

with open('inputs/day22.txt') as f:
    lines = f.read().splitlines()


def sign(x):
    return 0 if x == 0 else x//x


bricks = defaultdict(list)
for brick_id, line in enumerate(lines):
    c0, c1 = [tuple(int(x) for x in chunk.split(','))
              for chunk in line.split('~')]
    dx, dy, dz = c1[0]-c0[0], c1[1]-c0[1], c1[2]-c0[2]

    for i in range(max(dx, dy, dz) + 1):
        bricks[brick_id].append(c0)
        c0 = c0[0]+sign(dx), c0[1]+sign(dy), c0[2]+sign(dz)


def fall(bricks):
    n_fall = 0
    cubes = {}
    # Run gravity simulation by z-order to ensure a brick does not settle on a
    # mid-air brick.
    fall_order = []
    for brick_id, cube_list in bricks.items():
        for cube in cube_list:
            cubes[cube] = brick_id
        fall_order.append((min(c[2] for c in cube_list), brick_id))
    fall_order.sort()

    for min_z, brick_id in fall_order:
        settled = False
        has_fallen = False
        brick_cubes = [c for c in bricks[brick_id]]
        for cube in brick_cubes:
            del cubes[cube]
        while not settled:
            # Only consider the lowest cubes to avoid falling onto itself
            for x, y, z in brick_cubes:
                if z == min_z:
                    if z == 1 or (x, y, z - 1) in cubes:
                        settled = True
                        break
            else:
                for i, (x, y, z) in enumerate(brick_cubes):
                    brick_cubes[i] = x, y, z - 1
                min_z -= 1
                has_fallen = True
        for cube in brick_cubes:
            cubes[cube] = brick_id
        bricks[brick_id] = brick_cubes
        if has_fallen:
            n_fall += 1
    return cubes, n_fall


cubes, _ = fall(bricks)

support = defaultdict(set)
supported_by = defaultdict(set)

for (x, y, z), brick_id in cubes.items():
    if (x, y, z - 1) in cubes:
        support_id = cubes[x, y, z - 1]
        if support_id != brick_id:
            support[support_id].add(brick_id)
            supported_by[brick_id].add(support_id)

part1 = 0
for id in bricks:
    for supporting_id in support[id]:
        if supported_by[supporting_id] == {id}:
            break
    else:
        part1 += 1

print(part1)

part2 = 0
for brick_id in bricks:
    other_bricks = {id: bricks[id] for id in bricks if id != brick_id}
    _, n_fall = fall(other_bricks)
    part2 += n_fall

print(part2)
