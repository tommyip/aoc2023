import re

with open('inputs/day15.txt') as f:
    init_seq = f.read().strip().split(',')


def hash(value):
    sum = 0
    for c in value:
        sum = ((sum + ord(c)) * 17) % 256
    return sum


# part 1
print(sum(hash(x) for x in init_seq))

boxes = [[] for _ in range(256)]
for step in init_seq:
    match = re.search(r'([a-z]+)(-|=)(\d+)?', step)
    label, op, fl = match.groups()
    box = boxes[hash(label)]
    match op:
        case '-':
            for i, (their_label, _) in enumerate(box):
                if their_label == label:
                    box.pop(i)
                    break
        case '=':
            for i, (their_label, _) in enumerate(box):
                if their_label == label:
                    box[i] = (label, int(fl))
                    break
            else:
                box.append((label, int(fl)))


part2 = 0
for i, box in enumerate(boxes):
    for slot, (_, fl) in enumerate(box):
        part2 += (i + 1) * (slot + 1) * fl

print(part2)
