import PlanarRecoloring.P3Strip
import PlanarRecoloring.BinaryEndpoints

/-!
# Arbitrary-length bad runs

This proves `prop:badrun` for the actual twelve-state graph `R₃(P₃)`.
Two- and three-layer paths have prescribed adjacent endpoints in their last
layer.  A two-layer block has a retained first-layer edge; replacing that edge
by the previous strip appends two layers and keeps the same last-layer
endpoints.  Thus the construction covers every length at least two.
Natural-number layer tags avoid casts during the recursion.
-/

namespace PlanarRecoloring

set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev P3RunState := P3State × Nat

def P3RunAdjacent (x y : P3RunState) : Prop :=
  (x.2 = y.2 ∧ P3Adjacent x.1 y.1) ∨
    (x.1 = y.1 ∧ (x.2 + 1 = y.2 ∨ y.2 + 1 = x.2))

instance p3RunAdjacentDecidable (x y : P3RunState) :
    Decidable (P3RunAdjacent x y) := by
  unfold P3RunAdjacent
  infer_instance

def p3RunLayer (i : Nat) : List P3RunState :=
  (List.finRange 12).map (fun s => (s, i))

def p3RunStates : Nat → List P3RunState
  | 0 => []
  | n + 1 => p3RunStates n ++ p3RunLayer n

theorem p3RunLayer_mem_iff (i : Nat) (x : P3RunState) :
    x ∈ p3RunLayer i ↔ x.2 = i := by
  rcases x with ⟨s, layer⟩
  simp [p3RunLayer, Prod.mk.injEq, eq_comm]

theorem p3RunStates_mem_iff : ∀ n (x : P3RunState),
    x ∈ p3RunStates n ↔ x.2 < n := by
  intro n
  induction n with
  | zero => intro x; simp [p3RunStates]
  | succ n ih =>
      intro x
      simp only [p3RunStates, List.mem_append, ih, p3RunLayer_mem_iff]
      omega

def p3BlockShift (n : Nat) (x : P3StripState) : P3RunState :=
  (x.1, n + x.2.val)

private theorem p3BlockShift_injective (n : Nat) :
    Function.Injective (p3BlockShift n) := by
  intro x y h
  apply Prod.ext
  · change x.1 = y.1
    simpa [p3BlockShift] using congrArg Prod.fst h
  · apply Fin.ext
    have heq := congrArg Prod.snd h
    change n + x.2.val = n + y.2.val at heq
    omega

private theorem p3BlockShift_adjacent (n : Nat)
    {x y : P3StripState} (h : P3StripAdjacent x y) :
    P3RunAdjacent (p3BlockShift n x) (p3BlockShift n y) := by
  rcases h with ⟨hl, ha⟩ | ⟨hs, hl⟩
  · exact Or.inl ⟨congrArg (fun l : Fin 2 => n + l.val) hl, ha⟩
  · apply Or.inr
    refine ⟨hs, ?_⟩
    have hx := x.2.isLt
    have hy := y.2.isLt
    have hne : x.2.val ≠ y.2.val := by
      intro hv
      exact hl (Fin.ext hv)
    dsimp [p3BlockShift]
    omega

def p3BlockPrefix : List P3StripState :=
  [(0, 1), (2, 1), (3, 1), (7, 1), (5, 1), (5, 0),
   (4, 0), (8, 0), (9, 0), (9, 1), (11, 1), (11, 0),
   (10, 0), (10, 1), (8, 1), (4, 1), (6, 1), (6, 0),
   (7, 0), (3, 0), (2, 0), (0, 0)]

def p3BlockSuffix : List P3StripState := [(1, 0), (1, 1)]

private theorem p3BlockPrefix_path :
    HamiltonPathOn p3BlockPrefix P3StripAdjacent (0, 1) (0, 0) := by
  refine ⟨p3BlockPrefix, by decide, by decide, by decide, ?_, ?_⟩
  · intro x; rfl
  · simp only [p3BlockPrefix, Consecutive]
    decide

private theorem p3BlockSuffix_path :
    HamiltonPathOn p3BlockSuffix P3StripAdjacent (1, 0) (1, 1) := by
  refine ⟨p3BlockSuffix, by decide, by decide, by decide, ?_, ?_⟩
  · intro x; rfl
  · simp only [p3BlockSuffix, Consecutive]
    decide

private theorem p3Block_disjoint : DisjointLists p3BlockPrefix p3BlockSuffix := by
  have h : ∀ s : Fin 12, ∀ l : Fin 2,
      (s, l) ∈ p3BlockPrefix → (s, l) ∉ p3BlockSuffix := by decide
  intro x hx
  exact h x.1 x.2 hx

private theorem p3Block_covers : ∀ s : Fin 12, ∀ l : Fin 2,
    (s, l) ∈ p3BlockPrefix ∨ (s, l) ∈ p3BlockSuffix := by decide

def p3ShiftedPrefix (n : Nat) : List P3RunState :=
  p3BlockPrefix.map (p3BlockShift n)

def p3ShiftedSuffix (n : Nat) : List P3RunState :=
  p3BlockSuffix.map (p3BlockShift n)

private theorem p3ShiftedPrefix_path (n : Nat) :
    HamiltonPathOn (p3ShiftedPrefix n) P3RunAdjacent (0, n + 1) (0, n) := by
  simpa [p3ShiftedPrefix, p3BlockShift] using
    p3BlockPrefix_path.map (p3BlockShift n) (p3BlockShift_injective n)
      (fun {_ _} h => p3BlockShift_adjacent n h)

private theorem p3ShiftedSuffix_path (n : Nat) :
    HamiltonPathOn (p3ShiftedSuffix n) P3RunAdjacent (1, n) (1, n + 1) := by
  simpa [p3ShiftedSuffix, p3BlockShift] using
    p3BlockSuffix_path.map (p3BlockShift n) (p3BlockShift_injective n)
      (fun {_ _} h => p3BlockShift_adjacent n h)

private theorem p3Shifted_mem_lower_bound (n : Nat) {x : P3RunState}
    (h : x ∈ p3ShiftedPrefix n ∨ x ∈ p3ShiftedSuffix n) : n ≤ x.2 := by
  rcases h with h | h
  all_goals
    rcases List.mem_map.mp h with ⟨y, _, rfl⟩
    simp [p3BlockShift]

private theorem p3Shifted_disjoint (n : Nat) :
    DisjointLists (p3ShiftedPrefix n) (p3ShiftedSuffix n) := by
  intro x hx hy
  rcases List.mem_map.mp hx with ⟨a, ha, rfl⟩
  rcases List.mem_map.mp hy with ⟨b, hb, heq⟩
  have hba := p3BlockShift_injective n heq
  exact p3Block_disjoint ha (hba ▸ hb)

private theorem p3Shifted_covers (n : Nat) (x : P3RunState) :
    (x ∈ p3ShiftedPrefix n ∨ x ∈ p3ShiftedSuffix n) ↔
      x.2 = n ∨ x.2 = n + 1 := by
  constructor
  · intro h
    rcases h with h | h
    all_goals
      rcases List.mem_map.mp h with ⟨y, _, rfl⟩
      have hy := y.2.isLt
      dsimp [p3BlockShift]
      omega
  · intro h
    rcases x with ⟨s, layer⟩
    rcases h with h | h
    · change layer = n at h
      subst layer
      rcases p3Block_covers s 0 with h | h
      · exact Or.inl (List.mem_map.mpr ⟨(s, 0), h, by simp [p3BlockShift]⟩)
      · exact Or.inr (List.mem_map.mpr ⟨(s, 0), h, by simp [p3BlockShift]⟩)
    · change layer = n + 1 at h
      subst layer
      rcases p3Block_covers s 1 with h | h
      · exact Or.inl (List.mem_map.mpr ⟨(s, 1), h, by simp [p3BlockShift]⟩)
      · exact Or.inr (List.mem_map.mpr ⟨(s, 1), h, by simp [p3BlockShift]⟩)

private theorem p3Run_open_step {n : Nat} (hn : 2 ≤ n)
    (h : HamiltonPathOn (p3RunStates n) P3RunAdjacent (0, n - 1) (1, n - 1)) :
    HamiltonPathOn (p3RunStates (n + 2)) P3RunAdjacent (0, n + 1) (1, n + 1) := by
  have hdis₁ : DisjointLists (p3ShiftedPrefix n) (p3RunStates n) := by
    intro x hx hy
    have hge := p3Shifted_mem_lower_bound n (Or.inl hx)
    have hlt := (p3RunStates_mem_iff n x).mp hy
    omega
  have hedge₁ : P3RunAdjacent (0, n) (0, n - 1) := by
    apply Or.inr
    refine ⟨rfl, Or.inr ?_⟩
    omega
  have hp := (p3ShiftedPrefix_path n).appendOn h hdis₁ hedge₁
  have hdis₂ : DisjointLists (p3ShiftedPrefix n ++ p3RunStates n)
      (p3ShiftedSuffix n) := by
    intro x hx hy
    rcases List.mem_append.mp hx with hx | hx
    · exact p3Shifted_disjoint n hx hy
    · have hge := p3Shifted_mem_lower_bound n (Or.inr hy)
      have hlt := (p3RunStates_mem_iff n x).mp hx
      omega
  have hedge₂ : P3RunAdjacent (1, n - 1) (1, n) := by
    apply Or.inr
    refine ⟨rfl, Or.inl ?_⟩
    omega
  have hjoined := hp.appendOn (p3ShiftedSuffix_path n) hdis₂ hedge₂
  apply hjoined.congr_vertices
  intro x
  have hf := p3Shifted_covers n x
  have ho := p3RunStates_mem_iff n x
  have hn' := p3RunStates_mem_iff (n + 2) x
  simp only [List.mem_append]
  rw [hn']
  constructor
  · intro hx
    rcases hx with (hx | hx) | hx
    · have hx' := hf.mp (Or.inl hx); omega
    · have hx' := ho.mp hx; omega
    · have hx' := hf.mp (Or.inr hx); omega
  · intro hx
    by_cases hlt : x.2 < n
    · exact Or.inl (Or.inr (ho.mpr hlt))
    · have hx' : x.2 = n ∨ x.2 = n + 1 := by omega
      rcases hf.mpr hx' with hp | hs
      · exact Or.inl (Or.inl hp)
      · exact Or.inr hs

private theorem p3Run_open_two :
    HamiltonPathOn (p3RunStates 2) P3RunAdjacent (0, 1) (1, 1) := by
  have ha : P3RunAdjacent (0, 0) (1, 0) := Or.inl ⟨rfl, by decide⟩
  have h := (p3ShiftedPrefix_path 0).appendOn (p3ShiftedSuffix_path 0)
    (p3Shifted_disjoint 0) ha
  apply h.congr_vertices
  intro x
  simp only [List.mem_append]
  rw [p3Shifted_covers, p3RunStates_mem_iff]
  omega

def p3RunThreePath : List P3RunState :=
  [(0, 2), (2, 2), (2, 1), (2, 0), (0, 0), (0, 1),
   (1, 1), (1, 0), (3, 0), (3, 1), (7, 1), (7, 0),
   (5, 0), (5, 1), (5, 2), (4, 2), (4, 1), (8, 1),
   (8, 2), (9, 2), (9, 1), (9, 0), (11, 0), (11, 1),
   (11, 2), (10, 2), (10, 1), (10, 0), (8, 0), (4, 0),
   (6, 0), (6, 1), (6, 2), (7, 2), (3, 2), (1, 2)]

private theorem p3Run_open_three :
    HamiltonPathOn (p3RunStates 3) P3RunAdjacent (0, 2) (1, 2) := by
  refine ⟨p3RunThreePath, by decide, by decide, by decide, ?_, ?_⟩
  · intro x
    have hsmall : ∀ s : Fin 12, ∀ l : Fin 3,
        (s, l.val) ∈ p3RunStates 3 ↔ (s, l.val) ∈ p3RunThreePath := by decide
    by_cases hlt : x.2 < 3
    · exact hsmall x.1 ⟨x.2, hlt⟩
    · have hv : x ∉ p3RunStates 3 := by
        simpa only [p3RunStates_mem_iff] using hlt
      have hp : x ∉ p3RunThreePath := by
        intro hx
        simp only [p3RunThreePath, List.mem_cons, List.not_mem_nil, or_false] at hx
        rcases hx with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
          rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
          rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
          rfl | rfl | rfl | rfl | rfl <;> omega
      exact iff_of_false hv hp
  · simp only [p3RunThreePath, Consecutive]
    decide

theorem p3Run_hamiltonPath_last : ∀ n, 2 ≤ n →
    HamiltonPathOn (p3RunStates n) P3RunAdjacent (0, n - 1) (1, n - 1)
  | 0, hn => by omega
  | 1, hn => by omega
  | 2, _ => p3Run_open_two
  | 3, _ => p3Run_open_three
  | n + 4, _ => by
      have hprev : 2 ≤ n + 2 := by omega
      exact p3Run_open_step hprev (p3Run_hamiltonPath_last (n + 2) hprev)

/-- The full arbitrary-length bad-run proposition: the actual recolouring
graph of `P₃`, multiplied by the path on `n` layers, is Hamiltonian. -/
theorem p3_badrun_hamiltonCycle (n : Nat) (hn : 2 ≤ n) :
    HamiltonCycleOn (p3RunStates n) P3RunAdjacent := by
  rcases p3Run_hamiltonPath_last n hn with ⟨path, hs, ht, hnodup, hcover, hwalk⟩
  refine ⟨path, hnodup, hcover, (0, n - 1), (1, n - 1), hs, ht, hwalk, ?_⟩
  exact Or.inl ⟨rfl, (by decide : P3Adjacent 1 0)⟩

end PlanarRecoloring
