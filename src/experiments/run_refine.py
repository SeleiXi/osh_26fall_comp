import csv, json, subprocess, sys, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'src'))
from page_replacement import FRAMES, opt, read_trace
root=Path(__file__).resolve().parents[2]; out=root/'dse_results'; names=['sort1','lu','mm16','mm32']
opts={(n,f):opt(read_trace(root/'data'/f'{n}.txt'),f) for n in names for f in FRAMES}
configs=[(m,s) for m,s in [(64,1),(128,1),(256,1),(512,1),(512,4),(512,8)]]
with (out/'dse_log.csv').open('a',newline='',encoding='utf-8') as fh:
 writer=csv.writer(fh)
 for i,(minimum,scale) in enumerate(configs,44):
  start=time.time();results=[];score='';status='ok'
  try:
   for name in names:
    for f in FRAMES:
     r=subprocess.run([str(out/'sweep.exe'),str(root/'data'/f'{name}.txt'),str(f),str(minimum),str(scale),'1'],capture_output=True,text=True,check=True)
     num=int(r.stdout.strip());results.append(dict(trace=name,frames=f,faults=num,opt=opts[name,f],ratio=num/opts[name,f]))
   score=sum(x['ratio'] for x in results)/len(results)
  except Exception as exc:status=repr(exc)
  (out/'outputs'/f'iter_{i:02}.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
  (out/'configs'/f'iter_{i:02}.json').write_text(json.dumps(dict(minimum=minimum,scale=scale,mru=True)),encoding='utf-8')
  writer.writerow([i,minimum,scale,1,score,status,round(time.time()-start,2)]);fh.flush()
  print(i,minimum,scale,score,flush=True)
