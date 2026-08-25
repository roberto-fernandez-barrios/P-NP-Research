# Novelty / Frontier Audit — Jiang–Cai, "A Better Analysis For PPSZ For 3-SAT" (arXiv:2607.10697)

Audit date: 2026-08-25. Auditor: automated live-literature sweep (WebSearch + WebFetch + arXiv API + OpenAlex + GitHub API), supporting the hostile validation in research_cycle_07.

Scope: (a) accuracy of JC's claim that O*(1.307031578^n) is the best currently known worst-case randomized bound for general 3-SAT; (b) follow-ups / validations / refutations of 2607.10697; (c) precise claims of adjacent work; (d) Stage-I novelty pre-check (adding structural inequalities on critical-clause statistics to the recombination); (e) formal-verification / replication context.

Method note: every claim below carries a URL. "NOT FOUND" always means "not found by the logged searches on 2026-08-25", never "proven nonexistent".

---

## 1. Query log

All searches run 2026-08-25.

### 1.1 WebSearch queries (Claude Code WebSearch engine)

| # | Query | Outcome (relevant hits only) |
|---|-------|------------------------------|
| S1 | `"2607.10697"` | No relevant hits (bare arXiv IDs of this vintage are poorly indexed; unrelated numeric matches only) |
| S2 | `Jiang Cai PPSZ 3-SAT "better analysis"` | arXiv abs/pdf/html of 2607.10697; arXiv cs pastweek listing; Springer page for Scheder–Steinberger 2024. No third-party discussion |
| S3 | `"1.307031578"` | Only arXiv copies of 2607.10697 (abs/pdf/html). No other source uses this number |
| S4 | `"1.306969598"` | Only arXiv copies of 2607.10697 |
| S5 | `Hansen Kaplan Zamir Zwick "biased PPSZ" 3-SAT running time bound` | HKZZ STOC'19 PDF (people.csail.mit.edu), TheoretiCS 13222, arXiv:2207.11071, Springer s00037-024-00259-y |
| S6 | `Scheder Steinberger "PPSZ for general k-SAT" CCC 2017 3-SAT faster bound 1.32153` | DROPS LIPIcs.CCC.2017.9 page; dl.acm.org 10.5555/3135595.3135604; Springer/DNB copies. (The 1.32153 probe number was not confirmed anywhere; treated as not a real attribution) |
| S7 | `"biased PPSZ" erratum OR correction OR flaw OR bug Hansen Kaplan Zamir Zwick` | **No erratum/correction/retraction found.** Surfaced Qin–Watanabe IEICE 2022 improvement of biased-PPSZ (jstage) |
| S8 | `3-SAT algorithm improvement 2026 randomized worst-case bound` | Only 2607.10697 for 2026; rest are 2001–2011 classics |
| S9 | `PPSZ 2026 new bound improvement k-SAT` | Nothing 2026 beyond JC; SS 2024 journal copies; d-nb.info free copy of SS 2024 |
| S10 | `"PPSZ" 3-SAT reddit OR blog OR hackernews 2026 Jiang Cai 1.307` | **No blog/Reddit/HN discussion found**; only unrelated cybersecurity news |
| S11 | `scottaaronson.blog OR cstheory.stackexchange.com PPSZ 3-SAT best known bound 2026` | No Aaronson/StackExchange discussion found; arXiv copies of JC only |
| S12 | `"critical clause" graph indegree PPSZ analysis structural inequality` | Only the Scheder line (2207.11071, TheoretiCS 13222), JC 2026, Impatient PPSZ (2109.02795), HMS 2010 (1009.4830), Hertli 2014 (1311.2513) |
| S13 | `PPSZ "TwoCC" OR "two critical clauses" OR "sibling graph" Scheder analysis` | ECCC TR21-069 (orig + revision 1 downloads), FOCS 2021 PDF, arXiv:2207.11071, JC 2026. No other users of these statistics |
| S14 | `PPSZ formalization Lean OR Isabelle OR Coq SAT algorithm verified proof` | **No PPSZ formalization found**; only DPLL/CDCL solver verifications (Marić–Janičić, IsaFoL/Blanchette et al., Lescuyer–Conchon, Dafny DPLL) |
| S15 | `"critical clause tree" PPSZ 2026 improved analysis recombination` | Only the known line (PPSZ, Scheder versions, HMS 2010, Hertli 2014, Impatient PPSZ, AGR 2025, JC 2026) |
| S16 | `"Unique 3-SAT" new bound 2025 OR 2026 algorithm faster` | Nothing newer than JC; Hertli 2011/2014 records |
| S17 | `"1.306984" OR "QW-PPSZ"` | Only Qin–Watanabe IEICE 2022 itself (+ their 2018 Hertli-improvement paper on ResearchGate) |
| S18 | `biased PPSZ improvement 2023 OR 2024 OR 2025 3SAT success probability` | **No post-2022 continuation of the biased-PPSZ line found** |
| S19 | `"1.306972377" OR "1.307031594"` | Only arXiv copies of 2607.10697. These digit strings appear nowhere else on the indexed web |

### 1.2 Direct fetches (WebFetch / curl; arXiv API; OpenAlex; GitHub API)

| # | URL | Purpose / outcome |
|---|-----|-------------------|
| F1 | https://arxiv.org/abs/2607.10697 | Submission history: **"[v1] Sun, 12 Jul 2026 10:40:39 UTC (13 KB)"** — v1 only, no v2, no Comments field, cs.DS |
| F2 | https://api.semanticscholar.org/graph/v1/paper/arXiv:2607.10697?fields=... | HTTP 429 (rate-limited) on 5 attempts spread over the session (WebFetch ×1, curl ×4). Citation data taken from OpenAlex instead |
| F3 | https://export.arxiv.org/api/query?search_query=all:PPSZ&sortBy=submittedDate&sortOrder=descending&max_results=40 | 11 PPSZ papers total; **newest = 2607.10697 (2026-07-12)**; next: 2505.06146 (AGR), 2207.11071 (Scheder), 2109.02795 (Impatient PPSZ), 2007.07040, 2001.06536, 1611.01291, 1311.2513, 1103.2165, 1009.4830, 0801.3147 |
| F4 | https://export.arxiv.org/api/query?search_query=all:%223-SAT%22+AND+cat:cs.DS&... (30 newest) | Newest worst-case-upper-bound paper = JC; no competing 2025–2026 3-SAT upper-bound work (rest: random 3-SAT physics, sparsification, #SAT counting, NP-hardness applications) |
| F5 | https://export.arxiv.org/api/query?search_query=all:%223-SAT%22+AND+cat:cs.CC&... (25 newest) | Same: no competing upper-bound work 2024-08 → 2026-08 |
| F6 | https://arxiv.org/html/2607.10697 and https://arxiv.org/pdf/2607.10697 (full 15-page read) | Full claims, references, appendices; see §2.1 |
| F7 | https://arxiv.org/abs/2505.06146 | AGR v1 2025-05-09, v2 2025-05-30; abstract quoted §2.4 |
| F8 | arXiv:2505.06146v2 PDF pp. 1–4 | Exact related-work sentence on the 3-SAT frontier; quoted §2.4 |
| F9 | https://theoretics.episciences.org/13222/pdf pp. 1–8 (Scheder, TheoretiCS 2024) | Received 2022-07-25, revised 2023-10-19, accepted 2024-02-04, published 2024-03-13; quotes in §2.3 |
| F10 | https://people.csail.mit.edu/virgi/6.s078/papers/fasterksat.pdf pp. 1–3 (HKZZ STOC 2019) | Abstract + §1.2 + footnote 1 quoted in §2.2 |
| F11 | https://link.springer.com/article/10.1007/s00037-024-00259-y | 303 redirect to idp.springer.com (paywall); used DNB free copy instead |
| F12 | https://d-nb.info/1357042876/34 pp. 1–2 (SS, comput. complexity 33:13, 2024) | Published online 2024-11-04; abstract quoted §2.5; TOC confirms "Main Theorem 1.17" (as cited by JC) |
| F13 | https://drops.dagstuhl.de/opus/volltexte/2017/7535 (SS, CCC 2017) | Abstract quoted §2.5 |
| F14 | https://ieee-focs.org/FOCS-2021-Papers/pdfs/FOCS2021-5stbVHiOp5jRHWlSl41FkR/205500a205/205500a205.pdf pp. 1–3 | Scheder FOCS 2021; Theorem 6 and HKZZ passage quoted §2.3 |
| F15 | https://eccc.weizmann.ac.il/report/2021/069/ | ECCC TR21-069: original 2021-05-12, Revision #1 2021-10-15; unique bound O(1.306973^n) |
| F16 | https://www.jstage.jst.go.jp/article/transinf/E105.D/3/E105.D_2021FCP0009/_article and .../_pdf pp. 1–2 | Qin–Watanabe IEICE 2022; Table 1 quoted §2.6 |
| F17 | https://arxiv.org/abs/1311.2513 | Hertli 2014 (v1 2013-11-11, v2 2014-02-17); abstract quoted §2.7 |
| F18 | https://arxiv.org/abs/1103.2165 | Hertli 2011 (v1 2011-03-10, v2 2011-05-05); abstract quoted §2.7 |
| F19 | https://arxiv.org/abs/2109.02795 | Impatient PPSZ (Li–Scheder): improvement only for (d,k)-CSP with **d ≥ 3**; explicitly not boolean 3-SAT |
| F20 | https://api.openalex.org/works/doi:10.48550/arXiv.2607.10697 | W7168276266: **cited_by_count: 0**; type preprint; no institutional affiliations recorded. Duplicate record W7168432810 (arXiv PMH route) also cited_by_count: 0 |
| F21 | https://api.github.com/repos/jiangxioabai/A-Better-Analysis-For-PPSZ (+ /forks, /contents) | Created 2026-07-12T08:25:04Z, pushed 2026-07-12T08:27:55Z (never touched since); **0 stars, 0 forks, 0 issues**; files: README.md (1777 B), ppsz_certificate.json (1723 B), verification_output.txt (2336 B), "verify_ppsz_constants(1) (1).py" (14859 B) |
| F22 | https://dblp.org/search?q=A+Better+Analysis+For+PPSZ | Single record: CoRR abs/2607.10697 (informal publication). **No conference/journal version** |

---

## 2. Findings with sources and exact quotes

### 2.1 The audited paper (JC), first-hand from the PDF

Source: https://arxiv.org/abs/2607.10697 / https://arxiv.org/pdf/2607.10697 (v1, 2026-07-12; 15 pp.; only reference list entries: Attias–Gao–Reyzin; PPSZ JACM 2005; Scheder FOCS 2021, ECCC TR21-069, TheoretiCS 2024; Scheder–Steinberger comput. complexity 2024).

- Abstract table: Scheder's analysis — Unique-3-SAT O*(1.306972377^n), general O*(1.307031594^n); this work — Unique O*(1.306969598^n), general O*(1.307031578^n).
- Frontier claim (abstract): "To the best of our knowledge, O*(1.307031578^n) is the best currently known worst-case randomized running-time bound for general 3-SAT."
- Basis for the claim (p. 3): "Scheder and Steinberger identify PPSZ as the fastest known algorithm for k-SAT, and a recent account likewise treats Scheder's PPSZ analysis as the state of the art for worst-case 3-SAT [6, 1]. Since Corollary 1.2 strictly lowers that general-3-SAT base, it gives the best currently known worst-case randomized running-time bound for general 3-SAT."
- Scheder's published unique bonus (p. 1): gamma_old = 1/15218 = 0.000065711657247995..., "with unrounded base 1.306972376565153...". JC's new bonus: gamma_new = 0.0000687793 (certificate value gamma_* = 0.000068779380458836...).
- The "old" general number is JC's own computation, not Scheder's: p. 3, "Applying the same lifting calculation to the old and new unique-case bonuses gives the following limiting values" — old lifted bonus 0.0000003465837065 → base 1.307031593709762...; new 0.0000003640269421 → 1.307031577906796.... Corollary 1.2 uses eta = 0.000000364, final "2^{p0−0.000000364} = 1.307031577931205... < 1.307031578" (p. 9).
- Coordinates and inequalities (pp. 2–5): coordinates i0 = |ID_0|/n, i1 = |ID_1|/n, tau = |TwoCC|/n (indegree classes of the critical-clause graph; TwoCC = variables with ≥ 2 critical clauses). Structural inequalities used: (10) (18/17)|H_low| + 2|H_high| + 3|TwoCC| ≥ |H| and (11) |H| ≥ n − |ID_1| − 2|ID_0| − 2|TwoCC|, with the explicit statement: "Both inequalities are imported from Scheder's analysis." The new step is only the recombination: a 3-variable LP with dual certificate (Proposition 3.1).
- Non-optimality admission (p. 7): "We do not assert that this point is realized by a formula or that the displayed parameters are globally optimal once all structural constraints are imposed." Appendix A: "No optimality claim is made for the search."
- Repository (p. 11, footnote): https://github.com/jiangxioabai/A-Better-Analysis-For-PPSZ ; certificate version "2026-07-12-rational-v6"; files ppsz_certificate.json / verify_ppsz_constants.py / verification_output.txt.
- **Notable omission:** the paper cites neither Hertli (2011 or 2014), nor Hansen–Kaplan–Zamir–Zwick (STOC 2019), nor Qin–Watanabe (2018/2022). The "best currently known" claim is argued only against the Scheder/SS line plus the AGR remark.
- Acknowledgments: "We thank Shiteng Chen for helpful discussions."

### 2.2 HKZZ (biased PPSZ), STOC 2019 — the crucial unique-vs-general question

Source: https://people.csail.mit.edu/virgi/6.s078/papers/fasterksat.pdf (also https://dl.acm.org/doi/10.1145/3313276.3316359).

- Abstract: "For 3-SAT, a tiny improvement over PPSZ was obtained by Hertli. We introduce a biased version of the PPSZ algorithm using which we obtain an improvement over PPSZ for every k ≥ 3. For k = 3 we also improve on Herli's result and get a much more noticeable improvement over PPSZ, though still relatively small. **In particular, for Unique 3-SAT, we improve the current bound from 1.308^n to 1.307^n.**"
- Footnote 1 (p. 579): "With a slight 'tongue in cheek'. The base of the exponent of PPSZ is 1.30703... **Our current base is 1.30699...**"
- §1.2 (p. 579): "The improvement we obtain is for Unique k-SAT. **By [15], this implies some improvement also for k-SAT.**" ([15] = Scheder–Steinberger.) — i.e., the general-3-SAT consequence is asserted qualitatively, **never quantified**.
- §1.2: "The tighter analysis for NAE-3-SAT giving a bound of 1.305^n for Unique NAE-3-SAT, and the 1.307^n bound for Unique 3-SAT are deferred to the full version of the paper."
- Context quotes for the frontier table (p. 578): "[PPSZ] showed that c_3 ≤ 1.364 and c_k ≤ 2^{1−(1−o(1))·π²/6k}. They also showed that their 3-SAT algorithm runs in 1.308^n time, if the formula has a unique satisfying assignment"; "Hertli [3] extended the analysis of PPSZ to show that the bound obtained by PPSZ under the uniqueness assumption also holds for the general case, i.e., c_3 ≤ 1.308."
- On Hertli 2014 and the earlier Qin–Watanabe: "Hertli's improvement ... can be improved by about 10^{−24}, i.e., by a tiny bit" (p. 579); "(Qin and Watanabe [12] tried to push Herli's ideas to the limit and only obtained a 10^{−19} improvement.)" (p. 580).
- **No erratum/correction/retraction of HKZZ found** (query S7). The precise base 1.306995 attributed to HKZZ appears in Scheder's papers (below), consistent with HKZZ's own "1.30699...".

### 2.3 Scheder, "PPSZ is better than you think" (FOCS 2021 / ECCC TR21-069 / TheoretiCS 2024)

Sources: FOCS PDF https://ieee-focs.org/FOCS-2021-Papers/pdfs/FOCS2021-5stbVHiOp5jRHWlSl41FkR/205500a205/205500a205.pdf (DOI 10.1109/FOCS52979.2021.00028); ECCC https://eccc.weizmann.ac.il/report/2021/069/ (orig. 2021-05-12; Revision #1 2021-10-15); TheoretiCS https://theoretics.episciences.org/13222/pdf (vol. 3, art. 5, 2024, DOI 10.46298/theoretics.24.5).

- FOCS abstract: "For Unique-3-SAT we bound its running time by **O(1.306973^n)**, which is somewhat better than the algorithm of Hansen, Kaplan, Zamir, and Zwick."
- FOCS Theorem 6: "The success probability of PPSZ on 3-CNF formulas with a unique satisfying assignment is at least 1.306973^{−n}." — and "Our improvement for Unique 3-SAT is roughly fifty percent larger than that of Hansen, Kaplan, Zamir, and Zwick [8]."
- FOCS/TheoretiCS on HKZZ (identical in substance; TheoretiCS p. 5): "More recently, Hansen, Kaplan, Zamir, and Zwick [3] published an algorithm called biased-PPSZ ... In contrast to Hertli's, their improvement is 'visible': **for 3-SAT, it improves the success probability from 1.3070319^{−n} in Theorem 1.3 to 1.306995^{−n}**. Also, it works for all k (although the authors do not work out the exact magnitude of the improvement)." — Note this appears under the heading "Improved algorithms. Concerning the Unique-SAT case, ...": the 1.306995 is a **Unique-3-SAT** figure.
- General case in this line is qualitative only: FOCS Theorem 5 / TheoretiCS Theorem 1.5 ("for every k ≥ 3 there is eps_k > 0 such that the success probability of PPSZ on satisfiable k-CNF formulas is at least 2^{−n(1−s_k−eps_k)}") plus the lifting theorem (TheoretiCS Theorem 1.4): "If the success probability of PPSZ is at least 2^{−n+s_k n+eps n} on k-CNF formulas with a unique satisfying assignment, for some eps > 0, then it is at least 2^{−n+s_k n+eps' n} on k-CNF formulas with multiple solutions, too, for some (smaller) eps' > 0." **No explicit general-3-SAT base is published anywhere in the Scheder papers.**
- The journal version dropped the numeric k=3 part: TheoretiCS §1.4: "The full version of Hansen et al. and the ECCC version of this result [13] invest considerable energy to hammer out a concrete numerical result ... the analysis for k = 3 in [13] does not hit any natural wall, and therefore a simple tightening of inequalities and a better choice of constants and functions would already yield a better bound. **We therefore decided not to include the k = 3 part in this paper.**" — i.e., Scheder himself states in print (2024) that his 3-SAT constant is not tight; JC's improvement is exactly such a tightening.
- Comparison to HKZZ (TheoretiCS p. 6): "I suspect that one can combine two approaches and get improved numbers for small k, like k = 3; however, I fear that doing so would be extremely tedious and barely offer any additional insight." — an explicitly flagged open direction that neither JC nor anyone else has executed (per queries S12–S18).

### 2.4 Attias–Gao–Reyzin (arXiv:2505.06146) — the "recent account"

Source: https://arxiv.org/abs/2505.06146 (v1 2025-05-09, v2 2025-05-30); PDF v2.

- Abstract: "...we accelerate the exponential running time of the PPSZ family of algorithms due to Paturi, Pudlak, Saks and Zane, **which currently represent the state of the art in the worst case**."
- Related work, §1.3 "SAT" (p. 4), exact frontier sentence: "Hertli [Her14a, Her14b] improved the analysis of PPSZ, which was later simplified by Scheder and Steinberger [SS17] and slightly improved by Qin and Huang [QW20]. A variant of PPSZ, named biased PPSZ, was introduced by Hansen, Kaplan, Zamir, and Zwick [HKZZ19], and **an improved analysis of PPSZ by Scheder [Sch24] currently represents the state of the art, with 1.307^n for 3-SAT**." (Note: "Qin and Huang" is evidently a misnomer for Qin–Watanabe.)
- §2 (p. 4): "According to [Her14a, SS17, Sch24], Unique-k-SAT bounds can be lifted to general k-SAT..."
- So AGR (May 2025) confirm the pre-JC frontier exactly as JC portray it: Scheder's analysis, ≈1.307^n, for (general) 3-SAT.

### 2.5 Scheder–Steinberger (CCC 2017; comput. complexity 2024) — the lifting theorem

Sources: https://drops.dagstuhl.de/opus/volltexte/2017/7535 (LIPIcs CCC 2017); free journal copy https://d-nb.info/1357042876/34 (comput. complex. 33:13, 2024, published online 2024-11-04, DOI 10.1007/s00037-024-00259-y).

- CCC 2017 abstract: "...Second, we show a 'translation result': if you improve PPSZ for k-CNF formulas with a unique satisfying assignment, you will immediately get a (weaker) improvement for general k-CNF formulas. Combining this with a result by Hertli from 2014, in which he gives an algorithm for Unique-3-SAT slightly beating PPSZ, **we obtain an algorithm beating PPSZ for general 3-SAT, thus obtaining the so far best known worst-case bounds for 3-SAT**." — no explicit number.
- Journal 2024 abstract: "In combination ... with results by Hansen et al. (... STOC 2019) and Scheder (... FOCS 2021), who all prove improved time bounds for Unique-k-SAT, this gives improved bounds for general k-SAT." — again no explicit number. TOC confirms "Main Theorem 1.17" and a "Unique to general" section (§3.1), matching JC's citations (JC Imported Theorem 4.1 = SS Main Theorem 1.17; JC cite "Lifting Theorem 1.18").
- Consequence for the audit: from 2017 to 2026, every general-3-SAT statement in the SS/Scheder/HKZZ line below base 2^{2ln2−1} ≈ 1.3070320 was **qualitative** ("some improvement"). JC's Corollary 1.2 (and their own re-computation of the "old" 1.307031594) are, per these searches, the first explicit general-3-SAT decimals below 1.3070319.

### 2.6 Qin–Watanabe, IEICE Trans. Inf. & Syst. E105-D(3):481–490, 2022

Source: https://www.jstage.jst.go.jp/article/transinf/E105.D/3/E105.D_2021FCP0009/_article (DOI 10.1587/transinf.2021FCP0009; PDF read).

- Summary: "Hansen, Kaplan, Zamir and Zwick (STOC 2019) introduced a systematic way to use 'bias' ... and showed that their biased PPSZ algorithm achieves a relatively large success probability improvement of PPSZ **for Unique 3SAT**. We propose an additional way to use 'bias' and show **by numerical analysis** that the improvement gets increased further."
- Table 1 ("Comparison of exponential coefficients ... for solving **Unique 3SAT**"): Naive 1.0 → 2; PPSZ 0.386295 → 1.307031; Biased PPSZ (HKZZ) 0.386254 → 1.306995; **QW-PPSZ 0.386241 → 1.306984**.
- p. 482: "As shown by Scheder and Steinberger [9], a certain amount of efficiency improvement is guaranteed on the general 3SAT if there is any exponential efficiency improvement on Unique 3SAT." — again qualitative for general.
- Status vs JC: 1.306984 (unique, modified algorithm, numerical-grid analysis) is worse than Scheder's 1.306973 and JC's 1.306969598. It does not touch the general-3-SAT record. No follow-up after 2022 found (S18).

### 2.7 Hertli (2011, 2014) — for the frontier table

- Hertli 2011, arXiv:1103.2165 (v2 2011-05-05; FOCS 2011; SICOMP 43(2):718–729 as "3-SAT Faster and Simpler—Unique-SAT Bounds for PPSZ Hold in General", https://epubs.siam.org/doi/10.1137/120868177): abstract: "This improves our previous best bounds with Moser and Scheder [2011] for 3-SAT to **O(1.308^n)** and for 4-SAT to O(1.469^n)." (Rounded; the precise base is 2^{2ln2−1} = 1.3070319..., as used by Scheder and JC.)
- Hertli 2014, arXiv:1311.2513 (v2 2014-02-17; "Breaking the PPSZ Barrier for Unique 3-SAT", ICALP 2014): abstract: "We give an improved algorithm with **exponentially faster bounds for Unique 3-SAT**." — no explicit constant; HKZZ (p. 579) quantify it as "about 10^{−24}"; the earlier Qin–Watanabe push got "a 10^{−19} improvement" (HKZZ p. 580).

### 2.8 Follow-ups / uptake of 2607.10697 (as of 2026-08-25)

- arXiv: v1 only (2026-07-12); no v2, no withdrawal, no Comments field (F1).
- Citations: OpenAlex cited_by_count = 0 on both records (F20). Semantic Scholar API rate-limited (HTTP 429) on all 5 attempts — citation count there unverified.
- dblp: CoRR record only; no conference/journal version (F22).
- GitHub: author repo created and last pushed 2026-07-12; 0 stars, 0 forks, 0 issues; 4 files (F21). **No independent replication repository found** (S2, S10, S14).
- No blog, Reddit, Hacker News, cstheory.SE, or SAT-community discussion found (S10, S11).
- No independent verification, refutation, or improvement found (S3, S4, S8, S9, S15, S16, S19).

### 2.9 Stage-I novelty pre-check (structural inequality on critical-clause statistics in the recombination)

- The coordinate vocabulary (critical-clause graph, indegree classes J_i/ID_i, TwoCC, sibling graph H, H_low/H_high) originates in Scheder's full version (ECCC TR21-069 §§6–8; TheoretiCS journal version) — see S12/S13 hits; JC's Table (p. 4) maps their symbols to "Section 6 / Section 7 / Sections 6–8 / Section 8" of Scheder's full version.
- JC use exactly two structural inequalities, both imported: "(18/17)|H_low| + 2|H_high| + 3|TwoCC| ≥ |H|" (Scheder's sibling-graph construction, Scheder Eq. (11)) and "|H| ≥ n − |ID_1| − 2|ID_0| − 2|TwoCC|" (from Scheder's Lemma 34); "Both inequalities are imported from Scheder's analysis" (JC p. 5).
- JC explicitly disclaim optimality of their point/parameters "once all structural constraints are imposed" (p. 7) — i.e., adding further structural constraints to the recombination is an open, un-executed direction.
- Adjacent prior art that exploits critical-clause structure by *other means* (not by adding inequalities to a recombination LP): Hertli–Moser–Scheder 2010 "Improving PPSZ for 3-SAT using Critical Variables" (https://arxiv.org/abs/1009.4830); Hertli 2014 (https://arxiv.org/abs/1311.2513); HKZZ 2019 biased guessing keyed to critical-clause counts; Li–Scheder "Impatient PPSZ" (https://arxiv.org/abs/2109.02795 — improvement only for (d,k)-CSP with d ≥ 3, "not boolean 3-SAT"); Qin–Watanabe 2022 (§2.6).
- **No paper found that adds a new critical-clause-statistics inequality to Scheder's (or JC's) recombination**, and no 2026 refinement of Scheder's analysis beyond JC found (S12, S13, S15, S9).

### 2.10 Formal verification context

- No Lean/Isabelle/Coq formalization of PPSZ or of any PPSZ running-time bound found (S14). Existing verified-SAT work is solver-correctness (DPLL/CDCL: Marić–Janičić; Blanchette et al. IsaFoL; Lescuyer–Conchon; a Dafny DPLL), not success-probability bounds.
- The only machine-checkable artifact tied to 2607.10697 is the authors' own exact-rational interval checker (repo in §2.8; certificate "2026-07-12-rational-v6"). It checks the recombination and lifting arithmetic only — JC p. 10: "It verifies the recombination and lifting arithmetic, **not the integrals or auxiliary numerical bounds underlying those estimates**."

---

## 3. Frontier table — best known randomized worst-case bounds for 3-SAT

Bases rounded as stated by the cited source. "expl." = explicit numeric base published; "qual." = qualitative (exponential improvement asserted, no constant).

| Work | Year/venue | Unique-3-SAT | General 3-SAT | Where stated |
|---|---|---|---|---|
| PPSZ (Paturi–Pudlák–Saks–Zane) | JACM 52(3), 2005 | 1.308^n (= 2^{(2ln2−1)n} = 1.3070319...^n) expl. | c_3 ≤ 1.364 expl. | HKZZ p. 578 ("runs in 1.308^n time, if ... unique"; "c_3 ≤ 1.364"), https://people.csail.mit.edu/virgi/6.s078/papers/fasterksat.pdf |
| Hertli | FOCS 2011 / SICOMP 2014 | (inherits PPSZ) | **O(1.308^n)** expl. (unique bound holds in general; precise 1.3070319...) | arXiv:1103.2165 abstract; https://epubs.siam.org/doi/10.1137/120868177 |
| Hertli | ICALP 2014 | "exponentially faster" than PPSZ, ≈10^{−24} qual. | via SS 2017 lifting: qual. only | arXiv:1311.2513 abstract; HKZZ p. 579 |
| Scheder–Steinberger | CCC 2017 / comput. complex. 33:13 (online 2024-11-04) | — (lifting tool) | "beating PPSZ for general 3-SAT ... so far best known" qual. | https://drops.dagstuhl.de/opus/volltexte/2017/7535 ; https://d-nb.info/1357042876/34 |
| Hansen–Kaplan–Zamir–Zwick (biased-PPSZ; modified algorithm) | STOC 2019 | **1.307^n headline; base 1.30699... (= 1.306995)** expl. | "some improvement" via SS qual. only | STOC PDF abstract, fn. 1, §1.2 (https://people.csail.mit.edu/virgi/6.s078/papers/fasterksat.pdf); 1.306995 attribution: Scheder FOCS 2021 p. 206 / TheoretiCS 2024 p. 5 |
| Scheder ("PPSZ is better than you think"; original algorithm) | FOCS 2021 / ECCC TR21-069 (rev. 1, 2021-10-15) | **O(1.306973^n)** expl. (Thm 6; bonus 1/15218, unrounded base 1.306972376565... per JC p. 1) | qual. only (Thm 5 + lifting); **no explicit base ever published by Scheder** | FOCS PDF pp. 205–207; https://eccc.weizmann.ac.il/report/2021/069/ |
| Scheder (journal) | TheoretiCS 3:5, 2024-03-13 | k=3 numeric part deliberately dropped (§1.4) | qual. only | https://theoretics.episciences.org/13222/pdf |
| Qin–Watanabe (QW-PPSZ; modified algorithm, numerical analysis) | IEICE E105-D(3), 2022 | **1.306984** expl. (Table 1; coeff 0.386241) | qual. only (via SS) | https://www.jstage.jst.go.jp/article/transinf/E105.D/3/E105.D_2021FCP0009/_article |
| Attias–Gao–Reyzin (frontier account, not a new bound) | arXiv 2505.06146v2, 2025-05-30 | — | "Scheder [Sch24] currently represents the state of the art, with 1.307^n for 3-SAT" | arXiv:2505.06146 p. 4 |
| **Jiang–Cai** | arXiv 2607.10697v1, 2026-07-12 | **1.306969598** expl. (Thm 1.1; gamma_new = 0.0000687793) | **1.307031578** expl. (Cor. 1.2; limiting base 1.307031577906796...); also computes "old" Scheder-lifted base **1.307031594** (1.307031593709762...) | https://arxiv.org/pdf/2607.10697 pp. 1–3, 9 |
| Anything newer (2026-07-12 → 2026-08-25) | — | none found | none found | arXiv API sweeps F3–F5; searches S8, S9, S15, S16 |

Ordering on the unique side (all published explicit bases): 1.3070319 (PPSZ) > 1.306995 (HKZZ) > 1.306984 (QW) > 1.306973 / 1.306972377 (Scheder) > **1.306969598 (JC)**. JC's Section 4 proves the lifted general bonus is strictly increasing in the unique bonus ("the lifted bonus is strictly increasing in the unique-case bonus", p. 9), so within the SS-lifting route the best general bound necessarily comes from the best unique bound — which is JC's own. HKZZ/QW, besides being unique-only and unquantified in the general case, feed a *weaker* unique bonus into any such lifting.

---

## 4. Verdicts

**V-a. JC's claim "O*(1.307031578^n) is the best currently known worst-case randomized running-time bound for general 3-SAT": SUPPORTED (high confidence, with two caveats).**
No source found stating any explicit randomized general-3-SAT base below 1.3070319... other than JC's own Corollary 1.2 (1.307031578) and JC's own reconstruction of the Scheder-lifted "old" base (1.307031594). Every prior sub-1.3070319 statement for general 3-SAT in the literature is qualitative (SS 2017/2024 "beating PPSZ ... best known"; HKZZ "some improvement also for k-SAT"; QW citing SS "a certain amount of efficiency improvement is guaranteed"). The independent 2025 account (AGR) puts the frontier at "Scheder [Sch24] ... 1.307^n". Monotonicity of the lifted bonus in the unique bonus means the weaker HKZZ/QW unique inputs cannot beat the Scheder/JC route even in principle via the same lifting. Caveats: (i) JC never cite or discuss HKZZ, Hertli, or Qin–Watanabe — the claim is true but the paper does not argue it against the modified-algorithm line at all; (ii) the "old" general base 1.307031594 attributed to "Scheder's analysis" in JC's abstract table is JC's own computation via their Proposition 4.2, not a number appearing in any Scheder/SS publication (searches for "1.307031594" hit only JC).

**V-b. Follow-ups, new versions, independent validations, or refutations of 2607.10697: NOT FOUND (high confidence in the negative result of the search; the paper is 6 weeks old).**
arXiv v1 only; 0 citations (OpenAlex; Semantic Scholar unverifiable, HTTP 429); dblp CoRR-only; author repo untouched since submission day with 0 stars/forks/issues; no independent replication repo; no blog/forum/community discussion found.

**V-c. Any randomized general-3-SAT bound with base < 1.307031578 (before or after JC): NOT FOUND (high confidence).**
The candidate confusions were checked directly: HKZZ's 1.306995 is a Unique-3-SAT figure (their own abstract: "for Unique 3-SAT, we improve the current bound from 1.308^n to 1.307^n"; Scheder places 1.306995 explicitly under "Concerning the Unique-SAT case"); QW's 1.306984 is likewise "for solving Unique 3SAT" (Table 1 caption); AGR's "1.307^n" is a rounding of the Scheder-region base, not a smaller number. Non-PPSZ randomized lines (Schöning-type local search and derandomizations) are all ≥ 1.32; nothing 2024–2026 in the arXiv cs.DS/cs.CC sweeps claims better. No post-JC improvement found.

**V-d. Prior art on adding critical-clause structural inequalities to the PPSZ recombination: NOT FOUND (moderate-to-high confidence).**
The only structural inequalities in any recombination found are Scheder's two (sibling-graph inequality and the Lemma-34 degree bound), which JC import verbatim; JC's contribution is the LP-dual recombination of the *existing* inequalities, and they explicitly disclaim global optimality "once all structural constraints are imposed". No paper adds a *new* inequality on critical-clause statistics (indegree classes, TwoCC, sibling-graph refinements) to improve the recombination, and no 2026 work refines Scheder's analysis beyond JC. The nearest adjacent art exploits critical-clause structure through algorithm modification (HKZZ bias, QW-PPSZ, Hertli 2014, HMS 2010 critical variables) or other domains (Impatient PPSZ, d ≥ 3 CSP only). Residual risk: unpublished/in-submission work, and the ECCC/TheoretiCS Scheder papers' internal machinery (Sections 6–8) contain more inequalities than the two surfaced in his final simplification — any "new" inequality must be checked against Scheder's full version, not only against JC.

---

## 5. Caveats and coverage limits

1. **Absence of evidence is not proof of absence.** All "NOT FOUND" verdicts are relative to the queries logged in §1 on 2026-08-25. Non-indexed venues (in-submission manuscripts, Chinese-language venues, Dagstuhl talks, mailing lists, very recent ECCC reports) may contain material these searches cannot see.
2. **Semantic Scholar could not be queried** (persistent HTTP 429 on the public API, 5 attempts). Citation absence rests on OpenAlex (cited_by_count = 0 on both records) and on the null results of the numeric-literal searches (S3, S4, S19). Google Scholar was not directly queryable by this tooling.
3. **Bare-ID search limitation:** the query `"2607.10697"` returns noise; discussion referring to the paper only by arXiv ID could be missed. Mitigated by title, author, and numeric-literal searches (S2, S3, S4, S10, S11, S19), all null.
4. **The paper is 6 weeks old.** Zero uptake is expected at this age and is weak evidence about correctness in either direction. The community (Scheder, Zamir, et al.) has visibly not yet reacted in public.
5. **JC's claim is about *published explicit* bounds.** A referee could still argue that HKZZ + SS lifting "implicitly" beats plain-PPSZ-based general bounds; the monotonicity argument (§3) closes this for the SS route, but a bespoke general-case analysis of biased-PPSZ (never written, per these searches) is not logically excluded.
6. **Numeric probes** used exact digit strings; a competing bound stated with different rounding (e.g., "1.30703") would only surface via the broader sweeps (S8, S9, S16, F3–F5), which were clean.
7. The generic single-token query "1.306" was not run (uninformatively broad); the specific frontier-relevant literals (1.307031578, 1.306969598, 1.306972377, 1.307031594, 1.306984, 1.306995-adjacent queries) were all covered.
