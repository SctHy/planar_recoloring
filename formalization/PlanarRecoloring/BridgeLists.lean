import PlanarRecoloring.Core
import PlanarRecoloring.Bridge

namespace PlanarRecoloring

/-- A list of choices supports a list of available-colour predicates when every
entry is witnessed and consecutive choices are different. -/
def Supports : List (α → Prop) → List α → Prop
  | [], [] => True
  | S :: Ss, x :: xs => S x ∧ Consecutive (· ≠ ·) (x :: xs) ∧ Supports Ss xs
  | _, _ => False

def StartsAway (a : α) : List α → Prop
  | [] => True
  | x :: _ => x ≠ a

def EndsAway (b : α) : List α → Prop
  | [] => True
  | [x] => x ≠ b
  | _ :: xs => EndsAway b xs

/-- Given lists of predicates each having two choices, choose a supported list
whose final entry avoids a prescribed colour. -/
theorem backward_choice [DecidableEq α]
    (sets : List (α → Prop))
    (hsets : ∀ S ∈ sets, AtLeastTwo S) (b : α) :
    ∃ xs, Supports sets xs ∧ EndsAway b xs := by
  induction sets with
  | nil => exact ⟨[], trivial, trivial⟩
  | cons S Ss ih =>
    cases Ss with
    | nil =>
      rcases exists_avoiding_of_two (hsets S (by simp)) b with ⟨x, hx, hxb⟩
      exact ⟨[x], by simp [Supports, Consecutive, hx], by simpa [EndsAway] using hxb⟩
    | cons T Ts =>
      have htail : ∀ U ∈ T :: Ts, AtLeastTwo U := by
        intro U hU
        exact hsets U (by simp [hU])
      obtain ⟨ys, hys, hends⟩ := ih htail
      cases ys with
      | nil => simp [Supports] at hys
      | cons y ys =>
        rcases exists_avoiding_of_two (hsets S (by simp)) y with ⟨x, hx, hxy⟩
        refine ⟨x :: y :: ys, ?_, ?_⟩
        · rcases hys with ⟨hy, hcon, htail⟩
          exact ⟨hx, ⟨hxy, hcon⟩, ⟨hy, hcon, htail⟩⟩
        · simpa [EndsAway] using hends

/-- Arbitrary-length bridge-colour selection.  Every list has at least two
colours, and one list has at least three; the first and last choices also avoid
specified endpoint colours. -/
theorem bridge_colours_lists [DecidableEq α]
    (sets : List (α → Prop))
    (hsets : ∀ S ∈ sets, AtLeastTwo S)
    (hspecial : ∃ S, S ∈ sets ∧ AtLeastThree S)
    (a b : α) :
    ∃ xs, Supports sets xs ∧ StartsAway a xs ∧ EndsAway b xs := by
  induction sets generalizing a b with
  | nil =>
      rcases hspecial with ⟨S, hS, _⟩
      simp at hS
  | cons S Ss ih =>
      rcases hspecial with ⟨U, hU, hU3⟩
      by_cases hhead : U = S
      · subst U
        cases Ss with
        | nil =>
            rcases exists_avoiding_of_three hU3 a b with ⟨x, hx, hxa, hxb⟩
            exact ⟨[x], by simp [Supports, Consecutive, hx],
              by simpa [StartsAway] using hxa, by simpa [EndsAway] using hxb⟩
        | cons T Ts =>
            have htail : ∀ V ∈ T :: Ts, AtLeastTwo V := by
              intro V hV
              exact hsets V (by simp [hV])
            obtain ⟨ys, hys, hends⟩ := backward_choice (T :: Ts) htail b
            cases ys with
            | nil => simp [Supports] at hys
            | cons y ys =>
                rcases exists_avoiding_of_three hU3 a y with ⟨x, hx, hxa, hxy⟩
                refine ⟨x :: y :: ys, ?_, ?_, ?_⟩
                · rcases hys with ⟨hy, hcon, htail⟩
                  exact ⟨hx, ⟨hxy, hcon⟩, ⟨hy, hcon, htail⟩⟩
                · exact hxa
                · simpa [EndsAway] using hends
      · have hUtail : U ∈ Ss := by
          rcases (show U = S ∨ U ∈ Ss by simpa only [List.mem_cons] using hU) with hUS | hUS
          · exact False.elim (hhead hUS)
          · exact hUS
        cases Ss with
        | nil => simp at hUtail
        | cons T Ts =>
          have hspecial_tail : ∃ V, V ∈ T :: Ts ∧ AtLeastThree V := ⟨U, by simpa using hUtail, hU3⟩
          have hsets_tail : ∀ V ∈ T :: Ts, AtLeastTwo V := by
            intro V hV
            exact hsets V (by simp [hV])
          rcases exists_avoiding_of_two (hsets S (by simp)) a with ⟨x, hx, hxa⟩
          obtain ⟨ys, hys, hysa, hends⟩ := ih hsets_tail hspecial_tail x b
          refine ⟨x :: ys, ?_, ?_, ?_⟩
          · cases ys with
            | nil =>
                have hbad : Supports (T :: Ts) [] := hys
                simp [Supports] at hbad
            | cons y ys =>
                have hys' : T y ∧ Consecutive (· ≠ ·) (y :: ys) ∧ Supports Ts ys := by
                  simpa [Supports] using hys
                rcases hys' with ⟨hy, hcon, htail⟩
                have hyx : y ≠ x := by simpa [StartsAway] using hysa
                exact ⟨hx, ⟨Ne.symm hyx, hcon⟩, ⟨hy, hcon, htail⟩⟩
          · exact hxa
          · cases ys with
            | nil =>
                have hbad : Supports (T :: Ts) [] := hys
                simp [Supports] at hbad
            | cons y ys => simpa [EndsAway] using hends

end PlanarRecoloring
