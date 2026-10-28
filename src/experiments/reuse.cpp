#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
 if(argc!=5)return 2;
 int F=stoi(argv[2]), mode=stoi(argv[3]), alpha=stoi(argv[4]); ifstream in(argv[1]);if(!in)return 3;
 unordered_map<string,int> ids;vector<int>a;string s;while(in>>s){auto[it,inserted]=ids.emplace(s,ids.size());a.push_back(it->second);}int n=ids.size();
 vector<int>last(n,-1),present(n),seen(n),gap(n);vector<double>ema(n,0);vector<int>res; long long faults=0;
 for(int t=0;t<(int)a.size();t++){
  int x=a[t];
  if(!present[x]){faults++; if((int)res.size()==F){
   auto score=[&](int p){double age=t-last[p]; double g=ema[p]>0?ema[p]:double(F*4); if(mode==0)return g; if(mode==1)return g-age; if(mode==2)return g+age; if(mode==3)return g/(age+1); if(mode==4)return age/g; if(mode==5)return -age/g; return g;};
   int k=0;for(int i=1;i<F;i++){double q=score(res[i]),r=score(res[k]);if(q>r || (q==r&&last[res[i]]>last[res[k]]))k=i;} present[res[k]]=0;res[k]=x;
  }else res.push_back(x);present[x]=1;}
  if(last[x]>=0){int g=t-last[x];ema[x]=ema[x]==0?g:(ema[x]*(alpha-1)+g)/alpha;gap[x]=g;}
  seen[x]++;last[x]=t;
 }
 cout<<faults<<'\n';
}
