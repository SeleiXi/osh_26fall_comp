import csv, json, subprocess, sys, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'src'))
from page_replacement import FRAMES, opt, read_trace
root=Path(__file__).resolve().parents[2];out=root/'dse_results';names=['sort1','lu','mm16','mm32']
opts={(n,f):opt(read_trace(root/'data'/f'{n}.txt'),f) for n in names for f in FRAMES}
configs=[(w,h,mode,minimum) for w in (128,512) for h in (32,128) for mode in (0,1) for minimum in (4,16)]
with (out/'context_log.csv').open('w',newline='',encoding='utf-8') as fh:
 writer=csv.writer(fh);writer.writerow(['iteration','window','horizon','mode','min_predict','mean_ratio','status','seconds'])
 for i,(w,h,mode,minimum) in enumerate(configs):
  start=time.time();results=[];score='';status='ok'
  try:
   for name in names:
    for f in FRAMES:
     r=subprocess.run([str(out/'context.exe'),str(root/'data'/f'{name}.txt'),str(f),str(w),str(h),str(mode),str(minimum)],capture_output=True,text=True,check=True)
     num=int(r.stdout.strip());results.append(dict(trace=name,frames=f,faults=num,opt=opts[name,f],ratio=num/opts[name,f]))
   score=sum(x['ratio'] for x in results)/len(results)
  except Exception as exc:status=repr(exc)
  (out/'outputs'/f'context_{i:02}.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
  writer.writerow([i,w,h,mode,minimum,score,status,round(time.time()-start,2)]);fh.flush();print(i,w,h,mode,minimum,score,flush=True)
