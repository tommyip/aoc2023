with open('inputs/day05.txt') as f:
    header, *groups = [g.strip().split('\n') for g in f.read().split('\n\n')]

seeds = list(map(int, header[0].split(': ')[1].split(' ')))
maps = []
for group in groups:
    map = []
    for line in group[1:]:
        dst, src, span = (int(x) for x in line.split(' '))
        map.append((src, src+span, dst-src))
    maps.append(map)

part1 = max(seeds)
for seed in seeds:
    for map in maps:
        for (src_lo, src_hi, delta) in map:
            if src_lo <= seed < src_hi:
                seed += delta
                break
    part1 = min(part1, seed)

print(part1)

seed_ranges = {(seeds[i*2], seeds[i*2]+seeds[i*2+1])
               for i in range(int(len(seeds)/2))}
seed_ranges_2 = set()
for map in maps:
    for src_lo, src_hi, delta in map:
        for seed_lo, seed_hi in list(seed_ranges):
            if seed_lo < src_lo and seed_hi >= src_hi:
                # split 3 way
                seed_ranges.remove((seed_lo, seed_hi))
                seed_ranges.add((seed_lo, src_lo))
                seed_ranges.add((src_hi, seed_hi))
                seed_ranges_2.add((src_lo + delta, src_hi + delta))
            elif src_lo <= seed_lo < src_hi:
                seed_ranges.remove((seed_lo, seed_hi))
                if seed_hi <= src_hi:
                    # no split
                    seed_ranges_2.add((seed_lo + delta, seed_hi + delta))
                else:
                    # split once
                    seed_ranges_2.add(
                        (seed_lo + delta, src_hi + delta))
                    seed_ranges.add((src_hi, seed_hi))
            elif src_lo <= seed_hi <= src_hi:
                # split once
                seed_ranges.remove((seed_lo, seed_hi))
                seed_ranges_2.add((src_lo + delta, seed_hi + delta))
                seed_ranges.add((seed_lo, src_lo))

    if len(seed_ranges) > 0:
        seed_ranges_2 = seed_ranges_2.union(seed_ranges)

    seed_ranges, seed_ranges_2 = seed_ranges_2, set()

print(min(min(seed_ranges)))
