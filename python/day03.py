import re

with open('inputs/day03.txt') as f:
    lines = f.read().splitlines()
w, h = len(lines[0]), len(lines)

part1 = 0
part2 = 0
nums = {}
for j, line in enumerate(lines):
    for m in re.finditer(r'\d+', line):
        i0 = m.start()
        i1 = m.end()
        num = int(m[0])
        for k in range(len(m[0])):
            nums[(j, i0 + k)] = num

        neighbors = ''
        if j - 1 >= 0:
            neighbors += lines[j - 1][max(0, i0 - 1):min(w, i1 + 1)]
        if i0 > 0:
            neighbors += lines[j][i0 - 1]
        if i1 < w:
            neighbors += lines[j][i1]
        if j + 1 < h:
            neighbors += lines[j + 1][max(0, i0 - 1):min(w, i1 + 1)]
        if re.search(r'[^\d.]', neighbors):
            part1 += num

for j, line in enumerate(lines):
    for m in re.finditer(r'\*', line):
        i = m.start()
        stars = []
        for dj, di in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            i_, j_ = i + di, j + dj
            if (j_, i_) in nums and nums[(j_, i_)] not in stars:
                stars.append(nums[(j_, i_)])
        if len(stars) == 2:
            part2 += stars[0] * stars[1]

print(part1)
print(part2)
