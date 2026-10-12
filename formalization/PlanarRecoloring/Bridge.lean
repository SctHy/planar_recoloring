import Std

namespace PlanarRecoloring

/-!
## The bridge-colour argument

The paper's `bridge-colours` lemma is a greedy path argument.  The following
version isolates its nontrivial local step: three consecutive available lists,
with the middle list containing three distinct colours.  It is stated for
predicates rather than a particular finite-set implementation, so it remains
usable for the lists arising from graph colourings.
-/

def AtLeastTwo (S : α → Prop) : Prop :=
  ∃ x y, x ≠ y ∧ S x ∧ S y

def AtLeastThree (S : α → Prop) : Prop :=
  ∃ x y z, x ≠ y ∧ x ≠ z ∧ y ≠ z ∧ S x ∧ S y ∧ S z

theorem exists_avoiding_of_two [DecidableEq α] {S : α → Prop}
    (hS : AtLeastTwo S) (a : α) : ∃ x, S x ∧ x ≠ a := by
  rcases hS with ⟨x, y, hxy, hx, hy⟩
  by_cases hxa : x = a
  · refine ⟨y, hy, ?_⟩
    intro hya
    exact hxy (hxa.trans hya.symm)
  · exact ⟨x, hx, hxa⟩

theorem exists_avoiding_of_three [DecidableEq α] {S : α → Prop}
    (hS : AtLeastThree S) (a b : α) :
    ∃ x, S x ∧ x ≠ a ∧ x ≠ b := by
  rcases hS with ⟨x, y, z, hxy, hxz, hyz, hx, hy, hz⟩
  by_cases hxa : x = a
  · by_cases hya : y = a
    · exact False.elim (hxy (hxa.trans hya.symm))
    · by_cases hyb : y = b
      · refine ⟨z, hz, ?_, ?_⟩
        · intro hza
          exact hxz (hxa.trans hza.symm)
        · intro hzb
          exact hyz (hyb.trans hzb.symm)
      · exact ⟨y, hy, hya, hyb⟩
  · by_cases hxb : x = b
    · by_cases hya : y = a
      · by_cases hyb : y = b
        · exact False.elim (hxy (hxb.trans hyb.symm))
        · refine ⟨z, hz, ?_, ?_⟩
          · intro hza
            exact hyz (hya.trans hza.symm)
          · intro hzb
            exact hxz (hxb.trans hzb.symm)
      · refine ⟨y, hy, hya, ?_⟩
        intro hyb
        exact hxy (hxb.trans hyb.symm)
    · exact ⟨x, hx, hxa, hxb⟩

theorem bridge_colours_three [DecidableEq α]
    {S₀ S₁ S₂ : α → Prop}
    (h₀ : AtLeastTwo S₀) (h₁ : AtLeastThree S₁) (h₂ : AtLeastTwo S₂)
    (a b : α) :
    ∃ x₀ x₁ x₂,
      S₀ x₀ ∧ S₁ x₁ ∧ S₂ x₂ ∧
      x₀ ≠ a ∧ x₀ ≠ x₁ ∧ x₁ ≠ x₂ ∧ x₂ ≠ b := by
  rcases exists_avoiding_of_two h₀ a with ⟨x₀, hx₀, h₀a⟩
  rcases exists_avoiding_of_two h₂ b with ⟨x₂, hx₂, h₂b⟩
  rcases exists_avoiding_of_three h₁ x₀ x₂ with
    ⟨x₁, hx₁, h₁₀, h₁₂⟩
  exact ⟨x₀, x₁, x₂, hx₀, hx₁, hx₂, h₀a, h₁₀.symm, h₁₂, h₂b⟩

/- A cyclic three-layer special case of the list-cycle selection step. -/
theorem cyclic_three_colours [DecidableEq α]
    {S₀ S₁ S₂ : α → Prop}
    (h₀ : AtLeastTwo S₀) (h₁ : AtLeastThree S₁) (h₂ : AtLeastTwo S₂) :
    ∃ x₀ x₁ x₂,
      S₀ x₀ ∧ S₁ x₁ ∧ S₂ x₂ ∧
      x₀ ≠ x₁ ∧ x₁ ≠ x₂ ∧ x₂ ≠ x₀ := by
  rcases h₀ with ⟨a, _, _, ha, _⟩
  rcases exists_avoiding_of_two h₂ a with ⟨c, hc, hca⟩
  rcases exists_avoiding_of_three h₁ a c with ⟨b, hb, hba, hbc⟩
  exact ⟨a, b, c, ha, hb, hc, hba.symm, hbc, hca⟩

end PlanarRecoloring
