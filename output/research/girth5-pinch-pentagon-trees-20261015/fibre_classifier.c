/* Exact fibre classifier for deleted configurations (exploratory; needs a C compiler).
 * Build: cc -O3 -o fibre_classifier fibre_classifier.c
 * Run:   python3 fibre_configs.py NAME | ./fibre_classifier [K r]
 * Input format and reported quantities: see fibre_configs.py and checkpoint.md. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 20
#define MAXP 24
int n, m, P;
int nbl[MAXN][MAXN], nbc[MAXN];
int portk[MAXP], portx[MAXP][MAXN];
int allowed[MAXN];
static uint64_t *S; static long ns, caps;
static int *compof, *stk;
static uint64_t *hk; static int *hv; static long hcap;

static inline uint64_t hh(uint64_t k){ k^=k>>33; k*=0xff51afd7ed558ccdULL; k^=k>>33; return k; }
static void hclear(long need){ long c=1; while(c<2*need+16) c<<=1; if(c>hcap){free(hk);free(hv);hk=malloc(8*c);hv=malloc(4*c);hcap=c;} memset(hk,0xff,8*hcap); }
static inline void hput(uint64_t k,int v){ uint64_t h=hh(k)&(hcap-1); while(hk[h]!=~0ULL) h=(h+1)&(hcap-1); hk[h]=k; hv[h]=v; }
static inline int hget(uint64_t k){ uint64_t h=hh(k)&(hcap-1); while(hk[h]!=~0ULL){ if(hk[h]==k) return hv[h]; h=(h+1)&(hcap-1);} return -1; }

int col[MAXN];
static void enumerate(int v, uint64_t code){
    if(v==n){ if(ns==caps){caps=caps?2*caps:4096; S=realloc(S,8*caps);} S[ns++]=code; return; }
    int forb=0; for(int j=0;j<nbc[v];j++){ int u=nbl[v][j]; if(u<v) forb|=1<<col[u]; }
    int av=allowed[v]&~forb;
    for(int c=0;c<4;c++) if(av>>c&1){ col[v]=c; enumerate(v+1, code|((uint64_t)c<<(2*v))); }
}

int main(int argc,char**argv){
    int K=argc>1?atoi(argv[1]):1, R=argc>2?atoi(argv[2]):0;
    if(scanf("%d %d %d",&n,&m,&P)!=3) return 1;
    for(int i=0;i<m;i++){ int a,b; scanf("%d %d",&a,&b); nbl[a][nbc[a]++]=b; nbl[b][nbc[b]++]=a; }
    for(int p=0;p<P;p++){ scanf("%d",&portk[p]); for(int j=0;j<portk[p];j++) scanf("%d",&portx[p][j]); }
    long nwords=0,mine=0,nempty=0,ndisc=0,niso=0,nbad=0,nk1=0,minsize=1L<<50,maxfib=0,minfib=1L<<50,maxcomps=0; double tot=0;
    int w[MAXP]; memset(w,0,sizeof w);
    while(1){
        int mx=-1,canon=1; for(int i=0;i<P;i++){ if(w[i]>mx+1){canon=0;break;} if(w[i]>mx) mx=w[i]; }
        if(canon){ nwords++;
          if((nwords-1)%K==R){ mine++;
            for(int x=0;x<n;x++) allowed[x]=15;
            for(int p=0;p<P;p++) for(int j=0;j<portk[p];j++) allowed[portx[p][j]]&=~(1<<w[p]);
            ns=0; enumerate(0,0); tot+=ns; if(ns>maxfib) maxfib=ns; if(ns<minfib) minfib=ns;
            if(!ns) nempty++;
            else {
              hclear(ns); for(long i=0;i<ns;i++) hput(S[i],(int)i);
              compof=realloc(compof,4*ns); stk=realloc(stk,4*ns); for(long i=0;i<ns;i++) compof[i]=-1;
              int nc=0, iso=0;
              for(long r=0;r<ns;r++){ if(compof[r]>=0) continue;
                long sp=0; stk[sp++]=r; compof[r]=nc; long size=0; int seen[MAXN]; memset(seen,0,sizeof seen);
                int kill[MAXP]; for(int p=0;p<P;p++) kill[p]=15&~(1<<w[p]);
                while(sp){ long s=stk[--sp]; size++; uint64_t code=S[s]; int deg=0; int c[MAXN];
                  for(int x=0;x<n;x++){ c[x]=(code>>(2*x))&3; seen[x]|=1<<c[x]; }
                  for(int p=0;p<P;p++){ int sm=0; for(int j=0;j<portk[p];j++) sm|=1<<c[portx[p][j]]; kill[p]&=sm; }
                  for(int x=0;x<n;x++){ int forb=~allowed[x]|(1<<c[x]); for(int j=0;j<nbc[x];j++) forb|=1<<c[nbl[x][j]];
                    int av=15&~forb; while(av){ int d=__builtin_ctz(av); av&=av-1; deg++;
                      uint64_t nc2=(code&~((uint64_t)3<<(2*x)))|((uint64_t)d<<(2*x)); int t=hget(nc2);
                      if(t>=0 && compof[t]<0){ compof[t]=nc; stk[sp++]=t; } } }
                  if(!deg) iso=1; }
                int kills=0; for(int p=0;p<P;p++) kills+=__builtin_popcount(kill[p]);
                if(kills>=2){ nbad++; if(nbad<=3){ printf("BAD word="); for(int i=0;i<P;i++) printf("%d",w[i]); printf(" compsize=%ld kills=%d\n",size,kills);} }
                if(kills==1) nk1++;
                if(size<minsize) minsize=size; nc++; }
              if(nc>1) ndisc++; if(nc>maxcomps) maxcomps=nc; if(iso) niso++;
            }
          }
        }
        int i=P-1; while(i>=0 && w[i]==3){ w[i]=0; i--; } if(i<0) break; w[i]++;
    }
    printf("part %d/%d words=%ld processed=%ld empty=%ld disconnected=%ld maxcomps=%ld iso=%ld comps>=2kills=%ld comps1kill=%ld mincomp=%ld minfibre=%ld maxfibre=%ld avgfibre=%.1f\n",
        R,K,nwords,mine,nempty,ndisc,maxcomps,niso,nbad,nk1,minsize,minfib,maxfib,mine?tot/mine:0);
    return 0;
}
