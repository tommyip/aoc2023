from collections import Counter

with open('inputs/day07.txt') as f:
    lines = [line.split(' ') for line in f.read().splitlines()]

strength = '23456789TJQKA'
cards1 = []
for hand, multiplier in lines:
    hand_strength = [strength.index(h) for h in hand]
    strength_idx = Counter(hand_strength).most_common()
    rank = tuple(sum(c == 5 - i for (_, c) in strength_idx) for i in range(5))
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

    cards1.append((r, *[strength.index(h) for h in hand]))

multipliers = [int(multiplier)
               for card, (_, multiplier) in sorted(zip(cards1, lines), reverse=True, key=lambda x: x[0])]
print(sum((len(multipliers) - i) * multiplier for i,
      multiplier in enumerate(multipliers)))

strengthj = 'J23456789TQKA'
cards2 = []
for hand, multiplier in lines:
    j_count = sum(h == 'J' for h in hand)
    hand_strength = [strength.index(h) for h in hand if h != 'J']
    m = Counter(hand_strength).most_common()[0][0] if len(hand_strength) > 0 else len(strength)-1
    hand_strength = ([m] * j_count) + hand_strength
    strength_idx = Counter(hand_strength).most_common()
    rank = tuple(sum(c == 5 - i for (_, c) in strength_idx) for i in range(5))
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
    cards2.append((r, *[strengthj.index(h) for h in hand]))

multipliers = [int(multiplier)
               for card, (_, multiplier) in sorted(zip(cards2, lines), reverse=True, key=lambda x: x[0])]
print(sum((len(multipliers) - i) * multiplier for i,
      multiplier in enumerate(multipliers)))
