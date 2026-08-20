"""Exact diagnostics for the Cycle-2 balanced-chain repair track.

This file does not search for, or certify, an O01 construction.  It checks
finite identities used in ``proof_sat_repair_track.md``:

* the Catalan-family lower bound on a two-/d-block excursion under the
  actual filtration;
* the posterior upward probability and block-load drift at the published
  n=10 counterhistory;
* deterministic residual-threshold inequalities; and
* the geometric-log accounting bound for recursive covers.

All displayed probabilities are exact ``Fraction`` values.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, log


def falling(a: int, k: int) -> int:
    """Return the falling factorial (a)_k."""
    if not (0 <= k <= a):
        return 0
    out = 1
    for value in range(a - k + 1, a + 1):
        out *= value
    return out


def catalan(k: int) -> int:
    return comb(2 * k, k) // (k + 1)


def is_dyck_word(positive_positions: set[int], length: int) -> bool:
    height = 0
    for index in range(length):
        height += 1 if index in positive_positions else -1
        if height < 0:
            return False
    return height == 0


def count_dyck_words(k: int) -> int:
    """Independent brute-force count for the Catalan identity."""
    from itertools import combinations

    count = 0
    for positive_tuple in combinations(range(2 * k), k):
        if is_dyck_word(set(positive_tuple), 2 * k):
            count += 1
    return count


def count_primitive_dyck_words(k: int) -> int:
    """Brute-force paths positive at proper times and zero at time 2k."""
    from itertools import combinations

    count = 0
    for positive_tuple in combinations(range(2 * k), k):
        positive_positions = set(positive_tuple)
        height = 0
        primitive = True
        for index in range(2 * k):
            height += 1 if index in positive_positions else -1
            if index < 2 * k - 1 and height <= 0:
                primitive = False
                break
        if primitive and height == 0:
            count += 1
    return count


def initial_all_same_probability(M: int, d: int) -> Fraction:
    """Probability that d initial frontiers have one common sign.

    The ambient coloring is uniform with M pluses and M minuses.
    """
    return Fraction(2 * falling(M, d), falling(2 * M, d))


def conditional_dyck_probability(M: int, k: int, d: int = 2) -> Fraction:
    """Exact conditional probability of a primitive 2k-step Dyck event.

    Condition on d initial frontiers all being + and consume one.  There are
    then d-1 cached + frontiers and 2M-d uninspected signs, comprising M-d
    pluses and M minuses.  A fixed word with k signs of each type has the
    indicated ordered-hypergeometric probability.  There are Catalan(k-1)
    words whose partial sums are strictly positive before returning to zero
    at step 2k; these give one uninterrupted excursion outside |H|<=1.
    """
    assert d >= 2
    assert k <= M - d
    assert k >= 1
    numerator = catalan(k - 1) * falling(M - d, k) * falling(M, k)
    denominator = falling(2 * M - d, 2 * k)
    return Fraction(numerator, denominator)


def posterior_up_probability(R: int, h: int, d: int = 2) -> Fraction:
    """Up probability with d-1 cached bad-sign frontiers.

    R is the total unconsumed pool size and h>0 the current absolute
    imbalance.  The pool has (R-h)/2 bad-sign points, of which d-1 are
    already exposed.  Only one new frontier is random at the next step.
    """
    assert h > 0 and d >= 2
    assert (R - h) % 2 == 0
    same_sign = (R - h) // 2
    assert same_sign >= d - 1
    return Fraction(same_sign - (d - 1), R - (d - 1))


def verify_threshold_repair() -> None:
    """Exhaustively check the deterministic variable-threshold split."""
    m = 1_000_000
    base = 350
    gap = 1 + int(28 * log(m))
    descent = 1 + int(8 * (1 + 4 * log(m)))
    residual_max = int(m ** (2 / 3))
    threshold = 2 * (descent + base)

    for residual in range(residual_max + 1):
        if residual < threshold:
            # Absorb: tail plus the entire residual fits this local budget.
            assert gap + residual < gap + 2 * descent + 2 * base
        else:
            # Recurse: after the asserted descent, at least half the segment
            # and at least the base amount remain unconsumed.
            leftover = residual - descent
            assert leftover >= Fraction(residual, 2)
            assert leftover >= base


def verify_recursive_accounting() -> None:
    """Numerically check sum_j log(m_j) <= log(n)/(1-alpha)."""
    n = 10**120
    alpha = Fraction(2, 3)
    current_log = log(n)
    total_log = 0.0
    for _ in range(10_000):
        total_log += current_log
        if current_log <= log(2):
            break
        current_log *= float(alpha)
    assert total_log <= log(n) / (1 - float(alpha)) + 1e-9


def verify() -> None:
    for k in range(1, 8):
        assert count_dyck_words(k) == catalan(k)
        assert count_primitive_dyck_words(k) == catalan(k - 1)

    # Published n=10 counterhistory: R=8, h=2, one cached bad frontier.
    p = posterior_up_probability(R=8, h=2, d=2)
    assert p == Fraction(2, 7)
    # If the fresh frontier belongs to A, the expected increment of A-B is
    # 1-p: a correcting fresh sign consumes A, while a bad-sign tie has mean
    # zero.  This recovers probabilities 6/7 and 1/7 for +/- increments.
    assert 1 - p == Fraction(5, 7)

    # Reachable failure of iterated "fresh pair" conditioning.  In a balanced
    # n=10 coloring, expose three disjoint batches with signs (+,-), (-,-),
    # (+,-), choosing +, -, + respectively.  The choices are all minimizers
    # at the current heights 0, 1, 0.  The unchosen signs are three known
    # negatives.  The four still-unseen signs comprise three pluses and one
    # negative, so the next fresh pair is all-plus with probability 1/2.
    consumed = [1, -1, 1]
    deferred = [-1, -1, -1]
    unseen = [1, 1, 1, -1]
    assert sum(consumed) == 1
    assert sum(consumed + deferred + unseen) == 0
    fresh_pair_bad = Fraction(comb(3, 2), comb(4, 2))
    assert fresh_pair_bad == Fraction(1, 2)

    # A finite heavy-tail certificate with enough room that neither of two
    # blocks can exhaust during the selected 2k continuation.
    M, k = 10, 4
    assert 2 * k + 1 < M
    conditional = conditional_dyck_probability(M=M, k=k, d=2)
    unconditional_lower_bound = initial_all_same_probability(M, 2) * conditional
    assert conditional > 0
    assert unconditional_lower_bound > 0

    # The same cache trap is present for every fixed d.  Use an instance with
    # block length 2M/d exceeding the certified continuation length.
    M_d, k_d, d = 60, 4, 3
    assert 2 * k_d + 1 < (2 * M_d) // d
    assert conditional_dyck_probability(M_d, k_d, d) > 0

    # Fresh-choice/defer accounting: after T disjoint d-batches, the deferred
    # residual and the number of possible chosen subsets are both exact.
    d_fresh, rounds = 3, 8
    assert (d_fresh - 1) * rounds == 16
    assert d_fresh**rounds == 6561

    verify_threshold_repair()
    verify_recursive_accounting()

    print(f"counterhistory posterior p_up={p}")
    print(f"counterhistory E[delta(A-B)]={1-p}")
    print(f"reachable fresh-pair posterior all-bad probability={fresh_pair_bad}")
    print(f"n={2*M}, k={k}, conditional primitive-Dyck probability={conditional}")
    print(
        "n=20 unconditional lower bound on an 8-step first gap="
        f"{unconditional_lower_bound}"
    )
    print(
        "d=3 conditional primitive-Dyck probability (n=120,k=4)="
        f"{conditional_dyck_probability(M_d, k_d, d)}"
    )
    print("fresh d=3, T=8: residual=16, possible chosen sets=6561")
    print("variable-threshold residual repair: PASS on all integer residuals")
    print("geometric-log recursive accounting: PASS")


if __name__ == "__main__":
    verify()
