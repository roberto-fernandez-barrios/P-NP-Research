# Independent audit of ECCC TR26-007, Conjecture 1.4 / 4.2

**Audit status:** refuted as written.

**Scope and independence.** This audit was requested as an independent, blinded
check.  The auditor read the primary source but did not read another agent's
analysis or `literature/drafts/proof_sat.md` before deriving the construction
below.  A small finite enumeration was performed only after the parametric
construction had been derived.  This note does not audit the rest of the
paper.

**Primary source.** Yaroslav Alekseev and Nikita Gaevoy, *New
Polynomial-Depth Res(\(\oplus\)) Lower Bounds*, ECCC TR26-007 (2026),
[report page](https://eccc.weizmann.ac.il/report/2026/007/),
[PDF](https://eccc.weizmann.ac.il/report/2026/007/download).

## Statement audited

Conjectures 1.4 and 4.2 are the same claim.  In the notation of the paper, fix
constants \(r,q>0\).  Let \(\Phi_1,\ldots,\Phi_m\) be affine subspaces of
\(\mathbb F_2^n\), each of codimension at most \((\log n)^q\), and suppose

\[
  \left|\bigcup_{j=1}^m\Phi_j\right|\ge 2^{n-1}.
\]

For arbitrary subsets \(\Phi'_j\subseteq\Phi_j\) satisfying

\[
  |\Phi'_j|\ge (1-n^{-r})|\Phi_j|,
\]

the conjecture asserts that there is a constant \(c(q)>0\), depending only on
\(q\), such that

\[
  \left|\bigcup_{j=1}^m\Phi'_j\right|
  \ge (1-n^{-r c(q)})
       \left|\bigcup_{j=1}^m\Phi_j\right|.
\]

The paper invokes the conjecture for \(q>1\).  The construction below refutes
it for every fixed \(q>1\) and every fixed \(r>0\).  It even refutes a version
in which \(c\) is allowed to depend on both \(q\) and \(r\).

## Parametric counterexample

Fix \(q>1\), \(r>0\), and take all sufficiently large \(n\).  Put

\[
  t=\lceil r\log_2 n\rceil,
\]

so that \(2t+1\le n\) and \(t+1\le(\log n)^q\).  Write a vector in
\(\mathbb F_2^n\) as

\[
  (b,y,z)\in
  \mathbb F_2\times\mathbb F_2^{2t}
  \times\mathbb F_2^{n-2t-1}.
\]

Define the hyperplane

\[
  H=\{(b,y,z):b=0\}.
\]

For every \(t\)-element set \(A\subseteq[2t]\), define

\[
  S_A=\{(b,y,z): b=1\text{ and }y_j=0\text{ for every }j\notin A\}.
\]

Thus \(H\) has codimension one, while every \(S_A\) has codimension
\(t+1\le(\log n)^q\).  The number of subspaces is only

\[
  m=1+\binom{2t}{t}=n^{O(r)},
\]

so the failure does not require an unboundedly large or exponential-size
cover.

Let the marker layer be

\[
  L=\{(1,y,z): |y|=t\},
\]

where \(|y|\) is Hamming weight.  Prune the subspaces by setting

\[
  H'=H,
  \qquad
  S'_A=S_A\setminus L.
\]

### Local deletion bound

For a fixed \(A\), membership in \(S_A\) forces
\(\operatorname{supp}(y)\subseteq A\).  A point of \(S_A\) lies in \(L\)
only when \(|y|=t\), which forces \(y=\mathbf 1_A\).  Consequently,

\[
  S_A\cap L=
  \{(1,\mathbf 1_A,z):z\in\mathbb F_2^{n-2t-1}\}.
\]

Since \(|S_A|=2^{n-t-1}\) and
\(|S_A\cap L|=2^{n-2t-1}\),

\[
  \frac{|S_A\setminus S'_A|}{|S_A|}=2^{-t}\le n^{-r}.
\]

Nothing is deleted from \(H\).  Therefore every local pruning condition in
the conjecture is satisfied.

### Global loss

The subspaces cover at least half the cube already because they include
\(H\), whose size is \(2^{n-1}\).  More importantly, each point in \(L\) is
private to exactly one \(S_A\): if \(|y|=t\), then
\((1,y,z)\in S_A\) if and only if \(A=\operatorname{supp}(y)\).  The marker
coordinate \(b=1\) also keeps \(L\) disjoint from \(H\).  It follows exactly
that, with

\[
  U=H\cup\bigcup_{|A|=t}S_A,
  \qquad
  U'=H'\cup\bigcup_{|A|=t}S'_A,
\]

we have \(U'=U\setminus L\).  Now

\[
  |L|=\binom{2t}{t}2^{n-2t-1}.
\]

Using only \(|U|\le2^n\),

\[
  \frac{|U\setminus U'|}{|U|}
  =\frac{|L|}{|U|}
  \ge \frac{\binom{2t}{t}}{2^{2t+1}}
  =\Theta(t^{-1/2})
  =\Theta((\log n)^{-1/2}),
\]

where the middle asymptotic is the standard central-binomial-coefficient
estimate.  For every fixed \(c>0\),
\(\Theta((\log n)^{-1/2})>n^{-rc}\) for all sufficiently large \(n\).
Hence

\[
  |U'| < (1-n^{-rc})|U|,
\]

contradicting the proposed conclusion for every possible positive constant
\(c\).

## Smallest illustrative finite instance

Take \(t=1\) and omit the \(z\)-coordinates, so the ambient space is
\(\mathbb F_2^3\) with coordinates \((b,y_1,y_2)\):

\[
\begin{aligned}
H&=\{000,001,010,011\},\\
S_{\{1\}}&=\{100,110\},\\
S_{\{2\}}&=\{100,101\}.
\end{aligned}
\]

Delete \(110\) from \(S_{\{1\}}\) and \(101\) from \(S_{\{2\}}\).
Each nontrivial subspace loses one half of its points, but the union falls
from seven points to five, a loss of \(2/7\).  This is an illustration, not by
itself the asymptotic refutation.

Direct enumeration of the same construction for \(t=1,2,3,4,5\) gives:

| \(t\) | \(\binom{2t}{t}\) private fibers | \(|U|\) after suppressing common \(z\)-multiplicity | \(|U'|\) | global loss |
|---:|---:|---:|---:|---:|
| 1 | 2 | 7 | 5 | \(2/7\) |
| 2 | 6 | 27 | 21 | \(6/27\) |
| 3 | 20 | 106 | 86 | \(20/106\) |
| 4 | 70 | 419 | 349 | \(70/419\) |
| 5 | 252 | 1662 | 1410 | \(252/1662\) |

## Why overlap does not rescue the statement

The construction deliberately combines a heavily shared core with private
marker fibers.  The sets \(S_A\) overlap on all vectors whose \(y\)-support
has size below \(t\), but their weight-\(t\) fibers are private.  Each local
deletion spends only a \(2^{-t}\) fraction to erase its private fiber; across
the polynomially many subspaces those private fibers form an
\(\Omega(1/\sqrt{\log n})\) fraction of the global union.  Thus neither high
overlap nor restricting the number of subspaces to a polynomial repairs the
conjecture as stated.

## Consequence for the cited conditional result

Theorems 1.1 and 4.3 assume Conjecture 1.4/4.2 for \(q>1\).  This audit does
not refute those conditional implications, but it refutes their stated
combinatorial hypothesis in exactly that parameter regime.  Any repaired
hypothesis must add structural restrictions that forbid private-marker
fibers (or otherwise control overlap multiplicity); merely bounding
codimension and local deletion density is insufficient.
