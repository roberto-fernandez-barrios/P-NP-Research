# seg_bruteforce_chains.py — independent validation of the grid normal form
# (Lemma S1) by LITERAL enumeration of nested interval chains, tiny N.
# Written from the SEG statement only; no repository code reused.
#
# Linear check: ambient [0..N-1]; A=[a1..a2], B=[b1..b2]; chains D_0=A c ... c D_L=B,
#   every D_i an interval of the LINE (no wrap), |D_{i+1}|=|D_i|+1, all |f(D_i)|<=k.
#   Enumerated by DFS over interval states (the DFS is NOT told to stay inside B;
#   nestedness must prune escapes by itself), compared with monotone lattice-path
#   reachability computed by an independent 2D boolean DP.
# Cyclic check: ambient Z_N; A,B cyclic intervals, B != Z_N; chains through
#   cyclic intervals (extensions may wrap; the DFS is NOT told about any cut).
#   Compared with the lattice DP after cutting at a point outside B
#   (tests the no-wrap lemma of the cyclic reduction).
import random

def intervals_chain_exists_linear(f, N, a1, a2, b1, b2, k):
    pre = [0]*(N+1)
    for i in range(N): pre[i+1] = pre[i] + f[i]
    def s(l, r): return pre[r+1] - pre[l]
    if abs(s(a1, a2)) > k: return False
    seen = set(); stack = [(a1, a2)]
    while stack:
        l, r = stack.pop()
        if (l, r) == (b1, b2): return True
        if (l, r) in seen: continue
        seen.add((l, r))
        if l-1 >= 0 and abs(s(l-1, r)) <= k: stack.append((l-1, r))
        if r+1 < N and abs(s(l, r+1)) <= k: stack.append((l, r+1))
    return False

def grid_reach_linear(f, N, a1, a2, b1, b2, k):
    p = a1 - b1; m = b2 - a2
    pre = [0]*(N+1)
    for i in range(N): pre[i+1] = pre[i] + f[i]
    def s(l, r): return pre[r+1] - pre[l]
    ok = [[False]*(m+1) for _ in range(p+1)]
    for j in range(p+1):
        for i in range(m+1):
            if abs(s(a1-j, a2+i)) <= k:
                if j == 0 and i == 0: ok[j][i] = True
                else: ok[j][i] = (j > 0 and ok[j-1][i]) or (i > 0 and ok[j][i-1])
    return ok[p][m]

def cyclic_chain_exists(f, N, a1, aSize, p, m, k):
    bl = (a1 - p) % N; bsz = aSize + p + m
    if bsz >= N: return None  # B = Z_N excluded from the endorsed statement
    def ivsum(l, sz): return sum(f[(l+t) % N] for t in range(sz))
    if abs(ivsum(a1, aSize)) > k: return False
    seen = set(); stack = [(a1, aSize)]
    while stack:
        l, sz = stack.pop()
        if (l, sz) == (bl, bsz): return True
        if (l, sz) in seen: continue
        seen.add((l, sz))
        if sz + 1 <= N - 1:
            nl = (l - 1) % N
            if abs(ivsum(nl, sz+1)) <= k: stack.append((nl, sz+1))
            if abs(ivsum(l, sz+1)) <= k: stack.append((l, sz+1))
    return False

def cut_and_grid(f, N, a1, aSize, p, m, k):
    bl = (a1 - p) % N; bsz = aSize + p + m
    cut = (bl + bsz) % N  # first point after B — outside B since bsz < N
    g = [f[(cut + 1 + t) % N] for t in range(N)]
    pos = lambda x: ((x - cut - 1) % N)
    A1 = pos(a1); A2 = pos((a1 + aSize - 1) % N)
    B1 = pos(bl); B2 = pos((bl + bsz - 1) % N)
    assert B1 <= A1 <= A2 <= B2, (B1, A1, A2, B2)
    return grid_reach_linear(g, N, A1, A2, B1, B2, k)

def main():
    random.seed(20260822)
    # LINEAR: N=11, all 2^11 colorings, random battery of configs
    N = 11; mism = 0; tot = 0
    cfgs = []
    for a1 in range(N):
        for a2 in range(a1, min(a1+2, N)):
            for b1 in range(max(0, a1-4), a1+1):
                for b2 in range(a2, min(a2+4, N)):
                    L = (a1-b1) + (b2-a2)
                    if 1 <= L <= 7:
                        for k in (1, 2): cfgs.append((a1, a2, b1, b2, k))
    cfgs = random.sample(cfgs, min(300, len(cfgs)))
    for bits in range(1 << N):
        f = [1 if (bits >> i) & 1 else -1 for i in range(N)]
        for (a1, a2, b1, b2, k) in cfgs:
            e1 = intervals_chain_exists_linear(f, N, a1, a2, b1, b2, k)
            e2 = grid_reach_linear(f, N, a1, a2, b1, b2, k)
            tot += 1
            if e1 != e2:
                mism += 1
                if mism < 5: print("LIN MISMATCH", bits, (a1, a2, b1, b2, k), e1, e2)
    print(f"linear: N={N} checks={tot} mismatches={mism}")
    # CYCLIC: N=11, all colorings, configs including wrap-around A/B positions
    mism = 0; tot = 0
    ccfgs = []
    for a1 in range(N):
        for aSize in (1, 2):
            for p in (0, 1, 3):
                for m in (1, 2, 4):
                    if aSize + p + m < N:
                        for k in (1, 2): ccfgs.append((a1, aSize, p, m, k))
    ccfgs = random.sample(ccfgs, min(250, len(ccfgs)))
    for bits in range(1 << N):
        f = [1 if (bits >> i) & 1 else -1 for i in range(N)]
        for (a1, aSize, p, m, k) in ccfgs:
            e1 = cyclic_chain_exists(f, N, a1, aSize, p, m, k)
            e2 = cut_and_grid(f, N, a1, aSize, p, m, k)
            tot += 1
            if e1 != e2:
                mism += 1
                if mism < 5: print("CYC MISMATCH", bits, (a1, aSize, p, m, k), e1, e2)
    print(f"cyclic: N={N} checks={tot} mismatches={mism}")

if __name__ == "__main__":
    main()
