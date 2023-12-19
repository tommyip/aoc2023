from operator import gt, lt
from typing import NamedTuple, Tuple, Literal

with open('inputs/day19.txt') as f:
    workflows_, ratings = [chunk.split() for chunk in f.read().split('\n\n')]
    ratings = [{r[0]: int(r[2:]) for r in rating.strip(
        '{}').split(',')} for rating in ratings]


class Rule(NamedTuple):
    key: Literal['x', 'm', 'a', 's']
    op: Literal['>', '<']
    thres: int
    target: str

    def __call__(self, **rating):
        cmp = {'>': gt, '<': lt}[self.op]
        return cmp(rating[self.key], self.thres)


workflows = {}
for workflow in workflows_:
    name, rules = workflow.rstrip('}').split('{')
    parsed_rules = []
    for rule in rules.split(','):
        if ':' in rule:
            rule, target = rule.split(':')
            key, op, thres = rule[0], rule[1], int(rule[2:])
            parsed_rules.append(Rule(key, op, thres, target))
        else:
            parsed_rules.append(rule)
    workflows[name] = parsed_rules


part1 = 0
for rating in ratings:
    target = 'in'
    while target not in 'AR':
        for rule in workflows[target]:
            if isinstance(rule, Rule):
                if rule(**rating):
                    target = rule.target
                    break
            else:
                target = rule
    if target == 'A':
        part1 += sum(rating.values())

print(part1)


class RangeGroup(NamedTuple):
    x: Tuple[int, int] = (1, 4000)
    m: Tuple[int, int] = (1, 4000)
    a: Tuple[int, int] = (1, 4000)
    s: Tuple[int, int] = (1, 4000)

    def combinations(self):
        return (
            (self.x[1]-self.x[0]+1) *
            (self.m[1]-self.m[0]+1) *
            (self.a[1]-self.a[0]+1) *
            (self.s[1]-self.s[0]+1))

    def restrict(self, rule: Rule, inverse=False):
        old = getattr(self, rule.key)
        if not inverse:
            match rule.op:
                case '>': new = rule.thres + 1, 4000
                case '<': new = 1, rule.thres - 1
        else:
            match rule.op:
                case '<': new = rule.thres, 4000
                case '>': new = 1, rule.thres
        return self._replace(**{rule.key: (max(old[0], new[0]), min(old[1], new[1]))})


range_groups = []


def find_ranges(target: str, group: RangeGroup):
    if target == 'A':
        range_groups.append(group)
        return
    if target == 'R':
        return
    for rule in workflows[target]:
        if isinstance(rule, Rule):
            find_ranges(rule.target, group.restrict(rule))
            group = group.restrict(rule, inverse=True)
        else:
            find_ranges(rule, group)


find_ranges('in', RangeGroup())
print(sum(group.combinations() for group in range_groups))
