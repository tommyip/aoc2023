import queue
from itertools import chain
from dataclasses import dataclass, field
from collections import defaultdict

with open('inputs/day17.txt') as f:
    m = [[int(x) for x in l] for l in f.read().splitlines()]

w, h = len(m[0]), len(m)
start = complex(0, h - 1)
end = complex(w-1, 0)


@dataclass(order=True)
class Node:
    heat: int
    steps: int
    dir: complex = field(compare=False)
    pos: complex = field(compare=False)


def solve(min_steps, max_steps):
    dist = defaultdict(lambda: [None] * (max_steps + 1))
    dist[start, 1+0j][0] = dist[start, -1j][0] = 0

    q = queue.PriorityQueue()
    q.put(Node(0, 0, 1+0j, start))
    q.put(Node(0, 0, -1j, start))

    while not q.empty():
        node = q.get()
        u = node.pos
        u_heat = dist[u, node.dir][node.steps]
        for dir in (1j, 1+0j, -1j, -1+0j):
            # no backwards
            if dir == -node.dir:
                continue
            # must turn at max_steps in a single direction
            if node.dir == dir and node.steps == max_steps:
                continue

            is_turning = dir != node.dir
            next_step = min_steps if is_turning else node.steps + 1
            take_steps = min_steps if is_turning else 1
            v = u + dir * take_steps
            if 0 <= v.real < w and 0 <= v.imag < h:
                v_heat = dist[v, dir][next_step]
                new_v_heat = u_heat
                # Add intermediate heat loss
                for k in range(take_steps):
                    t = u + dir * (k + 1)
                    new_v_heat += m[h - int(t.imag) - 1][int(t.real)]
                # Visit if we can reduce heat loss
                if v_heat is None or new_v_heat < v_heat:
                    dist[v, dir][next_step] = new_v_heat
                    q.put(Node(new_v_heat, next_step, dir, v))

    return min(heat for heat in chain(dist[end, 1+0j], dist[end, -1j]) if heat is not None)


print(solve(1, 3))
print(solve(4, 10))
