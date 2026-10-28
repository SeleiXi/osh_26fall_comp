import csv, itertools, json, subprocess, sys, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'src'))
from page_replacement import FRAMES, opt, read_trace
root=Path(__file__).resolve().parents[2]
out=root/'dse_results'
traces=['sort1','lu','mm16','mm32']
opts={(name,f):opt(read_trace(root/'data'/f'{name}.txt'),f) for name in traces for f in FRAMES}
configs=[(64,4,1)]+[c for c in itertools.product((32,64,128,256),(2,4,8,16),(1,0)) if c!=(64,4,1)]
configs=configs[:32]
start=time.time(); best=None
with (out/'dse_log.csv').open('w',newline='',encoding='utf-8') as fh:
 writer=csv.writer(fh); writer.writerow(['iteration','minimum','scale','mru','mean_ratio_to_opt','status','elapsed_seconds'])
 for i,(minimum,scale,mru) in enumerate(configs):
  results=[]
  try:
   for name in traces:
    for f in FRAMES:
     run=subprocess.run([str(out/'sweep.exe'),str(root/'data'/f'{name}.txt'),str(f),str(minimum),str(scale),str(mru)],capture_output=True,text=True,check=True)
     n=int(run.stdout.strip()); results.append(dict(trace=name,frames=f,faults=n,opt=opts[name,f],ratio=n/opts[name,f]))
   score=sum(x['ratio'] for x in results)/len(results)
   status='ok'
   if best is None or score<best[0]: best=(score,i,minimum,scale,mru)
  except Exception as exc:
   score='';status=repr(exc)
  (out/'outputs'/f'iter_{i:02}.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
  (out/'configs'/f'iter_{i:02}.json').write_text(json.dumps(dict(minimum=minimum,scale=scale,mru=bool(mru))),encoding='utf-8')
  writer.writerow([i,minimum,scale,mru,score,status,round(time.time()-start,2)]);fh.flush()
  (out/'DSE_STATE.json').write_text(json.dumps(dict(iteration=i,best=best,status='in_progress',elapsed=time.time()-start),indent=2),encoding='utf-8')
  print(i, minimum,scale,mru, score,flush=True)
(out/'DSE_STATE.json').write_text(json.dumps(dict(iteration=i,best=best,status='sweep_complete',elapsed=time.time()-start),indent=2),encoding='utf-8')
