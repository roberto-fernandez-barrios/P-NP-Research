#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
independent_checker.py
======================

INDEPENDENT exact-rational certificate checker (arms-length replication) for

    Tao Jiang, Shaowei Cai,
    "A Better Analysis For PPSZ For 3-SAT", arXiv:2607.10697v1.

Written from scratch for a hostile validation audit (2026-08-25).

INDEPENDENCE STATEMENT
----------------------
The only inputs consulted are:
  1) frozen paper source:
       research_cycle_07/frozen_sources/arxiv_src/a_better_analysis_for_ppsz_3_.tex
     (all formulas below were transcribed from that file by hand; tex line
      numbers are cited in comments), and
  2) frozen certificate data:
       research_cycle_07/frozen_sources/ppsz_certificate.json  (pure data).
The authors' checker (verify_ppsz_constants.py) and its transcript
(verification_output.txt) were NOT read, opened, grepped, or accessed in any
way.  All algorithmic choices here (series depths, rounding scheme, tail
bounds, check structure) are our own.

EXACTNESS POLICY
----------------
* Every proof-relevant number is a fractions.Fraction.  No float ever enters
  any load-bearing computation; the Iv constructor and the JSON loader reject
  floats.  Decimal output is produced by exact integer arithmetic only.
* Every transcendental value (ln, exp, 2^x, log2) is enclosed in a PROVED
  rational interval [lo, hi] with lo <= true value <= hi.
* After each transcendental enclosure (and after selected products) endpoints
  are rounded OUTWARD to denominator 2^256:
      lo -> floor(lo * 2^256) / 2^256   (moves down or stays)
      hi -> ceil (hi * 2^256) / 2^256   (moves up or stays)
  Outward rounding replaces an interval by a superset, so every enclosure
  remains a true enclosure (soundness preserved); it merely widens the
  interval by < 2 * 2^-256 ~ 1.7e-77.  limit_denominator and float rounding
  are never used.
* Deterministic: fixed series depths, no search, no randomness, no clock.

SELF-DERIVED TRUNCATION-ERROR BOUNDS
------------------------------------
(1) Logarithm (atanh series).  For a rational y with 1 <= y <= 2 put
        z = (y-1)/(y+1)  in  [0, 1/3].
    Then (1+z)/(1-z) = y, hence
        ln y = ln((1+z)/(1-z)) = 2*atanh(z) = 2 * SUM_{j>=0} z^(2j+1)/(2j+1).
    Let S_N = 2 * SUM_{j=0}^{N-1} z^(2j+1)/(2j+1) and R_N = ln y - S_N.
    Every omitted term is >= 0, so R_N >= 0.  For j >= N,
        z^(2j+1)/(2j+1) <= z^(2j+1)/(2N+1)
                         = (z^(2N+1)/(2N+1)) * (z^2)^(j-N),
    and summing the geometric series SUM_{k>=0} (z^2)^k = 1/(1-z^2)  (z^2<1):
        0 <= R_N <= 2*z^(2N+1) / ((2N+1)*(1-z^2)).
    Therefore  ln y in [S_N, S_N + 2*z^(2N+1)/((2N+1)*(1-z^2))].   [proved]
    General argument x > 0: exact powers of two give x = m*2^k with
    m in [1,2), k in Z (invariant ln x = ln m + k*ln 2 is maintained by each
    exact halving/doubling), so ln x in [S_N(m), S_N(m)+tail] + k*[ln2 encl].
    ln 2 itself is the case y = 2, z = 1/3.
    Interval argument [a,b], 0 < a <= b: ln is increasing, so
    ln([a,b]) subset [lnlo(a), lnhi(b)].

(2) Exponential (Taylor series).  For rational x with 0 <= x < N+1,
        exp x = SUM_{j>=0} x^j/j!,   S_N = SUM_{j=0}^{N-1} x^j/j!,
        R_N = exp x - S_N = SUM_{j>=N} x^j/j! >= 0.
    For j >= N,
        x^j/j! = (x^N/N!) * x^(j-N) / ((N+1)(N+2)...j)
              <= (x^N/N!) * (x/(N+1))^(j-N),
    since each factor N+1,...,j is >= N+1.  Summing the geometric series
    (ratio x/(N+1) < 1):
        0 <= R_N <= (x^N/N!) / (1 - x/(N+1)).
    Therefore  exp x in [S_N, S_N + (x^N/N!)/(1 - x/(N+1))].       [proved]
    Negative arguments: exp x = 1/exp(-x); if exp(-x) in [c,d], 0 < c <= d,
    then exp x in [1/d, 1/c] (outward reciprocal).
    Interval argument: exp is increasing; use the endpoint rule.

(3) Derived functions (paper, tex lines 210-213, 331-349, 279-285, 516-519):
        f_KL(t)  = (1-t)*ln(1-t) + t                       (NATURAL log)
        h2(d)    = -d*log2(d) - (1-d)*log2(1-d)            (BINARY log)
        log2 x   = ln x / ln 2          (outward interval division)
        2^t      = exp(t * ln 2)
        p0 = 2 ln 2 - 1;  p* = 1 - 1/(2 ln 2);  q0 = p0 - p*.

SERIES DEPTHS (our own choice, independent of the authors' N=90):
    LN_TERMS  = 120:  tail <= 2*(1/3)^241/(241*(8/9)) < 10^-115  (z <= 1/3)
    EXP_TERMS = 100:  for |x| <= 1, tail <= (1/100!)/(1-1/101) < 10^-157
    so the 2^-256 outward rounding (~8.6e-78) dominates every width.
"""

import json
import sys
from fractions import Fraction as Fr

# ----------------------------------------------------------------------
# Part A -- exact rational utilities and outward rounding
# ----------------------------------------------------------------------

LN_TERMS = 120          # atanh-series depth for ln   (see derivation (1))
EXP_TERMS = 100         # Taylor depth for exp        (see derivation (2))
ROUND_BITS = 256        # outward endpoint rounding to denominator 2^256
DEN = 1 << ROUND_BITS
TEN = Fr(10)

FORBIDDEN_TYPES = (float, complex)


def Q(s):
    """Exact rational from a decimal string, 'p/q' string, int, or Fraction.
    Floats are rejected (exactness policy)."""
    if isinstance(s, Fr):
        return s
    if isinstance(s, int):
        return Fr(s)
    if isinstance(s, str):
        return Fr(s.strip())
    raise TypeError("refusing inexact numeric type: %r" % (s,))


def rdown(q):
    """Largest multiple of 2^-256 that is <= q (exact; Python // floors)."""
    return Fr(q.numerator * DEN // q.denominator, DEN)


def rup(q):
    """Smallest multiple of 2^-256 that is >= q."""
    n = q.numerator * DEN
    d = q.denominator
    return Fr(-((-n) // d), DEN)


# ----------------------------------------------------------------------
# Part B -- interval arithmetic on exact rationals
# ----------------------------------------------------------------------

class Iv(object):
    """Closed interval [lo, hi] with exact Fraction endpoints.

    Soundness: for x in [a,b], y in [c,d] the implemented endpoint formulas
    give supersets of {x op y} (standard interval arithmetic; division
    requires 0 outside the divisor).  All endpoint arithmetic is exact, so
    no rounding is needed for soundness; .rounded() only ever WIDENS."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        if isinstance(lo, FORBIDDEN_TYPES) or isinstance(hi, FORBIDDEN_TYPES):
            raise TypeError("float endpoint rejected")
        lo = Q(lo)
        hi = lo if hi is None else Q(hi)
        if lo > hi:
            raise ValueError("empty interval")
        self.lo = lo
        self.hi = hi

    # -- coercion ------------------------------------------------------
    @staticmethod
    def make(x):
        if isinstance(x, Iv):
            return x
        return Iv(Q(x))

    # -- arithmetic ----------------------------------------------------
    def __add__(self, o):
        o = Iv.make(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __sub__(self, o):
        o = Iv.make(o)
        return Iv(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return Iv.make(o).__sub__(self)

    def __mul__(self, o):
        o = Iv.make(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(ps), max(ps))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Iv.make(o)
        if not (o.lo > 0 or o.hi < 0):
            raise ZeroDivisionError("divisor interval contains 0")
        qs = (self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi)
        return Iv(min(qs), max(qs))

    def __rtruediv__(self, o):
        return Iv.make(o).__truediv__(self)

    # -- rounding / predicates ----------------------------------------
    def rounded(self):
        """Outward rounding to denominator 2^256 -- returns a SUPERSET."""
        return Iv(rdown(self.lo), rup(self.hi))

    def width(self):
        return self.hi - self.lo

    def contains(self, x):
        x = Q(x)
        return self.lo <= x <= self.hi

    def inside(self, o):
        o = Iv.make(o)
        return o.lo <= self.lo and self.hi <= o.hi

    def intersects(self, o):
        o = Iv.make(o)
        return self.lo <= o.hi and o.lo <= self.hi


def cert_gt(a, b):
    """Certified strict a > b (every point of a exceeds every point of b)."""
    a, b = Iv.make(a), Iv.make(b)
    return a.lo > b.hi


def cert_lt(a, b):
    a, b = Iv.make(a), Iv.make(b)
    return a.hi < b.lo


# ----------------------------------------------------------------------
# Part C -- exact decimal printing (integer arithmetic only; display layer)
# ----------------------------------------------------------------------

def _exp10_floor(aq):
    """e with 10^e <= aq < 10^(e+1) for exact aq > 0."""
    n, d = aq.numerator, aq.denominator
    e = len(str(n)) - len(str(d))
    while TEN ** e > aq:
        e -= 1
    while TEN ** (e + 1) <= aq:
        e += 1
    return e


def dec_str(q, sig=30, dirn=0):
    """Exact decimal string of Fraction q with sig significant digits.
    dirn=-1: round toward -inf (lower endpoints), +1: toward +inf (upper
    endpoints), 0: nearest (point display).  Pure integer arithmetic."""
    q = Q(q)
    if q == 0:
        return "0"
    aq = -q if q < 0 else q
    e = _exp10_floor(aq)
    scaled = q * TEN ** (sig - 1 - e)
    n, d = scaled.numerator, scaled.denominator
    if dirn < 0:
        m = n // d
    elif dirn > 0:
        m = -((-n) // d)
    else:
        m = (2 * n + d) // (2 * d)
    neg = m < 0
    s = str(-m if neg else m)
    if len(s) == sig + 1:          # rounding crossed a power of ten
        e += 1
        s = s[:sig]
    assert len(s) == sig
    return ("-" if neg else "") + s[0] + "." + s[1:] + "e" + ("%+03d" % e)


def agree_note(iv):
    w = iv.width()
    if w == 0:
        return "exact rational (width 0)"
    if iv.lo <= 0 <= iv.hi:
        b = max(abs(iv.lo), abs(iv.hi))
        return "contains 0; |value| <= " + dec_str(b, 3, +1)
    m = min(abs(iv.lo), abs(iv.hi))
    rel = w / m
    e = _exp10_floor(rel)
    return "relative width < 1e%+03d (endpoints agree to >= %d sig. digits)" \
        % (e + 1, max(0, -(e + 1)))


def fmt_iv(iv, sig=30):
    if iv.width() == 0:
        return "= %s  [%s]" % (dec_str(iv.lo, sig, 0), agree_note(iv))
    return "[%s, %s]  width <= %s  (%s)" % (
        dec_str(iv.lo, sig, -1), dec_str(iv.hi, sig, +1),
        dec_str(rup(iv.width()), 3, +1), agree_note(iv))


# ----------------------------------------------------------------------
# Part D -- proved transcendental enclosures
# ----------------------------------------------------------------------

def atanh_encl(z, N):
    """Enclosure of 2*atanh(z) = ln((1+z)/(1-z)) for exact 0 <= z <= 1/3.
    Tail bound: 0 <= R_N <= 2*z^(2N+1)/((2N+1)*(1-z^2)).  Derivation (1)."""
    z = Q(z)
    assert 0 <= z <= Fr(1, 3)
    z2 = z * z
    s = Fr(0)
    p = z                         # invariant: p = z^(2j+1) at loop head
    for j in range(N):
        s += p / (2 * j + 1)
        p *= z2
    # now p = z^(2N+1)
    s2 = 2 * s
    tail = 2 * p / ((2 * N + 1) * (1 - z2))
    return Iv(s2, s2 + tail).rounded()


LN2 = atanh_encl(Fr(1, 3), LN_TERMS)          # ln 2 (case y=2, z=1/3)


def ln_rat(x):
    """Enclosure of ln x for exact rational x > 0.
    Range reduction by exact powers of two: invariant ln(x) = ln(r) + k*ln2
    is maintained by r/=2,k+=1 and r*=2,k-=1; ends with r in [1,2)."""
    r = Q(x)
    assert r > 0
    k = 0
    while r >= 2:
        r /= 2
        k += 1
    while r < 1:
        r *= 2
        k -= 1
    z = (r - 1) / (r + 1)         # in [0, 1/3)
    base = atanh_encl(z, LN_TERMS)
    return (base + Iv(Fr(k)) * LN2).rounded()


def ln_iv(x):
    """Enclosure of ln over an interval (ln is strictly increasing)."""
    x = Iv.make(x)
    assert x.lo > 0
    if x.lo == x.hi:
        return ln_rat(x.lo)
    return Iv(ln_rat(x.lo).lo, ln_rat(x.hi).hi)


def _exp_nonneg(r, N):
    """Enclosure of exp r for exact rational 0 <= r < N+1.
    Tail bound: 0 <= R_N <= (r^N/N!)/(1 - r/(N+1)).  Derivation (2)."""
    r = Q(r)
    assert 0 <= r < N + 1
    s = Fr(0)
    t = Fr(1)                     # invariant: t = r^j/j! at loop head
    for j in range(N):
        s += t
        t = t * r / (j + 1)
    # now t = r^N/N!
    ratio = 1 - r / (N + 1)
    assert ratio > 0
    tail = t / ratio
    return Iv(s, s + tail)


def exp_rat(r):
    """Enclosure of exp r for any exact rational r."""
    r = Q(r)
    if r >= 0:
        return _exp_nonneg(r, EXP_TERMS).rounded()
    e = _exp_nonneg(-r, EXP_TERMS)
    assert e.lo > 0
    return Iv(1 / e.hi, 1 / e.lo).rounded()   # exp r = 1/exp(-r), outward

def exp_iv(x):
    """Enclosure of exp over an interval (exp is strictly increasing)."""
    x = Iv.make(x)
    if x.lo == x.hi:
        return exp_rat(x.lo)
    return Iv(exp_rat(x.lo).lo, exp_rat(x.hi).hi)


def log2_iv(x):
    """log2 x = ln x / ln 2 with outward interval division."""
    return (ln_iv(x) / LN2).rounded()


def pow2_iv(t):
    """2^t = exp(t * ln 2)."""
    t = Iv.make(t)
    return exp_iv((t * LN2).rounded()).rounded()


def f_KL(t):
    """f_KL(t) = (1-t)*ln(1-t) + t, natural log (tex lines 210-213)."""
    t = Q(t)
    assert 0 < t < 1
    return ((1 - t) * ln_rat(1 - t) + t).rounded()


def h2_rat(d):
    """Binary entropy h2(d) = -d*log2(d) - (1-d)*log2(1-d), 0<d<1
    (tex lines 516-519)."""
    d = Q(d)
    assert 0 < d < 1
    l2d = (ln_rat(d) / LN2).rounded()
    l2md = (ln_rat(1 - d) / LN2).rounded()
    return (-(d * l2d) - (1 - d) * l2md).rounded()


# Shared constants of the paper (tex lines 54-61, 508-514)
P0 = (2 * LN2 - 1).rounded()                  # p0 = 2 ln 2 - 1
PSTAR = (1 - 1 / (2 * LN2)).rounded()         # p* = 1 - 1/(2 ln 2)
Q0 = (P0 - PSTAR).rounded()                   # q0 = p0 - p*


# ----------------------------------------------------------------------
# Part E -- plumbing self-tests (guards against implementation bugs).
# These use only textbook constants/identities, not any paper artifact.
# ----------------------------------------------------------------------

def _selftest():
    ok = True

    def within(iv, ref, tol):
        ref, tol = Q(ref), Q(tol)
        return Iv(ref - tol, ref + tol).intersects(iv) and \
            iv.inside(Iv(ref - tol, ref + tol))

    # 30-digit textbook references (accurate to ~1e-30; tolerance 1e-26)
    ok &= within(LN2, "0.693147180559945309417232121458", "1e-26")
    ok &= within(exp_rat(1), "2.71828182845904523536028747135", "1e-26")
    ok &= within(ln_rat(10), "2.30258509299404568401799145468", "1e-26")
    ok &= within(pow2_iv(Iv(Fr(1, 2))), "1.41421356237309504880168872421",
                 "1e-26")
    # exact identities (enclosure must contain the exact value)
    ok &= (ln_rat(3) + ln_rat(5)).intersects(ln_rat(15))
    ok &= h2_rat(Fr(1, 2)).contains(1)                    # h2(1/2) = 1
    ok &= (exp_rat(-1) * exp_rat(1)).contains(1)          # e^-1 * e = 1
    sq = pow2_iv(Iv(Fr(1, 2)))
    ok &= (sq * sq).contains(2)                           # (2^(1/2))^2 = 2
    ok &= exp_rat(0).contains(1) and ln_rat(1).contains(0)
    # widths must be tiny
    for iv in (LN2, P0, PSTAR, Q0):
        ok &= iv.width() < Fr(1, 10 ** 70)
    if not ok:
        print("SELF-TEST FAILURE: implementation bug -- aborting.")
        sys.exit(2)
    print("Plumbing self-tests passed (ln2, e, ln10, sqrt2, h2(1/2)=1, "
          "exact identities; all widths < 1e-70).")


# ----------------------------------------------------------------------
# Part F -- check bookkeeping
# ----------------------------------------------------------------------

RESULTS = []


def record(cid, desc, ok, lines=()):
    RESULTS.append((cid, bool(ok), desc))
    print("[%s] %-4s %s" % ("PASS" if ok else "FAIL", cid, desc))
    for ln in lines:
        print("            " + ln)


def flag(msg):
    print("[FLAG]      " + msg)


def ref_ulp(ref_str):
    """One unit in the last printed place of a decimal reference string."""
    s = ref_str.strip().lower()
    if "e" in s:
        mant, ex = s.split("e")
        exp = int(ex)
    else:
        mant, exp = s, 0
    decs = len(mant.split(".")[1]) if "." in mant else 0
    return TEN ** (exp - decs)


def refcheck(cid, name, iv, ref_str):
    """Consistency with a printed paper value: our enclosure must intersect
    [ref - ulp, ref + ulp] (covers truncation or rounding of the print)."""
    ref = Q(ref_str)
    u = ref_ulp(ref_str)
    ok = iv.intersects(Iv(ref - u, ref + u))
    record(cid, "paper cross-ref %s ~ %s" % (name, ref_str), ok,
           ["ours: " + fmt_iv(iv)])
    return ok


# ----------------------------------------------------------------------
# Part G -- load frozen inputs
# ----------------------------------------------------------------------

JSON_PATH = (r"C:\Users\masteria.DOMINE\rf\P-NP-Research\research_cycle_07"
             r"\frozen_sources\ppsz_certificate.json")


def _no_float(_s):
    raise ValueError("unquoted decimal in JSON would become a float: " + _s)


with open(JSON_PATH, "r", encoding="ascii") as fh:
    CERT = json.load(fh, parse_float=_no_float)

# ---- values transcribed BY HAND from the frozen tex (line numbers cited) --
PAPER = {
    "version": "2026-07-12-rational-v6",                       # tex line 720
    "epsilon_R": "0.1024756190168075228998451658",             # tex line 419
    "epsilon_I": "0.07307238160252154687451293138",            # tex line 421
    "gamma_new": "0.0000687793",                               # tex line 113
    "gamma_old_den": 15218,                                    # tex line 81
    "gamma_old_decimal": "0.000065711657247995",               # tex line 82
    "endgame": (10118, 41391, 1380),                           # tex lines 65-67
    "coeff_intervals": {                                       # tex 425-435
        "A":     ("0.0000997582178549", "0.0000997582178550"),
        "P_reg": ("0.0000249890303097", "0.0000249890303098"),
        "S":     ("0.00235445147822", "0.00235445147823"),
        "b1":    ("0.00114549739595", "0.00114549739597"),
        "b0":    ("0.00363196877285", "0.00363196877287"),
        "bT":    ("-0.01318180201459", "-0.01318180201458"),
    },
    "lambda_prefix": "11.4827371678",                          # tex line 440
    "gamma_star_prefix": "0.000068779380458836",               # tex line 458
    "tight_i1_prefix": "0.060043244708778326",                 # tex line 463
    "q0_prefix": "0.107641881564372",                          # tex line 513
    "delta_old_bracket": ("0.00000321978491531273261",
                          "0.00000321978491531273262"),        # tex 587-589
    "delta_new_bracket": ("0.00000338183369577144614",
                          "0.00000338183369577144615"),        # tex 592-593
    "eta_old_interval": ("0.0000003465837065",
                         "0.0000003465837066"),                # tex 598-600
    "eta_new_interval": ("0.0000003640269421",
                         "0.0000003640269422"),                # tex 603-605
    "unique_base_upper": "1.306969598",                        # tex line 500
    "old_general_base_upper": "1.307031593710",                # tex line 611
    "new_general_base_upper": "1.307031577907",                # tex line 613
    "safe_general_base_upper": "1.307031578",                  # tex line 630
    "delta0": "0.00000338183369",                              # tex line 624
    "eta_safe": "0.000000364",                                 # tex line 619
    # Appendix B margin table, tex lines 744-759:
    "m_AmP": "0.00007476918754521059",
    "m_b0m2b1": "0.00134097398093794778",
    "m_bTlS": "0.01385374548423064739",
    "m_gstar_gap": "8.045883656550355e-11",
    "m_gnew_gold": "0.0000030676427520042",
    "m_eta_gap": "0.0000000174432356",
    "m_high_branch": "2.6941529384e-11",
    "m_unique_residual": "2.7050581864e-11",
    "m_unique_base": "1.306969597516246",
    "m_old_general_base": "1.307031593709762",
    "m_new_general_base": "1.307031577906796",
    "m_safe_base": "1.307031577931205",
    "old_unique_base_unrounded": "1.306972376565153",          # tex line 84
    "scheder_params_value": "0.000065719084",                  # tex line 702
    "pow2_p0_prefix": "1.3070319",                             # tex line 61
}

print("=" * 76)
print("INDEPENDENT EXACT-RATIONAL CERTIFICATE CHECKER (arms-length replication)")
print("paper : Jiang-Cai, 'A Better Analysis For PPSZ For 3-SAT'"
      " (arXiv:2607.10697v1)")
print("inputs: frozen tex source + ppsz_certificate.json ONLY")
print("policy: fractions.Fraction everywhere; proved series tails;"
      " outward 2^-256 rounding")
print("depths: LN_TERMS=%d, EXP_TERMS=%d (own choice; authors used 90/90)"
      % (LN_TERMS, EXP_TERMS))
print("=" * 76)
print()
_selftest()
print()

# ----------------------------------------------------------------------
# Part H -- provenance flags (Section 0)
# ----------------------------------------------------------------------

print("-" * 76)
print("SECTION 0: provenance and data integrity")
print("-" * 76)
print("JSON version string : %r" % CERT["version"])
print("Paper Appendix B    : 'The certificate version is "
      "\\texttt{2026-07-12-rational-v6}.' (tex line 720)")
if CERT["version"] != PAPER["version"]:
    flag("VERSION MISMATCH: JSON says %r but the paper's Appendix B says %r."
         % (CERT["version"], PAPER["version"]))
    flag("Documented as a provenance discrepancy in the report; it is not an"
         " arithmetic failure.")
else:
    print("Version strings agree.")
flag("Audit brief refers to the parameter display as 'eq. (13)'; in the"
     " frozen v1 source \\label{eq:parameter-values} is the 20th numbered"
     " display (eq. (13) is \\label{eq:Rlinear}).  Checked against"
     " \\label{eq:parameter-values} regardless.")
flag("JSON-only thresholds (not printed in the tex): old_unique_base_upper="
     "1.306972376566, relative_improvement_lower=0.0503,"
     " unique_relative_improvement_lower=0.04668.")
print("JSON series depths: log_terms=%r exp_terms=%r (paper Appendix B:"
      " 'uses N=90 for both series' -- consistent)."
      % (CERT["series"]["log_terms"], CERT["series"]["exp_terms"]))
print()

# ----------------------------------------------------------------------
# CHECK 1 -- parameters parse exactly; JSON == paper eq:parameter-values
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 1: fixed parameters epsilon_R, epsilon_I (exact rationals)")
print("-" * 76)

eR = Q(CERT["unique"]["epsilon_R"])
eI = Q(CERT["unique"]["epsilon_I"])

record("01a", "epsilon_R: JSON == paper eq:parameter-values",
       eR == Q(PAPER["epsilon_R"]),
       ["value = %s = %s" % (CERT["unique"]["epsilon_R"], eR)])
record("01b", "epsilon_I: JSON == paper eq:parameter-values",
       eI == Q(PAPER["epsilon_I"]),
       ["value = %s = %s" % (CERT["unique"]["epsilon_I"], eI)])
record("01c", "source-side admissibility ranges: eps_R <= 0.13 and"
       " eps_I <= 1/5 (tex lines 243, 265)",
       eR <= Q("0.13") and eI <= Fr(1, 5))
gamma_new = Q(CERT["lifting"]["gamma_new"])
record("01d", "gamma_new: JSON lifting == JSON unique.gamma_reported =="
       " paper 0.0000687793",
       gamma_new == Q(CERT["unique"]["gamma_reported"]) ==
       Q(PAPER["gamma_new"]))

# full JSON <-> paper literal concordance
conc = [
    ("unique.unique_base_upper", CERT["unique"]["unique_base_upper"],
     PAPER["unique_base_upper"]),
    ("lifting.gamma_old", CERT["lifting"]["gamma_old"], "1/15218"),
    ("lifting.delta_old_lower", CERT["lifting"]["delta_old_lower"],
     PAPER["delta_old_bracket"][0]),
    ("lifting.delta_old_upper", CERT["lifting"]["delta_old_upper"],
     PAPER["delta_old_bracket"][1]),
    ("lifting.delta_new_lower", CERT["lifting"]["delta_new_lower"],
     PAPER["delta_new_bracket"][0]),
    ("lifting.delta_new_upper", CERT["lifting"]["delta_new_upper"],
     PAPER["delta_new_bracket"][1]),
    ("lifting.delta_safe", CERT["lifting"]["delta_safe"], PAPER["delta0"]),
    ("lifting.eta_safe", CERT["lifting"]["eta_safe"], PAPER["eta_safe"]),
    ("lifting.old_base_upper", CERT["lifting"]["old_base_upper"],
     PAPER["old_general_base_upper"]),
    ("lifting.new_limiting_base_upper",
     CERT["lifting"]["new_limiting_base_upper"],
     PAPER["new_general_base_upper"]),
    ("lifting.safe_general_base_upper",
     CERT["lifting"]["safe_general_base_upper"],
     PAPER["safe_general_base_upper"]),
]
for k in ("A", "P_reg", "S", "b1", "b0", "bT"):
    conc.append(("reported_intervals.%s_lower" % k,
                 CERT["reported_intervals"]["%s_lower" % k],
                 PAPER["coeff_intervals"][k][0]))
    conc.append(("reported_intervals.%s_upper" % k,
                 CERT["reported_intervals"]["%s_upper" % k],
                 PAPER["coeff_intervals"][k][1]))
conc.append(("reported_intervals.lambda_lower",
             CERT["reported_intervals"]["lambda_lower"],
             PAPER["lambda_prefix"]))
conc.append(("reported_intervals.gamma_star_lower",
             CERT["reported_intervals"]["gamma_star_lower"],
             PAPER["gamma_star_prefix"]))
conc.append(("reported_intervals.tight_i1_lower",
             CERT["reported_intervals"]["tight_i1_lower"],
             PAPER["tight_i1_prefix"]))
bad = [name for (name, a, b) in conc if Q(a) != Q(b)]
record("01e", "JSON <-> paper literal concordance"
       " (%d shared constants compared as exact rationals)" % len(conc),
       not bad, ["all equal" if not bad else "MISMATCHES: %s" % bad])
print()

# ----------------------------------------------------------------------
# CHECK 2 -- regular-side coefficients (tex lines 326-349)
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 2: regular-side coefficients c_L, c_T, A, Thr, P_reg, S")
print("-" * 76)

cL = Q("0.001687") * eR - Q("0.006404") * eR * eR       # exact rational
fKL_R = f_KL(eR)
cT = (Q("0.009307") - Q("0.055") * eR - Q("0.1503") * fKL_R).rounded()
A_ = Fr(17, 18) * cL                                     # exact
IA = Iv(A_)
Thr_ = 2 * A_ / Q("0.9")                                 # exact
Preg_ = Q("1.1") * eR * Thr_                             # exact
IPreg = Iv(Preg_)
S_ = (cT - 5 * A_).rounded()

record("02a", "c_L = 0.001687 eR - 0.006404 eR^2 (exact)", True,
       ["c_L   " + fmt_iv(Iv(cL))])
record("02b", "c_T = 0.009307 - 0.055 eR - 0.1503 f_KL(eR)", True,
       ["f_KL(eR) " + fmt_iv(fKL_R), "c_T   " + fmt_iv(cT)])
record("02c", "A = (17/18) c_L ; Thr = 2A/0.9 ; P_reg = 1.1 eR Thr (exact)",
       True, ["A     " + fmt_iv(IA), "Thr   " + fmt_iv(Iv(Thr_)),
              "P_reg " + fmt_iv(IPreg)])
record("02d", "S = c_T - 5A", True, ["S     " + fmt_iv(S_)])
print()

# ----------------------------------------------------------------------
# CHECK 3 -- irregular-side coefficients (tex lines 278-286)
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 3: irregular-side coefficients b1, b0, bT")
print("-" * 76)

fKL_I = f_KL(eI)
fKL_5I = f_KL(5 * eI)
b1 = (Q("0.030966") * eI - Q("0.0028") * eI * eI
      - Q("0.4027") * fKL_I).rounded()
b0 = (Q("0.06259") * eI - Q("0.344") * fKL_I).rounded()
bT = (Q("0.009307") - Q("0.2405") * eI - Q("0.03125") * eI * eI
      - Q("0.06183") * fKL_5I).rounded()

record("03a", "b1 = 0.030966 eI - 0.0028 eI^2 - 0.4027 f_KL(eI)", True,
       ["f_KL(eI)  " + fmt_iv(fKL_I), "b1    " + fmt_iv(b1)])
record("03b", "b0 = 0.06259 eI - 0.344 f_KL(eI)", True,
       ["b0    " + fmt_iv(b0)])
record("03c", "bT = 0.009307 - 0.2405 eI - 0.03125 eI^2 - 0.06183 f_KL(5 eI)",
       True, ["f_KL(5eI) " + fmt_iv(fKL_5I), "bT    " + fmt_iv(bT)])
print()

# ----------------------------------------------------------------------
# CHECK 4 -- sign pattern and A - P_reg
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 4: sign pattern A>0, P_reg>0, A>P_reg, S>0, b0>0, b1>0, bT<0")
print("-" * 76)

AmP = A_ - Preg_                                         # exact rational
record("04a", "A > 0", A_ > 0)
record("04b", "P_reg > 0", Preg_ > 0)
record("04c", "A > P_reg (exact rational comparison)", AmP > 0,
       ["A - P_reg " + fmt_iv(Iv(AmP))])
record("04d", "S > 0", S_.lo > 0,
       ["margin S.lo = " + dec_str(S_.lo, 21, -1)])
record("04e", "b0 > 0", b0.lo > 0,
       ["margin b0.lo = " + dec_str(b0.lo, 21, -1)])
record("04f", "b1 > 0", b1.lo > 0,
       ["margin b1.lo = " + dec_str(b1.lo, 21, -1)])
record("04g", "bT < 0", bT.hi < 0,
       ["margin bT.hi = " + dec_str(bT.hi, 21, +1)])
refcheck("04h", "A - P_reg", Iv(AmP), PAPER["m_AmP"])
print()

# ----------------------------------------------------------------------
# CHECK 5 -- dual margins
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 5: dual margins b0 - 2 b1 > 0 and A bT + b1 S > 0")
print("-" * 76)

b0m2b1 = (b0 - 2 * b1).rounded()
prod_form = (IA * bT + b1 * S_).rounded()       # A bT + b1 S  (no division)
lam = (b1 / IA).rounded()                       # lambda = b1/A
div_form = (bT + lam * S_).rounded()            # bT + (b1/A) S

record("05a", "b0 - 2 b1 > 0", b0m2b1.lo > 0,
       ["b0 - 2 b1 " + fmt_iv(b0m2b1)])
refcheck("05b", "b0 - 2 b1", b0m2b1, PAPER["m_b0m2b1"])
record("05c", "A bT + b1 S > 0 (product form, no division)",
       prod_form.lo > 0, ["A bT + b1 S " + fmt_iv(prod_form)])
record("05d", "equivalent division form bT + (b1/A) S > 0 (A > 0)",
       div_form.lo > 0, ["bT + (b1/A) S " + fmt_iv(div_form),
                         "lambda = b1/A " + fmt_iv(lam)])
refcheck("05e", "bT + lambda S", div_form, PAPER["m_bTlS"])
refcheck("05f", "lambda", lam, PAPER["lambda_prefix"])
print()

# ----------------------------------------------------------------------
# CHECK 6 -- gamma_star vs gamma_new
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 6: gamma_star = b1 (A - P_reg)/(A + b1) exceeds gamma_new")
print("-" * 76)

gstar = (b1 * Iv(AmP) / (IA + b1)).rounded()
ggap = (gstar - gamma_new).rounded()

record("06a", "gamma_star > gamma_new = 0.0000687793", gstar.lo > gamma_new,
       ["gamma_star " + fmt_iv(gstar),
        "gamma_star - gamma_new " + fmt_iv(ggap)])
refcheck("06b", "gamma_star", gstar, PAPER["gamma_star_prefix"])
refcheck("06c", "gamma_star - gamma_new", ggap, PAPER["m_gstar_gap"])
print()

# ----------------------------------------------------------------------
# CHECK 7 -- corner (tight point) check
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 7: corner i1 = (A-P_reg)/(A+b1), i0 = tau = 0")
print("-" * 76)
# Symbolic identity (derived independently; also in the report):
#   L_irr = b1*i1 = b1 (A-P_reg)/(A+b1) = gamma_star            (definition)
#   L_reg = A(1 - i1) - P_reg = (A-P_reg) - A (A-P_reg)/(A+b1)
#         = (A-P_reg) (1 - A/(A+b1)) = (A-P_reg) b1/(A+b1) = gamma_star.
# Numerically we certify that independent interval evaluations of
# L_reg - gamma_star and L_irr - gamma_star both contain 0 with tiny width.

i1 = (Iv(AmP) / (IA + b1)).rounded()
Lreg = (IA * (1 - i1) - Preg_).rounded()
Lirr = (b1 * i1).rounded()
dreg = (Lreg - gstar).rounded()
dirr = (Lirr - gstar).rounded()
TINY = Fr(1, 10 ** 40)

record("07a", "0 < i1 < 1 (strict; also gives i0+i1+tau = i1 < 1)",
       i1.lo > 0 and i1.hi < 1, ["i1 " + fmt_iv(i1)])
refcheck("07b", "i1", i1, PAPER["tight_i1_prefix"])
record("07c", "L_reg = A(1-i1) - P_reg equals gamma_star"
       " (0 in enclosure of difference, width < 1e-40)",
       dreg.contains(0) and dreg.width() < TINY,
       ["L_reg " + fmt_iv(Lreg), "L_reg - gamma_star " + fmt_iv(dreg)])
record("07d", "L_irr = b1 i1 equals gamma_star"
       " (0 in enclosure of difference, width < 1e-40)",
       dirr.contains(0) and dirr.width() < TINY,
       ["L_irr " + fmt_iv(Lirr), "L_irr - gamma_star " + fmt_iv(dirr)])
print()

# ----------------------------------------------------------------------
# CHECK 8 -- unique-case base
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 8: unique base 2^(p0 - gamma_new) < 1.306969598 (STRICT)")
print("-" * 76)

base_new_unique = pow2_iv(P0 - gamma_new)
thr = Q(PAPER["unique_base_upper"])
record("08a", "2^(p0 - 0.0000687793) < 1.306969598",
       base_new_unique.hi < thr,
       ["2^(p0-gamma_new) " + fmt_iv(base_new_unique),
        "margin to threshold = " + dec_str(thr - base_new_unique.hi, 12, -1)])
refcheck("08b", "unique base", base_new_unique, PAPER["m_unique_base"])
base_p0 = pow2_iv(P0)
refcheck("08c", "2^p0 (classical PPSZ base)", base_p0,
         PAPER["pow2_p0_prefix"])
print()

# ----------------------------------------------------------------------
# CHECK 9 -- Scheder's one-dimensional endgame, exact rational minimax
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 9: old endgame min_{irr in [0,1]} max{(1-irr)/10118 - 1/41391,"
      " irr/1380} (all exact)")
print("-" * 76)
# f(irr) = (1-irr)/10118 - 1/41391 : strictly decreasing (slope -1/10118)
# g(irr) = irr/1380               : strictly increasing (slope +1/1380)
# f(0) > g(0) = 0 and f(1) < 0 < g(1)  =>  unique crossing x* in (0,1).
# For irr <= x*: max >= f(irr) >= f(x*) = v; for irr >= x*: max >= g(irr)
# >= g(x*) = v; at x* the max equals v.  Hence the minimax equals the
# crossing value v = g(x*).  Everything is exact rational arithmetic.

c1, c2, c3 = PAPER["endgame"]          # 10118, 41391, 1380


def f_end(x):
    return (1 - x) / Fr(c1) - Fr(1, c2)


def g_end(x):
    return x / Fr(c3)


xstar = (Fr(1, c1) - Fr(1, c2)) / (Fr(1, c3) + Fr(1, c1))
vstar = g_end(xstar)
gamma_old = Fr(1, PAPER["gamma_old_den"])

record("09a", "crossing point x* in (0,1) and f(x*) == g(x*) exactly",
       0 < xstar < 1 and f_end(xstar) == g_end(xstar),
       ["x* = %s" % xstar, "   = " + dec_str(xstar, 30, 0)])
record("09b", "monotonicity: f strictly decreasing, g strictly increasing"
       " (exact slopes -1/%d, +1/%d) => minimax = crossing value" % (c1, c3),
       Fr(-1, c1) < 0 < Fr(1, c3))
record("09c", "exact minimax value v = x*/1380",
       True,
       ["v  = %s" % vstar, "   = " + dec_str(vstar, 30, 0),
        "1/v = " + dec_str(1 / vstar, 30, 0)])
record("09d", "paper eq. (2) final step: minimax >= 1/15218 (exact)",
       vstar >= gamma_old,
       ["v - 1/15218 = %s" % (vstar - gamma_old),
        "            = " + dec_str(vstar - gamma_old, 21, 0),
        "1/v = 15218 + 1204/31273 = 15218.0384996... > 15218, hence"
        " v < 1/15218:",
        "the displayed pair supports only the smaller constant v; the"
        " terminal",
        "'>= 1/15218' of eq. (2) is REFUTED by exact rational arithmetic"
        " (FINDING F1)."])
record("09e", "JSON gamma_old parses to exactly 1/15218",
       Q(CERT["lifting"]["gamma_old"]) == gamma_old)
# decimal claimed in tex line 82
u = ref_ulp(PAPER["gamma_old_decimal"])
record("09f", "paper decimal 0.000065711657247995... matches 1/15218",
       abs(gamma_old - Q(PAPER["gamma_old_decimal"])) <= u,
       ["1/15218 = " + dec_str(gamma_old, 30, 0)])
record("09g", "corrected clean endgame bound derivable from eq. (1):"
       " v >= 1/15219 (exact)",
       vstar >= Fr(1, 15219),
       ["v - 1/15219 = %s" % (vstar - Fr(1, 15219)),
        "            = " + dec_str(vstar - Fr(1, 15219), 21, 0)])
base_corrected = pow2_iv(P0 - vstar)
record("09h", "impact guard: 2^(p0 - v) < 1.306972377 (Scheder's rounded"
       " published base, tex line 45) survives the correction",
       base_corrected.hi < Q("1.306972377"),
       ["2^(p0 - 31273/475913718) " + fmt_iv(base_corrected),
        "margin to 1.306972377 = "
        + dec_str(Q("1.306972377") - base_corrected.hi, 12, -1)])
print()

# ----------------------------------------------------------------------
# CHECK 10 -- old unique base
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 10: old unique base 2^(p0 - 1/15218) < 1.306972376566 (STRICT)")
print("-" * 76)

base_old_unique = pow2_iv(P0 - gamma_old)
thr = Q(CERT["lifting"]["old_unique_base_upper"])
record("10a", "2^(p0 - 1/15218) < 1.306972376566 (JSON threshold)",
       base_old_unique.hi < thr,
       ["2^(p0-1/15218) " + fmt_iv(base_old_unique),
        "margin to threshold = " + dec_str(thr - base_old_unique.hi, 12, -1)])
refcheck("10b", "old unique base (paper unrounded 1.306972376565153...)",
         base_old_unique, PAPER["old_unique_base_unrounded"])
print()

# ----------------------------------------------------------------------
# CHECK 11 -- p* and q0
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 11: p* = 1 - 1/(2 ln 2) and q0 = p0 - p*")
print("-" * 76)

q0_alt = (2 * LN2 - 2 + 1 / (2 * LN2)).rounded()   # algebraically = q0
record("11a", "p* enclosure (target ~ 0.27865247955551829632)",
       PSTAR.intersects(Iv(Q("0.27865247955551829632") - Fr(2, 10 ** 20),
                           Q("0.27865247955551829632") + Fr(2, 10 ** 20)))
       and PSTAR.width() < Fr(1, 10 ** 70),
       ["p*  " + fmt_iv(PSTAR)])
record("11b", "q0 enclosure (target ~ 0.10764188156437232251)",
       Q0.intersects(Iv(Q("0.10764188156437232251") - Fr(2, 10 ** 20),
                        Q("0.10764188156437232251") + Fr(2, 10 ** 20)))
       and Q0.width() < Fr(1, 10 ** 70),
       ["q0  " + fmt_iv(Q0)])
record("11c", "q0 > 0 and p* < 1 (needed later: g' > 0 and eta = q0 delta)",
       Q0.lo > 0 and PSTAR.hi < 1)
record("11d", "plumbing identity: q0 == 2 ln2 - 2 + 1/(2 ln2)"
       " (enclosures intersect)", Q0.intersects(q0_alt))
refcheck("11e", "q0 (paper prefix)", Q0, PAPER["q0_prefix"])
print()

# ----------------------------------------------------------------------
# CHECK 12 -- root brackets for g_gamma
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 12: root brackets for g_gamma(d) = h2(d) + (1 - p* + gamma) d"
      " - gamma")
print("-" * 76)
# Uniqueness (also in report): h2'(d) = log2((1-d)/d), so
# g'(d) = log2((1-d)/d) + 1 - p* + gamma > 0 on (0, 1/2]  because
# log2((1-d)/d) >= 0 there and 1 - p* + gamma > 0 (check 11c: p* < 1,
# gamma > 0).  g is therefore strictly increasing on (0,1/2]; a sign change
# over the bracket certifies exactly one root, lying inside the bracket.

d_old_lo = Q(CERT["lifting"]["delta_old_lower"])
d_old_hi = Q(CERT["lifting"]["delta_old_upper"])
d_new_lo = Q(CERT["lifting"]["delta_new_lower"])
d_new_hi = Q(CERT["lifting"]["delta_new_upper"])

H2 = {}
for d in (d_old_lo, d_old_hi, d_new_lo, d_new_hi):
    H2[d] = h2_rat(d)


def g_gamma(gamma, d):
    return (H2[d] + (1 - PSTAR + gamma) * Iv(d) - gamma).rounded()


g_ol = g_gamma(gamma_old, d_old_lo)
g_oh = g_gamma(gamma_old, d_old_hi)
g_nl = g_gamma(gamma_new, d_new_lo)
g_nh = g_gamma(gamma_new, d_new_hi)

record("12a", "g_{gamma_old}(0.00000321978491531273261) < 0", g_ol.hi < 0,
       ["g " + fmt_iv(g_ol)])
record("12b", "g_{gamma_old}(0.00000321978491531273262) > 0", g_oh.lo > 0,
       ["g " + fmt_iv(g_oh)])
record("12c", "g_{gamma_new}(0.00000338183369577144614) < 0", g_nl.hi < 0,
       ["g " + fmt_iv(g_nl)])
record("12d", "g_{gamma_new}(0.00000338183369577144615) > 0", g_nh.lo > 0,
       ["g " + fmt_iv(g_nh)])
record("12e", "brackets lie in (0, 1/2) where g is strictly increasing"
       " (uniqueness argument in report)",
       0 < d_old_lo < d_old_hi < Fr(1, 2) and
       0 < d_new_lo < d_new_hi < Fr(1, 2))
print()

# ----------------------------------------------------------------------
# CHECK 13 -- lifted bonuses eta = q0 * delta
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 13: eta_old/new = q0 * [delta bracket]; containment;"
      " strict improvement")
print("-" * 76)
# Since q0 > 0 (11c) and the true root delta_gamma lies in its bracket (12),
# eta_infty(gamma) = q0 * delta_gamma lies in the interval product
# q0_encl * bracket.  These enclosures are DATA-LIMITED: their width is
# dominated by the certificate's bracket width 1e-23, not by our arithmetic.

eta_old = (Q0 * Iv(d_old_lo, d_old_hi)).rounded()
eta_new = (Q0 * Iv(d_new_lo, d_new_hi)).rounded()
eo_tgt = Iv(Q("0.0000003465837065"), Q("0.0000003465837066"))
en_tgt = Iv(Q("0.0000003640269421"), Q("0.0000003640269422"))

record("13a", "eta_old inside [0.0000003465837065, 0.0000003465837066]",
       eta_old.inside(eo_tgt), ["eta_old " + fmt_iv(eta_old)])
record("13b", "eta_new inside [0.0000003640269421, 0.0000003640269422]",
       eta_new.inside(en_tgt), ["eta_new " + fmt_iv(eta_new)])
record("13c", "eta_new > eta_old (strict, certified)",
       cert_gt(eta_new, eta_old),
       ["gap eta_new - eta_old " + fmt_iv((eta_new - eta_old).rounded())])
refcheck("13d", "eta gap", (eta_new - eta_old).rounded(),
         PAPER["m_eta_gap"])
ratio = (eta_new / eta_old - 1).rounded()
record("13e", "eta_new/eta_old - 1 > 0.0503 (JSON"
       " relative_improvement_lower)", ratio.lo > Q("0.0503"),
       ["ratio - 1 " + fmt_iv(ratio),
        "margin = " + dec_str(ratio.lo - Q("0.0503"), 12, -1)])
print()

# ----------------------------------------------------------------------
# CHECK 14 -- safe-separator branch margins at delta_0
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 14: branch margins at delta_0 = 338183369/10^14,"
      " eta_safe = 0.000000364")
print("-" * 76)

delta0 = Fr(338183369, 10 ** 14)
record("14a", "delta_0 equals JSON delta_safe and paper's 0.00000338183369",
       delta0 == Q(CERT["lifting"]["delta_safe"]) == Q(PAPER["delta0"]))
eta_safe = Q(CERT["lifting"]["eta_safe"])
record("14b", "eta_safe equals paper's 0.000000364",
       eta_safe == Q(PAPER["eta_safe"]))

M1 = (Q0 * Iv(delta0) - eta_safe).rounded()        # high-branch margin
h2_d0 = h2_rat(delta0)
u_d0 = (gamma_new * (1 - Iv(delta0)) - (1 - P0) * Iv(delta0)
        - h2_d0).rounded()                          # u_{gamma_new}(delta_0)
M2 = (u_d0 - eta_safe).rounded()                    # unique-residual margin

record("14c", "q0 delta_0 - eta_safe > 2.69e-11",
       M1.lo > Q("0.0000000000269"),
       ["q0 delta_0 - eta_safe " + fmt_iv(M1),
        "margin over 2.69e-11 = "
        + dec_str(M1.lo - Q("0.0000000000269"), 12, -1)])
refcheck("14d", "high-branch margin", M1, PAPER["m_high_branch"])
record("14e", "u_{gamma_new}(delta_0) - eta_safe > 2.70e-11",
       M2.lo > Q("0.0000000000270"),
       ["u_{gamma_new}(delta_0) " + fmt_iv(u_d0),
        "u - eta_safe " + fmt_iv(M2),
        "margin over 2.70e-11 = "
        + dec_str(M2.lo - Q("0.0000000000270"), 12, -1)])
refcheck("14f", "unique-residual margin", M2, PAPER["m_unique_residual"])
print()

# ----------------------------------------------------------------------
# CHECK 15 -- safe general base
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 15: safe general base 2^(p0 - eta_safe) < 1.307031578 (STRICT)")
print("-" * 76)

base_safe = pow2_iv(P0 - eta_safe)
thr = Q(PAPER["safe_general_base_upper"])
record("15a", "2^(p0 - 0.000000364) < 1.307031578",
       base_safe.hi < thr,
       ["2^(p0-eta_safe) " + fmt_iv(base_safe),
        "margin to threshold = " + dec_str(thr - base_safe.hi, 12, -1)])
refcheck("15b", "safe base", base_safe, PAPER["m_safe_base"])
print()

# ----------------------------------------------------------------------
# CHECK 16 -- conservative general bases from the eta interval lower ends
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 16: conservative limiting bases (lower eta endpoints)")
print("-" * 76)
# t -> 2^(p0 - t) is strictly decreasing.  The true eta_infty exceeds the
# lower end of its certified interval, so 2^(p0 - eta_lo) upper-bounds the
# true limiting base; we certify 2^(p0 - eta_lo) < threshold.

base_old_gen = pow2_iv(P0 - Q("0.0000003465837065"))
base_new_gen = pow2_iv(P0 - Q("0.0000003640269421"))
thr_o = Q(CERT["lifting"]["old_base_upper"])
thr_n = Q(CERT["lifting"]["new_limiting_base_upper"])

record("16a", "2^(p0 - 0.0000003465837065) < 1.307031593710",
       base_old_gen.hi < thr_o,
       ["base " + fmt_iv(base_old_gen),
        "margin = " + dec_str(thr_o - base_old_gen.hi, 12, -1)])
refcheck("16b", "old limiting general base", base_old_gen,
         PAPER["m_old_general_base"])
record("16c", "2^(p0 - 0.0000003640269421) < 1.307031577907",
       base_new_gen.hi < thr_n,
       ["base " + fmt_iv(base_new_gen),
        "margin = " + dec_str(thr_n - base_new_gen.hi, 12, -1)])
refcheck("16d", "new limiting general base", base_new_gen,
         PAPER["m_new_general_base"])
record("16e", "ordering of certified bases: new limiting < safe theorem"
       " base < old limiting",
       base_new_gen.hi < base_safe.lo and base_safe.hi < base_old_gen.lo)
print()

# ----------------------------------------------------------------------
# CHECK 17 -- gamma_new vs gamma_old (exact)
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 17: gamma_new - gamma_old > 0 (exact rationals)")
print("-" * 76)

ggap_exact = gamma_new - gamma_old
record("17a", "gamma_new - gamma_old > 0", ggap_exact > 0,
       ["gamma_new - gamma_old = %s" % ggap_exact,
        "                      " + fmt_iv(Iv(ggap_exact))])
refcheck("17b", "gamma_new - gamma_old", Iv(ggap_exact),
         PAPER["m_gnew_gold"])
rel_unique = gamma_new / gamma_old - 1
record("17c", "gamma_new/gamma_old - 1 > 0.04668 (JSON"
       " unique_relative_improvement_lower; exact)",
       rel_unique > Q("0.04668"),
       ["exact value = %s = %s" % (rel_unique, dec_str(rel_unique, 21, 0))])
print()

# ----------------------------------------------------------------------
# CHECK 18 -- JSON reported_intervals concordance
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 18: JSON reported_intervals vs independent enclosures")
print("-" * 76)
print("JSON version string: %r" % CERT["version"])

RI = CERT["reported_intervals"]
pairs = [
    ("A", IA), ("P_reg", IPreg), ("S", S_), ("b1", b1), ("b0", b0),
    ("bT", bT), ("lambda", lam), ("gamma_star", gstar), ("tight_i1", i1),
]
for idx, (key, mine) in enumerate(pairs):
    theirs = Iv(Q(RI[key + "_lower"]), Q(RI[key + "_upper"]))
    inter = mine.intersects(theirs)
    if mine.inside(theirs):
        rel = "ours inside theirs"
    elif theirs.inside(mine):
        rel = "theirs inside ours"
    elif inter:
        rel = "PARTIAL OVERLAP"
    else:
        rel = "EMPTY INTERSECTION"
    record("18%s" % "abcdefghi"[idx],
           "%s: intersection with JSON [%s, %s]" %
           (key, RI[key + "_lower"], RI[key + "_upper"]),
           inter, ["ours  " + fmt_iv(mine), "relation: " + rel])
sbm = Q(RI["safe_branch_margin_lower"])
record("18j", "safe_branch_margin_lower %s: both branch margins at delta_0"
       " certified >= it" % RI["safe_branch_margin_lower"],
       M1.lo >= sbm and M2.lo >= sbm,
       ["min branch margin lower bound = "
        + dec_str(min(M1.lo, M2.lo), 21, -1)])
print()

# ----------------------------------------------------------------------
# CHECK 19 (bonus) -- cross-evaluation at Scheder's parameters (0.1, 0.029)
# ----------------------------------------------------------------------

print("-" * 76)
print("CHECK 19 (bonus): same affine program at Scheder's parameters"
      " (eps_R, eps_I) = (0.1, 0.029)")
print("-" * 76)
# tex line 702: 'At Scheder's final parameters (0.1, 0.029), the same affine
# program gives 0.000065719084...'.  Independent second data point that
# exercises every formula in checks 2-6.

eR2, eI2 = Q("0.1"), Q("0.029")
cL2 = Q("0.001687") * eR2 - Q("0.006404") * eR2 * eR2
cT2 = (Q("0.009307") - Q("0.055") * eR2 - Q("0.1503") * f_KL(eR2)).rounded()
A2 = Fr(17, 18) * cL2
Preg2 = Q("1.1") * eR2 * (2 * A2 / Q("0.9"))
S2 = (cT2 - 5 * A2).rounded()
fI2 = f_KL(eI2)
b1_2 = (Q("0.030966") * eI2 - Q("0.0028") * eI2 * eI2
        - Q("0.4027") * fI2).rounded()
b0_2 = (Q("0.06259") * eI2 - Q("0.344") * fI2).rounded()
bT_2 = (Q("0.009307") - Q("0.2405") * eI2 - Q("0.03125") * eI2 * eI2
        - Q("0.06183") * f_KL(5 * eI2)).rounded()
gstar2 = (b1_2 * Iv(A2 - Preg2) / (Iv(A2) + b1_2)).rounded()

record("19a", "certificate conditions hold at (0.1, 0.029): A>P_reg,"
       " b0-2b1>0, A bT + b1 S > 0",
       A2 > Preg2 and (b0_2 - 2 * b1_2).lo > 0
       and (Iv(A2) * bT_2 + b1_2 * S2).lo > 0,
       ["b0-2b1 " + fmt_iv((b0_2 - 2 * b1_2).rounded()),
        "A bT + b1 S " + fmt_iv((Iv(A2) * bT_2 + b1_2 * S2).rounded())])
refcheck("19b", "gamma_star(0.1, 0.029)", gstar2,
         PAPER["scheder_params_value"])
record("19c", "fixed parameters beat Scheder's parameters:"
       " gamma_star(eR,eI) > gamma_star(0.1,0.029)",
       cert_gt(gstar, gstar2),
       ["gamma_star(0.1,0.029) " + fmt_iv(gstar2)])
print()

# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------

print("=" * 76)
fails = [(cid, desc) for (cid, ok, desc) in RESULTS if not ok]
print("SUMMARY: %d sub-checks, %d PASS, %d FAIL"
      % (len(RESULTS), len(RESULTS) - len(fails), len(fails)))
for cid, desc in fails:
    print("  FAILED %s: %s" % (cid, desc))
if [c for c, _ in fails] == ["09d"]:
    print()
    print("FINDING F1 (the only FAIL; a genuine refutation, not a checker")
    print("  malfunction): the terminal inequality of paper eq. (2)")
    print("  [tex lines 70-78],   max{(1-irr)/10118 - 1/41391, irr/1380}")
    print("  >= 1/15218,   is FALSE near the crossing irr* ="
          " 7192790/79318953.")
    print("  The exact minimax of the displayed pair is")
    print("      v = 31273/475913718 = 1/(15218 + 1204/31273)")
    print("        = 0.0000657114910060230707617... < 1/15218,")
    print("  a shortfall of exactly 43/258659105733 ~= 1.6624e-10.  The")
    print("  clean bound actually derivable from eq. (1) is >= 1/15219")
    print("  (certified in 09g).  Impact: gamma_old = 1/15218 enters this")
    print("  paper only as the quoted historical constant; Theorem 1.2")
    print("  (gamma_new), its dual certificate, and Corollary 1.3 do not")
    print("  depend on eq. (2) and are fully certified above.  Check 09h")
    print("  certifies that Scheder's rounded published base 1.306972377")
    print("  survives the correction.")
    print()
    print("OVERALL: FAIL -- one refuted paper display (FINDING F1); every")
    print("  arithmetic claim underlying the paper's NEW results PASSes.")
elif fails:
    print("OVERALL: FAIL")
else:
    print("OVERALL: PASS -- every arithmetic claim checked is certified.")
print("(Version-string mismatch v5/v6 and eq-numbering note are provenance"
      " FLAGs, documented in the report; they are not arithmetic failures.)")
print("=" * 76)
sys.exit(1 if fails else 0)
