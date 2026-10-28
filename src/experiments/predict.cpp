#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
 if(argc!=7) return 2;
 int f=stoi(argv[2]),w=max(stoi(argv[3]),stoi(argv[4])*f),h=stoi(argv[5]), mode=stoi(argv[6]);
 ifstream in(argv[1]); if(!in) return 3;
 unordered_map<string,int> ids;vector<int>a;string s;while(in>>s){auto [it,ins]=ids.emplace(s,ids.size());a.push_back(it->second);}
 int n=ids.size(); vector<int>count(n),last(n,-1),present(n),succ(n,-1),steps(n,-1),stamp(n);deque<int>recent;vector<int>res;int prev=-1;long long faults=0;
 for(int t=0;t<(int)a.size();t++){
  int p=a[t];
  if(!present[p]){
   faults++;
   if((int)res.size()==f){
    int q=p;
    for(int i=1;i<=h;i++){q=succ[q];if(q<0)break;if(stamp[q]!=t+1){stamp[q]=t+1;steps[q]=i;}}
    int k=0;
    for(int i=1;i<f;i++){
     int x=res[i],y=res[k];int dx=stamp[x]==t+1?steps[x]:h+1,dy=stamp[y]==t+1?steps[y]:h+1;
     bool choose = mode==0 ? (dx>dy || (dx==dy && (count[x]<count[y] || (count[x]==count[y] && last[x]>last[y])))) : (count[x]<count[y] || (count[x]==count[y] && (dx>dy || (dx==dy && last[x]>last[y]))));
     if(choose)k=i;
    }
    present[res[k]]=0;res[k]=p;
   }else res.push_back(p);
   present[p]=1;
  }
  if(prev>=0)succ[prev]=p;
  prev=p;last[p]=t;recent.push_back(p);count[p]++;
  if((int)recent.size()>w){count[recent.front()]--;recent.pop_front();}
 }
 cout<<faults<<"\n";
}
