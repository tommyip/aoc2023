import numpy as np
from itertools import combinations, product

with open('inputs/day24.txt') as f:
    lines = [line.split(' @ ') for line in f.read().splitlines()]

MIN = 200000000000000
MAX = 400000000000000

stones = []
for pos, vel in lines:
    pos = np.array([int(x) for x in pos.split(', ')])
    vel = np.array([int(x) for x in vel.split(', ')])
    stones.append((pos, vel))


def is_future(pos, vel, intersect):
    return (intersect[0] - pos[0]) / vel[0] >= 0


def intersection(u_pos, u_vel, v_pos, v_vel):
    x, err, rank = np.linalg.lstsq(
        np.array([u_vel.T, -v_vel.T]).T, v_pos.T-u_pos.T, rcond=None)[:3]
    if rank == 2:
        return u_pos + u_vel * x[0]


part1 = 0
for (a_pos, a_vel), (b_pos, b_vel) in combinations(stones, r=2):
    a_pos_xy = np.array([*a_pos[:2], 0])
    a_vel_xy = np.array([*a_vel[:2], 0])
    b_pos_xy = np.array([*b_pos[:2], 0])
    b_vel_xy = np.array([*b_vel[:2], 0])
    intersect = intersection(a_pos_xy, a_vel_xy, b_pos_xy, b_vel_xy)
    if intersect is not None and np.all((intersect[:2] >= MIN) & (intersect[:2] <= MAX)):
        if is_future(a_pos_xy, a_vel_xy, intersect) and is_future(b_pos_xy, b_vel_xy, intersect):
            part1 += 1

print(part1)


BF_MAX = 300

xs = set(range(-BF_MAX, BF_MAX+1))
ys = set(range(-BF_MAX, BF_MAX+1))
zs = set(range(-BF_MAX, BF_MAX+1))


def prune_vels(ax, av, bx, bv, vs):
    if ax > bx and av > bv:
        for v in range(bv, av+1):
            if v in vs:
                vs.remove(v)


for (a_pos, a_vel), (b_pos, b_vel) in combinations(stones, r=2):
    prune_vels(a_pos[0], a_vel[0], b_pos[0], b_vel[0], xs)
    prune_vels(a_pos[1], a_vel[1], b_pos[1], b_vel[1], ys)
    prune_vels(a_pos[2], a_vel[2], b_pos[2], b_vel[2], zs)


s0_pos, s0_vel = stones[0]
s1_pos, s1_vel = stones[1]


for x, y, z in product(xs, ys, zs):
    r_vel = np.array([x, y, z])
    sr0_vel = s0_vel - r_vel
    sr1_vel = s1_vel - r_vel
    intersect0 = intersection(s0_pos, sr0_vel, s1_pos, sr1_vel)
    if intersect0 is None:
        continue
    for s_pos, s_vel in stones[2:]:
        sr_vel = s_vel - r_vel
        intersect = intersection(s0_pos, sr0_vel, s_pos, sr_vel)
        if intersect is None or not np.allclose(intersect, intersect0):
            break
    else:
        print(round(intersect0.sum()))
        break
