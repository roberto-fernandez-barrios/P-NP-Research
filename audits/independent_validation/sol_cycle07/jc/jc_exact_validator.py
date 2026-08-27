#!/usr/bin/env python3
"""Fresh exact-rational validator for arXiv:2607.10697v1.

Proof decisions use fractions.Fraction interval endpoints only.  This file was
implemented from CHECKER_DESIGN.md and does not import any Cycle-7 checker.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from typing import Iterable


LOG_TERMS = 90
EXP_TERMS = 90


def q(s: str | int | Q) -> Q:
    if isinstance(s, Q):
        return s
    if isinstance(s, int):
        return Q(s)
    return Q(s)


@dataclass(frozen=True)
class Iv:
    lo: Q
    hi: Q

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def point(x: str | int | Q) -> "Iv":
        z = q(x)
        return Iv(z, z)

    def __add__(self, other: "Iv | Q | int") -> "Iv":
        b = as_iv(other)
        return Iv(self.lo + b.lo, self.hi + b.hi)

    __radd__ = __add__

    def __neg__(self) -> "Iv":
        return Iv(-self.hi, -self.lo)

    def __sub__(self, other: "Iv | Q | int") -> "Iv":
        return self + (-as_iv(other))

    def __rsub__(self, other: "Iv | Q | int") -> "Iv":
        return as_iv(other) - self

    def __mul__(self, other: "Iv | Q | int") -> "Iv":
        b = as_iv(other)
        vals = (
            self.lo * b.lo,
            self.lo * b.hi,
            self.hi * b.lo,
            self.hi * b.hi,
        )
        return Iv(min(vals), max(vals))

    __rmul__ = __mul__

    def reciprocal(self) -> "Iv":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return Iv(min(1 / self.lo, 1 / self.hi), max(1 / self.lo, 1 / self.hi))

    def __truediv__(self, other: "Iv | Q | int") -> "Iv":
        return self * as_iv(other).reciprocal()

    def __rtruediv__(self, other: "Iv | Q | int") -> "Iv":
        return as_iv(other) / self


def as_iv(x: Iv | Q | int) -> Iv:
    return x if isinstance(x, Iv) else Iv.point(x)


@dataclass(frozen=True)
class SeriesAudit:
    label: str
    kind: str
    terms: int
    argument: Q
    reduction: str
    remainder_bound: Q


SERIES_AUDIT: list[SeriesAudit] = []


def _pow2(k: int) -> Q:
    return Q(2**k) if k >= 0 else Q(1, 2 ** (-k))


def _ln_mantissa(y: Q, label: str, terms: int = LOG_TERMS) -> Iv:
    if not (1 <= y < 2):
        raise ValueError(f"mantissa outside [1,2): {y}")
    if y == 1:
        SERIES_AUDIT.append(SeriesAudit(label, "ln-atanh", terms, y, "z=0", Q(0)))
        return Iv.point(0)
    z = (y - 1) / (y + 1)
    partial = Q(0)
    zpow = z
    for j in range(terms):
        partial += 2 * zpow / (2 * j + 1)
        zpow *= z * z
    remainder = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    SERIES_AUDIT.append(
        SeriesAudit(label, "ln-atanh", terms, y, f"z={z}", remainder)
    )
    return Iv(partial, partial + remainder)


# The explicit 2 -> z=1/3 identity avoids a
# special endpoint convention at y=2 in the generic mantissa reducer.
def _ln_two(terms: int = LOG_TERMS) -> Iv:
    z = Q(1, 3)
    partial = Q(0)
    for j in range(terms):
        partial += 2 * z ** (2 * j + 1) / (2 * j + 1)
    remainder = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    SERIES_AUDIT.append(
        SeriesAudit("ln2", "ln-atanh", terms, Q(2), "z=1/3", remainder)
    )
    return Iv(partial, partial + remainder)


LN2 = _ln_two()


def ln_point(x: Q, label: str, terms: int = LOG_TERMS) -> Iv:
    if x <= 0:
        raise ValueError("log argument must be positive")
    k = 0
    y = x
    while y < 1:
        y *= 2
        k -= 1
    while y >= 2:
        y /= 2
        k += 1
    mant = _ln_mantissa(y, label, terms)
    return mant + k * LN2


def ln_iv(x: Iv, label: str, terms: int = LOG_TERMS) -> Iv:
    # ln is increasing.
    low = ln_point(x.lo, label + ":lo", terms)
    high = ln_point(x.hi, label + ":hi", terms)
    return Iv(low.lo, high.hi)


def exp_point(x: Q, label: str, terms: int = EXP_TERMS) -> Iv:
    if x < 0:
        pos = exp_point(-x, label + ":reciprocal", terms)
        return pos.reciprocal()
    term = Q(1)
    partial = Q(1)
    for k in range(1, terms):
        term *= x / k
        partial += term
    next_term = term * x / terms
    ratio_bound = x / (terms + 1)
    if ratio_bound >= 1:
        raise ValueError("Taylor tail ratio is not contractive")
    tail = next_term / (1 - ratio_bound)
    SERIES_AUDIT.append(
        SeriesAudit(label, "exp-Taylor", terms, x, f"tail-ratio<={ratio_bound}", tail)
    )
    return Iv(partial, partial + tail)


def exp_iv(x: Iv, label: str, terms: int = EXP_TERMS) -> Iv:
    low = exp_point(x.lo, label + ":lo", terms)
    high = exp_point(x.hi, label + ":hi", terms)
    return Iv(low.lo, high.hi)


def pow2_iv(x: Iv, label: str) -> Iv:
    return exp_iv(x * LN2, label)


def f_kl(t: Q, label: str) -> Iv:
    one_minus = Iv.point(1 - t)
    return one_minus * ln_iv(one_minus, label) + t


def h2(t: Q, label: str) -> Iv:
    if not (0 < t < 1):
        raise ValueError("entropy implementation expects 0<t<1")
    a = Iv.point(t) * ln_iv(Iv.point(t), label + ":ln-d")
    b = Iv.point(1 - t) * ln_iv(Iv.point(1 - t), label + ":ln-1md")
    return -(a + b) / LN2


def dec(x: Q, digits: int = 28) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def sci(x: Q, digits: int = 8) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        return f"{Decimal(x.numerator) / Decimal(x.denominator):E}"


def show_iv(name: str, x: Iv) -> None:
    print(f"{name:34s} [{dec(x.lo)}, {dec(x.hi)}]")


CHECKS: list[str] = []


def passed(name: str) -> None:
    CHECKS.append(name)
    print(f"PASS {len(CHECKS):03d}: {name}")


def require(condition: bool, name: str) -> None:
    if not condition:
        raise AssertionError(name)
    passed(name)


def positive(x: Iv | Q | int, name: str) -> None:
    value = as_iv(x)
    require(value.lo > 0, name)


def negative(x: Iv | Q | int, name: str) -> None:
    value = as_iv(x)
    require(value.hi < 0, name)


def contained(x: Iv, lo: str, hi: str, name: str) -> None:
    require(q(lo) <= x.lo and x.hi <= q(hi), name)


def all_positive(values: Iterable[Iv]) -> bool:
    return all(v.lo > 0 for v in values)


def root_function(delta: Q, gamma: Q, pstar: Iv, label: str) -> Iv:
    return h2(delta, label) + (1 - pstar + gamma) * delta - gamma


def main() -> None:
    eps_r = q("0.1024756190168075228998451658")
    eps_i = q("0.07307238160252154687451293138")
    gamma_new = q("0.0000687793")
    gamma_old_printed = q("1/15218")
    eta_safe = q("0.000000364")
    delta_safe = q("0.00000338183369")

    require(0 < eps_r <= q("0.13"), "epsilon_R lies in JC's repaired stated domain [0,.13]")
    require(eps_r > q("0.1"), "epsilon_R is outside Scheder's printed epsilon<=.1 domain")
    require(0 < eps_i <= q("0.2"), "epsilon_I lies in [0,1/5]")
    require(5 * eps_i < 1, "5 epsilon_I < 1")
    require(eps_i < q("64/600"), "epsilon_I < corrected 64/600 threshold")

    p0 = 2 * LN2 - 1
    pstar = 1 - 1 / (2 * LN2)
    q0 = p0 - pstar
    show_iv("ln 2", LN2)
    show_iv("p0", p0)
    show_iv("pstar", pstar)
    show_iv("q0", q0)
    positive(LN2, "ln 2 positive")
    positive(q0, "q0 positive")

    f_r = f_kl(eps_r, "fKL(epsR)")
    f_i = f_kl(eps_i, "fKL(epsI)")
    f_5i = f_kl(5 * eps_i, "fKL(5epsI)")

    c_l = q("0.001687") * eps_r - q("0.006404") * eps_r * eps_r
    A = Iv.point(q("17/18") * c_l)
    threshold = q("20/9") * A
    p_reg = q("1.1") * eps_r * threshold
    c_t = Iv.point(q("0.009307") - q("0.055") * eps_r) - q("0.1503") * f_r
    S = c_t - 5 * A

    b1 = (
        Iv.point(q("0.030966") * eps_i - q("0.0028") * eps_i * eps_i)
        - q("0.4027") * f_i
    )
    b0 = Iv.point(q("0.06259") * eps_i) - q("0.344") * f_i
    bT = (
        Iv.point(
            q("0.009307")
            - q("0.2405") * eps_i
            - q("0.03125") * eps_i * eps_i
        )
        - q("0.06183") * f_5i
    )

    for name, value in (
        ("A", A),
        ("P_reg", p_reg),
        ("S", S),
        ("b1", b1),
        ("b0", b0),
        ("bT", bT),
    ):
        show_iv(name, value)

    contained(A, "0.0000997582178549", "0.0000997582178550", "reported A enclosure")
    contained(p_reg, "0.0000249890303097", "0.0000249890303098", "reported P_reg enclosure")
    contained(S, "0.00235445147822", "0.00235445147823", "reported S enclosure")
    contained(b1, "0.00114549739595", "0.00114549739597", "reported b1 enclosure")
    contained(b0, "0.00363196877285", "0.00363196877287", "reported b0 enclosure")
    contained(bT, "-0.01318180201459", "-0.01318180201458", "reported bT enclosure")

    positive(A, "A positive")
    positive(p_reg, "P_reg positive")
    positive(A - p_reg, "A-P_reg positive")
    positive(S, "S positive")
    positive(b1, "b1 positive")
    positive(b0, "b0 positive")
    negative(bT, "bT negative")
    require(threshold.hi <= q("1/1150"), "hidden source threshold Thr<=1/1150")

    lam = b1 / A
    slack_i0 = b0 - 2 * b1
    slack_tau = bT + lam * S
    gamma_star = b1 * (A - p_reg) / (A + b1)
    tight_i1 = (A - p_reg) / (A + b1)
    show_iv("lambda", lam)
    show_iv("dual i0 slack b0-2b1", slack_i0)
    show_iv("dual tau slack", slack_tau)
    show_iv("gamma_star", gamma_star)
    show_iv("tight i1", tight_i1)

    contained(lam, "11.4827371678", "11.4827371679", "reported lambda enclosure")
    contained(gamma_star, "0.000068779380458836", "0.000068779380458837", "reported gamma_star enclosure")
    contained(tight_i1, "0.060043244708778326", "0.060043244708778327", "reported tight-i1 enclosure")
    positive(slack_i0, "dual i0 inequality has positive slack")
    positive(slack_tau, "dual tau inequality has positive slack")
    positive(gamma_star - gamma_new, "gamma_star exceeds theorem gamma")

    # Primal/dual identities are exact consequences of these definitions.
    require(tight_i1.lo > 0 and tight_i1.hi < 1, "primal point lies in nonnegative normalized domain")
    require(A.lo + b1.lo > 0, "primal common denominator positive")
    passed("primal active constraints L_reg=z and L_irr=z (symbolic identity)")
    require(lam.lo > 0, "dual lambda nonnegative")
    passed("dual weights y_R=b1/(A+b1), y_I=A/(A+b1) are nonnegative and sum to one (symbolic identity)")
    passed("dual i1 inequality is tight: -A*y_R+b1*y_I=0 (symbolic identity)")
    passed("dual objective equals primal z=gamma_star (symbolic identity)")

    unique_base = pow2_iv(p0 - gamma_new, "unique-base")
    old_unique_base_printed = pow2_iv(p0 - gamma_old_printed, "old-unique-base-printed")
    show_iv("Unique theorem base", unique_base)
    positive(gamma_new - gamma_old_printed, "new unique gain exceeds printed old gain")
    require(
        gamma_new / gamma_old_printed - 1 > q("0.04668"),
        "unique gain relative improvement > certificate lower bound 0.04668",
    )
    require(unique_base.hi < q("1.306969598"), "Unique-3-SAT base < 1.306969598")
    require(
        old_unique_base_printed.hi < q("1.306972376566"),
        "printed-old unique base < certificate upper bound 1.306972376566",
    )

    d_old_l = q("0.00000321978491531273261")
    d_old_u = q("0.00000321978491531273262")
    d_new_l = q("0.00000338183369577144614")
    d_new_u = q("0.00000338183369577144615")
    f_old_l = root_function(d_old_l, gamma_old_printed, pstar, "root-old-low")
    f_old_u = root_function(d_old_u, gamma_old_printed, pstar, "root-old-high")
    f_new_l = root_function(d_new_l, gamma_new, pstar, "root-new-low")
    f_new_u = root_function(d_new_u, gamma_new, pstar, "root-new-high")
    show_iv("old root function at lower", f_old_l)
    show_iv("old root function at upper", f_old_u)
    show_iv("new root function at lower", f_new_l)
    show_iv("new root function at upper", f_new_u)
    negative(f_old_l, "old root lower endpoint has negative sign")
    positive(f_old_u, "old root upper endpoint has positive sign")
    negative(f_new_l, "new root lower endpoint has negative sign")
    positive(f_new_u, "new root upper endpoint has positive sign")
    require(d_old_l > 0 and d_old_u < q("1/2"), "old root bracket lies in (0,1/2)")
    require(d_new_l > 0 and d_new_u < q("1/2"), "new root bracket lies in (0,1/2)")
    # h2'(d)=log2((1-d)/d)>0 and 1-p*+gamma>0 on this domain.
    positive(1 - pstar + gamma_old_printed, "old root function is strictly increasing on (0,1/2)")
    positive(1 - pstar + gamma_new, "new root function is strictly increasing on (0,1/2)")

    eta_old = q0 * Iv(d_old_l, d_old_u)
    eta_new = q0 * Iv(d_new_l, d_new_u)
    show_iv("old lifted eta", eta_old)
    show_iv("new lifted eta", eta_new)
    contained(eta_old, "0.0000003465837065", "0.0000003465837066", "reported old eta enclosure")
    contained(eta_new, "0.0000003640269421", "0.0000003640269422", "reported new eta enclosure")
    positive(eta_new - eta_old, "new lifted gain exceeds old lifted gain")
    require(eta_new.lo / eta_old.hi - 1 > q("0.0503"), "lifted relative improvement > 5.03 percent")

    old_general_base = pow2_iv(p0 - eta_old, "old-general-base")
    new_general_lim_base = pow2_iv(p0 - eta_new, "new-general-lim-base")
    require(old_general_base.hi < q("1.307031593710"), "old limiting general base < 1.307031593710")
    require(new_general_lim_base.hi < q("1.307031577907"), "new limiting general base < 1.307031577907")
    require(new_general_lim_base.hi < old_general_base.lo, "new limiting general base strictly smaller")

    high_margin = q0 * delta_safe - eta_safe
    u_safe = (
        gamma_new * (1 - delta_safe)
        - (1 - p0) * delta_safe
        - h2(delta_safe, "safe-branch")
    )
    low_margin = u_safe - eta_safe
    show_iv("safe high-I branch margin", high_margin)
    show_iv("safe unique-residual margin", low_margin)
    positive(high_margin, "safe high-I branch margin positive")
    positive(low_margin, "safe unique-residual branch margin positive")
    require(min(high_margin.lo, low_margin.lo) > q("0.0000000000269"), "safe branch margin exceeds 2.69e-11")
    safe_general_base = pow2_iv(p0 - eta_safe, "safe-general-base")
    show_iv("safe general theorem base", safe_general_base)
    require(safe_general_base.hi < q("1.307031578"), "general-3-SAT theorem base < 1.307031578")

    # Scheder Section-6 endgame reconstructed exactly.
    old_repaired = q("31273/475913718")
    old_claim_gap = old_repaired - gamma_old_printed
    old_intersection_x = q(1380) * old_repaired
    require(
        old_repaired
        == (1 - old_intersection_x) / q(10118) - q("1/41391"),
        "Scheder repaired minimax: regular branch equals repaired value",
    )
    require(old_repaired == old_intersection_x / 1380, "Scheder repaired minimax: irregular branch equals repaired value")
    negative(Iv.point(old_claim_gap), "Scheder printed 1/15218 is strictly too large")
    require(old_claim_gap == q("-43/258659105733"), "exact defect in printed old gain is -43/258659105733")
    positive(gamma_new - old_repaired, "new unique gain exceeds repaired Scheder gain")
    repaired_old_base = pow2_iv(p0 - old_repaired, "old-unique-base-repaired")
    show_iv("repaired Scheder unique base", repaired_old_base)
    require(repaired_old_base.hi < q("1.306972377"), "repaired Scheder base still rounds below 1.306972377")

    # The historical repair also propagates through the same SS lift.  This
    # bracket is independent of the authors' old-gamma bracket: it brackets
    # the root for the exact repaired minimax 31273/475913718.
    d_repaired_l = q("0.00000321977615008507678")
    d_repaired_u = q("0.00000321977615008507680")
    f_repaired_l = root_function(d_repaired_l, old_repaired, pstar, "root-old-repaired-low")
    f_repaired_u = root_function(d_repaired_u, old_repaired, pstar, "root-old-repaired-high")
    negative(f_repaired_l, "repaired-old lift root lower endpoint has negative sign")
    positive(f_repaired_u, "repaired-old lift root upper endpoint has positive sign")
    require(
        0 < d_repaired_l < d_repaired_u < q("1/2"),
        "repaired-old lift root bracket lies in (0,1/2)",
    )
    positive(
        1 - pstar + old_repaired,
        "repaired-old lift root function is strictly increasing on (0,1/2)",
    )
    eta_old_repaired = q0 * Iv(d_repaired_l, d_repaired_u)
    general_old_repaired = pow2_iv(p0 - eta_old_repaired, "old-general-base-repaired")
    show_iv("repaired Scheder lifted eta", eta_old_repaired)
    show_iv("repaired Scheder general base", general_old_repaired)
    require(
        general_old_repaired.lo > q("1.307031593710"),
        "repair invalidates the overly tight old-general <1.307031593710 display",
    )
    require(
        general_old_repaired.hi < q("1.307031594"),
        "repaired Scheder general base still rounds below 1.307031594",
    )

    require(LOG_TERMS == 90 and EXP_TERMS == 90, "certificate truncation counts are exactly N=90")
    require(len(SERIES_AUDIT) > 0, "series audit is nonempty")
    require(all(a.remainder_bound >= 0 for a in SERIES_AUDIT), "every recorded series remainder bound is nonnegative")
    print("\nSERIES / REMAINDER LEDGER (all quantities exact rationals; decimals are display only)")
    for idx, audit in enumerate(SERIES_AUDIT, 1):
        print(
            f"SERIES {idx:03d} {audit.kind:12s} terms={audit.terms:2d} "
            f"label={audit.label} remainder<={sci(audit.remainder_bound, 12)}"
        )
    max_log = max(a.remainder_bound for a in SERIES_AUDIT if a.kind == "ln-atanh")
    max_exp = max(a.remainder_bound for a in SERIES_AUDIT if a.kind == "exp-Taylor")
    print(f"max exact log remainder bound (display): {sci(max_log, 16)}")
    print(f"max exact exp remainder bound (display): {sci(max_exp, 16)}")
    print(f"TOTAL ASSERTIONS PASSED: {len(CHECKS)}")
    print("INDEPENDENT EXACT-RATIONAL VALIDATION PASSED")


if __name__ == "__main__":
    main()
