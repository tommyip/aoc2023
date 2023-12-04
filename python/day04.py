import re

with open('inputs/day04.txt') as f:
    lines = f.read().splitlines()

part1 = 0
copies = [1] * len(lines)
for i, line in enumerate(lines):
    [theirs, ours] = line.split(': ')[1].split(' | ')
    theirs = set(int(x) for x in re.split(r'\s+', theirs.strip()))
    ours = set(int(x) for x in re.split(r'\s+', ours.strip()))
    intersect = theirs.intersection(ours)
    match = len(intersect)
    for j in range(match):
        copies[i + j + 1] += copies[i]
    if match > 0:
        part1 += 2 ** (match - 1)

print(part1)
print(sum(copies))
