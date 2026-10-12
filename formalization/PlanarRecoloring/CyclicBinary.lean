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

theorem alternating_last_odd [DecidableEq α]
    {a b : α} (_hab : a ≠ b) :
    ∀ k, (Alternating a b (2 * k + 1)).getLast? = some a := by
  intro k
  induction k with
  | zero => simp [Alternating]
  | succ k ih =>
      have hidx : 2 * (Nat.succ k) + 1 = Nat.succ (Nat.succ (2 * k + 1)) := by omega
      rw [hidx]
      simp only [Alternating]
      exact ih

/- The support list is forced once its first colour is fixed.  This is the
   elementary alternating argument used to rule out odd binary cycles. -/
theorem supports_exactlyTwo_of_head [DecidableEq α] :
    ∀ n {S : α → Prop} {a b : α}, ExactlyTwo S a b →
      ∀ {xs : List α}, Supports (List.replicate n S) xs →
        xs.head? = some a → xs = Alternating a b n := by
  intro n
  induction n with
  | zero =>
      intro S a b h xs hxs hhead
      cases xs with
      | nil => rfl
      | cons x xs => simp [Supports] at hxs
  | succ n ih =>
      intro S a b h xs hxs hhead
      cases xs with
      | nil => simp [Supports] at hxs
      | cons x xs =>
          have hx : x = a := by simpa using hhead
          subst x
          cases xs with
          | nil =>
              have hlen := Supports.length_eq hxs
              have hn : n = 0 := by
                simp at hlen
                omega
              subst n
              rfl
          | cons y ys =>
              have hxs' : S a ∧
                  Consecutive (· ≠ ·) (a :: y :: ys) ∧
                  Supports (List.replicate n S) (y :: ys) := by
                simpa [List.replicate_succ, Supports] using hxs
              have hay : a ≠ y := hxs'.2.1.1
              have hya : y ≠ a := Ne.symm hay
              have hy : S y := by
                cases n with
                | zero =>
                    have hbad : Supports ([] : List (α → Prop)) (y :: ys) := hxs'.2.2
                    simp [Supports] at hbad
                | succ n =>
                    have hdecomp : S y ∧
                        Consecutive (· ≠ ·) (y :: ys) ∧
                        Supports (List.replicate n S) ys := by
                      simpa [List.replicate_succ, Supports] using hxs'.2.2
                    exact hdecomp.1
              have hyb : y = b := by
                rcases (h.2 y).mp hy with hya' | hyb'
                · exact False.elim (hya hya')
                · exact hyb'
              subst y
              have htailhead : (b :: ys).head? = some b := rfl
              have hswap : ExactlyTwo S b a := h.swap
              have htail := ih hswap hxs'.2.2 htailhead
              simpa [Alternating] using htail

/-- An odd number of identical binary layers cannot satisfy the cyclic
    consecutive-difference condition. -/
theorem cyclic_colours_binary_odd_impossible [DecidableEq α]
    {S : α → Prop} {a b : α} (h : ExactlyTwo S a b) (k : Nat) :
    ¬ ∃ xs, Supports (List.replicate (2 * k + 1) S) xs ∧
      CyclicDifferent xs := by
  rintro ⟨xs, hxs, hcyc⟩
  rcases hcyc with ⟨hcon, first, last, hfirst, hlast, hclose⟩
  have hshape_of_a : first = a → xs = Alternating a b (2 * k + 1) := by
    intro hfa
    subst first
    exact supports_exactlyTwo_of_head (2 * k + 1) h hxs hfirst
  have hshape_of_b : first = b → xs = Alternating b a (2 * k + 1) := by
    intro hfb
    subst first
    exact supports_exactlyTwo_of_head (2 * k + 1) h.swap hxs hfirst
  have hfirst_mem : S first := by
    rw [List.head?_eq_some_iff] at hfirst
    rcases hfirst with ⟨tail, htail⟩
    subst xs
    have hdecomp : S first ∧
        Consecutive (· ≠ ·) (first :: tail) ∧
        Supports (List.replicate (2 * k) S) tail := by
      simpa [List.replicate_succ, Supports] using hxs
    exact hdecomp.1
  rcases (h.2 first).mp hfirst_mem with hfa | hfb
  · have hshape := hshape_of_a hfa
    subst xs
    have hlast' := alternating_last_odd h.1 k
    rw [hlast'] at hlast
    have hla : a = last := Option.some.inj hlast
    exact hclose (hla.symm.trans hfa.symm)
  · have hshape := hshape_of_b hfb
    subst xs
    have hlast' := alternating_last_odd h.1.symm k
    rw [hlast'] at hlast
    have hlb : b = last := Option.some.inj hlast
    exact hclose (hlb.symm.trans hfb.symm)

/-- The all-identical binary case of the cyclic bridge-colour lemma.  An even
number of copies can be solved by alternation. -/
theorem cyclic_colours_binary_even [DecidableEq α]
    {S : α → Prop} {a b : α} (h : ExactlyTwo S a b) (k : Nat) :
    ∃ xs, Supports (List.replicate (2 * k + 2) S) xs ∧
      CyclicDifferent xs := by
  refine ⟨Alternating a b (2 * k + 2), alternating_supports (2 * k + 2) h, ?_⟩
  refine ⟨alternating_consecutive (2 * k + 2) h.1, a, b, ?_, alternating_last_even h.1 k, h.1.symm⟩
  simp [Alternating]

/-!
The remaining binary case in the list-cycle lemma is heterogeneous: at least
one pair of consecutive layers has different available sets.  The following
lemma isolates the constructive step used after cutting the cycle at such a
pair.  The witness `x` is available in the first layer but not in the second;
we choose the rest backwards so that its final value also avoids `x`.  Since
`x` is absent from the second layer, the first bridge is automatically legal.

This formulation deliberately keeps the cut explicit.  A later permutation or
rotation lemma can apply it to an arbitrary list containing a heterogeneous
adjacent pair without duplicating the colour-choice argument.
-/
theorem cyclic_colours_binary_of_first_diff [DecidableEq α]
    {S T : α → Prop} {Ts : List (α → Prop)}
    (hST : ∃ x, S x ∧ ¬ T x)
    (hsets : ∀ U ∈ T :: Ts, AtLeastTwo U) :
    ∃ xs, Supports (S :: T :: Ts) xs ∧ CyclicDifferent xs := by
  rcases hST with ⟨x, hxS, hxT⟩
  obtain ⟨ys, hys, hends⟩ := backward_choice (T :: Ts) hsets x
  cases ys with
  | nil =>
      simp [Supports] at hys
  | cons y ys =>
      have hTy : T y := by
        simpa [Supports] using hys |>.1
      have hyx : y ≠ x := by
        intro hy
        apply hxT
        simpa [hy] using hTy
      have hcon : Consecutive (· ≠ ·) (y :: ys) := hys.consecutive
      let last := (y :: ys).getLast (by simp)
      have hlast : (y :: ys).getLast? = some last :=
        List.getLast?_eq_some_getLast (by simp)
      have hclose : last ≠ x :=
        (endsAway_iff_of_getLast? hlast).mp hends
      refine ⟨x :: y :: ys, ?_, ?_⟩
      · exact ⟨hxS, ⟨hyx.symm, hcon⟩, hys⟩
      · exact ⟨⟨hyx.symm, hcon⟩, x, last, rfl, by simpa using hlast, hclose⟩

/- A forward counterpart is useful when the heterogeneous pair supplies a
colour in the second layer but not the first.  The head value is fixed and
each subsequent layer is entered by avoiding the preceding value. -/
theorem forward_choice_of_head [DecidableEq α]
    {S : α → Prop} {Ss : List (α → Prop)} {a : α}
    (ha : S a) (hsets : ∀ U ∈ S :: Ss, AtLeastTwo U) :
    ∃ xs, Supports (S :: Ss) xs ∧ xs.head? = some a := by
  induction Ss generalizing S a with
  | nil =>
      exact ⟨[a], by simp [Supports, Consecutive, ha], rfl⟩
  | cons T Ts ih =>
      have hT : AtLeastTwo T := hsets T (by simp)
      rcases exists_avoiding_of_two hT a with ⟨b, hb, hba⟩
      have htail : ∀ U ∈ T :: Ts, AtLeastTwo U := by
        intro U hU
        exact hsets U (by simp [hU])
      obtain ⟨ys, hys, hhead⟩ := ih (S := T) (a := b) hb htail
      cases ys with
      | nil => simp [Supports] at hys
      | cons y ys =>
          have hy : y = b := by simpa using hhead
          subst y
          refine ⟨a :: b :: ys, ?_, rfl⟩
          rcases hys with ⟨hb', hcon, hrest⟩
          exact ⟨ha, ⟨hba.symm, hcon⟩, ⟨hb', hcon, hrest⟩⟩

/-- If the first two layers differ, either orientation of their difference
gives a cyclic choice.  This removes the orientation restriction from
`cyclic_colours_binary_of_first_diff`. -/
theorem cyclic_colours_binary_of_adjacent_diff [DecidableEq α]
    {S T : α → Prop} {Ts : List (α → Prop)}
    (hST : S ≠ T)
    (hsets : ∀ U ∈ S :: T :: Ts, AtLeastTwo U) :
    ∃ xs, Supports (S :: T :: Ts) xs ∧ CyclicDifferent xs := by
  have hdiff : (∃ x, S x ∧ ¬ T x) ∨ (∃ x, T x ∧ ¬ S x) := by
    by_cases hleft : ∃ x, S x ∧ ¬ T x
    · exact Or.inl hleft
    by_cases hright : ∃ x, T x ∧ ¬ S x
    · exact Or.inr hright
    exfalso
    apply hST
    funext x
    apply propext
    constructor
    · intro hx
      by_cases htx : T x
      · exact htx
      · exact False.elim (hleft ⟨x, hx, htx⟩)
    · intro htx
      by_cases hsx : S x
      · exact hsx
      · exact False.elim (hright ⟨x, htx, hsx⟩)
  rcases hdiff with hleft | hright
  · exact cyclic_colours_binary_of_first_diff hleft (by
      intro U hU
      exact hsets U (by simp [hU]))
  · rcases hright with ⟨x, hxT, hxS⟩
    have htail : ∀ U ∈ T :: Ts, AtLeastTwo U := by
      intro U hU
      exact hsets U (by simp [hU])
    obtain ⟨ys, hys, hhead⟩ :=
      forward_choice_of_head hxT htail
    cases ys with
    | nil => simp [Supports] at hys
    | cons y ys =>
        have hy : y = x := by simpa using hhead
        subst y
        have hcon : Consecutive (· ≠ ·) (x :: ys) := hys.consecutive
        let last := (x :: ys).getLast (by simp)
        have hlast : (x :: ys).getLast? = some last :=
          List.getLast?_eq_some_getLast (by simp)
        rcases hsets S (by simp) with ⟨a, b, hab, ha, hb⟩
        by_cases hax : a = last
        · refine ⟨b :: x :: ys, ?_, ?_⟩
          · exact ⟨hb, ⟨by
              intro hbx
              apply hxS
              rw [← hbx]
              exact hb, hcon⟩, hys⟩
          · have hclose : last ≠ b := by
              intro hlb
              apply hab
              exact hax.trans hlb
            exact ⟨⟨by
              intro hbx
              apply hxS
              rw [← hbx]
              exact hb, hcon⟩, b, last, rfl,
              by simpa using hlast, hclose⟩
        · refine ⟨a :: x :: ys, ?_, ?_⟩
          · exact ⟨ha, ⟨by
              intro hax'
              apply hxS
              rw [← hax']
              exact ha, hcon⟩, hys⟩
          · exact ⟨⟨by
              intro hax'
              apply hxS
              rw [← hax']
              exact ha, hcon⟩, a, last, rfl, by simpa using hlast,
              by intro hla; exact hax hla.symm⟩

end PlanarRecoloring
