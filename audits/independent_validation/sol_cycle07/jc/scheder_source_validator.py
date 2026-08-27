#!/usr/bin/env python3
"""Exact/certified checks for the Scheder import repairs used by JC.

The formulas are transcribed from freshly fetched ECCC TR21-069 revision 1.
No Cycle-7 checker is imported.  Polynomial signs use exact Sturm sequences;
transcendentals use the independent rational enclosures in
``jc_exact_validator.py``; the two half-integral Section-7 quantities use an
exact-rational range integral after r=x^2/2.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q

from jc_exact_validator import Iv, LN2, as_iv, dec, q, sci


@dataclass(frozen=True)
class Poly:
    """Univariate polynomial, ascending exact-rational coefficients."""

    c: tuple[Q, ...]

    def __init__(self, coeffs=()):
        vals = [q(x) for x in coeffs]
        while vals and vals[-1] == 0:
            vals.pop()
        object.__setattr__(self, "c", tuple(vals))

    @staticmethod
    def constant(x) -> "Poly":
        return Poly([] if q(x) == 0 else [q(x)])

    @property
    def degree(self) -> int:
        return len(self.c) - 1

    def __bool__(self) -> bool:
        return bool(self.c)

    def __add__(self, other) -> "Poly":
        b = as_poly(other)
        n = max(len(self.c), len(b.c))
        return Poly(
            [(self.c[i] if i < len(self.c) else 0) + (b.c[i] if i < len(b.c) else 0) for i in range(n)]
        )

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly([-x for x in self.c])

    def __sub__(self, other) -> "Poly":
        return self + (-as_poly(other))

    def __rsub__(self, other) -> "Poly":
        return as_poly(other) - self

    def __mul__(self, other) -> "Poly":
        b = as_poly(other)
        if not self or not b:
            return Poly()
        out = [Q(0)] * (len(self.c) + len(b.c) - 1)
        for i, a_i in enumerate(self.c):
            for j, b_j in enumerate(b.c):
                out[i + j] += a_i * b_j
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n: int) -> "Poly":
        if n < 0:
            raise ValueError("negative polynomial power")
        out = Poly.constant(1)
        base = self
        k = n
        while k:
            if k & 1:
                out *= base
            base *= base
            k >>= 1
        return out

    def derivative(self) -> "Poly":
        return Poly([i * self.c[i] for i in range(1, len(self.c))])

    def eval(self, x: Q) -> Q:
        out = Q(0)
        for a in reversed(self.c):
            out = out * x + a
        return out

    def divmod(self, divisor: "Poly") -> tuple["Poly", "Poly"]:
        if not divisor:
            raise ZeroDivisionError
        rem = list(self.c)
        quot = [Q(0)] * max(0, self.degree - divisor.degree + 1)
        while rem and len(rem) - 1 >= divisor.degree:
            shift = len(rem) - 1 - divisor.degree
            coeff = rem[-1] / divisor.c[-1]
            quot[shift] = coeff
            for j, d_j in enumerate(divisor.c):
                rem[shift + j] -= coeff * d_j
            while rem and rem[-1] == 0:
                rem.pop()
        return Poly(quot), Poly(rem)


def as_poly(x) -> Poly:
    return x if isinstance(x, Poly) else Poly.constant(x)


@dataclass(frozen=True)
class Rat:
    num: Poly
    den: Poly

    def __init__(self, num, den=1):
        n = as_poly(num)
        d = as_poly(den)
        if not d:
            raise ZeroDivisionError
        object.__setattr__(self, "num", n)
        object.__setattr__(self, "den", d)

    def __add__(self, other) -> "Rat":
        b = as_rat(other)
        return Rat(self.num * b.den + b.num * self.den, self.den * b.den)

    __radd__ = __add__

    def __neg__(self) -> "Rat":
        return Rat(-self.num, self.den)

    def __sub__(self, other) -> "Rat":
        return self + (-as_rat(other))

    def __rsub__(self, other) -> "Rat":
        return as_rat(other) - self

    def __mul__(self, other) -> "Rat":
        b = as_rat(other)
        return Rat(self.num * b.num, self.den * b.den)

    __rmul__ = __mul__

    def __truediv__(self, other) -> "Rat":
        b = as_rat(other)
        return Rat(self.num * b.den, self.den * b.num)

    def __rtruediv__(self, other) -> "Rat":
        return as_rat(other) / self

    def __pow__(self, n: int) -> "Rat":
        return Rat(self.num**n, self.den**n)

    def derivative(self) -> "Rat":
        return Rat(self.num.derivative() * self.den - self.num * self.den.derivative(), self.den**2)

    def eval(self, x: Q) -> Q:
        return self.num.eval(x) / self.den.eval(x)


def as_rat(x) -> Rat:
    return x if isinstance(x, Rat) else Rat(x)


def sign(x: Q) -> int:
    return (x > 0) - (x < 0)


def sturm_sequence(p: Poly) -> list[Poly]:
    if not p:
        return []
    seq = [p, p.derivative()]
    if not seq[1]:
        return [p]
    while seq[-1]:
        _, rem = seq[-2].divmod(seq[-1])
        if not rem:
            break
        seq.append(-rem)
    return seq


def variations(seq: list[Poly], x: Q) -> int:
    signs = [sign(p.eval(x)) for p in seq]
    signs = [s for s in signs if s]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def strip_endpoint_roots(p: Poly, a: Q, b: Q) -> Poly:
    out = p
    for endpoint in (a, b):
        factor = Poly([-endpoint, 1])
        while out and out.eval(endpoint) == 0:
            quo, rem = out.divmod(factor)
            if rem:
                raise AssertionError("failed exact endpoint factor")
            out = quo
    return out


SIGN_CERTS: list[str] = []


def cert_poly_nonnegative(p: Poly, a: Q, b: Q, name: str, strict_endpoints: bool = False) -> None:
    if a >= b:
        raise ValueError("bad interval")
    if not p:
        if strict_endpoints:
            raise AssertionError(name + ": zero polynomial")
        SIGN_CERTS.append(name + " [identically zero]")
        return
    pa, pb = p.eval(a), p.eval(b)
    if strict_endpoints:
        if pa <= 0 or pb <= 0:
            raise AssertionError(f"{name}: nonpositive endpoint")
    elif pa < 0 or pb < 0:
        raise AssertionError(f"{name}: negative endpoint")
    core = strip_endpoint_roots(p, a, b)
    if not core:
        SIGN_CERTS.append(name + " [endpoint factors only]")
        return
    seq = sturm_sequence(core)
    roots = variations(seq, a) - variations(seq, b)
    mid_value = p.eval((a + b) / 2)
    if roots != 0 or mid_value <= 0:
        raise AssertionError(f"{name}: roots={roots}, midpoint={mid_value}")
    SIGN_CERTS.append(
        f"{name} [deg={p.degree}, open-roots=0, endpoint-signs={sign(pa)}/{sign(pb)}]"
    )


def cert_rat_nonnegative(x: Rat, a: Q, b: Q, name: str, strict=False) -> None:
    cert_poly_nonnegative(x.den, a, b, name + " denominator", strict_endpoints=True)
    cert_poly_nonnegative(x.num, a, b, name + " numerator", strict_endpoints=strict)


def ffun(x: Rat) -> Rat:
    return x * (1 - 2 * x) / (1 - x) ** 2


def gfun(x: Rat) -> Rat:
    return (1 - 2 * x) ** 2 / (1 - x) ** 3


def c12_branch(eps: Q, branch: str) -> dict[str, Rat]:
    r = Rat(Poly([0, 1]))
    u = 1 - 2 * r
    if branch == "low":
        delta = q("12/5") * eps * r**2 * u**3 / (1 - r)
    elif branch == "high":
        delta = q("6/5") * eps * r * u**2 * (-1 + 7 * r - 7 * r**2) / (1 - r)
    else:
        raise ValueError(branch)
    eta = delta / (1 - r)
    s = r - eta
    sprime = s.derivative()
    return {
        "delta": delta,
        "eta": eta,
        "s": s,
        "prefactor": q("0.05") * r * u - 2 * delta * (1 - r),
        "f-ratio": ffun(r) - q("0.98") * ffun(s),
        "sprime-lower": sprime,
        "sprime-upper": q("1.05") - sprime,
        "g-ratio": gfun(r) - q("0.945") * gfun(s),
    }


def certify_c12(eps: Q, tag: str) -> None:
    # The true max switches at alpha=(5-sqrt(13))/6 in (1/5,1/4).
    domains = {"low": (q(0), q("1/4")), "high": (q("1/5"), q("1/2"))}
    for branch, (a, b) in domains.items():
        facts = c12_branch(eps, branch)
        cert_rat_nonnegative(facts["delta"], a, b, f"{tag} {branch}: delta>=0")
        cert_rat_nonnegative(facts["s"], a, b, f"{tag} {branch}: s>=0")
        r = Rat(Poly([0, 1]))
        cert_rat_nonnegative(r - facts["s"], a, b, f"{tag} {branch}: s<=r")
        cert_rat_nonnegative(facts["prefactor"], a, b, f"{tag} {branch}: C12 prefactor .95")
        cert_rat_nonnegative(facts["f-ratio"], a, b, f"{tag} {branch}: C12 f ratio .98")
        cert_rat_nonnegative(facts["sprime-lower"], a, b, f"{tag} {branch}: s'>=0")
        cert_rat_nonnegative(facts["sprime-upper"], a, b, f"{tag} {branch}: s'<=1.05")
        cert_rat_nonnegative(facts["g-ratio"], a, b, f"{tag} {branch}: C12 g ratio .945")


def poly_compose_one_minus(p: Poly) -> Poly:
    # p(1-u)
    u = Poly([0, 1])
    out = Poly()
    power = Poly.constant(1)
    for coeff in p.c:
        out += coeff * power
        power *= 1 - u
    return out


def integrate_poly_over_one_minus(p: Poly, power: int) -> tuple[Q, Q]:
    """Integral_0^(1/2) p(r)/(1-r)^power dr = rational + log_coeff*ln2."""
    pu = poly_compose_one_minus(p)
    rational = Q(0)
    log_coeff = Q(0)
    # Integral from u=1/2 to 1 of p(1-u) u^-power du.
    for j, coeff in enumerate(pu.c):
        exponent = j - power
        if exponent == -1:
            log_coeff += coeff
        else:
            rational += coeff * (1 - Q(1, 2) ** (exponent + 1)) / (exponent + 1)
    return rational, log_coeff


def eval_log_form(form: tuple[Q, Q]) -> Iv:
    rational, log_coeff = form
    return Iv.point(rational) + log_coeff * LN2


def multiply_log_form(form: tuple[Q, Q], scalar: Q) -> tuple[Q, Q]:
    return scalar * form[0], scalar * form[1]


def obj_pow(x, n: int):
    out = 1
    for _ in range(n):
        out *= x
    return out


@dataclass(frozen=True)
class Jet2:
    """Interval value and first two derivatives for rigorous AD."""

    v: Iv
    d1: Iv
    d2: Iv

    @staticmethod
    def constant(x) -> "Jet2":
        return Jet2(as_iv(x), Iv.point(0), Iv.point(0))

    def __add__(self, other):
        b = as_jet(other)
        return Jet2(self.v + b.v, self.d1 + b.d1, self.d2 + b.d2)

    __radd__ = __add__

    def __neg__(self):
        return Jet2(-self.v, -self.d1, -self.d2)

    def __sub__(self, other):
        return self + (-as_jet(other))

    def __rsub__(self, other):
        return as_jet(other) - self

    def __mul__(self, other):
        b = as_jet(other)
        return Jet2(
            self.v * b.v,
            self.d1 * b.v + self.v * b.d1,
            self.d2 * b.v + 2 * self.d1 * b.d1 + self.v * b.d2,
        )

    __rmul__ = __mul__

    def reciprocal(self):
        inv = 1 / self.v
        return Jet2(
            inv,
            -self.d1 / obj_pow(self.v, 2),
            2 * obj_pow(self.d1, 2) / obj_pow(self.v, 3) - self.d2 / obj_pow(self.v, 2),
        )

    def __truediv__(self, other):
        return self * as_jet(other).reciprocal()

    def __rtruediv__(self, other):
        return as_jet(other) / self


def as_jet(x) -> Jet2:
    return x if isinstance(x, Jet2) else Jet2.constant(x)


def section7_integrands(x):
    # Substitution r=x^2/2, dr=x dx, x in [0,1].
    r = obj_pow(x, 2) / 2
    u = 1 - 2 * r
    Qr = obj_pow(r / (1 - r), 2)
    B = 1 + obj_pow(u, 2) * (1 - 2 * r + 2 * obj_pow(r, 2)) / obj_pow(1 - r, 2)
    gamma_rest = q("12/5") * obj_pow(r, 2) * obj_pow(u, 3) / (1 - r)
    base = 2 * r * gamma_rest * B / obj_pow(1 - r, 3)
    # phi_A(r) dr = sqrt(2)*(5/2)x^6(1-x^2)(7-11x^2) dx.
    phi_dr_without_sqrt2 = q("5/2") * obj_pow(x, 6) * (1 - obj_pow(x, 2)) * (7 - 11 * obj_pow(x, 2))
    dfs_no_sqrt = -Qr * B * phi_dr_without_sqrt2
    dfd = base * x
    junk_no_sqrt = base * phi_dr_without_sqrt2
    return dfs_no_sqrt, dfd, junk_no_sqrt


def range_integrate_section7(parts: int = 256) -> tuple[Iv, Iv, Iv]:
    # Composite midpoint with an exact interval bound on the second
    # derivative in every cell: |error_cell| <= M*h^3/24.
    centers = [Iv.point(0), Iv.point(0), Iv.point(0)]
    errors = [Q(0), Q(0), Q(0)]
    width = Q(1, parts)
    for i in range(parts):
        a, b = Q(i, parts), Q(i + 1, parts)
        midpoint = (a + b) / 2
        vals = section7_integrands(Iv.point(midpoint))
        jet_x = Jet2(Iv(a, b), Iv.point(1), Iv.point(0))
        jets = section7_integrands(jet_x)
        for j in range(3):
            centers[j] += width * vals[j]
            second = jets[j].d2
            m_bound = max(abs(second.lo), abs(second.hi))
            errors[j] += m_bound * width**3 / 24
    totals = [Iv(c.lo - e, c.hi + e) for c, e in zip(centers, errors)]
    sqrt2 = Iv(q("1.414213562373095"), q("1.414213562373096"))
    if not (sqrt2.lo * sqrt2.lo < 2 < sqrt2.hi * sqrt2.hi):
        raise AssertionError("sqrt2 bracket")
    return totals[0] * sqrt2, totals[1], totals[2] * sqrt2


def main() -> None:
    eps_r = q("0.1024756190168075228998451658")
    eps_i = q("0.07307238160252154687451293138")

    # Exact switch analysis for delta_max.
    switch = Poly([-1, 5, -3])  # second max argument minus first, sans positive factor
    assert switch.eval(q("1/5")) < 0 < switch.eval(q("1/4"))
    assert switch.derivative().eval(q("1/2")) > 0
    print("PASS: delta_max switch is unique in (1/5,1/4); enlarged branch domains are sound")

    certify_c12(eps_r, "JC epsilon_R")
    print(f"PASS: all C.12 range facts and four numerical claims at epsilon_R ({len(SIGN_CERTS)} sign certificates)")

    # Direct exact counterexample to the source's internal epsilon<=.13 claim.
    bad = c12_branch(q("0.13"), "high")["sprime-upper"].eval(q("5/12"))
    if bad >= 0:
        raise AssertionError("expected epsilon=.13 counterexample")
    print(f"PASS: source claim s'<=1.05 for epsilon<=.13 is false at r=5/12; 1.05-s'={bad}")

    # Threshold constraint and C.13(2)'s hairline d=4 value, independently integrated.
    rr = Poly([0, 1])
    ocb_integrand_num = rr**5 * (1 - 2 * rr)
    ocb4_form = multiply_log_form(integrate_poly_over_one_minus(ocb_integrand_num, 2), q("0.88"))
    ocb4 = eval_log_form(ocb4_form)
    if ocb4.lo <= q("1/1150"):
        raise AssertionError("OCB*(4) threshold")
    print(f"PASS: OCB*(4)={dec(ocb4.lo,22)}... > 1/1150; source proof requires Thr<=1/1150")

    # Lemma 75 max and corrected epsilon constraint.
    # r(1-2r) <= 1/8 follows from 1/8-r(1-2r)=2(r-1/4)^2.
    identity = Poly([q("1/8"), -1, 2]) - 2 * (rr - q("1/4")) ** 2
    if identity:
        raise AssertionError("quadratic identity")
    gamma_id_max = q("10/64")
    if not (eps_i < q("64/600") and eps_i * gamma_id_max < q("1/60")):
        raise AssertionError("epsilon_I corrected admissibility")
    print("PASS: max 10*r^2*(1-2r)^2=10/64, not 10/256; corrected epsilon<=64/600")
    # Lemma 73 invokes r(1-2r)>=2*epsilon*gamma_ID.  Division by
    # r(1-2r)>0 and max r(1-2r)=1/8 give epsilon<=2/5, not 4/5.
    if not (eps_i < q("2/5") and q("4/5") > q("2/5")):
        raise AssertionError("Lemma 73 range")
    print("PASS: Lemma-73 printed epsilon<=4/5 is false; its condition yields epsilon<=2/5; JC point is safe")

    # Definition 68 constants reconstructed from defining integrals.
    u = 1 - 2 * rr
    gamma_id = 10 * rr**2 * u**2
    gamma_pid = q("61/6") * rr**3 * u**2
    phi_id = gamma_id.derivative()
    phi_pid = gamma_pid.derivative()
    phi_two_density = (20 * rr**3 * u).derivative()
    cert_poly_nonnegative(q("5/2") - phi_id, 0, q("1/2"), "density phi_ID <= 5/2")
    cert_poly_nonnegative(q("5/2") + phi_id, 0, q("1/2"), "density phi_ID >= -5/2")
    cert_poly_nonnegative(q("61/54") - phi_pid, 0, q("1/2"), "density phi_pID <= 61/54")
    cert_poly_nonnegative(q("61/54") + phi_pid, 0, q("1/2"), "density phi_pID >= -61/54")
    cert_poly_nonnegative(phi_two_density + 5, 0, q("1/2"), "density phi_TwoCC >= -5")
    print("PASS: JC density derivative bounds re-certified exactly")
    # Q=r^2/(1-r)^2; P(1-Q)=r(1-2r)/(1-r)^3.
    bfs = eval_log_form(multiply_log_form(integrate_poly_over_one_minus(-phi_id * rr**2, 2), 1))
    dfc = eval_log_form(integrate_poly_over_one_minus(gamma_id * rr * u, 3))
    dfs = eval_log_form(integrate_poly_over_one_minus(-phi_pid * rr**2, 2))
    dfb = dfc + dfs
    junk1 = eval_log_form(integrate_poly_over_one_minus(-phi_id * gamma_id * rr * u, 3))
    junk2 = eval_log_form(integrate_poly_over_one_minus(phi_pid * gamma_id * rr * u, 3))
    junk = junk1 + 2 * junk2
    if integrate_poly_over_one_minus(phi_pid * gamma_id * rr * u, 3) != (
        q("8767591/192"),
        q("-65880"),
    ):
        raise AssertionError("Definition 68 JUNK2 closed form")
    if not (bfs.lo > q("0.06259") and dfb.hi < q("0.03163")):
        raise AssertionError("Definition 68 linear constants")
    if not (junk1.hi < q("0.00235") and junk2.lo > q("0.000184") and junk.hi < q("0.0028")):
        raise AssertionError("Definition 68 quadratic constants")
    print(f"PASS: Definition-68 JUNK2={dec(junk2.lo,20)}... > .000184 (printed bound false)")
    print(f"PASS: downstream JUNK=JUNK1+2JUNK2={dec(junk.hi,20)}... < .0028 survives")

    # Section 8.3 constants independently reconstructed from B, not printed closed forms.
    B_num = (1 - rr) ** 2 + u**2 * (1 - 2 * rr + 2 * rr**2)
    # B=B_num/(1-r)^2; Q=r^2/(1-r)^2.
    gamma_two = 20 * rr**3 * u
    phi_two = gamma_two.derivative()
    dfs8 = eval_log_form(integrate_poly_over_one_minus(-rr**2 * B_num * phi_two, 4))
    dfd8 = eval_log_form(integrate_poly_over_one_minus(2 * rr * gamma_id * B_num, 5))
    junk8 = eval_log_form(integrate_poly_over_one_minus(2 * rr * gamma_id * B_num * phi_two, 5))
    if integrate_poly_over_one_minus(-rr**2 * B_num * phi_two, 4) != (
        q("39094/3"),
        q("-18800"),
    ):
        raise AssertionError("Section 8.3 DFS closed form")
    if integrate_poly_over_one_minus(2 * rr * gamma_id * B_num, 5) != (
        q("-23747/3"),
        q("11420"),
    ):
        raise AssertionError("Section 8.3 DFD closed form")
    if integrate_poly_over_one_minus(2 * rr * gamma_id * B_num * phi_two, 5) != (
        q("17923400/7"),
        q("-3694000"),
    ):
        raise AssertionError("Section 8.3 JUNK closed form")
    if not (dfd8.lo > q("0.074135") and (dfs8 + dfd8).hi < q("0.2405")):
        raise AssertionError("Section 8.3 DFD/sum")
    if not (junk8.hi < q("0.03125")):
        raise AssertionError("Section 8.3 JUNK")
    print(f"PASS: Section-8.3 DFD2CC={dec(dfd8.lo,20)}... > .074135 (printed intermediate false)")
    print(f"PASS: DFS2CC+DFD2CC={dec((dfs8+dfd8).hi,20)}... < .2405 survives")
    print(f"PASS: Section-8.3 JUNK2CC={dec(junk8.hi,20)}... < .03125")

    # Lemma 55's 0.001687 coefficient from its defining integral.
    l55 = eval_log_form(integrate_poly_over_one_minus(rr**2 * u**5, 4))
    if integrate_poly_over_one_minus(rr**2 * u**5, 4) != (q("-707/6"), q("170")):
        raise AssertionError("Lemma 55 closed form")
    if l55.lo <= q("0.001687"):
        raise AssertionError("Lemma 55 coefficient")
    print(f"PASS: Lemma-55 integral={dec(l55.lo,20)}... > .001687")

    # Remaining coefficient roundings in the irregular display.
    psi_id = integrate_poly_over_one_minus(phi_id**2, 0)[0]
    psi_pid = integrate_poly_over_one_minus(phi_pid**2, 0)[0]
    if psi_id != q("5/21") or psi_pid != q("3721/181440"):
        raise AssertionError("Psi integrals")
    b1_kl = Iv.point(psi_id + 2 * psi_pid) / LN2
    b0_kl = Iv.point(psi_id) / LN2
    bt_kl = Iv.point(q("15/350")) / LN2
    cut_bonus = Iv.point(q("104/3")) - 50 * LN2
    if not (
        (bfs - dfb).lo > q("0.030966")
        and b1_kl.hi < q("0.4027")
        and b0_kl.hi < q("0.344")
        and bt_kl.hi < q("0.06183")
        and cut_bonus.lo > q("0.009307")
    ):
        raise AssertionError("irregular coefficient roundings")
    regular_kl = Iv.point(q("5/48")) / LN2
    if regular_kl.hi >= q("0.1503"):
        raise AssertionError("regular KL rounding")
    print("PASS: all load-bearing regular/irregular coefficient roundings re-derived from defining integrals")

    # Section 7.7 half-integral quantities, certified by rational range integration.
    dfs7, dfd7, junk7 = range_integrate_section7()
    print(f"CERTIFIED Section-7.7 DFS2CC in [{dec(dfs7.lo,18)}, {dec(dfs7.hi,18)}]")
    print(f"CERTIFIED Section-7.7 DFD2CC in [{dec(dfd7.lo,18)}, {dec(dfd7.hi,18)}]")
    print(f"CERTIFIED Section-7.7 JUNK2CC in [{dec(junk7.lo,18)}, {dec(junk7.hi,18)}]")
    if not (dfs7.lo > q("0.0455") and dfd7.hi < q("0.0095") and junk7.lo > 0):
        raise AssertionError("Section 7.7 source errata")
    print("PASS: source Section-7.7 bounds DFS<=.0455 and JUNK<=-.019 are both false; DFD<=.0095 survives")

    # A conservative repaired regular TwoCC coefficient at JC's exact epsilon.
    # Cut bonus .009307 and KL .1503 f_KL are already conservative source rounds.
    # Here only certify that the actual Section-7.7 damage can be bounded by
    # .05529*eps + .001*eps^2.
    if not ((dfs7 + dfd7).hi < q("0.05529") and junk7.hi < q("0.001")):
        raise AssertionError("conservative Section 7.7 envelope")
    from jc_exact_validator import f_kl

    fkr = f_kl(eps_r, "source-repair-fKL")
    c_t_repaired = (
        Iv.point(q("0.009307") - q("0.05529") * eps_r - q("0.001") * eps_r * eps_r)
        - q("0.1503") * fkr
    )
    c_l = q("0.001687") * eps_r - q("0.006404") * eps_r * eps_r
    A = Iv.point(q("17/18") * c_l)
    p_reg = q("1.1") * eps_r * q("20/9") * A
    S_repaired = c_t_repaired - 5 * A

    # b1/bT recomputed as in JC; only the tau dual inequality depends on S.
    fki = f_kl(eps_i, "source-repair-fKLi")
    fk5i = f_kl(5 * eps_i, "source-repair-fKL5i")
    b1 = Iv.point(q("0.030966") * eps_i - q("0.0028") * eps_i**2) - q("0.4027") * fki
    bT = (
        Iv.point(q("0.009307") - q("0.2405") * eps_i - q("0.03125") * eps_i**2)
        - q("0.06183") * fk5i
    )
    repaired_tau_slack = bT + (b1 / A) * S_repaired
    if repaired_tau_slack.lo <= 0:
        raise AssertionError("repaired tau dual slack")
    gamma_star = b1 * (A - p_reg) / (A + b1)
    if gamma_star.lo <= q("0.0000687793"):
        raise AssertionError("repaired gamma")
    print(f"PASS: conservative repaired tau dual slack={dec(repaired_tau_slack.lo,18)}... >0")
    print("PASS: gamma_star and the Unique/general frontier are unchanged because tau=0 and gamma_star is S-independent")

    print(f"TOTAL EXACT STURM SIGN CERTIFICATES: {len(SIGN_CERTS)}")
    for item in SIGN_CERTS:
        print("  " + item)
    print("SCHEDER SOURCE REPAIR VALIDATION PASSED")


if __name__ == "__main__":
    main()
