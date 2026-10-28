import csv,sys,subprocess,json
from pathlib import Path
sys.path.insert(0,'src')
from page_replacement import FRAMES,opt,read_trace
root=Path('.'); out=root/'dse_results';names=['sort1','lu','mm16','mm32'];pairs=[(n,f) for n in names for f in FRAMES]
opts={(n,f):opt(read_trace(root/'data'/f'{n}.txt'),f) for n,f in pairs}
with (out/'hysteresis_log.csv').open('w',newline='') as fh:
 wr=csv.writer(fh);wr.writerow(['period','margin','mean_ratio','cycle7_f5','phase_f20'])
 for period in (256,512,1024,2048):
  for margin in (0,4,16,32,64):
   rows=[]
   for n,f in pairs:
    num=int(subprocess.check_output([str(out/'adaptive.exe'),str(root/'data'/f'{n}.txt'),str(f),str(period),str(margin)]));rows.append({'trace':n,'frames':f,'faults':num,'opt':opts[n,f],'ratio':num/opts[n,f]})
   score=sum(x['ratio'] for x in rows)/20
   c=int(subprocess.check_output([str(out/'adaptive.exe'),str(out/'outputs/cycle_7.txt'),'5',str(period),str(margin)]))
   p=int(subprocess.check_output([str(out/'adaptive.exe'),str(out/'outputs/phase_shift.txt'),'20',str(period),str(margin)]))
   wr.writerow([period,margin,score,c,p]);fh.flush();(out/'outputs'/f'hysteresis_{period}_{margin}.json').write_text(json.dumps(rows,indent=2));print(period,margin,round(score,5),c,p,flush=True)
