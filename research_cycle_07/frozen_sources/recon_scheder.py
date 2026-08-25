# NON-CERTIFYING RECONNAISSANCE for the Scheder import ledger (float-level).
# Checks plausibility of numeric claims in ECCC TR21-069 rev1 relevant to JC imports.
# Nothing here certifies anything; verdicts in the ledger rest on the printed text only.
import math
from math import log, sqrt

ln2 = math.log(2.0)

def integrate(f, a, b, n=200000):
    # Simpson's rule
    if n % 2: n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += f(x) * (4 if i % 2 else 2)
    return s * h / 3

def Q(r):  # k=3
    return (r / (1 - r))**2 if r < 0.5 else 1.0

def P(r):
    return r / (1 - r) if r < 0.5 else 1.0

print("=== s3 and baseline ===")
s3 = integrate(lambda r: Q(r), 0, 0.5) + 0.5
print("s3 numeric        :", s3)
print("2 - 2 ln 2        :", 2 - 2 * ln2)
print("2^(1-s3)          :", 2**(1 - s3), " (baseline base, cf. 1.3070319)")
print("2^(1-s3-1/15218)  :", 2**(1 - (2 - 2 * ln2) - 1 / 15218), " (cf. 1.306973)")

print()
print("=== Section 7 gamma, phi, delta_max ===")
def gam(r):
    return r * (1 - 2 * r)**1.5 if r < 0.5 else 0.0
def phi(r):
    return sqrt(1 - 2 * r) * (1 - 5 * r) if r < 0.5 else 0.0

# phi range check (source: -1/sqrt5 <= phi <= 1)
vals = [phi(i / 100000) for i in range(50000)]
print("min phi, max phi  :", min(vals), max(vals), " (-1/sqrt5 =", -1 / sqrt(5), ")")

def delta_max(r, eps):
    if r >= 0.5: return 0.0
    return 1.2 * eps * gam(r) * max(2 * gam(r) / (1 - r), gam(r) / (1 - r) - phi(r))

print()
print("=== Lemma 55 boost integral (0.001687) ===")
I55 = integrate(lambda r: gam(r)**2 * (1 - Q(r))**2, 0, 0.5)
print("int gamma^2 (1-Q)^2 =", I55, " (source floor 0.001687; OK if >= )")

print()
print("=== Lemma 53's 0.28 and 0.54 checks ===")
# 1.02*delta_root/(r(1-2r)) <= 0.28 eps ; delta_root = 1.2 eps gam max(0,-phi)
def ratio53(r):
    if r <= 0 or r >= 0.5: return 0.0
    droot = 1.2 * gam(r) * max(0.0, -phi(r))  # per eps
    return 1.02 * droot / (r * (1 - 2 * r))
m = max(ratio53(i / 200000) for i in range(1, 100000))
print("max 1.02*droot/(r(1-2r)) per eps =", m, "  (<= 0.28 ?)")
S = sum((d + 1)**(d + 1) / (d + 3)**(d + 3) for d in range(1, 2000))
print("sum_{d>=1}(d+1)^{d+1}/(d+3)^{d+3} =", S, " ; 9.792*S =", 9.792 * S, " (<= 0.54 ?)")

print()
print("=== Lemma 44/45 KL constants ===")
m2 = integrate(lambda r: phi(r)**2, 0, 1)
m3 = integrate(lambda r: phi(r)**3, 0, 1)
m4 = integrate(lambda r: phi(r)**4, 0, 1)
print("m2 =", m2, "(3/32 =", 3 / 32, ")  m3 =", m3, "(12/385 =", 12 / 385, ")  m4 =", m4, "(9/224 =", 9 / 224, ")")
t = 17
for eps in (0.13,):
    val = m2**2 / 2 + eps**2 * (m4**2 + 6 * m4 * m2**2 + 42 * m2**4) / 3  # per eps^2 t: (41)
    # (41): ln2*KL <= eps^2 t [ m2^2/2 + eps^2(m4^2+6 m4 m2^2 + 42 m2^4)/3 ]  -- wait, recheck powers
# direct source claim: <= 0.004434 eps^2 t  at eps=0.13, then /ln2 -> 0.0064
print("m2^2/2 =", m2**2 / 2, " -- hmm; source (41): eps^2 t [m2^2/2 + eps^2(m4^2+6m4m2^2+42m2^4)/3] <= 0.004434 eps^2 t")
inner = m2**2 / 2 + 0.13**2 * (m4**2 + 6 * m4 * m2**2 + 42 * m2**4) / 3
print("inner at eps=0.13 =", inner, " (<= 0.004434 ?) ; /ln2 =", inner / ln2, " (<= 0.0064 ?)")
print("0.004434/ln2 =", 0.004434 / ln2)
print("5/(48 ln2)   =", 5 / (48 * ln2), " (printed 0.1503; safe if printed >= actual)")

print()
print("=== Section 7.7 TwoCC constants (0.009307 / 0.055) ===")
# B(r) from HKZZ; try candidate forms, target int Q(B-1) on [0,1/2] = 104/3 - 50 ln2
target = 104 / 3 - 50 * ln2
print("104/3 - 50 ln2 =", target)
for name, Bm1 in [
    ("(1-2r)^2(1-2r+2r^2)/(1-r)^2", lambda r: (1 - 2 * r)**2 * (1 - 2 * r + 2 * r * r) / (1 - r)**2),
    ("(1-2r)(1-2r+2r^2)/(1-r)^2  ", lambda r: (1 - 2 * r) * (1 - 2 * r + 2 * r * r) / (1 - r)**2),
    ("(1-2r)^2(1-2r+2r^2)/(1-r)^4", lambda r: (1 - 2 * r)**2 * (1 - 2 * r + 2 * r * r) / (1 - r)**4),
]:
    v = integrate(lambda r: Q(r) * Bm1(r), 0, 0.5)
    print(f"  int Q*(B-1) with B-1 = {name} -> {v}")

print()
print("=== Prop C.12 claims at various eps ===")
def fC(r): return r * (1 - 2 * r) / (1 - r)**2
def gC(r): return (1 - 2 * r)**2 / (1 - r)**3
def s_of(r, eps): return r - delta_max(r, eps) / (1 - r)

def claimA(eps):  # r(1-2r) - 2 dmax (1-r) >= 0.95 r(1-2r)  <=>  2 dmax (1-r) <= 0.05 r(1-2r)
    worst = 1e9; wr = None
    for i in range(1, 100000):
        r = i / 200000.0
        lhs = 2 * delta_max(r, eps) * (1 - r)
        rhs = 0.05 * r * (1 - 2 * r)
        margin = rhs - lhs
        if margin < worst: worst, wr = margin, r
    return worst, wr

def claimB(eps):  # f(r) >= 0.98 f(s(r))
    worst = 1e9; wr = None
    for i in range(1, 100000):
        r = i / 200000.0
        s = s_of(r, eps)
        if s <= 0: continue
        margin = fC(r) - 0.98 * fC(min(s, 0.499999999))
        if margin < worst: worst, wr = margin, r
    return worst, wr

def claimC(eps):  # s'(r) <= 1.05 numerically
    worst = -1e9; wr = None
    h = 1e-6
    for i in range(1, 499000):
        r = i / 1000000.0
        d = (s_of(r + h, eps) - s_of(r - h, eps)) / (2 * h)
        if d > worst: worst, wr = d, r
    return worst, wr

def claimD(eps):  # g(r) >= 0.945 g(s(r))
    worst = 1e9; wr = None
    for i in range(1, 100000):
        r = i / 200000.0
        s = s_of(r, eps)
        if s <= 0: continue
        margin = gC(r) - 0.945 * gC(min(s, 0.499999999))
        if worst > margin: worst, wr = margin, r
    return worst, wr

for eps in (0.1, 0.1024756190168075228998451658, 0.11, 0.12, 0.13):
    a, ra = claimA(eps)
    b, rb = claimB(eps)
    c, rc = claimC(eps)
    d, rd = claimD(eps)
    print(f"eps={eps:.6f}: A-margin={a:+.3e}@r={ra:.4f}  B-margin={b:+.3e}@r={rb:.4f}  "
          f"max s'={c:.5f}@r={rc:.4f}  D-margin={d:+.3e}@r={rd:.4f}")

print()
print("=== Prop C.13(2): OCB*(d), MLB*(d) for d<=4 vs 1/1150 and Thr ===")
for d in range(0, 6):
    ocb = 0.88 * integrate(lambda r: fC(r) * r**d, 0, 0.5)
    mlb = 0.9 * integrate(lambda r: gC(r) * r**d, 0, 0.5)
    print(f"d={d}: OCB*={ocb:.7f}  MLB*={mlb:.7f}   1/1150={1/1150:.7f}")
print("Scheder Thr = 2/(0.9*10118) =", 2 / (0.9 * 10118))
# JC's Thr = 2A/0.9, A = (17/18) cL at eps_R
epsR = 0.1024756190168075228998451658
cL = 0.001687 * epsR - 0.006404 * epsR**2
A = 17 / 18 * cL
print("JC A =", A, " JC Thr = 2A/0.9 =", 2 * A / 0.9, "  <= 1/1150?", 2 * A / 0.9 <= 1 / 1150)

print()
print("=== C.13(1) spot check OCB* >= MLB* for d=5..30 ===")
bad = []
for d in range(5, 31):
    ocb = 0.88 * integrate(lambda r: fC(r) * r**d, 0, 0.5, 20000)
    mlb = 0.9 * integrate(lambda r: gC(r) * r**d, 0, 0.5, 20000)
    if ocb < mlb: bad.append((d, ocb, mlb))
print("violations d in 5..30:", bad if bad else "none")

print()
print("=== Lemma 75 Case 4: max gamma_ID and the 256/600 vs 64/600 issue ===")
mx = max((i / 1000000) ** 2 * (1 - 2 * i / 1000000) ** 2 for i in range(0, 500001))
print("max r^2(1-2r)^2 on [0,1/2] =", mx, " (1/64 =", 1 / 64, "; source claims <= 1/256 =", 1 / 256, ")")
print("max gamma_ID01 = 10*max =", 10 * mx)
print("corrected eps bound = (1/60)/(10/64) =", (1 / 60) / (10 / 64), " (= 64/600); printed: 256/600 =", 256 / 600)
epsI = 0.07307238160252154687451293138
print("JC epsI =", epsI, " <= 64/600?", epsI <= 64 / 600, " ; 1/5 <= 64/600?", 1 / 5 <= 64 / 600)

print()
print("=== Lemma 73's eps<=4/5 claim: r(1-2 eps r) >= 2 eps dmax, dmax=eps*gamma_ID? ===")
def gID(r): return 10 * r * r * (1 - 2 * r)**2 if r < 0.5 else 0.0
# reading 1: r(1-2 eps r) >= 2 eps * (eps*gID)   [dmax = eps gID, extra eps in front]
# reading 2: r(1-2 eps r) >= 2 * (eps*gID)       [2 dmax]
# reading 3: r(1-2r)      >= 2 * eps*gID
for name, cond in [
    ("r(1-2er)>=2e^2 gID", lambda r, e: r * (1 - 2 * e * r) - 2 * e * e * gID(r)),
    ("r(1-2er)>=2e gID  ", lambda r, e: r * (1 - 2 * e * r) - 2 * e * gID(r)),
    ("r(1-2r) >=2e gID  ", lambda r, e: r * (1 - 2 * r) - 2 * e * gID(r)),
]:
    # find max eps in (0,1] for which cond >= 0 for all r
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        ok = all(cond(i / 20000.0, mid) >= 0 for i in range(1, 10000))
        if ok: lo = mid
        else: hi = mid
    print(f"  {name}: max admissible eps ~ {lo:.4f}  (printed 4/5 = 0.8)")

print()
print("=== Section 8 Definition 68 closed forms ===")
def gpID(r): return (61 / 6) * r**3 * (1 - 2 * r)**2 if r < 0.5 else 0.0
def gTCC(r): return 20 * r**3 * (1 - 2 * r) if r < 0.5 else 0.0
h = 1e-7
def d(f):
    return lambda r: (f(r + h) - f(r - h)) / (2 * h)
phi1, phi2, phiT = d(gID), d(gpID), d(gTCC)

BFS = -integrate(lambda r: phi1(r) * Q(r), 0.0000001, 0.9999999)
DFC = integrate(lambda r: gID(r) * P(r) * (1 - Q(r)), 0, 0.5)
DFS = -integrate(lambda r: phi2(r) * Q(r), 0.0000001, 0.9999999)
J1 = -integrate(lambda r: phi1(r) * gID(r) * P(r) * (1 - Q(r)), 0.0000001, 0.5)
J2 = integrate(lambda r: phi2(r) * gID(r) * P(r) * (1 - Q(r)), 0.0000001, 0.5)
print("BFS  =", BFS, "  closed 380ln2-790/3 =", 380 * ln2 - 790 / 3, " printed >=0.06259")
print("DFC  =", DFC, "  closed 915/4-330ln2 =", 915 / 4 - 330 * ln2, " printed <=0.01144")
print("DFS  =", DFS, "  closed 1586ln2/3-52765/144 =", 1586 * ln2 / 3 - 52765 / 144, " printed <=0.0202")
print("DFB  =", DFC + DFS, " closed 596ln2/3-19825/144 =", 596 * ln2 / 3 - 19825 / 144, " printed <=0.03163")
print("JUNK1=", J1, " closed 46800ln2-227075/7 =", 46800 * ln2 - 227075 / 7, " printed <=0.00235")
print("JUNK2=", J2, " closed 8767591/192-65880ln2 =", 8767591 / 192 - 65880 * ln2, " printed <=0.000184")
print("BFS-DFB =", BFS - (DFC + DFS), "  printed >= 0.030966")
print("JUNK1+2JUNK2 =", J1 + 2 * J2, " printed <= 0.0028")

Psi10 = integrate(lambda r: phi1(r)**2, 0.0000001, 0.5)
Psi02 = integrate(lambda r: (2 * phi2(r))**2, 0.0000001, 0.5)
PsiT = integrate(lambda r: phiT(r)**2, 0.0000001, 0.5)
print("Psi_{1,0} =", Psi10, " (5/21 =", 5 / 21, ")")
print("Psi_{0,2}/2 =", Psi02 / 2, "; printed 3721/90720 =", 3721 / 90720, " -> (Psi10+Psi02/2)... wait (37) uses Psi_{A0,2}/2 as coefficient of |ID1|")
print("(Psi10 + Psi02/2/2?) check: fKL coeff of ID1 printed 0.4027 vs (5/21 + 3721/90720)/ln2 =", (5 / 21 + 3721 / 90720) / ln2)
print("Psi02/4 (=Psi01*... ) :", Psi02 / 4, " vs 3721/45360=", 3721/45360, " and 3721/90720*2=", 2*3721/90720)
print("fKL coeff of ID0 printed 0.344 vs (5/21)/ln2 =", (5 / 21) / ln2)
print("PsiTwoCC =", PsiT, " (15/14 =", 15 / 14, ")")
print("fKL(5e) coeff printed 0.06183 vs 15/(14*25*ln2) =", 15 / (14 * 25 * ln2))

print()
print("=== Section 8.3 TwoCC constants ===")
def B_HKZZ(r):
    # candidate that matched above will be reused; try the winner
    return 1 + (1 - 2 * r)**2 * (1 - 2 * r + 2 * r * r) / (1 - r)**4 if r < 0.5 else 1.0
Bonus = integrate(lambda r: Q(r) * (B_HKZZ(r) - 1), 0, 0.5)
print("Bonus2CC numeric (candidate B) =", Bonus, " closed 104/3-50ln2 =", 104 / 3 - 50 * ln2, " printed ~0.009307")
DFS2 = -integrate(lambda r: Q(r) * B_HKZZ(r) * phiT(r), 0.0000001, 0.5)
DFD2 = integrate(lambda r: 2 * r * gID(r) * B_HKZZ(r) / (1 - r)**3, 0, 0.5)
JUNK2CC = integrate(lambda r: 2 * r * gID(r) * B_HKZZ(r) * phiT(r) / (1 - r)**3, 0.0000001, 0.5)
print("DFS2CC =", DFS2, " closed 39094/3-18800ln2 =", 39094 / 3 - 18800 * ln2, " printed <=0.16634")
print("DFD2CC =", DFD2, " closed 11420ln2-23747/3 =", 11420 * ln2 - 23747 / 3, " printed <=0.074135")
print("DFS2CC+DFD2CC =", DFS2 + DFD2, " printed coeff 0.2405")
print("JUNK2CC=", JUNK2CC, " closed 17923400/7-3694000ln2 =", 17923400 / 7 - 3694000 * ln2, " printed ~0.03125 (need <= 0.03125 for safety)")

print()
print("=== 8.4 final display at eps=0.029 sanity (1380/600/617) ===")
def fKL(t): return (1 - t) * math.log(1 - t) + t if t < 1 else 1.0
e = 0.029
b1 = 0.030966 * e - 0.0028 * e * e - 0.4027 * fKL(e)
b0 = 0.06259 * e - 0.344 * fKL(e)
bT = 0.009307 - 0.2405 * e - 0.03125 * e * e - 0.06183 * fKL(5 * e)
print("b1(0.029) =", b1, " 1/1380 =", 1 / 1380)
print("b0(0.029) =", b0, " 1/600  =", 1 / 600)
print("bT(0.029) =", bT, " 1/617  =", 1 / 617)

print()
print("=== JC parameter values vs constraints ===")
print("JC eps_R =", epsR, "  > 0.1 ? ->", epsR > 0.1, "   (C.12 printed hypothesis eps<=0.1)")
print("JC eps_R <= 0.13 ?", epsR <= 0.13)
print("JC eps_I =", epsI, " <= 1/5?", epsI <= 0.2, " <= 64/600?", epsI <= 64 / 600)
# JC's A, Preg, S, b's at their fixed eps values (floats)
cT = 0.009307 - 0.055 * epsR - 0.1503 * fKL(epsR)
Thr = 2 * A / 0.9
Preg = 1.1 * epsR * Thr
Sco = cT - 5 * A
b1J = 0.030966 * epsI - 0.0028 * epsI**2 - 0.4027 * fKL(epsI)
b0J = 0.06259 * epsI - 0.344 * fKL(epsI)
bTJ = 0.009307 - 0.2405 * epsI - 0.03125 * epsI**2 - 0.06183 * fKL(5 * epsI)
print("A =", A, " (JC interval ~9.97582178549e-5)")
print("Preg =", Preg, " (JC ~2.49890303097e-5)")
print("S =", Sco, " (JC ~0.00235445147822)")
print("b1 =", b1J, " (JC ~0.00114549739595)")
print("b0 =", b0J, " (JC ~0.00363196877286)")
print("bT =", bTJ, " (JC ~-0.01318180201459)")
lam = b1J / A
gstar = lam * (A - Preg) / (1 + lam)
print("lambda =", lam, " (JC 11.4827371678)")
print("gamma* =", gstar, " (JC 0.000068779380458836)")
print("old endgame affine value at (0.1,0.029):")
cL_old = 0.001687 * 0.1 - 0.006404 * 0.01
A_old = 17 / 18 * cL_old
cT_old = 0.009307 - 0.0055 - 0.1503 * fKL(0.1)
Thr_old = 2 * A_old / 0.9
Preg_old = 0.11 * Thr_old
S_old = cT_old - 5 * A_old
b1_old = 0.030966 * 0.029 - 0.0028 * 0.029**2 - 0.4027 * fKL(0.029)
b0_old = 0.06259 * 0.029 - 0.344 * fKL(0.029)
bT_old = 0.009307 - 0.2405 * 0.029 - 0.03125 * 0.029**2 - 0.06183 * fKL(0.145)
lam_o = b1_old / A_old
print("gamma(0.1,0.029) =", lam_o * (A_old - Preg_old) / (1 + lam_o), " (JC claim 0.000065719084...)")
