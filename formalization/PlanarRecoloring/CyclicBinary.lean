import PlanarRecoloring.CyclicLists

namespace PlanarRecoloring

/-- A predicate is represented exactly by two distinct witnesses.  This is the
binary case in the list-cycle lemma. -/
def ExactlyTwo (S : α → Prop) (a b : α) : Prop :=
  a ≠ b ∧ ∀ x, S x ↔ x = a ∨ x = b

theorem exactlyTwo_of_atLeastTwo_of_not_three [DecidableEq α]
    {S : α → Prop} (h₂ : AtLeastTwo S) (h₃ : ¬ AtLeastThree S) :
    ∃ a b, ExactlyTwo S a b := by
  rcases h₂ with ⟨a, b, hab, ha, hb⟩
  refine ⟨a, b, hab, ?_⟩
  intro x
  constructor
  · intro hx
    by_cases hxa : x = a
    · exact Or.inl hxa
    · by_cases hxb : x = b
      · exact Or.inr hxb
      · exfalso
        apply h₃
        exact ⟨a, b, x, hab, fun h => hxa h.symm, fun h => hxb h.symm,
          ha, hb, hx⟩
  · intro hx
    rcases hx with rfl | rfl
    · exact ha
    · exact hb

theorem ExactlyTwo.swap {S : α → Prop} {a b : α}
    (h : ExactlyTwo S a b) : ExactlyTwo S b a := by
  rcases h with ⟨hab, hS⟩
  refine ⟨hab.symm, ?_⟩
  intro x
  rw [hS]
  constructor
  · intro hx
    rcases hx with rfl | rfl
    · exact Or.inr rfl
    · exact Or.inl rfl
  · intro hx
    rcases hx with rfl | rfl
    · exact Or.inr rfl
    · exact Or.inl rfl

def Alternating (a b : α) : Nat → List α
  | 0 => []
  | n + 1 => a :: Alternating b a n

theorem alternating_consecutive [DecidableEq α]
    : ∀ n {a b : α}, a ≠ b →
      Consecutive (· ≠ ·) (Alternating a b n) := by
  intro n
  induction n with
  | zero => intro a b hab; simp [Alternating, Consecutive]
  | succ n ih =>
      intro a b hab
      cases n with
      | zero => simp [Alternating, Consecutive]
      | succ n =>
          simp only [Alternating, Consecutive]
          exact ⟨hab, ih hab.symm⟩

theorem alternating_supports [DecidableEq α]
    : ∀ n {a b : α}, ExactlyTwo S a b →
      Supports (List.replicate n S) (Alternating a b n) := by
  intro n
  induction n with
  | zero => intro a b h; simp [Alternating, Supports]
  | succ n ih =>
      intro a b h
      cases n with
      | zero =>
          rcases h with ⟨hab, hS⟩
          have ha : S a := (hS a).2 (Or.inl rfl)
          simp [Alternating, Supports, Consecutive, ha]
      | succ n =>
          rcases h with ⟨hab, hS⟩
          have ha : S a := (hS a).2 (Or.inl rfl)
          have hswap : ExactlyTwo S b a := by
            refine ⟨hab.symm, ?_⟩
            intro x
            rw [hS]
            constructor <;> intro hx
            · rcases hx with rfl | rfl <;> simp
            · rcases hx with rfl | rfl <;> simp
          have htail := ih hswap
          simp only [Alternating, List.replicate_succ, Supports]
          exact ⟨ha, ⟨hab, htail.consecutive⟩, htail⟩

theorem alternating_last_even [DecidableEq α]
    {a b : α} (_hab : a ≠ b) :
    ∀ k, (Alternating a b (2 * k + 2)).getLast? = some b := by
  intro k
  induction k with
  | zero => simp [Alternating]
  | succ k ih =>
      have hidx : 2 * (Nat.succ k) + 2 = Nat.succ (Nat.succ (2 * k + 2)) := by omega
      rw [hidx]
      simp only [Alternating]
      exact ih

/-- The all-identical binary case of the cyclic bridge-colour lemma.  An even
number of copies can be solved by alternation. -/
theorem cyclic_colours_binary_even [DecidableEq α]
    {S : α → Prop} {a b : α} (h : ExactlyTwo S a b) (k : Nat) :
    ∃ xs, Supports (List.replicate (2 * k + 2) S) xs ∧
      CyclicDifferent xs := by
  refine ⟨Alternating a b (2 * k + 2), alternating_supports (2 * k + 2) h, ?_⟩
  refine ⟨alternating_consecutive (2 * k + 2) h.1, a, b, ?_, alternating_last_even h.1 k, h.1.symm⟩
  simp [Alternating]

end PlanarRecoloring
