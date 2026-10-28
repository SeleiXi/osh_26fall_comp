import csv,json,subprocess,time
from pathlib import Path
root=Path('.');out=root/'dse_results';baseline=json.loads((out/'outputs/hysteresis_1024_16.json').read_text())
with (out/'replay_log.csv').open('w',newline='',encoding='utf-8') as fh:
 wr=csv.writer(fh);wr.writerow(['window','context','horizon','mode','mean_ratio','max_ratio','status','seconds'])
 for W in (128,512):
  for K in (4,8,16):
   for H in (64,256):
    for mode in (0,1):
     start=time.time();results=[];status='ok';score='';maximum=''
     try:
      for item in baseline:
       name=item['trace'];f=item['frames'];num=int(subprocess.check_output([str(out/'context_replay.exe'),str(root/'data'/f'{name}.txt'),str(f),str(W),str(K),str(H),'16',str(mode)]));results.append({'trace':name,'frames':f,'faults':num,'opt':item['opt'],'ratio':num/item['opt']})
      score=sum(x['ratio'] for x in results)/len(results);maximum=max(x['ratio'] for x in results)
     except Exception as exc:status=repr(exc)
     (out/'outputs'/f'replay_{W}_{K}_{H}_{mode}.json').write_text(json.dumps(results,indent=2),encoding='utf-8');wr.writerow([W,K,H,mode,score,maximum,status,round(time.time()-start,2)]);fh.flush();print(W,K,H,mode,score,maximum,flush=True)
