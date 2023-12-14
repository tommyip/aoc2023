with open('inputs/day14.txt') as f:
    m = [list(l) for l in f.read().splitlines()]

w, h = len(m[0]), len(m)


def roll(m):
    moved = True
    while moved:
        moved = False
        for j in range(h - 1):
            for i in range(w):
                if m[j][i] == '.' and m[j+1][i] == 'O':
                    m[j][i] = 'O'
                    m[j+1][i] = '.'
                    moved = True


def load(m):
    return sum(sum(c == 'O' for c in l) * (h - j) for j, l in enumerate(m))


roll(m)
print(load(m))  # part 1

m_history = {'\n'.join(''.join(l) for l in m): 0}
for i in range(1, 1000):
    for _ in range(4):
        roll(m)
        m = [list(reversed(l)) for l in zip(*m)]

    m_ = '\n'.join(''.join(l) for l in m)
    if m_ in m_history:
        origin = m_history[m_]
        cycle = i - origin
        break
    m_history[m_] = i


cycle_offset = (1000000000 - origin) % cycle
for m_, i in m_history.items():
    if i == origin + cycle_offset:
        m_at_offset = m_

print(load(m_at_offset.split('\n')))  # part 2
