import re

with open('inputs/day01.txt') as f:
    lines = f.read().splitlines()

part1, part2 = 0, 0
for line in lines:
    digits = [int(c) for c in line if c.isdigit()]
    part1 += 10 * digits[0] + digits[-1]

print(part1)

words = ['one', 'two', 'three', 'four',
         'five', 'six', 'seven', 'eight', 'nine']


def word2digit(word):
    return int(word) if word.isdigit() else words.index(word) + 1


for line in lines:
    match = re.findall(
        '(?=(one|two|three|four|five|six|seven|eight|nine|\\d))', line)
    part2 += 10 * word2digit(match[0]) + word2digit(match[-1])

print(part2)
