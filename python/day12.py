from itertools import repeat
from functools import lru_cache

with open('inputs/day12.txt') as f:
    lines = f.read().splitlines()

def solve(records, r_i, groups, g_i):
    @lru_cache
    def aux(r_i, g_i):
        # Base cases
        if r_i == len(records):
            return int(g_i == len(groups))
        if g_i == len(groups):
            return all(c in '.?' for c in records[r_i:])
        if sum(groups[g_i:]) + len(groups) - g_i - 1 > len(records) - r_i:
            return 0

        # Recursive cases
        # Case 1: Advance til not .
        if records[r_i] == '.':
            r_i += 1
            while r_i < len(records) and records[r_i] == '.':
                r_i += 1
            return aux(r_i, g_i)

        # Case 2: Set ?s as #
        arrangements = 0
        group_len = groups[g_i]
        header = records[r_i:r_i+group_len]
        if all(c in '?#' for c in header):
            if r_i + group_len == len(records) or records[r_i + group_len] in '?.':
                arrangements += aux(r_i + group_len + 1, g_i + 1)

        # Case 3: Set ? as .
        if records[r_i] == '?':
            arrangements += aux(r_i + 1, g_i)
        return arrangements
    return aux(r_i, g_i)

part1 = 0
part2 = 0
for line in lines:
    records, groups = line.split(' ')
    groups = [int(x) for x in groups.split(',')]
    part1 += solve(records, 0, groups, 0)
    part2 += solve('?'.join(repeat(records, 5)), 0, groups * 5, 0)

print(part1, part2)
