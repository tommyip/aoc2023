from itertools import chain
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Tuple
import queue

with open('inputs/day17.txt') as f:
    m = [[int(x) for x in l] for l in f.read().splitlines()]

w, h = len(m[0]), len(m)


@dataclass
class Dist:
    heat: int
    history: Tuple[complex]


dist = defaultdict(lambda: [None, None, None, None])
dist[complex(0, h-1), 1+0j][0] = Dist(0, tuple())
dist[complex(0, h-1), -1j][0] = Dist(0, tuple())

start = complex(0, h - 1)


@dataclass(order=True)
class Cell:
    heat: int
    steps: int
    dir: complex = field(compare=False)
    pos: complex = field(compare=False)


def solve():
    q = queue.PriorityQueue()
    q.put(Cell(0, 0, 1+0j, start))
    q.put(Cell(0, 0, -1j, start))

    while not q.empty():
        cell = q.get()
        u = cell.pos
        u_dist = dist[u, cell.dir][cell.steps]
        for dir in (1j, 1+0j, -1j, -1+0j):
            # no backwards
            if dir == -cell.dir:
                continue
            # no 3 consecutive
            if cell.dir == dir and cell.steps == 3:
                continue

            next_step = cell.steps + 1 if dir == cell.dir else 1

            v = u + dir
            if 0 <= v.real < w and 0 <= v.imag < h:
                v_dist = dist[v, dir][next_step]
                i, j = int(v.real), h - int(v.imag) - 1
                new_v_heat = u_dist.heat + m[j][i]
                if v_dist is None or new_v_heat < v_dist.heat:
                    dist[v, dir][next_step] = Dist(
                        new_v_heat, u_dist.history + (dir,))
                    q.put(Cell(new_v_heat, next_step, dir, v))

    min_heat = None
    for cell in chain(dist[complex(w-1, 0), 1+0j], dist[complex(w-1, 0), -1j]):
        if cell is not None:
            if min_heat is None:
                min_heat = cell.heat
            else:
                min_heat = min(cell.heat, min_heat)
    print(min_heat)


solve()
