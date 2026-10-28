#include <bits/stdc++.h>
using namespace std;
vector<int> predstamp, predsteps; int predtime=0, predlen=0;
struct Policy {
 int f,w,which; vector<int>count,last,present,res;deque<int>recent; int faults=0;deque<int>errs;int errsum=0, period;
 Policy(int n,int F,int W,int K,int P):f(F),w(W),which(K),count(n),last(n,-1),present(n),period(P){}
 bool has(int p){return present[p];}
 int choose(){int k=0;for(int i=1;i<(int)res.size();i++){int x=res[i],y=res[k];bool freq=count[x]<count[y]||(count[x]==count[y]&&last[x]>last[y]); int dx=predstamp[x]==predtime?predsteps[x]:predlen+1,dy=predstamp[y]==predtime?predsteps[y]:predlen+1; bool take=which==0?last[x]<last[y]:(which==2?last[x]>last[y]:(which==3 && predlen>=16 ? (dx>dy||(dx==dy&&freq)) : freq));if(take)k=i;}return k;}
 void update(int p,int t){bool miss=!present[p];if(miss){faults++;if((int)res.size()==f){int k=choose();present[res[k]]=0;res[k]=p;}else res.push_back(p);present[p]=1;}last[p]=t;recent.push_back(p);count[p]++;if((int)recent.size()>w){count[recent.front()]--;recent.pop_front();}errs.push_back(miss);errsum+=miss;if((int)errs.size()>period){errsum-=errs.front();errs.pop_front();}}
};
int main(int argc,char**argv){if(argc!=6)return 2;int f=stoi(argv[2]),period=stoi(argv[3]),mode=stoi(argv[4]);ifstream in(argv[1]);if(!in)return 3;unordered_map<string,int>ids;vector<int>a;string s;while(in>>s){auto[it,x]=ids.emplace(s,ids.size());a.push_back(it->second);}int n=ids.size();predstamp.resize(n);predsteps.resize(n);unordered_map<unsigned long long,int> seen; unsigned long long hash=0,base=1000003,power=1;for(int i=0;i<4;i++)power*=base;
 vector<Policy> p;p.emplace_back(n,f,512,1,period);p.emplace_back(n,f,max(64,4*f),1,period);p.emplace_back(n,f,1,0,period);p.emplace_back(n,f,1,2,period); p.emplace_back(n,f,stoi(argv[5]),3,period);
 vector<int>real,present(n),last(n,-1);int faults=0;int chosen=0;
 for(int t=0;t<(int)a.size();t++){int x=a[t];hash=hash*base+(unsigned long long)x+1;if(t>=4)hash-=power*((unsigned long long)a[t-4]+1);int prior=-1;if(t>=3){auto it=seen.find(hash);if(it!=seen.end())prior=it->second;}predlen=prior>=0?min(256,t-prior-1):0;predtime=t+1;if(predlen>=16)for(int j=1;j<=predlen;j++){int q=a[prior+j];if(predstamp[q]!=predtime){predstamp[q]=predtime;predsteps[q]=j;}}if(!present[x]){faults++;if((int)real.size()==f){int candidate=chosen;for(int i=0;i<(int)p.size();i++)if(p[i].errsum<p[candidate].errsum)candidate=i; if(p[candidate].errsum+mode<p[chosen].errsum)chosen=candidate;int best=chosen;int victim=-1;for(int i=0;i<f;i++)if(!p[best].has(real[i])&&(victim<0||last[real[i]]>last[real[victim]]))victim=i;
 if(victim<0){victim=0;for(int i=1;i<f;i++){int u=real[i],v=real[victim];int cu=p[best].count[u],cv=p[best].count[v];bool freq=cu<cv||(cu==cv&&last[u]>last[v]);int du=predstamp[u]==predtime?predsteps[u]:predlen+1,dv=predstamp[v]==predtime?predsteps[v]:predlen+1; if(best==2 ? last[u]<last[v] : (best==3 ? last[u]>last[v] : (best==4&&predlen>=16 ? (du>dv||(du==dv&&freq)) : freq)))victim=i;}}
 present[real[victim]]=0;real[victim]=x;}else real.push_back(x);present[x]=1;}last[x]=t;for(auto &policy:p)policy.update(x,t);if(t>=3)seen[hash]=t;}
 cout<<faults<<"\n";}

