# Clean-room derivation log for Theorem CR

This note was frozen before reading the Cycle-7 proof or hostile-review
artifacts and before implementing the finite validator.  The only Cycle-7
material consulted for the construction was the raw statement/definition in
`research_cycle_07/corner_realizability.md`, lines 22--123.  The proof section
starting at line 124, the Cycle-7 audits, and the two prohibited validators
were not consulted.

## Raw construction transcribed

Work in `Z/nZ`.  Put

* `b = floor(n/3)+1` and `jmax = floor((n-3)/2)`;
* for `m>0`, `p_i=floor(i*n/m)`, `s_i=p_i-b`;
* choose the least `d` in
  `[2,min(floor(n/m)-2,jmax-b)]` for which `Q=P+d` is disjoint from
  `P` and `S=P-b`, and from `S+1` and `S-1`;
* `g(x)=x+b`, except that `g(s_i)=p_i+d`.

There is one critical clause

`C_x=(x or not(x+1) or not(g(x)))`

per variable.  Let `A` be the undirected projection of the two arcs
`x -> x+1` and `x -> g(x)`.  The pairs variant adds every positive pair
whose two vertices are not adjacent in `A`; the triples variant adds every
positive triple independent in `A`.  For `m=0`, the natural separately
defined case is `g(x)=x+b` with no exceptional sources.

## Independent parameter and degree derivation

Write `n=a*m+r`, `0<=r<m`; then `a=floor(n/m)>=10`.  For every cyclic
index difference `k`, the elements of `P-P` having that index difference
are among

`floor(k*n/m), ceil(k*n/m)` modulo `n`.

Thus the positive nonzero circular spacings in `P-P` are at least `a`.
Every candidate `d<=a-2` automatically makes `P+d` disjoint from `P`.
The other three conditions fail only if, for some `k`,

`d in {Delta-b-1, Delta-b, Delta-b+1}`,

where `Delta` is one of the (at most two consecutive) values belonging to
that `k`.  Hence one `k` forbids at most four consecutive integers.  The
expanded four-integer forbidden blocks for consecutive `k` have their
left endpoints separated by at least `a`.  Since the candidate interval is
contained in `[2,a-2]`, at most one such block intersects it: if a block
with coordinate `c` intersects the left endpoint then `c>=0`, while its
successor can intersect the right endpoint only if `c<=-1`.  Consequently
at most four candidate values are forbidden.  Once `jmax-b>=6`, all five
values `2,...,6` are candidates, so a valid least `d` exists and `d<=6`,
uniformly in `m<=n/10`.

The baseline map `x -> x+b` is bijective.  Removing the sources `S`
removes exactly the image set `P`; inserting the exceptional images adds
exactly `Q`.  Since `P` and `Q` are disjoint, the `g`-arc indegrees are
zero on `P`, two on `Q`, and one elsewhere.  The `+1` arcs add one
everywhere.  Hence precisely the `m` vertices in `P` have indegree one,
the `m` vertices in `Q` have indegree three, and all others have indegree
two.  This reasoning does not require `P` and `S` to be disjoint.

For sufficiently large `n`, `b>=2`, `b+d<n/2`, so both children of every
vertex are distinct from the parent and from each other.  Every critical
clause therefore has three distinct literals.

## Independent uniqueness reduction

For an assignment, let `Z` be its set of zero variables.  A critical
clause at `x in Z` is satisfied exactly when at least one out-neighbor of
`x` also lies in `Z`.  Therefore every nonempty satisfying `Z` contains a
directed cycle.

In the pairs variant, the positive clauses say that `Z` must be a clique
of `A`.  Thus uniqueness is equivalent to every directed cycle containing
a nonedge pair.

In the triples variant, the positive clauses say `alpha(A[Z])<=2`.
Thus uniqueness is equivalent to every directed cycle containing an
independent triple.  This equivalence is exact in both directions: a
directed cycle with no forbidden auxiliary subset is itself the zero set
of a second satisfying assignment.

The directed step sizes are `1`, `b`, and `b+d`.  Put
`c=3*b-n`, so `1<=c<=3`.  If a directed cycle of length `ell<=17` has
`r` long edges, exceptional-offset sum `E`, `u=ell-r` unit edges, and
winding number `k`, then

`r*b+E+u=k*n`.

If `r>=3*k`, the left side is strictly greater than or equal to `k*n`
(strictly greater in the equality case), impossible.  Thus
`h=3*k-r>=1`, and

`E+u=h*b-k*c >= b-k*c`.

But `E+u<=ell*(d+1)`.  Moreover, when `d<=6`, every step is at most
`b+d<=n/3+7`, so for `n>357` a cycle of length at most 17 has total
step sum strictly below `6n`; hence `k<=5`.  Thus a short cycle forces
`b<=17*(d+1)+15=17*d+32`, and therefore
`n<=51*d+96`.  Since the parameter argument gives `d<=6`, every
`n>402` has directed girth greater than 17.

For these same bounds, the undirected graph `A` has no triangle.  A
triangle would give a signed modular relation among three lengths from
`{1,b,b+d}`.  With zero long terms, a signed sum of three units is odd
and nonzero.  With one long term its absolute value cannot be zero and
is below `n`.  With two long terms, equal signs give magnitude at most
`2(b+d)+1<n`, while opposite signs leave one of `0,d,-d`, changed by
one; this is nonzero because `d>=2`.  With three long terms, equal signs
give a value strictly between `n` and `2n` (`3b>n` and
`3(b+d)<=n+21`), while the two-against-one case has magnitude in
`[b-d,b+2d]`, strictly between zero and `n`.  No signed sum is therefore
zero modulo `n`.  Directed 2-cycles and loops are excluded because two
positive steps total less than `n` and every step lies in `(0,n)`.

The CCG has outdegree two and indegree at most three, so `Delta(A)<=5`.
A directed cycle of length at least 18 therefore has an independent set
of size at least `ceil(18/6)=3` by the greedy bound.  This proves unique
satisfiability of the triples variant.  Triangle-freeness plus absence of
loops and directed 2-cycles proves it for the pairs variant.

## Independent closure analysis plan

The primary-source text of Scheder Definition 31 says that `F~` is `F`
plus all 3-clauses inferable from pairs of 3-clauses *of F*.  This is
textually a one-round construction, although `3-clause` can be read as
width exactly three or width at most three.  I will enumerate both parent
readings, every non-tautological resolvent of width at most three, and an
iterated fixpoint as a robustness diagnostic.

For the triples construction, two positive clauses cannot resolve.  A
critical and a positive triple have a nominal four-literal resolvent.
It can lose the extra positive literal only if the triple contains the
critical-clause parent, but that parent is adjacent to the pivot child and
such a triple was not added.  Any other collapse is tautological.  Two
critical clauses connected by a pivot also give a nominal four-literal
resolvent.  A repeated negative child would create an undirected triangle;
an opposite parent literal would create a directed 2-cycle.  Thus there
is no non-tautological resolvent of width at most three.  The triples
closure is consequently `F` even under iteration.

For the pairs construction under a width-at-most-three parent reading,
critical--positive-pair resolution can add a three-clause, but it has two
positive literals (or is tautological), so no one-round addition is a
critical clause.  Under the exact-width parent reading, the positive pairs
are not parents.  Iterated behavior is a separate non-source diagnostic.

In the triples variant `F~=F`; the only clauses having exactly one
positive literal are the `C_x`, one for each distinct positive variable.
Hence every variable has exactly one critical clause, `TwoCC` is empty,
and the canonical selection is forced.

## Limit-point plan

For every fixed `t in [0,1/10]`, take any integers `n_j -> infinity`
past the uniform threshold and `m_j=round(t*n_j)` (with the harmless
separate `m=0` case at `t=0`).  Then `0<=m_j<=n_j/10` needs care at the
upper endpoint: use `m_j=floor(t*n_j)` there, or simply floor for every
`t`.  We have `m_j/n_j -> t`, and the uniform construction conditions
remain valid.  In particular `floor(i_1^* n)/n -> i_1^*` because
`i_1^*<1/10`.  This yields the whole closed segment as limit points if
the preceding proof and source semantics survive exact checking.

## Post-clean-room primary-source check

After the derivation and validator above were frozen, I downloaded Scheder's
official ECCC Revision 1 directly from
`https://eccc.weizmann.ac.il/report/2021/069/revision/1/download/` on
2026-08-27.  Its SHA-256 is
`e4d634c4ea46f58041fd35bfd4978b7bb95e77ad26530735aa0577822dc4e506`,
byte-for-byte equal to the repository copy
`research_cycle_07/frozen_sources/scheder_tr21069_rev1.pdf` (both files are
1,582,177 bytes).  Thus there is no source-change issue here.

Definition 31 on printed page 19 defines `F~` as “F plus all 3-clauses that
can be inferred from pairs of 3-clauses of F”.  The words “of F” make this a
one-round operation, not an iterative closure.  The following paragraph
identifies the inference as resolution.  Printed page 2 defines a `k`-CNF as
having clauses of at most `k` literals.  Because “3-clause” itself can still
be read narrowly (exact width three), the validator checks both exact-three
and width-at-most-three parent conventions.  The triples construction has
only width-three parents and has zero non-tautological resolvents of width at
most three, so this ambiguity is immaterial there.  The pairs construction
gains mixed-sign three-clauses under the broad parent reading, but every such
clause has two positive literals; it gains no new critical clause.  Hence its
actual one-round `TwoCC` is also empty.  An iterated closure is not Definition
31 and is irrelevant to the theorem; the triples carrier is robust even to
that hypothetical reading because there is no first resolvent to iterate.

## Completed hostile-validation classifications

### H1 — WELL-DEFINED PARAMETERS: SOUND WITH REQUIRED REPAIR

For every `n>=403` and `1<=m<=floor(n/10)`, the Beatty-difference argument
above proves that at most four candidates are forbidden among `2,...,6`.
Thus the least valid `delta` exists and satisfies `2<=delta<=6`, uniformly
for **all** allowed `m`, including fixed or sublinear `m`; no
`m=Theta(n)` assumption is used.  For `m=0`, define `P=S=Q=empty` and
`g(x)=x+b`; no `delta` is needed.  This separate case is necessary because
the Cycle-7 displayed recipe contains `floor(n/m)` and is otherwise undefined
at the theorem's endpoint `m=0`.

The repository's current asymptotic prose does not contain this complete
uniform argument: it says the displacement is bounded when `m=Theta(n)`,
which does not discharge the theorem's quantifier over every `m`.  This is a
proof-level repair, not a counterexample to the repaired theorem.

### H2 — DEGREE STATISTICS: SOUND

Translations make `P,S,Q` internally collision-free.  The `g`-image of the
non-special sources is exactly `V\P`; adding the exceptional images adds one
extra preimage on `Q`, and `P cap Q=empty`.  Together with the successor
permutation, indegrees are one on `P`, three on `Q`, and two elsewhere.
There are no indegree-zero vertices and exactly `m` indegree-one vertices.
For `m=0` every indegree is two.  When `n>=403`, all arc steps lie strictly
between one and `n/2`, so both out-neighbors and all three clause variables
are distinct.  This proof covers wraparound and allows `P cap S` (which is
harmless).

### H3 — UNIQUE SATISFIABILITY: SOUND WITH REQUIRED PROOF REPAIR

The zero-set/directed-cycle equivalence above is exact, not merely a
necessary-condition heuristic.  The parameter proof gives `delta<=6`.  For
a putative directed cycle of length at most 17 and `n>402`, every step is at
most `n/3+7`, so its winding number is at most five.  The exact step equation
then contradicts `n>96+51*delta`.  Hence directed girth is greater than 17.
The signed-step case split proves the undirected projection triangle-free,
and its maximum degree is at most five.  Pairs uniqueness follows because a
closed zero set would contain a directed cycle but must be a clique in a
triangle-free graph.  Triples uniqueness follows because a cycle of length
at least 18 in a maximum-degree-five graph has an independent triple.

For `m=0`, the same proof applies with exceptional offset sum zero (or,
equivalently, `delta=0` only inside the inequalities).  Thus `n>=403`
handles every allowed `m`, including both endpoints.  This rules out an
infinite counterfamily; none was found computationally either.

### H4 — CLOSURE / TwoCC: SOUND UNDER THE ACTUAL DEFINITION

Definition 31 is one-round.  In triples, auxiliary--auxiliary pairs cannot
resolve; critical--auxiliary resolution is either tautological or has four
distinct literals; critical--critical resolution can shrink below four only
through a directed 2-cycle or an undirected triangle.  Both are absent.
Therefore **every** non-tautological resolvent has width greater than three:
`F~=F`, also at an iterated fixpoint.  In pairs, a broad-reading
critical--positive-pair resolvent has exactly two positive literals (unless
tautological), so it is not critical.  Both exact-parent and broad-parent
one-round readings leave exactly one critical clause per variable.

### H5 — CRITICAL CLAUSES: SOUND

In triples `F~=F`.  The clause `C_x` is the unique clause with exactly one
positive literal `x`; every auxiliary clause has three positive literals.
Thus each variable has exactly one critical clause, `TwoCC=empty`, and there
is no canonical-selection freedom.  The identical one-critical-clause
conclusion holds for pairs under the actual one-round Definition 31.  With
the degree result, the statistics are exactly `(0,m/n,0)`.

### THEOREM CR: SURVIVES WITH REPAIRS

The theorem is valid with the explicit uniform choice `n_0=403`.  Required
candidate-file repairs are:

1. in `research_cycle_07/corner_realizability.md` Theorem CR, remove the
   unused quantified constant `c>0`;
2. in its construction section, split out `m_1=0` as
   `P=S=Q=empty, g(x)=x+base`;
3. replace the current delta-existence paragraph with the complete cyclic
   Beatty-difference/block proof above, explicitly concluding `delta<=6`;
4. in the girth subsection, state the all-`m` uniformity and include the
   missing derivation `k<=5` from
   `17(base+delta)<6n` for `n>402`.

Consequently the current `RESEARCH_STATE.md` phrase that all asymptotic
repairs are already applied is stronger than the proof artifact supports;
it should either cite this repaired proof or be weakened until the above
changes are made.  No candidate theorem/proof file was modified here.

### COROLLARY CR-1: CR1-SOUND-WITH-REPAIRS

The strongest interval proved is exactly the claimed closed segment
`{(0,t,0):0<=t<=1/10}`.  For any fixed real `t` in this interval, take
`m_n=floor(t*n)`.  For every `n>=403`, `0<=m_n<=floor(n/10)`, all theorem
hypotheses hold, and `m_n/n -> t`.  At `t=0` this uses the separate `m=0`
construction.  At `t=1/10`, using `floor` avoids the endpoint error that a
nearest-integer choice can exceed `floor(n/10)`.  For an LP optimum
`i_1^*` lying strictly between zero and `1/10`, this gives a realizing
sequence for **every sufficiently large integer n**, not merely a
subsequence.  A finite realization at `0.06` is not used in this argument.

## Independent finite evidence and exact reproduction

All machine arithmetic used for signs, graph structure, resolution, and
statistics is integer/exact combinatorics.  Final tool/output hashes are:

* `cr_cleanroom_validator.py` SHA-256
  `65be2c49fe712d5c8030e538eb01a3b17b5626c87283ea670e12e704f776ffcb`;
* `fresh_suite_output.json` SHA-256
  `06dcb112ed6ef72d8aef9fe1fc5abb4b61acad44d62ba6f6acdec17ebbbab6f7`;
* `stored_21_comparison.json` SHA-256
  `f7f04d93cb3b7e3b42adda31508de323c611abf68a04ff2ef9e33945998292e7`;
* input `certificates/cycle07_corner/instances.json` SHA-256
  `1af8aff15117d948285bf32e82a87a8574195ea5c3266aeb4c1ccb42acac28cd`.

The fresh suite, selected before opening the stored certificates, found:

* 71,520 parameter cases (`10<=n<=1200`, every
  `1<=m<=floor(n/10)`): maximum `delta=6`; the only recipe failure with
  `n>=26` is `(27,2)`, and there is no failure with `n>=28`;
* 2,936 constructible structural cases: every `m` for `26<=n<=220`, plus
  six density regimes every 25 variables through `n=2000`; zero property
  failures for degrees, collisions, triangles, directed 2-cycles,
  critical-resolvent overlaps, pairs uniqueness, or triples uniqueness;
* 15 full formula/closure cases through `n=127`: triples had zero
  width-at-most-three resolvents at one round and fixpoint under both parent
  conventions; pairs had empty `TwoCC` under both actual one-round
  conventions;
* the all-small diagnostic (`3<=n<=27`) finds its first property failure at
  `(3,0)` (both variants non-unique), as expected for an asymptotic theorem.
  In the formerly advertised finite range beginning at 26, the first and
  only recipe failure is `(27,2)`; every constructible case there passes.

Only after this output was frozen did I open the Cycle-7 certificate and the
two previously prohibited implementations.  Reconstructing each stored
formula solely from its recorded `g`, the fresh engine reproduced **21/21**:
formula syntax, unique satisfiability by the exact dangerous-cycle
characterization, indegrees, `i_0,i_1,tau`, one-round closure, critical
clauses, and `TwoCC`.  For every stored triples instance it additionally
found zero resolvents and a trivial fixpoint.  Seven stored `*-explicit`
instances and the `m=0` instance match the final raw recipe; the older search
instances need not match it but independently satisfy their recorded claims.

Finite testing is not being promoted to an asymptotic proof.  The absence of
an infinite counterfamily follows from the separate `n>=403` argument above.
