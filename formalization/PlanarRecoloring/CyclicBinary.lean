import PlanarRecoloring.CyclicLists
import PlanarRecoloring.Fibre

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

private theorem cyclic_consecutive_prefix {α : Type u} {r : α → α → Prop}
    (xs ys : List α) (h : Consecutive r (xs ++ ys)) :
    Consecutive r xs := by
  induction xs with
  | nil => trivial
  | cons x xs ih =>
      cases xs with
      | nil => trivial
      | cons y ys' => exact ⟨h.1, ih h.2⟩

private theorem cyclic_consecutive_suffix {α : Type u} {r : α → α → Prop}
    (xs ys : List α) (h : Consecutive r (xs ++ ys)) :
    Consecutive r ys := by
  induction xs with
  | nil => exact h
  | cons x xs ih =>
      cases xs with
      | nil =>
          cases ys with
          | nil => trivial
          | cons y ys' => exact h.2
      | cons y ys' =>
          apply ih
          exact h.2

private theorem supports_split_append
    {α : Type u}
    {As Bs : List (α → Prop)} {xs : List α}
    (h : Supports (As ++ Bs) xs) :
    ∃ ys zs, xs = ys ++ zs ∧ Supports As ys ∧ Supports Bs zs := by
  induction As generalizing xs with
  | nil =>
      exact ⟨[], xs, by simp, by simp [Supports], by simpa using h⟩
  | cons A As ih =>
      cases xs with
      | nil => simp [Supports] at h
      | cons x xs =>
          have h' : A x ∧ Consecutive (· ≠ ·) (x :: xs) ∧
              Supports (As ++ Bs) xs := by
            simpa [List.cons_append, Supports] using h
          rcases ih h'.2.2 with ⟨ys, zs, hsplit, hys, hzs⟩
          refine ⟨x :: ys, zs, ?_, ?_, hzs⟩
          · simp [hsplit]
          · have hfull : Consecutive (· ≠ ·) ((x :: ys) ++ zs) := by
              simpa [hsplit] using h'.2.1
            exact ⟨h'.1, cyclic_consecutive_prefix (x :: ys) zs hfull, hys⟩

private theorem supports_append_of_consecutive
    {α : Type u}
    {As Bs : List (α → Prop)} {ys zs : List α}
    (hys : Supports As ys) (hzs : Supports Bs zs)
    (hcon : Consecutive (· ≠ ·) (ys ++ zs)) :
    Supports (As ++ Bs) (ys ++ zs) := by
  induction As generalizing ys with
  | nil =>
      cases ys with
      | nil => simpa using hzs
      | cons y ys => simp [Supports] at hys
  | cons A As ih =>
      cases ys with
      | nil => simp [Supports] at hys
      | cons y ys =>
          have hys' : A y ∧ Consecutive (· ≠ ·) (y :: ys) ∧
              Supports As ys := by
            simpa [Supports] using hys
          have htail : Consecutive (· ≠ ·) (ys ++ zs) :=
            cyclic_consecutive_suffix [y] (ys ++ zs) (by
              simpa [List.cons_append] using hcon)
          have hrest := ih hys'.2.2 htail
          have hfull : Consecutive (· ≠ ·) ((y :: ys) ++ zs) := by
            simpa [List.cons_append] using hcon
          exact ⟨hys'.1, hfull, hrest⟩

private theorem consecutive_boundary
    {α : Type u} {r : α → α → Prop} {xs ys : List α}
    (hx : xs ≠ []) (hy : ys ≠ [])
    (hcon : Consecutive r (xs ++ ys)) :
    ∃ a b, xs.getLast? = some a ∧ ys.head? = some b ∧ r a b := by
  cases xs with
  | nil => exact False.elim (hx rfl)
  | cons x xs =>
      cases xs with
      | nil =>
          cases ys with
          | nil => exact False.elim (hy rfl)
          | cons y ys =>
              exact ⟨x, y, by simp, by simp, hcon.1⟩
      | cons x' xs =>
          rcases consecutive_boundary (xs := x' :: xs) (ys := ys)
            (by simp) hy hcon.2 with ⟨a, b, ha, hb, hab⟩
          exact ⟨a, b, by simpa using ha, hb, hab⟩

private theorem cyclic_consecutive_rotate
    {α : Type u} {xs ys : List α}
    (hx : xs ≠ []) (hy : ys ≠ [])
    (hcon : Consecutive (· ≠ ·) (xs ++ ys))
    (hclose : ∃ a b, (xs ++ ys).head? = some a ∧
      (xs ++ ys).getLast? = some b ∧ b ≠ a) :
    Consecutive (· ≠ ·) (ys ++ xs) := by
  rcases hclose with ⟨a, b, ha, hb, hab⟩
  have hxs : Consecutive (· ≠ ·) xs :=
    cyclic_consecutive_prefix xs ys hcon
  have hys : Consecutive (· ≠ ·) ys :=
    cyclic_consecutive_suffix xs ys hcon
  have hfirst : xs.head? = some a := by
    rw [head_append_of_ne_nil hx] at ha
    exact ha
  have hlast : ys.getLast? = some b := by
    rw [getLast_append_of_ne_nil hy] at hb
    exact hb
  exact consecutive_append hys hxs hy hx hlast hfirst hab

private theorem cyclic_different_rotate
    {α : Type u} {xs ys : List α}
    (hx : xs ≠ []) (hy : ys ≠ [])
    (hcyc : CyclicDifferent (xs ++ ys)) :
    CyclicDifferent (ys ++ xs) := by
  rcases hcyc with ⟨hcon, a, b, ha, hb, hab⟩
  have hrot := cyclic_consecutive_rotate hx hy hcon ⟨a, b, ha, hb, hab⟩
  rcases consecutive_boundary hx hy hcon with ⟨c, d, hc, hd, hcd⟩
  have hfirst : (ys ++ xs).head? = some d := by
    rw [head_append_of_ne_nil hy, hd]
  have hlast : (ys ++ xs).getLast? = some c := by
    rw [getLast_append_of_ne_nil hx, hc]
  exact ⟨hrot, d, c, hfirst, hlast, hcd⟩

/-- A heterogeneous binary pair can occur after an arbitrary prefix: rotate the
cycle at that pair, apply the explicit cut construction, and rotate the
supported choices back. -/
theorem cyclic_colours_binary_of_split [DecidableEq α]
    {pre : List (α → Prop)} {S T : α → Prop}
    {post : List (α → Prop)}
    (hST : ∃ x, S x ∧ ¬ T x)
    (hsets : ∀ U ∈ pre ++ S :: T :: post, AtLeastTwo U) :
    ∃ xs, Supports (pre ++ S :: T :: post) xs ∧ CyclicDifferent xs := by
  have htailsets : ∀ U ∈ T :: post ++ pre, AtLeastTwo U := by
    intro U hU
    apply hsets U
    simp only [List.mem_append, List.mem_cons] at hU ⊢
    rcases hU with hU | hU
    · exact Or.inr (Or.inr hU)
    · exact Or.inl hU
  obtain ⟨rot, hrot, hrotcyc⟩ :=
    cyclic_colours_binary_of_first_diff (Ts := post ++ pre) hST htailsets
  cases pre with
  | nil =>
      have hrot' : Supports (S :: T :: post) rot := by
        simpa [List.append] using hrot
      exact ⟨rot, hrot', by simpa [List.append] using hrotcyc⟩
  | cons p pre =>
      rcases supports_split_append (As := S :: T :: post) (Bs := p :: pre)
        (by simpa [List.append_assoc] using hrot) with
        ⟨ys, zs, hsplit, hys, hzs⟩
      have hcyc : CyclicDifferent (ys ++ zs) := by
        simpa [← hsplit] using hrotcyc
      have hysne : ys ≠ [] := Supports.nonempty hys (by simp)
      have hzsne : zs ≠ [] := Supports.nonempty hzs (by simp)
      have hrotSupport : Supports ((p :: pre) ++ (S :: T :: post))
          (zs ++ ys) := by
        exact supports_append_of_consecutive hzs hys
          (cyclic_consecutive_rotate hysne hzsne hcyc.1 hcyc.2)
      have hrotCyclic : CyclicDifferent (zs ++ ys) :=
        cyclic_different_rotate hysne hzsne hcyc
      refine ⟨zs ++ ys, ?_, hrotCyclic⟩
      simpa [List.append_assoc] using hrotSupport

/-- The same rotation argument handles a heterogeneous pair across the cut of
the written list (the last set differs from the first set). -/
theorem cyclic_colours_binary_of_boundary_diff [DecidableEq α]
    {S T : α → Prop} {mid : List (α → Prop)}
    (hST : ∃ x, S x ∧ ¬ T x)
    (hsets : ∀ U ∈ T :: mid ++ [S], AtLeastTwo U) :
    ∃ xs, Supports (T :: mid ++ [S]) xs ∧ CyclicDifferent xs := by
  have htailsets : ∀ U ∈ T :: mid, AtLeastTwo U := by
    intro U hU
    apply hsets U
    simp only [List.mem_cons, List.mem_append] at hU ⊢
    rcases hU with hU | hU
    · exact Or.inl (Or.inl hU)
    · exact Or.inl (Or.inr hU)
  obtain ⟨rot, hrot, hrotcyc⟩ :=
    cyclic_colours_binary_of_first_diff (Ts := mid) hST htailsets
  rcases supports_split_append (As := [S]) (Bs := T :: mid)
      (by simpa [List.append_assoc] using hrot) with
      ⟨ys, zs, hsplit, hys, hzs⟩
  have hcyc : CyclicDifferent (ys ++ zs) := by
    simpa [← hsplit] using hrotcyc
  have hysne : ys ≠ [] := Supports.nonempty hys (by simp)
  have hzsne : zs ≠ [] := Supports.nonempty hzs (by simp)
  have hsupport : Supports ((T :: mid) ++ [S]) (zs ++ ys) := by
    exact supports_append_of_consecutive hzs hys
      (cyclic_consecutive_rotate hysne hzsne hcyc.1 hcyc.2)
  have hcyclic : CyclicDifferent (zs ++ ys) :=
    cyclic_different_rotate hysne hzsne hcyc
  exact ⟨zs ++ ys, by simpa [List.append_assoc] using hsupport, hcyclic⟩

end PlanarRecoloring
