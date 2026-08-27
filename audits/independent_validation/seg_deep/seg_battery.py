# seg_battery.py — orchestrates the exact/scan experiments for the SEG audit.
# Independent driver; cross-validates the C++ exact mode against a Python
# full enumeration at N=14, then runs the decay/split/N-scaling batteries.
import subprocess, sys, math, itertools

ENG = "./seg_engine.exe"

def run(*args):
    out = subprocess.run([ENG]+[str(a) for a in args], capture_output=True, text=True)
    return out.stdout.strip()

def pyth_exact(N, sigma, aSize, p, m, k, a1=0):
    # position-aware full enumeration on the CYCLE (tests translation too)
    npos = (N+sigma)//2
    assert (N+sigma) % 2 == 0
    from math import comb
    cnt = 0; tot = 0
    def ivsum(f,l,sz): return sum(f[(l+t)%N] for t in range(sz))
    for bits in range(1 << N):
        if bin(bits).count("1") != npos: continue
        tot += 1
        f = [1 if (bits>>i)&1 else -1 for i in range(N)]
        # grid DP at explicit position a1
        sA = ivsum(f,a1,aSize)
        if abs(sA) > k: continue
        ok = [[False]*(m+1) for _ in range(p+1)]
        good = True
        lam=[0]*(p+1); rho=[0]*(m+1)
        for j in range(1,p+1): lam[j]=lam[j-1]+f[(a1-j)%N]
        a2=(a1+aSize-1)%N
        for i in range(1,m+1): rho[i]=rho[i-1]+f[(a2+i)%N]
        for j in range(p+1):
            for i in range(m+1):
                if abs(sA+lam[j]+rho[i])<=k:
                    ok[j][i] = (j==0 and i==0) or (j>0 and ok[j-1][i]) or (i>0 and ok[j][i-1])
        if ok[p][m]: cnt += 1
    return cnt, tot

def main():
    which = sys.argv[1] if len(sys.argv)>1 else "all"

    if which in ("xval","all"):
        print("== cross-validation: C++ exact vs Python full enumeration, N=14 sigma=0, and translation ==")
        for (a,p,m,k) in [(1,3,4,1),(2,2,5,1),(1,0,6,1),(3,4,4,2),(1,5,5,2)]:
            cpp = run("exact", 14, 0, a, p, m, k)
            counts = set()
            for a1 in (0, 4, 13):
                c,t = pyth_exact(14,0,a,p,m,k,a1)
                counts.add(c)
            print(f"  cfg a={a} p={p} m={m} k={k}: python counts over a1(0,4,13) = {sorted(counts)} / {t}; cpp: {cpp.split('P=')[1]}")
            assert len(counts)==1, "TRANSLATION VARIANCE DETECTED"
            frac = list(counts)[0]/t
            cppP = float(cpp.split("P=")[1].split()[0])
            assert abs(frac-cppP) < 1e-9, (frac, cppP)
        print("  PASS: translation-exact and C++==Python")

    if which in ("decay","all"):
        print("== exact decay in L (N=4001 sigma=1, a=1, split p=m=L/2) ==")
        for k in (1,2):
            for L in (4,8,12,16,20,22):
                print("  ", run("exact", 4001, 1, 1, L//2, L//2, k))
        print("== same at N=2002 sigma=0 ==")
        for k in (1,):
            for L in (4,8,12,16,20,22):
                print("  ", run("exact", 2002, 0, 1, L//2, L//2, k))

    if which in ("split","all"):
        print("== split dependence (N=4001 sigma=1, a=1, L=16) ==")
        for k in (1,2):
            for p in (0,2,4,8,12,16):
                print("  ", run("exact", 4001, 1, 1, p, 16-p, k))

    if which in ("nscale","all"):
        print("== N-scaling at fixed (a=1,p=6,m=6,k=1), sigma=N%2 ==")
        for N in (15,21,41,101,1001,100001,10000001):
            print("  ", run("exact", N, N%2, 1, 6, 6, 1))
        print("== N-scaling at fixed (a=1,p=8,m=8,k=1) ==")
        for N in (19,21,41,101,1001,100001,10000001):
            print("  ", run("exact", N, N%2, 1, 8, 8, 1))

    if which in ("scan","all"):
        print("== adversarial scan (exact, N=41 sigma=1): max over a<=3, all splits ==")
        for L in (6,8,10,12,14,16,18,20):
            print(run("scan", 41, 1, L, 2))

    if which in ("offset","all"):
        print("== offset via aSize (N=4001 sigma=1, L=16, p=m=8) ==")
        for k in (1,2):
            for a in (1,2,3,4):
                print("  ", run("exact", 4001, 1, a, 8, 8, k))

if __name__=="__main__":
    main()
