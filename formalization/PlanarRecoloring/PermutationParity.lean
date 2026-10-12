import PlanarRecoloring.General

namespace PlanarRecoloring

theorem perm_fin3_cases (i : Fin 3) : i = 0 ∨ i = 1 ∨ i = 2 := by
  refine Fin.cases (Or.inl rfl) ?_ i
  intro j
  refine Fin.cases (Or.inr (Or.inl rfl)) ?_ j
  intro k
  refine Fin.cases (Or.inr (Or.inr rfl)) ?_ k
  intro l
  exact Fin.elim0 l

theorem perm_fin2_cases (i : Fin 2) : i = 0 ∨ i = 1 := by
  refine Fin.cases (Or.inl rfl) ?_ i
  intro j
  exact Fin.cases (Or.inr rfl) (fun k => Fin.elim0 k) j

/-! A finite `K₂` obstruction for the `d = 1`, `k = d+2` sharpness
bound.  A proper colouring of `K₂` with three colours is an ordered pair
of different colours.  Appending the unique unused colour gives a
permutation of the three-colour palette. -/

def K2Graph : FiniteGraph 2 :=
  { adj := fun u v => decide (u ≠ v) }

structure K2Coloring where
  x : Fin 3
  y : Fin 3
  distinct : x ≠ y

 def K2Coloring.toFun (s : K2Coloring) : Fin 2 → Fin 3 :=
  fun i => Fin.cases s.x (fun _ => s.y) i

def K2Coloring.toColoring (s : K2Coloring) : Coloring K2Graph 3 := by
  refine ⟨s.toFun, ?_⟩
  intro u v huv heq
  have hne : u ≠ v := by
    intro huv'
    subst v
    change decide (u ≠ u) = true at huv
    simp at huv
  have hc : u = 0 ∨ u = 1 := by
    refine Fin.cases (Or.inl rfl) ?_ u
    intro w
    refine Fin.cases (Or.inr rfl) ?_ w
    intro z
    exact Fin.elim0 z
  have hd : v = 0 ∨ v = 1 := by
    refine Fin.cases (Or.inl rfl) ?_ v
    intro w
    refine Fin.cases (Or.inr rfl) ?_ w
    intro z
    exact Fin.elim0 z
  rcases hc with rfl | rfl <;> rcases hd with rfl | rfl
  · exact False.elim (hne rfl)
  · apply s.distinct
    change s.x = s.y at heq
    exact heq
  · apply s.distinct
    change s.y = s.x at heq
    exact heq.symm
  · exact False.elim (hne rfl)

/-- All six proper colourings of `K₂` are represented without quotienting.
The relation is exactly one legal one-vertex recolouring. -/
def K2Adjacent (s t : K2Coloring) : Prop :=
  (s.x ≠ t.x ∧ s.y = t.y) ∨ (s.x = t.x ∧ s.y ≠ t.y)

theorem K2Adjacent.symm {s t : K2Coloring} :
    K2Adjacent s t → K2Adjacent t s := by
  intro h
  rcases h with ⟨hxy, hysame⟩ | ⟨hxsame, hyx⟩
  · exact Or.inl ⟨Ne.symm hxy, hysame.symm⟩
  · exact Or.inr ⟨hxsame.symm, Ne.symm hyx⟩

theorem k2_adj_recolour_adjacent {s t : K2Coloring}
    (h : K2Adjacent s t) :
    RecolourAdjacent s.toColoring t.toColoring := by
  rcases h with ⟨hxy, hysame⟩ | ⟨hxsame, hyx⟩
  · refine ⟨0, ?_, ?_⟩
    · change s.x ≠ t.x
      exact hxy
    · intro w hw
      rcases perm_fin2_cases w with rfl | rfl
      · exact False.elim (hw rfl)
      · exact hysame
  · refine ⟨1, ?_, ?_⟩
    · change s.y ≠ t.y
      exact hyx
    · intro w hw
      rcases perm_fin2_cases w with rfl | rfl
      · exact hxsame
      · exact False.elim (hw rfl)

theorem k2_recolour_adjacent_iff {s t : K2Coloring} :
    K2Adjacent s t ↔ RecolourAdjacent s.toColoring t.toColoring := by
  constructor
  · exact k2_adj_recolour_adjacent
  · intro h
    rcases h with ⟨v, hv, hrest⟩
    rcases perm_fin2_cases v with rfl | rfl
    · left
      constructor
      · change s.x ≠ t.x at hv
        exact hv
      · change s.y = t.y
        exact hrest 1 (by decide)
    · right
      constructor
      · change s.x = t.x
        exact hrest 0 (by decide)
      · change s.y ≠ t.y at hv
        exact hv

/-- The colour omitted by a proper `K₂` colouring. -/
def k2Missing (s : K2Coloring) : Fin 3 :=
  if s.x = 0 then
    if s.y = 1 then 2 else 1
  else if s.x = 1 then
    if s.y = 0 then 2 else 0
  else if s.y = 0 then 1 else 0

/-- The appended tuple is a permutation of the palette. -/
structure Permutation3 where
  a : Fin 3
  b : Fin 3
  c : Fin 3
  hab : a ≠ b
  hac : a ≠ c
  hbc : b ≠ c

def K2Coloring.toPermutation3 (s : K2Coloring) : Permutation3 := by
  refine ⟨s.x, s.y, k2Missing s, s.distinct, ?_, ?_⟩
  · rcases perm_fin3_cases s.x with hxs | hxs | hxs <;>
      rcases perm_fin3_cases s.y with hys | hys | hys <;>
      have hs := s.distinct <;>
      simp [hxs, hys, k2Missing] at hs ⊢
  · rcases perm_fin3_cases s.x with hxs | hxs | hxs <;>
      rcases perm_fin3_cases s.y with hys | hys | hys <;>
      have hs := s.distinct <;>
      simp [hxs, hys, k2Missing] at hs ⊢

/-- Inversion parity of a three-element permutation.  For a permutation
`(a,b,c)` this is the parity of its inversion count; since `c` is the
unique remaining value, the displayed two-coordinate decision computes it. -/
def permutationParity3 (p : Permutation3) : Bool :=
  if p.a = 0 then p.b = 2
  else if p.a = 1 then p.b = 0
  else p.b = 1

def K2Parity (s : K2Coloring) : Bool :=
  permutationParity3 s.toPermutation3

/-- Every recolouring edge of the `K₂` obstruction changes permutation parity. -/
theorem k2_adj_parity_flip (s t : K2Coloring) (h : K2Adjacent s t) :
    K2Parity s != K2Parity t := by
  rcases perm_fin3_cases s.x with hxs | hxs | hxs <;>
    rcases perm_fin3_cases s.y with hys | hys | hys <;>
    rcases perm_fin3_cases t.x with htx | htx | htx <;>
    rcases perm_fin3_cases t.y with hty | hty | hty <;>
    all_goals
      have hs := s.distinct
      have ht := t.distinct
      simp [hxs, hys, htx, hty, K2Adjacent, K2Parity,
        K2Coloring.toPermutation3, permutationParity3, k2Missing] at hs ht h ⊢

/-- A six-vertex spanning path in the recolouring graph of `K₂`. -/
def K2HamiltonPath (s t : K2Coloring) : Prop :=
  ∃ a b c d e f : K2Coloring,
    a = s ∧ f = t ∧
    a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ a ≠ e ∧ a ≠ f ∧
    b ≠ c ∧ b ≠ d ∧ b ≠ e ∧ b ≠ f ∧
    c ≠ d ∧ c ≠ e ∧ c ≠ f ∧
    d ≠ e ∧ d ≠ f ∧ e ≠ f ∧
    K2Adjacent a b ∧ K2Adjacent b c ∧ K2Adjacent c d ∧
    K2Adjacent d e ∧ K2Adjacent e f

def K2Triangle : Prop :=
  ∃ a b c : K2Coloring,
    K2Adjacent a b ∧ K2Adjacent b c ∧ K2Adjacent c a

 def k2s01 : K2Coloring := ⟨0, 1, by decide⟩
def k2s12 : K2Coloring := ⟨1, 2, by decide⟩

theorem bool_five_flips {a b c d e f : Bool}
    (hab : a != b) (hbc : b != c) (hcd : c != d)
    (hde : d != e) (hef : e != f) : a != f := by
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;>
    simp_all

theorem k2_not_hamilton_connected :
    ¬ (∀ s t : K2Coloring, s ≠ t → K2HamiltonPath s t) := by
  intro h
  have hneq : k2s01 ≠ k2s12 := by
    intro heq
    have hx : (0 : Fin 3) = 1 := congrArg K2Coloring.x heq
    exact Fin.zero_ne_one hx
  have hp := h k2s01 k2s12 hneq
  rcases hp with ⟨a, b, c, d, e, f, ha, hf, hab, hac, had, hae, haf,
    hbc, hbd, hbe, hbf, hcd, hce, hcf, hde, hdf, hef, hab', hbc', hcd', hde', hef'⟩
  have h₁ := k2_adj_parity_flip a b hab'
  have h₂ := k2_adj_parity_flip b c hbc'
  have h₃ := k2_adj_parity_flip c d hcd'
  have h₄ := k2_adj_parity_flip d e hde'
  have h₅ := k2_adj_parity_flip e f hef'
  have hodd := bool_five_flips h₁ h₂ h₃ h₄ h₅
  rw [ha, hf] at hodd
  simp [K2Parity, K2Coloring.toPermutation3, permutationParity3,
    k2Missing, k2s01, k2s12] at hodd

theorem k2_has_no_triangle : ¬ K2Triangle := by
  rintro ⟨a, b, c, hab, hbc, hca⟩
  have h₁ := k2_adj_parity_flip a b hab
  have h₂ := k2_adj_parity_flip b c hbc
  have h₃ := k2_adj_parity_flip c a hca
  cases hp : K2Parity a <;> cases hq : K2Parity b <;>
    cases hr : K2Parity c <;> simp_all

end PlanarRecoloring
