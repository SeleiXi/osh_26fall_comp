import csv, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from page_replacement import FRAMES, opt, lru
from wfm_experiment import wfm, wfm512
from adaptive import adaptive
rng=random.Random(20261028)
traces={
 'cycle_7': [str(i%7) for i in range(7000)],
 'cycle_21': [str(i%21) for i in range(7000)],
 'hot_scan': [str(rng.randrange(8) if i%5 else 10000+i//5) for i in range(7000)],
 'phase_shift': [str(rng.randrange(15)+(0 if (i//1000)%2==0 else 100)) for i in range(7000)],
 'hot_cold': [str(rng.randrange(5) if rng.random()<0.85 else rng.randrange(5,100)) for i in range(7000)],
}
with open('results/synthetic_validation.csv','w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['trace','frames','OPT','LRU','WFM','WFM-512','Adaptive'])
 for name,pages in traces.items():
  for n in FRAMES:
   row=[name,n]+[fn(pages,n) for fn in (opt,lru,wfm,wfm512,adaptive)];w.writerow(row); print(*row,sep=',')
