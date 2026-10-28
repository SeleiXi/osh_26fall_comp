#include <bits/stdc++.h>
using namespace std;
struct Policy {
 int f,w,which; vector<int>count,last,present,res;deque<int>recent; int faults=0;deque<int>errs;int errsum=0, period;
 Policy(int n,int F,int W,int K,int P):f(F),w(W),which(K),count(n),last(n,-1),present(n),period(P){}
 bool has(int p){return present[p];}
 int choose(){int k=0;for(int i=1;i<(int)res.size();i++){int x=res[i],y=res[k];bool take=which==0?last[x]<last[y]:(which==2?last[x]>last[y]:(count[x]<count[y]||(count[x]==count[y]&&last[x]>last[y])));if(take)k=i;}return k;}
 void update(int p,int t){bool miss=!present[p];if(miss){faults++;if((int)res.size()==f){int k=choose();present[res[k]]=0;res[k]=p;}else res.push_back(p);present[p]=1;}last[p]=t;recent.push_back(p);count[p]++;if((int)recent.size()>w){count[recent.front()]--;recent.pop_front();}errs.push_back(miss);errsum+=miss;if((int)errs.size()>period){errsum-=errs.front();errs.pop_front();}}
};
int main(int argc,char**argv){if(argc!=5)return 2;int f=stoi(argv[2]),period=stoi(argv[3]),mode=stoi(argv[4]);ifstream in(argv[1]);if(!in)return 3;unordered_map<string,int>ids;vector<int>a;string s;while(in>>s){auto[it,x]=ids.emplace(s,ids.size());a.push_back(it->second);}int n=ids.size();
 vector<Policy> p;p.emplace_back(n,f,512,1,period);p.emplace_back(n,f,max(64,4*f),1,period);p.emplace_back(n,f,1,0,period);
 vector<int>real,present(n),last(n,-1);int faults=0;int chosen=0;
 for(int t=0;t<(int)a.size();t++){int x=a[t];if(!present[x]){faults++;if((int)real.size()==f){int best=0;for(int i=1;i<3;i++)if(p[i].errsum<p[best].errsum)best=i;int victim=-1;for(int i=0;i<f;i++)if(!p[best].has(real[i])&&(victim<0||last[real[i]]>last[real[victim]]))victim=i;
 if(victim<0){victim=0;for(int i=1;i<f;i++){int u=real[i],v=real[victim];int cu=p[best].count[u],cv=p[best].count[v];if(best==2 ? last[u]<last[v] : (best==3 ? last[u]>last[v] : (cu<cv||(cu==cv&&last[u]>last[v]))))victim=i;}}
 present[real[victim]]=0;real[victim]=x;}else real.push_back(x);present[x]=1;}last[x]=t;for(auto &policy:p)policy.update(x,t);}
 cout<<faults<<"\n";}
