from collections import defaultdict

with open('inputs/day18.txt') as f:
    lines = f.read().splitlines()


def merge_intervals(intervals):
    intervals = [list(x) for x in sorted(intervals)]
    if len(intervals) == 0:
        return intervals
    merged = [intervals[0]]
    for current in intervals:
        previous = merged[-1]
        if current[0] <= previous[1]:
            previous[1] = max(previous[1], current[1])
        else:
            merged.append(current)
    return [tuple(x) for x in merged]


def solve(parse):
    pos = 0j
    levels = defaultdict(list)

    for line in lines:
        length, dir = parse(line)
        start = pos
        pos += dir * length
        if dir.imag == 0:
            # is a horizontal plane
            range_ = tuple(sorted((int(start.real), int(pos.real))))
            levels[int(start.imag)].append(range_)

    area = 0
    last_slices = []
    slices = []
    last_idx = 0
    for level_idx in sorted(levels):
        level = sorted(levels[level_idx])

        # Calculate areas
        for (a, b) in slices:
            area += (b - a + 1) * (level_idx - last_idx + 1)
        # Remove overlaps
        for a, b in last_slices:
            for u, v in slices:
                overlap = 0
                if a <= u <= b:
                    overlap = min(b, v) - u + 1
                elif a <= v <= b:
                    overlap = v - max(a, u) + 1
                elif u > a and v < b:
                    overlap = v - u + 1
                elif u < a and v > b:
                    overlap = b - a + 1
                area -= overlap
        last_slices = [x for x in slices]

        # Splice slices
        i = 0
        level_ = [x for x in level]
        while i < len(slices):
            j = 0
            bump = True
            while j < len(level_):
                s0, s1 = slices[i]
                l0, l1 = level_[j]
                # Remove
                if (s0, s1) == (l0, l1):
                    slices.pop(i)
                    bump = False
                # Split
                elif l0 > s0 and l1 < s1:
                    slices[i] = s0, l0
                    slices.insert(i+1, (l1, s1))
                # Truncate
                elif s0 == l0:
                    slices[i] = l1, s1
                elif s1 == l1:
                    slices[i] = s0, l0
                # Extend
                elif s1 == l0:
                    slices[i] = s0, l1
                elif s0 == l1:
                    slices[i] = l0, s1
                else:
                    j += 1
                    continue
                level_.pop(j)
            if bump:
                i += 1
        slices.extend(level_)
        slices = merge_intervals(slices)
        last_idx = level_idx

    return area


def parse1(line):
    dir, length, _ = line.split()
    dir_map = {
        'U': -1j,
        'D': 1j,
        'L': -1+0j,
        'R': 1+0j
    }
    return int(length), dir_map[dir]


def parse2(line):
    _, _, color = line.split()
    color = color.strip('()#')
    dir_map = [1+0j, 1j, -1+0j, -1j]
    return int(color[:-1], 16), dir_map[int(color[-1])]


print(solve(parse1))
print(solve(parse2))
