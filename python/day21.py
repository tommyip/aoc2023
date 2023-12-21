"""
All tiles have the same cycle (period=2), they just start at different
steps. Also noticed that the steps expands in a diamond shape. At the end of
PART2_STEPS steps, the 4 tips of the diamond are plots at the last row/col of
its respective tile relative to the center tile. All the tip and edge tiles
of the diamond haven't started their cycle yet.

We need to find the number of plots at each step of a cycling tile, as well as
the number of plots for the 4 tip and 4 edge (there are more than 1 tile per
diamond edge but all tiles from the same edge follows the same sequence) at
each step from empty to full/cycle.

Once we have these numbers, we can count the number of cycling/inner and edge
tiles (number of tip tiles are always 4). Then for each tile and tile type we
find its number of stepped plots using our cycling, tip and edge sequence.
"""

from tqdm import tqdm
from collections import defaultdict
from typing import Dict, Tuple, List, Set

PART1_STEPS = 64
PART2_STEPS = 26501365

with open('inputs/day21.txt') as f:
    m = f.read().splitlines()

w, h = len(m[0]), len(m)

# Partition plots being stepped on into their respective tile
PlotsGrid = Dict[Tuple[int, int], Set[Tuple[int, int]]]
plots_grid: PlotsGrid = defaultdict(set)

for j, row in enumerate(m):
    i = row.find('S')
    if i != -1:
        plots_grid[0, 0].add((i, j))
        break


# Cache the state of the center tile until it cycles.
plots_seq_map: Dict[Tuple[Tuple[int, int]], int] = {}
# The pattern of a tile at the start of a cycle
cycle_pattern: Tuple[Tuple[int, int]] = None
# The number of plots at each step within a loop
cycle_num_plots: List[int]
# Ignore tile that is already looping
tile_cycling = set()

NEIGHBORS = ((0, -1), (1, 0), (0, 1), (-1, 0))
EDGES = ((1, 1), (1, -1), (-1, -1), (-1, 1))
# The plots expands in a diamond shape
tip_seq_map = defaultdict(list)
edge_seq_map = defaultdict(list)

# Simulate enough steps to reach an edge tile - this ensures we have also
# reached an inner and tip tile.
for step in tqdm(range(3 * w + w//2)):
    if step == PART1_STEPS:
        print(len(plots_grid[0, 0]))

    # Run step simulation
    next_plots_grid: PlotsGrid = defaultdict(set)
    for tile_i, tile_j in plots_grid:
        for i, j in plots_grid[tile_i, tile_j]:
            for di, dj in NEIGHBORS:
                world_u, world_v = tile_i*w + i + di, tile_j*h + j + dj
                u, v = world_u % w, world_v % h
                if m[u][v] != '#':
                    next_tile = world_u // w, world_v // h
                    if next_tile not in tile_cycling:
                        next_plots_grid[next_tile].add((u, v))

    for tile in list(next_plots_grid):
        # Get a hashable repr of the current tile
        frozen_plots = tuple(sorted(next_plots_grid[tile]))

        if tile == (0, 0):
            if frozen_plots in plots_seq_map:
                # Tile repeating
                cycle_pattern = frozen_plots
                cycle_start = plots_seq_map[frozen_plots]
                # Calculate number of plots at each step of the cycle
                cycle_plots_seq = sorted(
                    plots_seq_map.items(), key=lambda kv: kv[1])
                cycle_num_plots = [
                    len(plot) for plot, step in cycle_plots_seq if step >= cycle_start]
            else:
                plots_seq_map[frozen_plots] = step

        # Memorize the plots number progression of tip and edge tiles
        elif tile in NEIGHBORS:
            tip_seq_map[tile].append(len(frozen_plots))
        elif tile in EDGES:
            edge_seq_map[tile].append(len(frozen_plots))

        if frozen_plots == cycle_pattern:
            del next_plots_grid[tile]
            tile_cycling.add(tile)

    plots_grid = next_plots_grid

# Running all STEPS would reach the edge of the n_reached_tiles-th tile
# in all 4 neighboring directions
n_reached_tiles = PART2_STEPS // w
n_small_edges = n_reached_tiles
small_edge_steps = w // 2
n_big_edges = n_small_edges - 1
big_edge_steps = w + small_edge_steps
increase = 0
part2 = cycle_num_plots[0]

# Sum of plots of completely reached and cycling tiles
for i in range(1, n_reached_tiles):
    increase += 4
    part2 += increase * cycle_num_plots[i % 2]

# Add plots in the diamond tips
for tip_seq in tip_seq_map.values():
    part2 += tip_seq[w - 1]

# Add plots in the diamond edges
for edge_seq in edge_seq_map.values():
    part2 += n_small_edges * edge_seq[small_edge_steps - 1]
    part2 += n_big_edges * edge_seq[big_edge_steps - 1]

print(part2)
