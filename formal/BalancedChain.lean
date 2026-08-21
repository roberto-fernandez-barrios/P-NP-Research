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

end BalancedChain
