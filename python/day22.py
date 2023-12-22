from queue import PriorityQueue
from collections import defaultdict

with open('inputs/day22.txt') as f:
    lines = f.read().splitlines()


def sign(x):
    return 0 if x == 0 else x//x


bricks = defaultdict(list)
for brick_id, line in enumerate(lines):
    c0, c1 = [tuple(int(x) for x in chunk.split(','))
              for chunk in line.split('~')]
    dx, dy, dz = (c1[0]-c0[0]), (c1[1]-c0[1]), (c1[2]-c0[2])
    assert dx >= 0 and dy >= 0 and dz >= 0

    c = c0
    for i in range(max(dx, dy, dz) + 1):
        bricks[brick_id].append(c)
        c = c[0]+sign(dx), c[1]+sign(dy), c[2]+sign(dz)


def fall(bricks):
    n_fall = 0
    cubes = {}
    fall_q = PriorityQueue()
    for brick_id, cube_list in bricks.items():
        for cube in cube_list:
            cubes[cube] = brick_id
        fall_q.put((min(c[2] for c in cube_list), brick_id))

    while not fall_q.empty():
        _, brick_id = fall_q.get()
        settled = False
        has_fallen = False
        while not settled:
            for x, y, z in bricks[brick_id]:
                # Already on the ground
                if z == 1:
                    settled = True
                    break
                # Resting on another brick
                if (x, y, z - 1) in cubes and cubes[x, y, z - 1] != brick_id:
                    settled = True
                    break
            else:
                new_brick = []
                for x, y, z in bricks[brick_id]:
                    del cubes[x, y, z]
                    new_cube = x, y, z - 1
                    cubes[new_cube] = brick_id
                    new_brick.append(new_cube)
                bricks[brick_id] = new_brick
                has_fallen = True
        if has_fallen:
            n_fall += 1
    return bricks, cubes, n_fall


bricks, cubes, _ = fall(bricks)

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
    bricks_ = {brick_id_: cubes for brick_id_,
               cubes in bricks.items() if brick_id != brick_id_}
    _, _, n_fall = fall(bricks_)
    part2 += n_fall

print(part2)
