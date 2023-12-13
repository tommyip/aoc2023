with open('inputs/day13.txt') as f:
    mirrors = [lines.split('\n') for lines in f.read().strip().split('\n\n')]


def mirror_line(mirror):
    h = len(mirror)
    for row in range(h - 1):
        for j in range(min(row + 1, h - row - 1)):
            if mirror[row-j] != mirror[row + 1 + j]:
                break
        else:
            return row


def smudge_line(mirror):
    w, h = len(mirror[0]), len(mirror)
    for row in range(h - 1):
        n_smudges = 0
        for j in range(min(row + 1, h - row - 1)):
            n_smudge = w - sum([a == b for a, b in zip(
                mirror[row - j], mirror[row + 1 + j])])
            n_smudges += n_smudge
            if n_smudge > 1:
                break
        if n_smudges == 1:
            return row


part1 = 0
part2 = 0
for i, mirror in enumerate(mirrors):
    mirror = [list(i) for i in mirror]
    mirror_t = [list(i) for i in zip(*mirror)]
    row = mirror_line(mirror)
    col = None
    if row is not None:
        part1 += 100 * (row + 1)
    else:
        col = mirror_line(mirror_t)
        part1 += col + 1

    srow = smudge_line(mirror)
    scol = None
    if srow is not None:
        part2 += 100 * (srow + 1)
    else:
        scol = smudge_line(mirror_t)
        part2 += scol + 1

print(part1)
print(part2)
