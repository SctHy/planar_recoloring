import PlanarRecoloring.BridgeLists

namespace PlanarRecoloring

/-- A nonempty list has different consecutive values, including the edge from
its last value back to its first. -/
def CyclicDifferent (xs : List α) : Prop :=
  Consecutive (· ≠ ·) xs ∧
    ∃ first last, xs.head? = some first ∧ xs.getLast? = some last ∧ last ≠ first

/-- The last-value condition used by the bridge argument is exactly the usual
endpoint inequality, when the list has a specified last value. -/
theorem endsAway_iff_of_getLast? {xs : List α} {a last : α}
    (hlast : xs.getLast? = some last) : EndsAway a xs ↔ last ≠ a := by
  induction xs with
  | nil => simp at hlast
  | cons x xs ih =>
    cases xs with
    | nil =>
      have hx : x = last := by simpa using hlast
      subst last
      simp [EndsAway]
    | cons y ys =>
      have htail : (y :: ys).getLast? = some last := by simpa using hlast
      simpa [EndsAway] using ih htail

/-- Cyclic choice for an arbitrary number of lists, when one list has a third
choice.  This is the first case in the proof of `lem:list-cycle` in `main.tex`.
The number of lists only needs to be at least two for this case. -/
theorem cyclic_colours_of_three [DecidableEq α]
    (sets : List (α → Prop)) (hlen : 2 ≤ sets.length)
    (hsets : ∀ S ∈ sets, AtLeastTwo S)
    (hspecial : ∃ S, S ∈ sets ∧ AtLeastThree S) :
    ∃ xs, Supports sets xs ∧ CyclicDifferent xs := by
  cases sets with
  | nil => simp at hlen
  | cons S Ss =>
    cases Ss with
    | nil => simp at hlen
    | cons T Ts =>
      rcases hspecial with ⟨U, hU, hU3⟩
      have htailsets : ∀ V ∈ T :: Ts, AtLeastTwo V := by
        intro V hV
        exact hsets V (by simp [hV])
      by_cases hUS : U = S
      · subst U
        rcases hsets T (by simp) with ⟨b, _, _, _, _⟩
        obtain ⟨ys, hys, _⟩ := backward_choice (T :: Ts) htailsets b
        cases ys with
        | nil => simp [Supports] at hys
        | cons y ys =>
          let last := (y :: ys).getLast (by simp)
          have hlast : (y :: ys).getLast? = some last :=
            List.getLast?_eq_some_getLast (by simp)
          rcases exists_avoiding_of_three hU3 y last with ⟨x, hx, hxy, hxl⟩
          rcases hys with ⟨hy, hcon, hrest⟩
          refine ⟨x :: y :: ys, ⟨hx, ⟨hxy, hcon⟩, ⟨hy, hcon, hrest⟩⟩, ?_⟩
          exact ⟨⟨hxy, hcon⟩, x, last, rfl, by simpa using hlast, hxl.symm⟩
      · have hUtail : U ∈ T :: Ts := by
          rcases (show U = S ∨ U ∈ T :: Ts by simpa only [List.mem_cons] using hU) with heq | hmem
          · exact False.elim (hUS heq)
          · exact hmem
        rcases hsets S (by simp) with ⟨x, _, _, hx, _⟩
        obtain ⟨ys, hys, hstart, hend⟩ :=
          bridge_colours_lists (T :: Ts) htailsets ⟨U, hUtail, hU3⟩ x x
        cases ys with
        | nil => simp [Supports] at hys
        | cons y ys =>
          have hyx : y ≠ x := hstart
          rcases hys with ⟨hy, hcon, hrest⟩
          let last := (y :: ys).getLast (by simp)
          have hlast : (y :: ys).getLast? = some last :=
            List.getLast?_eq_some_getLast (by simp)
          have hlx : last ≠ x := (endsAway_iff_of_getLast? hlast).mp hend
          refine ⟨x :: y :: ys, ⟨hx, ⟨hyx.symm, hcon⟩, ⟨hy, hcon, hrest⟩⟩, ?_⟩
          exact ⟨⟨hyx.symm, hcon⟩, x, last, rfl, by simpa using hlast, hlx⟩

end PlanarRecoloring
