from math import prod

with open('inputs/day06.txt') as f:
    lines = f.read().splitlines()

inputs = [map(int, line.split()[1:]) for line in lines]
print(prod(sum(int(i * (time - i) > dist) for i in range(1, time))
           for time, dist in zip(*inputs)))

time, dist = [int(line[11:].replace(' ', '')) for line in lines]
print(sum(int(i * (time - i) > dist) for i in range(1, time)))
