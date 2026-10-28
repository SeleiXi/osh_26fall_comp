import csv,json,subprocess,time
from pathlib import Path
root=Path('.'); out=root/'dse_results'; baseline=json.loads((out/'outputs/hysteresis_1024_16.json').read_text())
with (out/'reuse_log.csv').open('w',newline='',encoding='utf-8') as fh:
 wr=csv.writer(fh);wr.writerow(['mode','alpha','mean_ratio','max_ratio','status','seconds'])
 for mode in range(6):
  for alpha in (1,2,4,8):
   start=time.time();results=[];status='ok';score='';maximum=''
   try:
    for item in baseline:
     name=item['trace'];f=item['frames'];num=int(subprocess.check_output([str(out/'reuse.exe'),str(root/'data'/f'{name}.txt'),str(f),str(mode),str(alpha)]));results.append({'trace':name,'frames':f,'faults':num,'opt':item['opt'],'ratio':num/item['opt']})
    score=sum(x['ratio'] for x in results)/len(results);maximum=max(x['ratio'] for x in results)
   except Exception as exc:status=repr(exc)
   (out/'outputs'/f'reuse_{mode}_{alpha}.json').write_text(json.dumps(results,indent=2),encoding='utf-8');wr.writerow([mode,alpha,score,maximum,status,round(time.time()-start,2)]);fh.flush();print(mode,alpha,score,maximum,flush=True)
