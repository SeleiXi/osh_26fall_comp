"""Online adaptive replacement with shadow-policy advice; no prefetching."""
from collections import Counter, deque, OrderedDict


class Shadow:
    def __init__(self, capacity, window, lru=False, mru=False, evaluation=1024):
        self.capacity = capacity
        self.window = window
        self.lru = lru
        self.mru = mru
        self.evaluation = evaluation
        self.resident = OrderedDict()
        self.recent = deque()
        self.counts = Counter()
        self.errors = deque()
        self.error_sum = 0

    def update(self, page):
        miss = page not in self.resident
        if miss:
            if len(self.resident) == self.capacity:
                if self.lru:
                    self.resident.popitem(last=False)
                elif self.mru:
                    self.resident.popitem(last=True)
                else:
                    victim = min(reversed(self.resident), key=lambda p: self.counts[p])
                    del self.resident[victim]
            self.resident[page] = None
        else:
            self.resident.move_to_end(page)
        self.recent.append(page)
        self.counts[page] += 1
        if len(self.recent) > self.window:
            old = self.recent.popleft()
            self.counts[old] -= 1
            if not self.counts[old]:
                del self.counts[old]
        self.errors.append(miss)
        self.error_sum += miss
        if len(self.errors) > self.evaluation:
            self.error_sum -= self.errors.popleft()


def adaptive(pages, capacity, evaluation=1024, switch_margin=16):
    """Use recent shadow misses to choose eviction advice using only past data."""
    shadows = [Shadow(capacity, 512, evaluation=evaluation),
               Shadow(capacity, max(64, 4 * capacity), evaluation=evaluation),
               Shadow(capacity, 1, lru=True, evaluation=evaluation),
               Shadow(capacity, 1, mru=True, evaluation=evaluation)]
    resident = OrderedDict()
    faults = 0
    best = shadows[0]
    for page in pages:
        if page not in resident:
            faults += 1
            if len(resident) == capacity:
                candidate = min(shadows, key=lambda p: p.error_sum)
                if candidate.error_sum + switch_margin < best.error_sum:
                    best = candidate
                victim = next((p for p in reversed(resident) if p not in best.resident), None)
                if victim is None:
                    victim = (next(iter(resident)) if best.lru else
                              next(reversed(resident)) if best.mru else
                              min(reversed(resident), key=lambda p: best.counts[p]))
                del resident[victim]
            resident[page] = None
        else:
            resident.move_to_end(page)
        for shadow in shadows:
            shadow.update(page)
    return faults
