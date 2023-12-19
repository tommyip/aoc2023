with open('inputs/day18.txt') as f:
    lines = f.read().splitlines()


def solve(parser):
    pos = 0j
    area = 0
    boundary = 0
    for line in lines:
        dir, length = parser(*line.split())
        boundary += length
        pos, pos_ = pos + dir * length, pos
        area += pos.real * pos_.imag - pos_.real * pos.imag
    return abs(int(area) // 2) + (boundary // 2) + 1


print(solve(lambda d, l, _: (
    {'U': 1j, 'D': -1j, 'L': -1+0j, 'R': 1+0j}[d], int(l))))
print(solve(lambda _d, _l, c: (
    (1+0j, -1j, -1+0j, 1j)[int(c[-2])], int(c[2:-2], 16))))
