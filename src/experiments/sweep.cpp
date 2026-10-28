#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
 if(argc!=6) return 2;
 int f=stoi(argv[2]), w=max(stoi(argv[3]),stoi(argv[4])*f), mru=stoi(argv[5]);
 ifstream in(argv[1]); if(!in) return 3;
 unordered_map<string,int> ids; vector<int>a; string s;
 while(in>>s){auto [it,ins]=ids.emplace(s,ids.size()); a.push_back(it->second);}
 vector<int> count(ids.size(),0), last(ids.size(),-1), present(ids.size(),0); deque<int> recent; vector<int> res; long long faults=0;
 for(int t=0;t<(int)a.size();t++){
  int p=a[t];
  if(!present[p]){
   faults++;
   if((int)res.size()==f){int k=0; for(int i=1;i<f;i++){int x=res[i], y=res[k]; if(count[x]<count[y] || (count[x]==count[y] && (mru ? last[x]>last[y] : last[x]<last[y]))) k=i;} present[res[k]]=0;res[k]=p;} else res.push_back(p);
   present[p]=1;
  }
  last[p]=t; recent.push_back(p); count[p]++;
  if((int)recent.size()>w){count[recent.front()]--;recent.pop_front();}
 }
 cout<<faults<<"\n";
}
