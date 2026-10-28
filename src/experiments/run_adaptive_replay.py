import csv,json,subprocess,time
from pathlib import Path
root=Path('.');out=root/'dse_results';baseline=json.loads((out/'outputs/hysteresis_1024_16.json').read_text())
with (out/'adaptive_replay_log.csv').open('w',newline='',encoding='utf-8') as fh:
 wr=csv.writer(fh);wr.writerow(['window','period','margin','mean_ratio','max_ratio','status','seconds'])
 for W in (128,512):
  for period in (256,1024,2048):
   for margin in (4,16,32):
    start=time.time();rows=[];status='ok';score='';maximum=''
    try:
     for item in baseline:
      name=item['trace'];f=item['frames'];num=int(subprocess.check_output([str(out/'adaptive_replay.exe'),str(root/'data'/f'{name}.txt'),str(f),str(period),str(margin),str(W)]));rows.append({'trace':name,'frames':f,'faults':num,'opt':item['opt'],'ratio':num/item['opt']})
     score=sum(x['ratio'] for x in rows)/len(rows);maximum=max(x['ratio'] for x in rows)
    except Exception as exc:status=repr(exc)
    (out/'outputs'/f'adaptive_replay_{W}_{period}_{margin}.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');wr.writerow([W,period,margin,score,maximum,status,round(time.time()-start,2)]);fh.flush();print(W,period,margin,round(score,6) if score else score,round(maximum,4) if maximum else maximum,flush=True)
