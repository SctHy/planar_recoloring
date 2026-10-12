import PlanarRecoloring.P3Obstruction

/-!
# The first two-layer bad-run base case

The Chapter 4 bad-run construction starts with the product of the recolouring
graph of `P₃` and a two-vertex layer.  This file records that finite base case
directly.  It is a kernel-checked certificate for the 24-state strip; it does
not claim the arbitrary-length bad-run theorem.
-/

namespace PlanarRecoloring

set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev P3StripState := P3State × Fin 2

def P3StripAdjacent (x y : P3StripState) : Prop :=
  (x.2 = y.2 ∧ P3Adjacent x.1 y.1) ∨
    (x.1 = y.1 ∧ x.2 ≠ y.2)

instance p3StripAdjacentDecidable (x y : P3StripState) :
    Decidable (P3StripAdjacent x y) := by
  unfold P3StripAdjacent
  infer_instance

def P3StripStates : List P3StripState :=
  (List.finRange 12).flatMap (fun s =>
    (List.finRange 2).map (fun layer => (s, layer)))

def P3StripCycle : List P3StripState :=
  [ (0, 0), (1, 0), (1, 1), (0, 1),
    (2, 1), (3, 1), (7, 1), (5, 1),
    (5, 0), (4, 0), (8, 0), (9, 0),
    (9, 1), (11, 1), (11, 0), (10, 0),
    (10, 1), (8, 1), (4, 1), (6, 1),
    (6, 0), (7, 0), (3, 0), (2, 0) ]

theorem p3_strip_two_hamiltonCycleOn :
    HamiltonCycleOn P3StripStates P3StripAdjacent := by
  refine ⟨P3StripCycle, ?_, ?_, ?_⟩
  · decide
  · have hc : ∀ s : Fin 12, ∀ layer : Fin 2,
        (s, layer) ∈ P3StripStates ↔ (s, layer) ∈ P3StripCycle := by decide
    intro x
    exact hc x.1 x.2
  · refine ⟨(0, 0), (2, 0), ?_, ?_, ?_, ?_⟩
    · decide
    · decide
    · simp only [P3StripCycle, Consecutive]
      decide
    · decide

end PlanarRecoloring
