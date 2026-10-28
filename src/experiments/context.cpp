#include <bits/stdc++.h>
using namespace std;
static uint64_t key(int a,int b){return (uint64_t)(uint32_t)a<<32 | (uint32_t)b;}
int main(int argc,char**argv){
 if(argc!=7)return 2; int f=stoi(argv[2]),w=stoi(argv[3]),h=stoi(argv[4]),mode=stoi(argv[5]), minpredict=stoi(argv[6]);
 ifstream in(argv[1]);if(!in)return 3;unordered_map<string,int>ids;vector<int>a;string s;while(in>>s){auto[it,inserted]=ids.emplace(s,ids.size());a.push_back(it->second);}int n=ids.size();
 vector<int>count(n),last(n,-1),present(n),steps(n),stamp(n);deque<int>recent;vector<int>res;unordered_map<uint64_t,int> succ;int prev=-1, prev2=-1;long long faults=0;
 for(int t=0;t<(int)a.size();t++){
  int p=a[t];
  if(!present[p]){
   faults++;
   if((int)res.size()==f){
    int x=prev,y=p, length=0;
    if(x>=0)for(int i=1;i<=h;i++){auto it=succ.find(key(x,y));if(it==succ.end())break; int z=it->second;if(stamp[z]!=t+1){stamp[z]=t+1;steps[z]=i;}x=y;y=z;length=i;}
    int k=0;
    for(int i=1;i<f;i++){
     int x=res[i],y=res[k];int dx=stamp[x]==t+1?steps[x]:h+1,dy=stamp[y]==t+1?steps[y]:h+1;
     bool fcmp=(count[x]<count[y]||(count[x]==count[y] && last[x]>last[y]));
     bool choose=length>=minpredict && (mode==0 || (mode==1 && count[x]==count[y])) ? (dx>dy || (dx==dy&&fcmp)) : fcmp;
     if(choose)k=i;
    }
    present[res[k]]=0;res[k]=p;
   }else res.push_back(p);
   present[p]=1;
  }
  if(prev2>=0)succ[key(prev2,prev)]=p;
  prev2=prev;prev=p;last[p]=t;recent.push_back(p);count[p]++;
  if((int)recent.size()>w){count[recent.front()]--;recent.pop_front();}
 }
 cout<<faults<<"\n";
}
