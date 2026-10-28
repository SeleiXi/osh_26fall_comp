"""A page-trace adaptation of MemoryOS's segment heat eviction, not MemoryOS itself."""
import math
from collections import OrderedDict


def memoryos_heat(pages, capacity, tau=200):
    # One page represents one segment; each load starts a new resident lifetime.
    # N_visit is the number of accesses in that lifetime; L_interaction = 1.
    resident = OrderedDict()
    faults = 0
    for t, page in enumerate(pages):
        if page in resident:
            count, _ = resident[page]
            resident[page] = (count + 1, t)
            resident.move_to_end(page)
        else:
            faults += 1
            if len(resident) == capacity:
                victim = min(resident, key=lambda p: resident[p][0] + 1 + math.exp(-(t - resident[p][1]) / tau))
                del resident[victim]
            resident[page] = (1, t)
    return faults

