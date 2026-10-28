"""Demand-paging simulations. Page identifiers are opaque, case-sensitive strings."""
import argparse
import csv
import heapq
import sys
from collections import OrderedDict, deque
from pathlib import Path

FRAMES = (5, 10, 20, 50, 100)


def read_trace(path):
    pages = []
    with open(path, encoding='utf-8-sig') as f:
        for number, line in enumerate(f, 1):
            page = line.strip()
            if not page:
                continue
            if len(page.split()) != 1:
                raise ValueError(f'{path}:{number}: expected one page identifier per line')
            pages.append(page)
    if not pages:
        raise ValueError(f'{path}: trace is empty')
    return pages


def fifo(pages, capacity):
    resident, order, faults = set(), deque(), 0
    for page in pages:
        if page in resident:
            continue
        faults += 1
        if len(resident) == capacity:
            resident.remove(order.popleft())
        resident.add(page)
        order.append(page)
    return faults


def lru(pages, capacity):
    resident, faults = OrderedDict(), 0
    for page in pages:
        if page in resident:
            resident.move_to_end(page)
        else:
            faults += 1
            if len(resident) == capacity:
                resident.popitem(last=False)
            resident[page] = None
    return faults


def second_chance(pages, capacity):
    queue, bits, faults = deque(), {}, 0
    for page in pages:
        if page in bits:
            bits[page] = True
            continue
        faults += 1
        if len(bits) == capacity:
            while bits[queue[0]]:
                old = queue.popleft()
                bits[old] = False
                queue.append(old)
            del bits[queue.popleft()]
        bits[page] = True
        queue.append(page)
    return faults


def opt(pages, capacity):
    # Next-use indices are computed offline; this is a theoretical lower bound.
    next_use = [len(pages)] * len(pages)
    last = {}
    for i in range(len(pages) - 1, -1, -1):
        next_use[i] = last.get(pages[i], len(pages))
        last[pages[i]] = i
    resident, heap, faults = {}, [], 0
    for i, page in enumerate(pages):
        if page not in resident:
            faults += 1
            if len(resident) == capacity:
                while heap:
                    neg_next, old = heapq.heappop(heap)
                    if resident.get(old) == -neg_next:
                        del resident[old]
                        break
        resident[page] = next_use[i]
        heapq.heappush(heap, (-next_use[i], page))
        # Discard stale heap entries periodically to bound memory.
        if len(heap) > 4 * capacity:
            heap = [(-n, p) for p, n in resident.items()]
            heapq.heapify(heap)
    return faults


def recency_frequency(pages, capacity, window=200):
    """Evict least referenced resident in recent window; break ties by LRU.

    The window tracks all references, including nonresident pages. No future
    references are used. Only demanded pages enter the resident set.
    """
    recent, counts, resident, faults = deque(), {}, OrderedDict(), 0
    for page in pages:
        if page in resident:
            resident.move_to_end(page)
        else:
            faults += 1
            if len(resident) == capacity:
                victim = min(resident, key=lambda p: counts.get(p, 0))
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


ALGORITHMS = {'FIFO': fifo, 'OPT': opt, 'LRU': lru,
              'SecondChance': second_chance, 'WindowFreq': recency_frequency}


def main():
    parser = argparse.ArgumentParser(description='Compare demand-paging replacement algorithms')
    parser.add_argument('trace', type=Path, help='one page identifier per line')
    parser.add_argument('--window', type=int, default=200, help='WindowFreq recent-reference window (default: 200)')
    parser.add_argument('--csv', type=Path, help='also write results as CSV')
    args = parser.parse_args()
    if args.window < 1:
        parser.error('--window must be positive')
    try:
        pages = read_trace(args.trace)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f'Error: {exc}\n')
    rows = []
    for name, algorithm in ALGORITHMS.items():
        results = [algorithm(pages, n, args.window) if name == 'WindowFreq' else algorithm(pages, n) for n in FRAMES]
        rows.append([name, *results, sum(results) / len(results)])
    print(f'Trace: {args.trace} | references: {len(pages)} | unique pages: {len(set(pages))} | window: {args.window}')
    print(f'{"Algorithm":<15}' + ''.join(f'{n:>10}' for n in FRAMES) + f'{"Average":>12}')
    for row in rows:
        print(f'{row[0]:<15}' + ''.join(f'{v:>10}' for v in row[1:-1]) + f'{row[-1]:>12.2f}')
    if args.csv:
        with args.csv.open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['algorithm', *FRAMES, 'average'])
            writer.writerows(rows)


if __name__ == '__main__':
    main()

