import PlanarRecoloring.P3StripRecursive
import PlanarRecoloring.P3Obstruction

/-!
# Instantiating the recursive square strip in `R₃(P₃)`

`P3StripRecursive` proves the square component abstractly.  Here the four
corners are identified with the four states having a fixed middle colour in
the recolouring graph of `P₃`.  Thus each centre-colour component of
`R₃(P₃) □ Pₙ` receives a Hamilton-cycle certificate for every `n ≥ 2`.
The final splice between the three components is deliberately left as a
separate interface, matching the three-square argument in Chapter 4.
-/

namespace PlanarRecoloring

set_option maxHeartbeats 0
set_option maxRecDepth 100000

def p3SquareIndex (q : Fin 4) : Fin 4 :=
  if q = 2 then 3 else if q = 3 then 2 else q

def p3SquareState (b : Fin 3) (q : Fin 4) : P3State :=
  ⟨4 * b.val + (p3SquareIndex q).val, by omega⟩

def p3SquareStripState (b : Fin 3) (x : SquareStripState) :
    P3State × Nat :=
  (p3SquareState b x.1, x.2)

def p3SquareStripStates (b : Fin 3) (n : Nat) : List (P3State × Nat) :=
  (squareStripStates n).map (p3SquareStripState b)

def p3SquareStripAdjacent (x y : P3State × Nat) : Prop :=
  (x.2 = y.2 ∧ P3Adjacent x.1 y.1) ∨
    (x.1 = y.1 ∧ (x.2 + 1 = y.2 ∨ y.2 + 1 = x.2))

instance p3SquareStripAdjacentDecidable (x y : P3State × Nat) :
    Decidable (p3SquareStripAdjacent x y) := by
  unfold p3SquareStripAdjacent P3Adjacent p3AdjacentB
  infer_instance

private theorem p3_fin4_cases (q : Fin 4) :
    q = 0 ∨ q = 1 ∨ q = 2 ∨ q = 3 := by
  have h : q.val = 0 ∨ q.val = 1 ∨ q.val = 2 ∨ q.val = 3 := by omega
  rcases h with h | h | h | h
  · exact Or.inl (Fin.ext h)
  · exact Or.inr (Or.inl (Fin.ext h))
  · exact Or.inr (Or.inr (Or.inl (Fin.ext h)))
  · exact Or.inr (Or.inr (Or.inr (Fin.ext h)))

private theorem p3_fin3_cases (q : Fin 3) :
    q = 0 ∨ q = 1 ∨ q = 2 := by
  have h : q.val = 0 ∨ q.val = 1 ∨ q.val = 2 := by omega
  rcases h with h | h | h
  · exact Or.inl (Fin.ext h)
  · exact Or.inr (Or.inl (Fin.ext h))
  · exact Or.inr (Or.inr (Fin.ext h))

private theorem p3SquareIndex_injective : Function.Injective p3SquareIndex := by
  intro q r h
  rcases p3_fin4_cases q with rfl | rfl | rfl | rfl <;>
    rcases p3_fin4_cases r with rfl | rfl | rfl | rfl <;>
      simp [p3SquareIndex] at h ⊢

private theorem p3SquareState_injective (b : Fin 3) :
    Function.Injective (p3SquareState b) := by
  intro q r h
  apply p3SquareIndex_injective
  apply Fin.ext
  have hv := congrArg Fin.val h
  simp [p3SquareState] at hv
  omega

private theorem p3SquareState_adjacent (b : Fin 3) (q r : Fin 4)
    (h : square4Adjacent q r) :
    P3Adjacent (p3SquareState b q) (p3SquareState b r) := by
  rcases p3_fin3_cases b with rfl | rfl | rfl
  · rcases h with h | h | h | h | h | h | h | h
    all_goals rcases h with ⟨rfl, rfl⟩ <;> decide
  · rcases h with h | h | h | h | h | h | h | h
    all_goals rcases h with ⟨rfl, rfl⟩ <;> decide
  · rcases h with h | h | h | h | h | h | h | h
    all_goals rcases h with ⟨rfl, rfl⟩ <;> decide

private theorem p3SquareStripState_injective (b : Fin 3) :
    Function.Injective (p3SquareStripState b) := by
  intro x y h
  apply Prod.ext
  · exact p3SquareState_injective b (congrArg Prod.fst h)
  · exact congrArg (fun z : P3State × Nat => z.2) h

private theorem p3SquareStripState_rel (b : Fin 3) {x y : SquareStripState}
    (h : squareStripAdjacent x y) :
    p3SquareStripAdjacent (p3SquareStripState b x)
      (p3SquareStripState b y) := by
  rcases h with h | h
  · exact Or.inl ⟨h.1, p3SquareState_adjacent b _ _ h.2⟩
  · exact Or.inr ⟨congrArg (p3SquareState b) h.1, h.2⟩

private theorem hamiltonCycleOn_map {α β : Type} {vertices : List α}
    {r : α → α → Prop} {s : β → β → Prop} (f : α → β)
    (hf : Function.Injective f)
    (hrel : ∀ ⦃x y⦄, r x y → s (f x) (f y))
    (h : HamiltonCycleOn vertices r) :
    HamiltonCycleOn (vertices.map f) s := by
  have map_nodup : ∀ {xs : List α}, xs.Nodup → (xs.map f).Nodup := by
    intro xs hx
    induction xs with
    | nil => simp
    | cons a xs ih =>
      change (f a :: xs.map f).Nodup
      rw [List.nodup_cons] at hx ⊢
      refine ⟨?_, ih hx.2⟩
      intro hm
      rcases List.mem_map.mp hm with ⟨b, hb, hab⟩
      exact hx.1 (hf hab ▸ hb)
  have map_con : ∀ {xs : List α}, Consecutive r xs →
      Consecutive s (xs.map f) := by
    intro xs hx
    induction xs with
    | nil => trivial
    | cons a xs ih =>
      cases xs with
      | nil => trivial
      | cons b bs => exact ⟨hrel hx.1, ih hx.2⟩
  rcases h with ⟨path, hn, hc, hclosed⟩
  rcases hclosed with ⟨a, z, ha, hz, hw, hclose⟩
  refine ⟨path.map f, map_nodup hn, ?_, ?_⟩
  · intro x
    constructor
    · intro hx
      rcases List.mem_map.mp hx with ⟨y, hy, rfl⟩
      exact List.mem_map_of_mem ((hc y).mp hy)
    · intro hx
      rcases List.mem_map.mp hx with ⟨y, hy, rfl⟩
      exact List.mem_map_of_mem ((hc y).mpr hy)
  · refine ⟨f a, f z, ?_, ?_, map_con hw, hrel hclose⟩
    · rw [List.head?_map, ha]
      rfl
    · rw [List.getLast?_map, hz]
      rfl

/-- The square-strip theorem instantiated in the `P₃` recolouring graph. -/
theorem p3_square_strip_hamiltonCycle (b : Fin 3) (n : Nat) (hn : 2 ≤ n) :
    HamiltonCycleOn (p3SquareStripStates b n) p3SquareStripAdjacent := by
  apply hamiltonCycleOn_map (p3SquareStripState b)
    (p3SquareStripState_injective b)
    (fun {x y} h => p3SquareStripState_rel b h)
  exact square_strip_hamiltonCycle n hn

end PlanarRecoloring
