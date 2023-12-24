from itertools import combinations

with open('inputs/day24.txt') as f:
    lines = [line.split(' @ ') for line in f.read().splitlines()]

MIN = 200000000000000
MAX = 400000000000000

stones = []
for pos, vel in lines:
    pos = [int(x) for x in pos.split(', ')]
    vel = [int(x) for x in vel.split(', ')]
    stones.append((pos, vel))


def hail_intersection(a0, a1, b0, b1):
    denom = ((a0.real - a1.real) * (b0.imag - b1.imag) -
             (a0.imag - a1.imag) * (b0.real - b1.real))
    if denom == 0:
        return None
    num0 = a0.real * a1.imag - a0.imag * a1.real
    num1 = b0.real * b1.imag - b0.imag * b1.real
    x = num0 * (b0.real - b1.real) - (a0.real - a1.real) * num1
    y = num0 * (b0.imag - b1.imag) - (a0.imag - a1.imag) * num1
    return complex(x / denom, y / denom)


def hail_intersection2(a0, a1, b0, b1):
    x1, x2, x3, x4 = a0.real, a1.real, b0.real, b1.real
    y1, y2, y3, y4 = a0.imag, a1.imag, b0.imag, b1.imag
    numerator = ((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))
    denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
    if denominator == 0:
        return None
    t = numerator / denominator
    if not (0 <= t <= 1):
        return None
    px = x1 + t * (x2 - x1)
    py = y1 + t * (y2 - y1)
    return complex(px, py)


def is_future(pos, vel, intersect):
    # t = (intersect - pos) / vel
    # return t.real >= 0 and t.imag >= 0
    t = (intersect.real - pos.real) / vel.real
    return t >= 0


part1 = 0
for (a_pos, a_vel), (b_pos, b_vel) in combinations(stones, r=2):
    a0 = complex(*a_pos[:2])
    av = complex(*a_vel[:2])
    b0 = complex(*b_pos[:2])
    bv = complex(*b_vel[:2])
    intersect = hail_intersection(a0, a0+av*MAX, b0, b0+bv*MAX)
    # print(a_pos, b_pos, intersect)
    if intersect is not None and (MIN <= intersect.real <= MAX and MIN <= intersect.imag <= MAX):
        afuture = is_future(a0, av, intersect)
        bfuture = is_future(b0, bv, intersect)
        if afuture and bfuture:
            part1 += 1

print(part1)
