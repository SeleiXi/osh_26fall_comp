from collections import deque, OrderedDict


def _window_frequency_mru(pages, capacity, window):
    """Windowed frequency with MRU tie-break, W=max(64, 4*capacity)."""
    recent, counts, resident, faults = deque(), {}, OrderedDict(), 0
    for page in pages:
        if page in resident:
            resident.move_to_end(page)
        else:
            faults += 1
            if len(resident) == capacity:
                victim = min(reversed(resident), key=lambda p: counts.get(p, 0))
                del resident[victim]
            resident[page] = None
        recent.append(page)
        counts[page] = counts.get(page, 0) + 1
        if len(recent) > window:
            old = recent.popleft()
            counts[old] -= 1
            if not counts[old]:
                del counts[old]
    return faults


def wfm(pages, capacity):
    """Original WFM: window max(64, 4 * capacity)."""
    return _window_frequency_mru(pages, capacity, max(64, 4 * capacity))


def wfm512(pages, capacity):
    """WFM with a 512-reference window, selected on provided traces."""
    return _window_frequency_mru(pages, capacity, 512)
