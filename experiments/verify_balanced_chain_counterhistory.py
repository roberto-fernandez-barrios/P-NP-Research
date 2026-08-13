"""Exact check of the n=10 counterhistory in withdrawn ECCC TR26-043 v1.

The script conditions on a1=a2=b1=+1 in a uniformly random balanced
coloring of ten points.  The first two fair ties consume a1 and a2.  It then
computes exactly the conditional upward probability for absolute imbalance
and the next increment distribution of D=(# consumed from A)-(# from B).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def verify() -> None:
    # A = 0,...,4; B = 5,...,9.  Fixed positives are a1, a2, b1.
    fixed_positive = {0, 1, 5}
    remaining = sorted(set(range(10)) - fixed_positive)
    completions = []
    for extra_positive in combinations(remaining, 2):
        positive = fixed_positive | set(extra_positive)
        assert len(positive) == 5
        completions.append(positive)

    # After consuming a1,a2, the live frontiers are a3=2 and known b1=5.
    upward = sum(1 for positive in completions if 2 in positive)
    downward_choice = len(completions) - upward

    p_up = Fraction(upward, len(completions))
    # If a3 is negative, the rule consumes A and D increases.  If a3 is
    # positive, both frontiers are positive and a fair tie changes D by +/-1.
    p_d_plus = Fraction(downward_choice, len(completions)) + p_up / 2
    p_d_minus = p_up / 2

    assert len(completions) == 21
    assert p_up == Fraction(2, 7)
    assert p_up > Fraction(1, 4)
    assert p_d_plus == Fraction(6, 7)
    assert p_d_minus == Fraction(1, 7)
    assert p_d_plus != p_d_minus

    print(f"balanced completions={len(completions)}")
    print(f"Pr[absolute imbalance increases | history]={p_up}")
    print(f"Pr[D increment = +1 | history]={p_d_plus}")
    print(f"Pr[D increment = -1 | history]={p_d_minus}")


if __name__ == "__main__":
    verify()
