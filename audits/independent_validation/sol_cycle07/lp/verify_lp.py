#!/usr/bin/env python3
"""Independent exact-rational audit of the Jiang--Cai recombination LP.

This program deliberately does not import or call any Cycle-7 checker.  Every
printed interval is rational.  The only transcendental quantity needed by the
LP is

    f_KL(e) = (1-e) log(1-e) + e.

For rational 0 <= e < 1 we enclose log(1-e) with the finite series

    -sum_{k=1}^N e^k/k - e^(N+1)/((N+1)(1-e))
        <= log(1-e)
        <= -sum_{k=1}^N e^k/k.

The tail inequality follows termwise from 1/k <= 1/(N+1) for k>N.
Thus ordinary floating point is not used for any asserted sign or bracket.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def q(decimal: str) -> Fraction:
    """Interpret a finite decimal as the exact rational it denotes."""
    return Fraction(decimal)


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def point(x: Fraction) -> "Interval":
        return Interval(x, x)

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other: "Interval") -> "Interval":
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other: "Interval") -> "Interval":
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return Interval(Fraction(1, 1) / self.hi, Fraction(1, 1) / self.lo)

    def __truediv__(self, other: "Interval") -> "Interval":
        return self * other.reciprocal()


def fkl(e: Fraction, terms: int = 240) -> Interval:
    """Certified rational enclosure of (1-e) log(1-e)+e."""
    if not 0 <= e < 1:
        raise ValueError("fkl series requires 0 <= e < 1")
    if e == 0:
        return Interval.point(Fraction(0))
    power = e
    partial = Fraction(0)
    for k in range(1, terms + 1):
        partial += power / k
        power *= e
    # Here power=e^(terms+1).  This is a valid (slightly loose) geometric
    # upper bound on sum_{k=terms+1}^infty e^k/k.
    tail = power / ((terms + 1) * (1 - e))
    log_interval = Interval(-partial - tail, -partial)
    return Interval.point(1 - e) * log_interval + Interval.point(e)


def floor_scaled(x: Fraction, digits: int) -> int:
    scale = 10**digits
    return (x.numerator * scale) // x.denominator


def ceil_scaled(x: Fraction, digits: int) -> int:
    scale = 10**digits
    return -((-x.numerator * scale) // x.denominator)


def scaled_string(value: int, digits: int) -> str:
    sign = "-" if value < 0 else ""
    value = abs(value)
    if digits == 0:
        return sign + str(value)
    raw = str(value).rjust(digits + 1, "0")
    return f"{sign}{raw[:-digits]}.{raw[-digits:]}"


def bracket(iv: Interval, digits: int = 30) -> str:
    return (
        "["
        + scaled_string(floor_scaled(iv.lo, digits), digits)
        + ", "
        + scaled_string(ceil_scaled(iv.hi, digits), digits)
        + "]"
    )


def main() -> None:
    eps_r = q("0.1024756190168075228998451658")
    eps_i = q("0.07307238160252154687451293138")

    c_l = q("0.001687") * eps_r - q("0.006404") * eps_r * eps_r
    a = Fraction(17, 18) * c_l
    threshold = Fraction(2, 1) * a / q("0.9")
    p_reg = q("1.1") * eps_r * threshold
    c = a - p_reg

    f_r = fkl(eps_r)
    f_i = fkl(eps_i)
    f_5i = fkl(5 * eps_i)

    c_t = (
        Interval.point(q("0.009307") - q("0.055") * eps_r)
        - Interval.point(q("0.1503")) * f_r
    )
    s = c_t - Interval.point(5 * a)

    b1 = (
        Interval.point(q("0.030966") * eps_i - q("0.0028") * eps_i * eps_i)
        - Interval.point(q("0.4027")) * f_i
    )
    b0 = (
        Interval.point(q("0.06259") * eps_i)
        - Interval.point(q("0.344")) * f_i
    )
    bt = (
        Interval.point(
            q("0.009307")
            - q("0.2405") * eps_i
            - q("0.03125") * eps_i * eps_i
        )
        - Interval.point(q("0.06183")) * f_5i
    )

    a_iv = Interval.point(a)
    c_iv = Interval.point(c)
    lam = b1 / a_iv
    slack_i0 = b0 - Interval.point(2) * b1
    slack_tau = bt + lam * s

    denominator = a_iv + b1
    i1_star = c_iv / denominator
    gamma_star = b1 * c_iv / denominator
    y_r = b1 / denominator
    y_i = a_iv / denominator

    # All assertions below are statements about exact Fractions.
    assert p_reg > 0 and a > p_reg
    assert s.lo > 0
    assert b1.lo > 0 and b0.lo > 0 and bt.hi < 0
    assert slack_i0.lo > 0
    assert slack_tau.lo > 0
    assert i1_star.lo > 0 and i1_star.hi < Fraction(1, 10)
    assert y_r.lo > 0 and y_i.lo > 0
    assert y_r.hi + y_i.hi >= 1 and y_r.lo + y_i.lo <= 1

    print("All sign assertions PASS using exact rational arithmetic.")
    print(f"series terms: 240")
    print(f"epsilon_R (exact): {eps_r.numerator}/{eps_r.denominator}")
    print(f"epsilon_I (exact): {eps_i.numerator}/{eps_i.denominator}")
    print(f"A:          {bracket(a_iv)}")
    print(f"P_reg:      {bracket(Interval.point(p_reg))}")
    print(f"A-P_reg:    {bracket(c_iv)}")
    print(f"S:          {bracket(s)}")
    print(f"b_0:        {bracket(b0)}")
    print(f"b_1:        {bracket(b1)}")
    print(f"b_T:        {bracket(bt)}")
    print(f"lambda:     {bracket(lam)}")
    print(f"i0 slack:   {bracket(slack_i0)}")
    print(f"tau slack:  {bracket(slack_tau)}")
    print(f"i_1*:       {bracket(i1_star)}")
    print(f"gamma*:     {bracket(gamma_star)}")
    print(f"dual y_R:   {bracket(y_r)}")
    print(f"dual y_I:   {bracket(y_i)}")


if __name__ == "__main__":
    main()
