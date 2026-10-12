import PlanarRecoloring.General
import PlanarRecoloring.Hamilton

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

def HamiltonConnectedOn (vertices : List α) (r : α → α → Prop) : Prop :=
  ∀ s t, s ∈ vertices → t ∈ vertices → s ≠ t →
    HamiltonPathOn vertices r s t

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

end PlanarRecoloring
