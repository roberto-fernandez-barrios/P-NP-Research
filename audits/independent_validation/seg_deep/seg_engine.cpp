// seg_engine.cpp — standalone hostile SEG audit engine.
// Written from the SEG *statement* and the FLSY primary source (TR26-001)
// definitions ONLY.  No code or numbers reused from the repository engines
// or from the prior auditors' tools.
//
// The SEG event, my own formulation (Lemma S1 normal form):
//   ambient [N] (or Z_N), f uniform on {f:[N]->{-1,+1} : f([N]) = sigma},
//   fixed intervals A (nonempty) inside B, p = left slack, m = right slack,
//   L = p + m = |B|-|A|.  Event E(A,B,k):
//     exists a monotone lattice path (0,0) -> (p,m), steps +1 in one coord,
//     with |V(j,i)| <= k at every visited cell INCLUDING (0,0) and (p,m),
//   where V(j,i) = f(A) + lam(j) + rho(i),
//     lam(j) = f of the j points left-adjacent to A (reading outward),
//     rho(i) = f of the i points right-adjacent to A (reading outward).
//
// Modes:
//   exact   N sigma aSize p m k        exact probability (weighted over f|B)
//   scan    N sigma L kmax             adversarial max over (aSize,p) configs
//   cyc     N sigma                    per-coloring cyclic-vs-grid equality,
//                                      full enumeration (N <= 26)
//   mc      N sigma aSize p m k samples seed    Monte Carlo, huge N
//   walk    L split off k samples seed          offset-Frechet MC (pure walks)
//   fp      checks of the first-passage law (Lemma 4.5 basis), exact DP
//
// Exact mode: sum over xi in {-1,+1}^{|B|} of 1[E(xi)] * C(N-|B|, n+ - ones(xi)),
// divided by C(N, n+).  Exact in unsigned __int128 for N <= 60; long-double
// log-weights for larger N.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
typedef __uint128_t u128;
typedef long double ld;

static string u128str(u128 v){ if(!v) return "0"; string s; while(v){ s += char('0'+ (int)(v%10)); v/=10;} reverse(s.begin(), s.end()); return s; }

// ---------- binomials ----------
static u128 binom128(int n, int k){
    if(k<0||k>n) return 0;
    k = min(k, n-k);
    u128 r = 1;
    for(int i=1;i<=k;i++){ r = r*(u128)(n-k+i); r = r/(u128)i; }
    return r;
}
static ld lbinom(ld n, ld k){
    if(k<0||k>n) return -1e30L;
    return lgammal(n+1)-lgammal(k+1)-lgammal(n-k+1);
}

// ---------- the grid event ----------
// bits of xi: index 0..p-1  = left points, outward order (bit j-1 <-> lam step j)
//             index p..p+a-1 = A points
//             index p+a..p+a+m-1 = right points, outward order
// value of bit b: +1 if set else -1.
struct Cfg { int aSize, p, m, k; };
static bool eventGrid(u64 xi, const Cfg&c){
    int p=c.p, m=c.m, a=c.aSize, k=c.k;
    int sA=0; for(int t=0;t<a;t++) sA += (xi>>(p+t))&1 ? 1 : -1;
    if(abs(sA)>k) return false;
    static int lam[64], rho[64];
    lam[0]=0; for(int j=1;j<=p;j++) lam[j]=lam[j-1] + (((xi>>(j-1))&1)?1:-1);
    rho[0]=0; for(int i=1;i<=m;i++) rho[i]=rho[i-1] + (((xi>>(p+a+i-1))&1)?1:-1);
    // reachability over j-bitmask per column i
    u64 reach = 1ull; // j=0 reachable at i=0 (|V(0,0)|=|sA|<=k checked)
    // first, extend down column i=0: j passable iff |sA+lam[j]|<=k
    u64 pass0=0; for(int j=0;j<=p;j++) if(abs(sA+lam[j])<=k) pass0 |= (1ull<<j);
    if(!(pass0&1ull)) return false;
    // propagate within column: reach |= (reach<<1) & pass, iterated
    {
        u64 r=reach;
        for(;;){ u64 nr = (r | (r<<1)) & pass0; if(nr==r) break; r=nr; }
        reach = r;
    }
    for(int i=1;i<=m;i++){
        u64 pass=0; for(int j=0;j<=p;j++) if(abs(sA+lam[j]+rho[i])<=k) pass |= (1ull<<j);
        u64 r = reach & pass;           // step right
        for(;;){ u64 nr = (r | (r<<1)) & pass; if(nr==r) break; r=nr; } // steps down
        reach = r;
        if(!reach) return false;
    }
    return (reach>>p)&1ull;
}

// ---------- exact probability ----------
struct ExactRes { ld prob; bool exactInt; string num, den; };
static ExactRes exactProb(long long N, int sigma, const Cfg&c){
    int B = c.aSize + c.p + c.m;
    long long np = (N+sigma)/2;
    if((N+sigma)%2 != 0){ return {0.0L,false,"parity-mismatch",""}; }
    bool small = (N<=60);
    u128 num=0, den = small? binom128((int)N,(int)np) : 0;
    ld lnum = -1e30L, lden = lbinom((ld)N,(ld)np);
    vector<ld> lw(B+1); vector<u128> w(B+1);
    for(int s=0;s<=B;s++){
        long long rest = np - s; // ones outside B
        if(small) w[s] = binom128((int)(N-B), (int)rest);
        lw[s] = lbinom((ld)(N-B), (ld)rest);
    }
    for(u64 xi=0; xi < (1ull<<B); xi++){
        if(!eventGrid(xi,c)) continue;
        int s = __builtin_popcountll(xi);
        if(small) num += w[s];
        if(lw[s]>-1e29L){ ld hi = max(lnum, lw[s]), lo=min(lnum,lw[s]);
            lnum = hi + log1pl(expl(lo-hi)); }
    }
    ExactRes r;
    if(small){ r.prob = den? (ld)( (long double)(num)/(long double)(den) ):0.0L; r.exactInt=true; r.num=u128str(num); r.den=u128str(den); }
    else { r.prob = expl(lnum - lden); r.exactInt=false; }
    return r;
}

// ---------- cyclic evaluator (native, index arithmetic mod N) ----------
// full coloring f over Z_N; A = [a1..a1+aSize-1] cyclically; B extends p left, m right.
// event: exists chain of cyclic intervals A=D_0 c ... c D_L=B, all |f(D)|<=k.
// Native evaluation WITHOUT the grid claim: BFS over interval states (l,r)
// = cyclic interval [l..r]; extensions l-1 or r+1 (mod N); requires |D|<N.
static bool eventCyclicNative(const vector<int>&f, int N, int a1, int aSize, int p, int m, int k){
    int L = p+m; int a2 = (a1+aSize-1)%N;
    int bl = ((a1-p)%N+N)%N, br = (a2+m)%N;
    int sz0 = aSize;
    if(sz0 + L >= N+1) return false; // B must have size <= N (allow == N? we forbid B=Z_N)
    // f-sum of cyclic interval [x..y]
    auto ivsum=[&](int x,int len){ int s=0; for(int t=0;t<len;t++) s+=f[(x+t)%N]; return s; };
    int sA = ivsum(a1, aSize);
    if(abs(sA)>k) return false;
    // BFS over (l, size) states
    set<pair<int,int>> vis; deque<pair<int,int>> q;
    vis.insert({a1,aSize}); q.push_back({a1,aSize});
    int Bl=bl, Bsz=aSize+L;
    while(!q.empty()){
        auto [l,sz]=q.front(); q.pop_front();
        if(sz==Bsz && l==Bl) return true;
        if(sz>=Bsz) continue;
        // extend left
        int nl = ((l-1)%N+N)%N;
        // stay within B: check nl is in B: B = [Bl .. Bl+Bsz-1]
        auto inB=[&](int x){ int d=((x-Bl)%N+N)%N; return d<Bsz; };
        if(sz+1<=N && inB(nl)){
            int s = ivsum(nl, sz+1);
            if(abs(s)<=k && !vis.count({nl,sz+1})){ vis.insert({nl,sz+1}); q.push_back({nl,sz+1}); }
        }
        int r=(l+sz)%N; // next right point
        if(sz+1<=N && inB(r)){
            int s = ivsum(l, sz+1);
            if(abs(s)<=k && !vis.count({l,sz+1})){ vis.insert({l,sz+1}); q.push_back({l,sz+1}); }
        }
    }
    return false;
}

// ---------- Monte Carlo over colorings (huge N) ----------
static void mcMode(long long N, int sigma, Cfg c, long long samples, u64 seed){
    long long np=(N+sigma)/2;
    if((N+sigma)%2){ printf("parity mismatch\n"); return; }
    mt19937_64 rng(seed);
    int Bsz = c.aSize+c.p+c.m;
    // sample the restriction f|B directly from the conditional law:
    // hypergeometric: choose ones(B) ~ Hypergeom(N, np, Bsz), then place uniformly.
    // do it by sequential sampling of Bsz coordinates without replacement.
    long long hits=0;
    vector<int> bits(Bsz);
    for(long long it=0; it<samples; it++){
        long long onesLeft=np, tot=N;
        u64 xi=0;
        for(int t=0;t<Bsz;t++){
            u64 r = rng() % (u64)tot;
            int b = (r < (u64)onesLeft) ? 1:0;
            if(b){ xi |= (1ull<<t); onesLeft--; }
            tot--;
        }
        if(eventGrid(xi,c)) hits++;
    }
    printf("mc N=%lld sigma=%d a=%d p=%d m=%d k=%d samples=%lld hits=%lld phat=%.6e\n",
      N,sigma,c.aSize,c.p,c.m,c.k,samples,hits,(double)((ld)hits/(ld)samples));
}

// ---------- pure-walk offset-Frechet MC ----------
// X length mlen with X(0)=off ; Y length plen with Y(0)=0 ; iid +-1 steps.
// event: exists monotone path (0,0)->(plen,mlen) with |X(i)-Y(j)|<=k at all
// cells INCLUDING (0,0)  (matches the SEG chain event; d_F<=k only needs
// t>=1 but the chain includes t=0; we test the chain form).
static void walkMode(int L, int split, int off, int k, long long samples, u64 seed){
    int mlen=split, plen=L-split;
    mt19937_64 rng(seed);
    vector<int> X(mlen+1), Y(plen+1);
    vector<u64> reachW((plen+1+63)/64);
    long long hits=0;
    for(long long it=0; it<samples; it++){
        X[0]=off; for(int i=1;i<=mlen;i++) X[i]=X[i-1] + ((rng()&1)?1:-1);
        Y[0]=0;   for(int j=1;j<=plen;j++) Y[j]=Y[j-1] + ((rng()&1)?1:-1);
        if(abs(X[0]-Y[0])>k){ continue; }
        // column DP over i with bitmask over j (dynamic length)
        int W=(plen+1+63)/64;
        vector<u64> reach(W,0), pass(W,0);
        auto setbit=[&](vector<u64>&v,int b){ v[b>>6] |= (1ull<<(b&63)); };
        auto getbit=[&](const vector<u64>&v,int b)->bool{ return (v[b>>6]>>(b&63))&1ull; };
        auto shiftOrInPlace=[&](vector<u64>&v){ // v |= v<<1
            u64 carry=0;
            for(int w=0;w<W;w++){ u64 nc = v[w]>>63; v[w] |= (v[w]<<1)|carry; carry=nc; }
        };
        // i=0 column
        fill(pass.begin(),pass.end(),0);
        for(int j=0;j<=plen;j++) if(abs(X[0]-Y[j])<=k) setbit(pass,j);
        fill(reach.begin(),reach.end(),0); setbit(reach,0);
        for(;;){ auto old=reach; shiftOrInPlace(reach); for(int w=0;w<W;w++) reach[w]&=pass[w]; if(reach==old) break; }
        bool dead=false;
        for(int i=1;i<=mlen && !dead;i++){
            fill(pass.begin(),pass.end(),0);
            for(int j=0;j<=plen;j++) if(abs(X[i]-Y[j])<=k) setbit(pass,j);
            for(int w=0;w<W;w++) reach[w]&=pass[w];
            for(;;){ auto old=reach; shiftOrInPlace(reach); for(int w=0;w<W;w++) reach[w]&=pass[w]; if(reach==old) break; }
            dead=true; for(int w=0;w<W;w++) if(reach[w]) {dead=false;break;}
        }
        if(!dead && getbit(reach,plen)) hits++;
    }
    printf("walk L=%d mlen=%d plen=%d off=%d k=%d samples=%lld hits=%lld phat=%.6e\n",
      L,mlen,plen,off,k,samples,hits,(double)((ld)hits/(ld)samples));
}

// ---------- first-passage law checks (basis of FLSY Lemma 4.5) ----------
static void fpMode(){
    // exact DP for P[F_delta = y] (one-sided first passage of +-1 walk to +delta)
    // compare with the hitting-time-theorem formula (delta/y) 2^-y C(y,(y+delta)/2),
    // and tail P[F>=z] vs Theta(delta/sqrt z).
    for(int delta : {1,2,3,5}){
        int T=4000;
        vector<ld> cur(2*T+3,0.0L); int OFF=T+1;
        cur[OFF]=1.0L;
        vector<ld> hit(T+1,0.0L);
        for(int t=1;t<=T;t++){
            vector<ld> nxt(2*T+3,0.0L);
            for(int x=-t;x<=t;x++){
                ld v=cur[OFF+x]; if(v==0) continue;
                if(x>=delta) continue; // absorbed already
                int a=x+1,b=x-1;
                nxt[OFF+a]+=v*0.5L; nxt[OFF+b]+=v*0.5L;
            }
            hit[t]=nxt[OFF+delta]; // newly at delta (first time, since absorbed)
            cur.swap(nxt);
        }
        // formula check at several y
        printf("fp delta=%d:", delta);
        for(int y : {delta, delta+2, 10+ (delta%2), 100+(delta%2), 1000+(delta%2)}){
            if(y> T || (y-delta)%2) continue;
            ld formula = (ld)delta/(ld)y * expl(lbinom((ld)y,(ld)((y+delta)/2)) - (ld)y*logl(2.0L));
            printf("  y=%d dp=%.6e fm=%.6e", y, (double)hit[y], (double)formula);
        }
        printf("\n");
        // tail: P[F>=z]*sqrt(z)/delta should be ~const for z >> delta^2
        ld cum=0; vector<ld> tail(T+2,0);
        for(int y=T;y>=1;y--){ cum+=hit[y]; tail[y]=cum; }
        // note P[F>=z] for the INFINITE walk = tail[z] + P[no hit by T]; estimate latter:
        ld nohit=0; for(int x=-T;x<delta;x++) nohit+=cur[OFF+x];
        printf("fp-tail delta=%d:", delta);
        for(int z : {delta*delta*4, delta*delta*16, 400, 1600}){
            if(z>T) continue;
            ld p = tail[z]+nohit;
            printf("  z=%d P=%.4e P*sqrt(z)/d=%.4f", z, (double)p, (double)(p*sqrtl((ld)z)/delta));
        }
        printf("  (nohit@%d=%.3e)\n", T, nohit);
    }
}

int main(int argc, char**argv){
    if(argc<2){ fprintf(stderr,"mode?\n"); return 1; }
    string mode=argv[1];
    if(mode=="exact"){
        long long N=atoll(argv[2]); int sigma=atoi(argv[3]);
        Cfg c{atoi(argv[4]),atoi(argv[5]),atoi(argv[6]),atoi(argv[7])};
        ExactRes r=exactProb(N,sigma,c);
        printf("exact N=%lld sigma=%d a=%d p=%d m=%d k=%d P=%.10e", N,sigma,c.aSize,c.p,c.m,c.k,(double)r.prob);
        if(r.exactInt) printf("  = %s / %s", r.num.c_str(), r.den.c_str());
        printf("\n");
    } else if(mode=="scan"){
        long long N=atoll(argv[2]); int sigma=atoi(argv[3]); int L=atoi(argv[4]); int kmax=atoi(argv[5]);
        for(int k=1;k<=kmax;k++){
            ld best=-1; Cfg bc{0,0,0,0};
            for(int a=1;a<=3;a++) for(int p=0;p<=L;p++){
                Cfg c{a,p,L-p,k};
                if(a+L>26) continue;
                ExactRes r=exactProb(N,sigma,c);
                if(r.prob>best){ best=r.prob; bc=c; }
            }
            printf("scan N=%lld sigma=%d L=%d k=%d  max=%.8e at a=%d p=%d m=%d\n",
                N,sigma,L,k,(double)best,bc.aSize,bc.p,bc.m);
        }
    } else if(mode=="cyc"){
        int N=atoi(argv[2]); int sigma=atoi(argv[3]);
        // full enumeration over all colorings with sum sigma; compare native cyclic
        // event with grid event for a battery of (a1,aSize,p,m,k)
        long long np=(N+sigma)/2; if((N+sigma)%2){ printf("parity\n"); return 0; }
        vector<tuple<int,int,int,int,int>> cfgs;
        for(int a1 : {0, 3, N-2}) for(int aSize : {1,2}) for(int p : {0,2,3}) for(int m : {2,4})
            for(int k : {1,2}) if(aSize+p+m<N) cfgs.push_back({a1,aSize,p,m,k});
        long long mism=0, tested=0;
        vector<int> f(N);
        // iterate over all subsets with popcount np
        for(u64 mask=0; mask<(1ull<<N); mask++){
            if(__builtin_popcountll(mask)!=np) continue;
            for(int i=0;i<N;i++) f[i]= (mask>>i)&1 ? 1:-1;
            for(auto[a1,aSize,p,m,k]:cfgs){
                bool ec = eventCyclicNative(f,N,a1,aSize,p,m,k);
                // grid version: build xi in the engine's bit order
                u64 xi=0; int idx=0;
                for(int j=1;j<=p;j++){ int pos=((a1-j)%N+N)%N; if(f[pos]>0) xi|=1ull<<idx; idx++; }
                for(int t=0;t<aSize;t++){ int pos=(a1+t)%N; if(f[pos]>0) xi|=1ull<<idx; idx++; }
                int a2=(a1+aSize-1)%N;
                for(int i2=1;i2<=m;i2++){ int pos=(a2+i2)%N; if(f[pos]>0) xi|=1ull<<idx; idx++; }
                bool eg = eventGrid(xi,{aSize,p,m,k});
                tested++;
                if(ec!=eg){ mism++; if(mism<5) printf("MISMATCH mask=%llx a1=%d a=%d p=%d m=%d k=%d cyc=%d grid=%d\n",(unsigned long long)mask,a1,aSize,p,m,k,(int)ec,(int)eg); }
            }
        }
        printf("cyc N=%d sigma=%d tested=%lld mismatches=%lld\n",N,sigma,tested,mism);
    } else if(mode=="mc"){
        long long N=atoll(argv[2]); int sigma=atoi(argv[3]);
        Cfg c{atoi(argv[4]),atoi(argv[5]),atoi(argv[6]),atoi(argv[7])};
        mcMode(N,sigma,c,atoll(argv[8]),strtoull(argv[9],0,10));
    } else if(mode=="walk"){
        walkMode(atoi(argv[2]),atoi(argv[3]),atoi(argv[4]),atoi(argv[5]),atoll(argv[6]),strtoull(argv[7],0,10));
    } else if(mode=="fp"){
        fpMode();
    } else fprintf(stderr,"unknown mode\n");
    return 0;
}
