import re

with open('inputs/day02.txt') as f:
    lines = f.read().splitlines()

part1 = 0
part2 = 0
for i, line in enumerate(lines):
    fewest = {'red': 0, 'green': 0, 'blue': 0}
    counts = re.split('[,;] ', line.split(': ')[1])
    exceeded = False
    for count in counts:
        n, colour = count.split()
        n = int(n)
        if (colour == 'red' and n > 12 or
            colour == 'green' and n > 13 or
                colour == 'blue' and n > 14):
            exceeded = True
        fewest[colour] = max(fewest[colour], n)

    if not exceeded:
        print(i+1, end=' ')
        part1 += i + 1
    part2 += fewest['red'] * fewest['green'] * fewest['blue']

print(part1)
print(part2)
