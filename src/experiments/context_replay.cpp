#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
 if(argc!=8)return 2;
 int F=stoi(argv[2]),W=stoi(argv[3]),K=stoi(argv[4]),H=stoi(argv[5]),minimum=stoi(argv[6]),mode=stoi(argv[7]);
 ifstream in(argv[1]);if(!in)return 3;unordered_map<string,int>ids;vector<int>a;string s;while(in>>s){auto[it,ins]=ids.emplace(s,ids.size());a.push_back(it->second);}int n=ids.size();
 vector<int> count(n),last(n,-1),present(n),stamp(n),steps(n);deque<int>recent;vector<int>res;unordered_map<unsigned long long,int> seen;unsigned long long hash=0,base=1000003,power=1;for(int i=0;i<K;i++)power*=base;int faults=0;
 for(int t=0;t<(int)a.size();t++){
  int x=a[t]; hash=hash*base+(unsigned long long)x+1;if(t>=K)hash-=power*((unsigned long long)a[t-K]+1);
  int prior=-1;if(t>=K-1){auto it=seen.find(hash);if(it!=seen.end())prior=it->second;}
  if(!present[x]){faults++;if((int)res.size()==F){
    int len=(prior>=0)?min(H,t-prior-1):0;
    if(len>=minimum)for(int i=1;i<=len;i++){int q=a[prior+i];if(stamp[q]!=t+1){stamp[q]=t+1;steps[q]=i;}}
    int k=0;for(int i=1;i<F;i++){
     int u=res[i],v=res[k];bool freq=count[u]<count[v]||(count[u]==count[v]&&last[u]>last[v]);int du=stamp[u]==t+1?steps[u]:len+1,dv=stamp[v]==t+1?steps[v]:len+1;
     bool take=(len>=minimum&&(mode==0||(mode==1&&count[u]==count[v])))?(du>dv||(du==dv&&freq)):freq;
     if(take)k=i;
    }
    present[res[k]]=0;res[k]=x;
   }else res.push_back(x);present[x]=1;
  }
  if(t>=K-1)seen[hash]=t;last[x]=t;recent.push_back(x);count[x]++;if((int)recent.size()>W){count[recent.front()]--;recent.pop_front();}
 }
 cout<<faults<<'\n';
}
