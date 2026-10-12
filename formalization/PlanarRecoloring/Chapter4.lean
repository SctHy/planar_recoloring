import PlanarRecoloring.General
import PlanarRecoloring.Hamilton
import PlanarRecoloring.PairFiveTransport
import PlanarRecoloring.P3Obstruction

/-!
# Chapter 4: isolated-state obstructions

The sharpness arguments in Chapter 4 use frozen colourings.  A frozen state
has no incident recolouring edge, so it cannot be an endpoint of a spanning
path to a different state and cannot occur in a Hamilton cycle of a symmetric
state relation with another vertex.  These statements are independent of the
planar structural lemmas and the external colouring theorems used for the
upper bounds.
-/

namespace PlanarRecoloring

private theorem member_in_tail_has_incident
    {α : Type u} {r : α → α → Prop} {s prev : α}
    {xs : List α} (hcon : Consecutive r (prev :: xs))
    (hs : s ∈ xs) : ∃ y, r s y ∨ r y s := by
  cases xs with
  | nil => simp at hs
  | cons x xs =>
      by_cases hsx : s = x
      · subst s
        exact ⟨prev, Or.inr hcon.1⟩
      · have hs' : s ∈ xs := by
          simp only [List.mem_cons] at hs
          rcases hs with h | h
          · exact False.elim (hsx h)
          · exact h
        exact member_in_tail_has_incident hcon.2 hs'

private theorem member_in_path_has_incident
    {α : Type u} {r : α → α → Prop} {s : α}
    {path : List α} (hcon : Consecutive r path)
    (hpath : path ≠ []) (hlen : 2 ≤ path.length)
    (hs : s ∈ path) : ∃ y, r s y ∨ r y s := by
  cases path with
  | nil => exact False.elim (hpath rfl)
  | cons x xs =>
      cases xs with
      | nil => simp at hlen
      | cons y ys =>
          simp only [List.mem_cons] at hs
          rcases hs with rfl | hs
          · exact ⟨y, Or.inl hcon.1⟩
          · exact member_in_tail_has_incident hcon (by simp [hs])

theorem no_hamiltonPathOn_from_isolated
    {α : Type u} {vertices : List α} {r : α → α → Prop}
    {s t : α} (hs : s ∈ vertices) (ht : t ∈ vertices) (hst : s ≠ t)
    (hisol : ∀ y, ¬ r s y) :
    ¬ HamiltonPathOn vertices r s t := by
  intro h
  rcases h with ⟨path, hhead, hlast, hnodup, hcover, hcon⟩
  have hsmem : s ∈ path := (hcover s).mp hs
  have htem : t ∈ path := (hcover t).mp ht
  rcases List.head?_eq_some_iff.mp hhead with ⟨tail, hpath⟩
  subst path
  have htail : t ∈ tail := by
    simp only [List.mem_cons] at htem
    rcases htem with hst' | ht'
    · exact False.elim (hst hst'.symm)
    · exact ht'
  cases tail with
  | nil => simp at htail
  | cons y ys => exact hisol y hcon.1

theorem no_hamiltonCycleOn_from_isolated
    {α : Type u} {vertices : List α} {r : α → α → Prop}
    {s t : α} (hs : s ∈ vertices) (ht : t ∈ vertices) (hst : s ≠ t)
    (hsym : ∀ ⦃x y⦄, r x y → r y x)
    (hisol : ∀ y, ¬ r s y) :
    ¬ HamiltonCycleOn vertices r := by
  intro h
  rcases h with ⟨path, hnodup, hcover, hclosed⟩
  rcases hclosed with ⟨head, last, hhead, hlast, hcon, hclose⟩
  have hsmem : s ∈ path := (hcover s).mp hs
  have htem : t ∈ path := (hcover t).mp ht
  have hpath : path ≠ [] := by
    intro hnil
    subst path
    simp at hsmem
  have hlen : 2 ≤ path.length := by
    cases path with
    | nil => exact False.elim (hpath rfl)
    | cons x xs =>
        cases xs with
        | nil =>
            have hsx : s = x := by simpa using hsmem
            have htx : t = x := by simpa using htem
            exact False.elim (hst (hsx.trans htx.symm))
        | cons y ys => simp
  rcases member_in_path_has_incident hcon hpath hlen hsmem with
    ⟨y, hsy | hys⟩
  · exact hisol y hsy
  · exact hisol y (hsym hys)

theorem frozen_not_hamiltonConnectedOn
    {n k : Nat} {G : FiniteGraph n} {c : Coloring G k}
    (hf : FrozenColoring (G := G) c) {states : List (Coloring G k)}
    {t : Coloring G k} (hc : c ∈ states) (ht : t ∈ states) (hct : c ≠ t) :
    ¬ HamiltonConnectedOn states (fun x y => RecolourAdjacent x y) := by
  intro h
  exact no_hamiltonPathOn_from_isolated hc ht hct (frozen_isolated hf)
    (h c t hc ht hct)

theorem frozen_not_hamiltonCycleOn
    {n k : Nat} {G : FiniteGraph n} {c : Coloring G k}
    (hf : FrozenColoring (G := G) c) {states : List (Coloring G k)}
    {t : Coloring G k} (hc : c ∈ states) (ht : t ∈ states) (hct : c ≠ t) :
    ¬ HamiltonCycleOn states (fun x y => RecolourAdjacent x y) := by
  exact no_hamiltonCycleOn_from_isolated hc ht hct
    (fun {x y} hxy => recolour_adjacent_symm hxy) (frozen_isolated hf)

/-!
The finite adjacent-pair input used in the triangle-free planar argument is
now replayed by Lean.  The two theorems below deliberately expose the exact
finite hypotheses: the planar structural induction and its arbitrary-length
reset step remain separate results.
-/

theorem pairFive_endpoint_layer
    {m n : PairFiveMask} (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    (hkind : 3 ≤ (pairFiveKind m n).val) :
    HamiltonConnectedOn (PairFiveStates m n) PairFiveAdjacent :=
  pairFive_hamiltonConnected hm hn hkind

theorem pairFive_cycle_layer
    {m n : PairFiveMask} (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    {s t : PairFiveState} (hs : s ∈ PairFiveStates m n)
    (ht : t ∈ PairFiveStates m n) (hst : PairFiveAdjacent s t) :
    HamiltonCycleOn (PairFiveStates m n) PairFiveAdjacent :=
  pairFive_hamiltonCycle hm hn hs ht hst

theorem pairFive_edge_cycle_layer
    {m n : PairFiveMask} (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    {s t : PairFiveState} (hs : s ∈ PairFiveStates m n)
    (ht : t ∈ PairFiveStates m n) (hst : PairFiveAdjacent s t) :
    PairFiveCycleThrough m n s t :=
  pairFive_cycle_through hm hn hs ht hst

theorem pairFive_interface_exit
    {m n m' n' : PairFiveMask}
    (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    (hm' : pairFiveSmall m') (hn' : pairFiveSmall n')
    (hallowed :
      pairFiveAllowedB m n m' n' = true)
    {s : PairFiveState} (hs : s ∈ PairFiveStates m n) :
    ∃ q, q ∈ PairFiveStates m n ∧ q ∈ PairFiveStates m' n' ∧
      PairFiveAdjacent s q := by
  rcases pairFive_small_mask_index m hm with ⟨i, rfl⟩
  rcases pairFive_small_mask_index n hn with ⟨j, rfl⟩
  rcases pairFive_small_mask_index m' hm' with ⟨i', rfl⟩
  rcases pairFive_small_mask_index n' hn' with ⟨j', rfl⟩
  apply pairFive_interface_exit_of_certificate
  exact pairFive_interface_exit_indexed i j i' j' hallowed s hs

theorem pairFive_interface_path
    {m n m' n' : PairFiveMask}
    (hm : pairFiveSmall m) (hn : pairFiveSmall n)
    (hm' : pairFiveSmall m') (hn' : pairFiveSmall n')
    (hallowed :
      pairFiveAllowedB m n m' n' = true)
    {s : PairFiveState} (hs : s ∈ PairFiveStates m n) :
    ∃ q, q ∈ PairFiveStates m n ∧ q ∈ PairFiveStates m' n' ∧
      PairFiveAdjacent s q ∧
      HamiltonPathOn (PairFiveStates m n) PairFiveAdjacent s q := by
  rcases pairFive_interface_exit hm hn hm' hn' hallowed hs with
    ⟨q, hq, hq', hsq⟩
  exact ⟨q, hq, hq', hsq, pairFive_hamiltonPath_of_edge hm hn hs hq hsq⟩

end PlanarRecoloring
