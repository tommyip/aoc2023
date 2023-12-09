with open('inputs/day09.txt') as f:
    lines = [list(map(int, l.split(' '))) for l in f.read().splitlines()]

part1 = 0
part2 = 0
for history in lines:
    diffs = [history]
    last = history
    value = 0
    while True:
        value += last[-1]
        last = [last[i+1] - last[i] for i in range(len(last) - 1)]
        if all(x == 0 for x in last):
            break
        diffs.append(last)
    part1 += value
    x = 0
    for diff in reversed(diffs):
        x = diff[0] - x
    part2 += x

print(part1)
print(part2)
