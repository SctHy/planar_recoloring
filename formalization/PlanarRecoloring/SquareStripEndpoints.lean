import PlanarRecoloring.P3StripRecursive

/-!
# A fixed endpoint path for square strips

The recursive certificate alternates the two neighbours of corner `0` as it
retains a fresh cut edge.  Swapping the two neighbours is an automorphism of
the square, so the endpoint pair can be normalized uniformly.  This exposes
the `q₃ → q₀` path needed by the three-square splice in the bad-run proof.
-/

namespace PlanarRecoloring

set_option maxHeartbeats 0
set_option maxRecDepth 100000

def squareFlipIndex (q : Fin 4) : Fin 4 :=
  if q = 1 then 3 else if q = 3 then 1 else q

def squareFlipState (x : SquareStripState) : SquareStripState :=
  (squareFlipIndex x.1, x.2)

private theorem square_fin4_cases (q : Fin 4) :
    q = 0 ∨ q = 1 ∨ q = 2 ∨ q = 3 := by
  have h : q.val = 0 ∨ q.val = 1 ∨ q.val = 2 ∨ q.val = 3 := by omega
  rcases h with h | h | h | h
  · exact Or.inl (Fin.ext h)
  · exact Or.inr (Or.inl (Fin.ext h))
  · exact Or.inr (Or.inr (Or.inl (Fin.ext h)))
  · exact Or.inr (Or.inr (Or.inr (Fin.ext h)))

private theorem squareFlipIndex_injective : Function.Injective squareFlipIndex := by
  intro q r h
  rcases square_fin4_cases q with rfl | rfl | rfl | rfl <;>
    rcases square_fin4_cases r with rfl | rfl | rfl | rfl <;>
      simp [squareFlipIndex] at h ⊢

private theorem squareFlip_injective : Function.Injective squareFlipState := by
  intro x y h
  have hfst : x.1 = y.1 :=
    squareFlipIndex_injective (congrArg Prod.fst h)
  have hsnd' := congrArg Prod.snd h
  have hsnd : x.2 = y.2 := by
    simpa [squareFlipState] using hsnd'
  exact Prod.ext hfst hsnd

private theorem squareFlip_involutive (x : SquareStripState) :
    squareFlipState (squareFlipState x) = x := by
  rcases x with ⟨q, i⟩
  rcases square_fin4_cases q with rfl | rfl | rfl | rfl <;>
    simp [squareFlipState, squareFlipIndex]

private theorem squareFlipIndex_adjacent {q r : Fin 4}
    (h : square4Adjacent q r) :
    square4Adjacent (squareFlipIndex q) (squareFlipIndex r) := by
  rcases square_fin4_cases q with rfl | rfl | rfl | rfl <;>
    rcases square_fin4_cases r with rfl | rfl | rfl | rfl <;>
      simp [squareFlipIndex, square4Adjacent] at h ⊢

private theorem squareFlip_adjacent {x y : SquareStripState}
    (h : squareStripAdjacent x y) :
    squareStripAdjacent (squareFlipState x) (squareFlipState y) := by
  rcases h with h | h
  · refine Or.inl ⟨h.1, ?_⟩
    exact squareFlipIndex_adjacent h.2
  · exact Or.inr ⟨congrArg squareFlipIndex h.1, h.2⟩

private theorem squareFlip_states_mem_forward : ∀ (n : Nat)
    (x : SquareStripState), x ∈ squareStripStates n →
      squareFlipState x ∈ squareStripStates n
  | 0, x, hx => by simp [squareStripStates] at hx
  | n + 1, x, hx => by
      rw [squareStripStates_succ] at hx ⊢
      rcases List.mem_append.mp hx with h | h
      · exact List.mem_append.mpr (Or.inl
          (squareFlip_states_mem_forward n x h))
      · simp [squareLayer] at h ⊢
        rcases h with rfl | rfl | rfl | rfl <;>
          simp [squareFlipState, squareFlipIndex, squareLayer]

private theorem squareFlip_states_mem (n : Nat) (x : SquareStripState) :
    x ∈ squareStripStates n ↔ squareFlipState x ∈ squareStripStates n := by
  constructor
  · exact squareFlip_states_mem_forward n x
  · intro hx
    have h' := squareFlip_states_mem_forward n (squareFlipState x) hx
    rw [squareFlip_involutive] at h'
    exact h'

/-- Every square strip has an endpoint-prescribed path from corner `q₃` to
corner `q₀` in its newest layer. -/
theorem square_strip_q3_q0_path (n : Nat) (hn : 2 ≤ n) :
    HamiltonPathOn (squareStripStates n) squareStripAdjacent
      (3, n - 1) (0, n - 1) := by
  rcases squareStripCertificate_exists n hn with ⟨c⟩
  cases ho : c.orientation with
  | true =>
      have hbase : HamiltonPathOn (squareStripStates n) squareStripAdjacent
          (1, n - 1) (0, n - 1) := by
        simpa [ho] using c.openProof
      have hmap := hbase.map squareFlipState squareFlip_injective
        (fun {x y} h => squareFlip_adjacent h)
      have hvertices : ∀ x : SquareStripState,
          x ∈ (squareStripStates n).map squareFlipState ↔
            x ∈ squareStripStates n := by
        intro x
        constructor
        · intro hx
          rcases List.mem_map.mp hx with ⟨y, hy, rfl⟩
          exact (squareFlip_states_mem n y).mp hy
        · intro hx
          let y := squareFlipState x
          have hy : y ∈ squareStripStates n :=
            (squareFlip_states_mem n x).mp hx
          apply List.mem_map.mpr
          refine ⟨y, hy, ?_⟩
          exact squareFlip_involutive x
      exact hmap.congr_vertices hvertices
  | false =>
      simpa [ho] using c.openProof

end PlanarRecoloring
