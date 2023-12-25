"""
Ran Dijkstra's shortest path on a large set of random source/destination
components. The top 3 most traversed edges are *likely* to be the 3 edges that
we need to cut to form two connected groups.
"""

import random
from queue import PriorityQueue
from collections import defaultdict, Counter

with open('inputs/day25.txt') as f:
    lines = f.read().splitlines()

components = defaultdict(list)
for line in lines:
    name, others = line.split(': ')
    for other_name in others.split(' '):
        components[name].append(other_name)
        components[other_name].append(name)


def dijkstra(source, dest):
    dists = defaultdict(int)
    q = PriorityQueue()
    q.put((0, source, set()))
    while not q.empty():
        _, comp, edges = q.get()
        if comp == dest:
            return edges
        for neighbor in components[comp]:
            new_dist = dists[comp] + 1
            if neighbor not in dists or new_dist < dists[neighbor]:
                dists[neighbor] = new_dist
                q.put((new_dist, neighbor, edges.union(
                    {tuple(sorted([comp, neighbor]))})))


def reachable(root, ignore_edges):
    visited = set()
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        visited.add(node)
        for neighbor in components[node]:
            edge = tuple(sorted((node, neighbor)))
            if any(ignored == edge for ignored in ignore_edges):
                continue
            if neighbor not in visited:
                stack.append(neighbor)
    return len(visited)


counter = Counter()
for _ in range(300):
    source, dest = random.sample(list(components.keys()), k=2)
    counter.update(dijkstra(source, dest))
triple = counter.most_common(3)
(d1, _), (d2, _), (d3, _) = triple
reachable = reachable(source, (d1, d2, d3))

print(reachable * (len(components) - reachable))
