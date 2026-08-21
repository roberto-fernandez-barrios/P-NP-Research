# Disposition of the Cycle-5 final integration audit findings

**Audit:** `cycle05_final_integration_adversarial.md` (verdict at audit
time: NOT READY — one BLOCKER).  Every finding and the action taken:

| # | Severity | Finding | Action |
|---|---|---|---|
| D1 | BLOCKER | Cycle-5 certificate payloads were CRLF in the working tree while `core.autocrlf=true` and no `.gitattributes` coverage existed; committed LF blobs would not match the SHA manifest | Fixed: `/certificates/cycle05_hybrid/** text eol=lf` added to `.gitattributes`; all five payloads normalized to LF; manifest regenerated over LF bytes; verified `sha256sum -c` OK **and** every staged index blob's SHA-256 equals its manifest entry |
| C1-m1 | MINOR | Stale sentence "the pair-swap regime is genuinely open" in `switch_structure_theory.md` §6 contradicted Theorem E | Fixed: paragraph rewritten to state the actual coverage map (A/E unconditional, C/F conditional, open = `t ≥ 3` far-and-deep + ∞-moving) |
| C1-m2 | MINOR | Transposition `D_mid ≤ 1` presented as proved/exact in summaries while the source labels the all-`q` bound PROOF CANDIDATE | Fixed in `results/research_cycle_05.md` §3 and `RESEARCH_STATE.md`: machine-exact for `q ≤ 21`; all-`q` bound labeled proof candidate, used qualitatively |
| C2-m1 | MINOR | Prose figure "87.5%" (×4) matched no artifact (exact range 85.7–87.9%) | Fixed in results, state, and both affected `failure_knowledge.jsonl` entries |
| C2-m2 | MINOR | The `t = 3` headline (3 of 20,058,300; 308/305) had no stored artifact; `n = 42` triple figures unreproducible from stored data | Fixed: `experiments/cycle05_triple_probe.py` added (defines the shifted pair-swap explicitly; exhaustive `n = 28`, fixed-seed sampled `n = 42`); output stored as `certificates/cycle05_hybrid/triple_probe.json` (values reproduce the audit's own reproduction exactly: 308/305/3 and 6342/6026); manifest extended |
| C5-m1 | MINOR | README/STATE artifact indexes omitted the novelty audit, ∞-probe script/JSON, and barrier audit | Fixed: all added to `research_cycle_05/README.md` and `RESEARCH_STATE.md` |
| C5-m2 | MINOR | README's `n = 22` reproduction command pointed `--out` at the stored annotated certificate | Fixed: command now targets a scratch path with an explicit warning |

No mathematical content changed in any fix.  With D1 resolved and all
MINOR items addressed, the audit's stated condition for readiness ("Fix
D1 and the tree is commit-ready") is met.
