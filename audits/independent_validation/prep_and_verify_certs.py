"""Prepare cert-line files for the C++ engine and do Python-side structural checks
(witness chains, canonical flag, common-reject counts) with the auditor's own code."""
import json, sys, subprocess
from collections import Counter
from audit_ref import intervals_by_len, sum_ok, popcount

REPO = r"C:\Users\masteria.DOMINE\rf\P-NP-Research"

def load(n):
    return json.load(open(REPO + rf"\certificates\cycle05_hybrid\hybrid_only_n{n}_candidates.json"))

def check(n, rejfile):
    q = n - 1
    m = n // 2
    certs = load(n)
    print(f"n={n}: {len(certs)} certificates in file")
    R = set(int(l) for l in open(rejfile) if l.strip())
    idc = intervals_by_len(list(range(q)), q)
    circ_cache = {}
    lines = []
    bad_struct = 0
    canonical = []
    perm_words = set()
    commonrej_claims = {}
    for i, c in enumerate(certs):
        assert c["n"] == n
        pf = c["perm_finite"]
        assert sorted(pf) == list(range(q)), i
        w = int(c["word"], 16)
        assert popcount(w) == m, i
        key = tuple(pf)
        if key not in circ_cache:
            circ_cache[key] = intervals_by_len(list(pf), q)
        c2 = circ_cache[key]
        # witness chain structural check (auditor's own semantics)
        masks = [int(x, 16) for x in c["witness_chain_masks"]]
        ok = True
        if len(masks) != q - 1:
            ok = False
        else:
            prev = 0
            for j, msk in enumerate(masks, start=1):
                if popcount(msk) != j or (msk & prev) != prev:
                    ok = False; break
                if not (msk in idc[j] or msk in c2[j]):
                    ok = False; break
                if not sum_ok(msk, w, j):
                    ok = False; break
                prev = msk
        if not ok:
            bad_struct += 1
            print(f"  BAD WITNESS CHAIN at cert {i} label={c.get('label')}")
        if c.get("canonical"):
            canonical.append((i, c.get("label"), c["word"], pf))
        pw = (key, w)
        if pw in perm_words:
            print(f"  DUPLICATE cert {i}")
        perm_words.add(pw)
        commonrej_claims.setdefault(key, set()).add(c["common_rejects_of_pair"])
        lines.append(f"{','.join(map(str,pf))} {w} {c.get('min_switches', 1)}")
    open(f"certlines_n{n}.txt", "w").write("\n".join(lines) + "\n")
    print(f"  witness chains: {len(certs)-bad_struct} OK, {bad_struct} bad")
    print(f"  distinct (perm,word) pairs: {len(perm_words)}; distinct perms: {len(circ_cache)}")
    print(f"  canonical flagged: {canonical}")
    # verify common_rejects_of_pair per perm with own computation
    badcr = 0
    for key, claims in commonrej_claims.items():
        pf = list(key)
        pinv = [0] * q
        for idx, v in enumerate(pf): pinv[v] = idx
        cr = 0
        for r in R:
            # words w with w o pf in R and w in R:  w = r o pf^{-1}
            wv = 0
            for x in range(q):
                if (r >> pinv[x]) & 1: wv |= 1 << x
            if wv in R: cr += 1
        # note: iterate rejects r as copy-2-rejected images; equivalently count set
        cr2 = sum(1 for w0 in R if int_compose(w0, pf, q) in R)
        if len(claims) != 1 or cr2 not in claims:
            badcr += 1
            print(f"  COMMONREJ MISMATCH perm={pf[:6]}... mine={cr2} claimed={claims}")
    print(f"  common-reject claims checked for {len(commonrej_claims)} perms, mismatches={badcr}")
    # words rescued coverage at n=24: every single-copy failure word rescued by some pair?
    if n == 24:
        rescued_words = set(w for (_, w) in perm_words)
        print(f"  distinct words among certs: {len(rescued_words)}; |R|={len(R)}; R covered: {len(rescued_words & R)}")

def int_compose(w, perm, q):
    r = 0
    for x in range(q):
        if (w >> perm[x]) & 1: r |= 1 << x
    return r

if __name__ == "__main__":
    n = int(sys.argv[1])
    check(n, f"R{n}.txt")
