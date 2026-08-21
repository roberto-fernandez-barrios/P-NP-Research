# Cycle-4 multi-RR exact finite certificates

These files certify exact two-copy results for the literal union of relabelled
corrected `RR_n` families at `n=22,24,26,28,30`.

Each JSON file stores:

* the two old-label-to-new-label permutations;
* the complete fixed-weight necklace and one-copy failure counts;
* an internal FNV-1a checksum of the sorted normalized failure masks;
* the exact common individual rejection count;
* the full induced literal-union-DAG rejection count;
* the number of acceptances attributable only to hybrid paths; and
* the literal rank profile and total distinct-subset count.

The companion failure file contains every rejected rotation-orbit
representative, in hexadecimal, preceded by one comment header.  Its rotations
are the complete normalized one-copy rejection set.  Coprimality
`gcd(n-1,n/2)=1` guarantees that every such fixed-weight orbit has size
`n-1`.

The deterministic verifier is
`experiments/cycle04_multi_rr_verify.py`.  It does not import the C++ search
program.  It freshly exhausts fixed-weight necklaces, reconstructs all
literal subsets and all inclusion-by-one edges, and searches the full induced
DAG on the exact intersection of individual-copy rejection sets.

Run from the repository root:

```powershell
python -B experiments/cycle04_multi_rr_verify.py
```

The complete run takes about one minute on the machine used for Cycle 4.
For a literal traversal of the full union DAG on every one of the 352,716
normalized `n=22` colors, without using the exact common-rejection shortcut,
run:

```powershell
python -B experiments/cycle04_multi_rr_verify.py --direct-full-dag-n22 certificates/cycle04_multi_rr/cycle04_multi_rr_n22.json
```

That independent direct check also returns zero rejections.
The SHA-256 manifest covers the ten primary JSON/text certificate files.  It
can be checked with:

```powershell
Get-Content certificates/cycle04_multi_rr/cycle04_multi_rr_SHA256SUMS.txt | ForEach-Object {
    $fields = $_ -split '  ', 2
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path certificates/cycle04_multi_rr $fields[1])).Hash.ToLower()
    if ($actual -ne $fields[0]) { throw "hash mismatch: $($fields[1])" }
}
```

These are finite certificates only.  They imply no all-`n` bound and do not
resolve O01.
