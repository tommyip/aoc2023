import math
import re

with open('inputs/day08.txt') as f:
    instrs, _, *lines = f.read().splitlines()

lines = [re.findall('\w+', l) for l in lines]
m = {l[0]: (l[1], l[2]) for l in lines}

part1 = 0
i = 0
loc = 'AAA'
while True:
    turn = int(instrs[i] == 'R')
    loc = m[loc][turn]
    i = (i + 1) % len(instrs)
    part1 += 1
    if loc == 'ZZZ':
        break

print(part1)

loca = [loc for loc in m if loc[-1] == 'A']
part2 = 0
i = 0
stepsz = [None] * len(loca)
while True:
    turn = int(instrs[i] == 'R')
    for j, loc in enumerate(loca):
        loca[j] = m[loc][turn]
        if loca[j][-1] == 'Z' and stepsz[j] is None:
            stepsz[j] = part2 + 1
    i = (i + 1) % len(instrs)
    part2 += 1
    if all(x is not None for x in stepsz):
        break

print(math.lcm(*stepsz))
