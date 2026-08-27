import Mathlib

/-!
# Finite balanced-chain set systems

This file formalizes the reusable finite core of the balanced-chain problem.
The ground set is an arbitrary finite type `α`.  A maximal chain is encoded by
the order in which its elements are inserted; this makes every prefix an
actual subset and avoids quotienting chains by redundant presentations.
-/

open scoped BigOperators

namespace BalancedChain

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- A coloring is represented by its set of positive elements. -/
abbrev Coloring (α : Type*) := Finset α

/-- A coloring has equally many positive and negative elements. -/
def IsBalanced (P : Coloring α) : Prop := 2 * P.card = Fintype.card α

/-- The sign assigned by the coloring `P`. -/
def colorSign (P : Coloring α) (x : α) : ℤ := if x ∈ P then 1 else -1

/-- Signed imbalance of a subset. -/
def imbalance (P S : Finset α) : ℤ := ∑ x ∈ S, colorSign P x

/-- The subset has imbalance at most one in absolute value. -/
def Compatible (P S : Finset α) : Prop := |imbalance P S| ≤ 1

/-- An insertion order for all elements of a finite ground set. -/
structure MaximalChain (α : Type*) [Fintype α] where
  order : Fin (Fintype.card α) ≃ α

/-- The first `k` elements in the insertion order.  Values `k > |α|` simply
give the full set; all chain predicates below explicitly restrict to
`k ≤ |α|`. -/
def MaximalChain.prefix (C : MaximalChain α) (k : ℕ) : Finset α :=
  Finset.univ.filter fun x => (C.order.symm x).val < k

/-- Every subset in the represented maximal chain belongs to `X`. -/
def ChainContained (X : Set (Finset α)) (C : MaximalChain α) : Prop :=
  ∀ k ≤ Fintype.card α, C.prefix k ∈ X

/-- The represented maximal chain is 1-balanced for `P`. -/
def ChainGood (P : Coloring α) (C : MaximalChain α) : Prop :=
  ∀ k ≤ Fintype.card α, Compatible P (C.prefix k)

/-- A fixed subset family contains a 1-balanced maximal chain for every
balanced coloring. -/
def IsOneBalancedChain (X : Set (Finset α)) : Prop :=
  ∀ P : Coloring α, IsBalanced P →
    ∃ C : MaximalChain α, ChainContained X C ∧ ChainGood P C

/-!
## Relabeling and literal unions

The definitions in this section formalize the deterministic core used by
average-to-worst-case symmetrization.  A permutation acts on literal subsets,
colorings, maximal chains, and subset families.  The central equivalence is
for acceptance by the complete family, rather than for any selected list of
generating paths.
-/

/-- The literal image of a subset under a permutation. -/
def relabelSubset (pi : Equiv.Perm α) (S : Finset α) : Finset α :=
  S.map pi.toEmbedding

@[simp] theorem mem_relabelSubset_iff (pi : Equiv.Perm α)
    (S : Finset α) (x : α) :
    x ∈ relabelSubset pi S ↔ pi.symm x ∈ S := by
  simp [relabelSubset]

@[simp] theorem card_relabelSubset (pi : Equiv.Perm α) (S : Finset α) :
    (relabelSubset pi S).card = S.card := by
  simp [relabelSubset]

@[simp] theorem relabelSubset_symm_relabelSubset
    (pi : Equiv.Perm α) (S : Finset α) :
    relabelSubset pi.symm (relabelSubset pi S) = S := by
  ext x
  simp

@[simp] theorem relabelSubset_relabelSubset_symm
    (pi : Equiv.Perm α) (S : Finset α) :
    relabelSubset pi (relabelSubset pi.symm S) = S := by
  simpa using relabelSubset_symm_relabelSubset pi.symm S

/-- The literal image of a subset family under a permutation.  The preimage
presentation makes membership extensional and is equivalent to taking the
set image because `pi` is bijective. -/
def relabelFamily (pi : Equiv.Perm α) (X : Set (Finset α)) :
    Set (Finset α) :=
  {T | relabelSubset pi.symm T ∈ X}

@[simp] theorem relabelSubset_mem_relabelFamily_iff
    (pi : Equiv.Perm α) (X : Set (Finset α)) (S : Finset α) :
    relabelSubset pi S ∈ relabelFamily pi X ↔ S ∈ X := by
  simp [relabelFamily]

@[simp] theorem relabelFamily_symm_relabelFamily
    (pi : Equiv.Perm α) (X : Set (Finset α)) :
    relabelFamily pi.symm (relabelFamily pi X) = X := by
  ext S
  simp [relabelFamily]

theorem relabelFamily_eq_image (pi : Equiv.Perm α)
    (X : Set (Finset α)) :
    relabelFamily pi X = (fun S => relabelSubset pi S) '' X := by
  ext T
  constructor
  · intro hT
    refine ⟨relabelSubset pi.symm T, hT, ?_⟩
    simp
  · rintro ⟨S, hS, rfl⟩
    simpa using hS

/-- Pull a coloring on the relabeled ground set back along `pi`. -/
def pullbackColoring (pi : Equiv.Perm α) (P : Coloring α) : Coloring α :=
  relabelSubset pi.symm P

@[simp] theorem mem_pullbackColoring_iff (pi : Equiv.Perm α)
    (P : Coloring α) (x : α) :
    x ∈ pullbackColoring pi P ↔ pi x ∈ P := by
  simp [pullbackColoring]

@[simp] theorem card_pullbackColoring (pi : Equiv.Perm α)
    (P : Coloring α) :
    (pullbackColoring pi P).card = P.card := by
  simp [pullbackColoring]

@[simp] theorem pullbackColoring_symm_pullbackColoring
    (pi : Equiv.Perm α) (P : Coloring α) :
    pullbackColoring pi.symm (pullbackColoring pi P) = P := by
  ext x
  simp

@[simp] theorem pullbackColoring_pullbackColoring_symm
    (pi : Equiv.Perm α) (P : Coloring α) :
    pullbackColoring pi (pullbackColoring pi.symm P) = P := by
  simpa using pullbackColoring_symm_pullbackColoring pi.symm P

@[simp] theorem isBalanced_pullbackColoring_iff
    (pi : Equiv.Perm α) (P : Coloring α) :
    IsBalanced (pullbackColoring pi P) ↔ IsBalanced P := by
  simp [IsBalanced]

@[simp] theorem colorSign_pullbackColoring (pi : Equiv.Perm α)
    (P : Coloring α) (x : α) :
    colorSign (pullbackColoring pi P) x = colorSign P (pi x) := by
  simp [colorSign]

theorem imbalance_relabelSubset (pi : Equiv.Perm α)
    (P : Coloring α) (S : Finset α) :
    imbalance P (relabelSubset pi S) =
      imbalance (pullbackColoring pi P) S := by
  simp [imbalance, relabelSubset]

@[simp] theorem compatible_relabelSubset_iff (pi : Equiv.Perm α)
    (P : Coloring α) (S : Finset α) :
    Compatible P (relabelSubset pi S) ↔
      Compatible (pullbackColoring pi P) S := by
  simp only [Compatible, imbalance_relabelSubset]

/-- Relabel every insertion in a maximal chain. -/
def MaximalChain.relabel (C : MaximalChain α) (pi : Equiv.Perm α) :
    MaximalChain α where
  order := C.order.trans pi

@[simp] theorem MaximalChain.prefix_relabel (C : MaximalChain α)
    (pi : Equiv.Perm α) (k : ℕ) :
    (C.relabel pi).prefix k = relabelSubset pi (C.prefix k) := by
  ext x
  have hpos :
      (C.relabel pi).order.symm x = C.order.symm (pi.symm x) := by
    apply (C.relabel pi).order.injective
    simp [MaximalChain.relabel]
  simp only [MaximalChain.prefix, Finset.mem_filter, Finset.mem_univ,
    true_and, mem_relabelSubset_iff]
  rw [hpos]

theorem chainContained_relabel_iff (pi : Equiv.Perm α)
    (X : Set (Finset α)) (C : MaximalChain α) :
    ChainContained (relabelFamily pi X) (C.relabel pi) ↔
      ChainContained X C := by
  constructor
  · intro h k hk
    have hmem := h k hk
    simpa using hmem
  · intro h k hk
    have hmem := h k hk
    simpa using hmem

theorem chainGood_relabel_iff (pi : Equiv.Perm α)
    (P : Coloring α) (C : MaximalChain α) :
    ChainGood P (C.relabel pi) ↔
      ChainGood (pullbackColoring pi P) C := by
  constructor
  · intro h k hk
    have hcompat := h k hk
    simpa using hcompat
  · intro h k hk
    have hcompat := h k hk
    simpa using hcompat

/-- Acceptance of one coloring by the full induced subset family. -/
def AcceptsColoring (X : Set (Finset α)) (P : Coloring α) : Prop :=
  ∃ C : MaximalChain α, ChainContained X C ∧ ChainGood P C

/-- Exact equivariance of full-family acceptance under a relabeling. -/
theorem acceptsColoring_relabel_iff (pi : Equiv.Perm α)
    (X : Set (Finset α)) (P : Coloring α) :
    AcceptsColoring (relabelFamily pi X) P ↔
      AcceptsColoring X (pullbackColoring pi P) := by
  constructor
  · rintro ⟨C, hcontained, hgood⟩
    refine ⟨C.relabel pi.symm, ?_, ?_⟩
    · have hcontained' :=
        (chainContained_relabel_iff pi.symm (relabelFamily pi X) C).2 hcontained
      simpa using hcontained'
    · have hgood' :=
        (chainGood_relabel_iff pi.symm (pullbackColoring pi P) C).2 (by
          simpa using hgood)
      exact hgood'
  · rintro ⟨C, hcontained, hgood⟩
    exact ⟨C.relabel pi,
      (chainContained_relabel_iff pi X C).2 hcontained,
      (chainGood_relabel_iff pi P C).2 hgood⟩

/-- Relabeling a fixed family preserves the worst-case family property. -/
theorem isOneBalancedChain_relabel_iff (pi : Equiv.Perm α)
    (X : Set (Finset α)) :
    IsOneBalancedChain (relabelFamily pi X) ↔ IsOneBalancedChain X := by
  constructor
  · intro hX P hbalanced
    have hpushBalanced :
        IsBalanced (pullbackColoring pi.symm P) :=
      (isBalanced_pullbackColoring_iff pi.symm P).2 hbalanced
    have haccepted :
        AcceptsColoring (relabelFamily pi X)
          (pullbackColoring pi.symm P) := by
      simpa [AcceptsColoring] using
        hX (pullbackColoring pi.symm P) hpushBalanced
    have hpulled :=
      (acceptsColoring_relabel_iff pi X (pullbackColoring pi.symm P)).1
        haccepted
    simpa [AcceptsColoring] using hpulled
  · intro hX P hbalanced
    have hpullBalanced : IsBalanced (pullbackColoring pi P) :=
      (isBalanced_pullbackColoring_iff pi P).2 hbalanced
    have hpulled : AcceptsColoring X (pullbackColoring pi P) := by
      simpa [AcceptsColoring] using hX (pullbackColoring pi P) hpullBalanced
    have haccepted := (acceptsColoring_relabel_iff pi X P).2 hpulled
    simpa [AcceptsColoring] using haccepted

/-- If some member of an indexed collection accepts each balanced coloring,
then the literal union of the collection is a 1-balanced-chain family. -/
theorem iUnion_isOneBalancedChain_of_pointwise_accepts
    {iota : Sort*} (F : iota → Set (Finset α))
    (haccepts : ∀ P : Coloring α, IsBalanced P →
      ∃ i, AcceptsColoring (F i) P) :
    IsOneBalancedChain (⋃ i, F i) := by
  intro P hbalanced
  obtain ⟨i, C, hcontained, hgood⟩ := haccepts P hbalanced
  refine ⟨C, ?_, hgood⟩
  intro k hk
  exact Set.mem_iUnion.mpr ⟨i, hcontained k hk⟩

/-- Deterministic union-of-relabelings lemma in pulled-back-coloring form.
Its premise concerns acceptance inside an individual full family; additional hybrid
chains in the literal union can only add witnesses. -/
theorem union_relabelings_isOneBalancedChain
    {iota : Sort*} (X : Set (Finset α)) (pi : iota → Equiv.Perm α)
    (haccepts : ∀ P : Coloring α, IsBalanced P →
      ∃ i, AcceptsColoring X (pullbackColoring (pi i) P)) :
    IsOneBalancedChain (⋃ i, relabelFamily (pi i) X) := by
  apply iUnion_isOneBalancedChain_of_pointwise_accepts
  intro P hbalanced
  obtain ⟨i, hi⟩ := haccepts P hbalanced
  exact ⟨i, (acceptsColoring_relabel_iff (pi i) X P).2 hi⟩

/-- The two elements inserted at positions `2j` and `2j+1` have opposite
colors. -/
def PairCrosses (P : Coloring α) (C : MaximalChain α) (j : ℕ)
    (h : 2 * j + 1 < Fintype.card α) : Prop :=
  (C.order ⟨2 * j, by omega⟩ ∈ P) ≠
    (C.order ⟨2 * j + 1, h⟩ ∈ P)

/-- Every complete consecutive pair in the insertion order crosses the cut. -/
def ConsecutivePairsCross (P : Coloring α) (C : MaximalChain α) : Prop :=
  ∀ j, ∀ h : 2 * j + 1 < Fintype.card α, PairCrosses P C j h

@[simp] theorem MaximalChain.mem_prefix_iff (C : MaximalChain α) (x : α) (k : ℕ) :
    x ∈ C.prefix k ↔ (C.order.symm x).val < k := by
  simp [MaximalChain.prefix]

@[simp] theorem MaximalChain.prefix_zero (C : MaximalChain α) :
    C.prefix 0 = ∅ := by
  ext x
  simp

@[simp] theorem MaximalChain.prefix_card (C : MaximalChain α) :
    C.prefix (Fintype.card α) = Finset.univ := by
  ext x
  simp

theorem MaximalChain.prefix_succ (C : MaximalChain α) {k : ℕ}
    (hk : k < Fintype.card α) :
    C.prefix (k + 1) = insert (C.order ⟨k, hk⟩) (C.prefix k) := by
  ext x
  simp only [mem_prefix_iff, Finset.mem_insert]
  constructor
  · intro hx
    by_cases hEq : (C.order.symm x).val = k
    · left
      calc
        x = C.order (C.order.symm x) := (C.order.apply_symm_apply x).symm
        _ = C.order ⟨k, hk⟩ := by
          congr
          exact Fin.ext hEq
    · right
      omega
  · rintro (rfl | hx)
    · simp
    · omega

theorem MaximalChain.new_not_mem_prefix (C : MaximalChain α) {k : ℕ}
    (hk : k < Fintype.card α) :
    C.order ⟨k, hk⟩ ∉ C.prefix k := by
  simp

theorem imbalance_prefix_succ (P : Coloring α) (C : MaximalChain α) {k : ℕ}
    (hk : k < Fintype.card α) :
    imbalance P (C.prefix (k + 1)) =
      imbalance P (C.prefix k) + colorSign P (C.order ⟨k, hk⟩) := by
  rw [C.prefix_succ hk]
  simp [imbalance, C.new_not_mem_prefix hk, add_comm]

theorem imbalance_eq_card (P S : Finset α) :
    imbalance P S = 2 * ((S ∩ P).card : ℤ) - (S.card : ℤ) := by
  classical
  induction S using Finset.induction_on with
  | empty => simp [imbalance]
  | @insert x S hx ih =>
      by_cases hp : x ∈ P
      · simp [imbalance, colorSign, hx, hp]
        change 1 + imbalance P S =
          2 * (((S ∩ P).card + 1 : ℕ) : ℤ) - (((S.card + 1 : ℕ) : ℤ))
        rw [ih]
        push_cast
        ring
      · simp [imbalance, colorSign, hx, hp]
        change -1 + imbalance P S =
          2 * ((S ∩ P).card : ℤ) - (((S.card + 1 : ℕ) : ℤ))
        rw [ih]
        push_cast
        ring

theorem MaximalChain.prefix_card_eq (C : MaximalChain α) {k : ℕ}
    (hk : k ≤ Fintype.card α) : (C.prefix k).card = k := by
  induction k with
  | zero => simp
  | succ k ih =>
      have hklt : k < Fintype.card α := by omega
      rw [C.prefix_succ hklt, Finset.card_insert_of_notMem (C.new_not_mem_prefix hklt)]
      simp [ih (by omega)]

theorem compatible_even_imbalance_zero (P S : Finset α)
    (hcompat : Compatible P S) (heven : Even S.card) :
    imbalance P S = 0 := by
  obtain ⟨r, hr⟩ := heven
  rw [Compatible, abs_le] at hcompat
  rw [imbalance_eq_card, hr] at hcompat ⊢
  omega

theorem colorSign_add_eq_zero_iff (P : Coloring α) (a b : α) :
    colorSign P a + colorSign P b = 0 ↔ (a ∈ P) ≠ (b ∈ P) := by
  by_cases ha : a ∈ P <;> by_cases hb : b ∈ P <;>
    simp [colorSign, ha, hb]

theorem good_even_prefix_zero (P : Coloring α) (C : MaximalChain α)
    (hgood : ChainGood P C) {k : ℕ} (hk : k ≤ Fintype.card α)
    (heven : Even k) : imbalance P (C.prefix k) = 0 := by
  apply compatible_even_imbalance_zero P (C.prefix k) (hgood k hk)
  rw [C.prefix_card_eq hk]
  exact heven

theorem chainGood_implies_consecutivePairsCross (P : Coloring α)
    (C : MaximalChain α) (hgood : ChainGood P C) :
    ConsecutivePairsCross P C := by
  intro j hj
  have h0 : 2 * j < Fintype.card α := by omega
  have h1 : 2 * j + 1 < Fintype.card α := hj
  have h2 : 2 * j + 2 ≤ Fintype.card α := by omega
  have hz0 : imbalance P (C.prefix (2 * j)) = 0 :=
    good_even_prefix_zero P C hgood (by omega) (by simp)
  have hz2 : imbalance P (C.prefix (2 * j + 2)) = 0 :=
    good_even_prefix_zero P C hgood h2 (by use j + 1; omega)
  have hs0 := imbalance_prefix_succ P C h0
  have hs1 := imbalance_prefix_succ P C h1
  have hsum :
      colorSign P (C.order ⟨2 * j, h0⟩) +
        colorSign P (C.order ⟨2 * j + 1, h1⟩) = 0 := by
    rw [show 2 * j + 2 = (2 * j + 1) + 1 by omega] at hz2
    omega
  exact (colorSign_add_eq_zero_iff P _ _).mp hsum

theorem consecutivePairsCross_even_prefix_zero (P : Coloring α)
    (C : MaximalChain α) (hpairs : ConsecutivePairsCross P C) :
    ∀ j, 2 * j ≤ Fintype.card α →
      imbalance P (C.prefix (2 * j)) = 0 := by
  intro j
  induction j with
  | zero =>
      intro _
      simp [imbalance]
  | succ j ih =>
      intro hbound
      have h0 : 2 * j < Fintype.card α := by omega
      have h1 : 2 * j + 1 < Fintype.card α := by omega
      have hprev := ih (by omega)
      have hcross := hpairs j h1
      have hsum :
          colorSign P (C.order ⟨2 * j, h0⟩) +
            colorSign P (C.order ⟨2 * j + 1, h1⟩) = 0 :=
        (colorSign_add_eq_zero_iff P _ _).mpr hcross
      calc
        imbalance P (C.prefix (2 * (j + 1))) =
            imbalance P (C.prefix ((2 * j + 1) + 1)) := by
              congr 1
        _ = imbalance P (C.prefix (2 * j + 1)) +
              colorSign P (C.order ⟨2 * j + 1, h1⟩) :=
            imbalance_prefix_succ P C h1
        _ = (imbalance P (C.prefix (2 * j)) +
              colorSign P (C.order ⟨2 * j, h0⟩)) +
              colorSign P (C.order ⟨2 * j + 1, h1⟩) := by
            rw [imbalance_prefix_succ P C h0]
        _ = 0 := by omega

theorem consecutivePairsCross_implies_chainGood (P : Coloring α)
    (C : MaximalChain α) (hpairs : ConsecutivePairsCross P C) :
    ChainGood P C := by
  intro k hk
  obtain ⟨j, hj | hj⟩ := Nat.even_or_odd' k
  · subst k
    have hz := consecutivePairsCross_even_prefix_zero P C hpairs j hk
    simp [Compatible, hz]
  · subst k
    have h0 : 2 * j < Fintype.card α := by omega
    have hz := consecutivePairsCross_even_prefix_zero P C hpairs j (by omega)
    rw [Compatible, imbalance_prefix_succ P C h0, hz]
    by_cases hmem : C.order ⟨2 * j, h0⟩ ∈ P <;>
      simp [colorSign, hmem]

/-- Consecutive-pair characterization of a 1-balanced maximal chain. -/
theorem chainGood_iff_consecutivePairsCross (P : Coloring α)
    (C : MaximalChain α) :
    ChainGood P C ↔ ConsecutivePairsCross P C := by
  constructor
  · exact chainGood_implies_consecutivePairsCross P C
  · exact consecutivePairsCross_implies_chainGood P C

/-- An oriented open two-step arc of the contracted subset DAG.  The target
is `insert b (insert a S)` and the selected odd intermediary is
`insert a S`.  Reversing `a,b` represents use of the other intermediary. -/
structure ContractedArc (X : Set (Finset α)) (P : Coloring α)
    (S : Finset α) (a b : α) : Prop where
  source_mem : S ∈ X
  first_fresh : a ∉ S
  second_fresh : b ∉ insert a S
  middle_mem : insert a S ∈ X
  target_mem : insert b (insert a S) ∈ X
  crosses : (a ∈ P) ≠ (b ∈ P)

/-- A source-to-sink path in the contracted, coloring-filtered subset DAG,
encoded by the order of its oriented pair labels. -/
def ContractedPath (X : Set (Finset α)) (P : Coloring α)
    (C : MaximalChain α) : Prop :=
  C.prefix 0 ∈ X ∧
  C.prefix (Fintype.card α) ∈ X ∧
  ∀ j, ∀ h : 2 * j + 1 < Fintype.card α,
    ContractedArc X P (C.prefix (2 * j))
      (C.order ⟨2 * j, by omega⟩) (C.order ⟨2 * j + 1, h⟩)

theorem chainContained_and_pairs_implies_contractedPath
    (X : Set (Finset α)) (P : Coloring α) (C : MaximalChain α)
    (hcontained : ChainContained X C)
    (hpairs : ConsecutivePairsCross P C) : ContractedPath X P C := by
  refine ⟨hcontained 0 (by omega), hcontained _ (by omega), ?_⟩
  intro j h1
  have h0 : 2 * j < Fintype.card α := by omega
  have h2 : 2 * j + 2 ≤ Fintype.card α := by omega
  constructor
  · exact hcontained _ (by omega)
  · exact C.new_not_mem_prefix h0
  · have hfresh := C.new_not_mem_prefix h1
    rw [C.prefix_succ h0] at hfresh
    exact hfresh
  · have hmiddle := hcontained (2 * j + 1) (by omega)
    rw [show 2 * j + 1 = 2 * j + 1 by rfl, C.prefix_succ h0] at hmiddle
    exact hmiddle
  · have htarget := hcontained (2 * j + 2) h2
    rw [show 2 * j + 2 = (2 * j + 1) + 1 by omega,
      C.prefix_succ h1, C.prefix_succ h0] at htarget
    exact htarget
  · exact hpairs j h1

theorem contractedPath_implies_chainContained
    (X : Set (Finset α)) (P : Coloring α) (C : MaximalChain α)
    (heven : Even (Fintype.card α))
    (hpath : ContractedPath X P C) : ChainContained X C := by
  obtain ⟨m, hm⟩ := heven
  intro k hk
  obtain ⟨j, hj | hj⟩ := Nat.even_or_odd' k
  · subst k
    by_cases hterminal : 2 * j = Fintype.card α
    · simpa [hterminal] using hpath.2.1
    · have hpair : 2 * j + 1 < Fintype.card α := by omega
      exact (hpath.2.2 j hpair).source_mem
  · subst k
    have hpair : 2 * j + 1 < Fintype.card α := by omega
    have harc := hpath.2.2 j hpair
    have h0 : 2 * j < Fintype.card α := by omega
    rw [C.prefix_succ h0]
    exact harc.middle_mem

theorem contractedPath_implies_consecutivePairsCross
    (X : Set (Finset α)) (P : Coloring α) (C : MaximalChain α)
    (hpath : ContractedPath X P C) : ConsecutivePairsCross P C := by
  intro j h
  exact (hpath.2.2 j h).crosses

/-- Exact path-DAG reformulation for an even-size ground set. -/
theorem chainContained_and_good_iff_contractedPath
    (X : Set (Finset α)) (P : Coloring α) (C : MaximalChain α)
    (heven : Even (Fintype.card α)) :
    (ChainContained X C ∧ ChainGood P C) ↔ ContractedPath X P C := by
  constructor
  · rintro ⟨hcontained, hgood⟩
    exact chainContained_and_pairs_implies_contractedPath X P C hcontained
      ((chainGood_iff_consecutivePairsCross P C).mp hgood)
  · intro hpath
    exact ⟨contractedPath_implies_chainContained X P C heven hpath,
      (chainGood_iff_consecutivePairsCross P C).mpr
        (contractedPath_implies_consecutivePairsCross X P C hpath)⟩

/-- Family-level exact path-DAG reformulation. -/
theorem oneBalancedChain_iff_contractedPaths
    (X : Set (Finset α)) (heven : Even (Fintype.card α)) :
    IsOneBalancedChain X ↔
      ∀ P : Coloring α, IsBalanced P →
        ∃ C : MaximalChain α, ContractedPath X P C := by
  constructor
  · intro hX P hP
    obtain ⟨C, hcontained, hgood⟩ := hX P hP
    exact ⟨C, (chainContained_and_good_iff_contractedPath X P C heven).mp
      ⟨hcontained, hgood⟩⟩
  · intro hX P hP
    obtain ⟨C, hpath⟩ := hX P hP
    exact ⟨C, (chainContained_and_good_iff_contractedPath X P C heven).mpr hpath⟩

/-- `X` has exactly one selected singleton, namely `{v}`. -/
def HasUniqueSingleton (X : Set (Finset α)) (v : α) : Prop :=
  ({v} : Finset α) ∈ X ∧
    ∀ S : Finset α, S ∈ X → S.card = 1 → S = {v}

/-- Selected two-set neighbors of the singleton anchor. -/
noncomputable def lowerNeighbors (X : Set (Finset α)) (v : α) : Finset α := by
  classical
  exact Finset.univ.filter fun u => u ≠ v ∧ ({v, u} : Finset α) ∈ X

@[simp] theorem mem_lowerNeighbors_iff (X : Set (Finset α)) (v u : α) :
    u ∈ lowerNeighbors X v ↔ u ≠ v ∧ ({v, u} : Finset α) ∈ X := by
  classical
  simp [lowerNeighbors]

/-- Lemma S1: a unique singleton forces at least half of a star. -/
theorem unique_singleton_half_star
    (X : Set (Finset α)) (v : α)
    (heven : Even (Fintype.card α))
    (hX : IsOneBalancedChain X)
    (hunique : HasUniqueSingleton X v) :
    Fintype.card α / 2 ≤ (lowerNeighbors X v).card := by
  by_contra hnot
  have hsmall : (lowerNeighbors X v).card < Fintype.card α / 2 := by omega
  obtain ⟨m, hm⟩ := heven
  have hnpos : 0 < Fintype.card α := Fintype.card_pos_iff.mpr ⟨v⟩
  have hn2 : 2 ≤ Fintype.card α := by omega
  have hvnot : v ∉ lowerNeighbors X v := by simp
  have hanchorCard : (insert v (lowerNeighbors X v)).card ≤ Fintype.card α / 2 := by
    rw [Finset.card_insert_of_notMem hvnot]
    omega
  obtain ⟨P, hanchorP, hPcard⟩ :=
    Finset.exists_superset_card_eq hanchorCard (Nat.div_le_self _ _)
  have hPbalanced : IsBalanced P := by
    unfold IsBalanced
    rw [hPcard]
    omega
  obtain ⟨C, hcontained, hgood⟩ := hX P hPbalanced
  have h0 : 0 < Fintype.card α := hnpos
  have h1 : 1 < Fintype.card α := by omega
  have hp1mem := hcontained 1 (by omega)
  have hp1card : (C.prefix 1).card = 1 := C.prefix_card_eq (by omega)
  have hp1unique : C.prefix 1 = ({v} : Finset α) :=
    hunique.2 (C.prefix 1) hp1mem hp1card
  have hprefix1 :
      C.prefix 1 = ({C.order ⟨0, h0⟩} : Finset α) := by
    rw [show 1 = 0 + 1 by omega, C.prefix_succ h0]
    simp
  have hfirst : C.order ⟨0, h0⟩ = v := by
    apply Finset.singleton_inj.mp
    exact hprefix1.symm.trans hp1unique
  have hfin_ne : (⟨0, h0⟩ : Fin (Fintype.card α)) ≠ ⟨1, h1⟩ := by
    intro h
    have := congrArg Fin.val h
    norm_num at this
  have horder_ne : C.order ⟨0, h0⟩ ≠ C.order ⟨1, h1⟩ := by
    intro h
    exact hfin_ne (C.order.injective h)
  have hsecond_ne_v : C.order ⟨1, h1⟩ ≠ v := by
    intro h
    apply horder_ne
    rw [hfirst, h]
  have hp2mem := hcontained 2 hn2
  have hprefix2 :
      C.prefix 2 = ({C.order ⟨0, h0⟩, C.order ⟨1, h1⟩} : Finset α) := by
    calc
      C.prefix 2 = insert (C.order ⟨1, h1⟩) (C.prefix 1) := C.prefix_succ h1
      _ = insert (C.order ⟨1, h1⟩) {C.order ⟨0, h0⟩} := by rw [hprefix1]
      _ = {C.order ⟨0, h0⟩, C.order ⟨1, h1⟩} := by
        ext x
        simp only [Finset.mem_insert, Finset.mem_singleton]
        tauto
  have hpairmem : ({v, C.order ⟨1, h1⟩} : Finset α) ∈ X := by
    rw [← hfirst, ← hprefix2]
    exact hp2mem
  have hsecondGamma : C.order ⟨1, h1⟩ ∈ lowerNeighbors X v := by
    exact (mem_lowerNeighbors_iff X v _).2 ⟨hsecond_ne_v, hpairmem⟩
  have hvP : v ∈ P := hanchorP (by simp)
  have hsecondP : C.order ⟨1, h1⟩ ∈ P :=
    hanchorP (by simp [hsecondGamma])
  have hcross := (chainGood_iff_consecutivePairsCross P C).mp hgood 0 h1
  simp [PairCrosses, hfirst, hvP, hsecondP] at hcross

theorem MaximalChain.prefix_pred_eq_erase_last (C : MaximalChain α)
    (hnpos : 0 < Fintype.card α) :
    C.prefix (Fintype.card α - 1) =
      Finset.univ.erase (C.order ⟨Fintype.card α - 1, by omega⟩) := by
  ext x
  simp only [mem_prefix_iff, Finset.mem_erase, Finset.mem_univ, and_true]
  constructor
  · intro hlt heq
    have hval := congrArg (fun y => (C.order.symm y).val) heq
    simp at hval
    omega
  · intro hne
    by_contra hlt
    apply hne
    calc
      x = C.order (C.order.symm x) := (C.order.apply_symm_apply x).symm
      _ = C.order ⟨Fintype.card α - 1, by omega⟩ := by
        congr
        apply Fin.ext
        simp only [Fin.val_mk]
        have := (C.order.symm x).isLt
        omega

theorem MaximalChain.prefix_sub_two_eq_sdiff_pair (C : MaximalChain α)
    (hn2 : 2 ≤ Fintype.card α) :
    C.prefix (Fintype.card α - 2) =
      Finset.univ \ ({C.order ⟨Fintype.card α - 2, by omega⟩,
        C.order ⟨Fintype.card α - 1, by omega⟩} : Finset α) := by
  ext x
  simp only [mem_prefix_iff, Finset.mem_sdiff, Finset.mem_univ, true_and,
    Finset.mem_insert, Finset.mem_singleton]
  constructor
  · intro hlt
    intro heq
    rcases heq with heq | heq
    ·
      have hval := congrArg (fun y => (C.order.symm y).val) heq
      simp at hval
      omega
    ·
      have hval := congrArg (fun y => (C.order.symm y).val) heq
      simp at hval
      omega
  · intro hne
    by_contra hlt
    have hindex :
        (C.order.symm x).val = Fintype.card α - 2 ∨
          (C.order.symm x).val = Fintype.card α - 1 := by
      have := (C.order.symm x).isLt
      omega
    rcases hindex with hindex | hindex
    · apply hne
      left
      calc
        x = C.order (C.order.symm x) := (C.order.apply_symm_apply x).symm
        _ = C.order ⟨Fintype.card α - 2, by omega⟩ := by
          congr
          exact Fin.ext hindex
    · apply hne
      right
      calc
        x = C.order (C.order.symm x) := (C.order.apply_symm_apply x).symm
        _ = C.order ⟨Fintype.card α - 1, by omega⟩ := by
          congr
          exact Fin.ext hindex

/-- `X` has exactly one selected co-singleton, omitting `w`. -/
def HasUniqueCosingleton (X : Set (Finset α)) (w : α) : Prop :=
  Finset.univ.erase w ∈ X ∧
    ∀ S : Finset α, S ∈ X → S.card = Fintype.card α - 1 →
      S = Finset.univ.erase w

/-- Elements paired with `w` among selected complements of two-sets. -/
noncomputable def upperOmittedNeighbors
    (X : Set (Finset α)) (w : α) : Finset α := by
  classical
  exact Finset.univ.filter fun u =>
    u ≠ w ∧ Finset.univ \ ({w, u} : Finset α) ∈ X

@[simp] theorem mem_upperOmittedNeighbors_iff
    (X : Set (Finset α)) (w u : α) :
    u ∈ upperOmittedNeighbors X w ↔
      u ≠ w ∧ Finset.univ \ ({w, u} : Finset α) ∈ X := by
  classical
  simp [upperOmittedNeighbors]

/-- Lemma S2: the dual half-star at a unique co-singleton.  This proof is a
direct reversal of the S1 argument, avoiding any unformalized quotient of
families under complementation. -/
theorem unique_cosingleton_dual_half_star
    (X : Set (Finset α)) (w : α)
    (heven : Even (Fintype.card α))
    (hX : IsOneBalancedChain X)
    (hunique : HasUniqueCosingleton X w) :
    Fintype.card α / 2 ≤ (upperOmittedNeighbors X w).card := by
  by_contra hnot
  have hsmall :
      (upperOmittedNeighbors X w).card < Fintype.card α / 2 := by omega
  obtain ⟨m, hm⟩ := heven
  have hnpos : 0 < Fintype.card α := Fintype.card_pos_iff.mpr ⟨w⟩
  have hn2 : 2 ≤ Fintype.card α := by omega
  have hwnot : w ∉ upperOmittedNeighbors X w := by simp
  have hanchorCard :
      (insert w (upperOmittedNeighbors X w)).card ≤ Fintype.card α / 2 := by
    rw [Finset.card_insert_of_notMem hwnot]
    omega
  obtain ⟨P, hanchorP, hPcard⟩ :=
    Finset.exists_superset_card_eq hanchorCard (Nat.div_le_self _ _)
  have hPbalanced : IsBalanced P := by
    unfold IsBalanced
    rw [hPcard]
    omega
  obtain ⟨C, hcontained, hgood⟩ := hX P hPbalanced
  have hlastBound : Fintype.card α - 1 < Fintype.card α := by omega
  have hprevBound : Fintype.card α - 2 < Fintype.card α := by omega
  have hpredMem := hcontained (Fintype.card α - 1) (by omega)
  have hpredCard :
      (C.prefix (Fintype.card α - 1)).card = Fintype.card α - 1 :=
    C.prefix_card_eq (by omega)
  have hpredUnique :
      C.prefix (Fintype.card α - 1) = Finset.univ.erase w :=
    hunique.2 _ hpredMem hpredCard
  have hpredErase := C.prefix_pred_eq_erase_last hnpos
  have hlast : C.order ⟨Fintype.card α - 1, hlastBound⟩ = w := by
    by_contra hne
    have hmem : C.order ⟨Fintype.card α - 1, hlastBound⟩ ∈
        Finset.univ.erase w := by simp [hne]
    rw [← hpredUnique, hpredErase] at hmem
    simp at hmem
  have hfin_ne :
      (⟨Fintype.card α - 2, hprevBound⟩ : Fin (Fintype.card α)) ≠
        ⟨Fintype.card α - 1, hlastBound⟩ := by
    intro h
    have hval := congrArg Fin.val h
    simp only [Fin.val_mk] at hval
    omega
  have horder_ne :
      C.order ⟨Fintype.card α - 2, hprevBound⟩ ≠
        C.order ⟨Fintype.card α - 1, hlastBound⟩ := by
    intro h
    exact hfin_ne (C.order.injective h)
  have hprev_ne_w : C.order ⟨Fintype.card α - 2, hprevBound⟩ ≠ w := by
    intro h
    apply horder_ne
    rw [h, hlast]
  have hsubTwoMem := hcontained (Fintype.card α - 2) (by omega)
  have hsubTwoEq := C.prefix_sub_two_eq_sdiff_pair hn2
  have homittedMem :
      Finset.univ \ ({w, C.order ⟨Fintype.card α - 2, hprevBound⟩} : Finset α) ∈ X := by
    rw [← hlast]
    have hpairswap :
        ({C.order ⟨Fintype.card α - 1, hlastBound⟩,
          C.order ⟨Fintype.card α - 2, hprevBound⟩} : Finset α) =
        ({C.order ⟨Fintype.card α - 2, hprevBound⟩,
          C.order ⟨Fintype.card α - 1, hlastBound⟩} : Finset α) := by
      ext x
      simp only [Finset.mem_insert, Finset.mem_singleton]
      tauto
    rw [hpairswap, ← hsubTwoEq]
    exact hsubTwoMem
  have hprevGamma :
      C.order ⟨Fintype.card α - 2, hprevBound⟩ ∈
        upperOmittedNeighbors X w :=
    (mem_upperOmittedNeighbors_iff X w _).2 ⟨hprev_ne_w, homittedMem⟩
  have hwP : w ∈ P := hanchorP (by simp)
  have hprevP : C.order ⟨Fintype.card α - 2, hprevBound⟩ ∈ P :=
    hanchorP (by simp [hprevGamma])
  have hmpos : 0 < m := by omega
  have hpairIndex : 2 * (m - 1) + 1 < Fintype.card α := by omega
  have hcross :=
    (chainGood_iff_consecutivePairsCross P C).mp hgood (m - 1) hpairIndex
  have hidx0 :
      (⟨2 * (m - 1), by omega⟩ : Fin (Fintype.card α)) =
        ⟨Fintype.card α - 2, hprevBound⟩ := by
    apply Fin.ext
    simp only [Fin.val_mk]
    omega
  have hidx1 :
      (⟨2 * (m - 1) + 1, hpairIndex⟩ : Fin (Fintype.card α)) =
        ⟨Fintype.card α - 1, hlastBound⟩ := by
    apply Fin.ext
    simp only [Fin.val_mk]
    omega
  unfold PairCrosses at hcross
  rw [hidx0, hidx1, hlast] at hcross
  simp [hwP, hprevP] at hcross

/-!
## Cycle 5: multi-copy label sets, copy-pure and hybrid acceptance

The definitions below fix, over an arbitrary indexed list of literal subset
families, the provenance-invariant notions used by the hybrid-routing
analysis: the label set of a subset, copy-pure chains, pure acceptance,
hybrid-only colorings, and labelings with a bounded number of copy
switches.  Everything is stated for the full induced-subset semantics
(membership of every chain prefix), never for generating paths.
-/

section MultiCopy

variable {ι : Type*} [DecidableEq ι]

/-- The label set of a literal subset: the copies containing it.  This
depends only on the subset, never on how it was produced. -/
def labelSet (F : ι → Set (Finset α)) (S : Finset α) : Set ι :=
  {j | S ∈ F j}

/-- A chain is copy-pure for the list `F` when a single copy contains every
prefix. -/
def ChainPure (F : ι → Set (Finset α)) (C : MaximalChain α) : Prop :=
  ∃ j, ChainContained (F j) C

/-- Some individual copy accepts the coloring. -/
def AcceptsPure (F : ι → Set (Finset α)) (P : Coloring α) : Prop :=
  ∃ j, AcceptsColoring (F j) P

/-- The literal union accepts, but no individual copy does. -/
def HybridOnly (F : ι → Set (Finset α)) (P : Coloring α) : Prop :=
  AcceptsColoring (⋃ j, F j) P ∧ ¬ AcceptsPure F P

theorem chainContained_mono {X Y : Set (Finset α)} (hXY : X ⊆ Y)
    {C : MaximalChain α} (h : ChainContained X C) : ChainContained Y C :=
  fun k hk => hXY (h k hk)

/-- Pure acceptance transfers to the literal union. -/
theorem acceptsPure_acceptsUnion {F : ι → Set (Finset α)} {P : Coloring α}
    (h : AcceptsPure F P) : AcceptsColoring (⋃ j, F j) P := by
  obtain ⟨j, C, hC, hG⟩ := h
  exact ⟨C, chainContained_mono (Set.subset_iUnion F j) hC, hG⟩

/-- Union acceptance splits into pure acceptance or hybrid-only status. -/
theorem acceptsUnion_pure_or_hybridOnly {F : ι → Set (Finset α)}
    {P : Coloring α} (h : AcceptsColoring (⋃ j, F j) P) :
    AcceptsPure F P ∨ HybridOnly F P := by
  by_cases hp : AcceptsPure F P
  · exact Or.inl hp
  · exact Or.inr ⟨h, hp⟩

/-- A labeling of a chain: one copy per prefix, witnessing membership.  The
number of switches of the labeling is the number of indices at which the
label changes. -/
def IsLabeling (F : ι → Set (Finset α)) (C : MaximalChain α)
    (l : ℕ → ι) : Prop :=
  ∀ k ≤ Fintype.card α, C.prefix k ∈ F (l k)

/-- The chain admits a labeling with at most `s` copy switches. -/
def SwitchBound (F : ι → Set (Finset α)) (C : MaximalChain α)
    (s : ℕ) : Prop :=
  ∃ l : ℕ → ι, IsLabeling F C l ∧
    ((Finset.range (Fintype.card α)).filter fun k => l (k + 1) ≠ l k).card ≤ s

/-- Zero switches is exactly copy-purity. -/
theorem switchBound_zero_iff_chainPure {F : ι → Set (Finset α)}
    {C : MaximalChain α} :
    SwitchBound F C 0 ↔ ChainPure F C := by
  constructor
  · rintro ⟨l, hl, hcard⟩
    refine ⟨l 0, fun k hk => ?_⟩
    have hconst : ∀ k ≤ Fintype.card α, l k = l 0 := by
      intro k
      induction k with
      | zero => intro _; rfl
      | succ k ih =>
        intro hk1
        have hk0 : k ≤ Fintype.card α := Nat.le_of_succ_le hk1
        have hkmem : k ∈ Finset.range (Fintype.card α) :=
          Finset.mem_range.2 (Nat.lt_of_succ_le hk1)
        have : l (k + 1) = l k := by
          by_contra hne
          have : k ∈ (Finset.range (Fintype.card α)).filter
              fun k => l (k + 1) ≠ l k := Finset.mem_filter.2 ⟨hkmem, hne⟩
          have := Finset.card_pos.2 ⟨k, this⟩
          omega
        rw [this]
        exact ih hk0
    rw [← hconst k hk]
    exact hl k hk
  · rintro ⟨j, hj⟩
    exact ⟨fun _ => j, fun k hk => hj k hk, by simp⟩

/-- Every chain contained in the union admits some labeling (with the
trivial switch bound given by the ground-set size). -/
theorem chainContained_union_switchBound {F : ι → Set (Finset α)}
    {C : MaximalChain α} (h : ChainContained (⋃ j, F j) C) :
    SwitchBound F C (Fintype.card α) := by
  classical
  have hchoice : ∀ k, ∃ j, k ≤ Fintype.card α → C.prefix k ∈ F j := by
    intro k
    by_cases hk : k ≤ Fintype.card α
    · obtain ⟨s, ⟨j, rfl⟩, hmem⟩ := h k hk
      exact ⟨j, fun _ => hmem⟩
    · obtain ⟨s, ⟨j, rfl⟩, hmem⟩ := h 0 (Nat.zero_le _)
      exact ⟨j, fun hk' => absurd hk' hk⟩
  choose l hl using hchoice
  refine ⟨l, fun k hk => hl k hk, ?_⟩
  calc ((Finset.range (Fintype.card α)).filter
        fun k => l (k + 1) ≠ l k).card
      ≤ (Finset.range (Fintype.card α)).card := Finset.card_filter_le _ _
    _ = Fintype.card α := Finset.card_range _

end MultiCopy

end BalancedChain
