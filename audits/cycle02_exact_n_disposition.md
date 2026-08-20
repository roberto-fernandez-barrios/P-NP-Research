# Post-integration disposition of the exact finite `N(n)` track

**Date:** 2026-08-21  
**Prior frozen-hash audit:** [`cycle02_exact_n_adversarial.md`](cycle02_exact_n_adversarial.md)  
**Disposition:** **PASS.** The integration edits are limited to the documented editorial/status changes and two redundant checker-hardening assertions. The finite values, selected families, witnesses, level-cover certificates, and unsymmetrized `n=8` lower-bound certificate remain valid.

No exact-track artifact was edited and nothing was committed during this disposition. Fresh optimizer output was written only to an isolated system-temporary directory.

## 1. Current artifact hashes

| Artifact | Current SHA-256 | Frozen-audit SHA-256 |
|---|---|---|
| `research_cycle_02/exact_balanced_chain_values.md` | `C4FF20705FCC04808E0ACFF4E2522C9EB2DAD218588C8B1AA2B1C6BAEECC94D9` | `08B2C6D6589A32A1F1360574BCC9D886997C13E88420559A81AB19EA227C4233` |
| `experiments/balanced_chain_optimize.py` | `4E60D409FE5245F6FACF2BE596B923B8F82A93EEC257991A41CE183815CB126D` | `3FF99039431AF09424BAEB47EA907FD854AA963863BDA3EE662E88200FF034DE` |
| `experiments/check_balanced_chain_certificates.py` | `2EC04C5ACC1EDA13CA2F961F875D093DDE9BC1AA8561F5A8678D52EC0AB86E0B` | `A47B98412D1726FFA31E1F35AA5EB038FFC69D703B1A751A8BB4400A49E78DF8` |
| `certificates/balanced_chain_exact/README.md` | `16B442B221669753E532CE4CD02694A035D62EBEB9F682CD7738F6A398837471` | not frozen in the prior table |
| `exact_n2.json` | `C945ABAAF6541AEC5384F3DDD2C55D3C11E30487E0965D58C708A67BFD647EA6` | `281C84531EC15D67B205F43C4E0DAD20E43EF90B488A98F8E6A37D0B08FBE0AF` |
| `exact_n4.json` | `AB3007F3D0C7212B7C64690F652751165AE3F6C9EE45EE98610CE08479DE5C72` | `9E24756A443E354DF1BB1DF7ACE9BCE0B5E70FEDCA7010782193977E0AA7CD1F` |
| `exact_n6.json` | `D4C0E681F8A156B30B6CF1F02B41E084AF7D9688EFE2DFF85271E6583094E8F4` | `65B248730DCC838FD8D4C2282E9B45EF30E06A9D01B7177035ECA3A904183643` |
| `exact_n8.json` | `C04FC9615474FE1CA25B7644CD450EE50D1B372BE5647D66BF21C022B7C63B30` | `E8D2E2AB66CB3CE9E113E46673DC6ED32539D3F66EC25D430DFD3ECC48BED0D6` |
| `level_cover_lower_bounds.json` | `0C4A78D600E18D6D7425BDC22DC2701C5F550727E28F409806877119092067CD` | same |
| `n8_no_size19.json` | `17664A3B8E283AFBD2A2DA2149BF7CFEB15C6A0CC04E81092F46C3E2F4E55009` | same |

All JSON files in `certificates/balanced_chain_exact/` parse successfully.

## 2. Change-scope audit

### 2.1 Optimizer

The optimizer's mathematical code is byte-for-byte unchanged. Replacing only the new `epistemic_status` literal

```text
COMPUTATIONALLY VERIFIED; ADVERSARIALLY REVIEWED; UNFORMALIZED;
NOVELTY STATUS RECORDED SEPARATELY
```

with the former literal

```text
COMPUTATIONALLY VERIFIED BY TWO CODE PATHS; UNFORMALIZED;
NOT NOVELTY-AUDITED
```

reconstructs the prior frozen SHA-256 exactly:

`3FF99039431AF09424BAEB47EA907FD854AA963863BDA3EE662E88200FF034DE`.

There is no change to compatibility, complement quotienting, canonical-chain relabeling, flow construction, level inequalities, integrality, objective, witness extraction, or solver acceptance conditions.

### 2.2 Independent checker

The checker has exactly the two hardening additions requested by the adversarial audit:

1. re-encode `family_elements` and require exact equality with `family_masks`;
2. require `n8_no_size19.json`'s `prerequisite_level_counts` to equal the independently recomputed `n=8` level minima.

Deleting only those two assertions reconstructs the prior checker hash exactly:

`A47B98412D1726FFA31E1F35AA5EB038FFC69D703B1A751A8BB4400A49E78DF8`.

They reject inconsistent redundant metadata but do not change the finite definition or lower-bound enumeration.

### 2.3 Report

The report now has the documented corrections:

- “all `n+1` prefix masks,” replacing the false `n=8`-specific phrase “all nine”;
- “all choices of four reachable level-2 sets,” replacing the ambiguous phrase “all four reachable level-2 choices”;
- status metadata separating internal adversarial review from novelty status (`KNOWN` for the routine `n=2,4` cases and `UNCLEAR` for `n=6,8`);
- a provenance footer that time-scopes the proposer's original independence statement and points later editorial, literature, and validation work to repository audits.

The formal definition, exact-value table, displayed families, model, reductions, layer minima, size-19 exhaustion, and numerical conclusions are unchanged and still agree with the certificates.

The former novelty-search wording ambiguity is now closed. Section 6 says
that the **original computation track** performed no novelty search and links
the later independent literature audit and novelty log. Replacing only this
new five-line sentence/link block by the former unqualified sentence
reconstructs the immediately preceding report hash exactly:
`707F342F40DB388961D3644C64EB4209D21F9D8CB78236028375499289FFF486`.
Thus the final hash change is wholly accounted for by this editorial
time-qualification; no mathematical text changed.

### 2.4 Exact JSON certificates

The four current files carry the updated epistemic-status string and regenerated `elapsed_seconds` metadata. Comparing a retained fresh run from the prior audit with the present fresh run, after removing only `epistemic_status` and `optimizer.elapsed_seconds`, gives exact JSON-object equality for every `n=2,4,6,8`.

More directly, the current stored and newly generated certificates have identical:

- `claimed_optimum`;
- `family_masks` and `family_elements`;
- `level_counts`;
- the complete ordered witness list for every signed balanced coloring;
- all non-runtime optimizer metadata, including objective and dual bound.

The lower-bound artifacts did not change even at the byte level. In particular, the `n=8` branch counts, coverage histogram, maximum 64-of-70 coverage, and enumeration digest remain frozen.

**Change-scope result: PASS. No mathematical or search-semantic change was found.**

## 3. Independent checker rerun

Running

```text
python -B experiments/check_balanced_chain_certificates.py
```

on the current stored certificates returned:

```text
PASS n=2: upper witnesses exhaustive; lower bound=3
PASS n=4: upper witnesses exhaustive; lower bound=6
PASS n=6: upper witnesses exhaustive; lower bound=12
PASS n=8: upper witnesses exhaustive; lower bound=20
PASS n=8 no-size-19 enumeration: 100800 level-4 branches
ALL BALANCED-CHAIN CERTIFICATES PASS
```

The two new hardening assertions were therefore exercised successfully.

## 4. Fresh optimizer rerun

One fresh optimizer run was made for all requested sizes in an isolated system-temp directory:

```text
python -B experiments/balanced_chain_optimize.py \
  --n 2 4 6 8 --time-limit 600 --output-dir <system-temp-directory>
```

| `n` | fresh objective | fresh dual | B&B nodes | family identical to stored | witnesses identical to stored |
|---:|---:|---:|---:|---|---|
| 2 | 3 | 3 | 0 | yes | yes |
| 4 | 6 | 6 | 1 | yes | yes |
| 6 | 12 | 12 | 1 | yes | yes |
| 8 | 20 | 20 | 9 | yes | yes |

For each fresh file, the only difference from its stored counterpart is `optimizer.elapsed_seconds`.

I then copied only the unchanged `level_cover_lower_bounds.json` and `n8_no_size19.json` into that temporary output directory and ran the independent checker against the fresh optimizer certificates. It again returned all five PASS lines and `ALL BALANCED-CHAIN CERTIFICATES PASS`.

No third independent enumeration was redone in this narrow disposition; the prior adversarial audit remains the record of that validation.

## 5. Final disposition

The current artifacts continue to certify

\[
N(2)=3,\qquad N(4)=6,\qquad N(6)=12,\qquad N(8)=20.
\]

The status remains `COMPUTATIONALLY VERIFIED; ADVERSARIALLY REVIEWED; UNFORMALIZED`, with the separately recorded novelty labels described above. No value is claimed for `n=10`, and no asymptotic inference is warranted.

**Final disposition: PASS.**
