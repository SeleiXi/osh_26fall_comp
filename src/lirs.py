"""LIRS page replacement described by Jiang and Zhang (SIGMETRICS 2002)."""
from collections import OrderedDict


def lirs(pages, capacity, hir_fraction=0.01):
    if capacity < 1:
        raise ValueError('capacity must be positive')
    if capacity == 1:
        last = object()
        faults = 0
        for page in pages:
            if page != last:
                faults += 1
                last = page
        return faults
    hir_limit = min(capacity - 1, max(1, int(capacity * hir_fraction)))
    lir_limit = capacity - hir_limit
    # S contains all LIR pages and HIR pages with retained history, oldest first.
    stack = OrderedDict()
    # Q contains only resident HIR pages, oldest first.
    queue = OrderedDict()
    lir = set()
    resident = set()
    faults = 0

    def prune():
        while stack and next(iter(stack)) not in lir:
            stack.popitem(last=False)

    for page in pages:
        in_stack = page in stack
        if page not in resident:
            faults += 1
            if len(resident) == capacity:
                victim, _ = queue.popitem(last=False)
                resident.remove(victim)
            resident.add(page)
            if len(lir) < lir_limit:
                lir.add(page)
            elif in_stack:
                lir.add(page)
                demoted = next(iter(stack))
                lir.remove(demoted)
                queue[demoted] = None
            else:
                queue[page] = None
        elif page not in lir:
            if in_stack:
                del queue[page]
                lir.add(page)
                demoted = next(iter(stack))
                lir.remove(demoted)
                queue[demoted] = None
            else:
                queue.move_to_end(page)
        stack[page] = None
        stack.move_to_end(page)
        prune()
    return faults
