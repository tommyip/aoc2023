from collections import Counter

with open('inputs/day07.txt') as f:
    lines = [line.split(' ') for line in f.read().splitlines()]

# part1 = 0
# strength = '23456789TJQKA'
# cards = []
# for hand, multiplier in lines:
#     hand_strength = sorted([strength.index(h) for h in hand], reverse=True)
#     # print(hand_strength)
#     strength_idx = Counter(hand_strength).most_common()
#     # print(strength_idx)
#     rank = []
#     for i in range(5):
#         kind = 5 - i
#         # rank.append(
#         #     max([s for (s, c) in strength_idx if c == kind], default=0))
#         rank.append(tuple(s for (s, c) in strength_idx if c == kind))
#     cards.append(tuple(rank))

# print(cards)

# print([x[1]
#        for x in sorted(enumerate(cards), reverse=True, key=lambda x: x[1])])
# orders = [len(cards) - x[0]
#           for x in sorted(enumerate(cards), reverse=True, key=lambda x: x[1])]
# print(orders)

# print(sum(int(multiplier) * order
#       for (_, multiplier), order in zip(lines, orders)))


part1 = 0
strength = '23456789TJQKA'
cards = []
for hand, multiplier in lines:
    hand_strength = sorted([strength.index(h) for h in hand], reverse=True)
    # print(hand_strength)
    strength_idx = Counter(hand_strength).most_common()
    # print(strength_idx)
    rank = []
    for i in range(5):
        kind = 5 - i
        rank.append(len(tuple(s for (s, c) in strength_idx if c == kind)))
    rank = tuple(rank)
    r = None
    if rank[0] == 1:
        r = 6
    elif rank[1] == 1:
        r = 5
    elif rank[2] == 1 and rank[3] == 1:
        r = 4
    elif rank[2] == 1:
        r = 3
    elif rank[3] == 2:
        r = 2
    elif rank[3] == 1:
        r = 1
    else:
        r = 0

    cards.append((r, *[strength.index(h) for h in hand]))


multipliers = [int(multiplier)
               for card, (_, multiplier) in sorted(zip(cards, lines), reverse=True, key=lambda x: x[0])]
# print(sum(int(multiplier) * order
#       for (_, multiplier), order in zip(lines, orders)))
print(sum((len(multipliers) - i) * multiplier for i,
      multiplier in enumerate(multipliers)))
