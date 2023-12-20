from math import lcm
from queue import SimpleQueue

ff_state = {}
conj_state = {}
modules = {}
with open('inputs/day20.txt') as f:
    for line in f.read().splitlines():
        module, targets = line.split(' -> ')
        name = module.lstrip('%&')
        match module[0]:
            case '%': ff_state[name] = False
            case '&': conj_state[name] = {}
        modules[name] = targets.split(', ')

for module in modules:
    for target in modules[module]:
        if target in conj_state:
            conj_state[target][module] = False


n_low, n_high = 0, 0

q = SimpleQueue()


def q_extend(targets, is_high, source):
    for target in targets:
        q.put((target, is_high, source))


presses = 0
cycle_modules = ['pl', 'mz', 'lz', 'zm']
cycle_offsets = {}
while len(cycle_offsets) != 4:
    q.put(('broadcaster', False, 'button'))
    presses += 1
    while not q.empty():
        module, high, source = q.get()
        if module in cycle_modules and module not in cycle_offsets and not high:
            cycle_offsets[module] = presses
        if high:
            n_high += 1
        else:
            n_low += 1
        if module not in modules:
            continue
        targets = modules[module]
        if module == 'broadcaster':
            q_extend(targets, high, module)
        elif module in ff_state:
            if not high:
                on = ff_state[module] = not ff_state[module]
                q_extend(targets, on, module)
        elif module in conj_state:
            conj_state[module][source] = high
            if all(conj_state[module].values()):
                q_extend(targets, False, module)
            else:
                q_extend(targets, True, module)
    if presses == 1000:
        print(n_low * n_high)  # part 1

print(lcm(*cycle_offsets.values()))  # part 2
