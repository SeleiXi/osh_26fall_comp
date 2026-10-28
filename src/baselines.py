"""Page-replacement baselines adapted from the supplied C++ implementations."""
from collections import Counter, OrderedDict, deque


def lfu256(pages, capacity):
    counts, recent, resident, faults = Counter(), deque(), OrderedDict(), 0
    for page in pages:
        recent.append(page)
        counts[page] += 1
        if len(recent) > 256:
            old = recent.popleft()
            counts[old] -= 1
        if page not in resident:
            faults += 1
            if len(resident) == capacity:
                victim = min(reversed(resident), key=lambda p: counts[p])
                del resident[victim]
            resident[page] = None
        else:
            resident.move_to_end(page)
    return faults


def s3fifo_simplified(pages, capacity):
    small, main, ghost = deque(), deque(), deque()
    state, freq = {}, Counter()
    count, faults = 0, 0
    main_target = capacity - max(1, int(capacity * 0.05))
    for page in pages:
        if state.get(page, 0) > 0:
            freq[page] = min(3, freq[page] + 1)
            continue
        faults += 1
        while count == capacity:
            if len(main) > main_target or not small:
                while True:
                    victim = main.popleft()
                    if freq[victim]:
                        freq[victim] -= 1
                        main.append(victim)
                    else:
                        state[victim] = 0
                        count -= 1
                        break
            else:
                victim = small.popleft()
                if freq[victim] > 0:
                    freq[victim] = 0
                    state[victim] = 2
                    main.append(victim)
                else:
                    count -= 1
                    state[victim] = -1
                    ghost.append(victim)
                    while len(ghost) > max(1, capacity * 4):
                        old = ghost.popleft()
                        if state.get(old) == -1:
                            state[old] = 0
        if state.get(page, 0) == -1:
            state[page] = 2
            main.append(page)
        else:
            state[page] = 1
            small.append(page)
        freq[page] = 0
        count += 1
    return faults
