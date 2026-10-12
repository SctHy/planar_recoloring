import PlanarRecoloring.FibreHamilton

/-!
# Hamilton paths in finite complete fibres

A fibre of one restored vertex is a complete graph on its available colours.
For a finite list of distinct states, the prescribed endpoints can be put at
the ends and every other state between them. This gives the path existence
used by the single-coordinate cases of the article's lifting arguments.
-/

namespace PlanarRecoloring

/-- Distinct entries in a list are adjacent under the complete-graph relation. -/
theorem consecutive_ne_of_nodup {α : Type u} {xs : List α}
    (h : xs.Nodup) : Consecutive (· ≠ ·) xs := by
  induction xs with
  | nil => trivial
  | cons x xs ih =>
    cases xs with
    | nil => trivial
    | cons y ys =>
      have hx : x ≠ y := by
        intro hxy
        exact (List.nodup_cons.mp h).1 (by simp [hxy])
      exact ⟨hx, ih (List.nodup_cons.mp h).2⟩

/-- Every pair of distinct prescribed vertices in a finite complete graph
has a Hamilton path. The supplied list is the graph's vertex enumeration. -/
theorem complete_hamiltonPathOn [DecidableEq α]
    (vertices : List α) (hnodup : vertices.Nodup)
    {s t : α} (hs : s ∈ vertices) (ht : t ∈ vertices) (hst : s ≠ t) :
    HamiltonPathOn vertices (· ≠ ·) s t := by
  let middle := vertices.filter (fun x => decide (x ≠ s ∧ x ≠ t))
  have hmiddle_mem (x : α) : x ∈ middle ↔ x ∈ vertices ∧ x ≠ s ∧ x ≠ t := by
    simp [middle, List.mem_filter]
  have hmiddle_nodup : middle.Nodup :=
    List.Nodup.sublist List.filter_sublist hnodup
  have hsnot : s ∉ middle := by
    intro h
    exact (hmiddle_mem s).mp h |>.2.1 rfl
  have htnot : t ∉ middle := by
    intro h
    exact (hmiddle_mem t).mp h |>.2.2 rfl
  have htail_nodup : (middle ++ [t]).Nodup := by
    apply List.nodup_append.mpr
    refine ⟨hmiddle_nodup, by simp, ?_⟩
    intro a ha b hb
    have hbt : b = t := by simpa using hb
    subst b
    intro hat
    exact htnot (hat ▸ ha)
  have hpath_nodup : (s :: middle ++ [t]).Nodup := by
    apply List.nodup_cons.mpr
    constructor
    · simp [hsnot, hst]
    · exact htail_nodup
  refine ⟨s :: middle ++ [t], rfl, ?_, hpath_nodup, ?_,
    consecutive_ne_of_nodup hpath_nodup⟩
  · simpa [List.cons_append] using
      (getLast_append_of_ne_nil (xs := s :: middle) (ys := [t]) (by simp))
  · intro x
    constructor
    · intro hx
      by_cases hxs : x = s
      · simp [hxs]
      by_cases hxt : x = t
      · simp [hxt]
      have hm : x ∈ middle := (hmiddle_mem x).mpr ⟨hx, hxs, hxt⟩
      simp [hm]
    · intro hx
      rcases List.mem_cons.mp hx with hxs | htail
      · exact hxs.symm ▸ hs
      · rcases List.mem_append.mp htail with hm | hlast
        · exact ((hmiddle_mem x).mp hm).1
        · have hxt : x = t := by simpa using hlast
          exact hxt ▸ ht

/-- The complete-fibre construction can be transported to any relation that
contains every unequal pair. -/
theorem complete_hamiltonPathOn_of_neq [DecidableEq α]
    (vertices : List α) (hnodup : vertices.Nodup)
    {r : α → α → Prop} (hrel : ∀ ⦃x y⦄, x ≠ y → r x y)
    {s t : α} (hs : s ∈ vertices) (ht : t ∈ vertices) (hst : s ≠ t) :
    HamiltonPathOn vertices r s t := by
  rcases complete_hamiltonPathOn vertices hnodup hs ht hst with
    ⟨path, hhead, hlast, hpathnodup, hcover, hwalk⟩
  exact ⟨path, hhead, hlast, hpathnodup, hcover,
    consecutive_mono hrel hwalk⟩

/-- Variant for relations whose completeness is known only on the supplied
vertex list. -/
theorem complete_hamiltonPathOn_of_mem [DecidableEq α]
    (vertices : List α) (hnodup : vertices.Nodup)
    {r : α → α → Prop}
    (hrel : ∀ ⦃x y⦄, x ∈ vertices → y ∈ vertices → x ≠ y → r x y)
    {s t : α} (hs : s ∈ vertices) (ht : t ∈ vertices) (hst : s ≠ t) :
    HamiltonPathOn vertices r s t := by
  rcases complete_hamiltonPathOn vertices hnodup hs ht hst with
    ⟨path, hhead, hlast, hpathnodup, hcover, hneq⟩
  have mapCon : ∀ (xs : List α),
      (∀ x, x ∈ xs → x ∈ vertices) →
      Consecutive (· ≠ ·) xs → Consecutive r xs := by
    intro xs
    induction xs with
    | nil => intro _ _; trivial
    | cons x xs ih =>
      cases xs with
      | nil => intro _ _; trivial
      | cons y ys =>
        intro hmem hcon
        exact ⟨hrel (hmem x (by simp)) (hmem y (by simp)) hcon.1,
          ih (fun z hz => hmem z (by simp [hz])) hcon.2⟩
  have hwalk : Consecutive r path :=
    mapCon path (fun x hx => (hcover x).mpr hx) hneq
  exact ⟨path, hhead, hlast, hpathnodup, hcover, hwalk⟩

end PlanarRecoloring
