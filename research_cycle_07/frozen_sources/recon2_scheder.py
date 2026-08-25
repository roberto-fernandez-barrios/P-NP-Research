# NON-CERTIFYING RECONNAISSANCE part 2
import math
ln2 = math.log(2.0)

def integrate(f, a, b, n=200000):
    if n % 2: n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += f(x) * (4 if i % 2 else 2)
    return s * h / 3

def Q(r): return (r / (1 - r))**2 if r < 0.5 else 1.0
def B(r): return 1 + (1 - 2*r)**2 * (1 - 2*r + 2*r*r) / (1 - r)**2 if r < 0.5 else 1.0

# --- Section 7.7 TwoCC (gammaA = 40 r^{7/2} (1-2r)^2) ---
def gA7(r): return 40 * r**3.5 * (1 - 2*r)**2 if r < 0.5 else 0.0
h = 1e-7
def der(f): return lambda r: (f(r + h) - f(r - h)) / (2 * h)
phiA7 = der(gA7)
def gam(r): return r * (1 - 2*r)**1.5 if r < 0.5 else 0.0
def phi(r): return math.sqrt(1-2*r)*(1-5*r) if r < 0.5 else 0.0
def gtilde(r): return 2.4 * gam(r)**2 / (1 - r) if r < 0.5 else 0.0  # per eps

DFS7 = -integrate(lambda r: Q(r) * B(r) * phiA7(r), 1e-7, 0.5 - 1e-9)
DFD7 = integrate(lambda r: 2 * r * gtilde(r) * B(r) / (1 - r)**3, 0, 0.5)
JUNK7 = integrate(lambda r: 2 * r * gtilde(r) * B(r) * phiA7(r) / (1 - r)**3, 1e-7, 0.5 - 1e-9)
print("S7.7: DFS2CC =", DFS7, "(printed <=0.0455)   DFD2CC =", DFD7, "(printed <=0.0095)   JUNK2CC =", JUNK7, "(printed <= -0.019)")
print("      DFS+DFD =", DFS7 + DFD7, "(printed 0.055)")

# --- Section 8.3 with correct B ---
def gID(r): return 10*r*r*(1-2*r)**2 if r < 0.5 else 0.0
def gTCC(r): return 20*r**3*(1-2*r) if r < 0.5 else 0.0
phiT = der(gTCC)
Bon = integrate(lambda r: Q(r)*(B(r)-1), 0, 0.5)
DFS8 = -integrate(lambda r: Q(r)*B(r)*phiT(r), 1e-7, 0.5 - 1e-9)
DFD8 = integrate(lambda r: 2*r*gID(r)*B(r)/(1-r)**3, 0, 0.5)
JUNK8 = integrate(lambda r: 2*r*gID(r)*B(r)*phiT(r)/(1-r)**3, 1e-7, 0.5 - 1e-9)
print("S8.3: Bonus2CC =", Bon, "(closed 104/3-50ln2 =", 104/3 - 50*ln2, ")")
print("      DFS2CC =", DFS8, "(closed", 39094/3 - 18800*ln2, ", printed <=0.16634)")
print("      DFD2CC =", DFD8, "(closed", 11420*ln2 - 23747/3, ", printed <=0.074135)")
print("      sum    =", DFS8 + DFD8, "(printed coeff 0.2405 in 8.4)")
print("      JUNK2CC=", JUNK8, "(closed", 17923400/7 - 3694000*ln2, ", printed ~0.03125; 8.4 uses 0.03125)")

# --- Corollary 50 'furthermore': 1 - Q_{r-dmax} <= 1.02 (1-Qr) ---
def delta_max(r, eps):
    if r >= 0.5: return 0.0
    return 1.2 * eps * gam(r) * max(2*gam(r)/(1-r), gam(r)/(1-r) - phi(r))
for eps in (0.1, 0.1024756190168075, 0.11, 0.12, 0.13):
    worst = -1e9; wr = None
    for i in range(1, 100000):
        r = i / 200000.0
        s = max(r - delta_max(r, eps), 0.0)
        lhs = 1 - Q(s)
        rhs = 1.02 * (1 - Q(r))
        if lhs - rhs > worst: worst, wr = lhs - rhs, r
    print(f"Cor50 1.02-claim eps={eps:.6f}: max(LHS-RHS) = {worst:+.3e} at r={wr:.4f}  (OK if <= 0)")

# --- Prop 51 (TwoCC cleanup S7): printed hypothesis eps<=0.13; condition (44) unknown, skip ---

# --- JC's H-lower bridge: trivially |J1 cap TwoCC| + 2|J0 cap TwoCC| <= 2|TwoCC| : combinatorial, skip ---

# --- Lemma 43 at 5eps: requires |phi|<=1 for gTCC/5' ---
mphi = max(abs(phiT(i/200000)) for i in range(1, 100000))
print("max |phi_TwoCC| =", mphi, "(source: 5 at r=1/2);  |phi/5| <= 1 ?", mphi/5 <= 1 + 1e-9)

# --- 0.9*10118*Thr >= 2 check for JC's Thr ---
epsR = 0.1024756190168075228998451658
cL = 0.001687*epsR - 0.006404*epsR**2
A = 17/18*cL
ThrJC = 2*A/0.9
print("JC Thr =", ThrJC, " vs 1/1150 =", 1/1150, " OK:", ThrJC <= 1/1150)
print("JC Thr vs 1/4553 :", 1/4553, " (Scheder's; JC's exceeds Scheder's:", ThrJC > 1/4553, ")")

# --- density nonnegativity per JC Lemma A.1 at eps=1/5 (spot check) ---
phi1 = der(gID); phi2 = der(lambda r: (61/6)*r**3*(1-2*r)**2 if r < 0.5 else 0.0)
worst = 1e9; combo_worst = None
for a in (0,1):
    for m in (0,1,2):
        for i in range(1, 100000):
            r = i/200000.0
            v = 1 + 0.2*(-a*phi1(r) + m*phi2(r))
            if v < worst: worst, combo_worst = v, (a, m, r)
for i in range(1, 100000):
    r = i/200000.0
    v = 1 + 0.2*phiT(r)
    if v < worst: worst, combo_worst = v, ('TwoCC', r)
print("min density 1+eps*gamma'_v at eps=1/5:", worst, "at", combo_worst, " (>=0 ?)")

# --- JC's phi bounds in Lemma A.1: |phi_ID|<=5/2, |phi_pID|<=61/54, phi_TwoCC>=-5 ---
m1 = max(abs(phi1(i/200000)) for i in range(1,100000))
m2_ = max(abs(phi2(i/200000)) for i in range(1,100000))
mn = min(phiT(i/200000) for i in range(1,100000))
print("max|phi_ID| =", m1, "(5/2 =", 2.5, ")   max|phi_pID| =", m2_, "(61/54 =", 61/54, ")   min phi_TwoCC =", mn, "(-5)")
