# Cycle-4 RR acceptance certificates

This directory is reserved for exact output of
`experiments/cycle04_rr_necklace_count.cpp`.  Each JSON summary counts
sign-reversal-normalized balanced finite words, and each corresponding text
file contains one lexicographically least representative of every rejected
rotation orbit.

The producer enumerates fixed-density necklaces rather than all balanced
words.  `experiments/cycle04_rr_verify_counts.py` independently reconstructs
the interval recurrence, checks every stored representative and statistic,
checks the full literal induced subset DAG through `n=12`, and optionally
performs an independent exact necklace recount.

The committed range is `n=22,24,...,34`.  The full independent Python
recount was run through `n=30`; the faster C++ enumeration produced the
`n=32,34` counts, after which the Python checker verified every listed
failure, every orbit/run statistic, and the exact literal-family recurrence.
`SHA256SUMS.txt` freezes the certificate payloads.

From the repository root, a reproduction on a C++17 compiler is:

```powershell
g++ -O3 -std=c++17 experiments\cycle04_rr_necklace_count.cpp -o cycle04_rr_count.exe
.\cycle04_rr_count.exe 22 34 certificates\cycle04_rr_acceptance
python -B experiments\cycle04_rr_verify_counts.py
python -B experiments\cycle04_rr_verify_counts.py --skip-literal-equivalence --recount-through 30
```

The JSON `runtime_seconds_informational` field is non-canonical and will
naturally change on a reproduction; the mathematical integer fields and
failure lists are deterministic.
