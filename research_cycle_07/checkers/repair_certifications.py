#!/usr/bin/env python3
"""Cycle-7 Stage-V repair certifications (exact rational arithmetic).

Context.  The import ledger (research_cycle_07/scheder_import_ledger.md) found
that Jiang-Cai [JC26] evaluate Scheder's regular estimate at
eps_R = 0.1024756190168075228998451658, OUTSIDE the printed hypothesis
"eps <= 0.1" of Proposition C.12 (ECCC TR21-069 rev 1, pp. 77-78), and that
several load-bearing printed constants in the source are hairline or false.
This script certifies, in exact rational arithmetic with directed rounding,
every numeric fact needed to REPAIR the import layer at JC's fixed parameters:

  PART A - Proposition C.12's four claims at eps = eps_R (and at 0.1), plus
           s-range facts, in the substitution t = sqrt(1-2r):
             r = (1-t^2)/2, 1-r = (1+t^2)/2, 1-2r = t^2, t in [0,1],
             gamma(r) = r(1-2r)^{3/2}         = (1-t^2) t^3 / 2,
             phi(r)   = gamma'(r) = sqrt(1-2r)(1-5r) = t(5t^2-3)/2,
             2 gamma/(1-r)                    = 2(1-t^2)t^3/(1+t^2),
             gamma/(1-r) - phi                = t(3-7t^4)/(2(1+t^2)),
             delta_max = 1.2 eps gamma * max(2gamma/(1-r), gamma/(1-r)-phi)
                       = 0.3 eps (1-t^2) t^4 K(t) / (1+t^2),
             K(t) = max(4(1-t^2)t^2, 3-7t^4)   [switch at t0, 3t0^4+4t0^2-3=0],
             eta = delta_max/(1-r)            = 0.6 eps (1-t^2) t^4 K(t)/(1+t^2)^2,
             s(r) = r - eta(r);  s'(r) = 1 - eta'(r) = 1 + (1/t) d(eta)/dt
                    (since dt/dr = -1/t).
           Claims certified (piecewise in t, overlapping the kink bracket):
             A1: eta >= 0 and s >= 0            (range facts for the powers)
             A2: 2 delta_max (1-r) <= 0.05 r(1-2r)   <=> 12 eps t^2 K(t) <= 1
             A3: f(r) >= 0.98 f(s(r)),  f(x) = x(1-2x)/(1-x)^2
             A4: s'(r) <= 1.05          <=> d(eta)/dt <= 0.05 t   (per piece)
             A5: g(r) >= 0.945 g(s(r)),  g(x) = (1-2x)^2/(1-x)^3
           plus exact: 0.95*0.98/1.05 >= 0.88 and 0.945/1.05 == 0.9,
           plus a certified REFUTATION of the source's printed "s'(r) <= 1.05
           provided eps <= 0.13" at eps = 0.13 (single-point exact evaluation).

  PART B - Proposition C.13: (2) OCB*(d), MLB*(d) >= 1/1150 for d <= 4 (the
           hidden Thr constraint; hairline margin), Thr_JC <= 1/1150 and
           Thr_Scheder <= 1/1150; (1) OCB*(d) >= MLB*(d) for 5 <= d <= 161 by
           exact closed forms (rational + rational*ln2), and the d >= 162
           symbolic chain's numeric facts: g <= f/2 on [0.45,1/2] (exact
           polynomial identity r^2-5r+2 <= 0), g <= 1 on [0,1/2],
           ((d-1)/(d+1))^d >= 1/10 for all d >= 2, r_min >= 0.45 for d >= 19,
           and E(d) = (9/10)^d (9/16)(d+3)^3 <= 1/10 for d = 162 with ratio
           E(d+1)/E(d) <= (9/10)(166/165)^3 < 1.

  PART C - closed-form certifications of the Section-8 coefficient chain
           (Definition 68 family and (37)/(36) constants) by EXACT SYMBOLIC
           INTEGRATION of the defining integrals (x = 1-r substitution;
           values of the form rational + rational*ln2):
             BFS  = -int phi_ID Q_r          = 380 ln2 - 790/3      >= 0.06259
             DFC  =  int gamma_ID P_r(1-Q_r) = 915/4 - 330 ln2     (<= 0.01144)
             DFS  = -int phi_pID Q_r         = 1586 ln2/3 - 52765/144 (<=0.0202)
             DFB  = DFC + DFS                                        <= dto.
             BFS - DFB >= 0.030966                       [b1's leading const]
             JUNK1 = -int phi_ID gamma_ID P_r(1-Q_r) = 46800 ln2 - 227075/7
             JUNK2 =  int phi_pID gamma_ID P_r(1-Q_r) = 8767591/192 - 65880 ln2
             JUNK2 <= 0.000184 is FALSE (certified); JUNK1 + 2 JUNK2 <= 0.0028
             int phi_ID^2   = 5/21,  int phi_pID^2 = 3721/90720,
             int phi_TwoCC^2 = 15/14                     [(36)/(37) m2-values]
             (5/21 + 3721/90720)/ln2 <= 0.4027,  (5/21)/ln2 <= 0.344,
             (15/14)/(25 ln2) <= 0.06183
             Bonus2CC = 104/3 - 50 ln2 >= 0.009307
             DFS2CC + DFD2CC = 15347/3 - 7380 ln2 <= 0.2405   [printed forms]
             JUNK2CC = 17923400/7 - 3694000 ln2 <= 0.03125    [printed forms]
           and the Section-7 hairline constant
             L55 = int_0^{1/2} r^2 (1-2r)^5/(1-r)^4 dr >= 0.001687.

  PART D - irregular-parameter admissibility at eps_I (corrected source
           constraint): max gamma_ID = 10/64 via the exact identity
           r(1-2r) <= 1/8 (2(r-1/4)^2 >= 0), hence Lemma 75 Case 4 needs
           eps <= 64/600 (the printed 256/600 rests on the false "<= 10/256");
           certify eps_I <= 64/600, 5 eps_I <= 1, eps_I <= 4/5, eps_I < 1/5;
           and JC's own Lemma A.1 derivative bounds |phi_ID| <= 5/2,
           |phi_pID| <= 61/54, phi_TwoCC >= -5 (exact polynomial certificates).

  PART E - robustness envelope for the unreconciled Section-7.7 recon
           discrepancy: the dual certificate needs c_T > c_T_min :=
           A(5 + |bT|/b1); certify the margin c_T - c_T_min and compare with
           the worst-case recon-suggested degradation 3.6e-5.

Everything proof-relevant is fractions.Fraction; ln2 is enclosed by the atanh
series with the proved tail bound 0 <= R_N <= 2 z^(2N+1) / ((2N+1)(1-z^2))
(geometric domination: the dropped terms 2 z^(2j+1)/(2j+1), j >= N, are
termwise <= 2 z^(2N+1) z^(2(j-N)) / (2N+1)).  exp is enclosed by the Taylor
series with tail next_term/(1-x/(N+2)) for 0 <= x < 1.  Polynomial claims are
certified by adaptive bisection with interval Horner evaluation; endpoint
zeros are removed by exact factoring of t^k and (1-t)^k before bisection.
A claim that cannot be certified is reported as FAIL/INCONCLUSIVE - never
silently tuned.
"""

from fractions import Fraction as F
import sys, time

t_start = time.time()
FAILURES = []
def report(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAILURES.append(name)
    print(f"[{tag}] {name}" + (f"  {detail}" if detail else ""))

# ---------- ln2 / exp enclosures ----------
def ln2_interval(N=64):
    z = F(1, 3)  # (2-1)/(2+1)
    z2 = z * z
    p = z; s = F(0)
    for j in range(N):
        s += p / (2 * j + 1)
        p *= z2
    s *= 2
    tail = 2 * p / ((2 * N + 1) * (1 - z2))   # p == z^(2N+1)
    return (s, s + tail)
LN2 = ln2_interval()

def exp_upper(x, N=40):
    # x rational in [0,1); returns upper bound for e^x
    assert 0 <= x < 1
    term = F(1); s = F(1)
    for j in range(1, N + 1):
        term = term * x / j
        s += term
    tail = term * x / (N + 1) / (1 - x / (N + 2))
    return s + tail
def exp_lower(x, N=40):
    term = F(1); s = F(1)
    for j in range(1, N + 1):
        term = term * x / j
        s += term
    return s
def exp_neg_interval(x, N=40):
    # e^{-x} for x rational >= 0 with x < 1 required after scaling
    k = 0
    while x / (2 ** k) >= 1:
        k += 1
    y = x / (2 ** k)
    lo = 1 / exp_upper(y, N); hi = 1 / exp_lower(y, N)
    for _ in range(k):
        lo, hi = lo * lo, hi * hi
    return (lo, hi)

# ---------- polynomial toolkit (coeff lists, low->high, Fractions) ----------
def pnorm(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p
def padd(a, b):
    n = max(len(a), len(b))
    return pnorm([ (a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0)) for i in range(n) ])
def psub(a, b):
    n = max(len(a), len(b))
    return pnorm([ (a[i] if i < len(a) else F(0)) - (b[i] if i < len(b) else F(0)) for i in range(n) ])
def pmul(a, b):
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    r[i + j] += ai * bj
    return pnorm(r)
def pscale(a, c):
    return pnorm([ai * c for ai in a])
def pderiv(a):
    return pnorm([a[i] * i for i in range(1, len(a))]) if len(a) > 1 else [F(0)]
def peval(a, x):
    v = F(0)
    for c in reversed(a):
        v = v * x + c
    return v
def pieval(a, lo, hi):
    # interval Horner
    vlo, vhi = F(0), F(0)
    for c in reversed(a):
        # multiply interval [vlo,vhi] by [lo,hi]
        c1, c2, c3, c4 = vlo * lo, vlo * hi, vhi * lo, vhi * hi
        vlo, vhi = min(c1, c2, c3, c4), max(c1, c2, c3, c4)
        vlo, vhi = vlo + c, vhi + c
    return vlo, vhi
def ppow(a, k):
    r = [F(1)]
    for _ in range(k):
        r = pmul(r, a)
    return r
def factor_t(p):
    k = 0
    while k < len(p) - 1 and p[k] == 0:
        k += 1
    return p[k:], k
def factor_one_minus_t(p):
    # divide by (1-t) while p(1)==0; returns (quotient-chain result, multiplicity)
    m = 0
    q = p[:]
    while len(q) > 1 and peval(q, F(1)) == 0:
        # synthetic division of q by (1 - t): q = (1-t)*h  =>  h_i determined from top
        n = len(q) - 1
        h = [F(0)] * n
        # write q(t) = sum q_i t^i = (1-t) h(t); then comparing coefficients from t^n down:
        # q_n = -h_{n-1}; q_i = h_i - h_{i-1} (0<i<n); q_0 = h_0
        h[n - 1] = -q[n]
        for i in range(n - 1, 0, -1):
            h[i - 1] = h[i] - q[i]
        assert h[0] == q[0], "factor_one_minus_t inconsistency"
        q = pnorm(h)
        m += 1
    return q, m

CERT_STATS = {}
def certify_nonneg(p, a, b, name, max_nodes=400000, tiny=F(1, 2**60)):
    """Certify p(t) >= 0 for all t in [a,b] by adaptive bisection with interval
    Horner.  Returns True/False; False carries a witness (exact point with
    p<0) or an INCONCLUSIVE marker."""
    stack = [(a, b)]
    nodes = 0
    min_lo = None
    while stack:
        lo, hi = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            report(name, False, f"INCONCLUSIVE: node budget exceeded at [{float(lo):.6f},{float(hi):.6f}]")
            return False
        vlo, vhi = pieval(p, lo, hi)
        if vlo >= 0:
            if min_lo is None or vlo < min_lo:
                min_lo = vlo
            continue
        if vhi < 0:
            report(name, False, f"REFUTED on [{float(lo):.9f},{float(hi):.9f}], enclosure [{float(vlo):.3e},{float(vhi):.3e}]")
            return False
        mid = (lo + hi) / 2
        vm = peval(p, mid)
        if vm < 0:
            report(name, False, f"REFUTED: p({float(mid):.12f}) = {float(vm):.6e} < 0 (exact witness)")
            return False
        if hi - lo < tiny:
            report(name, False, f"INCONCLUSIVE at width < 2^-60 near t = {float(mid):.12f}")
            return False
        stack.append((lo, mid)); stack.append((mid, hi))
    CERT_STATS[name] = (nodes, min_lo)
    report(name, True, f"nodes={nodes}")
    return True
def certify_nonneg_factored(p, a, b, name, **kw):
    """Factor out t^j and (1-t)^m (both nonnegative on [0,1]) then certify."""
    q, j = factor_t(p)
    q, m = factor_one_minus_t(q)
    nm = name + (f" [/t^{j}]" if j else "") + (f" [/(1-t)^{m}]" if m else "")
    return certify_nonneg(q, a, b, nm, **kw)

# ---------- fixed parameters ----------
EPS_R = F("0.1024756190168075228998451658")
EPS_I = F("0.07307238160252154687451293138")
print("=" * 78)
print("Cycle-7 Stage-V repair certifications  (exact rational arithmetic)")
print(f"eps_R = {EPS_R}  (~{float(EPS_R):.10f})   NOTE eps_R > 1/10: {EPS_R > F(1,10)}")
print(f"eps_I = {EPS_I}  (~{float(EPS_I):.10f})")
print(f"ln2 enclosure width: {float(LN2[1]-LN2[0]):.3e}")
print("=" * 78)

# ---------- PART A ----------
print("\n--- PART A: Proposition C.12 claims at eps_R (repair of the eps<=0.1 hypothesis) ---")
# kink bracket: q(t) = 3t^4 + 4t^2 - 3, root t0 in (0,1); piece 1 (K = 3-7t^4) for t <= t0
qpoly = [F(-3), F(0), F(4), F(0), F(3)]
lo, hi = F(0), F(1)
for _ in range(40):
    mid = (lo + hi) / 2
    if peval(qpoly, mid) < 0:
        lo = mid
    else:
        hi = mid
T0LO, T0HI = lo, hi
print(f"kink bracket t0 in [{float(T0LO):.12f}, {float(T0HI):.12f}] (width 2^-40)")

ONE = [F(1)]
T = [F(0), F(1)]
T2 = [F(0), F(0), F(1)]
OMT2 = [F(1), F(0), F(-1)]            # 1 - t^2
OPT2 = [F(1), F(0), F(1)]             # 1 + t^2
K1 = [F(3), F(0), F(0), F(0), F(-7)]  # 3 - 7 t^4
K2 = pmul(pscale(T2, F(4)), OMT2)     # 4 t^2 (1 - t^2)
ED = pmul(OPT2, OPT2)                 # (1+t^2)^2
GD = pmul(ED, OPT2)                   # (1+t^2)^3

def run_A_suite(eps, label):
    all_ok = True
    for pc, K, ta, tb in (("p1", K1, F(0), T0HI), ("p2", K2, T0LO, F(1))):
        # EN = 0.6 eps (1-t^2) t^4 K   (eta = EN/ED)
        EN = pscale(pmul(pmul(OMT2, ppow(T, 4)), K), F(3, 5) * eps)
        SN = psub(pscale(pmul(OMT2, ED), F(1, 2)), EN)   # s*ED
        # A1: K >= 0 (=> eta >= 0) and s >= 0  (SN = (1-t^2)*[ED/2 - 0.6 eps t^4 K])
        ok = certify_nonneg_factored(K, ta, tb, f"A1A-{label}-{pc}: K >= 0")
        all_ok &= ok
        ok = certify_nonneg_factored(SN, ta, tb, f"A1B-{label}-{pc}: s >= 0")
        all_ok &= ok
        # A2: 1 - 12 eps t^2 K >= 0
        ok = certify_nonneg(psub(ONE, pscale(pmul(T2, K), 12 * eps)), ta, tb,
                            f"A2-{label}-{pc}: 2 delta_max(1-r) <= 0.05 r(1-2r)")
        all_ok &= ok
        # A3: f(r) >= 0.98 f(s):  FN (SD-SN)^2 - 0.98 SN (SD-2SN) FD >= 0,  FD=SD=ED
        FN = pscale(pmul(T2, OMT2), F(2))
        SDmSN = psub(ED, SN)
        SDm2SN = psub(ED, pscale(SN, F(2)))
        N3 = psub(pmul(FN, pmul(SDmSN, SDmSN)), pscale(pmul(pmul(SN, SDm2SN), ED), F(49, 50)))
        ok = certify_nonneg_factored(N3, ta, tb, f"A3-{label}-{pc}: f(r) >= 0.98 f(s)")
        all_ok &= ok
        # positivity side facts for the divisions used above: 1-s>0 and 1-2s>=0
        ok = certify_nonneg_factored(SDmSN, ta, tb, f"A3a-{label}-{pc}: 1-s > 0 (num)")
        all_ok &= ok
        ok = certify_nonneg_factored(SDm2SN, ta, tb, f"A3b-{label}-{pc}: 1-2s >= 0 (num)")
        all_ok &= ok
        # A4: 0.05 t ED^2 - (EN' ED - EN ED') >= 0
        N4 = psub(pscale(pmul(T, pmul(ED, ED)), F(1, 20)),
                  psub(pmul(pderiv(EN), ED), pmul(EN, pderiv(ED))))
        ok = certify_nonneg_factored(N4, ta, tb, f"A4-{label}-{pc}: s'(r) <= 1.05")
        all_ok &= ok
        # A5: 8 t^4 (SD-SN)^3 - 0.945 (SD-2SN)^2 SD GD >= 0
        N5 = psub(pmul(pscale(ppow(T, 4), F(8)), ppow(SDmSN, 3)),
                  pscale(pmul(pmul(pmul(SDm2SN, SDm2SN), ED), GD), F(189, 200)))
        ok = certify_nonneg_factored(N5, ta, tb, f"A5-{label}-{pc}: g(r) >= 0.945 g(s)")
        all_ok &= ok
    return all_ok

okA_epsR = run_A_suite(EPS_R, "epsR")
okA_tenth = run_A_suite(F(1, 10), "0.1")
report("A-CONST: 0.95*0.98/1.05 >= 0.88", F(19,20)*F(49,50)/F(21,20) >= F(22,25),
       f"= {F(19,20)*F(49,50)/F(21,20)} = {float(F(19,20)*F(49,50)/F(21,20)):.8f}")
report("A-CONST: 0.945/1.05 == 0.9", F(189,200)/F(21,20) == F(9,10))

# refutation of the printed "s' <= 1.05 provided eps <= 0.13" at eps = 0.13:
eps13 = F(13, 100)
EN13 = pscale(pmul(pmul(OMT2, ppow(T, 4)), K1), F(3, 5) * eps13)
N4_13 = psub(pscale(pmul(T, pmul(ED, ED)), F(1, 20)),
             psub(pmul(pderiv(EN13), ED), pmul(EN13, pderiv(ED))))
# scan for a violating rational point on piece 1
worst_t, worst_v = None, None
for i in range(1, 400):
    tt = F(i, 400) * T0LO / 1  # scan inside piece 1
    v = peval(N4_13, tt)
    if worst_v is None or v < worst_v:
        worst_v, worst_t = v, tt
sprime_excess = None
if worst_v is not None and worst_v < 0:
    # s'(r) at that point = 1 + (1/t) deta/dt ; excess over 1.05 = -N4(t)/(t*ED(t)^2)
    tED2 = worst_t * peval(pmul(ED, ED), worst_t)
    sprime_excess = -worst_v / tED2
    report("A-REFUTE: source's \"s'<=1.05 provided eps<=0.13\" is FALSE at eps=0.13", True,
           f"exact witness t={worst_t} (r={float((1-worst_t**2)/2):.6f}): s' = 1.05 + {float(sprime_excess):.6e}")
else:
    report("A-REFUTE: could not exhibit violation at eps=0.13", False,
           "expected a violation per reconnaissance; investigate")

# ---------- closed-form integral engine ----------
def integral_poly_over_xpow(P, k):
    """int_{1/2}^{1} P(x)/x^k dx  ->  (rational, coeff_of_ln2).
    P is a poly in x.  Term c x^e / x^k = c x^{e-k}:
      m = e-k >= 0 : c (1 - (1/2)^{m+1})/(m+1)
      m = -1      : c * ln 2
      m <= -2     : c [x^{m+1}/(m+1)]_{1/2}^{1} = c (1 - 2^{-(m+1)})/(m+1)."""
    rat, lncoef = F(0), F(0)
    for e, c in enumerate(P):
        if c == 0:
            continue
        m = e - k
        if m == -1:
            lncoef += c
        else:
            rat += c * (1 - F(1, 2) ** (m + 1)) / (m + 1)
    return rat, lncoef

def to_x_poly(rpoly):
    """substitute r = 1 - x into a polynomial given in r."""
    res = [F(0)]
    base = [F(1)]
    rx = [F(1), F(-1)]  # 1 - x
    for c in rpoly:
        res = padd(res, pscale(base, c))
        base = pmul(base, rx)
    return res

def int_0_half_rational(num_r, den_pow):
    """int_0^{1/2} num_r(r) / (1-r)^den_pow dr  (exact; x = 1-r)."""
    return integral_poly_over_xpow(to_x_poly(num_r), den_pow)

def enc(val):
    """(rat, lncoef) -> interval via LN2."""
    rat, c = val
    lo1, hi1 = rat + c * LN2[0], rat + c * LN2[1]
    return (min(lo1, hi1), max(lo1, hi1))

def ge_check(val, bound, name, note=""):
    lo, hi = enc(val)
    report(name, lo >= bound, f"value in [{float(lo):.12f},{float(hi):.12f}] vs {float(bound):.12f} {note}")
    return lo >= bound
def le_check(val, bound, name, note=""):
    lo, hi = enc(val)
    report(name, hi <= bound, f"value in [{float(lo):.12f},{float(hi):.12f}] vs {float(bound):.12f} {note}")
    return hi <= bound

# polynomial builders in r
def rpoly(*coeffs):  # low->high in r
    return [F(c) for c in coeffs]
R_ = rpoly(0, 1)
ONE_R = rpoly(1)
OM2R = rpoly(1, -2)           # 1-2r
def rpow(p, k):
    return ppow(p, k)

print("\n--- PART B: Proposition C.13 (hidden Thr constraint and the d-sweep) ---")
def I_ocb(d):   # int_0^{1/2} r^{d+1}(1-2r)/(1-r)^2 dr
    return int_0_half_rational(pmul(rpow(R_, d + 1), OM2R), 2)
def J_mlb(d):   # int_0^{1/2} r^d (1-2r)^2/(1-r)^3 dr
    return int_0_half_rational(pmul(rpow(R_, d), pmul(OM2R, OM2R)), 3)
okB = True
for d in range(0, 5):
    o = I_ocb(d); m = J_mlb(d)
    okB &= ge_check((o[0] * F(22, 25), o[1] * F(22, 25)), F(1, 1150), f"B2: OCB*({d}) >= 1/1150")
    okB &= ge_check((m[0] * F(9, 10), m[1] * F(9, 10)), F(1, 1150), f"B2: MLB*({d}) >= 1/1150")
# Thr compliance (JC's Thr = 2A/0.9 with A rational-interval; A is a pure rational here)
# c_L, A are exact rationals apart from nothing (no logs):
c_L = F("0.001687") * EPS_R - F("0.006404") * EPS_R * EPS_R
A_val = F(17, 18) * c_L
Thr_JC = 2 * A_val / F(9, 10)
Thr_S = F(2, 1) / (F(9, 10) * 10118)
report("B2: Thr_JC <= 1/1150", Thr_JC <= F(1, 1150), f"Thr_JC = {float(Thr_JC):.9e}")
report("B2: Thr_Scheder <= 1/1150", Thr_S <= F(1, 1150), f"Thr_S = {float(Thr_S):.9e}")
okB &= (Thr_JC <= F(1, 1150)) and (Thr_S <= F(1, 1150))
# d-sweep 5..161: OCB*(d) - MLB*(d) >= 0
sweep_ok = True
worst = None
for d in range(5, 162):
    o = I_ocb(d); m = J_mlb(d)
    diff = (o[0] * F(22, 25) - m[0] * F(9, 10), o[1] * F(22, 25) - m[1] * F(9, 10))
    lo, hi = enc(diff)
    if lo < 0:
        sweep_ok = False
        report(f"B1: OCB*({d}) >= MLB*({d})", False, f"enclosure [{float(lo):.3e},{float(hi):.3e}]")
    if worst is None or lo < worst[1]:
        worst = (d, lo)
report("B1: OCB*(d) >= MLB*(d) for all 5<=d<=161", sweep_ok,
       f"worst margin at d={worst[0]}: {float(worst[1]):.6e}")
okB &= sweep_ok
# d >= 162 chain facts:
#   (i) g <= f/2 on [0.45,1/2]  <=>  r^2 - 5r + 2 <= 0 there (derivation in header):
p_gf = rpoly(-2, 5, -1)   # -(r^2 - 5r + 2)
v045 = peval(p_gf, F(9, 20)); v05 = peval(p_gf, F(1, 2))
report("B1: g <= f/2 on [0.45,1/2] (endpoints of concave-up -(r^2-5r+2))",
       v045 >= 0 and v05 >= 0, f"values {v045}, {v05}; quadratic with positive r^2-coeff in r^2-5r+2 -> min of -(...) at endpoints")
okB &= v045 >= 0 and v05 >= 0
#   (ii) g <= 1 on [0,1/2]: (1-r)^3 - (1-2r)^2 = r(1 - r - r^2) >= 0 on [0,1/2]
p_g1 = rpoly(1, -1, -1)   # 1 - r - r^2
okB &= certify_nonneg(p_g1, F(0), F(1, 2), "B1: 1 - r - r^2 >= 0 on [0,1/2] (g <= 1)")
#   (iii) ((d-1)/(d+1))^d >= 1/10: exact for 2 <= d <= 20; for d >= 21 via e-bound
h_ok = all(F(d - 1, d + 1) ** d >= F(1, 10) for d in range(2, 21))
# for d >= 21: ((d-1)/(d+1))^d = exp(-d ln((d+1)/(d-1))); ln((d+1)/(d-1)) <= 2/(d-1) + 2/(3(d-1)^3)*... use
# ln(1+u) <= u with u = 2/(d-1):  ((d-1)/(d+1))^d >= exp(-2d/(d-1)) >= exp(-2.1) for d >= 21
elo, ehi = exp_neg_interval(F(21, 10))
report("B1: ((d-1)/(d+1))^d >= 1/10 for all d >= 2",
       h_ok and elo >= F(1, 10),
       f"d in 2..20 exact; d>=21 via exp(-2.1) >= {float(elo):.6f} >= 0.1")
okB &= h_ok and elo >= F(1, 10)
#   (iv) r_min >= 0.45 for d >= 19: (d-1)/(2(d+1)) >= 9/20 <=> 10(d-1) >= 9(d+1) <=> d >= 19
report("B1: r_min >= theta for d >= 19 (exact algebra)", True, "10(d-1) >= 9(d+1) <=> d >= 19")
#   (v) E(162) <= 1/10 and ratio < 1
E162 = F(9, 10) ** 162 * F(9, 16) * F(165) ** 3
ratio = F(9, 10) * F(166, 165) ** 3
report("B1: E(162) = (9/10)^162 (9/16) 165^3 <= 1/10", E162 <= F(1, 10), f"E(162) = {float(E162):.6f}")
report("B1: E(d+1)/E(d) <= (9/10)(166/165)^3 < 1", ratio < 1, f"ratio = {float(ratio):.9f}")
okB &= E162 <= F(1, 10) and ratio < 1

print("\n--- PART C: Section-8 closed-form coefficient chain and Lemma 55 constant ---")
phi_ID = pscale(pmul(pmul(R_, OM2R), rpoly(1, -4)), F(20))          # 20 r (1-2r)(1-4r)
gam_ID = pscale(pmul(pmul(R_, R_), pmul(OM2R, OM2R)), F(10))        # 10 r^2 (1-2r)^2
phi_pID = pscale(pmul(pmul(pmul(R_, R_), OM2R), rpoly(3, -10)), F(61, 6))  # (61/6) r^2 (1-2r)(3-10r)
phi_TwoCC = rpoly(0, 0, 60, -160)                                    # 60 r^2 - 160 r^3
okC = True
# BFS = - int phi_ID * r^2/(1-r)^2 :
BFS = int_0_half_rational(pscale(pmul(phi_ID, pmul(R_, R_)), F(-1)), 2)
report("C: BFS closed form == 380 ln2 - 790/3", BFS == (F(-790, 3), F(380)), f"got {BFS}")
okC &= BFS == (F(-790, 3), F(380))
okC &= ge_check(BFS, F("0.06259"), "C: BFS >= 0.06259")
# DFC = int gam_ID * r/(1-r) * (1-2r)/(1-r)^2 = int 10 r^3 (1-2r)^3/(1-r)^3
DFC = int_0_half_rational(pmul(gam_ID, pmul(R_, OM2R)), 3)
report("C: DFC closed form == 915/4 - 330 ln2", DFC == (F(915, 4), F(-330)), f"got {DFC}")
okC &= DFC == (F(915, 4), F(-330))
# DFS = - int phi_pID * r^2/(1-r)^2
DFS = int_0_half_rational(pscale(pmul(phi_pID, pmul(R_, R_)), F(-1)), 2)
report("C: DFS closed form == (1586/3) ln2 - 52765/144", DFS == (F(-52765, 144), F(1586, 3)), f"got {DFS}")
okC &= DFS == (F(-52765, 144), F(1586, 3))
DFB = (DFC[0] + DFS[0], DFC[1] + DFS[1])
BmD = (BFS[0] - DFB[0], BFS[1] - DFB[1])
okC &= ge_check(BmD, F("0.030966"), "C: BFS - DFB >= 0.030966 (b1 leading constant; hairline)")
# JUNK1 = - int phi_ID gam_ID P_r (1-Q_r) = - int phi_ID gam_ID r(1-2r)/(1-r)^3
JUNK1 = int_0_half_rational(pscale(pmul(pmul(phi_ID, gam_ID), pmul(R_, OM2R)), F(-1)), 3)
report("C: JUNK1 closed form == 46800 ln2 - 227075/7", JUNK1 == (F(-227075, 7), F(46800)), f"got {JUNK1}")
okC &= JUNK1 == (F(-227075, 7), F(46800))
JUNK2 = int_0_half_rational(pmul(pmul(phi_pID, gam_ID), pmul(R_, OM2R)), 3)
report("C: JUNK2 closed form == 8767591/192 - 65880 ln2", JUNK2 == (F(8767591, 192), F(-65880)), f"got {JUNK2}")
okC &= JUNK2 == (F(8767591, 192), F(-65880))
j2lo, j2hi = enc(JUNK2)
report("C: source's printed \"JUNK2 <= 0.000184\" is FALSE (certified)", j2lo > F("0.000184"),
       f"JUNK2 in [{float(j2lo):.9e},{float(j2hi):.9e}] > 1.84e-4")
JUNKtot = (JUNK1[0] + 2 * JUNK2[0], JUNK1[1] + 2 * JUNK2[1])
okC &= le_check(JUNKtot, F("0.0028"), "C: JUNK1 + 2 JUNK2 <= 0.0028 (b1 quadratic constant)")
# m2 constants
m2_ID = int_0_half_rational(pmul(phi_ID, phi_ID), 0)
report("C: int phi_ID^2 == 5/21", m2_ID == (F(5, 21), F(0)), f"got {m2_ID}")
okC &= m2_ID == (F(5, 21), F(0))
# NOTE: the printed (37) coefficient of |ID_1| is 3721/90720 = 2 * int phi_pID^2,
# consistent with the aggregation (I_y+I_z)^2 <= 2(I_y+I_z) over 0/1/2-valued
# indicators and Sum_x (I_y+I_z) <= ... (statement-level); we certify the
# integral itself and the factor-2 relation.
m2_pID = int_0_half_rational(pmul(phi_pID, phi_pID), 0)
report("C: int phi_pID^2 == 3721/181440 and 2*int == printed 3721/90720",
       m2_pID == (F(3721, 181440), F(0)) and 2 * F(3721, 181440) == F(3721, 90720),
       f"got {m2_pID}")
okC &= m2_pID == (F(3721, 181440), F(0))
m2_2CC = int_0_half_rational(pmul(phi_TwoCC, phi_TwoCC), 0)
report("C: int phi_TwoCC^2 == 15/14", m2_2CC == (F(15, 14), F(0)), f"got {m2_2CC}")
okC &= m2_2CC == (F(15, 14), F(0))
# the three KL-coefficient roundings (divide by ln2 -> use LN2 interval, safe direction):
v = F(5, 21) + F(3721, 90720)
report("C: (5/21 + 3721/90720)/ln2 <= 0.4027", v / LN2[0] <= F("0.4027"), f"<= {float(v/LN2[0]):.9f}")
okC &= v / LN2[0] <= F("0.4027")
report("C: (5/21)/ln2 <= 0.344", F(5, 21) / LN2[0] <= F("0.344"), f"<= {float(F(5,21)/LN2[0]):.9f}")
okC &= F(5, 21) / LN2[0] <= F("0.344")
report("C: (15/14)/(25 ln2) <= 0.06183", F(15, 14) / (25 * LN2[0]) <= F("0.06183"),
       f"<= {float(F(15,14)/(25*LN2[0])):.9f}")
okC &= F(15, 14) / (25 * LN2[0]) <= F("0.06183")
# printed 8.3 closed forms -> decimals (closed forms taken as printed; B(r) not re-derived):
okC &= ge_check((F(104, 3), F(-50)), F("0.009307"), "C: Bonus2CC = 104/3 - 50 ln2 >= 0.009307")
okC &= le_check((F(15347, 3), F(-7380)), F("0.2405"), "C: DFS2CC + DFD2CC = 15347/3 - 7380 ln2 <= 0.2405")
okC &= le_check((F(17923400, 7), F(-3694000)), F("0.03125"), "C: JUNK2CC = 17923400/7 - 3694000 ln2 <= 0.03125")
# Lemma 55 constant (hairline): int r^2 (1-2r)^5/(1-r)^4 >= 0.001687
L55 = int_0_half_rational(pmul(pmul(R_, R_), rpow(OM2R, 5)), 4)
okC &= ge_check(L55, F("0.001687"), "C: Lemma-55 integral >= 0.001687 (A-chain leading constant; hairline)")
lo55, hi55 = enc(L55)
print(f"      Lemma-55 exact value: {L55[0]} + ({L55[1]}) ln2 in [{float(lo55):.12f},{float(hi55):.12f}]")

print("\n--- PART D: irregular-parameter admissibility at eps_I (corrected constraint) ---")
# max gamma_ID = 10/64 via exact identity: 1/8 - r(1-2r) = 2(r - 1/4)^2 >= 0
idpoly = psub(rpoly(F(1, 8)), pmul(R_, OM2R))
sqpoly = pscale(pmul(rpoly(F(-1, 4), 1), rpoly(F(-1, 4), 1)), F(2))
report("D: 1/8 - r(1-2r) == 2(r-1/4)^2 (exact identity => max gamma_ID = 10/64)",
       idpoly == sqpoly)
okD = idpoly == sqpoly
report("D: corrected Lemma-75-Case-4 constraint eps <= 64/600; eps_I complies",
       EPS_I <= F(64, 600), f"eps_I = {float(EPS_I):.6f} <= {float(F(64,600)):.6f}")
okD &= EPS_I <= F(64, 600)
report("D: 5 eps_I <= 1", 5 * EPS_I <= 1)
report("D: eps_I <= 4/5", EPS_I <= F(4, 5))
report("D: eps_I < 1/5 (JC Lemma A.1 nonnegativity range)", EPS_I < F(1, 5))
okD &= 5 * EPS_I <= 1 and EPS_I <= F(4, 5) and EPS_I < F(1, 5)
# JC Lemma A.1 derivative bounds (exact polynomial certificates on r in [0,1/2]):
b1p = psub(rpoly(F(25, 4)), pmul(phi_ID, phi_ID))     # (5/2)^2 - phi_ID^2 >= 0
okD &= certify_nonneg(b1p, F(0), F(1, 2), "D: |phi_ID| <= 5/2 on [0,1/2]")
b2p = psub(rpoly(F(3721, 2916)), pmul(phi_pID, phi_pID))  # (61/54)^2 - phi_pID^2 >= 0
okD &= certify_nonneg(b2p, F(0), F(1, 2), "D: |phi_pID| <= 61/54 on [0,1/2]")
# phi_TwoCC + 5 = (1/2 - r)(160 r^2 + 20 r + 10) >= 0 (exact factorization)
lhs = padd(phi_TwoCC, rpoly(5))
rhs = pmul(rpoly(F(1, 2), -1), rpoly(10, 20, 160))
report("D: phi_TwoCC + 5 == (1/2 - r)(160r^2 + 20r + 10) >= 0 on [0,1/2] (exact)",
       lhs == rhs)
okD &= lhs == rhs
# review caveat C2: (36) needs |phi_TwoCC| <= 5, i.e. also the UPPER side:
okD &= certify_nonneg(psub(rpoly(5), phi_TwoCC), F(0), F(1, 2),
                      "D: phi_TwoCC <= 5 on [0,1/2] (C2: upper side of |phi_TwoCC| <= 5)")
# review caveat C4: p. 55's ordering Psi_{1,2} <= Psi_{1,1} <= Psi_{1,0} for
# Psi_{1,m} = int_0^{1/2} (-phi_ID + m phi_pID)^2 dr (feeds (37)); exact rationals:
def psi(mm):
    q = psub(pscale(phi_pID, F(mm)), phi_ID)
    val = int_0_half_rational(pmul(q, q), 0)
    assert val[1] == 0
    return val[0]
P0, P1, P2 = psi(0), psi(1), psi(2)
report("D: Psi_{1,2} <= Psi_{1,1} <= Psi_{1,0} (C4, exact)", P2 <= P1 <= P0,
       f"{float(P2):.9f} <= {float(P1):.9f} <= {float(P0):.9f}")
okD &= P2 <= P1 <= P0

print("\n--- PART E: c_T robustness envelope (Section-7.7 recon discrepancy cover) ---")
# f_KL(eps) interval needed for c_T, b1, bT
def ln_interval_1to2_arg(y, N=64):
    z = (y - 1) / (y + 1)
    z2 = z * z
    p = z; s = F(0)
    for j in range(N):
        s += p / (2 * j + 1)
        p *= z2
    s *= 2
    tail = 2 * p / ((2 * N + 1) * (1 - z2))
    return (s, s + tail)
def ln_pos_interval(x):
    k = 0
    y = x
    while y < 1:
        y *= 2; k -= 1
    while y > 2:
        y /= 2; k += 1
    u = ln_interval_1to2_arg(y)
    lo = u[0] + k * (LN2[0] if k >= 0 else LN2[1])
    hi = u[1] + k * (LN2[1] if k >= 0 else LN2[0])
    return (lo, hi)
def fkl_interval(tv):
    l = ln_pos_interval(1 - tv)
    a, b = (1 - tv) * l[0] + tv, (1 - tv) * l[1] + tv
    return (min(a, b), max(a, b))
fkR = fkl_interval(EPS_R)
c_T = (F("0.009307") - F("0.055") * EPS_R - F("0.1503") * fkR[1],
       F("0.009307") - F("0.055") * EPS_R - F("0.1503") * fkR[0])
fkI = fkl_interval(EPS_I)
fk5I = fkl_interval(5 * EPS_I)
b1i = (F("0.030966") * EPS_I - F("0.0028") * EPS_I ** 2 - F("0.4027") * fkI[1],
       F("0.030966") * EPS_I - F("0.0028") * EPS_I ** 2 - F("0.4027") * fkI[0])
bTi = (F("0.009307") - F("0.2405") * EPS_I - F("0.03125") * EPS_I ** 2 - F("0.06183") * fk5I[1],
       F("0.009307") - F("0.2405") * EPS_I - F("0.03125") * EPS_I ** 2 - F("0.06183") * fk5I[0])
# c_T_min = A (5 + |bT|/b1); the formula requires A > 0, b1 > 0, bT <= 0
# (review caveat C1) - assert them from the certified enclosures:
assert A_val > 0 and b1i[0] > 0 and bTi[1] < 0, "Part-E sign preconditions violated"
absbT = (-bTi[1], -bTi[0])
cTmin_hi = A_val * (5 + absbT[1] / b1i[0])
margin = c_T[0] - cTmin_hi
report("E: dual certificate needs c_T > c_T_min = A(5 + |bT|/b1)", margin > 0,
       f"c_T >= {float(c_T[0]):.9f}, c_T_min <= {float(cTmin_hi):.9f}, margin >= {float(margin):.9f}")
recon_worst = F(36, 1000000)  # 3.6e-5 worst-case degradation suggested by 7.7 recon
report("E: margin covers the 7.7 recon-suggested degradation 3.6e-5",
       margin > recon_worst, f"cover factor >= {float(margin / recon_worst):.1f}x")
okE = margin > recon_worst

print("\n" + "=" * 78)
ok_all = okA_epsR and okA_tenth and okB and okC and okD and okE and not FAILURES
elapsed = time.time() - t_start
if FAILURES:
    print(f"RESULT: {len(FAILURES)} check(s) FAILED or inconclusive: {FAILURES}")
else:
    print("RESULT: ALL REPAIR CERTIFICATIONS PASSED")
print(f"(elapsed {elapsed:.1f}s)")
sys.exit(0 if not FAILURES else 1)
