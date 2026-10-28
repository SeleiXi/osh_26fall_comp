import csv
from pathlib import Path
from page_replacement import FRAMES, lru, read_trace, recency_frequency
from wfm_experiment import wfm

with open('results/wfm.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['trace', 'algorithm', *FRAMES, 'average'])
    for trace in ('sort1', 'lu', 'mm16', 'mm32'):
        pages = read_trace(Path('data') / (trace + '.txt'))
        for name, fn in [('WFM', wfm), ('WindowFreq', recency_frequency), ('LRU', lru)]:
            values = [fn(pages, n) for n in FRAMES]
            writer.writerow([trace, name, *values, sum(values) / len(values)])
